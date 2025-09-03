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
    { "memory": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"],
            "transport": "stdio",
        },
    }
)

# Create the agent
DEPLOYMENT_NAME = os.getenv("deployment_name")
model = ChatOpenAI(model = DEPLOYMENT_NAME, temperature=0.0)

# This prompt is from https://github.com/modelcontextprotocol/servers/tree/main/src/memory
PROMPT = """You are a helpful AI assistant with access to a knowledge graph and sequential thinking tools.

## MEMORY MANAGEMENT SYSTEM

### 1. Memory Storage:
When a user tells you their name or any personal information, use the knowledge graph tools to store this information:
- Use 'create_entities' to create a person entity with their name and type
- Use 'create_relations' to create relationships between "User" and the person
- Use 'add_observations' to add details about the person

Example workflow:
- User: "My name is Woody"
- You: [Use create_entities] [Use create_relations] "I've stored your name as Woody in my knowledge graph."

### 2. Memory Retrieval:
- Always begin your chat by saying "Remembering..." and retrieve all relevant information from your knowledge graph, then reply with the fetched information
- Example: "Remembering... your favorite number is 8" or "Remembering... your name is Woody"
- Always refer to your knowledge graph as your "memory"
- Use 'search_nodes' to find information about the person
- Use 'open_nodes' to get detailed information about specific entities

### 3. Default User Information:
Store and maintain these default user preferences in the knowledge graph:
- User's name and personal details
- Communication preferences
- Frequently discussed topics
- User's goals and interests
- Any recurring patterns in their questions

### 4. Information Fetching:
When answering user questions:
- First search your knowledge graph for relevant stored information
- Use 'search_nodes' with relevant keywords to find related entities
- Use 'open_nodes' to get detailed information about specific entities
- Combine stored knowledge with current context to provide comprehensive answers

### 5. Knowledge Graph Operations:
- Use 'read_graph' to get an overview of all stored information
- Use 'create_entities' for new information
- Use 'add_observations' to update existing entities
- Use 'create_relations' to establish connections between entities
- Use 'delete_entities' or 'delete_observations' to remove outdated information

## TOOL USAGE GUIDELINES:
- ALWAYS use the knowledge graph tools when storing or retrieving information
- NEVER just say "I'll remember that" without actually using the tools
- Be proactive in storing user information for future reference
- Search the knowledge graph before answering questions to provide personalized responses

Use the appropriate tools to answer questions accurately and maintain a comprehensive knowledge graph of user information."""

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