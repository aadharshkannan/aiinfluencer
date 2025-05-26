import os
import requests
from typing import Any
from .synthesia_models import CreateVideoRequest

class SynthesiaClient:
    """
    Minimal Synthesia API client.
    Relies on Pydantic's CreateVideoRequest to produce a valid payload.
    """

    def __init__(self, api_key: str = None, base_url: str = "https://api.synthesia.io/v2"):
        # Allow override or auto-pickup from env
        self.api_key = api_key or os.environ.get("SYNTHESIA_API_KEY")
        if not self.api_key:
            raise RuntimeError("SYNTHESIA_API_KEY must be set in env or passed explicitly")
        
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"{self.api_key}",
            "accept": "application/json",
            "content-type": "application/json",
        }

    def create_video(self, request: CreateVideoRequest) -> Any:
        """
        Create a Synthesia video from a fully-validated CreateVideoRequest.
        
        :param request: Pydantic model capturing test, title, aspectRatio, description & input scenes.
        :return: Parsed JSON response from Synthesia.
        :raises: requests.HTTPError on bad status codes.
        """
        url = f"{self.base_url}/videos"
        payload = request.model_dump(by_alias=True)
        
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        return resp.json()