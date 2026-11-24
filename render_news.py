#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY for Tuesday 24 November 2026.

Draws a one-page newspaper front page (1024x1024) summing up the day's
world news, using only Pillow. Run: python3 render_news.py
Writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (31, 78, 121)
STEEL = (90, 110, 130)
LIGHT = (226, 220, 205)
SEA = (46, 111, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=6):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text):
    f = font(SANS_B, 17)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + 24


def headline(draw, x, y, text, size, width, fill=INK):
    f = font(SERIF_B, size)
    return para(draw, x, y, text, f, width, fill=fill, leading=2)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 178),
                 outline=INK, width=3)
    for bx, by, bw, bh in [(cx - r * 0.62, cy - r * 0.55, 62, 34),
                           (cx + r * 0.05, cy - r * 0.30, 70, 40),
                           (cx - r * 0.45, cy + r * 0.25, 78, 36),
                           (cx + r * 0.28, cy + r * 0.42, 44, 24)]:
        draw.ellipse([bx, by, bx + bw, by + bh], fill=(74, 150, 84))
    draw.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 200, 340,
             fill=(255, 255, 255), width=5)
    draw.arc([cx - r, cy - r * 0.2, cx + r, cy + r * 0.7], 20, 160,
             fill=(255, 255, 255), width=5)
    crack = [(cx - r * 0.15, cy - r), (cx + r * 0.10, cy - r * 0.45),
             (cx - r * 0.12, cy - r * 0.05), (cx + r * 0.14, cy + r * 0.35),
             (cx - r * 0.05, cy + r * 0.75), (cx + r * 0.08, cy + r)]
    draw.line(crack, fill=RED, width=5, joint="curve")


def draw_plane(draw, x, y, s, fill=INK):
    # Side-view jet: fuselage, swept wing, tail fin, motion lines.
    draw.polygon([(x, y + 12 * s), (x + 96 * s, y + 2 * s),
                  (x + 122 * s, y + 9 * s), (x + 118 * s, y + 15 * s),
                  (x + 96 * s, y + 20 * s), (x, y + 22 * s)], fill=fill)
    draw.polygon([(x + 44 * s, y + 14 * s), (x + 66 * s, y + 36 * s),
                  (x + 80 * s, y + 36 * s), (x + 62 * s, y + 14 * s)],
                 fill=fill)
    draw.polygon([(x + 6 * s, y + 12 * s), (x + 16 * s, y - 8 * s),
                  (x + 24 * s, y + 10 * s)], fill=fill)
    for i in range(3):
        draw.line([(x - 10 - i * 18, y + 40 * s),
                   (x + 16 - i * 18, y + 40 * s)], fill=STEEL, width=3)


def draw_ship_blast(draw, x, y, w):
    draw.rectangle([x, y + 62, x + w, y + 92], fill=SEA)
    for i in range(4):
        draw.arc([x + i * 52, y + 66, x + 48 + i * 52, y + 88], 180, 360,
                 fill=(255, 255, 255), width=3)
    draw.polygon([(x + 18, y + 62), (x + 34, y + 62), (x + 30, y + 26),
                  (x + 24, y + 26)], fill=(60, 60, 60))
    draw.polygon([(x + 30, y + 62), (x + w - 18, y + 62),
                  (x + w - 34, y + 34), (x + 52, y + 34)], fill=(40, 40, 40))
    cx, cy = x + w - 52, y + 6
    for ang in range(0, 360, 30):
        import math
        r1 = 30 if ang % 60 == 0 else 16
        ex = cx + r1 * math.cos(math.radians(ang))
        ey = cy + r1 * math.sin(math.radians(ang))
        draw.line([(cx, cy), (ex, ey)], fill=(230, 126, 34), width=6)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(241, 196, 15))


def draw_tanker(draw, x, y, w):
    draw.rectangle([x, y + 58, x + w, y + 92], fill=SEA)
    for i in range(4):
        draw.arc([x + i * 56, y + 62, x + 50 + i * 56, y + 86], 180, 360,
                 fill=(255, 255, 255), width=3)
    draw.polygon([(x + 8, y + 58), (x + w - 8, y + 58),
                  (x + w - 22, y + 30), (x + 22, y + 30)], fill=(120, 40, 40))
    draw.rectangle([x + 30, y + 12, x + 64, y + 30], fill=(200, 200, 200),
                   outline=INK, width=2)
    draw.rectangle([x + 72, y + 12, x + 106, y + 30], fill=(200, 200, 200),
                   outline=INK, width=2)
    draw.rectangle([x + 150, y + 12, x + 184, y + 30], fill=(200, 200, 200),
                   outline=INK, width=2)
    draw.line([(x + 10, y + 44), (x + w - 10, y + 44)], fill=(255, 255, 255), width=2)


def draw_chip(draw, x, y, s):
    draw.rectangle([x, y, x + 92 * s, y + 92 * s], fill=(30, 30, 40),
                   outline=INK, width=3)
    draw.rectangle([x + 22 * s, y + 22 * s, x + 70 * s, y + 70 * s],
                   fill=(70, 130, 180), outline=(255, 255, 255), width=2)
    f = font(SANS_B, int(26 * s))
    draw.text((x + 30 * s, y + 32 * s), "AI", font=f, fill=(255, 255, 255))
    for i in range(4):
        px = x + (16 + i * 20) * s
        draw.line([(px, y - 12 * s), (px, y)], fill=INK, width=3)
        draw.line([(px, y + 92 * s), (px, y + 104 * s)], fill=INK, width=3)
        py = y + (16 + i * 20) * s
        draw.line([(x - 12 * s, py), (x, py)], fill=INK, width=3)
        draw.line([(x + 92 * s, py), (x + 104 * s, py)], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 30
    # Masthead
    rule(d, m, 26, W - m, 3)
    f_title = font(SERIF_B, 76)
    d.text((W // 2, 38), "THE WORLD TODAY", font=f_title, fill=INK,
           anchor="ma")
    f_date = font(SANS_B, 21)
    d.text((W // 2, 140), "TUESDAY, 24 NOVEMBER 2026", font=f_date,
           fill=INK, anchor="ma")
    f_sub = font(SANS, 16)
    d.text((W // 2, 170), "THE DAY'S WORLD NEWS  •  IN ONE PAGE",
           font=f_sub, fill=STEEL, anchor="ma")
    rule(d, m, 196, W - m, 4)
    rule(d, m, 202, W - m, 1)

    # Lead story: COP31 collapse
    y = 218
    y = kicker(d, m, y, "Lead story — Climate")
    y = headline(d, m, y, "COP31 COLLAPSES", 66, 560)
    y = headline(d, m, y, "Climate talks end with no deal",
                 30, 560, fill=BLUE)
    y += 6
    body = ("Negotiations at the COP31 climate summit in Turkey failed "
            "to produce a final agreement, and talks may be suspended "
            "until next year.")
    y = para(d, m, y, body, font(SERIF, 21), 540, leading=5)
    draw_globe(d, 800, 340, 128)
    f_stamp = font(SANS_B, 40)
    d.text((800, 472), "NO DEAL", font=f_stamp, fill=RED, anchor="ma")
    rule(d, m, 520, W - m, 2)

    # Middle row: three stories
    cols = [(m, 306), (m + 326, 306), (m + 652, 306)]
    stories = [
        ("Europe — Security",
         "NATO SENDS EYES TO POLAND",
         "NATO will deploy an AWACS early-warning aircraft to Poland "
         "after three Russian missiles landed there on Friday.",
         "plane"),
        ("Libya — War at Sea",
         "UKRAINE SINKS RUSSIAN WARSHIP",
         "Ukraine said it sank a Russian naval corvette in the port of "
         "Benghazi, Libya, with maritime drones.",
         "ship"),
        ("Gulf — Standoff",
         "IRAN VOWS TO FIGHT US BLOCKADE",
         "Iran said it will use every means to confront a US naval "
         "blockade of the Strait of Hormuz.",
         "tanker"),
    ]
    top = 540
    for (cx, cw), (kick, head, body, art) in zip(cols, stories):
        y = kicker(d, cx, top, kick)
        y = headline(d, cx, y, head, 27, cw)
        y += 4
        if art == "plane":
            draw_plane(d, cx + 60, y + 6, 1.15)
            y += 62
        elif art == "ship":
            draw_ship_blast(d, cx, y, 240)
            y += 100
        else:
            draw_tanker(d, cx, y, 240)
            y += 100
        para(d, cx, y, body, font(SERIF, 17), cw, leading=3)
    rule(d, m, 846, W - m, 2)

    # Bottom row
    y = 866
    y = kicker(d, m, y, "Business — Technology")
    y = headline(d, m, y, "HUANG BACK AT NVIDIA", 26, 430)
    draw_chip(d, 470, 876, 0.72)
    para(d, m, y + 4,
         "President Trump said he struck a deal with Nvidia's board to "
         "reinstate Jensen Huang as chief executive.",
         font(SERIF, 17), 420, leading=3)
    d.line([(560, 866), (560, 994)], fill=LIGHT, width=1)
    y2 = kicker(d, 584, 866, "Also today")
    para(d, 584, y2,
         "Israeli strikes kill at least three in Gaza, including a "
         "worker with the UN relief agency UNRWA.  •  Iran flogs singer "
         "Parastoo Ahmadi with 74 lashes over a concert performed "
         "without a hijab.",
         font(SERIF, 17), 410, leading=4)

    rule(d, m, 1000, W - m, 3)
    d.text((W // 2, 1006), "THE WORLD TODAY  •  Tuesday 24 November 2026",
           font=font(SANS, 13), fill=STEEL, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
