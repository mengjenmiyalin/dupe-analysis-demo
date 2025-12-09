from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# 這裡把我們剛剛寫好的檔案 (零件) 匯入進來
# config: 設定檔 （告訴電腦資料放哪）
# data_io: 搬運工 (讀寫檔案)
# cleaning: 清潔工 (斷詞＋去掉雜質)
from .config import FIGURE_DIR, MIN_WORD_FREQ, REPORT_DIR
from .data_io import load_raw_posts, save_processed
from .cleaning import add_token_column

def compute_word_freq(df: pd.DataFrame) -> pd.DataFrame:
    """
    【功能】計算詞頻 (Word Frequency)
    這是最基礎的文本分析，看看大家都在討論什麼關鍵字（文字雲的前身）。
    """
    # 1. 把所有貼文的 tokens (斷詞結果) 全部放在一起變成一個超級長的清單
    # 例如: [['平替', '好用'], ['平替', '便宜']] -> ['平替', '好用', '平替', '便宜']
    all_tokens = [t for tokens in df["tokens"] for t in tokens]
    
    # 2. 使用 Python 內建的好棒棒工具Counter自動計算出現次數
    counter = Counter(all_tokens)
    
    # 3. 過濾掉出現次數太少的詞 (雜職)
    # MIN_WORD_FREQ我們在config.py裡設定成 3，代表出現不到 3 次的詞我們不看
    rows = [
        {"token": token, "freq": freq}
        for token, freq in counter.items()
        if freq >= MIN_WORD_FREQ
    ]
    
    # 4. 轉成表格並依照頻率由大到小排序 (ascending=False代表降冪排序：大->小)
    return pd.DataFrame(rows).sort_values("freq", ascending=False)
    # pd.DataFrame(rows)=把清單變成 Excel 表
    # .sort_values("freq") = 依照某個欄位排順序，我們這裡指令用freq，也就頻率這欄
    # ascending=False = 從小排到大「的相反」，所以越大越前面

def plot_top_words(freq_df: pd.DataFrame, top_n: int = 20) -> Path:
    """
    【功能】畫圖
    畫出前 N 名的熱門關鍵字長條圖，並存成圖片。
    """
    # 確保圖片資料夾存在 (沒有的話幫我蓋一個資料夾)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # 【解決中文亂碼問題】
    # 這是告訴 Matplotlib請優先找這些字體來用 (Mac 常用 Heiti TC 或 Arial Unicode MS)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC', 'Microsoft JhengHei', 'SimHei']
    # 這行是為了解決負號 '-' 有時候也會變亂碼的問題（我遇到的是空白框框ＴＡＴ）
    plt.rcParams['axes.unicode_minus'] = False
    
    # 只取前 20 名
    top = freq_df.head(top_n)
    
    # 開始畫畫 (Matplotlib 設定)
    plt.figure(figsize=(10, 6)) # 設定畫布大小
    
    # 畫長條圖 (x軸=詞，y軸=頻率，顏色=天空藍，都可以在調)
    plt.bar(top["token"], top["freq"], color='skyblue')
    
    # 設定標題和xy標籤
    plt.title("Top Words Frequency (Study 1)", fontsize=16)
    plt.xlabel("Tokens", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    
    # x 軸文字轉 45 度，避免字擠在一起 （也可以不轉啦，圖清楚就好）
    plt.xticks(rotation=45, ha="right")
    
    # 自動調整版面，不要讓字被切掉
    plt.tight_layout() 
    
    # 存檔
    out_path = FIGURE_DIR / "word_freq_top.png"
    plt.savefig(out_path, dpi=300) # dpi=300 代表高解析度
    plt.close() # 畫完要關掉，釋放記憶體，如果電腦記憶體夠大當我雞婆
    
    return out_path

def main():
    print("✨Pipeline START...")

    # 1. Load raw data
    df_raw = load_raw_posts()
    print(f"1. Successfully loaded raw data. Total rows: {len(df_raw)}")
    
    # 2. Clean + tokenize
    print("2. Cleaning and tokenizing data...")
    df_clean = add_token_column(df_raw)

    clean_path = save_processed(df_clean)
    print(f"   -> Cleaned data saved to: {clean_path}")


    # 3. 分析 Analyze word frequency
    print("3. Computing word frequency...")
    freq_df = compute_word_freq(df_clean)
    
    # 【為 Datawrapper 準備資料】
    # 我們把算好的頻率表存成 CSV，這樣你就可以直接把這個檔丟進 Datawrapper（一個繪圖軟體，如果直接用python生的圖也可以啦）
    dw_csv_path = REPORT_DIR / "data_for_datawrapper.csv"
    freq_df.to_csv(dw_csv_path, index=False, encoding='utf-8-sig')
    print(f"   -> [IMPORTANT] Datawrapper export saved to: {dw_csv_path}")

    # 印出前 5 名
    top_5 = freq_df.head(5)['token'].tolist()
    print(f"   -> Top 5 keywords identified: {top_5}")

    # 4. 畫圖 Plotting
    print("4. Generating automated plots...")
    fig_path = plot_top_words(freq_df)
    print(f"   -> Figure saved to: {fig_path}")
    
    print("✅ Pipeline DONE！")

if __name__ == "__main__":
    main()