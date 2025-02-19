import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Q&A Demo")

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)


model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.header("Gemini Conversational AI ")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    with st.spinner("Processing..."):  # Add a loading animation
        response = get_gemini_response(user_input)
        st.session_state['chat_history'].append(("You", user_input))
        st.subheader("The Response is")
        
        # Process the response chunks safely
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:  # Check if 'text' exists
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
            else:
                st.error("Sorry, I didn't get a proper response.")  # Handle missing text case


st.subheader("The Chat history is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
