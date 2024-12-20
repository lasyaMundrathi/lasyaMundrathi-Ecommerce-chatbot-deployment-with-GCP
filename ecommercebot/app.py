import streamlit as st
from datetime import datetime
from retrieval_generation import generation
from ingestpinecone import ingestdata

print("hello...")

# Initialize Pinecone vector store and chain
vstore, inserted_ids = ingestdata(None)
chain = generation(vstore)

# Custom CSS for Chatbot UI
st.markdown(
    """
    <style>
    /* Global Styles */
    body {
        background-color: #1E1E2F;
    }
    .title-container {
        display: flex;
        align-items: center;
        background-color: #232335;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        color: white;
    }
    .title-container img {
        height: 50px;
        margin-right: 15px;
    }
    .title-container h1 {
        margin: 0;
        font-size: 24px;
    }

    /* Message Rows */
    .message-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .message-avatar {
        height: 40px;
        width: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .message {
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 70%;
        font-size: 16px;
        position: relative;
    }
    .user-message {
        background-color: #4CAF50;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .user-message:before {
        content: "";
        position: absolute;
        top: 10px;
        right: -10px;
        width: 0;
        height: 0;
        border-left: 10px solid #4CAF50;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
    }
    .bot-message {
        background-color: #007BFF;
        color: white;
    }
    .bot-message:before {
        content: "";
        position: absolute;
        top: 10px;
        left: -10px;
        width: 0;
        height: 0;
        border-right: 10px solid #007BFF;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
    }
    .timestamp {
        font-size: 12px;
        color: #A9A9A9;
        margin-top: 5px;
    }

    /* Input Section */
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .chat-input {
        flex: 1;
        padding: 10px;
        border-radius: 10px;
        border: none;
        outline: none;
        background-color: #2B2B3C;
        color: white;
    }
    .chat-button {
        padding: 10px 20px;
        background-color: #4C79F4;
        border: none;
        border-radius: 10px;
        color: white;
        cursor: pointer;
        font-size: 16px;
    }
    .chat-button:hover {
        background-color: #365BB8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Description
st.markdown(
    """
    <div class="title-container">
        <img src="https://static.vecteezy.com/system/resources/previews/016/017/018/non_2x/ecommerce-icon-free-png.png" alt="Chatbot Icon">
        <h1>E-Commerce Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat State Initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display Chat Messages
for message in st.session_state["messages"]:
    role, content, timestamp = message["role"], message["content"], message["timestamp"]
    if role == "user":
        st.markdown(
            f"""
            <div class="message-row">
                <div class="message user-message">{content}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="message-row">
                <img class="message-avatar" src="https://i.ibb.co/d5b84Xw/Untitled-design.png" alt="Bot Avatar">
                <div class="message bot-message">{content}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input(
        "Type your message:", key="input", placeholder="Type your message...", label_visibility="collapsed"
    )
with col2:
    send_button = st.button("Send", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Process User Input
if send_button and user_input:
    current_time = datetime.now().strftime("%H:%M")
    # Add user message
    st.session_state["messages"].append(
        {"role": "user", "content": user_input, "timestamp": current_time}
    )

    # Get bot response
    bot_response = chain(user_input)
    st.session_state["messages"].append(
        {"role": "bot", "content": bot_response, "timestamp": current_time}
    )

    # Clear input box and rerun
    st.rerun()
