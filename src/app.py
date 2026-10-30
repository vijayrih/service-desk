import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import uuid
from src.agent import execute_agent

st.set_page_config(page_title="AI Service Desk", page_icon="🤖")

@st.dialog("Sign In")
def login_modal():
    st.markdown("Please sign in to access the IT Support Desk.")
    email = st.text_input("Email", placeholder="vip@example.com")

    st.caption("Test Accounts: vip@example.com and standard@example.com")
    
    if st.button("Sign In", type="primary", use_container_width=True):
        if email:
            st.session_state.user_email = email.strip()
            st.rerun()
        else:
            st.error("Please enter a valid email address.")

if "user_email" not in st.session_state:
    login_modal()
    st.stop()

st.sidebar.title("Service Desk")
st.sidebar.info(f"👤 **{st.session_state.user_email}**")

if st.sidebar.button("Sign Out", use_container_width=True):
    del st.session_state.user_email
    st.session_state.messages = [] 
    st.rerun()

user_email = st.session_state.user_email

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Autonomous Service Desk")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Describe your issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing request and executing tools..."):
            try:
                response = execute_agent(
                    user_input=prompt,
                    user_email=user_email,
                    session_id=st.session_state.session_id
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"System Error: {str(e)}")