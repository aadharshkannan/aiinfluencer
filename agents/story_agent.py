from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END


class StoryInput(TypedDict):
    """Schema for the agent's input."""

    proverb: str


class StoryOutput(TypedDict):
    """Schema for the agent's output."""

    story: str


class StoryState(StoryInput, StoryOutput):
    """Combined schema for internal state."""

    critique_comments: str


class StoryAgent:
    def __init__(self, llm: ChatOpenAI, prompt_file: str, critique_prompt_file: str):
        self.llm = llm
        self.template = open(prompt_file, encoding="utf-8").read()
        self.critique_template = open(critique_prompt_file, encoding="utf-8").read()

        # Build the StateGraph with explicit input/output filtering
        builder = StateGraph(StoryState, input=StoryInput, output=StoryOutput)
        builder.add_node("story_node", self.story_node)
        builder.add_node("critique_node", self.critique_node)
        builder.add_node("edit_node", self.edit_node)

        builder.add_edge(START, "story_node")
        builder.add_edge("story_node", "critique_node")
        builder.add_conditional_edges(
            "critique_node",
            self._should_revise,
            path_map={"revise": "edit_node", "accept": END},
        )
        builder.add_edge("edit_node", END)

        self.compiled_graph = builder.compile()

    def story_node(self, state: StoryInput) -> StoryState:
        """Generate a story based on the given proverb."""
        prompt = self.template.replace("{proverb}", state["proverb"])
        response = self.llm.invoke([SystemMessage(content=prompt)])
        return {"proverb": state["proverb"], "story": response.content}

    def critique_node(self, state: StoryState) -> StoryState:
        """Critique the story and decide if it needs revision."""
        prompt = self.critique_template.replace("{story}", state["story"])
        resp = self.llm.invoke([SystemMessage(content=prompt)])
        print(f"Critique:{resp.content}")
        return {**state, "critique_comments": resp.content}

    def _should_revise(self, state: StoryState) -> str:
        comments = state.get("critique_comments", "").strip().lower()
        if not comments or comments.startswith("accept"):
            return "accept"
        return "revise"

    def edit_node(self, state: StoryState) -> StoryState:
        """Apply the revision suggested by the critique step."""
        prompt = (
            self.template.replace("{proverb}", state["proverb"]) + "\n" + state["critique_comments"]
        )
        resp = self.llm.invoke([SystemMessage(content=prompt)])
        return {**state, "story": resp.content}

    def run(self, proverb: str) -> StoryOutput:
        result = self.compiled_graph.invoke({"proverb": proverb})
        return result
