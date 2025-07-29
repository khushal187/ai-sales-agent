import streamlit as st
from smart_agent import (
    extract_hiring_info,
    recommend_service_gpt,
    generate_proposal,
    generate_follow_up_loop,
    log_structured_data,
    save_conversation_log,
)
import uuid

# Session state setup
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.extracted_data = None
    st.session_state.proposal = None
    st.session_state.initial_done = False

# Title
st.title("🤖 Smart Hiring Agent")
st.markdown("Chat with the assistant to find the right hiring solution for your business.")

# Chat display
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("Tell us your hiring requirement..."):
    # First message: Generate proposal
    if not st.session_state.initial_done:
        st.session_state.extracted_data = extract_hiring_info(user_input)
        service = recommend_service_gpt(st.session_state.extracted_data)
        st.session_state.proposal = generate_proposal(st.session_state.extracted_data, service)
        log_structured_data(st.session_state.session_id, st.session_state.extracted_data)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.proposal})
        st.session_state.initial_done = True

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(st.session_state.proposal)

    else:
        # Follow-up flow
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        full_chat = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
        )
        reply = generate_follow_up_loop(user_input, st.session_state.proposal, full_chat)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(reply)

        if any(x in user_input.lower() for x in ["exit", "bye", "thanks", "quit"]):
            save_conversation_log([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history])
