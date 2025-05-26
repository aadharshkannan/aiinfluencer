from pydantic import BaseModel, Field, ConfigDict

class CreateVideoRequest(BaseModel):
    test: bool = Field(..., description="Flag to mark test video creation")
    title: str = Field(..., min_length=1, description="Title of the video")
    script_text: str = Field(..., alias="scriptText", min_length=1, description="Script content for the video")
    avatar: str = Field(..., description="Avatar identifier (e.g., anna_costume1_cameraA)")
    background: str = Field(..., description="Background setting (e.g., green_screen)")

    model_config = ConfigDict(
        validate_default=False,
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )
