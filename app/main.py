from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uuid

from app.workflows.code_review import create_code_review_graph

app = FastAPI(title="AI Workflow Engine")

# --- In-Memory Storage ---
graphs = {}  # Stores graph definitions (if you allowed dynamic creation)
runs = {}  # Stores execution results: {run_id: {"status": "completed", "result": ...}}


# --- Models ---
class CreateGraphRequest(BaseModel):
    nodes: List[str]
    edges: Dict[str, str]


class RunGraphRequest(BaseModel):
    # For this assignment, we mostly run the pre-defined Code Review graph
    # But we can allow selecting a graph_id if we were fully dynamic
    initial_state: Dict[str, Any]


# --- Endpoints ---

@app.post("/graph/create")
async def create_graph(request: CreateGraphRequest):
    """
    we have just acknowledge the request register a simple config.
    """
    graph_id = str(uuid.uuid4())
    graphs[graph_id] = request.model_dump()
    return {"graph_id": graph_id, "message": "Graph structure saved (mock logic for dynamic graphs)"}


@app.post("/graph/run")
async def run_workflow(request: RunGraphRequest):

    run_id = str(uuid.uuid4())

    # Initialize the specific workflow
    workflow = create_code_review_graph()

    # Execute (Async)
    try:
        result = await workflow.run(request.initial_state)

        # Store result
        runs[run_id] = {
            "status": "completed",
            "final_state": result["final_state"],
            "logs": result["logs"]
        }

        return {
            "run_id": run_id,
            "status": "completed",
            "result": result
        }
    except Exception as e:
        runs[run_id] = {"status": "failed", "error": str(e)}
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return runs[run_id]