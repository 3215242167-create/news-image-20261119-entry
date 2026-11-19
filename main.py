"""Draw the front page of THE WORLD TODAY for 19 November 2026.

A single deterministic PIL program: it draws the whole 1024x1024
newspaper front page from code and writes entry.png into the output
directory. No network, no randomness, no clock.
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 46
CONTENT = WIDTH - 2 * MARGIN

INK = (18, 18, 18)
PAPER = (250, 247, 238)
GREY = (90, 88, 80)
RULE = (18, 18, 18)
ACCENT = (140, 30, 25)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_IT = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, leading, color=INK):
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x, y, width, thickness=2):
    draw.rectangle([x, y, x + width, y + thickness], fill=RULE)


def globe(draw, cx, cy, r):
    """A small line-drawn globe: circle, meridians and parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=INK, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=15, end=165, fill=INK, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=195, end=345, fill=INK, width=2)
    draw.arc([cx - r * 0.8, cy - r * 0.9, cx + r * 0.8, cy + r * 0.9],
             start=250, end=290, fill=INK, width=2)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    d = ImageDraw.Draw(img)

    masthead = font(SERIF, 72)
    dateline = font(SANS, 22)
    kicker = font(SANS, 20)
    headline = font(SERIF, 40)
    subhead = font(SERIF, 28)
    body = font(SERIF_REG, 22)
    small = font(SANS_REG, 19)
    small_bold = font(SANS, 19)
    footer = font(SANS_IT, 18)

    y = 24
    # Masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=masthead)
    d.text(((WIDTH - tw) / 2, y), title, font=masthead, fill=INK)
    y += 88
    date_line = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date_line, font=dateline)
    d.text(((WIDTH - dw) / 2, y), date_line, font=dateline, fill=ACCENT)
    y += 30
    rule(d, MARGIN, y, CONTENT, 5)
    y += 11
    rule(d, MARGIN, y, CONTENT, 2)
    y += 14

    # Lead story: trilateral summit, with globe at right
    globe(d, WIDTH - MARGIN - 48, y + 52, 48)
    lead_w = CONTENT - 140
    d.text((MARGIN, y), "SUMMIT  |  APEC", font=kicker, fill=ACCENT)
    y += 24
    y = draw_wrapped(d, MARGIN, y,
                     "Trump, Xi and Putin meet in first-ever three-way summit",
                     headline, lead_w, 44)
    y += 4
    y = draw_wrapped(d, MARGIN, y,
                     "Nuclear arms control tops the agenda as the last "
                     "US-Russia treaty expires in February. Ukraine is "
                     "not on the agenda.",
                     body, lead_w, 27)
    y += 8
    rule(d, MARGIN, y, CONTENT, 2)
    y += 10

    # Two-column middle: Gaza (left) and The Hague (right)
    col_w = (CONTENT - 30) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + 30
    col_top = y

    d.text((left_x, y), "GAZA", font=kicker, fill=ACCENT)
    ly = y + 24
    ly = draw_wrapped(d, left_x, ly,
                      "Israel crosses 'Yellow Line' in first Gaza push since ceasefire",
                      subhead, col_w, 33)
    ly += 2
    ly = draw_wrapped(d, left_x, ly,
                      "Israeli forces cross the line in central Gaza, the "
                      "first major ground operation since the October 2025 "
                      "ceasefire. Hamas calls it a flagrant violation.",
                      body, col_w, 27)

    d.text((right_x, y), "THE HAGUE", font=kicker, fill=ACCENT)
    ry = y + 24
    ry = draw_wrapped(d, right_x, ry,
                      "World court rules on Rohingya genocide case",
                      subhead, col_w, 33)
    ry += 2
    ry = draw_wrapped(d, right_x, ry,
                      "The International Court of Justice rules today on "
                      "Gambia v. Myanmar. A genocide finding would make "
                      "Myanmar the first state liable under the 1948 "
                      "Genocide Convention.",
                      body, col_w, 27)

    y = max(ly, ry) + 8
    rule(d, MARGIN, y, CONTENT, 2)
    y += 10

    # Washington and Culture, side by side
    d.text((left_x, y), "WASHINGTON", font=kicker, fill=ACCENT)
    ly = y + 24
    ly = draw_wrapped(d, left_x, ly,
                      "Jeffries nominated for Speaker, set to be first Black Speaker",
                      subhead, col_w, 33)
    ly += 2
    ly = draw_wrapped(d, left_x, ly,
                      "House Democrats nominate Hakeem Jeffries for Speaker.",
                      body, col_w, 27)

    d.text((right_x, y), "CULTURE", font=kicker, fill=ACCENT)
    ry = y + 24
    ry = draw_wrapped(d, right_x, ry,
                      "GTA VI unlocks after 13-year wait, scores 99",
                      subhead, col_w, 33)
    ry += 2
    ry = draw_wrapped(d, right_x, ry,
                      "After thirteen years, it unlocks worldwide. Early "
                      "reviews: 99 on Metacritic.",
                      body, col_w, 27)

    y = max(ly, ry) + 8
    rule(d, MARGIN, y, CONTENT, 2)
    y += 10

    # Weather strip
    d.text((MARGIN, y), "WEATHER", font=kicker, fill=ACCENT)
    y += 24
    y = draw_wrapped(d, MARGIN, y,
                     "Cyclone Akvan nears landfall between Machilipatnam and "
                     "Puri; Andhra Pradesh and Odisha on high alert.",
                     body, CONTENT, 27)
    y += 8
    rule(d, MARGIN, y, CONTENT, 2)
    y += 10

    # Also today box
    box_top = y
    d.rectangle([MARGIN, box_top, WIDTH - MARGIN, box_top + 104],
                outline=INK, width=2)
    d.text((MARGIN + 16, box_top + 8), "ALSO TODAY",
           font=small_bold, fill=ACCENT)
    items = [
        "Van Gogh painting sells for a record $190.4 million.",
        "NASA's Voyager 1 reaches one light-day from Earth.",
        "Modi meets the Prince and Princess of Wales.",
    ]
    iy = box_top + 32
    for item in items:
        d.text((MARGIN + 16, iy), "\u2022", font=small, fill=INK)
        iy = draw_wrapped(d, MARGIN + 36, iy, item, small,
                          CONTENT - 52, 21)
    y = box_top + 104 + 8

    # Footer
    rule(d, MARGIN, y, CONTENT, 2)
    y += 8
    foot = "The World Today  \u00b7  Thursday, 19 November 2026  \u00b7  One day, in one page."
    fw = d.textlength(foot, font=footer)
    d.text(((WIDTH - fw) / 2, y), foot, font=footer, fill=GREY)

    img.save(os.path.join(out_dir, "entry.png"))
    print("wrote", os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
