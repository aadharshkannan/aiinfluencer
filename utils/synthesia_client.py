import requests
from typing import Any
from .synthesia_models import CreateVideoRequest

class SynthesiaClient:
    def __init__(self, api_key: str, base_url: str = "https://api.synthesia.io/v2"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def create_video(self, params: CreateVideoRequest) -> Any:
        """
        Create a video in Synthesia by posting the given parameters.
        Raises HTTPError on bad status codes.
        """
        url = f"{self.base_url}/videos"

        # build the payload to match the sample structure
        payload = {
            "test": params.test,
            "title": params.title,
            "visibility": getattr(params, "visibility", "private"),
            "aspectRatio": getattr(params, "aspect_ratio", "9:16"),
            "input": [
                {
                    "scriptText": params.script_text,
                    "avatar": params.avatar,
                    "avatarSettings": getattr(params, "avatar_settings", {}),
                    "background": params.background,
                    "backgroundSettings": getattr(params, "background_settings", {}),
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()