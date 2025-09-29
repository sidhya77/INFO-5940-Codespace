# 1 ─ Imports
# 2 Standard library
from pathlib import Path # 3
import os # 4


# 5 Third‑party
import streamlit as st # 6
# If you're using OpenAI python client v1.x:
from openai import OpenAI # 7


# 8 ─ Configuration
# 9 Read API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # 10
if not OPENAI_API_KEY: # 11
    st.stop() # 12 Halts app if key missing


client = OpenAI(api_key=OPENAI_API_KEY) # 13


# 14 App title & basic page config
st.set_page_config(page_title="Week 5B Chatbot", page_icon="💬") # 15
st.title("Week 5B – Chatbot + Knowledge Base Demo") # 16
st.caption("Stream responses • Session state • KB in user role") # 17
# 18 ─ Load optional knowledge base (plain text)
KB_PATH = Path("data/important_knowledge.txt") # 19
kb_text = "" # 20
if KB_PATH.exists(): # 21
    kb_text = KB_PATH.read_text(encoding="utf-8").strip() # 22


# 23 ─ Initialize conversation state
if "messages" not in st.session_state: # 24
    st.session_state.messages = [] # 25


# 26 ─ Sidebar controls
with st.sidebar: # 27
    st.subheader("Settings") # 28
model = st.selectbox(
"Model", [
"gpt-4o-mini", "gpt-4.1-mini", "o4-mini" # 29 (examples)
], index=0
)
temperature = st.slider("Temperature", 0.0, 1.2, 0.3, 0.1) # 30
use_kb = st.toggle("Include knowledge base in user prompt", value=bool(kb_text)) # 31


# 32 ─ Render previous messages
for m in st.session_state.messages: # 33
    st.chat_message(m["role"]).write(m["content"]) # 34


# 35 ─ Chat input
user_input = st.chat_input("Ask me anything…") # 36


if user_input: # 37
# 38 Push the user's message
    st.session_state.messages.append({"role": "user", "content": user_input}) # 39


# 40 Construct the request messages
request_messages = [] # 41


# 42 (Optional) Prepend KB in the user role
if use_kb and kb_text:
    kb_header = "Here is relevant background knowledge (provided by the user):\n\n" # 43
request_messages.append({
"role": "user",
"content": kb_header + kb_text
}) # 44


# 45 Append chat history (user/assistant roles only)
for m in st.session_state.messages:
    request_messages.append({"role": m["role"], "content": m["content"]}) # 46


# 47 Stream the assistant reply
with st.chat_message("assistant"): # 48
    placeholder = st.empty() # 49
    stream_text = "" # 50


# 51 OpenAI chat.completions stream
stream = client.chat.completions.create(
model=model,
temperature=temperature,
messages=request_messages,
stream=True
) # 52


for chunk in stream: # 53
    delta = chunk.choices[0].delta # 54
token = getattr(delta, "content", None) # 55
if token:
    stream_text += token # 56
placeholder.write(stream_text) # 57


# 58 Save assistant message to history
st.session_state.messages.append({
"role": "assistant", "content": stream_text
}) # 59