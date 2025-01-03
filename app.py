# The following file is based on the example of the link.
# https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/

import streamlit as st
# from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.core import VectorStoreIndex,Settings
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader


openai.api_key = st.secrets.openai_key
st.header("Chat with the Streamlit docs 💬 📚")

if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5,system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
        index = VectorStoreIndex.from_documents(docs)
        return index


index = load_data()

chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history



#  ServiceContext is deprecated. Use llama_index.settings.Settings
#
# instead, or pass in modules to local functions/methods/interfaces.
#
# See the docs for updated usage/migration:
#
# https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/
