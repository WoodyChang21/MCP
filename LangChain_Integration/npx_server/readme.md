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

## What is MCP Inspector?

MCP Inspector is a debugging tool that allows you to:
- **Inspect MCP servers** and their available tools
- **Test tool calls** directly
- **View tool schemas** and parameters
- **Debug MCP connections**

## How to Use MCP Inspector

```bash
# Install and run MCP Inspector
npx @modelcontextprotocol/inspector
```

## 🔧 Inspecting Your Knowledge Graph Server

### Step 1: Start Your MCP Server

First, make sure your Knowledge Graph server is running:

```bash
<code_block_to_apply_changes_from>
```

### Step 2: Connect MCP Inspector

```bash
# In another terminal, start the inspector
npx @modelcontextprotocol/inspector
```

### Step 3: Configure the Inspector

In the MCP Inspector interface:

1. **Add Server**: Click "Add Server"
2. **Server Type**: Select "STDIO"
3. **Command**: `npx`
4. **Args**: 
    - `"-y", "@modelcontextprotocol/server-sequential-thinking"` $\rightarrow$ For npx Sequential-Thinking server
    - `"-y", "@modelcontextprotocol/server-memory"` $\rightarrow$ For npx Graph Memory server
5. **Transport**: `stdio`

### Step 4: Inspect Tools

Once connected, you'll see:
- **Available Tools**: List of all tools (create_entities, search_nodes, etc.)
- **Tool Schemas**: Parameters and return types for each tool
- **Test Interface**: Ability to call tools directly

## Using MCP Inspector for Debugging

### Common Use Cases:

1. **Tool Schema Inspection**: See exactly what parameters each tool expects
2. **Direct Tool Testing**: Test tools without going through your agent
3. **Connection Debugging**: Verify your MCP server is working correctly
4. **Parameter Validation**: Test different parameter combinations

### Example Inspection Workflow:

1. **Start Inspector**: `npx @modelcontextprotocol/inspector`
2. **Connect to Server**: Configure your Knowledge Graph server
3. **Browse Tools**: See all available tools and their schemas
4. **Test create_entities**: Try creating a test entity
5. **Test search_nodes**: Search for the entity you just created
6. **Verify Results**: Make sure tools work as expected