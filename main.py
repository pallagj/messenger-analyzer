import os
import zipfile
import tempfile
import streamlit as st

from storage import MessageStorage

st.set_page_config(
    page_title="Hello",
    page_icon="👋",

)

st.markdown(
    """
Welcome to Facebook Messenger Analyzer! ;)    

"""
)

uploaded_file = st.file_uploader("Válaszd ki az inbox mappát", type="zip")

if 'messages' not in st.session_state:
    st.session_state['messages'] = MessageStorage()

if uploaded_file is not None:
    with st.spinner("Kicsomagolás..."):
        temp_dir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            zip_ref.extractall(temp_dir.name)

    with st.spinner("Feldolgozás..."):
        messages = MessageStorage()
        messages.read_messages(temp_dir.name)
        st.session_state['messages'] = messages
        st.write("Succesful...")

    temp_dir.cleanup()
