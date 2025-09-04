# 02 - LangChain MCP Servers

This directory contains practical examples and implementations for building MCP (Model Context Protocol) servers that integrate with LangChain agents. After understanding the fundamentals, this section shows you how to create custom MCP servers and use LangChain as the client framework.

## Contents

### Custom Server Implementation
- **Location**: `02.1-build_your_own_server/`
- **Description**: Complete examples of custom MCP server implementations with LangChain integration
- **Features**:
  - HTTP, SSE, and STDIO server implementations
  - Multi-server client using LangChain agents
  - Custom tool definitions and handlers
  - Real-world server patterns

### NPX Server Examples
- **Location**: `02.2-prebuilt_npx_server/`
- **Description**: Examples using pre-built NPX MCP servers with LangChain
- **Features**:
  - Graph Memory server integration
  - Sequential Thinking server
  - MCP Inspector debugging setup
  - Server configuration and testing

## Learning Objectives

After completing this section, you will understand:
- How to build custom MCP servers from scratch
- Different server transport methods (HTTP, SSE, STDIO)
- Tool definition and implementation patterns
- **LangChain Integration**: Using LangChain agents as MCP clients
- Server debugging and testing techniques
- Integration with existing NPX MCP servers

## Getting Started

1. **Prerequisites**: Complete the MCP fundamentals section first
2. **Choose your path**:
   - Start with `02.1-build_your_own_server/` for custom server development
   - Or begin with `02.2-prebuilt_npx_server/` for pre-built server integration
4. **Follow the README files** in each subdirectory for specific setup instructions

## Quick Start Example

Here's a simple example of using LangChain with MCP servers:

```python
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI
from mcp import MultiServerMCPClient

# Initialize MCP client
client = MultiServerMCPClient()

# Create LangChain agent with MCP tools
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, client.get_tools())

# Use the agent
response = agent.invoke({"input": "What data can you access?"})
print(response)
```

## What You'll Build

- Custom MCP servers with specific functionality
- **LangChain agents** that connect to MCP servers
- Server-client communication patterns
- Tool integration and error handling
- Debugging and monitoring capabilities

## LangChain Integration Highlights

- **Multi-Server Clients**: Connect to multiple MCP servers simultaneously
- **Agent Framework**: Use LangChain's agent framework with MCP tools
- **Tool Aggregation**: Combine tools from different MCP servers
- **Async Operations**: Handle multiple server connections efficiently
- **Real-time Processing**: Live updates and streaming responses

---

**Next Step**: After mastering server development with LangChain, proceed to the third-party MCP integrations section to learn about using existing solutions with LangChain agents.
