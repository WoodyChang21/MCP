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

# Helper
from helper import stream_agent_output


# MCP connection setup
client = MultiServerMCPClient(
    { # the key is the server names
    
# This is for stdio connection
        "sequentialthinking": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
            "transport": "stdio",
        }
    }
)

# Create the agent
DEPLOYMENT_NAME = os.getenv("deployment_name")
model = ChatOpenAI(model = DEPLOYMENT_NAME, temperature=0.0)

PROMPT = """
    You are an expert problem solver. For each user query, if a tool named "sequential thinking" or similar is available, you should use that tool to guide your reasoning process step by step. Do not attempt to perform sequential reasoning yourself unless explicitly instructed; instead, delegate the sequential thinking process to the dedicated tool by invoking it with the user's question or problem.

    When you receive a user question:
    - Identify if the "sequential thinking" tool is available.
    - If it is, use that tool to process the question and follow its output to structure your answer.
    - Only use other tools directly if the sequential thinking tool instructs you to, or if it is not available.

    Do not manually break down, plan, or execute sequential steps unless the tool is unavailable. Always prefer to trigger the sequential reasoning process via the dedicated tool, and present the results to the user.
    """

# Run the agent
async def run_agent(client = client):
    # Keep sessions alive during agent execution
    all_tools = await client.get_tools()
    # Print just the tool names, not the full objects
    print("Available tools:")
    for i, tool in enumerate(all_tools, 1):
        print(f"  {i}. {tool.name}")
    print()
        
    agent = create_react_agent(
        model=model,
        tools=all_tools,
        prompt=PROMPT,
        debug=False,
        )

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == 'quit':
            break
            
        input_data = {"messages": [{"role": "user", "content": user_input}]}
        
        print("Agent: ", end="", flush=True)
        
        # Stream the response
        await stream_agent_output(agent, input_data)

if __name__ == "__main__":
    print(asyncio.run((run_agent())))
    # print("Hi")