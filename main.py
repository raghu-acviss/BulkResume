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

try:
    global job_description
    with pdfplumber.open(uploadedJD) as pdf:
        pages = pdf.pages[0]
        job_description = pages.extract_text()

except:
    st.write("")

eligibility_percentage = None  # Initialize with a default value

try:
    eligibility_percentage = float(ep)
except:
    st.write("")


# logic
def getResult(JD_txt, resume_txt):
    content = [JD_txt, resume_txt]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match = similarity_matrix[0][1] * 100
    return match


# button
if click:
    if eligibility_percentage is not None:
        if uploadedCVs:
            for uploadedCV in uploadedCVs:
                try:
                    global resume
                    with pdfplumber.open(uploadedCV) as pdf:
                        pages = pdf.pages[0]
                        resume = pages.extract_text()
                except:
                    st.write(f"Failed to process one of the uploaded resumes.")
                    continue

                match = getResult(job_description, resume)
                match = round(match, 2)
                st.write(f"Match Percentage for CV: {uploadedCV.name}: {match}%")

                if match >= eligibility_percentage:
                    st.success(f"{uploadedCV.name} is eligible for the position!")
                else:
                    st.write(f"Sorry, {uploadedCV.name} is not eligible")
        else:
            st.write("Please upload at least one resume.")
    else:
        st.write("Please enter a valid eligibility percentage.")

st.caption("~ Made by Raghu")
