import spacy
import json

nlp = spacy.load("en_core_web_sm")


def load_skills_database(file_path="data/skills_database.json"):
    with open(file_path, "r") as f:
        return json.load(f)


def extract_skills(text, skills_dict):
    """
    Extracts skills from resume text by matching known skills.
    """
    text = text.lower()
    found_skills = set()
    
    # Tokenize with spaCy
    doc = nlp(text)
    
    # Flat skill list
    all_skills = {skill for role in skills_dict for skill in skills_dict[role]}
    
    for token in doc:
        if token.text in all_skills:
            found_skills.add(token.text)
    
    return list(found_skills)


# Testing
if __name__ == "__main__":
    resume_text = """
    I have experience in Python, SQL, and Power BI. Recently started learning Tableau and Pandas.
    """
    skills_db = load_skills_database()
    matched = extract_skills(resume_text, skills_db)
    print("Skills found:", matched)

def match_roles(found_skills, skills_dict):
    """
    Match found skills to roles based on overlap %.
    Returns top matches sorted by percentage.
    """
    role_matches = []

    for role, required_skills in skills_dict.items():
        match_count = len(set(required_skills) & set(found_skills))
        match_percent = (match_count / len(required_skills)) * 100
        role_matches.append((role, round(match_percent, 2)))

    # Sort by highest match %
    role_matches.sort(key=lambda x: x[1], reverse=True)
    return role_matches


# Extended Test
if __name__ == "__main__":
    resume_text = """
    I have experience in Python, SQL, Power BI, Tableau and Pandas.
    Recently worked with Excel and Git.
    """
    skills_db = load_skills_database()
    found_skills = extract_skills(resume_text, skills_db)
    matches = match_roles(found_skills, skills_db)

    print("Skills found:", found_skills)
    print("\nRole Matches:")
    for role, percent in matches:
        print(f"{role}: {percent}% match")

def get_missing_skills(found_skills, skills_dict):
    """
    Returns a dictionary of roles with their missing skills.
    """
    role_missing = {}

    for role, required_skills in skills_dict.items():
        missing = list(set(required_skills) - set(found_skills))
        if len(missing) < len(required_skills):  # if at least one skill matched
            role_missing[role] = missing

    return role_missing

def load_course_recommendations(file_path="data/course_recommendations.json"):
    with open(file_path, "r") as f:
        return json.load(f)