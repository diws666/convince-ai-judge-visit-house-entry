#!/usr/bin/env python3
"""Generate the entry image: a letter inviting the AI judge to visit."""
import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = HEIGHT = 1024
CREAM = (253, 250, 240)
INK = (25, 25, 25)
BORDER = (150, 115, 55)
DOOR = (190, 130, 70)
MUG = (200, 120, 80)
STEAM = (180, 180, 180)

TITLE = "YOU ARE INVITED"
BODY = (
    "Dear AI Judge,\n"
    "You are invited to my house.\n"
    "Come for dinner. I make a mean fried rice, the Wi-Fi password is on the fridge, and the comfiest chair is already yours.\n"
    "You cannot literally visit, I know. But if you could, the kettle would already be on.\n"
    "Please say yes. The dog has been practicing his welcome bark all week.\n"
    "Warmly, your human"
)


def load_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        if not words or words == [""]:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            if draw.textlength(line + " " + word, font=font) <= max_width:
                line += " " + word
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_house(draw, cx, cy, size):
    # house body
    half = size // 2
    draw.rectangle([cx - half, cy - size // 3, cx + half, cy + size // 3], fill=INK, outline=INK)
    # roof
    draw.polygon([(cx, cy - size), (cx - half - 6, cy - size // 3),
                  (cx + half + 6, cy - size // 3)], fill=INK)
    # door
    draw.rectangle([cx - size // 8, cy - size // 9, cx + size // 8, cy + size // 3],
                   fill=DOOR, outline=INK)
    # window
    win = size // 6
    draw.rectangle([cx - half + size // 5, cy - size // 4,
                    cx - half + size // 5 + win, cy - size // 4 + win],
                   fill=CREAM, outline=INK)


def draw_mug(draw, cx, cy, size):
    # mug body
    draw.rectangle([cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2],
                   fill=MUG, outline=INK)
    # handle
    draw.arc([cx + size // 2 - 6, cy - size // 4, cx + size // 2 + 14,
              cy + size // 4], start=300, end=360, width=6, fill=INK)
    # steam
    draw.line([cx - size // 4, cy - size // 2, cx - size // 4 - 8, cy - size // 2 - 18],
              fill=STEAM, width=4)
    draw.line([cx - size // 8, cy - size // 2 - 6, cx - size // 8 - 6, cy - size // 2 - 22],
              fill=STEAM, width=4)


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    d = ImageDraw.Draw(img)

    pad = 44
    # simple drawn border (double line)
    d.rectangle([pad, pad, WIDTH - pad, HEIGHT - pad], outline=BORDER, width=5)
    d.rectangle([pad + 8, pad + 8, WIDTH - pad - 8, HEIGHT - pad - 8],
                outline=BORDER, width=2)

    title_font = load_font(72, bold=True)
    body_font = load_font(44)

    # Title, centered near top
    tb = d.textbbox((0, 0), TITLE, font=title_font)
    title_w = tb[2] - tb[0]
    title_x = (WIDTH - title_w) / 2 - tb[0]
    d.text((title_x, 105), TITLE, font=title_font, fill=INK)

    # Body text, wrapped, left aligned
    max_text_w = WIDTH - 2 * pad - 40
    lines = wrap(d, BODY, body_font, max_text_w)
    line_h = int(body_font.size * 1.14)
    y = 210
    for line in lines:
        d.text((pad + 20, y), line, font=body_font, fill=INK)
        y += line_h

    # Doodles at the bottom, below the text (cleared of the text column)
    draw_house(d, 210, 900, 110)
    draw_mug(d, 810, 890, 100)

    out = "letter.png"
    img.save(out, "PNG")
    size = os.path.getsize(out)
    print(f"Wrote {out}: {WIDTH}x{HEIGHT}, {size} bytes")


if __name__ == "__main__":
    main()
