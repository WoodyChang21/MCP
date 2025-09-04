"""
MCP Agent with Streaming - Improved Version

A clean, robust Streamlit application for interacting with MCP servers
through LangChain agents with real-time streaming and step-by-step visualization.
"""

import asyncio
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
from streamlit.components.v1 import iframe as st_iframe

# ──────────────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────────────
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent.absolute()
sys.path.insert(0, str(parent_dir))

from tako_graph import stream_agent_response, clear_chat_history_async

# Constants
EMBED_HEIGHT = 560
MAX_RETRIES = 3
CHUNK_DELAY = 0.02  # Reduced delay for better performance

# Compiled regex patterns (performance optimization)
IFRAME_SPLIT_RE = re.compile(r"(<iframe[\s\S]*?</iframe>)", re.IGNORECASE)
IFRAME_TAG_RE = re.compile(r"^\s*<iframe[\s\S]*?</iframe>\s*$", re.IGNORECASE)
SRC_RE = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MCP Agent with Streaming",
    page_icon="🤖",
    layout="wide"
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS Styles
# ──────────────────────────────────────────────────────────────────────────────
CSS_STYLES = """
<style>
/* Make native shells transparent so our own blocks control the look */
[data-testid="stChatMessage"] > div:first-child { 
    background: transparent !important; 
    box-shadow: none !important; 
}
[data-testid="stChatMessageContent"] { 
    background: transparent !important; 
}

/* Step cards */
.step-box { 
    border: 1px solid #e5e7eb; 
    border-radius: 10px; 
    padding: 12px; 
    margin: 8px 0; 
    background: #f8fafc; 
    color: #111827; 
    font-weight: 500; 
}
.tool-step { 
    border-left: 4px solid #ff6b6b; 
    background: #fff5f5; 
}
.completed-step { 
    border-left: 4px solid #45b7d1; 
    background: #f0f8ff; 
}

/* Text blocks */
.msg-text-block {
    background: transparent;
    border: 0;
    padding: 2px 0;          /* less padding inside */
    margin: 4px 0 6px;       /* less vertical margin outside */
    line-height: 1.35;       /* compact but still readable */
    white-space: pre-line;
    color: #111827;
    font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans";
    font-size: 0.95rem;      /* optional: slightly smaller */
}

@media (prefers-color-scheme: dark) {
    .msg-text-block { color: #e5e7eb; }
}

/* Embed cards */
.embed-card {
    background: #fff; 
    border: 1px solid #e5e7eb; 
    border-radius: 12px;
    padding: 12px 14px; 
    margin: 8px 0 20px;
    color: #111827;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.embed-caption { 
    font-size: 0.9rem; 
    opacity: 0.8; 
    margin-bottom: 8px; 
}

/* Loading states */
.loading-text {
    color: #6b7280;
    font-style: italic;
}
</style>
"""

st.markdown(CSS_STYLES, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Utility Functions
# ──────────────────────────────────────────────────────────────────────────────

def safe_get_chunk_content(chunk: Dict[str, Any]) -> str:
    """Safely extract content from chunk with error handling."""
    try:
        return chunk.get("content", "") or ""
    except (AttributeError, TypeError):
        return ""

def validate_iframe_url(url: str) -> bool:
    """Validate iframe URL for security."""
    if not url:
        return False
    # Basic validation - allow only http/https URLs
    return url.startswith(("http://", "https://"))

def handle_clear_all() -> None:
    """Clear database and UI state with error handling."""
    try:
        asyncio.run(clear_chat_history_async(1))
        st.success("✅ Chat history cleared successfully!")
    except Exception as e:
        st.warning(f"⚠️ Database clear error (continuing): {e}")
    
    st.session_state.clear()
    st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# Rendering Functions
# ──────────────────────────────────────────────────────────────────────────────

def render_steps_into(container, steps: List[Dict[str, Any]], last_rendered_count: int = 0) -> int:
    """Render tool steps incrementally with error handling."""
    if not steps:
        return last_rendered_count
    
    new_steps = steps[last_rendered_count:]
    if not new_steps:
        return last_rendered_count
    
    with container:
        if last_rendered_count == 0:
            st.markdown("### 💭 Step-by-Step Process")
        
        for step in new_steps:
            try:
                step_type = step.get("type", "unknown")
                step_number = step.get("step_number", "?")
                
                if step_type == "tool_start":
                    tool_name = step.get("tool_name", "Unknown")
                    tool_input = step.get("input", {})
                    
                    st.markdown(f"""
                    <div class="step-box tool-step">
                        <strong>🔧 Step {step_number}: Using Tool</strong><br/>
                        <strong>Tool:</strong> <code>{tool_name}</code><br/>
                        <strong>Input:</strong> {tool_input}
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif step_type == "tool_end":
                    tool_name = step.get("tool_name", "Unknown")
                    output = step.get("output", "No output")
                    output_text = f"<strong>Output:</strong> {output}" if output != "No output" else ""
                    
                    st.markdown(f"""
                    <div class="step-box completed-step">
                        <strong>✅ Step {step_number}: Tool Completed</strong><br/>
                        <strong>Tool:</strong> <code>{tool_name}</code><br/>
                        {output_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error rendering step: {e}")
    
    return len(steps)

def render_final_message_into(container, full_output_text: str) -> None:
    """Render final message with optimized iframe handling - only process iframes when needed."""
    if not full_output_text:
        return
    
    try:
        # Quick check: if no iframe tags, render as simple text for performance
        if "<iframe" not in full_output_text:
            with container:
                st.markdown(f'<div class="msg-text-block">{full_output_text}</div>', unsafe_allow_html=True)
            return
        
        # Only split and process if iframes are present
        parts = [p for p in IFRAME_SPLIT_RE.split(full_output_text) if p and p.strip()]
        
        with container:
            for part in parts:
                if IFRAME_TAG_RE.match(part):
                    # Handle iframe content
                    src_match = SRC_RE.search(part)
                    if src_match and validate_iframe_url(src_match.group(1)):
                        try:
                            st_iframe(src_match.group(1), height=EMBED_HEIGHT, scrolling=True)
                        except Exception as e:
                            st.error(f"Could not load embed: {e}")
                            st.markdown(f'<div class="msg-text-block">Embed unavailable: {e}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Embed unavailable: invalid or missing URL")
                else:
                    # Handle text content
                    if part.strip():
                        st.markdown(f'<div class="msg-text-block">{part}</div>', unsafe_allow_html=True)
                        
    except Exception as e:
        st.error(f"Error rendering message: {e}")
        st.markdown(f'<div class="msg-text-block">{full_output_text}</div>', unsafe_allow_html=True)

async def drive_stream(
    prompt: str, 
    stream_placeholder, 
    steps_container, 
    notice_placeholder=None
) -> Tuple[str, List[Dict[str, Any]]]:
    """Stream agent response with optimized performance - no iframe detection during streaming."""
    response_text = ""
    steps = []
    display_step = 0
    rendered_steps_count = 0
    retry_count = 0
    iframe_detected = False  # Track if iframe was detected during streaming
    
    try:
        async for chunk in stream_agent_response(prompt):
            try:
                chunk_type = chunk.get("type")
                
                if chunk_type == "text":
                    chunk_content = safe_get_chunk_content(chunk)
                    response_text += chunk_content
                    
                    # Filter out iframe content during streaming to prevent premature rendering
                    streaming_text = response_text
                    if "<iframe" in response_text:
                        # Remove iframe tags and content for streaming display
                        streaming_text = re.sub(r'<iframe[\s\S]*?</iframe>', '', response_text)
                        # Also remove any remaining iframe-related text
                        streaming_text = re.sub(r'\*\*Interactive Visualization:\*\*.*?(?=\n\n|\n\*\*|$)', '', streaming_text, flags=re.DOTALL)
                        streaming_text = streaming_text.strip()
                    
                    # Render streaming text (without iframe content)
                    stream_placeholder.markdown(
                        f'<div class="msg-text-block">{streaming_text}</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Only check for iframe once and show notice
                    if notice_placeholder and not iframe_detected and "<iframe" in response_text:
                        iframe_detected = True
                        notice_placeholder.info("📊 Interactive visualization will appear here once streaming completes...")
                    
                    # Small delay for streaming effect
                    await asyncio.sleep(CHUNK_DELAY)
                    
                elif chunk_type == "tool_start":
                    display_step += 1
                    steps.append({
                        "type": "tool_start",
                        "tool_name": chunk.get("tool_name", "Unknown"),
                        "input": chunk.get("input", {}),
                        "step_number": display_step
                    })
                    rendered_steps_count = render_steps_into(steps_container, steps, rendered_steps_count)
                    
                elif chunk_type == "tool_end":
                    steps.append({
                        "type": "tool_end",
                        "tool_name": chunk.get("tool_name", "Unknown"),
                        "output": chunk.get("output", "No output"),
                        "step_number": display_step
                    })
                    rendered_steps_count = render_steps_into(steps_container, steps, rendered_steps_count)
                    
            except Exception as e:
                st.error(f"Error processing chunk: {e}")
                retry_count += 1
                if retry_count >= MAX_RETRIES:
                    st.error("Max retries exceeded. Stopping stream.")
                    break
                    
    except Exception as e:
        st.error(f"Streaming error: {e}")
    
    return response_text, steps

# ──────────────────────────────────────────────────────────────────────────────
# Main UI
# ──────────────────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    """Render sidebar with session info and controls."""
    with st.sidebar:
        st.markdown("### 📋 About This Project: MCP × LangChain")
        st.markdown("""
        **Goal:** Implement an MCP server plugin with LangChain.

        This app shows how to integrate **Model Context Protocol (MCP)** servers with **LangChain**
        agents for standardized access to external tools and data.
        """)
        
        st.markdown("### 📊 Session")
        st.write(f"Turns: **{len(st.session_state.turns)}**")

        if st.button("🗑️ Clear Chat & History", use_container_width=True, type="secondary"):
            handle_clear_all()

        st.markdown("### 🧱 MCP Server")
        mcp_lookup = {"tako_graph": ("Tako MCP Server", "https://github.com/TakoData/tako-mcp", "💻")}
        mod = str(stream_agent_response.__module__)
        server_name, server_link, server_emoji = mcp_lookup.get(
            mod, ("Custom / Unknown", "https://github.com/modelcontextprotocol/servers", "🛠️")
        )
        st.link_button(f"{server_emoji} {server_name}", server_link, use_container_width=True)

        st.markdown("### 👤 Built by")
        st.markdown(
            "- GitHub: [WoodyChang21](https://github.com/WoodyChang21)\n"
            "- LinkedIn: [woody-chang](https://www.linkedin.com/in/woody-chang/)\n"
            "- Blog: [Personal Blog](https://woodychang21.github.io/Personal-Blog/)"
        )

def render_chat_history() -> None:
    """Render past chat turns."""
    for turn in st.session_state.turns:
        with st.chat_message("user"):
            st.markdown(turn["user"])
        with st.chat_message("assistant"):
            msg_container = st.container()
            render_final_message_into(msg_container, turn["response"])
            with st.expander("📋 Step-by-Step Process", expanded=False):
                inner_steps = st.container()
                render_steps_into(inner_steps, turn["steps"], 0)

def handle_new_message(prompt: str) -> None:
    """Handle new user message with streaming response."""
    turn_id = str(time.time_ns())

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        turn_container = st.container()
        live_text = turn_container.empty()
        live_notice = turn_container.empty()

        with st.expander("📋 Step-by-Step Process", expanded=True):
            expander_inner_steps = st.container()

        async def run_turn():
            try:
                response_text, steps = await drive_stream(
                    prompt,
                    live_text,
                    expander_inner_steps,
                    notice_placeholder=live_notice
                )

                # Final render
                live_notice.empty()
                live_text.empty()
                render_final_message_into(turn_container, response_text)

                # Persist turn
                st.session_state.turns.append({
                    "id": turn_id,
                    "user": prompt,
                    "response": response_text,
                    "steps": steps,
                })
                
            except Exception as e:
                st.error(f"Error processing request: {e}")

        asyncio.run(run_turn())

# ──────────────────────────────────────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────────────────────────────────────

def main():
    """Main application entry point."""
    # Header
    st.title("🤖 MCP Agent with Streaming")
    st.markdown("Ask questions and see the step-by-step process with intermediate results!")

    # Initialize session state
    if "turns" not in st.session_state:
        st.session_state.turns = []

    # Render UI components
    render_sidebar()
    render_chat_history()

    # Handle new input
    prompt = st.chat_input("What would you like to know?")
    if prompt:
        handle_new_message(prompt)

    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit + LangChain + MCP | 🤖 Powered by TAKO MCP Server")

if __name__ == "__main__":
    main()
