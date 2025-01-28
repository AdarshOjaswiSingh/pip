import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import re

def extract_pdf_text(file):
    try:
        reader = PdfReader(file)
        return ''.join(page.extract_text() for page in reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_word_text(file):
    try:
        doc = Document(file)
        return '\n'.join(para.text for para in doc.paragraphs)
    except Exception as e:
        st.error(f"Error reading Word document: {e}")
        return ""

@st.cache
def load_database():
    try:
        return pd.read_excel("End-to-End-AI-driven-pipeline-with-real-time-interview-insights-main/compliance-checker/src/Adarsh_Generated_Candidate_Data.xlsx")
    except Exception as e:
        st.error(f"Failed to load database: {e}")
        return pd.DataFrame()

def extract_skills(resume_text):
    skills = set(["Python", "Java", "C++", "Machine Learning", "AI", "Data Science", "SQL", "Project Management"])
    return [skill for skill in skills if skill.lower() in resume_text.lower()]

def generate_interview_questions(skills):
    database = load_database()
    questions = []
    for skill in skills:
        matched_questions = database[database['Skill'].str.contains(skill, case=False)]['Interview Questions'].tolist()
        questions.extend(matched_questions)
    return questions

def process_resume():
    uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        resume_text = extract_pdf_text(uploaded_file) if uploaded_file.type == "application/pdf" else extract_word_text(uploaded_file)
        st.text_area("Resume Text", resume_text, height=300)
        skills = extract_skills(resume_text)
        st.write(f"Extracted Skills: {', '.join(skills)}")
        
        questions = generate_interview_questions(skills)
        if questions:
            st.write("Suggested Interview Questions:")
            for question in questions:
                st.write(f"- {question}")
        else:
            st.warning("No relevant questions found for the extracted skills.")

def evaluate_candidate(answers):
    required_keywords = {"expert", "strong", "advanced"}
    score = sum(any(keyword in ans.lower() for keyword in required_keywords) for ans in answers)
    
    return "Selected" if score >= 3 else "Rejected"

def main():
    st.title("Resume Analysis and Interview Question Generation")
    st.sidebar.header("Navigation")
    options = st.sidebar.radio("Select a page:", ["Home", "Resume Analysis"])

    if options == "Home":
        st.header("Welcome to the Resume Analysis App")
        st.write("This app helps in analyzing resumes and generating interview questions based on skills.")

    elif options == "Resume Analysis":
        st.header("Upload and Analyze Resume")
        process_resume()
        st.write("After generating interview questions, you can evaluate the answers manually or automatically.")
        dummy_answers = ["I am an expert in Python.", "I have strong experience in Machine Learning.", "I have advanced SQL skills."]
        result = evaluate_candidate(dummy_answers)
        st.write(f"Candidate Evaluation: {result}")

if __name__ == "__main__":
    main()
