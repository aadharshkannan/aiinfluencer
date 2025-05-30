import os
import pytest
from types import SimpleNamespace

from agents.screenplay_agent import ScreenplayAgent


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
    template = (
        "Convert the following story into a screenplay format.\n\n"
        "Proverb: {proverb}\n\n"
        "Story: {story}"
    )
    file = tmp_path / "screenplay_template.txt"
    file.write_text(template, encoding="utf-8")
    critique_file = tmp_path / "screenplay_critique.txt"
    critique_file.write_text("Critique: {screenplay}", encoding="utf-8")
    return str(file), str(critique_file)


def test_screenplay_agent_replaces_placeholders_and_returns_screenplay(prompt_files):
    prompt_file, critique_file = prompt_files
    dummy_output = "INT. KITCHEN - MORNING\nA toaster makes a confession."
    llm = DummyLLM(responses=[dummy_output, "accept"])
    agent = ScreenplayAgent(
        llm=llm, prompt_file=prompt_file, critique_prompt_file=critique_file
    )

    story = "A toaster falls in love with a microwave."
    proverb = "Love knows no voltage."
    output = agent.run(story=story, proverb=proverb)

    # Assert output structure and content
    assert isinstance(output, dict), "Output should be a dict matching ScreenplayOutput"
    assert "screenplay" in output, "Output must contain 'screenplay' key"
    assert output["screenplay"] == dummy_output

    # Assert prompt correctness
    sent_system_msg = llm.calls[0][0].content
    expected_prompt = (
        f"Convert the following story into a screenplay format.\n\n"
        f"Proverb: {proverb}\n\n"
        f"Story: {story}"
    )
    assert sent_system_msg == expected_prompt


def test_screenplay_agent_applies_revision_when_requested(prompt_files):
    prompt_file, critique_file = prompt_files
    llm = DummyLLM(responses=["orig", "Needs color", "better"])
    agent = ScreenplayAgent(
        llm=llm, prompt_file=prompt_file, critique_prompt_file=critique_file
    )

    output = agent.run(story="s", proverb="p")
    assert output["screenplay"] == "better"
