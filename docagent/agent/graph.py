from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import route_node, generate_node

# Cache compiled agent (module-level singleton)
_compiled_agent = None

def create_document_agent():
    """创建文档生成Agent"""
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("route", route_node)
    workflow.add_node("generate", generate_node)

    # 设置入口点
    workflow.set_entry_point("route")

    # 添加边
    workflow.add_edge("route", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()

def get_compiled_agent():
    """Get or create the compiled agent (cached)."""
    global _compiled_agent
    if _compiled_agent is None:
        _compiled_agent = create_document_agent()
    return _compiled_agent

def run_agent(content: str) -> str:
    """运行Agent并返回生成的文档"""
    agent = get_compiled_agent()

    initial_state = AgentState(
        content=content,
        content_type="",
        document_type=None,
        generated_document=None,
        error=None
    )

    result = agent.invoke(initial_state)

    return result.get("generated_document", "文档生成失败")