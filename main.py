from openai import OpenAI
import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
)

hide_streamlit_style = """
<style>
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
#MainMenu,
header,
footer {
    visibility: hidden;
    height: 0%;
    position: fixed;
}
</style>
"""

st.markdown("### AI PET ADVISOR")
st.markdown("*Using a local install of Llama2*")

if not firebase_admin._apps:
    cred = credentials.Certificate("sprint1-dataflow-test-firebase-adminsdk-j3s7u-7ad4f76319.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sprint1-dataflow-test-default-rtdb.firebaseio.com/'
    })

ref = db.reference('pet_info')
pet_info = ref.get()
prompt = pet_info.get('pet_string')

client = OpenAI(base_url=st.secrets["LLM"], api_key="not-needed")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama2"

if "messages" not in st.session_state:
    st.session_state.messages = []

for idx, message in reversed(list(enumerate(st.session_state.messages))):
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Generate a unique key for each delete button
            delete_button_key = f"delete_{message['role']}_{idx}_{message['content']}"
            if st.button(f"🗑️", key=delete_button_key):
                st.session_state.messages.pop(idx)
                st.rerun()

with st.sidebar:
    st.markdown("### Instructions")
    st.write("This AI Assistant has been fine-tuned on your pet's needs. Feel free to ask it about any concerns you may have about your pet!")

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

for idx, message in enumerate(st.session_state.messages):
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_instructions = f"You are an AI pet Health advisor. Only answer questions related to pets/animals. If a user asks an unrelated question, please tell them that you cannot respond. Here is some info about the user's pet: User: {prompt}"

if user_instructions:
    st.session_state.messages.append({"role": "system", "content": user_instructions})

if prompt := st.chat_input("Enter To Start Chat"):
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
        message_placeholder.markdown(ful
