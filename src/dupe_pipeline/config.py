from pathlib import Path

# 專案根目錄 = 這個檔案所在位置往上兩層
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORT_DIR = ROOT_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

# 一些簡單的分析參數
MIN_WORD_FREQ = 3  # 過濾太少見的字
STOPWORDS = {
    "的", "了", "是", "也", "在", "有", "和", "跟", "就", "會",
    "其實", "真的"
}

# 為什麼我們需要這個檔案？ 這個檔案的目的是「幫我們的程式碼找到回家的路」。
# 如果我在程式碼裡面把檔案的路徑寫死，那換到研究室的電腦就不能用了ＱＱ
# 所以我們在這邊寫好告訴他說檔案要去哪裡找，讓他動抓出「現在這個專案資料夾在哪裡」，這樣不管換到哪台電腦都能跑惹！