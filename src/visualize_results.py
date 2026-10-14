
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Find the project root and input/output paths.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "outputs" / "combined_rankings.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    # Load the existing combined ranking.
    df = pd.read_csv(INPUT_FILE)

    # Check that the required columns are available.
    required_columns = [
        "combined_rank",
        "ID",
        "Category",
        "skill_match_percent",
        "similarity_score_percent",
        "combined_score",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Chart 1: Distribution of combined scores.
    plt.figure(figsize=(9, 5))
    plt.hist(
        df["combined_score"],
        bins=20,
        edgecolor="black",
    )
    plt.title("Distribution of Combined Resume Scores")
    plt.xlabel("Combined Score (%)")
    plt.ylabel("Number of Resumes")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "score_distribution.png",
        dpi=150,
    )
    plt.close()

    # Chart 2: Compare component scores for the top 10 resumes.
    top10 = df.head(10).sort_values(
        "combined_rank",
        ascending=False,
    )

    labels = [
        f"Rank {rank} (ID {resume_id})"
        for rank, resume_id in zip(
            top10["combined_rank"],
            top10["ID"],
        )
    ]

    positions = range(len(top10))
    width = 0.38

    plt.figure(figsize=(12, 6))
    plt.bar(
        [p - width / 2 for p in positions],
        top10["skill_match_percent"],
        width,
        label="Skill Match",
    )
    plt.bar(
        [p + width / 2 for p in positions],
        top10["similarity_score_percent"],
        width,
        label="TF-IDF Similarity",
    )
    plt.xticks(list(positions), labels, rotation=45, ha="right")
    plt.title("Skill Match vs TF-IDF Similarity: Top 10 Resumes")
    plt.xlabel("Ranked Resume")
    plt.ylabel("Score (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_10_resumes.png",
        dpi=150,
    )
    plt.close()

    # Chart 3: Most common categories among the top 10 resumes.
    category_counts = (
        df.head(10)["Category"]
        .fillna("Unknown")
        .value_counts()
        .sort_values()
    )

    plt.figure(figsize=(9, 5))
    category_counts.plot(kind="barh")
    plt.title("Categories Among the Top 10 Ranked Resumes")
    plt.xlabel("Number of Resumes")
    plt.ylabel("Resume Category")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_categories.png",
        dpi=150,
    )
    plt.close()

    print("Visualization generation completed.")
    print("Created charts:")
    print(f"- {OUTPUT_DIR / 'score_distribution.png'}")
    print(f"- {OUTPUT_DIR / 'top_10_resumes.png'}")
    print(f"- {OUTPUT_DIR / 'top_categories.png'}")


if __name__ == "__main__":
    main()
