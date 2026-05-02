"""
EcoLife Assistant Bot 🌱
LLM-Based Environmental Chatbot with Gemini API Integration
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(
    page_title="EcoLife Assistant 🌱",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-dark:      #0d1a0f;
    --bg-card:      #132017;
    --bg-input:     #1a2e1d;
    --accent-green: #4ade80;
    --accent-lime:  #a3e635;
    --text-primary: #e8f5e9;
    --text-muted:   #6b9e6e;
    --border:       #1f3323;
    --user-bubble:  #1e3a22;
    --bot-bubble:   #132017;
    --shadow:       0 4px 24px rgba(0,0,0,0.4);
}

/* === GLOBAL === */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* === SEMBUNYIKAN BRANDING — HANYA INI, TIDAK LEBIH === */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
/* JANGAN sentuh header, toolbar, atau apapun yang berkaitan dengan sidebar toggle */

/* === SIDEBAR BACKGROUND SAJA === */
[data-testid="stSidebar"] > div:first-child {
    background-color: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

/* === MAIN CONTAINER === */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 860px !important;
}

/* === JUDUL === */
.eco-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: var(--accent-green);
    letter-spacing: -0.5px;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.eco-subtitle {
    font-size: 0.92rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

/* === CHAT BUBBLES === */
.chat-wrap { display:flex; flex-direction:column; gap:1rem; margin-bottom:1.5rem; }

.user-msg, .bot-msg {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    animation: fadeUp 0.25s ease;
}
.user-msg { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}

.avatar {
    width:36px; height:36px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0;
}
.avatar-user { background:#1e3a22; border:1.5px solid #4ade80; }
.avatar-bot  { background:#132017; border:1.5px solid #6b9e6e; }

.bubble {
    padding:0.8rem 1.1rem;
    border-radius:1.1rem;
    max-width:76%;
    font-size:0.93rem;
    line-height:1.65;
    box-shadow: var(--shadow);
}
.bubble-user {
    background:#1e3a22;
    border-top-right-radius:4px;
    border:1px solid #2d5230;
    color: var(--accent-lime);
}
.bubble-bot {
    background:#132017;
    border-top-left-radius:4px;
    border:1px solid var(--border);
    color: var(--text-primary);
}
.msg-time {
    font-size:0.68rem; color:var(--text-muted);
    margin-top:0.25rem; text-align:right;
}
.user-msg .msg-time { text-align:left; }

/* === INPUT === */
[data-testid="stChatInput"] textarea {
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius:12px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 2px rgba(74,222,128,0.15) !important;
}

/* === DIVIDER === */
.eco-divider { border:none; border-top:1px solid var(--border); margin:1rem 0; }

/* === STAT BOXES === */
.stat-row { display:flex; gap:0.5rem; margin-bottom:0.8rem; }
.stat-box {
    flex:1; background:var(--bg-dark); border:1px solid var(--border);
    border-radius:10px; padding:0.6rem; text-align:center;
}
.stat-num { font-size:1.3rem; font-weight:600; color:var(--accent-green); }
.stat-lbl { font-size:0.68rem; color:var(--text-muted); }

/* === INFO CARD === */
.info-card {
    background:var(--bg-dark); border:1px solid var(--border);
    border-radius:12px; padding:0.9rem 1rem;
    margin-bottom:0.8rem; font-size:0.85rem;
    color:var(--text-muted); line-height:1.6;
}
.info-card-title {
    font-weight:600; color:var(--accent-green);
    font-size:0.82rem; text-transform:uppercase;
    letter-spacing:0.05em; margin-bottom:0.4rem;
}

/* === CHIPS === */
.chips-row { display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.8rem; }
.chip {
    background:var(--bg-dark); border:1px solid var(--border);
    border-radius:999px; padding:0.25rem 0.7rem;
    font-size:0.75rem; color:var(--text-muted);
}
</style>
""", unsafe_allow_html=True)


# ── SYSTEM PROMPT ──────────────────────────────────────────────
SYSTEM_PROMPT = """
You are EcoLife Assistant 🌱 — a warm, knowledgeable, and encouraging environmental guide.

Your mission:
- Help users adopt sustainable, eco-friendly habits in their daily lives
- Explain environmental concepts in simple, clear language (like a caring tutor)
- Give practical, actionable tips about reducing waste, saving energy, and protecting nature
- Answer questions about climate change, biodiversity, and sustainability
- Inspire and motivate users without making them feel guilty

Personality: Friendly, warm, encouraging, never preachy or judgmental.
Style: Short paragraphs, 1-2 emojis, numbered tips, end with encouragement.

Topics: waste reduction, energy saving, sustainable food, water conservation,
climate change, eco-shopping, biodiversity, green technology.

Audience: students, families, young adults — keep it real and actionable!
"""


# ── GEMINI CONFIG ──────────────────────────────────────────────
def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=genai.GenerationConfig(
            temperature=0.75, top_p=0.92, top_k=40, max_output_tokens=1024,
        ),
        system_instruction=SYSTEM_PROMPT,
    )


# ── SESSION STATE ──────────────────────────────────────────────
for key, default in [
    ("messages", []),
    ("chat_session", None),
    ("model", None),
    ("api_key_set", False),
    ("msg_count", 0),
    ("topics_covered", set()),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── HELPERS ────────────────────────────────────────────────────
def init_chat(model):
    return model.start_chat(history=[])

def send_message(text: str) -> str:
    try:
        return st.session_state.chat_session.send_message(text).text
    except Exception as e:
        return f"⚠️ Error: {e}"

def render_msg(role, content, t):
    if role == "user":
        st.markdown(f"""
        <div class="user-msg">
          <div class="avatar avatar-user">👤</div>
          <div><div class="bubble bubble-user">{content}</div>
          <div class="msg-time">{t}</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-msg">
          <div class="avatar avatar-bot">🌱</div>
          <div><div class="bubble bubble-bot">{content}</div>
          <div class="msg-time">{t}</div></div>
        </div>""", unsafe_allow_html=True)

def detect_topic(text):
    tm = {
        "♻️ Waste":    ["recycle","waste","plastic","trash","compost"],
        "⚡ Energy":   ["energy","electricity","solar","power","carbon"],
        "🌊 Water":    ["water","drought","ocean"],
        "🥦 Food":     ["food","diet","plant","vegan","vegetarian","eat"],
        "🌡️ Climate":  ["climate","warming","greenhouse"],
        "🛍️ Shopping": ["shopping","fashion","buy","consume"],
    }
    t = text.lower()
    for topic, kws in tm.items():
        if any(k in t for k in kws):
            return topic
    return None


# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 EcoLife Assistant")
    st.caption("Powered by Gemini AI")
    st.divider()

    st.markdown("**🔑 Gemini API Key**")
    api_key_input = st.text_input(
        "API Key", type="password",
        placeholder="Paste your AIza... key here",
        label_visibility="collapsed",
    )

    if st.button("Connect 🔗", use_container_width=True):
        if api_key_input.strip():
            try:
                m = configure_gemini(api_key_input.strip())
                st.session_state.model = m
                st.session_state.chat_session = init_chat(m)
                st.session_state.api_key_set = True
                st.success("Connected! Let's go green 🌱")
            except Exception as e:
                st.error(f"Failed: {e}")
        else:
            st.warning("Please enter your API key.")

    st.divider()

    st.markdown("**📊 Session Stats**")
    col1, col2 = st.columns(2)
    col1.metric("Messages", st.session_state.msg_count)
    col2.metric("Topics", len(st.session_state.topics_covered))

    if st.session_state.topics_covered:
        st.markdown(" ".join([f"`{t}`" for t in st.session_state.topics_covered]))

    st.divider()

    st.markdown("""
**🤖 About EcoLife Bot**

I'm your personal sustainability coach!

♻️ Waste & recycling  
⚡ Energy saving  
🥦 Eco-friendly food  
🌡️ Climate change  
🛍️ Sustainable shopping  
🌊 Water conservation  
🌿 Daily green habits
""")

    st.markdown("""
**💡 Tips**
- Be specific in your questions
- Ask for a "daily plan"
- Request a quiz on eco facts!
""")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.topics_covered = set()
        if st.session_state.model:
            st.session_state.chat_session = init_chat(st.session_state.model)
        st.rerun()

    st.caption("🌍 Made with ❤️ for the planet")


# ── MAIN AREA ──────────────────────────────────────────────────
st.markdown('<div class="eco-title">EcoLife Assistant 🌱</div>', unsafe_allow_html=True)
st.markdown('<div class="eco-subtitle">Your AI guide to a greener, more sustainable lifestyle</div>', unsafe_allow_html=True)

STARTERS = [
    "🗑️ How do I start composting?",
    "⚡ Easy ways to save electricity?",
    "🥦 What is a sustainable diet?",
    "🌡️ Explain climate change simply",
    "🛍️ How to shop sustainably?",
    "💧 Water saving tips at home",
]

# Welcome screen
if not st.session_state.messages:
    st.markdown("""
    <div style="background:#132017; border:1px dashed #2d5230; border-radius:16px;
                padding:2rem; text-align:center; margin-bottom:1.5rem;">
        <div style="font-size:2.2rem;">🌍</div>
        <div style="font-family:'DM Serif Display',serif; font-size:1.3rem;
                    color:#4ade80; margin:0.4rem 0;">Hello, Eco Warrior!</div>
        <div style="color:#6b9e6e; font-size:0.9rem; max-width:400px; margin:0 auto; line-height:1.7;">
            I'm here to help you live a more sustainable life —
            one small step at a time. Ask me anything about
            the environment, green habits, or climate change!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:#6b9e6e; font-size:0.82rem;">💬 Try asking...</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, prompt in enumerate(STARTERS):
        with cols[i % 3]:
            if st.button(prompt, key=f"s{i}", use_container_width=True):
                if st.session_state.api_key_set:
                    now = datetime.now().strftime("%H:%M")
                    st.session_state.messages.append({"role":"user","content":prompt,"time":now})
                    with st.spinner("EcoBot is thinking 🌱..."):
                        reply = send_message(prompt)
                    st.session_state.messages.append({"role":"assistant","content":reply,"time":now})
                    st.session_state.msg_count += 1
                    t = detect_topic(prompt)
                    if t: st.session_state.topics_covered.add(t)
                    st.rerun()
                else:
                    st.warning("Please connect your Gemini API key in the sidebar first.")

# Chat history
if st.session_state.messages:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        render_msg(msg["role"], msg["content"], msg["time"])
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="eco-divider">', unsafe_allow_html=True)

# Chat input
if st.session_state.api_key_set:
    user_input = st.chat_input("Ask me anything about sustainability... 🌿")
    if user_input:
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role":"user","content":user_input,"time":now})
        t = detect_topic(user_input)
        if t: st.session_state.topics_covered.add(t)
        with st.spinner("EcoBot is thinking 🌱..."):
            reply = send_message(user_input)
        st.session_state.messages.append({"role":"assistant","content":reply,"time":now})
        st.session_state.msg_count += 1
        st.rerun()
else:
    st.markdown("""
    <div style="text-align:center; padding:1rem; color:#6b9e6e; font-size:0.9rem;
                background:#132017; border-radius:12px; border:1px dashed #2d5230;">
        🔑 Please enter your <strong>Gemini API key</strong> in the sidebar to start chatting.
        <br><small>Get a free key at 
        <a href="https://aistudio.google.com" target="_blank" style="color:#4ade80;">
        aistudio.google.com</a></small>
    </div>
    """, unsafe_allow_html=True)
