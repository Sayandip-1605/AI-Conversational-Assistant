import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime
import pytz

# ========== CONFIG ==========
# Load API key (Streamlit Secrets + local fallback)
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(page_title="AI Conversational Assistant", page_icon="🤖", layout="wide")

# ========== UI ==========
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1a1a2e, #0f0f1a);
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}

.block-container {
    max-width: 850px;
    margin: auto;
    padding-bottom: 100px;
}

.header {
    text-align: center;
    padding: 20px;
}
.header h1 {
    font-size: 34px;
    background: linear-gradient(90deg, #4f46e5, #9333ea, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header p { color: #aaa; }

.chat-box {
    max-height: 70vh;
    overflow-y: auto;
    padding: 10px;
}

.msg {
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 20px;
    max-width: 75%;
}

.user {
    background: linear-gradient(135deg, #6366f1, #9333ea);
    margin-left: auto;
    color: white;
    text-align: right;
}

.bot {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: #fff;
    border-radius: 20px;
    padding: 10px;
}

[data-testid="stChatInput"] textarea {
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("""
<div class="header">
    <h1>🤖 AI Conversational Assistant</h1>
    <p>Powered by Gemini API • Smart intelligent responses</p>
</div>
""", unsafe_allow_html=True)

# ========== SESSION ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== DISPLAY ==========
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg bot">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========== AI FUNCTION ==========
def generate_reply(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "⚠️ No response generated."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ========== INPUT ==========
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    text = prompt.lower()

    # Local responses
    if "date" in text:
        reply = f"📅 {now.strftime('%A, %d %B %Y')}"
    elif "time" in text:
        reply = f"⏰ {now.strftime('%I:%M %p IST')}"
    else:
        reply = generate_reply(prompt)

    st.session_state.messages.append({"role": "bot", "content": reply})
    st.rerun()
