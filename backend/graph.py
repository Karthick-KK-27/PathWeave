import json
from langgraph.graph import StateGraph, END
from schemas import PathState
from agents.career_research import career_research_node
from agents.gap_analysis import gap_analysis_node
from agents.semester_decision import decision_node

campus_options = json.load(open("data/campus_options.json"))

def build_graph():
    graph = StateGraph(PathState)

    graph.add_node("research", career_research_node)
    graph.add_node("gap_analysis", gap_analysis_node)
    graph.add_node("decide", lambda state: decision_node(state, campus_options))

    graph.set_entry_point("research")
    graph.add_edge("research", "gap_analysis")
    graph.add_edge("gap_analysis", "decide")
    graph.add_edge("decide", END)

    return graph.compile()

app_graph = build_graph()