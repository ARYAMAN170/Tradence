Hi there. You asked for a backend assignment that demonstrates fundamentals in Python, API design, and logical structuring without relying on heavy ML libraries or frontend flashiness. You wanted to see if I could build a system that manages state, handles loops, and keeps things clean.




This is that system.

I built this project to function as a lightweight, graph-based workflow engine. The core idea was to create something generic enough to run any sequence of steps—like a very simplified version of LangGraph—but transparent enough that you can see exactly how the state moves from A to B.

I separated the project into two distinct parts. First, there is the Engine. This is the brain. It handles the nodes, the edges, and the scary conditional logic where the path splits based on data. It uses asyncio because blocking the main thread while waiting for a step to finish feels wrong in a modern backend system.

Second, there are the Workflows. This is where the specific business logic lives. I kept these completely decoupled from the engine so that if you wanted to add a "Data Quality Pipeline" later, you wouldn't have to touch the core graph code at all.

The Example: Code Review Agent
For the required sample workflow, I chose Option A: The Code Review Mini-Agent. I picked this one because it perfectly illustrates the need for loops. We have all been there—you write a function, check the complexity, realize it's a mess, refactor it, and check it again. It’s a cycle.

In my implementation, the system extracts code, checks its complexity, and detects issues. If the "quality score" isn't high enough, the engine uses a conditional edge to loop the state back to the beginning. It only lets the workflow finish once the code meets the threshold. It’s a simple rule-based loop, but it proves the engine can handle cycles without crashing.

How to Run It
Install the requirements.

After the dependencies are settled, fire up the server with uvicorn app.main:app --reload. The API will start listening on port 8000. I included Swagger documentation, so if you open your browser to http://127.0.0.1:8000/docs, you can test the endpoints interactively without needing to construct curl commands manually.

Using the API
I implemented the three main endpoints you requested. You can create a graph structure via POST /graph/create, though for this demo, the logic is mostly pre-configured to ensure the Code Review example runs smoothly.


To actually see the magic, hit the POST /graph/run endpoint. You can pass it an initial state—maybe a JSON object with a low quality score just to force it to loop a few times. The engine will return a run ID and the final state, along with a log of every step it took so you can verify it actually followed the logic. If you need to check on a specific run later, I added the GET /graph/state/{run_id} endpoint as well.



If I Had More Time
There is always more to do. Right now, the state is stored in memory. It works great for a demo, but if the server restarts, that data vanishes. In a production scenario, I would swap those Python dictionaries for a proper database like PostgreSQL or even a lightweight SQLite file. I also think adding a WebSocket endpoint to stream the logs line-by-line would be a nice touch, so you don't have to wait for the whole process to finish to see what's happening.


But for now, this meets the brief: it's clean, it works, and it respects the state. I hope you enjoy breaking it as much as I enjoyed building it.


