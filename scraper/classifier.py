"""記事の分類: 車種(四輪/二輪) / メーカー / カテゴリ。"""
from config import (
    FOUR_WHEEL_KEYWORDS, TWO_WHEEL_KEYWORDS, TWO_WHEEL_BRANDS,
    OTHER_MAKERS, MITSUBISHI_MODELS, CATEGORY_KEYWORDS,
)


def classify_vehicle(article):
    """車種(four_wheel / two_wheel / unknown)を判定。

    判定順:
      1. URLに xe-may が含まれる → two_wheel
      2. URLに o-to / xe-hoi が含まれる → four_wheel
      3. テキスト内の四輪語/二輪語をカウントして多いほう
      4. 二輪ブランド名が出ていれば → two_wheel
      5. それ以外 → unknown
    """
    url = article.get("url", "").lower()
    if "xe-may" in url or "xemay" in url:
        return "two_wheel"
    if "/o-to" in url or "/oto" in url or "xe-hoi" in url:
        return "four_wheel"

    text = (article.get("title", "") + " " + article.get("summary", "")).lower()

    four_score = sum(1 for kw in FOUR_WHEEL_KEYWORDS if kw.lower() in text)
    two_score = sum(1 for kw in TWO_WHEEL_KEYWORDS if kw.lower() in text)

    if two_score > four_score and two_score > 0:
        return "two_wheel"
    if four_score > two_score and four_score > 0:
        return "four_wheel"

    for brand in TWO_WHEEL_BRANDS:
        if brand.lower() in text:
            return "two_wheel"

    return "unknown"


def classify_makers(article):
    """記事中に登場するメーカー名のリストを返す。

    Mitsubishi は車種名 (Xpander等) も含めて判定する。
    """
    text = article.get("title", "") + " " + article.get("summary", "")
    text_lower = text.lower()

    found = []

    # Mitsubishi 特別扱い
    is_mitsubishi = ("mitsubishi" in text_lower
                     or any(m.lower() in text_lower for m in MITSUBISHI_MODELS))
    if is_mitsubishi:
        found.append("Mitsubishi")

    for maker in OTHER_MAKERS:
        if maker.lower() in text_lower:
            found.append(maker)

    return found


def classify_categories(article):
    """記事のカテゴリを判定して配列で返す(複数該当可)。"""
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    found = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                found.append(cat)
                break  # 同カテゴリ重複登録を避ける
    return found
