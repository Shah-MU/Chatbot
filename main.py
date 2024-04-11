from openai import OpenAI
import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
import json



st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",  # Open book icon
    layout="wide",  # Set the layout to wide
)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """


st.markdown("### AI PET ADVISOR")
st.markdown("*Using a local install of Llama2*")

# Initialize Firebase app
if not firebase_admin._apps:
    # Initialize Firebase app
    cred = credentials.Certificate("sprint1-dataflow-test-firebase-adminsdk-j3s7u-7ad4f76319.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sprint1-dataflow-test-default-rtdb.firebaseio.com/'
    })

# Firebase reference
ref = db.reference('pet_info')
pet_info = ref.get()
prompt = pet_info.get('pet_string')




client = OpenAI(base_url=st.secrets["LLM"], api_key="not-needed")

tab1 = st.sidebar.tabs(['Instructions'])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama2"

if "messages" not in st.session_state:
    st.session_state.messages = []

# # Sidebar section for session state download
# def download_session_state():
#     session_state_json = json.dumps(st.session_state.messages, indent=2)
#     session_state_bytes = session_state_json.encode("utf-8")

#     st.download_button(
#         label="Save Conversation (JSON)",
#         data=session_state_bytes,
#         file_name=f"{datetime.today().strftime('%Y-%m-%d')}.json",
#         key="download_session_state",
#     )

# with tab2:
#     download_session_state()
#     # Sidebar section for file upload
#     uploaded_file = st.file_uploader("Upload Past Conversations(JSON)", type=["json"])

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    st.session_state.messages = json.loads(content)
    st.sidebar.error('''Select (×) to unmount JSON to continue using the application''')

# Display only user and assistant messages to the end user
for idx, message in enumerate(st.session_state.messages):
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Add a button to delete the last message
            if st.button(f"🗑️", key=f"delete_{message['role']}_{idx}"):
                st.session_state.messages.pop(idx)
                st.rerun()

# Reinforce special instructions every time the user enters a message
with tab1:
    user_instructions = f"You are a AI pet Health advisor, ONLY ANSWER QUESTIONS RELATED TO PETS/ANIMALS, if a user asks an unrelated question please tell them that you cannot respond, Here is some info about the user's pet: User: {prompt}"
    st.markdown(
        """
### Note: 

This is an AI assistent which can help you understand your pets better!

""")

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
        message_placeholder.markdown(full_response)

        # Reinforce special instructions after every user input
        if user_instructions:
            st.session_state.messages.append({"role": "system", "content": user_instructions})

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()
