#!/usr/bin/env python3
"""Draw the front page summing up Friday 20 November 2026.

"THE WORLD IN ONE DAY" -- a 1024x1024 newspaper front page drawn with
Pillow at build time. main.py (the graded program) only copies the
finished entry.png into the grader's output directory, so this script
runs once here, now, and its output is committed to the repository.

The drawing is fully deterministic: no clock, no network, no input
files, no randomness. Running it twice gives the same bytes.

Stories, each re-checked against live reporting on 20 Nov 2026:
  lead    Trump tells Axios and Reuters he will not decide on Iran
          until after the new year; the Senate rejects a war-powers
          curb 51-48.
  india   Cyclone Akvan: 300,000 people moved to safety in Odisha;
          landfall near Gopalpur on Friday, 423 rescue teams out.
  europe  Berlin summit of the Coalition of the Willing: Europe is
          ready to negotiate with Russia, but only with Ukraine and
          Europe at the table.
  justice The International Court of Justice rules Myanmar committed
          genocide against the Rohingya (9-6) -- the first such
          finding against a state.
  games   GTA 6: Sensor Tower ESTIMATES $1.84bn and 19.05m digital
          copies by launch day. Rockstar and Take-Two confirm no
          figures. The number is flagged as an estimate in the image.
  ticker  Voyager 1 is now a light-day out (its signals take a full
          day; science data stopped 14 Nov), Hayabusa2 retargets
          after ion-engine trouble, Anthropic shares +17% on a
          record IPO debut.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
DEST = Path(__file__).resolve().parent / "entry.png"

# palette
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (20, 20, 18)
TEXT = (60, 58, 52)
MUTED = (110, 108, 100)
CRIMSON = (172, 28, 40)
NAVY = (24, 50, 92)
TEAL = (12, 98, 102)
PLUM = (88, 40, 108)
GOLD = (224, 178, 60)
PALE_BLUE = (214, 222, 234)
DARK_NAVY = (16, 32, 64)

DEJAVU = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{DEJAVU}/DejaVuSerif-Bold.ttf"
SERIF = f"{DEJAVU}/DejaVuSerif.ttf"
SANS = f"{DEJAVU}/DejaVuSans.ttf"
SANS_B = f"{DEJAVU}/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap into lines no wider than `width`."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, text, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((SIZE - w) / 2, y), text, font=fnt, fill=fill)


# ------------------------------------------------------------------ art
def cyclone_spiral(draw, cx, cy, radius, colour):
    """Eight arcs tightening into the eye of the storm."""
    for i in range(8):
        r = radius * (1.0 - i * 0.11)
        start = i * 47
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
                 fill=colour, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


def star_ring(draw, cx, cy, radius, colour):
    """Twelve dots in a circle, the EU emblem."""
    for i in range(12):
        angle = math.radians(i * 30 - 90)
        sx = cx + radius * math.cos(angle)
        sy = cy + radius * math.sin(angle)
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=colour)


def justice_scales(draw, x, y, size, colour):
    """A simple scales-of-justice emblem."""
    top = y + 6
    base = y + size
    mid = x + size // 2
    draw.line([mid, top, mid, base - 14], fill=colour, width=4)
    draw.line([x + 6, top + 16, x + size - 6, top + 16], fill=colour, width=4)
    draw.line([mid, top, mid - 2, top], fill=colour, width=4)
    for side in (-1, 1):
        px = mid + side * (size // 2 - 10)
        draw.line([px, top + 16, px, top + 34], fill=colour, width=3)
        draw.arc([px - 16, top + 30, px + 16, top + 62], 0, 180,
                 fill=colour, width=3)
        draw.line([px - 16, top + 46, px + 16, top + 46], fill=colour, width=3)
    draw.line([mid - 18, base - 6, mid + 18, base - 6], fill=colour, width=4)
    draw.ellipse([mid - 4, top - 4, mid + 4, top + 4], fill=colour)


def game_controller(draw, x, y, width, colour):
    """Rounded gamepad with sticks, d-pad and buttons."""
    height = int(width * 0.52)
    draw.rounded_rectangle([x, y, x + width, y + height],
                           radius=int(height * 0.42), fill=colour)
    for sx in (0.16, 0.68):
        cx = x + int(width * sx)
        cy = y + int(height * 0.55)
        draw.ellipse([cx, cy, cx + 20, cy + 20], fill=PAPER)
    cx, cy = x + int(width * 0.30), y + int(height * 0.38)
    draw.rectangle([cx - 4, cy - 14, cx + 4, cy + 14], fill=PAPER)
    draw.rectangle([cx - 14, cy - 4, cx + 14, cy + 4], fill=PAPER)
    bx, by = x + int(width * 0.78), y + int(height * 0.34)
    for dx, dy in ((0, -10), (10, 0), (0, 10), (-10, 0)):
        draw.ellipse([bx + dx - 5, by + dy - 5, bx + dx + 5, by + dy + 5],
                     fill=GOLD)


def delay_arrow(draw, x, y, width):
    """A timeline: NOV 2026 --(delayed)--> JAN 2027, the 1st circled."""
    draw.line([x, y + 44, x + width, y + 44], fill=INK, width=4)
    draw.polygon([(x + width, y + 44), (x + width - 18, y + 34),
                  (x + width - 18, y + 54)], fill=INK)
    draw.ellipse([x - 8, y + 36, x + 8, y + 52], fill=CRIMSON)
    label = font(SANS_B, 20)
    draw.text((x - 8, y + 62), "NOV 2026", font=label, fill=TEXT)
    draw.text((x + width - 108, y + 62), "JAN 2027", font=label, fill=CRIMSON)
    big = font(SERIF_B, 42)
    draw.text((x + 30, y + 98), "2027", font=big, fill=NAVY)
    draw.ellipse([x + 16, y + 94, x + 156, y + 150], outline=CRIMSON, width=4)
    small = font(SANS, 17)
    draw.text((x + 24, y + 168), "Decision deferred", font=small, fill=MUTED)


# -------------------------------------------------------------- sections
def masthead(draw):
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 56)
    centred(draw, title, 16, tf, INK)
    draw.line([28, 90, 996, 90], fill=INK, width=3)
    draw.line([28, 96, 996, 96], fill=INK, width=1)
    date = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    df = font(SANS_B, 23)
    centred(draw, date, 106, df, CRIMSON)
    tag = "FIVE STORIES  •  ONE DAY  •  EVERYTHING THAT MATTERED"
    tg = font(SANS, 15)
    centred(draw, tag, 136, tg, MUTED)


def panel(draw, x, y, w, h, accent, kicker, head, body, art=None):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 9], fill=accent)
    tx = x + 20
    ty = y + 22
    draw.text((tx, ty), kicker, font=font(SANS_B, 18), fill=accent)
    ty += 30
    head_w = w - 40 if art is None else w - 150
    hf = font(SERIF_B, 25)
    ty = draw_lines(draw, fit_lines(draw, head, hf, head_w), tx, ty,
                    hf, INK, 30) + 8
    bf = font(SANS, 17)
    draw_lines(draw, fit_lines(draw, body, bf, w - 40), tx, ty,
               bf, TEXT, 23)
    if art == "cyclone":
        cyclone_spiral(draw, x + w - 56, y + 58, 30, accent)
    elif art == "ring":
        star_ring(draw, x + w - 60, y + 58, 28, accent)
    elif art == "scales":
        justice_scales(draw, x + w - 128, y + 34, 96, accent)
    elif art == "pad":
        game_controller(draw, x + w - 136, y + 36, 110, accent)


def lead(draw):
    x, y, w, h = 28, 162, 968, 272
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 9], fill=NAVY)
    tx, ty = x + 24, y + 24
    draw.text((tx, ty), "WASHINGTON  —  IRAN", font=font(SANS_B, 19),
              fill=CRIMSON)
    ty += 32
    hf = font(SERIF_B, 42)
    ty = draw_lines(draw, fit_lines(draw, "TRUMP PUTS IRAN DECISION OFF TO 2027",
                                     hf, 590), tx, ty, hf, INK, 48) + 10
    bf = font(SANS, 20)
    body = ("\u201cI\u2019m not rushing into any decision,\u201d the president "
            "tells Axios and Reuters. \u201cWe\u2019ll see what happens after "
            "the beginning of the year.\u201d The Senate votes 51\u201348 "
            "against curbing his war powers.")
    draw_lines(draw, fit_lines(draw, body, bf, 590), tx, ty, bf, TEXT, 26)
    delay_arrow(draw, x + 660, y + 40, 250)


def ticker(draw):
    src = ("Stories reported Friday 20 November 2026  •  Reuters  •  IMD  •  "
           "ICJ  •  NASA  •  Sensor Tower (estimate)")
    sf = font(SANS, 13)
    centred(draw, src, 922, sf, MUTED)
    y0 = 940
    draw.rectangle([28, y0, 996, y0 + 52], fill=INK)
    tick = ("VOYAGER 1 NOW A LIGHT-DAY OUT  •  HAYABUSA2 RETARGETS  •  "
            "ANTHROPIC +17% ON RECORD IPO DEBUT")
    size = 19
    tf = font(SANS_B, size)
    while draw.textlength(tick, font=tf) > 936 and size > 11:
        size -= 1
        tf = font(SANS_B, size)
    centred(draw, tick, y0 + 16, tf, CARD)


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    masthead(draw)
    lead(draw)

    gx, gy, gw, gh = 28, 450, 476, 224
    gx2 = gx + gw + 16
    gy2 = gy + gh + 16

    panel(draw, gx, gy, gw, gh, TEAL, "INDIA  —  CYCLONE",
          "AKVAN: 300,000 MOVED TO SAFETY",
          "The severe cyclone strikes near Gopalpur at noon on Friday; "
          "423 rescue teams deployed, 9,341 shelters ready, 69 trains "
          "cancelled along the coast.",
          art="cyclone")
    panel(draw, gx2, gy, gw, gh, NAVY, "EUROPE  —  UKRAINE",
          "EUROPE READY TO TALK TO RUSSIA",
          "At a Berlin summit of Kyiv\u2019s allies, leaders say they will "
          "negotiate to end the war \u2014 but only with Ukraine and "
          "Europe at the table.",
          art="ring")
    panel(draw, gx, gy2, gw, gh, CRIMSON, "THE HAGUE  —  JUSTICE",
          "MYANMAR COMMITTED GENOCIDE",
          "The ICJ rules 9\u20136 on the 2017 campaign against the "
          "Rohingya \u2014 the first genocide finding against a state.",
          art="scales")
    panel(draw, gx2, gy2, gw, gh, PLUM, "GAMES  —  BUSINESS",
          "GTA 6: $1.84 BILLION*",
          "Sensor Tower estimates 19.05m digital copies by launch day, "
          "19 Nov. Rockstar and Take-Two confirm no figures. "
          "*Estimate, not official.",
          art="pad")

    ticker(draw)
    img.save(DEST, optimize=True)
    print("wrote", DEST, DEST.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
