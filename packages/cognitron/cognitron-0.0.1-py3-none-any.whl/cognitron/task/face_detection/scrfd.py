# -*- coding: utf-8 -*-

# this whole file is ported from:
# https://github.com/deepinsight/insightface/tree/master/detection/scrfd

# @Organization  : insightface.ai
# @Author        : Jia Guo
# @Time          : 2021-05-04
# @Function      :

import numpy as np
import os

from cognitron.core import hub
from cognitron.pipeline.accelerator import Pipeline
from cognitron.pipeline.device import Device
from cognitron.package import lazy_import

from .options import Options


onnxruntime = lazy_import("onnxruntime")


def softmax(z):
	assert len(z.shape) == 2
	s = np.max(z, axis=1)
	s = s[:, np.newaxis]  # necessary step to do broadcasting
	e_x = np.exp(z - s)
	div = np.sum(e_x, axis=1)
	div = div[:, np.newaxis]  # dito
	return e_x / div


def distance2bbox(points, distance, max_shape=None):
	"""Decode distance prediction to bounding box.

	Args:
		points (Tensor): Shape (n, 2), [x, y].
		distance (Tensor): Distance from the given point to 4
			boundaries (left, top, right, bottom).
		max_shape (tuple): Shape of the image.

	Returns:
		Tensor: Decoded bboxes.
	"""
	x1 = points[:, 0] - distance[:, 0]
	y1 = points[:, 1] - distance[:, 1]
	x2 = points[:, 0] + distance[:, 2]
	y2 = points[:, 1] + distance[:, 3]
	if max_shape is not None:
		x1 = x1.clamp(min=0, max=max_shape[1])
		y1 = y1.clamp(min=0, max=max_shape[0])
		x2 = x2.clamp(min=0, max=max_shape[1])
		y2 = y2.clamp(min=0, max=max_shape[0])
	return np.stack([x1, y1, x2, y2], axis=-1)


def distance2kps(points, distance, max_shape=None):
	"""Decode distance prediction to bounding box.

	Args:
		points (Tensor): Shape (n, 2), [x, y].
		distance (Tensor): Distance from the given point to 4
			boundaries (left, top, right, bottom).
		max_shape (tuple): Shape of the image.

	Returns:
		Tensor: Decoded bboxes.
	"""
	preds = []
	for i in range(0, distance.shape[1], 2):
		px = points[:, i % 2] + distance[:, i]
		py = points[:, i % 2 + 1] + distance[:, i + 1]
		if max_shape is not None:
			px = px.clamp(min=0, max=max_shape[1])
			py = py.clamp(min=0, max=max_shape[0])
		preds.append(px)
		preds.append(py)
	return np.stack(preds, axis=-1)


class SCRFD(Pipeline):
	def __init__(self, options: Options, device: Device):
		super().__init__(options, device=device)

		provider_id, sub_model_id = self.options.the_model_id.split("/")
		assert provider_id == "insightface"

		model_file = hub.load(options.the_model_id)
		self.model_file = model_file
		self.batched = False
		if not os.path.exists(self.model_file):
			raise RuntimeError(f"no model found at {self.model_file}")
		self.session = onnxruntime.InferenceSession(
			self.model_file, providers=device.onnx_providers)
		self.center_cache = {}
		self.nms_thresh = 0.4
		self._init_vars()
		if self.input_size is None:
			self.input_size = options.size

	def _init_vars(self):
		input_cfg = self.session.get_inputs()[0]
		input_shape = input_cfg.shape
		if isinstance(input_shape[2], str):
			self.input_size = None
		else:
			self.input_size = tuple(input_shape[2:4][::-1])
		input_name = input_cfg.name
		outputs = self.session.get_outputs()
		if len(outputs[0].shape) == 3:
			self.batched = True
		output_names = []
		for o in outputs:
			output_names.append(o.name)
		self.input_name = input_name
		self.output_names = output_names
		self.use_kps = False
		self._num_anchors = 1
		if len(outputs) == 6:
			self.fmc = 3
			self._feat_stride_fpn = [8, 16, 32]
			self._num_anchors = 2
		elif len(outputs) == 9:
			self.fmc = 3
			self._feat_stride_fpn = [8, 16, 32]
			self._num_anchors = 2
			self.use_kps = True
		elif len(outputs) == 10:
			self.fmc = 5
			self._feat_stride_fpn = [8, 16, 32, 64, 128]
			self._num_anchors = 1
		elif len(outputs) == 15:
			self.fmc = 5
			self._feat_stride_fpn = [8, 16, 32, 64, 128]
			self._num_anchors = 1
			self.use_kps = True

	def prepare(self, **kwargs):
		nms_thresh = kwargs.get('nms_thresh', None)
		if nms_thresh is not None:
			self.nms_thresh = nms_thresh
		input_size = kwargs.get('input_size', None)
		if input_size is not None:
			if self.input_size is not None:
				print('warning: det_size is already set in scrfd model, ignore')
			else:
				self.input_size = input_size

	def forward(self, blob, thresh):
		scores_list = []
		bboxes_list = []
		kpss_list = []

		net_outs = self.session.run(self.output_names, {self.input_name: blob})

		input_height = blob.shape[2]
		input_width = blob.shape[3]
		fmc = self.fmc
		for idx, stride in enumerate(self._feat_stride_fpn):
			# If model support batch dim, take first output
			kps_preds = None
			if self.batched:
				scores = net_outs[idx][0]
				bbox_preds = net_outs[idx + fmc][0]
				bbox_preds = bbox_preds * stride
				if self.use_kps:
					kps_preds = net_outs[idx + fmc * 2][0] * stride
			# If model doesn't support batching take output as is
			else:
				scores = net_outs[idx]
				bbox_preds = net_outs[idx + fmc]
				bbox_preds = bbox_preds * stride
				if self.use_kps:
					kps_preds = net_outs[idx + fmc * 2] * stride

			height = input_height // stride
			width = input_width // stride
			key = (height, width, stride)
			if key in self.center_cache:
				anchor_centers = self.center_cache[key]
			else:
				# solution-1, c style:
				# anchor_centers = np.zeros( (height, width, 2), dtype=np.float32 )
				# for i in range(height):
				#    anchor_centers[i, :, 1] = i
				# for i in range(width):
				#    anchor_centers[:, i, 0] = i

				# solution-2:
				# ax = np.arange(width, dtype=np.float32)
				# ay = np.arange(height, dtype=np.float32)
				# xv, yv = np.meshgrid(np.arange(width), np.arange(height))
				# anchor_centers = np.stack([xv, yv], axis=-1).astype(np.float32)

				# solution-3:
				anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(np.float32)
				# print(anchor_centers.shape)

				anchor_centers = (anchor_centers * stride).reshape((-1, 2))
				if self._num_anchors > 1:
					anchor_centers = np.stack([anchor_centers] * self._num_anchors, axis=1).reshape((-1, 2))
				if len(self.center_cache) < 100:
					self.center_cache[key] = anchor_centers

			pos_inds = np.where(scores >= thresh)[0]
			bboxes = distance2bbox(anchor_centers, bbox_preds)
			pos_scores = scores[pos_inds]
			pos_bboxes = bboxes[pos_inds]
			scores_list.append(pos_scores)
			bboxes_list.append(pos_bboxes)
			if self.use_kps:
				kpss = distance2kps(anchor_centers, kps_preds)
				# kpss = kps_preds
				kpss = kpss.reshape((kpss.shape[0], -1, 2))
				pos_kpss = kpss[pos_inds]
				kpss_list.append(pos_kpss)
		return scores_list, bboxes_list, kpss_list

	def __call__(self, message: dict):
		return [self.process(x) for x in message["images"]]

	def process(self, img, thresh=0.5, input_size=None, max_num=0, metric='default'):
		assert input_size is not None or self.input_size is not None
		input_size = self.input_size if input_size is None else input_size

		im_ratio = float(img.height) / img.width
		model_ratio = float(input_size[1]) / input_size[0]
		if im_ratio > model_ratio:
			new_height = input_size[1]
			new_width = int(new_height / im_ratio)
		else:
			new_width = input_size[0]
			new_height = int(new_width * im_ratio)
		det_scale = float(new_height) / img.height
		# resized_img = cv2.resize(img, (new_width, new_height))
		resized_img = (img.resize((new_width, new_height)).pixels("sRGB", dtype=np.uint8) - 127.5) / 128.0

		det_img = np.zeros((input_size[1], input_size[0], 3), dtype=np.float32)
		det_img[:new_height, :new_width, :] = resized_img

		scores_list, bboxes_list, kpss_list = self.forward(
			np.transpose(det_img, (2, 0, 1))[np.newaxis, :], thresh)

		scores = np.vstack(scores_list)
		scores_ravel = scores.ravel()
		order = scores_ravel.argsort()[::-1]
		bboxes = np.vstack(bboxes_list) / det_scale
		if self.use_kps:
			kpss = np.vstack(kpss_list) / det_scale
		else:
			kpss = None
		pre_det = np.hstack((bboxes, scores)).astype(np.float32, copy=False)
		pre_det = pre_det[order, :]
		keep = self.nms(pre_det)
		det = pre_det[keep, :]
		if self.use_kps:
			kpss = kpss[order, :, :]
			kpss = kpss[keep, :, :]
		else:
			kpss = None
		if 0 < max_num < det.shape[0]:
			area = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
			img_center = img.shape[0] // 2, img.shape[1] // 2
			offsets = np.vstack([
				(det[:, 0] + det[:, 2]) / 2 - img_center[1],
				(det[:, 1] + det[:, 3]) / 2 - img_center[0]
			])
			offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
			if metric == 'max':
				values = area
			else:
				values = area - offset_dist_squared * 2.0  # some extra weight on the centering
			bindex = np.argsort(
				values)[::-1]  # some extra weight on the centering
			bindex = bindex[0:max_num]
			det = det[bindex, :]
			if kpss is not None:
				kpss = kpss[bindex, :]

		img_size = np.array(img.size, dtype=np.float64)
		xyxy = (det[:, :4].reshape((-1, 2, 2)) / img_size).reshape((-1, 4))

		return {
			'xyxy_s': np.concatenate((xyxy, det[:, 4][:, None]), axis=-1),
			'key_xy_s': np.concatenate((kpss / img_size, np.full(kpss.shape[:-1] + (1,), np.nan)), axis=-1)
		}

	def nms(self, dets):
		thresh = self.nms_thresh
		x1 = dets[:, 0]
		y1 = dets[:, 1]
		x2 = dets[:, 2]
		y2 = dets[:, 3]
		scores = dets[:, 4]

		areas = (x2 - x1 + 1) * (y2 - y1 + 1)
		order = scores.argsort()[::-1]

		keep = []
		while order.size > 0:
			i = order[0]
			keep.append(i)
			xx1 = np.maximum(x1[i], x1[order[1:]])
			yy1 = np.maximum(y1[i], y1[order[1:]])
			xx2 = np.minimum(x2[i], x2[order[1:]])
			yy2 = np.minimum(y2[i], y2[order[1:]])

			w = np.maximum(0.0, xx2 - xx1 + 1)
			h = np.maximum(0.0, yy2 - yy1 + 1)
			inter = w * h
			ovr = inter / (areas[i] + areas[order[1:]] - inter)

			inds = np.where(ovr <= thresh)[0]
			order = order[inds + 1]

		return keep
