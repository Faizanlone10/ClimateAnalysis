import streamlit as st

def file_upload():
    st.title('File Upload')
    uploaded_file = st.file_uploader("Upload a file")

    if uploaded_file:
        return uploaded_file
    else:
        return None
