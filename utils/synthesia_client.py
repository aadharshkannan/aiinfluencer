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
        payload = params.model_dump(by_alias=True)
        response = requests.post(url, headers=self.headers, json=payload)
        # Will raise requests.exceptions.HTTPError for 4xx/5xx responses
        response.raise_for_status()
        return response.json()