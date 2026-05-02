# 🌱 EcoLife Assistant Bot
### LLM-Based Environmental Chatbot with Gemini API Integration

> **Final Project** | AI Engineering | Google Gemini + Streamlit

---

<img width="959" height="440" alt="image" src="https://github.com/user-attachments/assets/c1dda833-f1c3-477d-a096-01fc5649e6a0" />


## 📋 Table of Contents
1. [Project Background](#1-project-background)
2. [Problem Statement](#2-problem-statement)
3. [Solution](#3-solution)
4. [Objectives](#4-objectives)
5. [System Design](#5-system-design)
6. [Features](#6-features)
7. [Tech Stack](#7-tech-stack)
8. [Project Structure](#8-project-structure)
9. [How to Run](#9-how-to-run)
10. [UI Explanation](#10-ui-explanation)
11. [Bot Personality & Prompt Design](#11-bot-personality--prompt-design)
12. [API Integration Details](#12-api-integration-details)
13. [Conversation Memory](#13-conversation-memory)

---

## 1. Project Background

Environmental degradation and climate change are among the most critical challenges of our time. Despite widespread awareness, many people struggle to translate concern into daily action. The gap between **knowing** and **doing** is where technology can play a transformative role.

Large Language Models (LLMs) represent a breakthrough in human-computer interaction — they can explain complex topics conversationally, provide personalized guidance, and motivate behavior change through natural dialogue.

This project harnesses **Google Gemini's** powerful language capabilities to create **EcoLife Assistant**, an AI chatbot specifically designed to guide everyday users toward more sustainable habits.

---

## 2. Problem Statement

| Problem | Impact |
|---|---|
| Environmental information is complex and technical | General public disengages |
| Eco-advice is generic, not personalized | Low adoption of sustainable habits |
| No interactive, conversational eco-guide exists | Users lose motivation quickly |
| Climate anxiety without actionable steps | Feeling overwhelmed, not empowered |

**Core question:** *How can AI make environmental education accessible, personal, and actionable for everyday people?*

---

## 3. Solution

**EcoLife Assistant** is a conversational AI chatbot powered by Google Gemini that:

- 💬 Engages users in natural, friendly conversation about sustainability
- 🎓 Explains complex environmental topics in simple language
- 🔁 Maintains conversation history for personalized, contextual advice
- 📋 Provides practical, actionable eco-tips tailored to user questions
- 🌍 Covers a wide range of topics: waste, energy, food, climate, shopping, water

---

## 4. Objectives

| # | Objective | How Achieved |
|---|---|---|
| 1 | Integrate Gemini LLM for intelligent responses | `google-generativeai` SDK with ChatSession |
| 2 | Build an accessible chat UI | Streamlit with custom CSS |
| 3 | Maintain conversation memory | Gemini's built-in `ChatSession` history |
| 4 | Friendly, educational tone | Carefully designed system prompt |
| 5 | Cover key environmental topics | Prompt scoping + topic detection |
| 6 | Track user engagement | Session stats (messages, topics) |

---

## 5. System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    EcoLife Assistant                         │
│                                                             │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │   Streamlit UI   │         │    Google Gemini API     │ │
│  │                  │         │                          │ │
│  │ • Chat interface │ ──────► │ • gemini-2.0-flash       │ │
│  │ • Sidebar info   │         │ • System prompt          │ │
│  │ • Quick prompts  │ ◄────── │ • ChatSession (memory)   │ │
│  │ • Session stats  │         │ • Temperature: 0.75      │ │
│  └──────────────────┘         └──────────────────────────┘ │
│           │                                                 │
│  ┌────────▼────────┐                                        │
│  │  Session State   │                                       │
│  │                  │                                       │
│  │ • messages[]     │  ← Full chat history (UI display)    │
│  │ • chat_session   │  ← Gemini ChatSession (LLM memory)   │
│  │ • topics_covered │  ← Session analytics                 │
│  │ • msg_count      │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User types message
        │
        ▼
Streamlit captures input (st.chat_input)
        │
        ▼
Message stored in st.session_state.messages (for UI)
        │
        ▼
send_message() called → chat_session.send_message()
        │
        ▼
Gemini API receives: [system_prompt + full history + new message]
        │
        ▼
Gemini returns response text
        │
        ▼
Response stored in st.session_state.messages
        │
        ▼
st.rerun() → UI re-renders with new message
```

---

## 6. Features

### Core Features

| Feature | Description |
|---|---|
| 🤖 **Gemini AI Integration** | Uses `gemini-2.0-flash` for fast, intelligent responses |
| 💬 **Chat Interface** | Clean, bubble-style chat UI with user/bot avatars |
| 🧠 **Conversation Memory** | Full chat history maintained via Gemini's `ChatSession` |
| 🌿 **Eco Personality** | Carefully crafted system prompt for educational, friendly tone |
| ⚡ **Quick Start Prompts** | 6 clickable starter questions for instant engagement |
| 📊 **Session Analytics** | Live count of messages sent and topics discussed |
| 🗑️ **Clear Chat** | Reset conversation and start fresh |
| 🔑 **API Key Input** | Secure sidebar input (password field) |

### UI Features

| Feature | Description |
|---|---|
| 🎨 **Dark Eco Theme** | Deep forest-green color palette, DM Serif + DM Sans fonts |
| 📱 **Responsive Layout** | Sidebar + main chat area, max 900px centered |
| 🫧 **Chat Bubbles** | User (lime) and bot (dark green) styled differently |
| ⏱️ **Timestamps** | Each message shows the time sent |
| 🏷️ **Topic Chips** | Topics covered shown as tags in sidebar |

---

## 7. Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.0 Flash (`gemini-2.0-flash`) |
| **SDK** | `google-generativeai` ≥ 0.8 |
| **UI Framework** | Streamlit ≥ 1.35 |
| **Styling** | Custom CSS (injected via `st.markdown`) |
| **Fonts** | Google Fonts: DM Serif Display + DM Sans |
| **Language** | Python 3.10+ |
| **State Management** | Streamlit `session_state` |

---

## 8. Project Structure

```
ecolife-assistant/
│
├── app.py                  # Main Streamlit application (all-in-one)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

> **Design choice:** Single-file architecture (`app.py`) keeps the project simple and easy to run, perfect for a final project demonstration.

---

## 9. How to Run

### Prerequisites
- Python 3.10 or higher
- A free Google Gemini API key (get one at [aistudio.google.com](https://aistudio.google.com))

### Step-by-Step Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/ecolife-assistant.git
cd ecolife-assistant
```

**2. Create a virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open in browser**
The app automatically opens at: `http://localhost:8501`

**6. Connect your API key**
- Paste your Gemini API key in the sidebar
- Click **Connect 🔗**
- Start chatting! 🌱

### Optional: Use `.env` for auto-loading key
```bash
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_key_here
```

---

## 10. UI Explanation

```
┌─────────────────────────────────────────────────────────────┐
│  SIDEBAR                    │  MAIN AREA                    │
│  ─────────────────────────  │  ─────────────────────────    │
│  🔑 API Key input           │  EcoLife Assistant 🌱         │
│  [Connect button]           │  Your AI guide to a greener   │
│                             │  lifestyle                    │
│  📊 Session Stats           │                               │
│  [3 messages] [2 topics]    │  ┌─── Welcome Card ──────┐   │
│                             │  │  Hello, Eco Warrior!   │   │
│  ♻️ Waste  ⚡ Energy         │  │  [Starter prompt btns] │   │
│                             │  └────────────────────────┘   │
│  🤖 About EcoLife Bot       │                               │
│  [Topics list]              │  👤 User bubble (lime)        │
│                             │  🌱 Bot bubble (dark green)   │
│  💡 Quick Tips              │  👤 User bubble               │
│  [Usage hints]              │  🌱 Bot bubble                │
│                             │                               │
│  [🗑️ Clear Chat]            │  ─────────────────────────    │
│                             │  [Type your message... 🌿]    │
│  Made with ❤️ for planet    │                               │
└─────────────────────────────┴───────────────────────────────┘
```

### Color Palette

| Color | Hex | Usage |
|---|---|---|
| Background | `#0d1a0f` | App background (deep forest) |
| Card | `#132017` | Cards, bot bubbles |
| Accent Green | `#4ade80` | Titles, highlights, bot name |
| Accent Lime | `#a3e635` | User bubble text |
| Text Muted | `#6b9e6e` | Secondary text, timestamps |
| Border | `#1f3323` | Card borders |

---

## 11. Bot Personality & Prompt Design

The system prompt is carefully engineered to produce consistent, high-quality responses:

**Key prompt principles:**

1. **Role definition** — Clearly defines EcoLife as a "warm, knowledgeable, encouraging environmental guide"
2. **Mission scoping** — Lists exactly what topics to cover, preventing hallucination into unrelated areas  
3. **Tone constraints** — "Never preachy or judgmental" prevents the bot from making users feel guilty
4. **Response format rules** — Short paragraphs, emojis, numbered lists for readability
5. **Audience awareness** — "Everyday people — students, families, young adults" keeps language accessible
6. **Positivity framing** — Focus on solutions and hope, not doom — maintains user motivation

---

## 12. API Integration Details

```python
# Model configuration
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",        # Fast, capable model
    generation_config=genai.GenerationConfig(
        temperature=0.75,                  # Balanced (not too creative, not too rigid)
        top_p=0.92,                        # Nucleus sampling
        top_k=40,                          # Token selection pool
        max_output_tokens=1024,            # ~700-800 words max
    ),
    system_instruction=SYSTEM_PROMPT,     # Personality injected here
)

# Chat session (maintains history automatically)
chat_session = model.start_chat(history=[])
response = chat_session.send_message(user_input)
```

**Why `gemini-2.0-flash`?**
- Fast response times (ideal for chat)
- Excellent instruction following
- Strong knowledge of environmental topics
- Cost-effective for demos and student projects

---

## 13. Conversation Memory

EcoLife uses **Gemini's built-in `ChatSession`** for memory, which means:

- The SDK automatically appends each user + model turn to the history
- Every new message is sent with the FULL conversation context
- No manual history management needed
- Responses are contextually aware of the entire conversation

This is different from "fake memory" (just passing the last N messages) — Gemini genuinely sees everything said in the session, enabling natural multi-turn conversations like:

```
User: "What's composting?"
Bot:  "Composting is... [explanation]"
User: "How do I start?"  ← Bot knows "start" refers to composting
Bot:  "To start composting at home... [practical steps]"
```

---

## 📄 License

MIT License — free to use, modify, and share.

---

*🌍 Built with love for the planet. Every line of code is one small step toward a greener future.*
