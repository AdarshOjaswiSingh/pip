import streamlit as st
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from docx import Document

def process_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        st.write("CSV file loaded successfully!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

def process_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        st.write("PDF file loaded successfully!")
        st.text_area("PDF Content", text, height=300)
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")

def process_word(uploaded_file):
    try:
        doc = Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        st.write("Word document loaded successfully!")
        st.text_area("Word Content", text, height=300)
    except Exception as e:
        st.error(f"Error reading Word file: {e}")

def main():
    st.title("File Upload and Data Processing App")

    options = st.sidebar.selectbox("Choose an option", ["Home", "Data Upload"])

    if options == "Home":
        st.header("Welcome to the File Upload and Data Processing App")

    elif options == "Data Upload":
        st.header("Upload Your Dataset")
        uploaded_file = st.file_uploader("Upload a file", type=["csv", "pdf", "docx", "doc"])

        if uploaded_file is not None:
            file_type = uploaded_file.type
            if file_type == "application/pdf":
                process_pdf(uploaded_file)
            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
                process_word(uploaded_file)
            elif file_type == "text/csv":
                process_csv(uploaded_file)
            else:
                st.write("Unsupported file type!")

if __name__ == "__main__":
    main()
