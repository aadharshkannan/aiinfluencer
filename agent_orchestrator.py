import os

from langchain_openai  import ChatOpenAI
from agents.story_agent import StoryAgent
from agents.screenplay_agent import ScreenplayAgent
from utils import SynthesiaClient,CreateVideoRequest, CreateVideoInput
import random

class AgentOrchestrator:
    """
    Orchestrator for the aiinfluencer pipeline.
    Initializes the LLM and agents with the given configuration and prompt directory.
    """

    def __init__(self, model_name: str = "gpt-4o",
                 temperature: float = 0.0,
                 prompts_dir: str = "data/prompts"):
        """
        :param model_name: OpenAI model name, e.g. "gpt-4o"
        :param temperature: Sampling temperature for the LLM
        :param prompts_dir: Directory containing prompt template files
        """
        # Initialize the OpenAI LLM

        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        self.prompts_dir = prompts_dir

        # Prepare the story agent by loading its prompt template
        story_template_path = os.path.join(self.prompts_dir, "story_generation.txt")
        screenplay_template_path = os.path.join(self.prompts_dir, "screenplay_generation.txt")

        if not os.path.exists(story_template_path):
            raise FileNotFoundError(f"Prompt template not found: {story_template_path}")
        
        if not os.path.exists(screenplay_template_path):
            raise FileNotFoundError(f"Prompt template not found: {screenplay_template_path}")
        

        # Init agents
        self.story_agent = StoryAgent(
            llm=self.llm,
            prompt_file=story_template_path
        )

        self.screenplay_agent = ScreenplayAgent(
            llm = self.llm,
            prompt_file=screenplay_template_path
        )

        self.synthesia_client = SynthesiaClient(api_key=None)

    def generate_story(self, proverb: str) -> str:
        """
        Generate a short story based on the given proverb.

        :param proverb: The proverb to illustrate
        :return: Generated story text
        """
        return self.story_agent.run(proverb)
    
    def generate_screenplay(self,story: str,proverb: str)-> str:
        """
        Generate a short screenplay based on the given story.

        :param story: The story to illustrate
        :return: Generated screenplay text
        """
        return self.screenplay_agent.run(story,proverb)

    def generate_video(
        self,
        story: str,
        title: str,
        description: str,
        aspect_ratio: str = "9:16",
        test: bool = True
    ) -> dict:
        """
        Create a Synthesia video from the given story text.

        :param story: The narrative text to turn into video speech.
        :param title: The video title shown in Synthesia’s dashboard.
        :param description: A short description of the video.
        :param aspect_ratio: Aspect ratio (e.g., "9:16").
        :param test: If True, marks this as a test render in Synthesia.
        :return: The JSON response from Synthesia’s Create Video API.
        """
        avatar_options = [
        "anna_costume1_cameraA",
        "440548a8-4701-402f-afdb-6d32a851a3a6",
        "5e95491a-8101-44a7-a8cf-96f083e699ae",
        "c107b417-6957-4675-b021-905c2843c3a8",
        "a1b370c6-8f8f-4b26-bd29-e276b25ddd44",
        "santa_costume1_cameraA",        
        ]
        background_options = [
        "luxury_lobby",
        "synthesia.f6898dc2-36a1-4913-94ed-f0cdd7f553d2",
        "synthesia.2d6c9bf2-896b-4194-8164-3a5c217a6f56",
        "synthesia.35a9ab38-5294-4ee2-a0c6-456ad4372b03",
        "synthesia.b5b11f20-9461-45f2-b647-5bc4e3d52f94",
        ]

        avatar_id = random.choice(avatar_options)
        background_id = random.choice(background_options)

        # Wrap the story into a single-scene input model
        scene = CreateVideoInput(
            scriptText=story,
            avatar=avatar_id,
            background=background_id
        )

        # Construct the top-level request
        payload = CreateVideoRequest(
            test=test,
            title=title,
            description=description,
            aspectRatio=aspect_ratio,
            input=[scene]
        )

        # Delegate to the Synthesia client
        return self.synthesia_client.create_video(payload)