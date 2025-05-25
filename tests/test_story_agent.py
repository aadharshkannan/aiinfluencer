import os
import pytest
from types import SimpleNamespace

from agents.story_agent import StoryAgent

class DummyLLM:
    """A stub LLM that records the last messages and returns a fixed story."""
    def __init__(self, response_text="Once upon a time..."):
        self.response_text = response_text
        self.last_messages = None

    def invoke(self, messages):
        # Record what was passed in so we can assert on it
        self.last_messages = messages
        return SimpleNamespace(content=self.response_text)

@pytest.fixture
def prompt_file(tmp_path):
    # Simulate data/prompts/story_template.txt
    template = 'Write a short story illustrating the proverb: "{proverb}"'
    file = tmp_path / "story_template.txt"
    file.write_text(template, encoding="utf-8")
    return str(file)

def test_story_agent_replaces_placeholder_and_returns_story(prompt_file):
    # Arrange: stub LLM and agent
    dummy_story = "An old tailor saved the day—truly a timely stitch!"
    llm = DummyLLM(response_text=dummy_story)
    agent = StoryAgent(llm=llm, prompt_file=prompt_file)

    # Act: run the agent
    proverb = "A stitch in time saves nine"
    output = agent.run(proverb)

    # Assert: output has the expected shape and content
    assert isinstance(output, dict), "Output should be a dict matching StoryOutput"
    assert "story" in output, "Output must contain 'story' key"
    assert output["story"] == dummy_story

    # Also assert that the prompt used by the LLM stub had the placeholder replaced
    sent_system_msg = llm.last_messages[0].content
    expected_prompt = f'Write a short story illustrating the proverb: "{proverb}"'
    assert sent_system_msg == expected_prompt