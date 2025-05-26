import os

from langchain_openai  import ChatOpenAI
from agents.story_agent import StoryAgent
from agents.screenplay_agent import ScreenplayAgent
from utils import SynthesiaClient,CreateVideoRequest

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

        # Init Synthesia client once, pulling API key from env
        api_key = os.getenv("SYNTHESIA_API_KEY")
        if not api_key:
            raise RuntimeError("Environment variable SYNTHESIA_API_KEY is required")
        self.synthesia_client = SynthesiaClient(api_key=api_key)

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
        avatar_id: str = "anna_costume1_cameraA",
        background_id: str = "luxury_lobby",
        test: bool = True
    ) -> dict:
        """
        Create a Synthesia video from the given story text.

        :param story: The narrative text to turn into video speech.
        :param title: The video title shown in Synthesia’s dashboard.
        :param avatar_id: The avatar identifier (e.g., "anna_costume1_cameraA").
        :param background_id: The background setting (e.g., "green_screen").
        :param test: If True, marks this as a test render in Synthesia.
        :return: The JSON response from Synthesia’s Create Video API.
        """
        # Build the request payload
        payload = CreateVideoRequest(
            test=test,
            title=title,
            script_text=story,
            avatar=avatar_id,
            background=background_id,
            aspectRatio="9:16",
            description = description
        )

        # Call Synthesia and return the result
        return self.synthesia_client.create_video(payload)