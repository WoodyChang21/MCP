# This file is used for helper function

# Streaming the agent output
async def stream_agent_output(agent, input_data):
    # Stream the response
    async for event in agent.astream_events(input_data, version="v2"):
        event_type = event["event"]
        
        # Show all event types for debugging
        if event_type == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, 'content') and chunk.content:
                print(chunk.content, end="", flush=True)
                
        elif event_type == "on_tool_start":
            tool_name = event["name"]
            print(f"\n[TOOL START] Using: {tool_name}")
            
        elif event_type == "on_tool_end":
            tool_name = event["name"]
            tool_output = event.get("data", {}).get("output", "No output")
            print(f"\n[TOOL END] {tool_name} completed")
            # print(f"   Output: {tool_output}")
    
    print()  # New line after response
