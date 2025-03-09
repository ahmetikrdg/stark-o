import re

import pandas as pd


def clean_text(text):
    if pd.isna(text) or text is None:
        print("Boş veya NaN değer bulundu!")
        return ""
    try:
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\@\w+', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text
    except Exception as e:
        print(f"Temizleme sırasında hata: {e} için değer: {text}")
        return ""
