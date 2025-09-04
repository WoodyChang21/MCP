# MCP Learning Journey

A comprehensive guide to learning and implementing Model Context Protocol (MCP) from fundamentals to production-ready applications.

## Learning Path

This repository is organized in a logical progression that takes you from MCP basics to advanced implementations:

## What You'll Build

By the end of this tutorial, you'll have built a **production-ready Streamlit application** that demonstrates the full power of MCP + LangChain integration:

![Tako MCP Demo](tako_mcp.gif)

**Ready to build this?** Check out the [03 - LangChain Third-Party Integrations](./03-langchain-third-party-integrations/) section!


### [01 - MCP Fundamentals](./01-mcp-fundamentals/)
**Start here if you're new to MCP**
- Complete MCP crash course with hands-on examples
- Understanding MCP concepts and architecture
- Basic server and client implementations
- **Source**: [Dave Ebbelaar's AI Cookbook](https://github.com/daveebbelaar/ai-cookbook)

### [02 - LangChain MCP Servers](./02-langchain-mcp-servers/)
**Learn to build MCP servers with LangChain agents**
- Custom server implementations from scratch
- HTTP, SSE, and STDIO transport methods
- Tool definition and implementation patterns
- NPX server integration and debugging
- **LangChain Integration**: Using LangChain agents as MCP clients

### [03 - LangChain Third-Party Integrations](./03-langchain-third-party-integrations/)
**Integrate production-ready MCP solutions with LangChain**
- Tako MCP server for data visualization
- Streamlit frontend development
- Production deployment strategies
- Real-world application patterns
- **LangChain Integration**: Third-party MCP servers with LangChain agents

## Quick Start

1. **Begin with fundamentals**: Navigate to `01-mcp-fundamentals/`
2. **Follow the numbered sequence**: Each section builds upon the previous
3. **Hands-on learning**: Execute code examples and build projects
4. **LangChain Integration**: Learn to use MCP servers with LangChain agents
5. **Production ready**: End with deployable MCP applications using LangChain

## What You'll Master

- **MCP Architecture**: Understanding the protocol and its components
- **Server Development**: Building custom MCP servers
- **LangChain Integration**: Using LangChain agents as MCP clients
- **Tool Development**: Creating and implementing MCP tools
- **Production Deployment**: Real-world MCP applications with LangChain
- **Third-Party Integration**: Using existing MCP solutions with LangChain agents

## Prerequisites

- **Python 3.8+** (recommended: Python 3.11+)
- Basic Python knowledge
- Understanding of APIs and web services
- Docker (for some advanced examples)
- Git (for cloning and version control)
- **OpenAI API Key** (for LangChain integrations)
- **Tako API Key** (for data visualization examples)

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp
   ```

2. **Set up Python environment**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure API keys**:
   ```bash
   # Create .env file in the root directory
   touch .env
   
   # Add your API keys
   echo "OPENAI_API_KEY=your_openai_key_here" >> .env
   echo "TAKO_API_KEY=your_tako_key_here" >> .env
   ```

## How to Use This Repository

1. **Sequential Learning**: Follow the numbered folders in order
2. **Read the READMEs**: Each folder contains detailed instructions
3. **Run the Examples**: Execute code to understand concepts
4. **Experiment**: Modify examples to deepen understanding
5. **Build Projects**: Apply knowledge to real-world scenarios

## Troubleshooting

### Common Issues

- **Import Errors**: Ensure you're in the correct directory and virtual environment is activated
- **API Key Issues**: Verify your `.env` file is in the root directory and contains valid API keys
- **Docker Issues**: Ensure Docker is running and you have sufficient permissions
- **Port Conflicts**: If ports are in use, modify the port numbers in the configuration files

### Getting Help

- Check the individual README files in each directory for specific troubleshooting
- Review the original source repositories for additional support
- Ensure all prerequisites are properly installed

## Credits & Attribution

This repository contains content from multiple sources:
- **MCP Crash Course**: [Dave Ebbelaar](https://github.com/daveebbelaar) - [AI Cookbook](https://github.com/daveebbelaar/ai-cookbook)
- **Tako MCP Server**: [TakoData](https://github.com/TakoData/tako-mcp)
- All content is properly attributed to original authors

## License

Content follows the licenses of the original repositories. Please refer to individual source repositories for specific license information.

---

**Ready to start your MCP journey?** Begin with [01 - MCP Fundamentals](./01-mcp-fundamentals/) and follow the learning path!