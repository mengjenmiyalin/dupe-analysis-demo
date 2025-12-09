import re
import jieba
import pandas as pd
from typing import List
# 從我們的設定檔匯入STOPWORDS，也就是 "的", "了" 這種沒什麼意義的字來做斷句
from .config import STOPWORDS

# 【自定義字典】
# 告訴 jieba 這些詞很重要，不要亂切，也不要過濾掉
jieba.add_word("cp值")  # 因為我們在等一下的步驟會把不論大小寫都轉成小寫了，所以這裡設定小寫
jieba.add_word("dupe")
jieba.add_word("fomo") # 應該是沒什麼人會提到啦但就示範一下
jieba.add_word("平替")

def basic_clean(text: str) -> str:
    """
    【功能】基礎版大掃除
    把text裡面對於「語意分析」沒有幫助的雜質清掉。
    """
    # 防呆：如果這一格是空的(NaN)或不是文字，直接回傳空字串，不然程式會報錯
    if not isinstance(text, str):
        return ""
    
    # 1.【移除網址】
    # 網址(http...)對分析「情感」或「動機」通常沒用，而且會干擾我們斷詞
    text = re.sub(r"http\S+", "", text)
    
# 2.【叫他保留中文、英文、數字】
    # 如果我們不看CP值這種有包含英文的字的話，就要叫他不是中文的部分都變空白，像醬：r"[^\u4e00-\u9fff]+"
    # 現在是 r"[^a-zA-Z0-9\u4e00-\u9fff]+"
    # 意思就是：除了「英文、數字、中文」以外的符號（如標點、表情符號），全部變空白
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", " ", text)
    
    # 記得把英文全部轉成小寫
    # 這樣 "CP", "cp", "Cp" 就會被當成同一個字計算，詞頻才會準！
    text = text.lower()
    
    # 3.【整理空白】
    # 把因為刪除英數而留下的多餘空白 (例如 "  ") 縮成一個空格
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def tokenize(text: str) -> List[str]:
    """
    【功能】斷詞 (Tokenization)
    把一句話切成單字，並過濾掉沒用的廢話 (剛剛說的STOPWORDS)。
    """
    # 1. 先做上面的基礎掃除
    cleaned = basic_clean(text)
    
    # 2. 用jieba切割 (lcut 會回傳一個清單 list)
    # 3. 列表推導式 (List Comprehension，這只是一個聽起來很難的詞，反正就是我們列一堆條件給他ㄛ)：
    #   把切好的那堆詞，一個一個拿出來看（暫時叫做 t）-> 確認 t 不是空的（有時候 jieba 會切出空字串，要濾掉）
    #   ->確認 t 不是廢話（像「的」、「了」）。
    #   ->如果上面兩關都過了，就把這個 t 放進新名單。
    #   目的：只保留「不是空字串」且「不在停用詞名單」的詞
    tokens = [t for t in jieba.lcut(cleaned) if t and t not in STOPWORDS]
    
    return tokens

def add_token_column(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    """
    【功能】Pipeline 的接口
    很好，我們現在拿到一整張表 (DataFrame)了，幫每一列都做完斷詞，然後回傳新的表df。
    """
    # 複製一份（另存新檔的意思，這樣原始的資料就不會被我們動到比較保險）
    df = df.copy()
    
    df["tokens"] = df[text_col].apply(tokenize)
    # df[text_col] = 我們在另存新檔的表上選則某一欄
    # apply(tokenize) ＝ 叫他幫我們自動把這欄的每個字都丟到(tokenize)這個斷詞加工處跑一次
    # df["tokens"] = 把加工好的那些結果丟到另一個欄位"tokens"裡面
    
    return df
    # 把這張處理好的新表格交出去