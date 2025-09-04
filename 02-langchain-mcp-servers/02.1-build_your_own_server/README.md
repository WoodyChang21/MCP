# Build Your Own MCP Server

This directory contains practical examples of building custom MCP (Model Context Protocol) servers using different transport methods. Learn how to create your own MCP servers from scratch and connect them to LangChain agents.

## 📁 Contents

### Server Implementations
- **`server.py`** - Basic calculator server with STDIO transport
- **`server_http.py`** - Weather server with Streamable HTTP transport  
- **`server_sse.py`** - Weather server with Server-Sent Events (SSE) transport
- **`graph.py`** - Multi-server client that connects to all three servers

## 🚀 Quick Start

### Prerequisites
```bash
pip install mcp fastmcp langchain-openai langchain-mcp-adapters python-dotenv
```

### 1. Environment Setup
Create a `.env` file in the parent directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
deployment_name=gpt-4
```

### 2. Run Individual Servers

#### Calculator Server (STDIO)
```bash
python server.py
```

#### Weather Server (HTTP)
```bash
python server_http.py
```

#### Weather Server (SSE)
```bash
python server_sse.py
```

### 3. Run Multi-Server Client
```bash
python graph.py
```

## 🔧 Server Examples

### Calculator Server (`server.py`)
- **Transport**: STDIO
- **Tool**: `add(a, b)` - Adds two numbers
- **Usage**: Direct process communication

### Weather Server - HTTP (`server_http.py`)
- **Transport**: Streamable HTTP
- **Tool**: `temperature(city)` - Gets temperature for a city
- **Port**: 8000
- **Endpoint**: `http://localhost:8000/mcp`

### Weather Server - SSE (`server_sse.py`)
- **Transport**: Server-Sent Events
- **Tool**: `weather(city)` - Gets weather for a city
- **Port**: 8050
- **Endpoint**: `http://localhost:8050/sse`

## 🌐 Multi-Server Client (`graph.py`)

The `graph.py` file demonstrates how to connect to multiple MCP servers simultaneously:

### Features
- **Multi-Server Connection**: Connects to all three server types
- **LangChain Integration**: Uses LangChain agents with MCP tools
- **Async Operations**: Handles multiple server connections efficiently
- **Tool Aggregation**: Combines tools from all connected servers

### Server Configuration
```python
client = MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": ["server.py"],
        "transport": "stdio",
    },
    "weather": {
        "url": "http://localhost:8050/sse",
        "transport": "sse",
    },
    "temperature": {
        "url": "http://localhost:8000/mcp",
        "transport": "streamable_http",
    },
})
```

## 🛠️ Transport Methods Explained

### STDIO Transport
- **Best for**: Direct process communication
- **Use case**: Local development, CLI tools
- **Pros**: Simple, no network setup
- **Cons**: Limited to local processes

### HTTP Transport
- **Best for**: Web applications, microservices
- **Use case**: RESTful API integration
- **Pros**: Standard web protocol, easy debugging
- **Cons**: Stateless, requires HTTP server

### SSE Transport
- **Best for**: Real-time applications
- **Use case**: Live updates, streaming data
- **Pros**: Real-time communication, efficient
- **Cons**: One-way communication (server to client)

## 🎯 Learning Objectives

After completing this section, you will understand:
- How to create MCP servers using FastMCP
- Different transport methods and their use cases
- Tool definition and implementation
- Multi-server client configuration
- LangChain integration with MCP servers

## 🔍 Testing Your Servers

### Using MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```

### Manual Testing
1. Start your server
2. Use the appropriate client connection method
3. Test tool calls and responses
4. Verify error handling

## 📝 Customization

### Adding New Tools
```python
@mcp.tool()
def your_tool(param1: str, param2: int) -> str:
    """Your tool description"""
    # Your implementation
    return "result"
```

### Changing Transport
Modify the `transport` variable in the server files:
```python
transport = "stdio"  # or "sse" or "streamable-http"
```

### Adding Authentication
```python
mcp = FastMCP(
    name="your-server",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
    # Add authentication here
)
```

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in server configurations
2. **Environment variables**: Ensure `.env` file is properly loaded
3. **Dependencies**: Install all required packages
4. **Server order**: Start servers before running the client

### Debug Tips
- Check server logs for error messages
- Verify port availability
- Test individual servers before multi-server setup
- Use MCP Inspector for debugging

---

**Next Step**: After mastering custom server development, explore the prebuilt NPX servers in the next section!
