import os
import pytest
from types import SimpleNamespace

from agents.story_agent import StoryAgent


class DummyLLM:
    """A stub LLM that yields predetermined responses."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        idx = len(self.calls) - 1
        return SimpleNamespace(content=self.responses[idx])


@pytest.fixture
def prompt_files(tmp_path):
    story_template = tmp_path / "story_template.txt"
    story_template.write_text('Write a short story illustrating the proverb: "{proverb}"', encoding="utf-8")
    critique_template = tmp_path / "story_critique.txt"
    critique_template.write_text("Critique: {story}", encoding="utf-8")
    return str(story_template), str(critique_template)


def test_story_agent_replaces_placeholder_and_returns_story(prompt_files):
    prompt_file, critique_file = prompt_files
    dummy_story = "An old tailor saved the day—truly a timely stitch!"
    llm = DummyLLM(responses=[dummy_story, "accept"])
    agent = StoryAgent(llm=llm, prompt_file=prompt_file, critique_prompt_file=critique_file)

    proverb = "A stitch in time saves nine"
    output = agent.run(proverb)

    assert isinstance(output, dict)
    assert output["story"] == dummy_story

    sent_prompt = llm.calls[0][0].content
    expected_prompt = f'Write a short story illustrating the proverb: "{proverb}"'
    assert sent_prompt == expected_prompt


def test_story_agent_applies_revision_when_requested(prompt_files):
    prompt_file, critique_file = prompt_files
    original = "Bad story"
    critique = "Needs more drama"
    revised = "Better story"
    llm = DummyLLM(responses=[original, critique, revised])
    agent = StoryAgent(llm=llm, prompt_file=prompt_file, critique_prompt_file=critique_file)

    output = agent.run("moral")
    # Third response should be returned after applying critique
    assert output["story"] == "Better story"
