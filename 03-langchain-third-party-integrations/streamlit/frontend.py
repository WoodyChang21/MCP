import asyncio
import re
import sys
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import iframe as st_iframe

# ──────────────────────────────────────────────────────────────────────────────
# Local imports
# ──────────────────────────────────────────────────────────────────────────────
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent.absolute()
sys.path.insert(0, str(parent_dir))

from tako_graph import stream_agent_response, clear_chat_history_async

# ──────────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="MCP Agent with Streaming", page_icon="🤖", layout="wide")

EMBED_HEIGHT = 560  # fixed

# ──────────────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Make native shells transparent so our own blocks control the look */
[data-testid="stChatMessage"] > div:first-child { background: transparent !important; box-shadow: none !important; }
[data-testid="stChatMessageContent"] { background: transparent !important; }

/* Step cards (unchanged) */
.step-box { border:1px solid #e5e7eb; border-radius:10px; padding:12px; margin:8px 0; background:#f8fafc; color:#111827; font-weight:500; }
.tool-step { border-left:4px solid #ff6b6b; background:#fff5f5; }
.completed-step { border-left:4px solid #45b7d1; background:#f0f8ff; }

/* Transparent text blocks — look native, but force readable color */
.msg-text-block {
  background: transparent; border: 0; padding: 6px 0; margin: 8px 0 14px;
  line-height: 1.6; white-space: pre-line;
  color: #111827;   /* Light mode default */
  font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans";
  font-size: 1rem;
}
@media (prefers-color-scheme: dark) {
  .msg-text-block { color: #e5e7eb; }  /* readable on dark background */
}

/* Keep embeds on a clean white card so charts/tables are crisp */
.embed-card {
  background:#fff; border:1px solid #e5e7eb; border-radius:12px;
  padding:12px 14px; margin: 8px 0 20px;
  color:#111827;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.embed-caption { font-size:0.9rem; opacity:0.8; margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def handle_clear_all():
    try:
        asyncio.run(clear_chat_history_async(1))
    except Exception as e:
        st.warning(f"DB clear error (continuing): {e}")
    st.session_state.clear()
    st.rerun()

def render_steps_into(container, steps, last_rendered_count=0):
    if not steps: return last_rendered_count
    new_steps = steps[last_rendered_count:]
    if not new_steps: return last_rendered_count
    with container:
        if last_rendered_count == 0:
            st.markdown("### 💭 Step-by-Step Process")
        for step in new_steps:
            t = step["type"]; n = step.get("step_number", "?")
            if t == "tool_start":
                st.markdown(
                    f"""
                    <div class="step-box tool-step">
                      <strong>🔧 Step {n}: Using Tool</strong><br/>
                      <strong>Tool:</strong> <code>{step['tool_name']}</code><br/>
                      <strong>Input:</strong> {step.get('input', 'None')}
                    </div>
                    """, unsafe_allow_html=True)
            elif t == "tool_end":
                output = step.get("output", "No output")
                body = f"<strong>Output:</strong> {output}" if output != "No output" else ""
                st.markdown(
                    f"""
                    <div class="step-box completed-step">
                      <strong>✅ Step {n}: Tool Completed</strong><br/>
                      <strong>Tool:</strong> <code>{step['tool_name']}</code><br/>
                      {body}
                    </div>
                    """, unsafe_allow_html=True)
    return len(steps)

# Split text and iframes from LLM output
IFRAME_SPLIT_RE = re.compile(r"(<iframe[\s\S]*?</iframe>)", re.IGNORECASE)
IFRAME_TAG_RE   = re.compile(r"^\s*<iframe[\s\S]*?</iframe>\s*$", re.IGNORECASE)
SRC_RE          = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)

def render_final_message_into(container, full_output_text: str):
    """
    Final/past-turn renderer:
      - Text chunks -> transparent text blocks
      - Iframe chunks -> white embed card with st_iframe
    """
    parts = [p for p in IFRAME_SPLIT_RE.split(full_output_text or "") if p and p.strip()]
    with container:
        for part in parts:
            if IFRAME_TAG_RE.match(part):
                m = SRC_RE.search(part)
                src = m.group(1) if m else ""
                if src:
                    st_iframe(src, height=EMBED_HEIGHT, scrolling=True)
                else:
                    st.warning("Embed unavailable: no src")
            else:
                st.markdown(f'<div class="msg-text-block">{part}</div>', unsafe_allow_html=True)

async def drive_stream(prompt, stream_placeholder, steps_container, notice_placeholder=None):
    """
    Streaming renderer:
      - writes accumulating text into stream_placeholder as a transparent text block
      - shows a temporary notice if an <iframe> tag appears (actual iframe shown after completion)
    """
    response_text = ""
    steps = []; display_step = 0; rendered_steps_count = 0

    async for chunk in stream_agent_response(prompt):
        ctype = chunk.get("type")
        if ctype == "text":
            response_text += chunk.get("content", "")
            stream_placeholder.markdown(f'<div class="msg-text-block">{response_text}</div>', unsafe_allow_html=True)
            if notice_placeholder and "<iframe" in response_text:
                notice_placeholder.info("📊 Interactive visualization will appear here once streaming completes...")
        elif ctype == "tool_start":
            display_step += 1
            steps.append({"type":"tool_start","tool_name":chunk["tool_name"],"input":chunk.get("input", {}),"step_number":display_step})
            rendered_steps_count = render_steps_into(steps_container, steps, rendered_steps_count)
        elif ctype == "tool_end":
            steps.append({"type":"tool_end","tool_name":chunk["tool_name"],"output":chunk.get("output","No output"),"step_number":display_step})
            rendered_steps_count = render_steps_into(steps_container, steps, rendered_steps_count)

    return response_text, steps

# ──────────────────────────────────────────────────────────────────────────────
# UI – Header
# ──────────────────────────────────────────────────────────────────────────────
st.title("🤖 MCP Agent with Streaming")
st.markdown("Ask questions and see the step-by-step process with intermediate results!")

if "turns" not in st.session_state:
    st.session_state.turns = []   # {id, user, response, steps}

# ──────────────────────────────────────────────────────────────────────────────
# Past turns
# ──────────────────────────────────────────────────────────────────────────────
for turn in st.session_state.turns:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        msg_container = st.container()
        render_final_message_into(msg_container, turn["response"])
        with st.expander("📋 Step-by-Step Process", expanded=False):
            inner_steps = st.container()
            render_steps_into(inner_steps, turn["steps"], 0)

# ──────────────────────────────────────────────────────────────────────────────
# Input + streaming
# ──────────────────────────────────────────────────────────────────────────────
prompt = st.chat_input("What would you like to know?")
if prompt:
    import time
    turn_id = str(time.time_ns())

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        turn_container = st.container()
        # child placeholders (so they don't clobber each other)
        live_text = turn_container.empty()
        live_notice = turn_container.empty()

        with st.expander("📋 Step-by-Step Process", expanded=True):
            expander_inner_steps = st.container()

        async def run_turn():
            response_text, steps = await drive_stream(
                prompt,
                live_text,
                expander_inner_steps,
                notice_placeholder=live_notice
            )

            # final render in same container
            live_notice.empty()
            live_text.empty()
            render_final_message_into(turn_container, response_text)

            st.session_state.turns.append({
                "id": turn_id,
                "user": prompt,
                "response": response_text,
                "steps": steps,
            })

        asyncio.run(run_turn())

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with Streamlit + LangChain + MCP | 🤖 Powered by TAKO MCP Server")
