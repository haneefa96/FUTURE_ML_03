
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "cleaned_resumes.csv"
)

OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "resumes_with_skills.csv"
)

# Each key is the standard name we want to display.
# Each value contains alternative ways the skill may appear.
SKILL_DICTIONARY = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "C++": ["c++"],
    "C#": ["c#"],
    "SQL": ["sql"],
    "HTML": ["html"],
    "CSS": ["css"],
    "React": ["react", "react.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Linux": ["linux"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Natural Language Processing": [
        "natural language processing",
        "nlp",
    ],
    "Artificial Intelligence": [
        "artificial intelligence",
        "ai",
    ],
    "Data Analysis": ["data analysis"],
    "Data Visualization": ["data visualization"],
    "Statistics": ["statistics", "statistical analysis"],
    "NumPy": ["numpy"],
    "Pandas": ["pandas"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Excel": ["excel", "microsoft excel"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Communication": ["communication skills"],
    "Leadership": ["leadership"],
    "Project Management": ["project management"],
    "Recruitment": ["recruitment", "recruiting"],
    "Payroll": ["payroll"],
    "Employee Relations": ["employee relations"],
}


def extract_skills(text):
    """Return known skills found in a piece of resume text."""

    if pd.isna(text):
        return []

    text = str(text).lower()
    found_skills = []

    for skill, aliases in SKILL_DICTIONARY.items():
        for alias in aliases:
            # Match whole terms, ignoring letter case.
            # This avoids matching 'java' inside 'javascript'.
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


def main():
    print("RESUME SKILL EXTRACTION")
    print("=" * 40)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    if "cleaned_resume" not in df.columns:
        raise ValueError(
            "The dataset must contain 'cleaned_resume'. "
            "Run prepare_data.py first."
        )

    # Extract skills from every resume.
    df["extracted_skills"] = df["cleaned_resume"].apply(
        extract_skills
    )

    # Count how many resumes mention each skill.
    skill_counts = {}

    for skills in df["extracted_skills"]:
        for skill in skills:
            skill_counts[skill] = (
                skill_counts.get(skill, 0) + 1
            )

    print(f"Total resumes: {len(df)}")
    print(
        "Resumes with at least one recognized skill:",
        (df["extracted_skills"].str.len() > 0).sum()
    )

    print("\nMost frequently detected skills:")
    for skill, count in sorted(
        skill_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:15]:
        print(f"{skill}: {count} resumes")

    print("\nFirst 5 extracted skill lists:")
    print(
        df[["Category", "extracted_skills"]]
        .head()
        .to_string(index=False)
    )

    # Store the lists as readable text in the CSV.
    df["extracted_skills"] = df["extracted_skills"].apply(
        lambda skills: "; ".join(skills)
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved results to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
