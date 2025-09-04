# from langgraph_supervisor import create_supervisor
import asyncio
from langchain_openai import ChatOpenAI

# Import the agent
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
# Environment Setup
import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
# Load the .env file from the project root or a specific path
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print(env_path)
# MCP
from langchain_mcp_adapters.client import MultiServerMCPClient


# MCP connection setup
# This is for Tako MCP server running in Docker
# To start the server:
# docker run -d -p 8002:8001 -e ENVIRONMENT=remote -e TAKO_API_KEY=your_api_key --name tako-mcp-server tako-mcp

client = MultiServerMCPClient({
    "tako": {
        "url": "http://localhost:8002/mcp",
        "transport": "streamable_http",
    },
})

# Create the agent
DEPLOYMENT_NAME = os.getenv("deployment_name")
model = ChatOpenAI(model = DEPLOYMENT_NAME, temperature=0.0)


# Global agent instance for Streamlit
_agent = None

os.makedirs("checkpoint", exist_ok=True)
async def clear_chat_history_async(thread_id):
    """Clear chat history for a specific thread_id using AsyncSqliteSaver"""
    try:
        async with AsyncSqliteSaver.from_conn_string("checkpoint/tako_checkpoint.sqlite") as saver:
            # Use the saver's connection to clear specific thread
            await saver.adelete_thread(str(thread_id))
            print(f"✅ Cleared chat history for thread_id: {thread_id}")
    except Exception as e:
        print(f"❌ Error clearing async history: {e}")

async def get_enhanced_prompt(user_input: str) -> str:
    """Get an enhanced prompt using MCP prompts"""
    try:
        # Use the MCP prompt to generate a better system prompt
        search_prompt = await client.get_prompt("tako", "generate_search_tako_prompt", arguments={"text": user_input})
        
        # Combine with base instructions
        enhanced_prompt = f"""
        You are an expert data analyst with access to Tako's knowledge base and visualization tools.
        
        {search_prompt}
        
       Visualization Instructions:
        - When you get visualization results from Tako tools, ALWAYS provide BOTH:
          1. An embedded iframe for inline viewing (if supported)
          2. A clickable link as fallback for full interactive access
        
        - Format for each visualization:
          **Interactive Visualization:**
          
          <iframe src="EMBED_URL" width="100%" height="1000" frameborder="0" scrolling="yes" style="border-radius: 8px; margin: 10px 0; overflow: auto; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></iframe>
          
          **🔗 Full Interactive View:** [Open in New Tab](WEBPAGE_URL)
          - **Description:** [Brief description of what the chart shows]
          - **Data Source:** [Source information if available]
        
        - If multiple visualizations are available, provide each one separately with clear titles
        - Always extract both the webpage URL and embed URL from Tako tool responses
        - Use smaller iframe height (300px) to fit better in chat
        - Include clickable links as backup for better accessibility
        - Include relevant metadata like data sources and methodology
        
        Additional instructions:
        - Always use the available Tako tools to get real-time data
        - Be specific and data-driven in your responses
        - If you need to search multiple aspects, make separate tool calls for each
        - Prioritize providing clear, accessible links to interactive visualizations
        - Include context about what each visualization represents
        """
        
        return enhanced_prompt
        
    except Exception as e:
        print(f"Error getting MCP prompt: {e}")
        # Fallback to basic prompt
        return "Use the tools available to you to answer the question with data and visualizations."

async def stream_agent_response(user_input):
    """Stream agent response for Streamlit frontend"""
    input_data = {"messages": [{"role": "user", "content": user_input}]}
    thread = {"configurable": {"thread_id": 1}}
    all_tools = await client.get_tools()
    
    # Get enhanced prompt using MCP
    enhanced_prompt = await get_enhanced_prompt(user_input)
    
    async with AsyncSqliteSaver.from_conn_string("checkpoint/tako_checkpoint.sqlite") as saver:
        # Your code here
        agent = create_react_agent(
            model=model,
            tools=all_tools,
            prompt=enhanced_prompt,  # Use the enhanced prompt instead of basic one
            debug=False,
            checkpointer=saver,  # Enable memory (Checkpoint) feature
        )
        
        # Stream the response and yield structured data
        async for event in agent.astream_events(input_data, version="v2", config=thread):
            event_type = event["event"]
            
            if event_type == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if hasattr(chunk, 'content') and chunk.content:
                    yield {
                        "type": "text",
                        "content": chunk.content
                    }
                    
            elif event_type == "on_tool_start":
                tool_name = event["name"]
                tool_input = event.get("data", {}).get("input", {})
                yield {
                    "type": "tool_start",
                    "tool_name": tool_name,
                    "input": tool_input
                }
                
            elif event_type == "on_tool_end":
                tool_name = event["name"]
                tool_output = event.get("data", {}).get("output", "No output")
                yield {
                    "type": "tool_end",
                    "tool_name": tool_name,
                    "output": tool_output
                }
                
            elif event_type == "on_chain_start":
                chain_name = event.get("name", "Unknown")
                yield {
                    "type": "chain_start",
                    "chain_name": chain_name
                }
                
            elif event_type == "on_chain_end":
                chain_name = event.get("name", "Unknown")
                yield {
                    "type": "chain_end",
                    "chain_name": chain_name
                }
                
            elif event_type == "on_llm_start":
                yield {
                    "type": "llm_start"
                }
                
            elif event_type == "on_llm_end":
                yield {
                    "type": "llm_end"
                }


# Run the agent
async def run_agent(client = client):
    # Keep sessions alive during agent execution
    all_tools = await client.get_tools()
    print(all_tools)
    user_input = "Show me a chart of Japan's GDP growth over the last 10 years"
    async with AsyncSqliteSaver.from_conn_string("checkpoint/tako_checkpoint.sqlite") as saver:
    # Your code here
        enhanced_prompt = await get_enhanced_prompt(user_input)
        agent = create_react_agent(
            model=model,
            tools=all_tools,
            debug=False,
            prompt=enhanced_prompt,
            checkpointer=saver,  # Enable memory (Checkpoint) feature
        )
        thread = {"configurable": {"thread_id": 1}}
        # Example Tako question that searches and shows a visualization:
        tako_response = await agent.ainvoke({"messages":[{"role": "user", "content": user_input}]}, thread)
    return tako_response["messages"][-1].content

async def test_prompt_tools(client=client):
    # Keep sessions alive during agent execution
    TAKO_API_KEY = "0fcec11a049843f60f061cc9c412e4d318a73f33"
    all_tools = await client.get_tools()
    print("Available tools:", [tool.name for tool in all_tools])
    
    # Test getting prompts
    try:
        prompt = await client.get_prompt("tako", "generate_search_tako_prompt", arguments={"text": "Show me a chart of Japan's GDP growth over the last 10 years"})
        print("✅ Successfully got search prompt")
        print("Prompt preview:", str(prompt)[:200] + "...")
    except Exception as e:
        print(f"❌ Error getting prompt: {e}")
if __name__ == "__main__":
    print(asyncio.run((run_agent())))
    # asyncio.run(test_prompt_tools())
    # asyncio.run(clear_chat_history_async(1))