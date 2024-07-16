# sgpa_calculator.py

import streamlit as st
import tabula
import pandas as pd

# Function to process PDF and calculate SGPA
def calculate_sgpa(pdf_path):
    # Extract tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    # Save the first table to a DataFrame
    df = tables[0]
    
    # Drop rows with any NaN values
    df.dropna(inplace=True)
    
    # Rename columns
    df.columns = ["Semester", "Course Name", "Grade point", "Grade", "Credit", "Result status"]
    
    # Trim the Course Name column
    df['Course Name'] = df['Course Name'].str[:10]
    
    # Filter out excluded subjects
    excluded_sub = ["U18AIP3607", "U18TLR2001", "U18CHR0002", "U18AIP2607", "U18AIP2708", "U18TLR1001", "U18MAR0003"]
    df_filtered = df[~df["Course Name"].isin(excluded_sub)]
    
    # Calculate 'Grade point * Credit'
    df_filtered['Grade point * Credit'] = df_filtered['Grade point'].astype(int) * df_filtered['Credit'].astype(int)
    
    # Calculate sum of credits
    sum_of_credits = df_filtered['Credit'].astype(int).sum()
    
    # Calculate multiplied sum
    multiplied_sum = df_filtered['Grade point * Credit'].sum()
    
    # Calculate SGPA
    sgpa = multiplied_sum / sum_of_credits
    
    return sgpa, sum_of_credits, multiplied_sum

# Streamlit app
st.title("SGPA CALCULATOR")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Calculate SGPA
    sgpa, sum_of_credits, multiplied_sum = calculate_sgpa("uploaded_file.pdf")
    
    # Display results
    st.write(f"Multiplied Sum (Grade Point * Credit) = {multiplied_sum}")
    st.write(f"Sum of Credits = {sum_of_credits}")
    st.write(f"Calculated SGPA = {sgpa}")
