import pytest
import requests
from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from utils import SynthesiaClient, CreateVideoRequest


def test_create_video_request_valid():
    params = CreateVideoRequest(
        test=True,
        title="Demo",
        script_text="Hello!",
        avatar="anna_costume1_cameraA",
        background="green_screen",
        description="Some description",
        aspectRatio="9:16"
    )
    # Check alias mapping in serialized dict
    data = params.model_dump(by_alias=True)
    assert data["scriptText"] == "Hello!"
    assert data["title"] == "Demo"

def test_create_video_request_missing_fields():
    # Missing 'title' should raise a ValidationError
    with pytest.raises(ValidationError):
        CreateVideoRequest(
            test=False,
            script_text="Hi",
            avatar="anna",
            background="bg",
            description="Desc",
            aspectRatio="16:9"
        )

@patch("utils.requests.post")
def test_synthesia_client_create_video_success(mock_post):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": "vid_123"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    client = SynthesiaClient(api_key="testkey")
    params = CreateVideoRequest(
        test=False,
        title="TestVid",
        script_text="Script",
        avatar="avatar1",
        background="bg1",
        description="Desc",
        aspectRatio="16:9"
    )
    result = client.create_video(params)

    # Verify HTTP call
    mock_post.assert_called_once_with(
        "https://api.synthesia.io/v2/videos",
        headers=client.headers,
        json=params.model_dump(by_alias=True),
    )
    assert result == {"id": "vid_123"}

@patch("utils.requests.post")
def test_synthesia_client_create_video_http_error(mock_post):
    # Simulate HTTP error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
    mock_post.return_value = mock_response

    client = SynthesiaClient(api_key="key")
    params = CreateVideoRequest(
        test=True,
        title="ErrVid",
        script_text="Err",
        avatar="avatar",
        background="bg",
        description="Desc",
        aspectRatio="16:9"
    )
    with pytest.raises(requests.exceptions.HTTPError):
        client.create_video(params)