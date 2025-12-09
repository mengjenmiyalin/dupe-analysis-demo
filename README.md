# Research Proposal Demo: Semantic Analysis of "Dupe" Product Consumption
> **Project Focus:** Purchase Intention & Motivational Drivers (Hedonic vs. Utilitarian)

This repository serves as a **technical demonstration** for my PhD research proposal. It showcases the statistical analysis pipeline used to quantify consumer behaviors regarding "dupe" (alternative) products.

> **⚠️ Note on Source Code:**
> This represents the **public demonstration layer** of the project.
> The upstream **AI Automation Agent** (the core engine responsible for data fetching and LLM-based labeling) is maintained in a **private repository** to protect the intellectual property of an ongoing longitudinal study.
> *Access to the full codebase can be provided to the admissions committee upon request.*

## 📂 Repository Contents

* `analysis_demo.py`: The main Python script that performs statistical verification (Chi-square & Logistic Regression) on the processed data.
* `data/processed/`: Contains the structured dataset used for this analysis.
    * *Note: The current dataset consists of **100 simulated records** generated to mimic authentic social media linguistic patterns for demonstration purposes.*
* `reports/`: Visualization outputs and statistical summaries.
* `requirements.txt`: List of dependencies for reproducing the environment.

## 🚀 Methodological Evolution (RP vs. Implementation)

While the original Research Proposal (RP) suggested using **Structural Topic Modeling (STM)**, this implementation upgrades the methodology to a **Generative AI approach** for higher semantic precision.

### Why this upgrade?
1.  **Precision:** Unlike keyword-based STM, LLMs can understand context (e.g., distinguishing "I want to buy" from "I bought it").
2.  **Efficiency (Groq Integration):** The system utilizes **Groq API** serving **Llama-3.3-70b**. I chose Groq over proprietary models (like Gemini/GPT-4) to leverage the **open-weights nature of Llama-3** (better for academic reproducibility) and to overcome API rate limits for high-throughput batch processing.

## 🧠 The AI Labeling Mechanism

To ensure the data used in this demo is rigorous, the upstream private agent uses a sophisticated labeling process:

1.  **Zero-shot Classification:** The model classifies text without needing thousands of training examples, using advanced prompt engineering.
2.  **JSON Schema Enforcement:** Instead of letting the AI "chat," we force it to output strict computer-readable code (JSON).
3.  **Deterministic Output (Temp=0):** We set the model's "creativity" to zero. This ensures that if you run the same data twice, you get the exact same result—crucial for scientific replication.

## 📊 Key Findings (Hypothesis 1 Verification)

The pipeline successfully verifies **Hypothesis 1 (H1)**: *Hedonic motivation drives higher purchase intention for dupes than utilitarian motivation.*

| Motivation Type | Purchase Rate | Sample Size |
| :--- | :--- | :--- |
| **Hedonic** | **91.84%** | 49 |
| **Utilitarian** | **50.00%** | 50 |

* **Statistical Significance:** $\chi^2 = 20.91$, $p < 0.001$ (Highly Significant).
* **Logistic Regression:** The coefficient for Hedonic motivation is **2.42**, indicating a strong positive predictor for purchase intent.

## 🛠️ How to Run

1. **Install dependencies:**
   Run the following command in your terminal to install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install dependencies:**
    Run the following command in your terminal:
    ```bash
    python analysis_demo.py
    ```

3. **View Results:**
    The script will output the sample size, purchase rates, and Chi-square statistics directly in the terminal console.

## 📦 Requirements

* numpy==2.3.5
* packaging==25.0
* pandas==2.3.3
* patsy==1.0.2
* python-dateutil==2.9.0.post0
* pytz==2025.2
* scipy==1.16.3
* six==1.17.0
* statsmodels==0.14.6
* tzdata==2025.2

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
**Contact:**
If you wish to review the full source code of the automation agent, please contact:
**Meng-Jen (Miya) Lin**
*National Taiwan Normal University*
*Email: mengjen.miya.lin@gmail.com*