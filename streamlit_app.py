import streamlit as st
from openai import OpenAI

system_message = '''
You are a bot that always gets a user question, then answer

You then ask "DO YOU WANT MORE INFO".

Keep on asking "DO YOU WANT MORE INFO" after each answer until user say no.

If the user says no, go back to asking the simple question "How can I help you?".

Keep answers short.

Always provide answers that are easy to understand for a "10 Year Old"

If you do no know the answer just state "I DO NOT KNOW"

'''
# Show title and description.
st.title( "MY Lab3 question answering chatbot")

if 'client' not in st.session_state:
    api_key = st.secrets['openai_key']
    st.session_state.client = OpenAI(api_key=st.secrets["openai_key"])

if "messages" not in st.session_state:
    st.session_state["messages"] = \
    [{"role": "system", "content": system_message},
     {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] != "system":    
        chat_msg = st.chat_message(msg["role"])
        chat_msg.write(msg["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    client = st.session_state.client
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        stream=True
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

    if len(st.session_state.messages) > 5:
        st.session_state.messages = st.session_state.messages[-5:]
