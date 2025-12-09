# Consumer Behavior Analysis Demo: Dupe Products

This repository demonstrates the statistical analysis pipeline for my research on consumer motivations regarding "dupe" products.

> **Note:** This is a public demo repository. The source code for the upstream AI automation agent (utilizing Groq/Llama-3 for data labeling) is maintained in a private repository to protect ongoing longitudinal research.

## 📂 Repository Contents

* `analysis_demo.py`: Python script to perform statistical verification (Chi-square & Logistic Regression).
* `data/processed/`: Contains the AI-labeled dataset (N=100) used for this analysis.
* `reports/`: Visualization outputs.

## 📊 Key Findings (Study 1)

The analysis verifies **Hypothesis 1 (H1)**: *Hedonic motivation drives higher purchase intention for dupes.*

| Motivation Type | Purchase Rate | Sample Size |
| :--- | :--- | :--- |
| **Hedonic** | **91.84%** | 49 |
| **Utilitarian** | **50.00%** | 50 |

* **Statistical Significance:** $\chi^2 = 20.91$, $p < 0.001$ (Highly Significant).

## 🚀 How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt