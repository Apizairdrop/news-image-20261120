#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

A 1024x1024 newspaper front page, "THE WORLD IN ONE DAY", rendered with
Pillow at build time. Deterministic on purpose: fixed random seed, no
clock, no network, no file reads outside this script. Run it and it writes
entry.png next to this file; main.py is what the grader runs, and it only
copies that PNG to the output directory.

Stories (all re-checked against live reporting on 20 Nov 2026):
  lead   Trump tells Axios/Reuters he will decide on Iran after the new
         year; Senate rejects a war-powers curb 51-48.
  india  Cyclone Akvan: 300,000+ evacuated in Odisha, landfall at noon
         near Gopalpur, 423 rescue teams out.
  europe Berlin summit: Europe ready to negotiate with Russia, but only
         with Ukraine and Europe at the table.
  space  Voyager 1 reaches one light-day from Earth; Hayabusa2 retargets
         after ion-engine trouble.
  games  GTA 6: Sensor Tower estimates $1.84bn / 19.05m copies by launch
         day (19 Nov) -- an estimate, not an official figure.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (248, 244, 235)
CARD = (255, 255, 255)
INK = (18, 18, 18)
BODY = (58, 58, 54)
RED = (178, 30, 42)
NAVY = (22, 48, 90)
TEAL = (13, 96, 104)
GOLD = (180, 128, 24)
PLUM = (82, 38, 102)
FAINT = (96, 96, 92)
STAR = (255, 213, 92)
PALE = (216, 222, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def blurb(d, lines, x, y, font, fill, step):
    """Draw wrapped lines, return the y below the last one."""
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def flag(d, x, y, text, color, size=19):
    """Small caps kicker line; returns y below it."""
    d.text((x, y), text, font=fnt(SANS_B, size), fill=color)
    return y + size + 8


# ---------------------------------------------------------------- icons
def draw_spiral(d, cx, cy, radius, color):
    """Seven overlapping arcs shrinking toward the eye of the storm."""
    for i in range(7):
        start = i * 52
        r = radius * (1.0 - i * 0.115)
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 235,
              fill=color, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)


def draw_stars(d, x, y, w, h, rng):
    """Deterministic starfield inside a rectangle."""
    for _ in range(24):
        sx = x + rng.randint(0, w)
        sy = y + rng.randint(0, h)
        r = rng.choice((1, 1, 2))
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))


def draw_probe(d, x, y):
    """A tiny deep-space probe: gold dish, grey bus, antenna."""
    d.polygon([(x, y + 8), (x + 30, y + 18), (x, y + 28)], fill=(205, 212, 226))
    d.ellipse([x + 24, y, x + 44, y + 20], outline=STAR, width=3)
    d.line([x + 6, y + 18, x - 14, y + 34], fill=(205, 212, 226), width=3)
    d.line([x + 2, y + 6, x - 6, y - 8], fill=STAR, width=2)


def draw_pad(d, x, y, w, color):
    """Game controller: rounded body, two sticks, d-pad, four buttons."""
    h = int(w * 0.54)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(h * 0.44), fill=color)
    for sx in (int(w * 0.17), int(w * 0.71)):
        d.ellipse([x + sx, y + int(h * 0.52), x + sx + 22, y + int(h * 0.52) + 22],
                  fill=PAPER)
    cx, cy = x + int(w * 0.26), y + int(h * 0.36)
    d.rectangle([cx - 4, cy - 15, cx + 4, cy + 15], fill=PAPER)
    d.rectangle([cx - 15, cy - 4, cx + 15, cy + 4], fill=PAPER)
    bx, by = x + int(w * 0.76), y + int(h * 0.32)
    for dx, dy in ((0, -11), (11, 0), (0, 11), (-11, 0)):
        d.ellipse([bx + dx - 5, by + dy - 5, bx + dx + 5, by + dy + 5],
                  fill=STAR)


def draw_calendar(d, x, y, w, h):
    """Wall calendar flipped to January 2027, the 1st circled in red."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=INK, width=3)
    d.rounded_rectangle([x, y, x + w, y + 50], radius=10, fill=RED)
    d.rectangle([x, y + 38, x + w, y + 50], fill=RED)
    label = "JANUARY 2027"
    lf = fnt(SANS_B, 29)
    d.text((x + (w - d.textlength(label, font=lf)) / 2, y + 10), label,
           font=lf, fill=CARD)
    for rx in (x + 54, x + w - 54):
        d.line([rx, y - 10, rx, y + 12], fill=INK, width=6)
    for row in range(4):
        for col in range(7):
            dx = x + 36 + col * 32
            dy = y + 80 + row * 32
            d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(182, 182, 174))
    d.ellipse([x + 18, y + 62, x + 54, y + 98], outline=RED, width=5)
    d.text((x + 20, y + 104), "2027", font=fnt(SERIF, 62), fill=NAVY)


def draw_eu_ring(d, cx, cy, r):
    """Ring of twelve small stars, the EU emblem, in navy on white."""
    import math
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx = cx + r * math.cos(a)
        sy = cy + r * math.sin(a)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=NAVY)


# ---------------------------------------------------------------- layout
def story_card(d, x, y, w, h, accent, kick, head, body, art=None):
    """One white panel: coloured top bar, kicker, headline, body, art."""
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 9], fill=accent)
    tx, ty = x + 20, y + 22
    ty = flag(d, tx, ty, kick, accent)
    head_w = w - 40 if art is None else w - 168
    hf = fnt(SERIF_B, 27)
    ty = blurb(d, wrap_text(d, head, hf, head_w), tx, ty, hf, INK, 33) + 6
    bf = fnt(SANS, 18)
    blurb(d, wrap_text(d, body, bf, w - 40), tx, ty, bf, BODY, 24)
    if art == "spiral":
        draw_spiral(d, x + w - 58, y + 56, 32, accent)
    elif art == "eu":
        draw_eu_ring(d, x + w - 62, y + 58, 30)
    elif art == "pad":
        draw_pad(d, x + w - 132, y + 34, 108, accent)


def masthead(d):
    title = "THE WORLD IN ONE DAY"
    tf = fnt(SERIF_B, 58)
    d.text(((PAGE - d.textlength(title, font=tf)) / 2, 14), title,
           font=tf, fill=INK)
    d.line([28, 92, 996, 92], fill=INK, width=3)
    d.line([28, 98, 996, 98], fill=INK, width=1)
    date = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    df = fnt(SANS_B, 24)
    d.text(((PAGE - d.textlength(date, font=df)) / 2, 110), date,
           font=df, fill=RED)
    tag = "FIVE STORIES  •  ONE DAY  •  EVERYTHING THAT MATTERED"
    tg = fnt(SANS, 15)
    d.text(((PAGE - d.textlength(tag, font=tg)) / 2, 140), tag,
           font=tg, fill=FAINT)


def lead_story(d):
    x, y, w, h = 28, 168, 968, 272
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 9], fill=NAVY)
    tx, ty = x + 24, y + 24
    ty = flag(d, tx, ty, "WASHINGTON  —  IRAN", RED)
    hf = fnt(SERIF_B, 44)
    ty = blurb(d, wrap_text(d, "TRUMP PUTS IRAN CALL OFF TO 2027",
                            hf, 580), tx, ty, hf, INK, 50) + 8
    bf = fnt(SANS, 21)
    body = ("\u201cI\u2019m not rushing into any decision,\u201d the president "
            "tells Axios and Reuters. \u201cWe\u2019ll see what happens after "
            "the beginning of the year.\u201d The Senate votes 51\u201348 "
            "against curbing his war powers.")
    blurb(d, wrap_text(d, body, bf, 580), tx, ty, bf, BODY, 27)
    draw_calendar(d, x + 648, y + 44, 262, 208)


def space_card(d, x, y, w, h, rng):
    """Dark navy panel: Voyager 1, one light-day out, drawn on stars."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 9], fill=STAR)
    tx, ty = x + 20, y + 22
    ty = flag(d, tx, ty, "SPACE", STAR)
    hf = fnt(SERIF_B, 27)
    ty = blurb(d, wrap_text(d, "VOYAGER 1: ONE LIGHT-DAY OUT", hf, w - 40),
               tx, ty, hf, CARD, 33) + 6
    bf = fnt(SANS, 18)
    body = ("NASA confirms the probe is a full day\u2019s radio signal from "
            "Earth \u2014 even as it stops sending science data. Japan\u2019s "
            "Hayabusa2 switches asteroid target after engine trouble.")
    blurb(d, wrap_text(d, body, bf, w - 40), tx, ty, bf, PALE, 24)
    draw_stars(d, x + w - 150, y + 12, 130, 34, rng)
    draw_probe(d, x + w - 104, y + 52)


def ticker(d):
    y0 = 948
    d.rectangle([28, y0, 996, y0 + 50], fill=INK)
    tick = ("WORLD CHILDREN\u2019S DAY   \u2022   AKVAN LANDFALL TODAY   "
            "\u2022   VOYAGER 1: ONE LIGHT-DAY   \u2022   GTA 6 LAUNCHES")
    size = 19
    while size > 12:
        tf = fnt(SANS_B, size)
        if d.textlength(tick, font=tf) <= 936:
            break
        size -= 1
    d.text(((PAGE - d.textlength(tick, font=tf)) / 2, y0 + 15), tick,
           font=tf, fill=CARD)
    src = ("Stories first reported Friday 20 November 2026  •  Reuters  •  "
           "BBC  •  IMD  •  NASA  •  Sensor Tower (estimate)")
    sf = fnt(SANS, 13)
    d.text(((PAGE - d.textlength(src, font=sf)) / 2, 931), src,
           font=sf, fill=FAINT)


def main():
    rng = random.Random(20261120)
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    masthead(d)
    lead_story(d)

    gy, gh, gw = 456, 228, 476
    gx2 = 28 + gw + 16
    gy2 = gy + gh + 16

    story_card(d, 28, gy, gw, gh, TEAL, "INDIA  —  CYCLONE",
               "AKVAN: 300,000 MOVED TO SAFETY",
               "The severe cyclone strikes near Gopalpur at noon; 423 "
               "rescue teams deployed, 9,300 shelters ready, trains "
               "cancelled across the coast.",
               art="spiral")
    story_card(d, gx2, gy, gw, gh, NAVY, "EUROPE  —  UKRAINE",
               "EUROPE READY TO TALK TO RUSSIA",
               "At a Berlin summit of Kyiv\u2019s allies, leaders say they "
               "will negotiate to end the war \u2014 but only with Ukraine "
               "and Europe at the table.",
               art="eu")
    space_card(d, 28, gy2, gw, gh, rng)
    story_card(d, gx2, gy2, gw, gh, PLUM, "GAMES  —  BUSINESS",
               "GTA 6: $1.84BN*",
               "Sensor Tower counts 19.05m copies by launch day, 19 Nov "
               "\u2014 the biggest launch ever, on paper. Rockstar and "
               "Take-Two confirm no figures. *Estimate, not official.",
               art="pad")

    ticker(d)
    img.save(OUT, optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
