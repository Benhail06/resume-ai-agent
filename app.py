import streamlit as st
from utils import calculate_match_score, extract_text_from_pdf, generate_interview_questions, generate_recommendations

st.set_page_config(page_title="AI Resume Matcher")

st.set_page_config(
    page_title="Resume AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Resume AI Agent")
st.markdown("AI-powered resume evaluation and job match analysis.")
st.divider()


st.title("🧠 AI Resume–Job Matcher")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Job Description", height=200)





import streamlit as st
from utils import (
    extract_text_from_pdf,
    extract_skills_from_text,
    extract_requirements_from_jd,
    calculate_match_score,
    find_missing_skills
)

# import streamlit as st
# from utils import (
#     extract_text_from_pdf,
#     extract_skills_from_text,
#     extract_requirements_from_jd
# )


if st.button("Analyze"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing Resume..."):


            resume_text = extract_text_from_pdf(uploaded_file)

            st.subheader("Resume Analysis")
            resume_data = extract_skills_from_text(resume_text)
            st.json(resume_data)

            st.subheader("Job Description Analysis")
            jd_data = extract_requirements_from_jd(job_description)
            st.json(jd_data)


            
            st.subheader("Match Analysis")

            score_color = "green" if match_score >= 70 else "orange" if match_score >= 40 else "red"

            st.metric("Match Score (%)", f"{match_score}%")
            st.progress(int(match_score))

            match_score = calculate_match_score(
            resume_data["technical_skills"],
            jd_data["required_skills"]
    )

            missing_skills = find_missing_skills(
            resume_data["technical_skills"],
            jd_data["required_skills"]
    )
            recommendations = generate_recommendations(
            resume_data,
            jd_data,
            missing_skills

    )
            
            st.success("Analysis Complete ✅")

            st.metric("Match Score (%)", match_score)
            st.progress(int(match_score))


            st.subheader("Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.markdown(f"- 🔴 {skill}")
                else:
                    st.success("No major skill gaps detected.")


            st.subheader("AI Career Advice")
            st.write(recommendations)


            with st.expander("📊 Extracted Resume Data"):
                st.json(resume_data)

            with st.expander("📋 Extracted Job Requirements"):
                st.json(jd_data)




            questions = generate_interview_questions(jd_data)

            st.subheader("Likely Interview Questions")
            for q in questions["questions"]:
                st.write("•", q)




    else:
        st.warning("Please upload resume and paste job description.")

st.info("💡 Tip: Improve missing skills and re-run analysis to increase your match score.")






st.divider()
st.caption("Built with Streamlit + Groq LLM | Designed by Ben")

