"""Build the 30-card TOMONOWA preview and exact-type print PNGs.

Usage: python tools/build_mikuji.py PATH_TO_EXISTING_20_CARD_FOLDER
The original twenty files are copied without changing their wording or design.
"""

from __future__ import annotations

import html
import json
import shutil
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "mikuji"
PREVIEW = ROOT / "mikuji-preview"
CARDS = json.loads((ROOT / "mikuji" / "new-cards.json").read_text(encoding="utf-8"))
FONT_GOTHIC = Path("C:/Windows/Fonts/NotoSansJP-VF.ttf")
FONT_MINCHO = Path("C:/Windows/Fonts/yumin.ttf")
KANJI = {
    21: "二十一", 22: "二十二", 23: "二十三", 24: "二十四", 25: "二十五",
    26: "二十六", 27: "二十七", 28: "二十八", 29: "二十九", 30: "三十",
}


def gothic(size: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(FONT_GOTHIC), size)
    font.set_variation_by_axes([900])
    return font


def render_card(card: dict) -> None:
    columns = card["columns"]
    image = Image.new("RGB", (1448, 1086), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rectangle((70, 118, 1378, 1001), outline="#777777", width=4)

    header_font = ImageFont.truetype(str(FONT_MINCHO), 57)
    header = f"第　{KANJI[card['number']]}　番"
    draw.text((724, 24), header, font=header_font, fill="#707070", anchor="mt")

    compact = len(columns) >= 8 or max(map(len, columns)) >= 8
    size = 89 if compact else 103
    pitch_x = 130 if compact else 153
    pitch_y = 92 if compact else 108
    font = gothic(size)
    group_width = (len(columns) - 1) * pitch_x
    first_x = 724 + group_width / 2
    top_y = 222
    assert first_x + size / 2 < 1378 and first_x - group_width - size / 2 > 70
    assert top_y + (max(map(len, columns)) - 1) * pitch_y + size / 2 < 990
    for column_index, column in enumerate(columns):
        x = first_x - column_index * pitch_x
        for row_index, character in enumerate(column):
            y = top_y + row_index * pitch_y
            if character in "、。":
                # Noto's horizontal punctuation ink sits in the lower-left of its
                # em box. Shift the ink to the upper-right of the vertical cell.
                draw.text((x + size * 0.64, y - size * 0.60), character, font=font, fill="#090909", anchor="mm")
            else:
                draw.text((x, y), character, font=font, fill="#090909", anchor="mm")

    footer_font = ImageFont.truetype(str(FONT_MINCHO), 30)
    draw.text((72, 1020), "TOMONOWA ひとことみくじ", font=footer_font, fill="#707070")
    image.save(OUTPUT / f"fortune-{card['number']:02d}.png", optimize=True)


def build_preview() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    titles = {card["number"]: "".join(card["columns"]) for card in CARDS}
    tiles = []
    for number in range(1, 31):
        filename = f"fortune-{number:02d}.png"
        image_url = f"../assets/mikuji/{filename}" + ("?v=short-boat-3" if number == 21 else "?v=vertical-punctuation-2" if number > 20 else "")
        alt = titles.get(number, f"恋みくじ {number}番")
        tag = "NEW / 恋・友達・人生" if number > 20 else "恋みくじ"
        tiles.append(
            f'<figure><a href="{image_url}"><img src="{image_url}" '
            f'alt="{html.escape(alt, quote=True)}" loading="lazy"></a>'
            f'<figcaption><span>{number:02d} / {tag}</span>'
            f'{html.escape(alt)}</figcaption></figure>'
        )
    page = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>TOMONOWAみくじ｜30枚確認用</title>
<style>*{box-sizing:border-box}body{margin:0;background:#101418;color:#edf4f7;font-family:system-ui,sans-serif}
header{max-width:1200px;margin:auto;padding:42px 22px 20px}a{color:inherit}h1{font-size:clamp(26px,5vw,44px);margin:8px 0 16px}
p{line-height:1.8;color:#bfd0db}header a{display:inline-block;padding:12px 18px;background:#9cd4ed;color:#10222d;text-decoration:none;font-weight:700}
main{max-width:1200px;margin:auto;padding:20px 22px 80px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
figure{margin:0;background:#1d2831}img{width:100%;height:auto;display:block}figcaption{padding:14px 18px;line-height:1.6;font-size:13px}
figcaption span{display:block;color:#9cd4ed;font-size:11px;letter-spacing:.08em;margin-bottom:6px}
@media(max-width:700px){main{grid-template-columns:1fr;gap:18px;padding-inline:12px}header{padding-inline:16px}}
</style></head><body><header><p>REVIEW COPY / 全30枚</p><h1>TOMONOWAみくじ</h1>
<p>既存の恋みくじ20枚に、恋・友達・人生の一言を10枚追加。画像をタップすると原寸で確認できます。</p>
<a href="../assets/mikuji/TOMONOWA-mikuji-30.zip?v=short-boat-3" download>30枚をまとめて保存（ZIP）</a></header>
<main>""" + "\n".join(tiles) + "</main></body></html>"
    (PREVIEW / "index.html").write_text(page, encoding="utf-8")


def build_contact_sheet() -> None:
    sheet = Image.new("RGB", (1448, 2720), "#dce4e8")
    for offset, card in enumerate(CARDS):
        with Image.open(OUTPUT / f"fortune-{card['number']:02d}.png") as image:
            thumbnail = image.convert("RGB").resize((700, 525), Image.Resampling.LANCZOS)
            x = 16 + (offset % 2) * 716
            y = 16 + (offset // 2) * 540
            sheet.paste(thumbnail, (x, y))
    sheet.save(PREVIEW / "new-10-contact.png", optimize=True)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Pass the existing 20-card folder as the only argument")
    original = Path(sys.argv[1]).resolve()
    missing = [number for number in range(1, 21) if not (original / f"fortune-{number:02d}.png").is_file()]
    if missing:
        raise SystemExit(f"Missing original cards: {missing}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for number in range(1, 21):
        filename = f"fortune-{number:02d}.png"
        shutil.copyfile(original / filename, OUTPUT / filename)
    for card in CARDS:
        render_card(card)
    archive = OUTPUT / "TOMONOWA-mikuji-30.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for number in range(1, 31):
            filename = f"fortune-{number:02d}.png"
            package.write(OUTPUT / filename, filename)
    build_preview()
    build_contact_sheet()
    print(f"Built 30 cards, {archive}, and {PREVIEW / 'index.html'}")


if __name__ == "__main__":
    main()
