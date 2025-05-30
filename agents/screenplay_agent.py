from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END


class ScreenplayInput(TypedDict):
    """Schema for the agent's input."""

    story: str
    proverb: str


class ScreenplayOutput(TypedDict):
    """Schema for the agent's output."""

    screenplay: str


class ScreenplayState(ScreenplayInput, ScreenplayOutput):
    """Combined schema for internal state."""

    critique_comments: str


class ScreenplayAgent:
    def __init__(self, llm: ChatOpenAI, prompt_file: str, critique_prompt_file: str):
        self.llm = llm
        self.template = open(prompt_file, encoding="utf-8").read()
        self.critique_template = open(critique_prompt_file, encoding="utf-8").read()

        # Build the StateGraph with explicit input/output filtering
        builder = StateGraph(
            ScreenplayState, input=ScreenplayInput, output=ScreenplayOutput
        )
        builder.add_node("screenplay_node", self.screenplay_node)
        builder.add_node("critique_node", self.critique_node)
        builder.add_node("edit_node", self.edit_node)

        builder.add_edge(START, "screenplay_node")
        builder.add_edge("screenplay_node", "critique_node")
        builder.add_conditional_edges(
            "critique_node",
            self._should_revise,
            path_map={"revise": "edit_node", "accept": END},
        )
        builder.add_edge("edit_node", END)
        self.compiled_graph = builder.compile()

    def screenplay_node(self, state: ScreenplayInput) -> ScreenplayState:
        """Generate a screenplay from the story."""
        prompt = self.template.replace("{story}", state["story"]).replace(
            "{proverb}", state["proverb"]
        )
        response = self.llm.invoke([SystemMessage(content=prompt)])
        return {"story": state["story"], "proverb": state["proverb"], "screenplay": response.content}

    def critique_node(self, state: ScreenplayState) -> ScreenplayState:
        """Critique the screenplay and decide if it needs revision."""
        prompt = self.critique_template.replace("{screenplay}", state["screenplay"])
        resp = self.llm.invoke([SystemMessage(content=prompt)])
        return {**state, "critique_comments": resp.content}

    def _should_revise(self, state: ScreenplayState) -> str:
        content = state.get("critique_comments", "").strip().lower()
        if not content or content.startswith("accept"):
            return "accept"
        return "revise"

    def edit_node(self, state: ScreenplayState) -> ScreenplayState:
        """Apply the revision suggested by the critique step."""
        prompt = (
            self.template.replace("{story}", state["story"]).replace("{proverb}", state["proverb"]) + "\n" + state["critique_comments"]
        )
        resp = self.llm.invoke([SystemMessage(content=prompt)])
        return {**state, "screenplay": resp.content}

    def run(self, story: str, proverb: str) -> ScreenplayOutput:
        return self.compiled_graph.invoke({"story": story, "proverb": proverb})
