import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage


doc_to_url = {'dəxʷtulalikʷ-rev.-5_23.pdf': 'https://tulaliplushootseed.com/wp-content/uploads/2023/03/d%C9%99x%CA%B7tulalik%CA%B7-rev.-5_23.pdf'}

doc_to_name = {'dəxʷtulalikʷ-rev.-5_23.pdf': 'Conversational Lushootseed'}

def nodes_to_markdown(nodes):
    markdown = []
    for node in nodes:
        if (file_name := node.metadata.get('file_name')) in doc_to_name:
            if 'page_label' in node.metadata:
                link_name = doc_to_name[file_name] + ', page ' + node.metadata['page_label']
                link_url = doc_to_url[file_name] + '#page=' + node.metadata['page_label']
            else:
                link_name = doc_to_name[file_name]
                link_url = doc_to_url[file_name]
            markdown.append(f'[{link_name}]({link_url})')
    return ', '.join(markdown)


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="storage")

st.title("Welcome to your dxʷləšucid chatbot!")
st.header("You can ask me questions about conversing in Lushootseed or click on one of the buttons containing common questions")
st.info("I am still under development so my answers might always be accurate. Please visit https://tulaliplushootseed.com/ for more Lushootseed learning resources!")

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

    if not index:
        index = load_index_from_storage(storage_context)
        chat_engine = index.as_chat_engine()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        streaming_response = chat_engine.stream_chat(prompt + ". Please provide detailed examples and assume that I am a beginner. Return the context that I have provided as part of your response.")
        response = st.write_stream(streaming_response.response_gen)
        context_md = nodes_to_markdown(streaming_response.source_nodes)
        if context_md:
            context = 'Please see these links for additional information: ' + context_md
            st.markdown(context)
            response += context
            
        
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