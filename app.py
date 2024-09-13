import streamlit as st
import os
from llama_index.core import StorageContext, load_index_from_storage


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"



# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="storage")

st.title("Welcome to your dxʷləšucid chatbot!")
st.header("You can ask me questions about conversing in Lushootseed")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

index = None
chat_engine = None

def handle_prompt(prompt):
    global index
    global chat_engine

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not index:
        os.environ['OPENAI_API_KEY'] = openai_api_key
        index = load_index_from_storage(storage_context)
        chat_engine = index.as_chat_engine()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        streaming_response = chat_engine.stream_chat(prompt)
        response = st.write_stream(streaming_response.response_gen)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


prebaked_prompts = ['How do I introduce myself', 'How do I ask your name', 'How do I count from 1 to 10']

cols = st.columns(len(prebaked_prompts))

# Accept user input
prompt = None

for col, text in zip(cols, prebaked_prompts):
    if st.button(text):
        prompt = text + ' in Lushootseed'
        handle_prompt(prompt)

if prompt := st.chat_input("Ask me a question such as how do I introduce myself in Lushootseed?"):
    handle_prompt(prompt)    