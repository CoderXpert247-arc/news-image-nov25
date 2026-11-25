"""Generate news.png - a 1024x1024 premium newspaper front page for 25 Nov 2026.

Deterministic: pure PIL drawing from fixed constants, no network, no randomness.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (250, 247, 241)      # #FAF7F1 warm white paper
CHARCOAL = (26, 26, 30)      # #1A1A1E
CRIMSON = (158, 27, 50)      # #9E1B32
FOREST = (31, 92, 74)        # #1F5C4A
GOLD = (200, 149, 43)        # #C8952B
SLATE = (90, 100, 114)       # #5A6472
WHITE = (255, 255, 255)
CARD = (255, 255, 255)

F = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


def lines_for(text, fnt, max_w):
    """Greedy word wrap using exact font metrics."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, fnt, x, y, max_w, lh, fill, max_lines=99):
    lines = lines_for(text, fnt, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def draw_tracked(d, text, fnt, x, y, fill, spacing=2, right=None, center=None):
    """Draw text with letterspacing. Supports left, right-align or center anchor x."""
    widths = [fnt.getlength(c) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    if right is not None:
        x = right - total
    if center is not None:
        x = center - total / 2
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=fnt, fill=fill)
        x += cw + spacing
    return total


def vtext(base, text, fnt, fill, cx, cy):
    """Draw text rotated 90 CCW (reads bottom-to-top), centered at (cx, cy)."""
    tmp = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), text, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4 - bb[0], 4 - bb[1]), text, font=fnt, fill=fill)
    rot = img.rotate(90, expand=True)
    base.paste(rot, (int(cx - rot.width / 2), int(cy - rot.height / 2)), rot)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- Left vertical sidebar (charcoal) ----------------
    d.rectangle([0, 0, 150, H], fill=CHARCOAL)
    d.rectangle([150, 0, 152, H], fill=GOLD)

    f_date_big = font("segoeuib.ttf", 46)
    f_date = font("arialbd.ttf", 20)
    f_tiny = font("arialbd.ttf", 12)

    # Stacked date block at top of sidebar
    d.text((75, 26), "25", font=f_date_big, fill=GOLD, anchor="mm")
    d.text((75, 76), "NOV", font=f_date, fill=WHITE, anchor="mm")
    d.text((75, 102), "2026", font=f_date, fill=WHITE, anchor="mm")
    d.rectangle([40, 124, 110, 126], fill=CRIMSON)
    draw_tracked(d, "WED", f_tiny, 0, 136, GOLD, 2, center=75)

    # Rotated masthead in sidebar (spacing chosen so blocks never overlap)
    f_mast = font("segoeuib.ttf", 34)
    f_mast_sub = font("arialbd.ttf", 15)
    vtext(img, "THE WORLD TODAY", f_mast, WHITE, 75, 395)   # ~240..550
    vtext(img, "GLOBAL EDITION", f_mast_sub, GOLD, 75, 625)  # ~557..693
    vtext(img, "FROM GLOBAL WIRES", f_tiny, SLATE, 75, 775)  # ~720..830

    # Bottom of sidebar
    d.rectangle([40, 858, 110, 860], fill=CRIMSON)
    draw_tracked(d, "FINAL", f_tiny, 0, 874, WHITE, 2, center=75)
    draw_tracked(d, "EDITION", f_tiny, 0, 894, WHITE, 2, center=75)
    d.text((75, 946), "$4", font=font("georgiab.ttf", 30), fill=GOLD, anchor="mm")
    d.text((75, 986), "NO.", font=f_tiny, fill=SLATE, anchor="mm")
    d.text((75, 1006), "329", font=font("arialbd.ttf", 16), fill=WHITE, anchor="mm")

    # ---------------- Main content geometry ----------------
    L, R = 176, 1000
    CW = R - L  # 824

    # Top header line
    f_hdr = font("arialbd.ttf", 13)
    draw_tracked(d, "WEDNESDAY, 25 NOVEMBER 2026", f_hdr, L, 30, CHARCOAL, 2)
    draw_tracked(d, "WORLD EDITION", f_hdr, 0, 30, SLATE, 2, right=R)
    d.rectangle([L, 52, R, 54], fill=CHARCOAL)
    d.rectangle([L, 58, R, 59], fill=GOLD)

    # ---------------- Hero story ----------------
    f_kicker = font("arialbd.ttf", 14)
    f_hero = font("georgiab.ttf", 28)
    f_deck = font("georgia.ttf", 15)
    f_note = font("arialbd.ttf", 11)

    y = 70
    draw_tracked(d, "LEAD STORY / MARKETS", f_kicker, L, y, CRIMSON, 2)
    y += 24
    hero = ("World stocks fall as fresh US tariff threats loom and the AI rally "
            "fizzles; dollar rises ahead of US inflation data that could bring a "
            "Fed rate hike")
    y = draw_wrapped(d, hero, f_hero, L, y, 520, 34, CHARCOAL)
    y += 8
    deck = ("The dollar firmed in New York as traders waited on US inflation data "
            "that could push the Federal Reserve toward a rate hike, while fresh "
            "tariff threats from Washington and a fading AI rally dragged global "
            "indexes lower.")
    y = draw_wrapped(d, deck, f_deck, L, y, 520, 20, SLATE)
    hero_end = y

    # Bar-chart motif (declining global indexes) on the right of hero
    cx0, base_y = 710, 300
    draw_tracked(d, "GLOBAL INDEXES", f_note, cx0, 84, CHARCOAL, 2)
    d.text((R, 84), "25 NOV CLOSE", font=f_note, fill=CRIMSON, anchor="ra")
    d.rectangle([cx0, 104, R, 105], fill=SLATE)

    heights = [168, 150, 138, 120, 104, 92, 74, 58]
    colors = [FOREST, FOREST, FOREST, GOLD, GOLD, GOLD, CRIMSON, CRIMSON]
    bw, gap = 24, 14
    total_bars = len(heights) * bw + (len(heights) - 1) * gap
    bx = cx0 + (R - cx0 - total_bars) / 2
    for hgt, col in zip(heights, colors):
        d.rectangle([bx, base_y - hgt, bx + bw, base_y], fill=col)
        bx += bw + gap
    d.rectangle([cx0, base_y, R, base_y + 2], fill=CHARCOAL)
    # downward trend arrow, tip kept just above the shortest (last) bar
    ax0, ay0, ax1, ay1 = cx0 + 6, 118, 984, 236
    d.line([ax0, ay0, ax1, ay1], fill=CRIMSON, width=3)
    ux, uy = (ax1 - ax0), (ay1 - ay0)
    ulen = (ux * ux + uy * uy) ** 0.5
    ux, uy = ux / ulen, uy / ulen
    bx0, by0 = ax1 - 16 * ux, ay1 - 16 * uy
    px, py = -uy * 7, ux * 7
    d.polygon([(ax1, ay1), (bx0 + px, by0 + py), (bx0 - px, by0 - py)],
              fill=CRIMSON)
    draw_tracked(d, "EQUITIES SLIDE AS TARIFFS BIT", f_note, 0, base_y + 12, SLATE,
                 1, center=(cx0 + R) / 2)

    # Hero divider
    y_div = max(hero_end, 344) + 14
    d.rectangle([L, y_div, R, y_div + 2], fill=CHARCOAL)
    d.rectangle([L, y_div + 7, R, y_div + 8], fill=GOLD)

    # ---------------- 2 x 4 story card grid ----------------
    grid_top = y_div + 20
    grid_bot = 964
    rows, colgap, rowgap = 4, 20, 14
    card_w = (CW - colgap) // 2
    card_h = (grid_bot - grid_top - (rows - 1) * rowgap) // rows

    stories = [
        ("MIDEAST", CRIMSON,
         "Houthi drone strikes Riyadh's PIF Tower for second time in a week; 11 injured",
         "Saudi Arabia's tallest building hit again as regional tensions spike."),
        ("SCIENCE", FOREST,
         "China launches Shenzhou-24 with a Pakistani national aboard - first foreign astronaut",
         "Beijing opens its crewed programme to international partners."),
        ("IRAN", CRIMSON,
         "Iran says it will use \"all means\" to end the US blockade as Trump plays down Strait of Hormuz closure",
         "War of words intensifies over the vital shipping lane."),
        ("EUROPE", FOREST,
         "Germany's Merz warns \"Russia wants more than Ukraine\" - Moscow escalating \"on a massive scale\"",
         "Berlin alerts partners to a broader Russian campaign."),
        ("ISRAEL", GOLD,
         "Judges recommend dropping bribery charges in Netanyahu corruption trial",
         "Panel backs acquittal on two of three counts."),
        ("PACIFIC", GOLD,
         "Solomon Islands bans foreign military bases in new treaty with Australia",
         "Accord curbs China's reach across the Pacific."),
        ("MIGRATION", SLATE,
         "Migrant arrivals in Spain's Canary Islands break single-day record",
         "Rescue boats stream into the archipelago overnight."),
        ("TRAVEL", SLATE,
         "Eurostar cancels London-Paris-Brussels trains over strike",
         "Cross-Channel operators warn of day-long disruption."),
    ]

    f_tag = font("arialbd.ttf", 12)
    f_card_h = font("georgiab.ttf", 17)
    f_dek = font("georgia.ttf", 13)

    for i, (tag, accent, head, dek) in enumerate(stories):
        r, c = divmod(i, 2)
        x = L + c * (card_w + colgap)
        y = grid_top + r * (card_h + rowgap)
        d.rectangle([x, y, x + card_w, y + card_h], fill=CARD,
                    outline=(226, 220, 209), width=1)
        d.rectangle([x, y, x + card_w, y + 4], fill=accent)
        pad = 12
        draw_tracked(d, tag, f_tag, x + pad, y + 12, accent, 2)
        hy = y + 32
        hy = draw_wrapped(d, head, f_card_h, x + pad, hy, card_w - 2 * pad, 21,
                          CHARCOAL, max_lines=4)
        # dek only if it fits
        dek_lines = lines_for(dek, f_dek, card_w - 2 * pad)
        if hy + 4 + len(dek_lines) * 16 <= y + card_h - 6:
            draw_wrapped(d, dek, f_dek, x + pad, hy + 4, card_w - 2 * pad, 16, SLATE)

    # ---------------- Footer strip ----------------
    f_foot = font("arialbd.ttf", 12)
    d.rectangle([L, 976, R, 1008], fill=CRIMSON)
    draw_tracked(d, "THE WORLD TODAY  -  WEDNESDAY 25 NOVEMBER 2026  -  "
                    "COMPILED BY AI FROM GLOBAL WIRES  -  MORE INSIDE",
                 f_foot, 0, 987, WHITE, 1, center=(L + R) / 2)
    d.rectangle([L, 1012, R, 1016], fill=GOLD)

    img.save("news.png", format="PNG", optimize=True)
    print(f"saved news.png {img.size} {img.mode} hero_end={hero_end} "
          f"grid_top={grid_top} card={card_w}x{card_h}")


if __name__ == "__main__":
    main()
