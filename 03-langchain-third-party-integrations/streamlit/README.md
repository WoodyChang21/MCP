# MCP Agent with Streamlit Frontend

This setup provides a Streamlit frontend that directly uses your MCP agent backend logic, showing intermediate results and step-by-step processes.

## 🚀 Complete Setup Walkthrough

Follow these three steps to launch the chat interface:

### Step 1: Launch the Tako MCP Server
```bash
# Navigate to the tako-mcp directory
cd ../tako-mcp

# Set up your Tako API key
cp env.template .env
# Edit .env and add your TAKO_API_KEY

# Launch the server with Docker Compose (run this from tako-mcp directory)
docker compose up -d
```

**Verify the server is running:**
```bash
docker compose ps
docker compose logs -f
```
The server will be available at `http://localhost:8002/mcp`

### Step 2: Launch the Streamlit Frontend
```bash
# Make sure you're in the streamlit directory
cd ../streamlit

streamlit run frontend.py
```

## 🎯 What You'll See

Once all three components are running:
1. **Streamlit Interface**: Open your browser to the provided URL (usually `http://localhost:8501`)
2. **Chat Interface**: Interactive chat with the MCP agent
3. **Real-time Responses**: See the agent's responses as they're generated
4. **Tool Usage**: Visual indicators when MCP tools are being used

## 🎯 Features

- **Real-time Streaming**: See the agent's response as it's generated
- **Step-by-Step Process**: Visualize each tool usage and intermediate result
- **Interactive Chat**: Chat interface with message history
- **Session Management**: Clear chat and view session statistics
- **No API Required**: Direct function calls, no web server needed
