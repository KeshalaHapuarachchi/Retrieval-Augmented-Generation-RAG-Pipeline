import streamlit as st
import requests
import os
import json

st.title("ThankYou GPT POC")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send requests to your FastAPI backend
def send_to_openai_api(prompt):
    url = "http://localhost:5001/analyze_comment"  # Update with your FastAPI endpoint
    headers = {"Content-Type": "application/json"}
    data = {"text": prompt}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# ... (Rest of the Streamlit code from previous example) ...

# React to user input
if prompt := st.chat_input("What is up?"):
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send the request to the OpenAI API through your FastAPI backend
    openai_response = send_to_openai_api(prompt)

    # Handle potential errors
    if isinstance(openai_response, str):  # Check if an error message was returned 
        st.error(openai_response)
    else:
        # Display the OpenAI response
        with st.chat_message("assistant"):
            st.markdown(openai_response)  # Assuming the response is already formatted
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": openai_response})
