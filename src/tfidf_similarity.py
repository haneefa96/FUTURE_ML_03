
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Locate the project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define input and output files.
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "resumes_with_skills.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "tfidf_similarity_scores.csv"

# Job description for our first experiment.
JOB_DESCRIPTION = """
We are looking for a Python Developer.
Required skills include Python, SQL, Git, Django and data analysis.
The candidate should be able to develop applications,
work with databases, manage source code and analyze data.
"""


def main():
    # Load the resumes and their previously extracted skills.
    df = pd.read_csv(INPUT_FILE)

    # Ensure resume text is usable even if some entries are blank.
    resume_texts = df["cleaned_resume"].fillna("").astype(str)

    # Fit TF-IDF using both the resumes and the job description.
    documents = resume_texts.tolist() + [JOB_DESCRIPTION]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=10000
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    # The last row represents the job description.
    resume_vectors = tfidf_matrix[:-1]
    job_vector = tfidf_matrix[-1]

    # Compare every resume with the job description.
    scores = cosine_similarity(resume_vectors, job_vector).flatten()

    # Store similarity scores on a 0-100 scale for readability.
    results = df[["ID", "Category"]].copy()
    results["similarity_score"] = scores
    results["similarity_score_percent"] = scores * 100

    # Rank resumes from highest similarity to lowest.
    results = results.sort_values(
        by=["similarity_score", "ID"],
        ascending=[False, True]
    ).reset_index(drop=True)

    results.insert(0, "rank", range(1, len(results) + 1))

    # Save the results.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    # Display a small sample of the results.
    print("TF-IDF AND COSINE SIMILARITY")
    print("=" * 45)
    print(f"Resumes processed: {len(results)}")
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    print("\nTop 10 resumes by text similarity:")
    print(
        results[
            ["rank", "ID", "Category", "similarity_score_percent"]
        ].head(10).to_string(index=False)
    )
    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
