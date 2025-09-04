# 03 - LangChain Third-Party Integrations

This directory contains third-party MCP servers and integrations that work with LangChain agents. These are production-ready solutions that extend MCP functionality with specialized capabilities, all integrated with LangChain as the client framework.

## Contents

### Tako MCP Server
- **Location**: `tako-mcp/`
- **Description**: Real-time data visualization and analysis MCP server
- **Features**:
  - Search and query Tako for real-time data
  - File upload and visualization capabilities
  - Dataset visualization tools
  - Docker deployment support
- **Source**: [TakoData/tako-mcp](https://github.com/TakoData/tako-mcp)

### Streamlit Frontend
- **Location**: `streamlit/`
- **Description**: Streamlit-based frontend for MCP agent interactions
- **Features**:
  - Real-time streaming responses
  - Interactive chat interface
  - Step-by-step process visualization
  - Session management
  - Interactive data visualizations with embedded charts and graphs
  - Responsive design with dark theme support
  - Performance optimized streaming with iframe handling
  - Advanced error handling and retry mechanisms
  - Full type hints and validation throughout

### Backend
- **Location**: `tako_graph.py`
- **Description**: Graph-based tools and utilities
- **Features**: Additional graph processing capabilities

## Learning Objectives

After completing this section, you will understand:
- How to integrate third-party MCP servers with LangChain
- Configuration and deployment strategies
- Frontend development with MCP backends and LangChain agents
- Production deployment considerations
- API key management and security
- **LangChain Integration**: Using third-party MCP servers with LangChain agents

## Prerequisites

- **Completed**: MCP fundamentals (01-mcp-fundamentals) and server building (02-langchain-mcp-servers)
- **Python 3.8+** (recommended: Python 3.11+)
- **Docker & Docker Compose**: For Tako MCP server
- **OpenAI API Key**: Required for LangChain agents
- **Tako API Key**: Required for data visualization (get from [TakoData](https://takodata.com))
- **Streamlit**: `pip install streamlit`

## Getting Started

1. **Prerequisites**: Complete the MCP fundamentals and server building sections
2. **Choose your integration**:
   - **Tako MCP**: For data visualization and analysis
   - **Streamlit Frontend**: For building user interfaces
4. **Follow the README files** in each subdirectory for setup instructions

## API Key Setup

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to your `.env` file: `OPENAI_API_KEY=your_key_here`

### Tako API Key
1. Visit [TakoData](https://takodata.com) and sign up
2. Get your API key from the dashboard
3. Add to your `.env` file: `TAKO_API_KEY=your_key_here`

## Quick Demo: Streamlit Chat Interface

To see the complete system in action, follow this 3-step process:

### Step 1: Launch Tako MCP Server
```bash
cd tako-mcp
cp env.template .env
# Edit .env and add your TAKO_API_KEY
docker compose up -d
```

### Step 2: Launch Streamlit Frontend
```bash
cd ../streamlit
pip install -r requirements.txt
# Set up .env with OPENAI_API_KEY and deployment_name
streamlit run frontend.py
```

### Step 3: Backend Logic
The `tako_graph.py` file handles the MCP server connections and LangChain agent integration.

**Result**: You'll have a fully functional chat interface using MCP servers with LangChain agents!

## Application Demo

The Streamlit application provides a powerful interface for data analysis and visualization. Here's what you can expect:

### Example: Political Data Analysis
When you ask questions like "Show me Donald Trump's favorability ratings", the application:

1. **Processes your query** through the LangChain agent
2. **Calls the Tako MCP server** to fetch real-time data
3. **Streams the response** with step-by-step progress
4. **Displays interactive visualizations** embedded directly in the chat
5. **Shows detailed metadata** including data sources and methodology

### Key Features Demonstrated
- **Real-time Data**: Live data from Tako's knowledge base
- **Interactive Charts**: Embedded visualizations with full interactivity
- **Step-by-Step Process**: Transparent view of how the agent processes requests
- **Professional UI**: Clean, responsive design with dark theme support
- **Session Management**: Persistent chat history and state management

### Sample Query Results
The application can handle complex queries and return rich, interactive visualizations including:
- Political polling data with trend analysis
- Economic indicators with comparative charts
- Social media metrics with time-series data
- Any data available through the Tako platform

## What You'll Learn

- Third-party server integration patterns with LangChain
- Frontend-backend communication using LangChain agents
- Production deployment strategies
- Security and API key management
- Real-world MCP application development with LangChain
- **LangChain Agent Integration**: Using MCP servers as tools in LangChain workflows

## Production Ready

These servers are designed for production use and include:
- Docker containerization
- Environment variable configuration
- Health checks and monitoring
- Error handling and logging
- Scalability considerations

## Troubleshooting

### Common Issues

**Docker Issues**:
- Ensure Docker is running: `docker --version`
- Check if ports are available: `netstat -tulpn | grep :3000`
- Restart Docker service if needed

**API Key Issues**:
- Verify `.env` file is in the correct directory
- Check API key format and validity
- Ensure no extra spaces or quotes in API keys

**Streamlit Issues**:
- Port conflicts: Use `streamlit run frontend.py --server.port 8502`
- Import errors: Ensure virtual environment is activated
- Memory issues: Restart the application

**MCP Connection Issues**:
- Check if Tako MCP server is running: `docker ps`
- Verify server logs: `docker logs tako-mcp`
- Test connection: `curl http://localhost:3000/health`

### Getting Help

- Check individual subdirectory README files for specific issues
- Review Docker logs for server problems
- Verify all prerequisites are installed correctly
- Ensure API keys have proper permissions

---

**Congratulations!** You've completed the full MCP learning journey from fundamentals to production-ready implementations.
