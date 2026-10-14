
from pathlib import Path

import pandas as pd


# Find the project root directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output file paths.
SKILL_FILE = PROJECT_ROOT / "outputs" / "skill_match_rankings.csv"
SIMILARITY_FILE = PROJECT_ROOT / "outputs" / "tfidf_similarity_scores.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs" / "combined_rankings.csv"

# Weights used to calculate the combined score.
SKILL_WEIGHT = 0.60
SIMILARITY_WEIGHT = 0.40


def main():
    # Load the skill-based rankings and TF-IDF similarity scores.
    skill_df = pd.read_csv(SKILL_FILE)
    similarity_df = pd.read_csv(SIMILARITY_FILE)

    print("Loaded both input files.")
    print(f"Skill rankings: {len(skill_df)} resumes")
    print(f"TF-IDF scores: {len(similarity_df)} resumes")

    # Keep the required columns from the skill rankings.
    skill_df = skill_df[
        [
            "ID",
            'Category',
            "skill_match_percent",
            "matched_skills",
            "missing_skills",
        ]
    ]

    # Keep the required columns from the similarity results.
    similarity_df = similarity_df[
        [
            "ID",
            "similarity_score_percent",
        ]
    ]

    # Check for duplicate resume IDs before merging.
    if skill_df["ID"].duplicated().any():
        raise ValueError(
            "Duplicate resume IDs found in skill rankings."
        )

    if similarity_df["ID"].duplicated().any():
        raise ValueError(
            "Duplicate resume IDs found in TF-IDF scores."
        )

    # Merge the results using resume ID.
    # Do not assume that the rows in both files are in the same order.
    results = skill_df.merge(
        similarity_df,
        on="ID",
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    # Verify that every resume exists in both files.
    if not (results["_merge"] == "both").all():
        unmatched = results.loc[
            results["_merge"] != "both", ["ID", "_merge"]
        ]
        raise ValueError(
            "Some resume IDs are missing from one of the files:\n"
            + unmatched.head(10).to_string(index=False)
        )

    # Remove the temporary merge indicator.
    results = results.drop(columns=["_merge"])

    # Calculate the weighted combined score.
    results["combined_score"] = (
        SKILL_WEIGHT * results["skill_match_percent"]
        + SIMILARITY_WEIGHT * results["similarity_score_percent"]
    )

    # Sort from highest combined score to lowest.
    # Use resume ID to break ties consistently.
    results = results.sort_values(
        by=["combined_score", "ID"],
        ascending=[False, True],
    ).reset_index(drop=True)

    # Assign a rank to every resume.
    results.insert(
        0,
        "combined_rank",
        range(1, len(results) + 1),
    )

    # Save the combined rankings without overwriting earlier results.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    # Display a summary and the top 10 results.
    print("\nCOMBINED RESUME RANKING")
    print("=" * 50)
    print(f"Total resumes ranked: {len(results)}")
    print(f"Skill-match weight: {SKILL_WEIGHT:.0%}")
    print(f"TF-IDF similarity weight: {SIMILARITY_WEIGHT:.0%}")

    print("\nTop 10 resumes:")
    print(
        results[
            [
                "combined_rank",
                "ID",
                "skill_match_percent",
                "similarity_score_percent",
                "combined_score",
            ]
        ].head(10).to_string(index=False)
    )

    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
