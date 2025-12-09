from pathlib import Path
import pandas as pd
from .config import RAW_DIR, PROCESSED_DIR

def load_raw_posts(filename: str = "dupe_posts_sample.csv") -> pd.DataFrame:
    """
    【功能說明】
    這支函式負責去data/raw這個資料夾把CSV檔案抓進來。
    
    【參數設定】
    filename (str): 你要讀哪一個檔案？預設是 "dupe_posts_sample.csv"。
                    如果要讀別的，呼叫時可以再來改，例如：load_raw_posts("my_new_data.csv")
    
    【回傳結果】
    pd.DataFrame: 讀取成功後，會吐出一個Pandas表格讓我們後續分析。
    """
    # 組合出完整的檔案路徑 (例如: C:/Users/.../data/raw/dupe_posts_sample.csv)
    path = RAW_DIR / filename
    
    # 【防呆機制】
    # 先檢查檔案在不在！如果不檢查直接讀，檔案不存在時程式會一直噴FileNotFoundError很煩ㄉ（問就是有過）。
    # 這裡我們讓確認清楚有沒有檔案，就可以事先知道：「這檔案找不到喔，要重新檢查路徑！」
    if not path.exists():
        raise FileNotFoundError(f"找不到原始資料檔，請確認這個路徑是否有檔案：{path}")
    
    df = pd.read_csv(path)
    return df

def save_processed(df: pd.DataFrame, filename: str = "dupe_posts_cleaned.csv") -> Path:
    """
    【功能說明】
    這段函式負責把我們「清洗完、斷詞完」的乾淨資料存檔。
    它會自動存到data/processed資料夾，這樣不會跟原始資料混在一起。
    """
    # 【自動建資料夾（mkdir）】
    # 如果電腦裡還沒有 data/processed 這個資料夾，這行程式會自動幫你建一個。
    # parents=True代表如果連上一層目錄（他爸媽）都沒有，也會順便幫你建好，不用手動去按右鍵新增。
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    out_path = PROCESSED_DIR / filename
    
    # 【存檔關鍵】
    # encoding='utf-8-sig'非常重要！
    # 如果只用utf-8，中文在Excel打開會變成亂碼。加了-sig就可以在Excel正常顯示中文。
    # index=False是在跟他說不要把0, 1, 2...這種索引數字存進去（就像是excel最左邊都會有的那種小灰數字），保持版面乾淨。
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    
    return out_path