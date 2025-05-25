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
    pass

class ScreenplayAgent:
    def __init__(self, llm: ChatOpenAI, prompt_file: str):
        self.llm = llm
        self.template = open(prompt_file, encoding="utf-8").read()

        # Build the StateGraph with explicit input/output filtering
        builder = StateGraph(ScreenplayState, input=ScreenplayInput, output=ScreenplayOutput)
        builder.add_node("screenplay_node", self.screenplay_node)
        builder.add_edge(START, "screenplay_node")
        builder.add_edge("screenplay_node", END)
        self.compiled_graph = builder.compile()

    def screenplay_node(self, state: ScreenplayInput) -> ScreenplayState:
        """
        Node that converts a story into a screenplay.
        """
        prompt = self.template\
            .replace("{story}", state["story"])\
            .replace("{proverb}",state["proverb"])
    
        response = self.llm.invoke([SystemMessage(content=prompt)])
        return {"screenplay": response.content}

    def run(self, story: str, proverb: str) -> ScreenplayOutput:
        return self.compiled_graph.invoke({"story": story,"proverb": proverb})