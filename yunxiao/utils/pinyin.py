from typing import Optional
from pypinyin import pinyin, Style

def get_pinyin(text: str, separator: Optional[str] = '') -> str:
    return separator.join([item[0] for item in pinyin(text, style=Style.NORMAL)])
