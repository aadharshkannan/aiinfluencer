from pydantic import BaseModel, Field

class CreateVideoRequest(BaseModel):
    test: bool = Field(..., description="Flag to mark test video creation")
    title: str = Field(..., min_length=1, description="Title of the video")
    script_text: str = Field(..., alias="scriptText", min_length=1, description="Script content for the video")
    avatar: str = Field(..., description="Avatar identifier (e.g., anna_costume1_cameraA)")
    background: str = Field(..., description="Background setting (e.g., green_screen)")

    class Config:
        # Allow population by Python field names (snake_case) or aliases (camelCase)
        validate_by_name = True
        # When serializing, use camelCase names
        alias_generator = None
        validate_assignment = True
        extra = "forbid"
