import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime
import pytz

# ========== CONFIG ==========
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ✅ Updated working model
MODEL_NAME = "gemini-2.0-flash"

st.set_page_config(page_title="AI Conversational Assistant", page_icon="🤖", layout="wide")

# ========== UI ==========
st.markdown("""
<style>

/* Background */
body {
    background: radial-gradient(circle at top, #1a1a2e, #0f0f1a);
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}

/* Hide default */
#MainMenu, footer, header {visibility: hidden;}

/* Container */
.block-container {
    max-width: 850px;
    margin: auto;
    padding-bottom: 100px;
}

/* Header */
.header {
    text-align: center;
    padding: 20px;
}
.header h1 {
    font-size: 36px;
    background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header p {
    color: #aaa;
}

/* Chat */
.chat-box {
    max-height: 70vh;
    overflow-y: auto;
    padding: 10px;
}

/* Messages */
.msg {
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 20px;
    max-width: 75%;
    font-size: 15px;
}

/* User */
.user {
    background: linear-gradient(135deg, #6366f1, #9333ea);
    margin-left: auto;
    color: white;
    text-align: right;
}

/* Bot */
.bot {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Input box */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 65%;
    background: #ffffff;
    border-radius: 25px;
    padding: 10px;
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

/* Fix typing color issue */
[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    caret-color: #000000 !important;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("""
<div class="header">
    <h1>🤖 AI Conversational Assistant</h1>
    <p>Smart AI chatbot powered by Gemini</p>
</div>
""", unsafe_allow_html=True)

# ========== SESSION ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== DISPLAY ==========
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(f'<div class="msg {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========== AI FUNCTION ==========
def generate_reply(prompt):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        else:
            return "⚠️ No response generated."

    except Exception as e:
        err = str(e)

        if "429" in err:
            return "⚠️ API limit reached. Try again later."
        elif "404" in err:
            return "⚠️ Model not available. Check model name."
        else:
            return f"⚠️ Error: {err}"

# ========== INPUT ==========
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Time setup
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    text = prompt.lower()

    # Local quick responses
    if "date" in text:
        reply = f"📅 {now.strftime('%A, %d %B %Y')}"
    elif "time" in text:
        reply = f"⏰ {now.strftime('%I:%M %p IST')}"
    elif "jersey 18" in text:
        reply = "🏏 Jersey No.18 → Virat Kohli"
    else:
        reply = generate_reply(prompt)

    st.session_state.messages.append({"role": "bot", "content": reply})

    st.rerun()
