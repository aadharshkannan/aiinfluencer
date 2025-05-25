import os

from langchain_openai  import ChatOpenAI
from agents.story_agent import StoryAgent
from agents.screenplay_agent import ScreenplayAgent

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
        

        self.story_agent = StoryAgent(
            llm=self.llm,
            prompt_file=story_template_path
        )

        self.screenplay_agent = ScreenplayAgent(
            llm = self.llm,
            prompt_file=screenplay_template_path
        )

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