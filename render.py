#!/usr/bin/env python3
"""Render the front page for Friday 20 November 2026.

Draws a 1024x1024 newspaper front page with PIL, using only the fonts
installed on this machine. Deterministic: fixed seed, no network, no clock.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 32, 44)
NAVY = (20, 49, 92)
TEAL = (14, 92, 102)
GOLD = (176, 124, 22)
PURPLE = (74, 32, 96)
WHITE = (255, 255, 255)
GREY = (90, 90, 86)
LIGHT = (238, 232, 220)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    fnt = font(SANS_B, 19)
    draw.text((x, y), text, font=fnt, fill=color)
    return y + 26


def cyclone_icon(draw, cx, cy, r, color):
    """Spiral of arcs for the cyclone panel."""
    for i in range(7):
        a0 = i * 52
        a1 = a0 + 230
        rr = r * (1 - i * 0.11)
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1,
                 fill=color, width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)


def quote_icon(draw, x, y, color):
    fnt = font(SERIF, 120)
    draw.text((x, y), "\u201c", font=fnt, fill=color)


def space_icon(draw, x, y, w, h, rng):
    for _ in range(46):
        sx = x + rng.randint(0, w)
        sy = y + rng.randint(0, h)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    # dashed trajectory
    for i in range(0, w - 40, 14):
        draw.line([x + 10 + i, y + h - 18 - i // 3,
                   x + 10 + i + 8, y + h - 18 - (i + 8) // 3],
                  fill=(255, 214, 90), width=3)
    # tiny probe: body + dish
    px, py = x + w - 52, y + 26
    draw.polygon([(px, py), (px + 34, py + 10), (px, py + 22)], fill=(200, 210, 225))
    draw.ellipse([px + 26, py - 4, px + 46, py + 16], outline=(255, 214, 90), width=3)
    draw.line([px + 8, py + 10, px - 16, py + 26], fill=(200, 210, 225), width=3)


def controller_icon(draw, x, y, s, color):
    """Simple game controller silhouette, s = overall width."""
    h = int(s * 0.52)
    draw.rounded_rectangle([x, y, x + s, y + h], radius=int(h * 0.42), fill=color)
    draw.ellipse([x + int(s * 0.16), y + int(h * 0.52), x + int(s * 0.30), y + int(h * 0.82)],
                 fill=PAPER)
    draw.ellipse([x + int(s * 0.70), y + int(h * 0.52), x + int(s * 0.84), y + int(h * 0.82)],
                 fill=PAPER)
    # d-pad
    cx, cy = x + int(s * 0.24), y + int(h * 0.34)
    draw.rectangle([cx - 4, cy - 16, cx + 4, cy + 16], fill=PAPER)
    draw.rectangle([cx - 16, cy - 4, cx + 16, cy + 4], fill=PAPER)
    # buttons
    bx, by = x + int(s * 0.74), y + int(h * 0.30)
    for dx, dy in [(0, -12), (12, 0), (0, 12), (-12, 0)]:
        draw.ellipse([bx + dx - 5, by + dy - 5, bx + dx + 5, by + dy + 5],
                     fill=(255, 214, 90))


def calendar_icon(draw, x, y, w, h):
    """A calendar page turned to January 2027."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE,
                           outline=INK, width=3)
    draw.rounded_rectangle([x, y, x + w, y + 52], radius=10, fill=RED)
    draw.rectangle([x, y + 40, x + w, y + 52], fill=RED)
    fnt = font(SANS_B, 30)
    txt = "JANUARY 2027"
    tw = draw.textlength(txt, font=fnt)
    draw.text((x + (w - tw) / 2, y + 10), txt, font=fnt, fill=WHITE)
    # rings
    for rx in (x + 52, x + w - 52):
        draw.line([rx, y - 12, rx, y + 12], fill=INK, width=6)
    # day grid dots
    for row in range(4):
        for col in range(7):
            dx = x + 34 + col * 34
            dy = y + 78 + row * 34
            draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(180, 180, 172))
    # circle the 1st
    draw.ellipse([x + 16, y + 60, x + 52, y + 96], outline=RED, width=5)
    fnt2 = font(SERIF, 64)
    draw.text((x + 18, y + 108), "2027", font=fnt2, fill=NAVY)


def panel(draw, x, y, w, h, accent, kick, head, body, icon=None):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 9], fill=accent)
    tx = x + 20
    ty = y + 22
    ty = kicker(draw, tx, ty, kick, accent)
    hf = font(SERIF, 27)
    head_w = (w - 170) if icon == "controller" else (w - 40)
    lines = wrap(draw, head, hf, head_w)
    ty = draw_lines(draw, lines, tx, ty, hf, INK, 33) + 4
    bf = font(SANS, 18)
    blines = wrap(draw, body, bf, w - 40)
    draw_lines(draw, blines, tx, ty, bf, (52, 52, 48), 24)
    if icon == "cyclone":
        cyclone_icon(draw, x + w - 62, y + 52, 34, accent)
    elif icon == "quote":
        quote_icon(draw, x + w - 96, y - 6, (216, 222, 232))
    elif icon == "space":
        pass  # space panel paints its own art
    elif icon == "controller":
        controller_icon(draw, x + w - 128, y + 30, 104, accent)


def main():
    rng = random.Random(20261120)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF, 60)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    d.line([28, 96, 996, 96], fill=INK, width=3)
    d.line([28, 102, 996, 102], fill=INK, width=1)

    date = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    df = font(SANS_B, 25)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 114), date, font=df, fill=RED)

    # ---- Lead story: Trump / Iran ----
    lx, ly, lw, lh = 28, 152, 968, 288
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=WHITE, outline=INK, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 9], fill=NAVY)
    tx = lx + 24
    ty = ly + 24
    ty = kicker(d, tx, ty, "WASHINGTON  —  IRAN", RED)
    hf = font(SERIF, 47)
    lines = wrap(d, "TRUMP: NO RUSH ON IRAN", hf, 590)
    ty = draw_lines(d, lines, tx, ty, hf, INK, 54) + 6
    bf = font(SANS, 21)
    sub = ("The president pushes any war decision into 2027, saying he "
           "will \u201csee what happens\u201d after Jan 1 \u2014 no rush, "
           "as Europe and the region wait.")
    blines = wrap(d, sub, bf, 590)
    draw_lines(d, blines, tx, ty, bf, (52, 52, 48), 28)
    calendar_icon(d, lx + 648, ly + 48, 260, 210)

    # ---- 2x2 grid ----
    gy = 456
    gh = 232
    gw = 476
    gx2 = 28 + gw + 16
    gy2 = gy + gh + 16

    panel(d, 28, gy, gw, gh, TEAL, "INDIA  —  CYCLONE",
          "AKVAN: 300,000 EVACUATED",
          "Severe cyclone nears the Odisha coast; 423 rescue teams "
          "deployed and schools shut in eight districts.",
          icon="cyclone")

    panel(d, gx2, gy, gw, gh, NAVY, "EUROPE  —  UKRAINE",
          "EUROPE READY FOR TALKS",
          "Leaders say they are ready to negotiate with Russia to end "
          "the war \u2014 as Russian strikes damage the Austrian and "
          "Dutch embassies in Kyiv.",
          icon="quote")

    # Space panel: dark background variant
    sx, sy = 28, gy2
    d.rectangle([sx, sy, sx + gw, sy + gh], fill=NAVY, outline=INK, width=2)
    d.rectangle([sx, sy, sx + gw, sy + 9], fill=(255, 214, 90))
    tx = sx + 20
    ty = sy + 22
    ty = kicker(d, tx, ty, "SPACE", (255, 214, 90))
    hf = font(SERIF, 27)
    lines = wrap(d, "VOYAGER 1: ONE LIGHT-DAY", hf, gw - 40)
    ty = draw_lines(d, lines, tx, ty, hf, WHITE, 33) + 4
    bf = font(SANS, 18)
    blines = wrap(d, "NASA confirms the probe\u2019s milestone \u2014 a full "
                     "day for a signal to reach it. Japan\u2019s Hayabusa2 "
                     "scraps its asteroid landing after engine trouble.",
                  bf, gw - 40)
    draw_lines(d, blines, tx, ty, bf, (214, 220, 232), 24)
    space_icon(d, sx + gw - 152, sy + 14, 132, 78, rng)

    panel(d, gx2, gy2, gw, gh, PURPLE, "GAMES  —  BUSINESS",
          "GTA 6 PASSES $1.8BN",
          "Sales overtake The Odyssey\u2019s $1.80 billion global run, "
          "days after the game\u2019s record launch.",
          icon="controller")

    # ---- Ticker ----
    ty0 = 944
    d.rectangle([28, ty0, 996, ty0 + 52], fill=INK)
    tick = ("WORLD CHILDREN\u2019S DAY  \u2022  CYCLONE AKVAN LANDFALL  "
            "\u2022  VOYAGER 1: ONE LIGHT-DAY")
    size = 19
    while size > 12:
        tf2 = font(SANS_B, size)
        if d.textlength(tick, font=tf2) <= 940:
            break
        size -= 1
    tw2 = d.textlength(tick, font=tf2)
    d.text(((W - tw2) / 2, ty0 + 15), tick, font=tf2, fill=WHITE)

    img.save(OUT, optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
