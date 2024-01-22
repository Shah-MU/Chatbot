from openai import OpenAI
import streamlit as st

st.markdown("### Local LLM Custom Front-End")

client = OpenAI(base_url="http://144.172.137.100:1234/v1", api_key="not-needed")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama2"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display only user and assistant messages to the end user
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Reinforce special instructions every time the user enters a message
user_instructions = st.sidebar.text_area("Enter Specific Instructions:", "")
if user_instructions:
    st.session_state.messages.append({"role": "system", "content": user_instructions})

# "Delete Last Generated Message" button
if st.sidebar.button("Delete Last Generated Message"):
    # Find the index of the last assistant message
    last_assistant_index = None
    for i, message in enumerate(reversed(st.session_state.messages)):
        if message["role"] == "assistant":
            last_assistant_index = len(st.session_state.messages) - 1 - i
            break

    # Remove the last assistant message if found
    if last_assistant_index is not None:
        st.session_state.messages.pop(last_assistant_index)

    # Use st.experimental_rerun to force a rerun of the app
    st.experimental_rerun()

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        # Reinforce special instructions after every user input
        if user_instructions:
            st.session_state.messages.append({"role": "system", "content": user_instructions})

    st.session_state.messages.append({"role": "assistant", "content": full_response})
