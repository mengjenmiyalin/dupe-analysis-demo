# analysis_demo.py (公開版專用：展示統計分析能力)
import pandas as pd
import statsmodels.api as sm
import numpy as np
from pathlib import Path
from collections import defaultdict

# 設定讀取路徑 (請確認 data/processed/ai_labeled_results.csv 存在)
DATA_PATH = Path("data/processed/ai_labeled_results.csv")

def show_stats():
    print(f"📂 Reading data from: {DATA_PATH}...")
    
    if not DATA_PATH.exists():
        print("❌ Error: Data file not found. Please ensure 'data/processed/ai_labeled_results.csv' exists.")
        return

    # 1. 讀取數據
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Loaded dataset: {len(df)} records.\n")

    # 2. 資料前處理 (Data Preparation)
    counts = defaultdict(lambda: {"yes": 0, "no": 0})
    
    # 用來跑回歸的 List
    y_list, x_list = [], []

    for _, row in df.iterrows():
        # 確保轉小寫並去除空白
        m = str(row.get("motivation_type", "")).strip().lower()
        intent = str(row.get("purchase_intent", "")).strip().lower()
        
        # 只分析 Hedonic vs Utilitarian (排除 both/none)
        if m not in ["utilitarian", "hedonic"]:
            continue
            
        is_purchase = intent in ["weak", "strong"]
        
        # 統計次數
        if is_purchase:
            counts[m]["yes"] += 1
        else:
            counts[m]["no"] += 1
            
        # 準備回歸數據 (Hedonic=1, Utilitarian=0)
        x_list.append(1 if m == "hedonic" else 0)
        y_list.append(1 if is_purchase else 0)

    # 3. 執行卡方檢定 (Chi-Square Test)
    print("--- 🔬 Hypothesis Testing (H1) ---")
    u_yes, u_no = counts["utilitarian"]["yes"], counts["utilitarian"]["no"]
    h_yes, h_no = counts["hedonic"]["yes"], counts["hedonic"]["no"]
    
    obs = np.array([[u_yes, u_no], [h_yes, h_no]])
    n = np.sum(obs)
    
    print(f"Valid Sample Size (N): {n}")
    
    # 計算比率
    u_total = u_yes + u_no
    h_total = h_yes + h_no
    u_rate = (u_yes / u_total) * 100 if u_total > 0 else 0
    h_rate = (h_yes / h_total) * 100 if h_total > 0 else 0
    
    print(f"Utilitarian Purchase Rate: {u_rate:.2f}% ({u_yes}/{u_total})")
    print(f"Hedonic Purchase Rate:     {h_rate:.2f}% ({h_yes}/{h_total})")

    # 使用 statsmodels 進行檢定
    table = sm.stats.Table(obs)
    rslt = table.test_nominal_association()
    
    print(f"\n[Chi-Square Result]")
    print(f"Statistic: {rslt.statistic:.4f}")
    print(f"P-value:   {rslt.pvalue:.5f}")
    
    if rslt.pvalue < 0.05:
        print(">> Significant difference detected! (p < 0.05)")
    else:
        print(">> No significant difference.")

    # 4. 執行 Logistic Regression (驗證 Robustness)
    print("\n--- 📈 Logistic Regression Model ---")
    try:
        X_const = sm.add_constant(np.array(x_list)) # 加上截距項
        model = sm.Logit(np.array(y_list), X_const)
        result = model.fit(disp=0)
        
        print(result.summary2().tables[1]) # 印出漂亮的係數表
        
        # 抓取重點
        coef = result.params[1]
        p_val = result.pvalues[1]
        print(f"\nHedonic Coefficient: {coef:.4f}")
        print(f"Model P-value:       {p_val:.5f}")
        
    except Exception as e:
        print(f"Regression skipped: {e}")

if __name__ == "__main__":
    show_stats()