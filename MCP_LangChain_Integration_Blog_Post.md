# MCP + LangChain: From NPX Servers to Production Applications

*Connect LangChain agents to pre-built MCP servers and build production-ready AI applications*

---

> **📚 This blog is based on the [MCP Learning Journey repository](https://github.com/WoodyChang21/MCP) that I built to provide hands-on code examples and a complete learning path for MCP development. Every code example in this blog comes from working implementations you can run yourself.**

## 1. Introduction: The Power of External MCP Servers

In our previous post, we learned the fundamentals of the Model Context Protocol (MCP) and built our own servers from scratch. Now it's time to unlock the real power of MCP by connecting LangChain agents to pre-built servers and building production-ready applications.

The beauty of MCP lies in its ecosystem: instead of building every tool from scratch, you can leverage a growing collection of pre-built servers that provide specialized capabilities like memory management, data visualization, and API integrations.

**The robustness of connecting external MCP servers to improve your AI agents built with LangChain cannot be overstated.** By leveraging standardized, production-ready MCP servers, you can:

- **Dramatically enhance capabilities** without building everything from scratch
- **Access specialized tools** that would take months to develop independently
- **Maintain consistency** across different tools and services
- **Focus on business logic** rather than integration complexity
- **Scale efficiently** by adding new servers as needed

This approach transforms your LangChain agents from simple chatbots into powerful, production-ready applications that can handle complex real-world tasks.

---

## 2. NPX Pre-built MCP Servers

### 2.1: Official MCP Team Servers

The MCP team has built a comprehensive collection of pre-built servers that are readily available through NPX. These servers are production-ready, well-documented, and can be installed with a single command. The complete list of official servers can be found in the [Model Context Protocol Servers repository](https://github.com/modelcontextprotocol/servers).

These servers cover essential functionality like:
- **Memory Management**: Graph-based knowledge storage and retrieval
- **Sequential Thinking**: Advanced reasoning and problem-solving tools  
- **File System Operations**: Secure file and directory management
- **Git Integration**: Repository management and version control
- **Database Operations**: SQLite and PostgreSQL integration

The key advantage is that these servers are **pre-installed in NPX** and can simply run with `npx` commands, making them incredibly easy to integrate into your LangChain applications.

### 2.2: Implementation with NPX Servers

Here's how to integrate NPX servers with your LangChain agents, based on the implementation in the [Prebuilt NPX Server section](https://github.com/WoodyChang21/MCP/tree/main/02-langchain-mcp-servers/02.2-prebuilt_npx_server):

#### Memory Management Server

```python
# graph_memory_server.py - Memory Management with NPX
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Connect to NPX memory server
client = MultiServerMCPClient({
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "transport": "stdio",
    },
})

# Enhanced prompt for memory management
PROMPT = """You are a helpful AI assistant with access to a knowledge graph.

## MEMORY MANAGEMENT SYSTEM
- Use 'create_entities' to store user information
- Use 'search_nodes' to retrieve stored data
- Always begin responses with "Remembering..." and fetch relevant info
- Maintain persistent knowledge across conversations
"""

# Create agent with memory capabilities
agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4"),
    tools=all_tools,
    prompt=PROMPT,
)
```

#### Sequential Thinking Server

```python
# sequential_server.py - Advanced Reasoning with NPX
client = MultiServerMCPClient({
    "sequentialthinking": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        "transport": "stdio",
    },
})

PROMPT = """You are an expert problem solver. 
Use the sequential thinking tool to guide your reasoning process step by step.
Delegate complex reasoning to the dedicated tool rather than doing it manually.
"""
```

**Key Benefits:**
- **Zero Installation**: Servers run directly via NPX
- **Production Ready**: Built and maintained by the MCP team
- **Standardized**: Consistent interface across all servers
- **Extensible**: Easy to add new capabilities

---

## 3. Third-Party MCP Servers

### 3.1: The Growing MCP Ecosystem

Due to the rapid rise of MCP adoption, there are now hundreds of public MCP servers built by third-party corporations and developers. The [official MCP servers repository](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file) showcases this growing ecosystem, featuring servers for:

- **Data Visualization**: Real-time charting and analytics
- **API Integrations**: CRM, productivity, and business tools
- **Cloud Services**: AWS, Azure, and Google Cloud integrations
- **Specialized Domains**: Healthcare, finance, and scientific computing

### 3.2: Tako MCP Server Integration

In this section, we'll demonstrate integrating the Tako MCP server into our LangChain agent to build a functional chatbot that demonstrates the Tako tools. Tako provides real-time data analysis and interactive chart generation, making it perfect for demonstrating the power of third-party MCP integrations.

### 3.3: Implementation with Tako MCP Server

Here's the working pseudo code for integrating Tako MCP server with LangChain, based on the complete implementation in the [Third-Party Integrations section](https://github.com/WoodyChang21/MCP/tree/main/03-langchain-third-party-integrations):

#### Tako MCP Server Connection

```python
# tako_graph.py - Third-Party MCP Integration
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# Connect to Tako MCP server (running in Docker)
client = MultiServerMCPClient({
    "tako": {
        "url": "http://localhost:8002/mcp",
        "transport": "streamable_http",
    },
})

# Enhanced prompt with MCP prompts
async def get_enhanced_prompt(user_input: str) -> str:
    # Use MCP prompt to generate better system prompt
    search_prompt = await client.get_prompt(
        "tako", 
        "generate_search_tako_prompt", 
        arguments={"text": user_input}
    )
    
    return f"""
    You are an expert data analyst with access to Tako's knowledge base.
    
    {search_prompt}
    
    Visualization Instructions:
    - Provide embedded iframes for inline viewing
    - Include clickable links as fallback
    - Format visualizations with proper styling
    - Include data sources and methodology
    """

# Streaming agent with memory
async def stream_agent_response(user_input):
    all_tools = await client.get_tools()
    enhanced_prompt = await get_enhanced_prompt(user_input)
    
    async with AsyncSqliteSaver.from_conn_string("checkpoint/tako_checkpoint.sqlite") as saver:
        agent = create_react_agent(
            model=ChatOpenAI(model="gpt-4"),
            tools=all_tools,
            prompt=enhanced_prompt,
            checkpointer=saver,  # Enable persistent memory
        )
        
        # Stream response with structured data
        async for event in agent.astream_events(input_data, version="v2"):
            if event["event"] == "on_chat_model_stream":
                yield {"type": "text", "content": chunk.content}
            elif event["event"] == "on_tool_start":
                yield {"type": "tool_start", "tool_name": tool_name}
            elif event["event"] == "on_tool_end":
                yield {"type": "tool_end", "tool_name": tool_name}
```

#### Streamlit Frontend Integration

```python
# frontend.py - Production-Ready Chat Interface
import streamlit as st
from streamlit.components.v1 import iframe as st_iframe

# Real-time streaming with step-by-step visualization
async def drive_stream(prompt, stream_placeholder, steps_container):
    response_text = ""
    steps = []
    
    async for chunk in stream_agent_response(prompt):
        if chunk["type"] == "text":
            response_text += chunk["content"]
            # Update UI with streaming text
        elif chunk["type"] == "tool_start":
            steps.append({"type": "tool_start", "tool_name": chunk["tool_name"]})
            # Show tool usage in UI
        elif chunk["type"] == "tool_end":
            steps.append({"type": "tool_end", "tool_name": chunk["tool_name"]})
            # Mark tool completion
    
    return response_text, steps

# Main Streamlit interface
st.title("🤖 MCP Agent with Streaming")
prompt = st.chat_input("What would you like to know?")

if prompt:
    with st.chat_message("assistant"):
        # Stream response with real-time updates
        response_text, steps = await drive_stream(prompt, live_text, steps_container)
        
        # Render final message with embedded visualizations
        render_final_message_into(container, response_text)
```

### 3.4: Result Demonstration

The complete implementation results in a production-ready chatbot that demonstrates the full power of MCP + LangChain integration. The application features:

- **Real-time Data Analysis**: Live queries to Tako's knowledge base
- **Interactive Visualizations**: Embedded charts and graphs
- **Step-by-Step Process**: Transparent view of agent reasoning
- **Persistent Memory**: Conversation history and context retention
- **Professional UI**: Clean, responsive Streamlit interface

![Tako MCP Demo](https://github.com/WoodyChang21/MCP/blob/main/tako_mcp.gif)

*The demo shows the agent processing complex data queries, generating interactive visualizations, and providing comprehensive analysis - all powered by MCP server integration.*

---

## 4. Final Wrap-up

The journey from MCP fundamentals to production-ready applications demonstrates the transformative power of standardized tool integration. By leveraging both official NPX servers and third-party MCP solutions, you can build sophisticated AI agents that:

- **Access specialized capabilities** without building everything from scratch
- **Scale efficiently** by adding new MCP servers as needed
- **Maintain consistency** across different tools and services
- **Focus on business logic** rather than integration complexity

The MCP ecosystem continues to grow, with new servers being added regularly. This standardized approach to AI tool integration represents the future of intelligent application development - where developers can focus on creating value rather than reinventing integrations.

**Ready to explore the full potential?** Check out the complete implementations in the [MCP Learning Journey repository](https://github.com/WoodyChang21/MCP) and start building your own MCP-powered applications today.
