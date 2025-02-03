import streamlit as st
import requests


st.title('Prompting hospital system')

query = st.text_input('What\'s in your mind?')

if query:
    response = requests.post('http://localhost:5000/rag',json={'query': query})
    answer = response.json()['answer']
    st.write(answer)