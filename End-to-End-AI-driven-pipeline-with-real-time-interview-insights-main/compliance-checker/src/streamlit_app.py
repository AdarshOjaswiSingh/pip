import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the app
st.title("Infosys Project Dashboard")

# Sidebar for user navigation
st.sidebar.header("Navigation")
options = st.sidebar.radio("Select a page:", ["Home", "Data Upload", "Visualizations", "About"])

if options == "Home":
    st.header("Welcome to the Infosys Project Dashboard")
    st.write("This app is designed to showcase the key features and outputs of your project.")
    st.write("Use the sidebar to navigate through the app.")

elif options == "Data Upload":
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded data:")
        st.dataframe(data)

elif options == "Visualizations":
    st.header("Data Visualizations")
    st.write("Upload a dataset first to visualize data.")

    if 'data' in locals() or 'data' in globals():
        column = st.selectbox("Select a column to visualize:", data.columns)

        # Plot histogram
        st.write(f"Histogram for {column}:")
        fig, ax = plt.subplots()
        data[column].hist(ax=ax, bins=10)
        st.pyplot(fig)
    else:
        st.warning("No data uploaded. Please upload a dataset in the 'Data Upload' section.")

elif options == "About":
    st.header("About This App")
    st.write("This app was created to demonstrate the capabilities of Streamlit for interactive dashboards.")
    st.write("Author: Adarsh Ojaswi Singh")
