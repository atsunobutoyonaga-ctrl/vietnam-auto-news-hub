"""記事の除外判定。

タイトル+サマリー本文に除外キーワードが含まれていれば True を返す。
"""
from config import EXCLUSION_KEYWORDS


def is_excluded(article):
    """事故・違反系などの除外対象かを判定。

    Args:
        article: dict. title と summary キーを持つ。

    Returns:
        bool. True なら除外。
    """
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    for kw in EXCLUSION_KEYWORDS:
        if kw.lower() in text:
            return True
    return False
