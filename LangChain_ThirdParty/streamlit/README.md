# MCP Agent with Streamlit Frontend

This setup provides a Streamlit frontend that directly uses your MCP agent backend logic, showing intermediate results and step-by-step processes.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Make sure you have a `.env` file in the project root with:
```env
OPENAI_API_KEY=your_openai_api_key_here
deployment_name=gpt-4
```

### 3. Run the Streamlit App
```bash
streamlit run frontend.py
```

## 🎯 Features

- **Real-time Streaming**: See the agent's response as it's generated
- **Step-by-Step Process**: Visualize each tool usage and intermediate result
- **Interactive Chat**: Chat interface with message history
- **Session Management**: Clear chat and view session statistics
- **No API Required**: Direct function calls, no web server needed

## 🔧 How It Works

1. **Backend Logic**: Uses your `npx_server/sequential_server.py` as the backend
2. **Streaming**: Captures and displays intermediate steps in real-time
3. **Frontend**: Streamlit provides the user interface
4. **Direct Integration**: No API layer - functions are called directly

## 🎨 What You'll See

- **Text Streaming**: Agent response appears character by character
- **Tool Steps**: Visual indicators when tools are used
- **Intermediate Results**: See what each tool returns
- **Process Flow**: Chain starts, tool usage, and completions
- **Session Info**: Message count and step tracking

## 🛠️ Available Tools

- **Sequential Thinking**: Complex problem-solving tool
- **Step-by-step Analysis**: Structured reasoning process
- **Real-time Processing**: Live updates as the agent works

## 💡 Tips

- Ask complex questions to see sequential thinking in action
- Watch the step-by-step process unfold in real-time
- Each step shows tool usage and intermediate results
- Use the sidebar to track progress and clear chat history
