import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from docx import Document
import os

DB_PATH = "End-to-End-AI-driven-pipeline-with-real-time-interview-insights-main/compliance-checker/src/Adarsh_Generated_Candidate_Data.xlsx"

def load_database():
    if os.path.exists(DB_PATH):
        return pd.read_excel(DB_PATH)
    else:
        st.error("Database file not found! Please ensure the file exists.")
        return pd.DataFrame()

def save_database(data):
    try:
        data.to_excel(DB_PATH, index=False)
        st.success("Database updated successfully!")
    except Exception as e:
        st.error(f"Error saving the database: {e}")

def upload_data():
    uploaded_file = st.file_uploader("Upload a file (CSV, PDF, or DOCX)", type=["csv", "pdf", "docx"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        try:
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
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    return None

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return ''.join([page.extract_text() for page in reader.pages])

def extract_word_text(uploaded_file):
    doc = Document(uploaded_file)
    return '\n'.join([para.text for para in doc.paragraphs])

def main():
    st.title("Contract Analysis System with Permanent Database")
    st.sidebar.header("Navigation")
    options = st.sidebar.radio("Select a page:", ["Home", "Data Upload", "Database", "About"])

    if options == "Home":
        st.header("Welcome to the Infosys Project Dashboard")
        st.write("This app is designed to showcase the key features and outputs of my project.")
        st.write("Use the sidebar to navigate through the app.")

    elif options == "Data Upload":
        st.header("Upload New Data")
        new_data = upload_data()
        if new_data is not None:
            st.session_state.new_data = new_data

    elif options == "Database":
        st.header("Permanent Database")
        database = load_database()
        st.write("Current Database:")
        st.dataframe(database)

        if st.button("Save Uploaded Data to Database"):
            if 'new_data' in st.session_state and isinstance(st.session_state.new_data, pd.DataFrame):
                updated_database = pd.concat([database, st.session_state.new_data], ignore_index=True)
                save_database(updated_database)
            else:
                st.warning("No new data available to save!")

    elif options == "About":
        st.header("About This App")
        st.write("The End-to-End AI-Driven Recruitment Pipeline streamlines hiring by automating key processes like resume screening, skill assessment, and interview analysis. Using NLP, it delivers real-time insights into candidate communication and expertise, while a cultural fit scoring system evaluates alignment with organizational values. This scalable, AI-powered solution ensures faster, data-driven hiring decisions with improved precision.")
        st.write("Author: Adarsh Ojaswi Singh")

if __name__ == "__main__":
    main()
