from agent_orchestrator import AgentOrchestrator
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="Generate a short AI-driven story based on a moral or proverb."
    )
    parser.add_argument(
        "moral",
        type=str,
        help="The moral or proverb to illustrate in the story."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Sampling temperature for the LLM (default: 0.0)."
    )
    parser.add_argument(
        "--prompts-dir",
        type=str,
        default="data/prompts",
        help="Directory where prompt templates are stored."
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator(
        model_name=args.model,
        temperature=args.temperature,
        prompts_dir=args.prompts_dir
    )
    story = orchestrator.generate_story(proverb=args.moral)
    print(story)

    screenplay = orchestrator.generate_screenplay(story=story['story'],
                                                  proverb=args.moral)
    print(screenplay)

if __name__ == "__main__":
    main()