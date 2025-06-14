import streamlit as st
import requests
import jwt



API_URL = "http://localhost:8000"

if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def login_ui():
    st.title("🔐 FinBot Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            try:
                res = requests.post(f"{API_URL}/login", data={"username": username, "password": password}, headers={"Content-Type": "application/x-www-form-urlencoded"})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.token = data["access_token"]
                    decoded = jwt.decode(data["access_token"], options={"verify_signature": False}, algorithms=["HS256"])
                    st.session_state.role = decoded["role"]
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {e}")

def chatbot_ui():
    st.title("💬 FinBot Chat")
    st.markdown(f"**Role:** `{st.session_state.role}`")
    query = st.text_input("Ask a question:")
    if st.button("Send") and query:
        try:
            res = requests.post(f"{API_URL}/chat", json={"query": query, "token": st.session_state.token})
            if res.status_code == 200:
                result = res.json()
                st.session_state.chat_history.append((query, result["answer"]))
            else:
                st.error("⚠️ Something went wrong.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    for q, a in st.session_state.chat_history[::-1]:
        with st.expander(f"💬 You: {q}"):
            st.markdown(f"**🤖 FinBot:** {a}")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.chat_history = []
        st.rerun()

if st.session_state.token:
    chatbot_ui()
else:
    login_ui()
