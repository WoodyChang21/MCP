## Reference
For the Graph-Memory server, check the following github repo: https://github.com/modelcontextprotocol/servers/tree/main/src/memory

For the SequentialThinking server, check the following github repo: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking

## Running Guideline
1. Make sure you have [uv](https://github.com/astral-sh/uv) installed (or use `pip` if you prefer).
2. Install the required dependencies by running:
   ```
   uv pip install -r requirements.txt
   ```
3. Open a terminal and navigate (`cd`) to the `npx_server` directory:
   ```
   cd npx_server
   ```
4. To run the Graph-Memory server example, execute:
   ```
   python graph_memory_server.py
   ```
5. To run the SequentialThinking server example, execute:
   ```
   python sequential_server.py
   ```
6. Interact with the agent in the terminal. Type `quit` to exit the program.