#!/usr/bin/env python3
"""news-image-20261118 -- newspaper front page for 18 November 2026.

Draws a 1024x1024 front page for THE WORLD summing up six verified
news stories from Wednesday, 18 November 2026. PIL + Python stdlib only.
No network, no external images, no timestamps: the output is fully
deterministic (same input -> same PNG bytes, every run).
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CONTENT_W = W - 2 * MARGIN

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RULE = (18, 18, 18)
ACCENT = (140, 30, 30)
SKY_TOP = (168, 204, 232)
SKY_MID = (206, 222, 236)
SKY_BOT = (236, 228, 202)
SUN = (232, 164, 48)
BUILDING = (52, 68, 92)
BUILDING2 = (86, 102, 124)
FLAG_RED = (178, 34, 34)
FLAG_BLUE = (30, 64, 140)
FLAG_GREEN = (34, 120, 70)
SEA = (64, 110, 140)

SERIF_BOLD = [
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SERIF_REG = [
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def load_font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center_text(draw, y, text, font, fill=INK):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)


def rule(draw, y, width=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=width)


def text_block(draw, x, y, width, lines, font, fill=INK, align="left"):
    """Draw lines top-aligned; returns the y just below the last line."""
    lh = int(font.size * 1.24)
    for i, line in enumerate(lines):
        if align == "center":
            w = draw.textlength(line, font=font)
            draw.text((x + (width - w) / 2, y + i * lh), line,
                      font=font, fill=fill)
        else:
            draw.text((x, y + i * lh), line, font=font, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- pictograms
# Every pictogram is drawn with plain PIL shapes, centred on (cx, cy),
# and placed BELOW its story deck so it can never cover any text.

def pict_scales(draw, cx, cy, s=1.0):
    """Balance / scales of justice (Britain sanctions)."""
    u = 26 * s
    draw.line([(cx, cy - u), (cx, cy + u)], fill=INK, width=3)
    draw.line([(cx - u, cy - u * 0.72), (cx + u, cy - u * 0.72)],
              fill=INK, width=3)
    draw.ellipse([cx - 4, cy - u - 6, cx + 4, cy - u + 2], fill=ACCENT)
    for sx in (-u, u):
        draw.line([(cx + sx, cy - u * 0.72), (cx + sx, cy - u * 0.18)],
                  fill=INK, width=2)
        draw.polygon([(cx + sx - 15 * s, cy - u * 0.18),
                      (cx + sx + 15 * s, cy - u * 0.18),
                      (cx + sx, cy + u * 0.42)], outline=INK, width=2)
    draw.line([(cx - 16 * s, cy + u), (cx + 16 * s, cy + u)], fill=INK, width=3)


def pict_bars(draw, cx, cy, s=1.0):
    """Rising bar chart (Canada-China trade)."""
    u = 24 * s
    draw.line([(cx - u - 8, cy + u * 0.7), (cx + u + 8, cy + u * 0.7)],
              fill=INK, width=3)
    heights = [0.45, 0.7, 1.0]
    for i, h in enumerate(heights):
        bx = cx - u + i * (u * 0.95)
        top = cy + u * 0.7 - u * 1.15 * h
        colour = FLAG_BLUE if i < 2 else FLAG_GREEN
        draw.rectangle([bx, top, bx + 18 * s, cy + u * 0.7], fill=colour)
    draw.line([(cx - u - 4, cy - u * 0.55), (cx + u + 2, cy - u * 0.85)],
              fill=ACCENT, width=3)


def pict_spiral(draw, cx, cy, s=1.0):
    """Cyclone spiral (Akvan)."""
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps * 3.4 * math.pi
        r = 3 + i / steps * 30 * s
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    draw.line(pts, fill=SEA, width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=ACCENT)


def pict_bat_ball(draw, cx, cy, s=1.0):
    """Cricket bat and ball (Dhoni)."""
    draw.polygon([(cx - 26 * s, cy + 6 * s), (cx + 2 * s, cy - 26 * s),
                  (cx + 12 * s, cy - 16 * s), (cx - 16 * s, cy + 16 * s)],
                 fill=(196, 154, 92), outline=INK)
    draw.line([(cx + 2 * s, cy - 26 * s), (cx + 16 * s, cy - 38 * s)],
              fill=INK, width=4)
    draw.ellipse([cx + 6 * s, cy + 12 * s, cx + 30 * s, cy + 36 * s],
                 fill=FLAG_RED, outline=INK)
    draw.arc([cx + 6 * s, cy + 12 * s, cx + 30 * s, cy + 36 * s],
             start=40, end=320, fill=(255, 255, 255), width=2)


def pict_turbine(draw, cx, cy, s=1.0):
    """Wind turbine with a small sun (Amazon renewables)."""
    u = 26 * s
    draw.ellipse([cx + 18 * s, cy - u - 8, cx + 34 * s, cy - u + 8],
                 fill=SUN)
    for k in range(8):
        a = k * math.pi / 4
        draw.line([(cx + 26 * s + 12 * s * math.cos(a),
                    cy - u + 12 * s * math.sin(a)),
                   (cx + 26 * s + 18 * s * math.cos(a),
                    cy - u + 18 * s * math.sin(a))], fill=SUN, width=2)
    draw.line([(cx - 12 * s, cy + u), (cx - 12 * s, cy - u * 0.55)],
              fill=INK, width=3)
    hub = (cx - 12 * s, cy - u * 0.55)
    for k in range(3):
        a = -math.pi / 2 + k * 2 * math.pi / 3
        tip = (hub[0] + 24 * s * math.cos(a), hub[1] + 24 * s * math.sin(a))
        side = (hub[0] + 6 * s * math.cos(a + 2.6),
                hub[1] + 6 * s * math.sin(a + 2.6))
        draw.polygon([hub, tip, side], fill=FLAG_GREEN, outline=INK)
    draw.ellipse([hub[0] - 4, hub[1] - 4, hub[0] + 4, hub[1] + 4],
                 fill=INK)
    draw.line([(cx - 22 * s, cy + u), (cx - 2 * s, cy + u)], fill=INK, width=3)


def hero_band(draw, x0, y0, x1, y1):
    """Simple skyline, sun and three flags -- PIL shapes only."""
    band_h = y1 - y0
    steps = 24
    for i in range(steps):
        t0 = y0 + band_h * i / steps
        t1 = y0 + band_h * (i + 1) / steps
        f = i / (steps - 1)
        col = tuple(int(SKY_TOP[c] + (SKY_BOT[c] - SKY_TOP[c]) * f)
                    for c in range(3))
        draw.rectangle([x0, t0, x1, t1], fill=col)
    draw.ellipse([x1 - 150, y0 + 14, x1 - 86, y0 + 78], fill=SUN)
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(58, 84, 104))
    towers = [(0.00, 62, 78), (0.09, 44, 96), (0.18, 58, 66),
              (0.30, 40, 108), (0.40, 66, 72), (0.50, 46, 92),
              (0.60, 60, 64), (0.72, 42, 100), (0.82, 56, 70),
              (0.92, 48, 88)]
    bw = (x1 - x0)
    for fx, tw, th in towers:
        bx = x0 + bw * fx
        colour = BUILDING if int(fx * 100) % 2 == 0 else BUILDING2
        draw.rectangle([bx, y1 - 26 - th, bx + tw, y1 - 26], fill=colour)
        for wy in range(y1 - 26 - th + 10, y1 - 34, 18):
            for wx in (bx + 8, bx + tw - 14):
                draw.rectangle([wx, wy, wx + 6, wy + 8],
                               fill=(240, 214, 130))
    for i, colour in enumerate((FLAG_RED, FLAG_BLUE, FLAG_GREEN)):
        px = x0 + 120 + i * 150
        draw.line([(px, y1 - 26 - 52), (px, y1 - 26)], fill=INK, width=3)
        draw.polygon([(px, y1 - 26 - 52), (px + 42, y1 - 26 - 42),
                      (px, y1 - 26 - 32)], fill=colour)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ------------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    masthead = load_font(SERIF_BOLD, 66)
    dateline = load_font(SERIF_REG, 20)
    lead_head = load_font(SERIF_BOLD, 52)
    lead_deck_f = load_font(SERIF_REG, 20)
    head2 = load_font(SERIF_BOLD, 25)
    deck2 = load_font(SERIF_REG, 18)
    head3 = load_font(SERIF_BOLD, 22)
    deck3 = load_font(SERIF_REG, 17)
    footer_f = load_font(SERIF_REG, 17)

    # Masthead + dateline
    center_text(draw, 22, "THE WORLD", masthead)
    rule(draw, 104)
    center_text(draw, 112, "WEDNESDAY, 18 NOVEMBER 2026", dateline)
    rule(draw, 142)

    # Lead story: Quad meets in Manila
    center_text(draw, 152, "QUAD MEETS IN MANILA", lead_head)
    lead_deck = wrap(
        draw,
        "Trump is in Manila for Quad talks, opening a three-day Asia trip "
        "ending in China. APEC meets in Shenzhen 18-19 Nov; Xi, Trump and "
        "Putin meet Thursday 19 Nov.",
        lead_deck_f, CONTENT_W)
    assert len(lead_deck) <= 2, lead_deck
    text_block(draw, MARGIN, 218, CONTENT_W, lead_deck, lead_deck_f,
               align="center")

    # Hero band
    hero_band(draw, MARGIN, 282, W - MARGIN, 418)
    rule(draw, 430)

    # Row 2: two stories, pictogram BELOW each deck
    col2_w = 452
    col2_x = [MARGIN, MARGIN + col2_w + 48]
    row2 = [
        ("BRITAIN SANCTIONS SETTLEMENT FIRMS",
         "Asset freezes on eight firms and Tzav 9, to protect the "
         "two-state solution. - Ed Miliband",
         pict_scales),
        ("CANADA-CHINA EXTEND TRADE DEALS",
         "Xi meets Carney in Shenzhen; China cuts tariffs on C$400m of "
         "Canadian pork and seafood.",
         pict_bars),
    ]
    for x, (headline, deck, pict) in zip(col2_x, row2):
        h_lines = wrap(draw, headline, head2, col2_w)
        assert len(h_lines) <= 2, h_lines
        y = text_block(draw, x, 444, col2_w, h_lines, head2)
        d_lines = wrap(draw, deck, deck2, col2_w)
        assert len(d_lines) <= 2, d_lines
        y = text_block(draw, x, y + 6, col2_w, d_lines, deck2)
        pict(draw, x + col2_w // 2, 600, s=1.0)
    rule(draw, 648)

    # Row 3: three stories, pictogram BELOW each deck
    col3_w = 304
    col3_x = [MARGIN, MARGIN + col3_w + 20, MARGIN + 2 * (col3_w + 20)]
    row3 = [
        ("CYCLONE AKVAN BEARS DOWN",
         "Severe storm in the Bay of Bengal; landfall 20 Nov, gusts "
         "145 km/h.",
         pict_spiral),
        ("DHONI CALLS TIME ON IPL",
         "Five-time champion retires; CSK mentor from 2027. "
         "5,439 IPL runs.",
         pict_bat_ball),
        ("AMAZON BETS $7BN ON GREEN INDIA",
         "$7bn by 2030; four projects add 934 MW, led by a 234 MW "
         "wind farm.",
         pict_turbine),
    ]
    for x, (headline, deck, pict) in zip(col3_x, row3):
        h_lines = wrap(draw, headline, head3, col3_w)
        assert len(h_lines) <= 2, h_lines
        y = text_block(draw, x, 662, col3_w, h_lines, head3)
        d_lines = wrap(draw, deck, deck3, col3_w)
        assert len(d_lines) <= 2, d_lines
        y = text_block(draw, x, y + 6, col3_w, d_lines, deck3)
        pict(draw, x + col3_w // 2, 830, s=1.0)

    # Footer
    rule(draw, 936)
    center_text(draw, 948,
                "WEDNESDAY, 18 NOVEMBER 2026 \u2014 THE DAY IN SIX STORIES",
                footer_f)
    return img


def main():
    img = build()
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
