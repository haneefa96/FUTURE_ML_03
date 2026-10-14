
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "raw" / "Resume.csv"


def main():
    print("RESUME DATASET INSPECTION")
    print("=" * 40)

    if not DATA_PATH.exists():
        print(f"Dataset not found: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    print(f"\nNumber of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    if "Category" in df.columns:
        print("\nResume categories:")
        print(df["Category"].value_counts().to_string())

    if "Resume_str" in df.columns:
        valid_text = df["Resume_str"].dropna()

        if not valid_text.empty:
            print("\nFirst resume text sample:")
            print(valid_text.iloc[0][:500])


if __name__ == "__main__":
    main()
