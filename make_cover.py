"""
Zenn用カバー画像生成スクリプト (500×250px)
books/rag-multiagent-build/cover.png を出力
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 500, 250
OUT = os.path.join("books", "rag-multiagent-build", "cover.png")

# --- カラーパレット ---
BG_TOP    = (15,  23,  42)   # ダークネイビー
BG_BOTTOM = (30,  41,  59)   # 少し明るいネイビー
ACCENT    = (99, 202, 183)   # ティール
TEXT_MAIN = (248, 250, 252)  # ほぼ白
TEXT_SUB  = (148, 163, 184)  # グレー

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

# グラデーション背景
for y in range(H):
    ratio = y / H
    r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
    g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
    b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# アクセントライン（左側バー）
draw.rectangle([20, 30, 26, H - 30], fill=ACCENT)

# 右上に小さなドットパターン（装飾）
for dx in range(6):
    for dy in range(4):
        cx = W - 60 + dx * 10
        cy = 20 + dy * 10
        draw.ellipse([cx, cy, cx+4, cy+4], fill=(60, 80, 100))

# フォント設定（システムフォントをフォールバック付きで取得）
def get_font(size):
    paths = [
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/YuGothM.ttc",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_title   = get_font(26)
font_sub     = get_font(14)
font_en      = get_font(11)

# タグライン
draw.text((40, 32), "実践技術書", font=font_en, fill=ACCENT)

# メインタイトル
draw.text((40, 58), "RAGマルチエージェント", font=font_title, fill=TEXT_MAIN)
draw.text((40, 96), "実装ガイド", font=font_title, fill=TEXT_MAIN)

# サブタイトル
draw.text((40, 140), "Dify・LangGraph・Azure で構築する", font=font_sub, fill=TEXT_SUB)
draw.text((40, 160), "8エージェント構成の完全設計", font=font_sub, fill=TEXT_SUB)

# 区切り線
draw.line([(40, 190), (W - 40, 190)], fill=(50, 70, 90), width=1)

# キーワード
keywords = ["#RAG", "#LLM", "#マルチエージェント", "#LoRA", "#土木DX"]
kfont = get_font(11)
x = 40
for kw in keywords:
    bbox = draw.textbbox((0, 0), kw, font=kfont)
    tw = bbox[2] - bbox[0]
    draw.text((x, 200), kw, font=kfont, fill=ACCENT)
    x += tw + 14
    if x > W - 60:
        break

img.save(OUT, "PNG")
print(f"Saved: {OUT} ({W}x{H}px)")
