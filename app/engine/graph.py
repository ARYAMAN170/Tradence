import uuid
import asyncio
from typing import Callable, Dict, Any, Optional


class WorkflowGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}  # simple linear edges
        self.conditional_edges: Dict[str, Callable[[Dict], str]] = {}  # branching logic
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        """Register a node (function) to the graph."""
        self.nodes[name] = func

    def set_entry_point(self, node_name: str):
        """Define where the graph starts."""
        self.entry_point = node_name

    def add_edge(self, from_node: str, to_node: str):
        """Define a direct transition."""
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition: Callable[[Dict], str]):
        """
        Define a branching transition.
        'condition' is a function that looks at state and returns the name of the next node.
        """
        self.conditional_edges[from_node] = condition

    async def run(self, initial_state: Dict[str, Any]):
        """Executes the graph from the entry point."""
        if not self.entry_point:
            raise ValueError("Entry point not set.")

        state = initial_state
        current_node_name = self.entry_point
        execution_log = []

        # Safety limit to prevent infinite loops (important for "Looping" requirement)
        steps = 0
        max_steps = 50

        while current_node_name and steps < max_steps:
            # 1. Log execution
            execution_log.append(f"Step {steps + 1}: Running {current_node_name}")

            # 2. Get and run the node function
            node_func = self.nodes.get(current_node_name)
            if not node_func:
                raise ValueError(f"Node {current_node_name} not found.")

            # Execute node (supports both async and sync functions)
            if asyncio.iscoroutinefunction(node_func):
                state = await node_func(state)
            else:
                state = node_func(state)

            steps += 1

            # 3. Determine next node
            # Check for conditional edge first (Branching/Looping)
            if current_node_name in self.conditional_edges:
                router = self.conditional_edges[current_node_name]
                current_node_name = router(state)  # Router decides next node or "END"
            # Check for standard edge
            elif current_node_name in self.edges:
                current_node_name = self.edges[current_node_name]
            else:
                current_node_name = None  # End of workflow

        return {
            "final_state": state,
            "logs": execution_log
        }