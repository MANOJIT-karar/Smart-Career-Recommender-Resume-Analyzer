import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, match_roles, load_skills_database,get_missing_skills
from skill_matcher import load_course_recommendations

st.set_page_config(page_title="Smart Career Recommender", layout="centered")

st.title("📄 Smart Career Recommender")
st.subheader("Analyze your resume & get matched to the best-fit tech roles!")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file:
    with open("resumes/temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract resume text
    resume_text = extract_text_from_pdf("resumes/temp_resume.pdf")

    # Load skills data and extract skills from resume
    skills_db = load_skills_database()
    found_skills = extract_skills(resume_text, skills_db)

    # Match roles
    role_matches = match_roles(found_skills, skills_db)
    missing_skills_dict = get_missing_skills(found_skills, skills_db)

    # Display results
    st.markdown("### ✅ Skills Detected:")
    st.write(", ".join(found_skills) if found_skills else "No known skills found.")

        # Role Match % Bar Chart
    if role_matches:
        role_names = [role for role, _ in role_matches]
        match_percents = [percent for _, percent in role_matches]

        df = pd.DataFrame({
            'Role': role_names,
            'Match %': match_percents
        })

        st.markdown("### 📊 Skill Match Overview")
        fig, ax = plt.subplots(figsize=(8, len(role_names) * 0.4))
        ax.barh(df['Role'], df['Match %'], color='skyblue')
        ax.invert_yaxis()
        ax.set_xlabel("Match %")
        ax.set_title("Resume vs Career Role Match")
        st.pyplot(fig)
        
    st.markdown("### 🎯 Role Match Recommendations:")
    if role_matches:
        for role, percent in role_matches:
            st.markdown(f"{role}** — {percent}% match")

            missing = missing_skills_dict.get(role, [])
            if missing:
                st.write(f"❌ Missing Skills for {role}: {', '.join(missing)}")
            st.markdown("---")
    else:
        st.write("No roles matched.")

    # Load course recommendations
    course_recs = load_course_recommendations()

    st.markdown("### 📚 Recommended Courses for Missing Skills:")
    for role, missing_skills in missing_skills_dict.items():
        if missing_skills:
            st.subheader(f"For {role}:")
            for skill in missing_skills:
                rec = course_recs.get(skill.lower())
                if rec:
                    st.markdown(f"- *{skill.title()}*: [{rec['course']}]({rec['url']}) on {rec['platform']}")
            st.markdown("---")

    
        