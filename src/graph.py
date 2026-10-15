from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes import recall_memory_node, generate_copy_node, brand_critique_node

def create_brand_engine_graph():
    """Builds and compiles the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("recall_memory", recall_memory_node)
    workflow.add_node("generate_copy", generate_copy_node)
    workflow.add_node("brand_critique", brand_critique_node)

    # 2. Set entry point
    workflow.set_entry_point("recall_memory")

    # 3. Add edges (Linear pipeline)
    workflow.add_edge("recall_memory", "generate_copy")
    workflow.add_edge("generate_copy", "brand_critique")
    workflow.add_edge("brand_critique", END)

    # 4. Compile the graph
    app = workflow.compile()
    return app