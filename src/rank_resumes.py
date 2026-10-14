
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "resumes_with_skills.csv"
)

OUTPUT_PATH = (
    PROJECT_DIR / "outputs"
    / "skill_match_rankings.csv"
)

# Example job description.
# We will make this customizable later.
JOB_DESCRIPTION = """
We are looking for a Python Developer.
Required skills include Python, SQL, Git,
Django and data analysis.
"""

# Skills the recruiter requires for this role.
REQUIRED_SKILLS = [
    "Python",
    "SQL",
    "Git",
    "Django",
    "Data Analysis",
]


def parse_job_description(description):
    """Identify required skills mentioned in the job description."""

    description = description.lower()

    matched = [
        skill
        for skill in REQUIRED_SKILLS
        if skill.lower() in description
    ]

    return matched


def calculate_skill_match(candidate_skills, required_skills):
    """Calculate the percentage of required skills found."""

    if not required_skills:
        return 0.0, [], []

    candidate_set = {
        skill.strip().lower()
        for skill in str(candidate_skills).split(";")
        if skill.strip()
    }

    matched = [
        skill for skill in required_skills
        if skill.lower() in candidate_set
    ]

    missing = [
        skill for skill in required_skills
        if skill.lower() not in candidate_set
    ]

    score = len(matched) / len(required_skills) * 100

    return round(score, 2), matched, missing


def main():
    print("RESUME RANKING BY SKILL MATCH")
    print("=" * 45)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Skill dataset not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    if "extracted_skills" not in df.columns:
        raise ValueError(
            "The input dataset must contain extracted_skills."
        )

    required_skills = parse_job_description(
        JOB_DESCRIPTION
    )

    print("\nRequired skills:")
    print(", ".join(required_skills))

    results = []

    for _, row in df.iterrows():
        score, matched, missing = calculate_skill_match(
            row["extracted_skills"],
            required_skills,
        )

        results.append({
            "ID": row["ID"],
            "Category": row["Category"],
            "skill_match_percent": score,
            "matched_skills": "; ".join(matched),
            "missing_skills": "; ".join(missing),
        })

    rankings = pd.DataFrame(results)

    rankings = rankings.sort_values(
        by=["skill_match_percent", "ID"],
        ascending=[False, True],
    ).reset_index(drop=True)

    rankings.insert(
        0,
        "rank",
        range(1, len(rankings) + 1),
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rankings.to_csv(OUTPUT_PATH, index=False)

    print("\nTop 10 candidates by skill match:")
    print(rankings.head(10).to_string(index=False))

    print(f"\nTotal candidates ranked: {len(rankings)}")
    print(f"Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
