import streamlit as st
from groq import Groq

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 Groq AI Chatbot")

# ---------------------------
# LOAD API KEY (FROM STREAMLIT SECRETS)
# ---------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
    st.stop()

# ---------------------------
# CHAT MEMORY
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# ---------------------------
# USER INPUT
# ---------------------------
user_input = st.chat_input("Type your message...")

# ---------------------------
# CHAT LOGIC
# ---------------------------
if user_input:
    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(("user", user_input))

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # show bot reply
    st.chat_message("assistant").write(bot_reply)
    st.session_state.chat_history.append(("assistant", bot_reply))