import streamlit as st
from storage import MessageStorage

if 'messages' in st.session_state:
    messages = st.session_state['messages']  # type: MessageStorage
    counted = messages.get_messages_count()
    st.table(counted)
