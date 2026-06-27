import streamlit as st
from app.parser import extract_text_from_file
from app.extractor import parse_resume, parse_job_description
from app.scorer import compute_match
from app.models import ParsedResume, JobDescription

st.set_page_config(page_title="AI Resume Matcher", page_icon="🤖", layout="wide")

st.title("Automated AI Resume Matcher & Gap Analyzer")
st.caption("Upload a candidate profile against job benchmarks to compute real-time structural and semantic alignment scores.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Candidate Document")
    uploaded_file = st.file_uploader("Upload CV (PDF, DOCX)", type=["pdf", "docx"])

with col2:
    st.subheader("Job Description Target")
    job_title = st.text_input("Target Job Title", value="Machine Learning Engineer")
    job_text = st.text_area("Paste Job Requirements Here", height=200)

if st.button("Execute Pipeline Analysis") and uploaded_file and job_text:
    with st.spinner("Processing documents, executing NER extraction, and computing semantic embeddings..."):
        try:
            # 1. Extract raw text
            file_bytes = uploaded_file.read()
            raw_text = extract_text_from_file(file_bytes, uploaded_file.name)
            
            # 2. Extract entities via spaCy & regex
            resume_dict = parse_resume(raw_text)
            jd_dict = parse_job_description(job_text, job_title)
            
            # 3. Instantiate validation schemas
            resume_obj = ParsedResume(**resume_dict)
            jd_obj = JobDescription(**jd_dict)
            
            # 4. Process deep calculations
            result = compute_match(resume_obj, jd_obj)
            
            st.success("Analysis Complete!")
            
            # --- Render metrics UI ---
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall Match", f"{result.overall_score}%")
            m2.metric("Skill Alignment", f"{result.skill_match_score}%")
            m3.metric("Experience Score", f"{result.experience_score}%")
            m4.metric("Semantic Context", f"{result.semantic_score}%")
            
            # Detailed reporting splits
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.subheader("Identified Core Competencies")
                st.write(", ".join(result.matched_skills) if result.matched_skills else "None matched.")
                
            with r_col2:
                st.subheader("Critical Skill Deficiencies")
                st.write(", ".join(result.missing_skills) if result.missing_skills else "None detected.")
                
            st.subheader("Strategic Optimization Recommendations")
            for rec in result.recommendations:
                st.info(rec)
                
        except Exception as e:
            st.error(f"Execution Error: {e}")