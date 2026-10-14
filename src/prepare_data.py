
from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = PROJECT_DIR / "data" / "raw" / "Resume.csv"
OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "cleaned_resumes.csv"


def clean_resume_text(text):
    """Remove HTML markup and normalize resume text."""

    if pd.isna(text):
        return ""

    # Convert the value to a string.
    text = str(text)

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs.
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Normalize whitespace and line breaks.
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary spaces at the beginning and end.
    text = text.strip()

    return text


def main():
    print("RESUME DATA CLEANING")
    print("=" * 40)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_PATH}"
        )

    # Load the original dataset.
    df = pd.read_csv(INPUT_PATH)

    # Clean the resume text.
    df["cleaned_resume"] = df["Resume_str"].apply(
        clean_resume_text
    )

    # Report the results.
    print(f"Original resume count: {len(df)}")
    print(
        "Empty cleaned resumes:",
        (df["cleaned_resume"].str.len() == 0).sum()
    )

    print("\nBefore cleaning:")
    print(df["Resume_str"].iloc[0][:300])

    print("\nAfter cleaning:")
    print(df["cleaned_resume"].iloc[0][:300])

    # Create the output directory if necessary.
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save all original columns plus the cleaned text.
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCleaned dataset saved to:\n{OUTPUT_PATH}")
    print(f"Total records saved: {len(df)}")


if __name__ == "__main__":
    main()
