import os
import pytest
from types import SimpleNamespace

from agents.screenplay_agent import ScreenplayAgent

class DummyLLM:
    """A stub LLM that records the last messages and returns a fixed screenplay."""
    def __init__(self, response_text="INT. ROOM - DAY\nA robot stares at the rain."):
        self.response_text = response_text
        self.last_messages = None

    def invoke(self, messages):
        # Record what was passed in so we can assert on it
        self.last_messages = messages
        return SimpleNamespace(content=self.response_text)

@pytest.fixture
def prompt_file(tmp_path):
    # Simulate data/prompts/screenplay_template.txt
    template = (
        'Convert the following story into a screenplay format.\n\n'
        'Proverb: {proverb}\n\n'
        'Story: {story}'
    )
    file = tmp_path / "screenplay_template.txt"
    file.write_text(template, encoding="utf-8")
    return str(file)

def test_screenplay_agent_replaces_placeholders_and_returns_screenplay(prompt_file):
    # Arrange
    dummy_output = "INT. KITCHEN - MORNING\nA toaster makes a confession."
    llm = DummyLLM(response_text=dummy_output)
    agent = ScreenplayAgent(llm=llm, prompt_file=prompt_file)

    # Act
    story = "A toaster falls in love with a microwave."
    proverb = "Love knows no voltage."
    output = agent.run(story=story, proverb=proverb)

    # Assert output structure and content
    assert isinstance(output, dict), "Output should be a dict matching ScreenplayOutput"
    assert "screenplay" in output, "Output must contain 'screenplay' key"
    assert output["screenplay"] == dummy_output

    # Assert prompt correctness
    sent_system_msg = llm.last_messages[0].content
    expected_prompt = (
        f"Convert the following story into a screenplay format.\n\n"
        f"Proverb: {proverb}\n\n"
        f"Story: {story}"
    )
    assert sent_system_msg == expected_prompt