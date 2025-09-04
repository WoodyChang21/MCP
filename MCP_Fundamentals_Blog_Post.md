# MCP Fundamentals: Building Your First Model Context Protocol Server

*Learn the core concepts of the Model Context Protocol and build your own MCP servers from scratch*

---

> **📚 This blog is based on the [MCP Learning Journey repository](https://github.com/WoodyChang21/MCP) that I built to provide hands-on code examples and a complete learning path for MCP development. Every code example in this blog comes from working implementations you can run yourself.**

Artificial intelligence systems are advancing rapidly, but one of their biggest challenges remains unchanged: **how can we reliably and securely connect AI models to the outside world?**

Traditionally, developers who wanted their AI agents to interact with APIs, databases, or internal tools had to build **custom integrations for every use case**. While this works in the short term, it often leads to:

* Repetitive and brittle implementations
* Vendor or framework lock-in  
* Limited reusability of tools across different AI systems
* Maintenance nightmares as tools evolve

The **Model Context Protocol (MCP)** addresses this challenge by introducing an **open standard** for connecting AI models to external tools and data sources. Instead of reinventing the wheel for each integration, developers can wrap their functionality as an **MCP-compatible server**, which can then be used by any MCP-aware client.

Think of MCP as the **USB of AI tools**: write once, reuse everywhere.

## Why MCP Matters

The rise of MCP comes at a time when enterprises and developers are increasingly adopting AI agents in production. The key advantages include:

* **Standardization** → Tools follow a consistent schema and behavior
* **Reusability** → One MCP server can serve multiple clients across different frameworks
* **Security & Governance** → Permissioning and structured interfaces provide confidence for enterprise use
* **Framework-Agnostic** → Works with LangGraph, Semantic Kernel, LangChain, or custom setups

In practice, this means that **developers focus on building tools**, not reinventing integrations for every new agent framework.

---

## Understanding MCP: Core Concepts

Before diving into building servers, let's understand the fundamental components of MCP. For a comprehensive understanding of MCP fundamentals, I highly recommend these excellent resources:

- **[MCP Crash Course Video Tutorial](https://www.youtube.com/watch?v=5xqFjh56AwM&t=126s)** - Step-by-step video walkthrough by Dave Ebbelaar
- **[MCP Crash Course Repository](https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course)** - Complete source code and examples

These resources provide the foundational knowledge that I've integrated into the [MCP Learning Journey repository](https://github.com/WoodyChang21/MCP) to create a complete hands-on learning experience.

### MCP Architecture Overview

The Model Context Protocol follows a client-host-server architecture:

- **MCP Hosts**: Programs like Claude Desktop, IDEs, or your Python application that want to access data through MCP
- **MCP Clients**: Protocol clients that maintain 1:1 connections with servers
- **MCP Servers**: Lightweight programs that each expose specific capabilities through the standardized Model Context Protocol (tools, resources, prompts)
- **Local Data Sources**: Your computer's files, databases, and services that MCP servers can securely access
- **Remote Services**: External systems available over the internet (e.g., through APIs) that MCP servers can connect to

This separation of concerns allows for modular, composable systems where each server can focus on a specific domain (like file access, web search, or database operations).

### MCP Core Primitives

MCP defines three core primitives that servers can implement:

1. **Tools**: Model-controlled functions that LLMs can invoke (like API calls, computations)
2. **Resources**: Application-controlled data that provides context (like file contents, database records)
3. **Prompts**: User-controlled templates for LLM interactions

For Python developers, the most immediately useful primitive is **tools**, which allow LLMs to perform actions programmatically.

### Transport Mechanisms

MCP supports three main transport mechanisms:

1. **STDIO (Standard IO)**: 
   - Communication occurs over standard input/output streams
   - Best for local integrations when the server and client are on the same machine
   - Simple setup with no network configuration required

2. **SSE (Server-Sent Events)**:
   - Uses HTTP for client-to-server communication and SSE for server-to-client
   - Suitable for remote connections across networks
   - Allows for distributed architectures

3. **Streamable HTTP** *(Introduced March 24, 2025)*:
   - Modern HTTP-based streaming transport that supersedes SSE
   - Uses a unified endpoint for bidirectional communication
   - **Recommended for production deployments** due to better performance and scalability
   - Supports both stateful and stateless operation modes

---

## Using LangChain as Client to Integrate with MCP

Now that we understand the fundamentals of MCP, let's explore how to use LangChain as a client to integrate with MCP servers. 

{%preview https://github.com/WoodyChang21/MCP/tree/main/02-langchain-mcp-servers/02.1-build_your_own_server %}

> **This demonstrate three different transport methods and their integration with LangChain agents.**
### Building MCP Servers with Different Transport Methods

The repository contains three server implementations, each demonstrating a different transport method:

#### 1. STDIO Transport

The STDIO transport is perfect for local development and direct process communication. Here's the pseudo code structure:

```python
# server.py - STDIO Transport
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="Calculator", host="0.0.0.0", port=8050)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# Run with STDIO transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Key Features:**
- Direct process-to-process communication
- No network configuration required
- Ideal for CLI tools and local integrations
- Simple setup and debugging

#### 2. SSE Transport

Server-Sent Events (SSE) enable real-time data streams and work well across networks:

```python
# server_sse.py - SSE Transport
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="weather", host="0.0.0.0", port=8050)

@mcp.tool()
def weather(city: str) -> str:
    """Get the weather for a city"""
    return f"The weather in {city} is sunny"

# Run with SSE transport
if __name__ == "__main__":
    mcp.run(transport="sse")
```

**Key Features:**
- Real-time communication
- Works through firewalls
- One-way communication (server to client)
- Perfect for live updates and monitoring

#### 3. Streamable HTTP Transport

Streamable HTTP is the modern approach, recommended for production deployments:

```python
# server_http.py - Streamable HTTP Transport
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="weather", host="0.0.0.0", port=8000)

@mcp.tool()
def temperature(city: str) -> str:
    """Get the temperature for a city"""
    return f"The temperature in {city} is 20 degrees"

# Run with Streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Key Features:**
- Bidirectional communication
- Scalable and stateless
- Standard web protocol
- Production-ready deployment

### Multi-Server LangChain Integration

While each of the servers described above (math, weather, and temperature) can be connected individually, the real advantage of MCP is that you can connect all of them simultaneously through a single MCP client. This unified approach allows your LangChain agent to access and orchestrate tools from multiple servers—regardless of their transport protocol—as if they were part of one seamless toolkit. This means you can mix and match capabilities (e.g., math over stdio, weather over SSE, temperature over HTTP) without worrying about the underlying communication details.

The `graph.py` file demonstrates this pattern:

```python
# graph.py - Multi-Server LangChain Client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Connect to all three servers simultaneously
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

# Create LangChain agent with all MCP tools
async def run_agent():
    all_tools = await client.get_tools()
    agent = create_react_agent(
        model=ChatOpenAI(model="gpt-4"),
        tools=all_tools,
        prompt="Use the tools available to answer the question",
    )
    
    # Agent can now use tools from all three servers
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What is 102+298 and what's the weather in Tokyo?"}]
    })
    return response
```

**Key Benefits:**
- **Unified Interface**: All tools from different servers appear as standard LangChain tools
- **Transport Agnostic**: LangChain doesn't need to know about transport differences
- **Scalable**: Easy to add new servers without changing agent code
- **Error Handling**: Built-in retry logic and connection management

### Running the Complete System

To run the complete multi-server setup:

1. **Start the servers** (in separate terminals):
   ```bash
   # Terminal 1: STDIO server
   python server.py
   
   # Terminal 2: SSE server  
   python server_sse.py
   
   # Terminal 3: HTTP server
   python server_http.py
   ```

2. **Run the LangChain client**:
   ```bash
   python graph.py
   ```

The agent will automatically discover and use tools from all three servers, demonstrating the power of MCP's standardized approach to tool integration.

> **📖 Complete implementation details and working code are available in the [Build Your Own Server section](https://github.com/WoodyChang21/MCP/tree/main/02-langchain-mcp-servers/02.1-build_your_own_server) of the MCP Learning Journey repository.**


---

## Next Steps - Advanced MCP Integration with LangChain

Ready to supercharge your LangChain projects? In the next post, I’ll show you how to instantly tap into powerful, prebuilt MCP servers—no setup required. Discover how to unlock advanced tools and integration tricks with just a few lines of code. Don’t miss out!

For the complete code and hands-on examples for this section, check out my repository
{%preview https://github.com/WoodyChang21/MCP/tree/main/03-langchain-third-party-integrations %}

You can also read the detailed blog post for next section at: {%preview https://hackmd.io/@WoodyChang1121/SygEw08qgl %}

These resources provide step-by-step guides, code walkthroughs, and practical tips for integrating LangChain with advanced MCP and third-party servers.

---

## Resources

- **[MCP Learning Journey Repository](https://github.com/WoodyChang21/MCP)** - Complete codebase I built with all examples and hands-on projects
- **[MCP Crash Course Video Tutorial](https://www.youtube.com/watch?v=5xqFjh56AwM&t=126s)** - Step-by-step video walkthrough by Dave Ebbelaar
- **[MCP Crash Course Repository](https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course)** - Original source material that inspired this repository
