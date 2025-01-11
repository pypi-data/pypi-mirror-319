import requests
from pathlib import Path
from tqdm import tqdm


MODEL_URLS = {
	"cognitron/fer_plus_yolov8x.pt": "https://www.dropbox.com/scl/fi/y0410842ia9uy1eqmwpq2/best.pt?rlkey=q6m4fdr9tjm39uv3kyptd2j8q&st=1gy4i0gw&dl=1",
	"insightface/scrfd_10g_kps.onnx": "https://www.dropbox.com/scl/fi/9q0ote1gsfezce4ap6xnf/scrfd_10g_kps.onnx?rlkey=9o9wwylyaerr7evs3rf59wnyt&st=nkpwic08&dl=1",
	"insightface/w600k_r50.onnx": "https://www.dropbox.com/scl/fi/eqb0hjd3dpmz13i4zku7c/w600k_r50.onnx?rlkey=gm1gkcld2w1i32xf06avdk4s5&st=kmogdgop&dl=1",
	"transnet/transnetv2.pt": "https://www.dropbox.com/scl/fi/gvhr1vjshms87jw3m7r6v/transnetv2.pt?rlkey=bac5pn3c56xdd77gcwkogafoo&st=2jxhkic1&dl=1"
}


def download(model_id: str, p: Path):
	url = MODEL_URLS.get(model_id)
	if url is None:
		raise ValueError(f"Failed to find model {model_id} in the cognitron hub registry")

	r = requests.get(
		url,
		allow_redirects=True,
		stream=True)

	total_size = int(r.headers.get('content-length', 0))
	block_size = 1024

	with tqdm(total=total_size, unit="B", unit_scale=True, desc=f"downloading {model_id}") as progress_bar:
		with open(p, "wb") as f:
			for data in r.iter_content(block_size):
				progress_bar.update(len(data))
				f.write(data)


def cached_model_path(model_id: str) -> Path:
	if Path(model_id).exists():
		return Path(model_id)
	else:
		p = Path(model_id.replace("/", "_"))
		shared = Path.home() / ".cognitron" / "models"
		shared.mkdir(exist_ok=True, parents=True)
		return shared / p


def load(model_id: str) -> Path:
	p = cached_model_path(model_id)
	if not p.exists():
		download(model_id, p)
	return p
