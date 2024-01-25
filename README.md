# Chatbot with Local LLM Custom Front-End:

**See the app live here!:**  https://shah-mu-chatbot.streamlit.app/

This code implements a Streamlit-based front-end for interacting with a local installation of the Llama2 language model. The application allows users to engage in a conversation with the language model, providing instructions and receiving responses.

## Setup and Dependencies

Make sure you have the necessary dependencies installed by running:

```bash
pip install openai streamlit
```

## Usage

1. Run the script.
2. Enter specific instructions in the "Instructions" tab, if desired.
3. Press "Enter To Start Chat" to initiate a conversation.
4. Communicate with the chatbot by entering messages in the input box.
5. Optionally, delete the last generated message by clicking "Delete Last Generated Message."
6. Save the conversation by clicking the "Save Conversation (JSON)" button in the "Save Conversation" tab.

## Instructions Tab

In the "Instructions" tab, you can enter specific instructions for the chatbot, reinforcing them every time you submit a new message. Use this feature to guide the model's responses according to your requirements.

## Save Conversation Tab

In the "Save Conversation" tab, you can download the conversation as a JSON file. Additionally, you can upload past conversations for review and continuation.

**Note:** Ensure that you unmount the uploaded JSON file by selecting (×) before continuing to use the application.

## Important Points

- The code uses the Streamlit library for creating a user-friendly interface.
- Messages are stored in the session state to maintain the conversation history.
- The OpenAI API is accessed through a local Llama2 instance for generating model responses.
- The application provides an interactive chat interface, allowing users to communicate with the language model.

Feel free to customize the code to fit your specific use case and preferences.
