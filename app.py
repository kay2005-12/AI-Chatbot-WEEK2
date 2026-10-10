"""
AI - Intelligent Customer Support Assistant
Frontend: Streamlit Clean & Minimal Web Interface
Backend: TF-IDF Vectorization & Cosine Similarity (chatbot.py)
"""

import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path for local module resolution
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import existing chatbot function without modifying chatbot.py or intents.json
from chatbot import get_responses

# -----------------------------------------------------------------------------
# Page Configuration
st.set_page_config(
    page_title=" Customer  Support Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Clean & Minimal CSS (Navy-blue accents on light background)
st.markdown(
    """
    <style>
    /* Clean typography & background */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Header styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.85rem;
        margin-bottom: 1.25rem;
    }

    .header-title-box {
        display: flex;
        flex-direction: column;
    }

    .header-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1E3A8A; /* Navy blue */
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 0.88rem;
        color: #64748B; /* Slate gray */
        margin: 0;
        font-weight: 500;
    }

    /* Small status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #15803D;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #22C55E;
        border-radius: 50%;
        display: inline-block;
    }

    /* Discreet metadata styling below assistant messages */
    .chat-meta {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 6px;
        padding-top: 4px;
        border-top: 1px solid #F1F5F9;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .meta-tag {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        color: #1E293B;
    }

    .meta-sim {
        color: #1D4ED8;
        font-weight: 600;
    }

    .meta-fallback {
        color: #DC2626;
        font-weight: 500;
    }

    /* Sidebar quick question button subtle styling */
    [data-testid="stSidebar"] .stButton > button {
        border-radius: 6px;
        font-size: 0.84rem;
        font-weight: 500;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Helper Functions
def get_welcome_message() -> dict:
    """Standardized welcome message on chat start."""
    return {
        "role": "assistant",
        "content": (
            "Hello! I am **TechNova AI**, your customer support assistant. "
            "I can answer questions regarding our services, pricing, "
            "working hours, payment options, and support. How can I help you today?"
        ),
        "intent": "welcome",
        "confidence": None
    }


def format_similarity(confidence) -> str:
    """Format similarity score as a percentage safely."""
    if confidence is None:
        return "N/A"
    try:
        val = float(confidence)
        # Cosine similarity is clamped between 0% and 100%
        pct = min(100.0, max(0.0, val * 100.0))
        return f"{pct:.1f}%"
    except (ValueError, TypeError):
        return "N/A"


# -----------------------------------------------------------------------------
# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [get_welcome_message()]

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# -----------------------------------------------------------------------------
# Sidebar: Project Info, New Chat & Suggested Questions
with st.sidebar:
    st.subheader("AI Assistant")
    st.write(
        "An intelligent customer support chatbot using **TF-IDF Vectorization** "
        "and **Cosine Similarity** to match client inquiries to predefined intents."
    )

    # New Chat Button
    if st.button("🔄 New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = [get_welcome_message()]
        st.session_state.pending_query = None
        st.rerun()

    st.markdown("---")
    st.markdown("##### Suggested Questions")
    
    suggested_questions = [
        "What services do you offer?",
        "How much does it cost?",
        "What are your working hours?",
        "How can I contact support?",
        "Which payment methods do you accept?"
    ]

    for idx, question in enumerate(suggested_questions):
        if st.button(question, key=f"sq_{idx}", use_container_width=True):
            st.session_state.pending_query = question
            st.rerun()

    st.markdown("---")
    st.caption("AI Customer Support • Student Portfolio Project")

# -----------------------------------------------------------------------------
# Main Header
st.markdown(
    """
    <div class="header-container">
        <div class="header-title-box">
            <h1 class="header-title">AI Assistant</h1>
            <p class="header-subtitle">Intelligent Customer Support Assistant</p>
        </div>
        <div class="status-badge">
            <span class="status-dot"></span>
            <span>Chatbot Ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Process Pending Quick Query (from Sidebar Buttons)
if st.session_state.pending_query:
    active_prompt = st.session_state.pending_query.strip()
    st.session_state.pending_query = None

    if active_prompt:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": active_prompt
        })

        # Fetch bot response safely
        try:
            bot_result = get_responses(active_prompt)
            intent = str(bot_result.get("intent", "unknown"))
            response_text = str(bot_result.get("response", "I could not find a suitable answer."))
            confidence = bot_result.get("confidence", 0.0)
        except Exception as err:
            intent = "error"
            response_text = f"An unexpected error occurred while communicating with the chatbot: {err}"
            confidence = 0.0

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "intent": intent,
            "confidence": confidence
        })

# -----------------------------------------------------------------------------
# Display Conversation History
for msg in st.session_state.messages:
    role = msg.get("role", "assistant")
    with st.chat_message(role):
        st.markdown(msg.get("content", ""))

        # Discreet metadata display below assistant responses
        if role == "assistant":
            intent = msg.get("intent")
            conf = msg.get("confidence")

            if intent == "welcome":
                st.markdown(
                    """
                    <div class="chat-meta">
                        <span>Ready to assist</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif intent:
                sim_display = format_similarity(conf)
                fallback_note = ""
                if intent in ["unknown", "empty_input", "error"]:
                    fallback_note = '<span class="meta-fallback">(Fallback match)</span>'

                st.markdown(
                    f"""
                    <div class="chat-meta">
                        <span>Intent: <span class="meta-tag">{intent}</span></span>
                        <span>&bull;</span>
                        <span>Similarity: <span class="meta-sim">{sim_display}</span></span>
                        {fallback_note}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# -----------------------------------------------------------------------------
# User Chat Input
user_input = st.chat_input("Type your message here...")

if user_input and user_input.strip():
    clean_input = user_input.strip()

    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": clean_input
    })

    # Fetch response from existing chatbot.py logic
    try:
        bot_result = get_responses(clean_input)
        intent = str(bot_result.get("intent", "unknown"))
        response_text = str(bot_result.get("response", "I could not find a suitable answer."))
        confidence = bot_result.get("confidence", 0.0)
    except Exception as err:
        intent = "error"
        response_text = f"An unexpected error occurred while communicating with the chatbot: {err}"
        confidence = 0.0

    # Append bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "intent": intent,
        "confidence": confidence
    })

    # Rerun to cleanly update the message thread
    st.rerun()

