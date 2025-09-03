import streamlit as st
import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from npx_server
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent.absolute()
sys.path.insert(0, str(parent_dir))

from tako_graph import stream_agent_response, clear_chat_history_async

# Page configuration
st.set_page_config(
    page_title="MCP Agent with Streaming",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .step-box {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        background-color: #f8f9fa;
        color: #333333;
        font-weight: 500;
    }
    .tool-step {
        border-left: 4px solid #ff6b6b;
        background-color: #fff5f5;
        color: #333333;
    }
    .thinking-step {
        border-left: 4px solid #4ecdc4;
        background-color: #f0fffe;
        color: #333333;
    }
    .completed-step {
        border-left: 4px solid #45b7d1;
        background-color: #f0f8ff;
        color: #333333;
    }
    .chain-step {
        border-left: 4px solid #96ceb4;
        background-color: #f0fff4;
        color: #333333;
    }
    .streaming-text {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #e9ecef;
        font-family: 'Courier New', monospace;
        color: #333333;
    }
    .step-box strong {
        color: #000000;
        font-weight: 700;
    }
    .step-box code {
        background-color: #e9ecef;
        color: #d63384;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: 600;
    }
    .intermediate-result {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 10px;
        margin: 5px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        white-space: pre-line;
    }
    .clickable-widget {
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #007bff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .clickable-widget:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    <style>
    :root{
    --sb-bg:#11161d;
    --sb-card:#0f141a;
    --sb-border:rgba(255,255,255,.08);
    --sb-text:#e6edf3;
    --sb-muted:#9aa4b2;
    --sb-accent:#5eead4;
    --sb-accent-2:#a78bfa;
    }
    .sidebar .block-container{padding-top:1.25rem}
    .sb-card{
    background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.00));
    border:1px solid var(--sb-border);
    border-radius:16px;
    padding:14px 14px 12px;
    margin-bottom:12px;
    box-shadow:0 6px 16px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.03);
    }
    .sb-title{
    display:flex; align-items:center; gap:.5rem;
    font-weight:700; letter-spacing:.2px;
    font-size:0.95rem; color:var(--sb-text);
    padding-bottom:.35rem; margin-bottom:.6rem;
    border-bottom:1px dashed var(--sb-border);
    }
    .sb-title .tag{
    font-weight:600; font-size:.7rem; color:#0b141a;
    background:linear-gradient(90deg, var(--sb-accent), var(--sb-accent-2));
    padding:.15rem .45rem; border-radius:999px;
    }
    .sb-body{ color:var(--sb-muted); font-size:.88rem; line-height:1.35rem; }
    .sb-kv{ display:flex; justify-content:space-between; align-items:center; 
            background:rgba(255,255,255,.02); border:1px solid var(--sb-border);
            padding:.5rem .7rem; border-radius:12px; }
    .sb-kv .kv-label{ color:var(--sb-muted); font-size:.8rem; }
    .sb-kv .kv-value{ font-weight:800; font-size:1.1rem; color:var(--sb-text); }

    .sb-btn{
    display:flex; align-items:center; justify-content:center; gap:.5rem;
    text-decoration:none; font-weight:700; letter-spacing:.15px;
    padding:.55rem .8rem; width:100%;
    border-radius:12px; border:1px solid var(--sb-border);
    background:linear-gradient(180deg, rgba(94,234,212,.18), rgba(167,139,250,.12));
    color:var(--sb-text);
    transition:transform .15s ease, box-shadow .15s ease, border-color .15s ease;
    box-shadow:0 6px 14px rgba(94,234,212,.10);
    }
    .sb-btn:hover{
    transform:translateY(-1px);
    box-shadow:0 10px 22px rgba(167,139,250,.18);
    border-color:rgba(167,139,250,.45);
    }
    .sb-muted{ color:var(--sb-muted); font-size:.8rem; margin-top:.45rem; }

    .sb-links{ list-style:none; padding-left:0; margin:.2rem 0 0 0; }
    .sb-links li{ margin:.25rem 0; }
    .sb-links a{ color:var(--sb-text); text-decoration:none; border-bottom:1px dotted var(--sb-border); }
    .sb-links a:hover{ color:var(--sb-accent); border-bottom-color:var(--sb-accent); }

    @media (prefers-reduced-motion: reduce){
    .sb-btn{ transition:none }
    }
    </style>
    """, unsafe_allow_html=True)

async def clear_all_data():
    """Clear both UI state and database chat history"""
    try:
        # Clear database chat history
        await clear_chat_history_async(1)
        # Clear UI state
        st.session_state.turns = []
        st.success("✅ Cleared all chat history and UI state!")
    except Exception as e:
        st.error(f"❌ Error clearing data: {e}")

def handle_clear_all():
    """Handle the clear all button click"""
    import asyncio
    
    # Clear UI immediately
    st.session_state.turns = []
    
    # Clear database in background
    try:
        asyncio.run(clear_chat_history_async(1))
        st.success("Cleared all chat history!")
    except Exception as e:
        st.error(f"❌ Error clearing database: {e}")
    
    # No need for st.rerun() - Streamlit automatically reruns after button callbacks

# Title and description
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🤖 MCP Agent with Streaming")
    st.markdown("Ask questions and see the step-by-step process with intermediate results!")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
        handle_clear_all()

# Initialize session state
if "turns" not in st.session_state:
    # Each turn: {id, user, response, steps, inter}
    st.session_state.turns = []

def render_steps_into(container, steps, last_rendered_count=0):
    """Render step cards into an existing container (incremental updates only)."""
    if not steps:
        return last_rendered_count
    
    # Only render new steps that haven't been rendered yet
    new_steps = steps[last_rendered_count:]
    if not new_steps:
        return last_rendered_count
    
    with container:
        # Only add the header if this is the first time rendering
        if last_rendered_count == 0:
            st.markdown("### 💭 Step-by-Step Process")
        
        # Render only the new steps
        for step in new_steps:
            t = step["type"]
            n = step.get("step_number", "?")
            if t == "tool_start":
                st.markdown(f"""
                <div class="step-box tool-step">
                    <strong>🔧 Step {n}: Using Tool</strong><br>
                    <strong>Tool:</strong> <code>{step['tool_name']}</code><br>
                    <strong>Input:</strong> {step.get('input', 'None')}
                </div>
                """, unsafe_allow_html=True)

            elif t == "tool_end":
                output = step.get("output", "No output")
                if output != "No output":
                    st.markdown(f"""
                    <div class="step-box completed-step">
                        <strong>✅ Step {n}: Tool Completed</strong><br>
                        <strong>Tool:</strong> <code>{step['tool_name']}</code><br>
                        <strong>Output:</strong> {output}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="step-box completed-step">
                        <strong>✅ Step {n}: Tool Completed</strong><br>
                        <strong>Tool:</strong> <code>{step['tool_name']}</code>
                    </div>
                    """, unsafe_allow_html=True)

            # elif t == "chain_start":
            #     st.markdown(f"""
            #     <div class="step-box chain-step">
            #         <strong>🚀 Step {n}: Starting Process</strong><br>
            #         <strong>Process:</strong> {step['chain_name']}
            #     </div>
            #     """, unsafe_allow_html=True)

            # elif t == "chain_end":
            #     st.markdown(f"""
            #     <div class="step-box completed-step">
            #         <strong>🏁 Step {n}: Process Completed</strong><br>
            #         <strong>Process:</strong> {step['chain_name']}
            #     </div>
            #     """, unsafe_allow_html=True)

            # elif t == "llm_start":
            #     st.markdown(f"""
            #     <div class="step-box thinking-step">
            #         <strong>🤔 Step {n}: AI Thinking</strong><br>
            #         Processing the request...
            #     </div>
            #     """, unsafe_allow_html=True)

            # elif t == "llm_end":
            #     st.markdown(f"""
            #     <div class="step-box completed-step">
            #         <strong>💭 Step {n}: Thinking Completed</strong><br>
            #         AI has finished processing
            #     </div>
            #     """, unsafe_allow_html=True)
    
    return len(steps)

# Removed render_intermediate_list function - we don't want to show detailed intermediate results

# Render past turns (each with its own stable expander)
for turn in st.session_state.turns:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(f'<div class="streaming-text">{turn["response"]}</div>', unsafe_allow_html=True)

        # Stable expander label: DO NOT include changing numbers in the title.
        with st.expander(f"📋 Step-by-Step Process", expanded=False):
            # Single container for steps only
            inner_steps = st.container()
            render_steps_into(inner_steps, turn["steps"], 0)

async def drive_stream(prompt, response_container, expander_inner_steps):
    response_text = ""
    steps = []
    # step_counter tracks *all* event ordering (optional)
    step_counter = 0
    # display_step drives the visible numbering in the UI
    display_step = 0
    rendered_steps_count = 0

    async for chunk in stream_agent_response(prompt):
        ctype = chunk.get("type")

        if ctype == "text":
            response_text += chunk.get("content", "")
            response_container.markdown(
                f'<div class="streaming-text">{response_text}</div>',
                unsafe_allow_html=True
            )

        elif ctype == "tool_start":
            step_counter += 1
            display_step += 1
            steps.append({
                "type": "tool_start",
                "tool_name": chunk["tool_name"],
                "input": chunk.get("input", {}),
                "step_number": display_step,  # << use visible index
            })
            rendered_steps_count = render_steps_into(expander_inner_steps, steps, rendered_steps_count)

        elif ctype == "tool_end":
            # do NOT increment display_step here; this closes the same step
            steps.append({
                "type": "tool_end",
                "tool_name": chunk["tool_name"],
                "output": chunk.get("output", "No output"),
                "step_number": display_step,  # same visible index
            })
            rendered_steps_count = render_steps_into(expander_inner_steps, steps, rendered_steps_count)

        elif ctype == "chain_start":
            # If you’re not rendering chain events, don’t change display_step
            step_counter += 1
            # (optional) ignore / or keep for internal logs
            # no render call

        elif ctype == "chain_end":
            # ignore display_step
            # no render call
            pass

        elif ctype == "llm_start":
            step_counter += 1
            # ignore display_step
            # no render call
            pass

        elif ctype == "llm_end":
            # ignore display_step
            # no render call
            pass

    return response_text, steps


# New input
prompt = st.chat_input("What would you like to know?")
if prompt:
    import time
    turn_id = str(time.time_ns())

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Live response stream
        response_container = st.empty()

        # Create the expander ONCE per turn with a STABLE label (no dynamic numbers in title)
        with st.expander(f"📋 Step-by-Step Process", expanded=True):
            expander_inner_steps = st.container()  # keep this stable; we will update its content only

        async def run_turn():
            response_text, steps = await drive_stream(
                prompt,
                response_container,
                expander_inner_steps
            )

            # Persist this turn
            st.session_state.turns.append({
                "id": turn_id,
                "user": prompt,
                "response": response_text,
                "steps": steps
            })

            # Final re-render inside the existing expander container (still open)
            # render_steps_into(expander_inner_steps, steps, 0)

        asyncio.run(run_turn())

# Sidebar
# Sidebar
# Sidebar
with st.sidebar:
    # About
    st.markdown('<div class="sb-card">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">📋 About This Project: MCP × LangChain', unsafe_allow_html=True)
    st.markdown("""
<div class="sb-body">
<b>Goal:</b> Implement MCP server plugin with LangChain.<br><br>
This project shows how to integrate <b>Model Context Protocol (MCP)</b> servers with <b>LangChain</b> agents for seamless, standardized access to external tools and data.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Session
    st.markdown('<div class="sb-card">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">📊 Session</div>', unsafe_allow_html=True)
    st.markdown(f'''
<div class="sb-kv">
  <div class="kv-label">Turns</div>
  <div class="kv-value">{len(st.session_state.turns)}</div>
</div>
''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # MCP Server
    mcp_lookup = {
        "tako_graph": (
            "Tako MCP Server",
            "https://github.com/TakoData/tako-mcp",
            "💻",
        )
    }
    mod = str(stream_agent_response.__module__)
    server_name, server_link, server_emoji = mcp_lookup.get(
        mod, ("Custom / Unknown", "https://github.com/modelcontextprotocol/servers", "🛠️")
    )

    st.markdown('<div class="sb-card">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🧱 MCP Server</div>', unsafe_allow_html=True)
    st.markdown(
        f'<a class="sb-btn" href="{server_link}" target="_blank">{server_emoji} {server_name}</a>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sb-muted">Open the server’s API docs</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Built by
    st.markdown('<div class="sb-card">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">👤 Built by</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-body"><b>Woody Chang</b></div>', unsafe_allow_html=True)
    st.markdown('<ul class="sb-links">', unsafe_allow_html=True)
    st.markdown('<li>GitHub: <a href="https://github.com/WoodyChang21" target="_blank">WoodyChang21</a></li>', unsafe_allow_html=True)
    st.markdown('<li>LinkedIn: <a href="https://www.linkedin.com/in/woody-chang/" target="_blank">woody-chang</a></li>', unsafe_allow_html=True)
    st.markdown('<li>Blog: <a href="https://woodychang21.github.io/Personal-Blog/" target="_blank">Personal Blog</a></li>', unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)




# Footer
st.markdown("---")
st.markdown("Built with Streamlit + LangChain + MCP | 🤖 Powered by Sequential Thinking")
