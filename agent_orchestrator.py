import os
import logging
import random

from langchain_openai import ChatOpenAI
from agents.story_agent import StoryAgent
from agents.screenplay_agent import ScreenplayAgent
from utils import (
    SynthesiaClient,
    CreateVideoRequest,
    CreateVideoInput,
    TemplateData,
    CreateVideoFromTemplateRequest,
)
from sqlalchemy.orm import Session
from db import store_video_metadata


class AgentOrchestrator:
    """Orchestrator for the aiinfluencer pipeline."""

    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.0, prompts_dir: str = "data/prompts"):
        """Initialize the orchestrator and its agents."""
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.prompts_dir = prompts_dir

        story_template_path = os.path.join(self.prompts_dir, "story_generation.txt")
        screenplay_template_path = os.path.join(self.prompts_dir, "screenplay_generation.txt")

        if not os.path.exists(story_template_path):
            raise FileNotFoundError(f"Prompt template not found: {story_template_path}")
        if not os.path.exists(screenplay_template_path):
            raise FileNotFoundError(f"Prompt template not found: {screenplay_template_path}")

        self.story_agent = StoryAgent(llm=self.llm, prompt_file=story_template_path)
        self.screenplay_agent = ScreenplayAgent(llm=self.llm, prompt_file=screenplay_template_path)
        self.synthesia_client = SynthesiaClient(api_key=None)
        self.logger = logging.getLogger(__name__)

    def generate_story(self, proverb: str) -> str:
        """Generate a short story based on the given proverb."""
        return self.story_agent.run(proverb)

    def generate_screenplay(self, story: str, proverb: str) -> str:
        """Generate a short screenplay based on the given story."""
        return self.screenplay_agent.run(story, proverb)

    def generate_video(
        self,
        screenplay: str,
        title: str,
        description: str,
        proverb: str,
        story: str,
        session: Session,
        aspect_ratio: str,
        test: bool = True,
    ) -> dict:
        """Create a Synthesia video from the given screenplay text and store metadata."""

        avatar_options = [
            "af145939-708c-4855-8451-b7fc0810b0a5",
            "c9a26b8f-205b-4993-b059-85c68b4cdd48",
            "af145939-708c-4855-8451-b7fc0810b0a5",
        ]
        background_options = [
            "workspace-media.189b337f-7b34-497b-a030-9f87815bbc6f",
            "workspace-media.e11ba7cb-55ad-4baf-8326-8c2e79a2f760",
            "workspace-media.0ee3a9b3-b3c0-4936-8969-8798e731e420",
            "workspace-media.7bbb37f2-090f-4e1c-bb25-78355e2c6cb9"
        ]

        avatar_id = random.choice(avatar_options)
        background_id = random.choice(background_options)

        scene = CreateVideoInput(scriptText=screenplay, avatar=avatar_id, background=background_id)

        payload = CreateVideoRequest(
            test=test,
            title=title,
            description=description,
            aspectRatio=aspect_ratio,
            input=[scene],
        )

        response = self.synthesia_client.create_video(payload)
        store_video_metadata(session, proverb, story, screenplay, response)
        return response

    def generate_video_from_template(
        self,
        screenplay: str,
        title: str,
        description: str,
        proverb: str,
        story: str,
        session: Session,
        visibility: str = "private",
        test: bool = True,
    ) -> dict:
        """Create a Synthesia video using a template and store metadata."""

        template_options = [
            "f3fcb06b-416c-48aa-98f8-f32dd9573cdd",
            "a7a6602a-c2e3-464c-a06f-32a586ba1328",
            "cecb9b14-50f5-4db9-803d-6e7c509c1a42"
        ]

        template_id = random.choice(template_options)

        data = TemplateData(screenplay=screenplay)
        payload = CreateVideoFromTemplateRequest(
            test=test,
            templateData=data,
            visibility=visibility,
            templateId=template_id,
            title=title,
            description=description,
        )

        response = self.synthesia_client.create_video_from_template(payload)
        store_video_metadata(session, proverb, story, screenplay, response)
        return response
