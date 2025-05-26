import os
import pytest
import requests
from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from utils import SynthesiaClient, CreateVideoRequest, CreateVideoInput


def test_create_video_request_valid():
    # Build a valid nested input scene
    inp = CreateVideoInput(
        scriptText="Hello, Pydantic!",
        avatar="anna_costume1_cameraA",
        background="green_screen"
    )
    params = CreateVideoRequest(
        test=True,
        title="Demo Video",
        description="A quick demo",
        aspectRatio="9:16",
        input=[inp]
    )

    data = params.model_dump(by_alias=True)
    # top‐level fields
    assert data["test"] is True
    assert data["title"] == "Demo Video"
    assert data["description"] == "A quick demo"
    assert data["aspectRatio"] == "9:16"

    # nested input mapping
    assert isinstance(data["input"], list)
    scene = data["input"][0]
    assert scene["scriptText"] == "Hello, Pydantic!"
    assert scene["avatar"] == "anna_costume1_cameraA"
    assert scene["background"] == "green_screen"


def test_create_video_request_missing_fields():
    # Missing the required 'input' list entirely should error
    with pytest.raises(ValidationError):
        CreateVideoRequest(
            test=False,
            title="No Scenes",
            description="Oops",
            aspectRatio="16:9"
        )


def test_create_video_request_invalid_nested_input():
    # Nested input missing 'scriptText' should error
    with pytest.raises(ValidationError):
        CreateVideoRequest(
            test=False,
            title="Bad Scene",
            description="Missing script",
            aspectRatio="16:9",
            input=[{"avatar": "anna", "background": "bg"}]  # no scriptText
        )


@patch("utils.requests.post")
def test_synthesia_client_create_video_success(mock_post):
    # Arrange: fake a successful 201 response
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": "vid_123"}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    # Act
    client = SynthesiaClient(api_key="fakekey")
    scene = CreateVideoInput(
        scriptText="Test scene",
        avatar="avatar1",
        background="bg1"
    )
    params = CreateVideoRequest(
        test=False,
        title="TestVid",
        description="Desc",
        aspectRatio="16:9",
        input=[scene]
    )
    result = client.create_video(params)

    # Assert HTTP call was made correctly
    mock_post.assert_called_once_with(
        "https://api.synthesia.io/v2/videos",
        headers=client.headers,
        json=params.model_dump(by_alias=True),
    )
    assert result == {"id": "vid_123"}


@patch("utils.requests.post")
def test_synthesia_client_create_video_http_error(mock_post):
    # Arrange: simulate an HTTP 400
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
    mock_post.return_value = mock_resp

    client = SynthesiaClient(api_key="fakekey")
    scene = CreateVideoInput(
        scriptText="Error scene",
        avatar="avatarErr",
        background="bgErr"
    )
    params = CreateVideoRequest(
        test=True,
        title="ErrVid",
        description="Desc",
        aspectRatio="9:16",
        input=[scene]
    )

    # Act & Assert
    with pytest.raises(requests.exceptions.HTTPError):
        client.create_video(params)