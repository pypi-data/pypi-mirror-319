from pydantic import BaseModel, Field


class Options(BaseModel):
	the_model_id: str = Field(alias="model_id", default="insightface/scrfd_10g_kps")
	size: tuple = (640, 640)


class VideoOptions(Options):
	fps: str = "1"
