from typing import List
from pydantic import BaseModel, Field, ConfigDict

class CreateVideoInput(BaseModel):
    scriptText: str = Field(..., alias="scriptText", min_length=1, description="Script content for the video")
    avatar: str = Field(..., description="Avatar identifier (e.g., anna_costume1_cameraA)")
    background: str = Field(..., description="Background setting (e.g., green_screen)")

    model_config = ConfigDict(
        validate_default=False,
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )


class CreateVideoRequest(BaseModel):
    test: bool = Field(..., description="Flag to mark test video creation")
    title: str = Field(..., min_length=1, description="Title of the video")
    aspectRatio: str = Field(...,description="Aspect Ratio (e.g., 16:9)")
    description: str = Field(...,description="Description of the Video")
    input: List[CreateVideoInput] = Field(...,description="Scenes that are input from video")

    model_config = ConfigDict(
        validate_default=False,
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )
