from app.engine.graph import WorkflowGraph

def extract_code(state):
    # Simulate extracting functions
    print("Extracting code...")
    state["code_functions"] = ["def hello(): pass", "def process(): return 1"]
    return state


def check_complexity(state):
    # Simulate complexity check
    print("Checking complexity...")
    # Just a mock metric
    state["complexity_score"] = 10 if "complexity_score" not in state else state["complexity_score"] - 2
    return state


def detect_issues(state):
    print("Detecting issues...")
    state["issues"] = ["Line 10: Too complex"] if state["complexity_score"] > 5 else []
    return state


def suggest_improvements(state):
    print("Suggesting improvements...")
    state["suggestions"] = "Refactor logic"
    # Simulate fixing the code slightly, which eventually breaks the loop
    state["quality_score"] = state.get("quality_score", 0) + 20
    return state


# --- Routing Logic (The Branching/Looping) ---

def quality_gate(state):
    """
    If quality score is high enough, END.
    Otherwise, go back to 'check_complexity' (Loop).
    """
    if state.get("quality_score", 0) >= 80:
        return None  # End workflow
    else:
        return "check_complexity"  # LOOP BACK


# --- Graph Assembly ---

def create_code_review_graph():
    graph = WorkflowGraph()

    # 1. Add Nodes
    graph.add_node("extract_code", extract_code)
    graph.add_node("check_complexity", check_complexity)
    graph.add_node("detect_issues", detect_issues)
    graph.add_node("suggest_improvements", suggest_improvements)

    # 2. Set Entry
    graph.set_entry_point("extract_code")

    # 3. Add Edges (Linear)
    graph.add_edge("extract_code", "check_complexity")
    graph.add_edge("check_complexity", "detect_issues")

    # 4. Conditional Logic (Branching)
    # After detecting issues, we decide: do we need improvements?
    graph.add_edge("detect_issues", "suggest_improvements")

    # 5. Looping
    # After suggestions, we check if quality is good enough.
    graph.add_conditional_edge("suggest_improvements", quality_gate)

    return graph