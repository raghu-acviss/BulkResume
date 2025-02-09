import streamlit as st
import PyPDF2
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("TECH RAGHU MULTIPLE RESUME ANALYZER")

st.subheader("Resume Screener App")

uploadedJD = st.file_uploader("Upload Job Description", type="pdf")

uploadedCVs = st.file_uploader("Upload Resumes (Multiple)", type="pdf", accept_multiple_files=True)

ep = st.text_input("Enter the eligibility percentage ", type="default")

click = st.button("Process")

def extract_text_from_pdf(pdf_file):
    """Extracts text from all pages of a PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except:
        st.write(f"Failed to process {pdf_file.name}")
    return text.strip()

job_description = ""
if uploadedJD:
    job_description = extract_text_from_pdf(uploadedJD)

eligibility_percentage = None
try:
    eligibility_percentage = float(ep)
except:
    st.write("Please enter a valid eligibility percentage.")

def getResult(JD_txt, resume_txt):
    content = [JD_txt, resume_txt]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match = similarity_matrix[0][1] * 100
    return match

if click:
    if eligibility_percentage is not None:
        if uploadedCVs:
            for uploadedCV in uploadedCVs:
                resume_text = extract_text_from_pdf(uploadedCV)
                if resume_text:
                    match = getResult(job_description, resume_text)
                    match = round(match, 2)
                    st.write(f"Match Percentage for CV: {uploadedCV.name}: {match}%")
                    if match >= eligibility_percentage:
                        st.success(f"{uploadedCV.name} is eligible for the position!")
                    else:
                        st.write(f"Sorry, {uploadedCV.name} is not eligible.")
                else:
                    st.write(f"No text extracted from {uploadedCV.name}, skipping analysis.")
        else:
            st.write("Please upload at least one resume.")
    else:
        st.write("Please enter a valid eligibility percentage.")

st.caption("~ Made by Raghu")
