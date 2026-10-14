# FUTURE_ML_03 — Resume Screening and Ranking System

## Project Overview

The Resume Screening and Ranking System is a Python-based machine learning project that analyzes resumes against a job description.

It combines predefined skill extraction, TF-IDF text similarity, and weighted scoring to rank resumes by their potential relevance to a sample job role.

This project is an educational decision-support tool for human reviewers, not an automated hiring or rejection system.

## Objectives

- Clean and preprocess resume text.
- Extract technical and professional skills using a predefined skill dictionary.
- Compare resumes with a job description using TF-IDF and cosine similarity.
- Calculate skill-match scores.
- Combine skill-match and text-similarity scores into a final ranking.
- Generate reports and visualizations.

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Regular expressions (Regex)

## Dataset

This project uses a dataset containing 2,484 resumes, including resume text and category labels.

Dataset source: [Kaggle — Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)

The raw and processed resume datasets are excluded from this repository because they contain resume text and may include personal information.

To run the project:

1. Obtain the dataset from the source above and review its license and usage terms.
2. Create the `data/raw/` directory in the project root.
3. Place the downloaded CSV at `data/raw/Resume.csv`.
4. Run the scripts in the order listed under How to Run.

## Project Workflow

1. **Data preparation:** Clean resume text.
2. **Skill extraction:** Identify skills using a predefined dictionary and regular expressions.
3. **Skill matching:** Compare extracted skills with the required skills.
4. **TF-IDF similarity:** Calculate text similarity between resumes and the job description.
5. **Combined ranking:** Combine skill-match and similarity scores.
6. **Validation:** Check record counts, duplicate IDs, missing values, score ranges, and ranking order.
7. **Visualization:** Generate charts for result analysis.

## Ranking Method

The combined score uses two components:

- Skill-match score: 60%
- TF-IDF similarity score: 40%

**Formula:**

Combined Score = (0.60 × Skill-Match Score) + (0.40 × TF-IDF Similarity Score)

Both component scores use a 0–100 scale, so the combined score also falls within that range.

Resumes are sorted by combined score in descending order. Resume ID breaks ties consistently.

## Sample Job Description

The current ranking script uses a sample Python Developer profile with these required skills:

- Python
- SQL
- Git
- Django
- Data Analysis

The skill-match score measures how many required skills are recognized in a resume. TF-IDF measures textual similarity to the job description.

Results depend on the chosen job description, required skills, and score weights.

## Project Structure

```text
FUTURE_ML_03/
|-- data/
|   |-- raw/                 # Local input dataset; not committed
|   |-- processed/           # Generated data; not committed
|-- outputs/
|   |-- score_distribution.png
|   |-- top_10_resumes.png
|   |-- top_categories.png
|-- src/
|   |-- inspect_data.py
|   |-- prepare_data.py
|   |-- extract_skills.py
|   |-- rank_resumes.py
|   |-- tfidf_similarity.py
|   |-- combine_rankings.py
|   |-- visualize_results.py
|-- requirements.txt
|-- .gitignore
|-- README.md
```

The output CSV reports are generated locally and are excluded from Git.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/haneefa96/FUTURE_ML_03.git
cd FUTURE_ML_03
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Run

Run these commands from the project root, in order:

```bash
python src/inspect_data.py
python src/prepare_data.py
python src/extract_skills.py
python src/rank_resumes.py
python src/tfidf_similarity.py
python src/combine_rankings.py
python src/visualize_results.py
```

Make sure `data/raw/Resume.csv` exists before running the pipeline. Later scripts depend on the files produced by earlier scripts.

## Output Files

| File | Description |
|---|---|
| `skill_match_rankings.csv` | Skill-match scores and matched or missing required skills |
| `tfidf_similarity_scores.csv` | TF-IDF similarity scores |
| `combined_rankings.csv` | Combined scores, categories, and final ranks |
| `score_distribution.png` | Distribution of combined scores |
| `top_10_resumes.png` | Component scores for the top 10 ranked resumes |
| `top_categories.png` | Categories among the top 10 ranked resumes |

CSV reports are generated locally and are not committed to the repository.

## Validation

The generated combined ranking passed seven quality checks:

- Exactly 2,484 resume records
- No duplicate resume IDs
- Required columns present with no missing values
- All scores between 0 and 100
- Correct weighted-score formula
- Consecutive ranks
- Descending combined-score order

## Limitations

- Skill extraction depends on the predefined dictionary and may miss synonyms or unlisted skills.
- TF-IDF measures textual similarity but does not fully understand context, experience quality, or skill proficiency.
- Results depend on the job description, skill list, and score weights.
- A high score does not guarantee that a candidate is qualified.
- A low score does not prove that a candidate is unsuitable.
- The dataset and sample job description may not represent real recruitment requirements.

## Responsible Use

This project is intended for educational purposes and preliminary resume analysis. Human reviewers should assess relevant experience, qualifications, and other job-related evidence.

Do not use this ranking as the sole basis for hiring or rejecting candidates. Evaluate potential errors and bias before considering real-world use.

## Future Improvements

- Expand the skill dictionary and support synonyms.
- Allow custom job descriptions and required skills.
- Add a web interface for uploading resumes and viewing rankings.
- Compare alternative text representation and ranking methods.
- Add automated tests and comprehensive evaluation metrics.
- Improve privacy protection and assess potential bias.

## Author

**Haneefa Riham**

GitHub: [haneefa96](https://github.com/haneefa96)

## Project Status

The initial resume processing, skill extraction, TF-IDF similarity, weighted ranking, output validation, and visualization pipeline has been implemented. Further improvements and evaluation may be added in future versions.