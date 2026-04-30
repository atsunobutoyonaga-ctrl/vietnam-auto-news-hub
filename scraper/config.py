"""Vietnam Auto News Hub - スクレイパー設定値

ここを編集すれば、ソース・除外キーワード・分類辞書を変更できる。
ロジック側のファイル (filter.py / classifier.py / fetcher.py / main.py) は変更不要。
"""

# ----------------------------------------------------------------------
# 取得ソース
# ----------------------------------------------------------------------

# ベトナム主要ニュースサイト RSS
RSS_SOURCES = [
    {"name": "VnExpress",  "url": "https://vnexpress.net/rss/oto-xe-may.rss",   "category": "general"},
    {"name": "VietnamNet", "url": "https://vietnamnet.vn/rss/oto-xe-may.rss",   "category": "general"},
    {"name": "Tuoi Tre",   "url": "https://tuoitre.vn/rss/xe.rss",              "category": "general"},
    {"name": "Dan Tri",    "url": "https://dantri.com.vn/rss/o-to-xe-may.rss",  "category": "general"},
    {"name": "Thanh Nien", "url": "https://thanhnien.vn/rss/xe.rss",            "category": "general"},
    {"name": "AutoPro",    "url": "https://autopro.com.vn/xe-may.rss",          "category": "specialty"},
]

# Google News RSS (3クエリ並走で Mitsubishi 強化)
GOOGLE_NEWS_SOURCES = [
    {
        "name": "Google News (Mitsubishi EN)",
        "url": "https://news.google.com/rss/search?q=Mitsubishi+Vietnam&hl=en-US&gl=US&ceid=US:en",
        "category": "googlenews",
    },
    {
        "name": "Google News (Mitsubishi VI)",
        "url": "https://news.google.com/rss/search?q=Mitsubishi+Vi%E1%BB%87t+Nam&hl=vi&gl=VN&ceid=VN:vi",
        "category": "googlenews",
    },
    {
        "name": "Google News (Models)",
        "url": "https://news.google.com/rss/search?q=Xpander+OR+Triton+OR+Outlander+OR+Pajero+OR+Attrage&hl=vi&gl=VN&ceid=VN:vi",
        "category": "googlenews",
    },
]

MAX_PER_SOURCE = 50  # 各ソース最大取得件数

# ----------------------------------------------------------------------
# 除外キーワード(交通事故・違反系)
# ----------------------------------------------------------------------
EXCLUSION_KEYWORDS = [
    # 事故系
    "tai nạn", "đâm", "va chạm", "lật xe", "đụng",
    # 違反系
    "phạt", "vi phạm", "biên bản", "CSGT", "cảnh sát giao thông",
    "quá tốc độ", "không biển số",
    # 飲酒・薬物
    "say xỉn", "nồng độ cồn", "rượu bia", "ma túy",
    # 死傷系
    "tử vong", "chết", "thiệt mạng", "bị thương", "cấp cứu",
    # 運転トラブル
    "buồn ngủ", "cãi cọ", "thót tim",
    # 犯罪
    "trộm", "cướp",
]

# ----------------------------------------------------------------------
# 車種判定キーワード
# ----------------------------------------------------------------------
FOUR_WHEEL_KEYWORDS = [
    "ô tô", "oto", "xe hơi", "xe ô tô", "sedan", "suv", "crossover",
    "MPV", "hatchback", "coupe", "pickup", "bán tải", "minivan",
]

TWO_WHEEL_KEYWORDS = [
    "xe máy", "xe gắn máy", "xe tay ga", "scooter", "mô tô", "moto",
    "xe điện hai bánh", "xe đạp điện",
]

# 二輪と判別が分かりにくいケース用のブランド辞書
TWO_WHEEL_BRANDS = [
    "Yadea", "Vespa", "Piaggio", "SYM", "Honda Wave", "Honda Vision", "Honda SH",
    "Yamaha Exciter", "Yamaha Sirius", "VinFast Klara", "VinFast Evo",
    "VinFast Theon", "VinFast Vento",
]

# ----------------------------------------------------------------------
# メーカー判定
# ----------------------------------------------------------------------

# Mitsubishi 特別扱い: 車種名でも Mitsubishi として認識
MITSUBISHI_MODELS = [
    "Xpander", "Outlander", "Pajero", "Triton", "Attrage", "Mirage", "Eclipse Cross",
]

# 22メーカー (Mitsubishi 除く)
OTHER_MAKERS = [
    "Toyota", "Honda", "Mazda", "Nissan", "Suzuki", "Isuzu",
    "Hyundai", "Kia", "VinFast", "BYD", "Chery", "Geely", "MG",
    "Wuling", "Haval", "Ford", "Mercedes", "BMW", "Audi", "Porsche",
    "Skoda", "Volvo",
]

# ----------------------------------------------------------------------
# カテゴリ判定キーワード
# ----------------------------------------------------------------------
CATEGORY_KEYWORDS = {
    "EV":     ["xe điện", "EV", "BEV", "electric vehicle"],
    "HEV":    ["hybrid", "HEV", "PHEV"],
    "Policy": ["thuế", "chính sách", "quy định", "nghị định"],
    "Sales":  ["doanh số", "tiêu thụ", "bán chạy"],
    "Launch": ["ra mắt", "công bố", "giới thiệu"],
    "Recall": ["triệu hồi", "thu hồi", "recall"],
}
