#!/usr/bin/env python3
"""news-image-20261118 — front page of THE WORLD, Wednesday 18 November 2026.

Six verified stories from 18 November 2026, drawn with PIL only.
Deterministic: fixed seed, no network, no timestamps, no external images.
Output: entry.png (1024x1024 RGB) next to this script.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (17, 17, 17)
PAPER = (255, 255, 255)
ACCENT = (139, 0, 0)
SKY_TOP = (38, 84, 124)
SKY_BOT = (122, 168, 205)
SUN = (242, 183, 65)
GREY = (90, 90, 90)
RULE = (17, 17, 17)

random.seed(20261118)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf"
SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FALLBACK_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FALLBACK_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(preferred, fallback, size):
    for path in (preferred, fallback):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def serif_black(size):
    return load_font(SERIF_BLACK, FALLBACK_SERIF, size)


def serif_bold(size):
    return load_font(SERIF_BOLD, FALLBACK_SERIF, size)


def serif_reg(size):
    return load_font(SERIF_REG, FALLBACK_SERIF, size)


def sans(size):
    return load_font(SANS_REG, FALLBACK_SANS, size)


def sans_bold(size):
    return load_font(SANS_BOLD, FALLBACK_SANS, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, font, fill=INK):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size + 4


def draw_wrapped_centered(draw, cx, y, text, font, max_width, leading=None):
    lines = wrap_text(draw, text, font, max_width)
    step = leading if leading is not None else int(font.size * 1.28)
    for line in lines:
        draw_centered(draw, cx, y, line, font)
        y += step
    return y, lines


def draw_wrapped_left(draw, x, y, text, font, max_width, leading=None):
    lines = wrap_text(draw, text, font, max_width)
    step = leading if leading is not None else int(font.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=font, fill=INK)
        y += step
    return y, lines


def hrule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


# ---------------------------------------------------------------- pictograms
def pic_scales(draw, cx, cy, s, color=INK):
    """Balance scales: pole, crossbar, two hanging pans."""
    draw.line([(cx, cy - s), (cx, cy + s)], fill=color, width=3)
    draw.line([(cx - s, cy - s + 6), (cx + s, cy - s + 6)], fill=color, width=3)
    draw.ellipse([cx - 4, cy - s - 2, cx + 4, cy - s + 6], fill=color)
    for sx in (-s, s):
        draw.line([(cx + sx, cy - s + 6), (cx + sx, cy + s - 12)], fill=color, width=2)
        draw.arc([cx + sx - 16, cy + s - 22, cx + sx + 16, cy + s + 2],
                 start=0, end=180, fill=color, width=3)
        draw.line([(cx + sx - 16, cy + s - 10), (cx + sx + 16, cy + s - 10)],
                  fill=color, width=2)


def pic_bars(draw, cx, cy, s, color=INK):
    """Rising bar chart with axes."""
    draw.line([(cx - s, cy + s), (cx + s, cy + s)], fill=color, width=3)
    draw.line([(cx - s, cy - s), (cx - s, cy + s)], fill=color, width=3)
    heights = [0.35, 0.6, 0.9]
    bw = int(s * 0.42)
    for i, frac in enumerate(heights):
        x0 = cx - s + 8 + i * (bw + 8)
        top = cy + s - 4 - int(2 * s * frac)
        draw.rectangle([x0, top, x0 + bw, cy + s - 4], fill=color)


def pic_spiral(draw, cx, cy, s, color=INK):
    """Cyclone spiral: Archimedean spiral plus a calm eye."""
    pts = []
    turns = 2.6
    steps = 120
    for i in range(steps + 1):
        t = turns * 2 * math.pi * i / steps
        r = s * i / steps
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    draw.line(pts, fill=color, width=3, joint="curve")
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=color, width=2)


def pic_bat_ball(draw, cx, cy, s, color=INK):
    """Cricket bat leaning on a ball."""
    bat = [(cx - 16, cy - s + 6), (cx + 2, cy - s + 6), (cx + 12, cy + s - 16),
           (cx - 2, cy + s - 4), (cx - 26, cy + s - 16)]
    draw.polygon(bat, outline=color, width=3)
    draw.line([(cx - 7, cy - s + 6), (cx - 14, cy - s - 8)], fill=color, width=4)
    bx, by = cx + s - 12, cy + s - 12
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=color)
    draw.arc([bx - 12, by - 12, bx + 12, by + 12], start=200, end=340,
             fill=PAPER, width=2)


def pic_turbine_sun(draw, cx, cy, s, color=INK):
    """Wind turbine with a small sun behind it."""
    sx, sy = cx + s - 10, cy - s + 8
    draw.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=SUN)
    for ang in (0, 72, 144, 216, 288):
        a = math.radians(ang)
        draw.line([(sx, sy), (sx + 18 * math.cos(a), sy + 18 * math.sin(a))],
                  fill=SUN, width=2)
    draw.line([(cx - 6, cy + s), (cx - 6, cy - s + 14)], fill=color, width=3)
    hub = (cx - 6, cy - s + 14)
    for deg in (90, 210, 330):
        a = math.radians(deg)
        tip = (hub[0] + 26 * math.cos(a), hub[1] + 26 * math.sin(a))
        side = (hub[0] + 7 * math.cos(a + math.pi / 2),
                hub[1] + 7 * math.sin(a + math.pi / 2))
        draw.polygon([hub, tip, side], fill=color)
    draw.ellipse([hub[0] - 4, hub[1] - 4, hub[0] + 4, hub[1] + 4], fill=color)


# ------------------------------------------------------------------- layout
def draw_hero_band(draw, x0, x1, y0, y1):
    """Skyline, sun and three small flags — PIL shapes only, no text."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY_TOP)
    bands = 12
    for i in range(bands):
        t = i / bands
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        yy = y0 + int((y1 - y0) * i / bands)
        draw.rectangle([x0, yy, x1, yy + int((y1 - y0) / bands) + 1], fill=(r, g, b))
    sun_cx, sun_cy, sun_r = x1 - 110, y0 + 34, 26
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=SUN)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(sun_cx + (sun_r + 4) * math.cos(a), sun_cy + (sun_r + 4) * math.sin(a)),
                   (sun_cx + (sun_r + 14) * math.cos(a), sun_cy + (sun_r + 14) * math.sin(a))],
                  fill=SUN, width=3)
    # Skyline silhouettes along the bottom of the band.
    buildings = [(0, 52, 96), (70, 34, 74), (150, 62, 110), (230, 40, 88),
                 (320, 56, 120), (440, 36, 70), (510, 66, 104), (610, 44, 92),
                 (700, 58, 116), (800, 38, 80), (880, 54, 72)]
    for bx, bw, bh in buildings:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(24, 38, 54))
    # Three small flags on poles above the skyline.
    flag_cols = [(178, 34, 34), (34, 102, 52), (24, 68, 140)]
    for i, col in enumerate(flag_cols):
        px = x0 + 130 + i * 330
        draw.line([(px, y1 - 118), (px, y1 - 62)], fill=(24, 38, 54), width=3)
        draw.rectangle([px, y1 - 118, px + 56, y1 - 96], fill=col)
        draw.rectangle([px, y1 - 96, px + 56, y1 - 88], fill=PAPER)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 36
    cx = W // 2

    # Masthead.
    draw_centered(draw, cx, 22, "THE WORLD", serif_black(86))
    hrule(draw, mx, W - mx, 122, 2)
    draw_centered(draw, cx, 130, "WEDNESDAY, 18 NOVEMBER 2026", sans_bold(19))
    hrule(draw, mx, W - mx, 162, 3)
    hrule(draw, mx, W - mx, 167, 1)

    # Lead story.
    draw_centered(draw, cx, 178, "ASIA SUMMIT WEEK", sans_bold(17), fill=ACCENT)
    draw_centered(draw, cx, 202, "QUAD MEETS IN MANILA", serif_bold(52))
    lead_deck = ("Trump in Manila for Quad talks, first stop of a three-day Asia trip "
                 "ending in China; APEC meets in Shenzhen 18-19 Nov, and Xi, Trump "
                 "and Putin meet on Thursday 19 Nov.")
    _, lead_lines = draw_wrapped_centered(draw, cx, 268, lead_deck, sans(19), 940)
    assert len(lead_lines) <= 2, lead_lines

    # Hero band.
    draw_hero_band(draw, mx, W - mx, 322, 442)
    hrule(draw, mx, W - mx, 460, 2)

    # Row 2: two stories.
    row2_y = 474
    col_w2 = 452
    stories2 = [
        ("UNITED KINGDOM", "BRITAIN SANCTIONS SETTLEMENT FIRMS",
         "Ed Miliband announces asset freezes on eight firms and Tzav 9, "
         "to protect the two-state solution.", pic_scales),
        ("TRADE", "CANADA-CHINA EXTEND TRADE DEALS",
         "Xi meets Carney in Shenzhen; C$400m tariff relief; Canada extends "
         "steel remission two years.", pic_bars),
    ]
    for i, (kicker, headline, deck, pic) in enumerate(stories2):
        x0 = mx + i * (col_w2 + 24)
        ccx = x0 + col_w2 // 2
        draw_centered(draw, ccx, row2_y, kicker, sans_bold(15), fill=ACCENT)
        y = row2_y + 24
        y, hl = draw_wrapped_centered(draw, ccx, y, headline, serif_bold(29),
                                       col_w2, leading=34)
        assert len(hl) <= 2, hl
        y, dl = draw_wrapped_centered(draw, ccx, y + 4, deck, sans(17),
                                       col_w2, leading=21)
        assert len(dl) <= 2, dl
        pic(draw, ccx, 638, 20)
    draw.line([(512, 474), (512, 648)], fill=GREY, width=1)
    hrule(draw, mx, W - mx, 664, 2)

    # Row 3: three stories.
    row3_y = 678
    col_w3 = 296
    stories3 = [
        ("WEATHER", "CYCLONE AKVAN BEARS DOWN",
         "Severe storm in the Bay of Bengal; landfall due 20 Nov, winds "
         "120-130, gusts 145 km/h.", pic_spiral),
        ("CRICKET", "DHONI CALLS TIME ON IPL",
         "Five-time champion, 5,439 IPL runs, retires as a player; CSK "
         "mentor from 2027.", pic_bat_ball),
        ("ENERGY", "AMAZON BETS $7BN ON GREEN INDIA",
         "$7bn in renewables by 2030; four projects, 934 MW, incl. "
         "234 MW Karnataka wind.", pic_turbine_sun),
    ]
    for i, (kicker, headline, deck, pic) in enumerate(stories3):
        x0 = mx + i * (col_w3 + 16)
        ccx = x0 + col_w3 // 2
        draw_centered(draw, ccx, row3_y, kicker, sans_bold(14), fill=ACCENT)
        y = row3_y + 22
        y, hl = draw_wrapped_centered(draw, ccx, y, headline, serif_bold(25),
                                       col_w3, leading=29)
        assert len(hl) <= 2, hl
        y, dl = draw_wrapped_centered(draw, ccx, y + 4, deck, sans(15),
                                       col_w3, leading=19)
        assert len(dl) <= 2, dl
        pic(draw, ccx, 912, 24)
    draw.line([(348, 678), (348, 946)], fill=GREY, width=1)
    draw.line([(676, 678), (676, 946)], fill=GREY, width=1)

    # Footer.
    hrule(draw, mx, W - mx, 960, 2)
    draw_centered(draw, cx, 972, "WEDNESDAY, 18 NOVEMBER 2026 — THE DAY IN SIX STORIES",
                  sans_bold(16))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, img.mode)


if __name__ == "__main__":
    main()
