# from langgraph_supervisor import create_supervisor
import asyncio
from langchain_openai import ChatOpenAI

# Import the agent
from langgraph.prebuilt import create_react_agent


# Environment Setup
import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
# Load the .env file from the project root or a specific path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# MCP
from langchain_mcp_adapters.client import MultiServerMCPClient


# MCP connection setup
client = MultiServerMCPClient(
    { # the key is the server names
    
# This is for stdio connection
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["server.py"],
            "transport": "stdio",
        },

# This is for SSE connection
    """
    Make sure:
    1. The server is running before running this script.
    2. The server is configured to use SSE transport.
    3. The server is listening on port 8050.

    To run the server:
    python server_sse.py
    """
        "weather": {
            # Make sure you start your weather server on port 8050
            "url": "http://localhost:8050/sse",
            "transport": "sse",
        },

# This is for Streamable HTTP connection
    """
    Make sure:
    1. The server is running before running this script.
    2. The server is configured to use SSE transport.
    3. The server is listening on port 8000.

    To run the server:
    python server_http.py
    """
        "temperature": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        },
    }
)

# Create the agent
DEPLOYMENT_NAME = os.getenv("deployment_name")
model = ChatOpenAI(model = DEPLOYMENT_NAME, temperature=0.0)


# Run the agent
async def run_agent(client = client):
    # Keep sessions alive during agent execution
    all_tools = await client.get_tools()
    print(all_tools)
        
    agent = create_react_agent(
        model=model,
        tools=all_tools,
        prompt="Use the tools available to you to answer the question",
        debug=False,
    )
    
    math_response = await agent.ainvoke({"messages":[{"role": "user", "content": "What is 102+298"}]})
    weather_response = await agent.ainvoke({"messages":[{"role": "user", "content": "What is the weather in Tokyo"}]})
    temperature_response = await agent.ainvoke({"messages": [{"role": "user", "content": "What is the temperature in Tokyo"}]})
    return math_response["messages"][-1].content, weather_response["messages"][-1].content, temperature_response["messages"][-1].content

if __name__ == "__main__":
    print(asyncio.run((run_agent())))
    # print("Hi")