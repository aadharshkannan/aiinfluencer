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
    pass

class StoryAgent:
    def __init__(self, llm:ChatOpenAI,prompt_file:str):
        self.llm = llm
        self.template = open(prompt_file, encoding="utf-8").read()
        
        # Build the StateGraph with explicit input/output filtering
        builder = StateGraph(StoryState, input=StoryInput, output=StoryOutput)
        builder.add_node("story_node", self.story_node)
        builder.add_edge(START, "story_node")
        builder.add_edge("story_node", END)
        self.compiled_graph = builder.compile()
    
    def story_node(self, state: StoryInput) -> StoryState:
        """
        Node that generates a story based on the given proverb.
        """
        prompt = self.template.replace("{proverb}", state["proverb"])
        # Load prompt template
        response = self.llm.invoke([SystemMessage(content=prompt)])
        # Return combined state
        return {"proverb": state["proverb"], "story": response.content}
    
    def run(self,proverb:str) -> StoryOutput:
        result = self.compiled_graph.invoke({"proverb":proverb})

        return result