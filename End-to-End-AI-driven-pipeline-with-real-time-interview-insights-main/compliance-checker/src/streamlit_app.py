import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from docx import Document

def upload_data():
    uploaded_file = st.file_uploader("Upload a file (CSV, PDF, or DOCX)", type=["csv", "pdf", "docx"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "text/csv":
            data = pd.read_csv(uploaded_file)
            st.write("Preview of the uploaded data:")
            st.dataframe(data)
            return data
        elif file_type == "application/pdf":
            text = extract_pdf_text(uploaded_file)
            st.write("PDF Content:")
            st.text_area("PDF Content", text, height=300)
            return text
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_word_text(uploaded_file)
            st.write("Word Document Content:")
            st.text_area("Word Content", text, height=300)
            return text
        else:
            st.error("Unsupported file type!")
    return None

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_word_text(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def create_visualization(data):
    if isinstance(data, pd.DataFrame):
        column = st.selectbox("Select a column to visualize:", data.columns)
        st.write(f"Histogram for {column}:")
        fig, ax = plt.subplots()
        data[column].hist(ax=ax, bins=10)
        st.pyplot(fig)
    else:
        st.warning("Visualizations are only available for CSV data.")

def main():
    st.title("Contract Analysis System")
    st.sidebar.header("Navigation")
    options = st.sidebar.radio("Select a page:", ["Home", "Data Upload", "Visualizations", "About"])

    if options == "Home":
        st.header("Welcome to the Infosys Project Dashboard")
        st.write("This app is designed to showcase the key features and outputs of my project.")
        st.write("Use the sidebar to navigate through the app.")

    elif options == "Data Upload":
        st.header("Upload Your Dataset")
        data = upload_data()
        if data is not None:
            st.session_state.data = data

    elif options == "Visualizations":
        st.header("Data Visualizations")
        if 'data' in st.session_state and isinstance(st.session_state.data, pd.DataFrame):
            create_visualization(st.session_state.data)
        else:
            st.write("Upload a dataset first to visualize data.")

    elif options == "About":
        st.header("About This App")
        st.write("The End-to-End AI-Driven Recruitment Pipeline streamlines hiring by automating key processes like resume screening, skill assessment, and interview analysis. Using NLP, it delivers real-time insights into candidate communication and expertise, while a cultural fit scoring system evaluates alignment with organizational values. This scalable, AI-powered solution ensures faster, data-driven hiring decisions with improved precision.")
        st.write("Author: Adarsh Ojaswi Singh")

if __name__ == "__main__":
    main()
