# Backend Switching Guide

This Streamlit frontend supports multiple backend agents. You can easily switch between different backends by changing a single import line.

## Available Backends

### 1. Sequential Thinking Server
- **File**: `npx_server/sequential_server.py`
- **Tools**: Sequential thinking, problem solving, step-by-step analysis
- **Use Case**: Complex reasoning and problem decomposition

### 2. Graph Memory Server
- **File**: `npx_server/graph_memory_server.py`
- **Tools**: Knowledge graph memory, entity management, relationship mapping
- **Use Case**: Memory management and knowledge graph operations

## How to Switch Backends

In `frontend.py`, simply change the import line:

```python
# For Sequential Thinking Backend
from npx_server.sequential_server import stream_agent_response

# For Graph Memory Backend
from npx_server.graph_memory_server import stream_agent_response
```

## Backend Requirements

Each backend must implement:
- `stream_agent_response(user_input)` function that yields structured data
- Support for the following event types:
  - `text`: Streaming text content
  - `tool_start`: Tool execution start
  - `tool_end`: Tool execution end
  - `chain_start`: Chain execution start
  - `chain_end`: Chain execution end
  - `llm_start`: LLM processing start
  - `llm_end`: LLM processing end

## Adding New Backends

To add a new backend:

1. Create a new server file in `npx_server/`
2. Implement the `stream_agent_response(user_input)` function
3. Follow the same event structure as existing backends
4. Update this documentation with the new backend details
5. Add the import option to `frontend.py`

## Example Usage

```python
# Switch to graph memory backend
from npx_server.graph_memory_server import stream_agent_response

# The frontend will automatically detect the backend and show appropriate tools
# in the sidebar
```
