"""Render news.png: The World Brief, Wednesday 25 November 2026.

Deterministic: pure PIL drawing from fixed constants - no network, no clock,
no randomness. Running this file twice produces byte-identical PNG output.
Canvas is exactly 1024x1024 RGB, well under 1 MiB.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# Palette: dark "night edition" broadsheet
INK = (16, 20, 26)          # page background
PANEL = (24, 30, 38)        # card background
PANEL2 = (30, 37, 46)       # alt card background
CREAM = (242, 234, 216)     # primary text
DIM = (168, 176, 186)       # secondary text
FAINT = (110, 120, 132)     # tertiary text
GOLD = (232, 163, 61)       # accent
RED = (224, 82, 74)         # alert / negative
TEAL = (62, 156, 143)       # positive / alt category
BLUE = (74, 118, 196)       # category
LINE = (52, 62, 74)         # hairlines
WHITE = (255, 255, 255)

F = "C:/Windows/Fonts/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

def georgia_b(s): return font("georgiab.ttf", s)
def georgia(s): return font("georgia.ttf", s)
def arial_b(s): return font("arialbd.ttf", s)
def arial(s): return font("arial.ttf", s)
def arial_i(s): return font("ariali.ttf", s)
def impact(s): return font("impact.ttf", s)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def paragraph(draw, xy, text, fnt, fill, max_w, lh, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def chip(draw, x, y, label, bg, fg=WHITE, fnt=None):
    fnt = fnt or arial_b(9)
    tw = draw.textlength(label, font=fnt)
    draw.rounded_rectangle([x, y, x + tw + 14, y + 17], radius=3, fill=bg)
    draw.text((x + 7, y + 3), label, font=fnt, fill=fg)
    return x + tw + 14

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 92], fill=(12, 15, 20))
d.text((24, 16), "THE WORLD BRIEF", font=georgia_b(44), fill=CREAM)
d.text((24, 66), "ONE DAY · THE PLANET'S NEWS, SET IN TYPE", font=arial_b(10), fill=GOLD)
date = "WEDNESDAY 25 NOVEMBER 2026"
dw = d.textlength(date, font=arial_b(15))
d.text((W - 24 - dw, 22), date, font=arial_b(15), fill=CREAM)
sub = "EVERY STORY FIRST REPORTED TODAY  ·  FINAL EDITION  ·  NO. 329"
sw = d.textlength(sub, font=arial(10))
d.text((W - 24 - sw, 46), sub, font=arial(10), fill=DIM)
# flag stripe
stripe = [(RED, 0, 250), (GOLD, 250, 430), (TEAL, 430, 640), (BLUE, 640, 820), (RED, 820, 1024)]
for c, a, b in stripe:
    d.rectangle([a, 92, b, 96], fill=c)

# ---------------------------------------------------------------- stat band
stats = [
    ("20%", "top proposed US tariff\non the EU · China +12", RED),
    ("-6.2%", "Kospi close, worst\nin the AI chip sell-off", RED),
    ("+26%", "UK energy price cap\nfrom 1 January", GOLD),
    ("30+", "killed in a Cairo\ntanker fireball", RED),
    ("9", "dead, 17 trapped in\na Java gold pit", GOLD),
    ("17,500", "taka: Bangladesh's new\ngarment minimum wage", TEAL),
]
d.rectangle([0, 96, W, 176], fill=PANEL)
sx = 24
colw = (W - 48) / 6
for i, (num, lab, col) in enumerate(stats):
    x = sx + i * colw
    if i:
        d.line([(x - 12, 106), (x - 12, 166)], fill=LINE, width=1)
    d.text((x, 104), num, font=georgia_b(30), fill=col)
    for j, ln in enumerate(lab.split("\n")):
        d.text((x, 140 + j * 13), ln, font=arial(10), fill=DIM)

# ---------------------------------------------------------------- heroes
heroes = [
    dict(kick="WASHINGTON · TRADE", kbg=RED,
         head="US proposes tariffs of up to 20% on the EU, China and 12 more",
         dek="China faces the top rate. The EU 'strongly rejects the premise'; Beijing calls the duties a 'false excuse'.",
         why="Two of America's top trade partners face duties"),
    dict(kick="SEOUL · TOKYO · TAIPEI · MARKETS", kbg=RED,
         head="AI doubts sink Asian chip stocks: Kospi closes -6.2%",
         dek="SK Hynix -11.1%, Samsung -9.9%, Taiex -4.8%. The dollar rises before US inflation data that could bring a Fed hike.",
         why="Investors doubt the AI boom will pay off"),
    dict(kick="JIUQUAN, CHINA · SPACE", kbg=BLUE,
         head="Pakistan's first astronaut docks at China's space station",
         dek="Muhammad Zeeshan Ali, 40, the first foreigner to reach Tiangong, flew on Shenzhou-24 for a 5-to-10-day stay.",
         why="China's station takes its first foreign astronaut"),
]
hy = 188
hh = 252
gap = 14
mw = 24
pw = (W - 2 * mw - 2 * gap) / 3
for i, h in enumerate(heroes):
    x = mw + i * (pw + gap)
    d.rounded_rectangle([x, hy, x + pw, hy + hh], radius=6, fill=PANEL, outline=LINE, width=1)
    # illustration well: editorial scenes, no text overlays
    ix0, iy0, ix1, iy1 = x + 1, hy + 1, x + pw - 1, hy + 84
    for k in range(int(iy1 - iy0)):
        t = k / max(int(iy1 - iy0) - 1, 1)
        d.line([(ix0, iy0 + k), (ix1, iy0 + k)], fill=(int(17 - 9 * t), int(21 - 11 * t), int(29 - 15 * t)))
    if i == 0:
        # TRADE WAR: globe, dashed trade arcs stopped by a striped tariff wall
        gx, gy, gr = x + 62, hy + 45, 30
        d.ellipse([gx - gr - 4, gy - gr - 4, gx + gr + 4, gy + gr + 4], outline=(34, 48, 68), width=3)
        gl = Image.new("RGBA", (2 * gr + 6, 2 * gr + 6), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        for hw in (gr, gr * 0.55, gr * 0.16):
            gd.ellipse([3 + gr - hw, 3, 3 + gr + hw, 3 + 2 * gr], outline=(78, 126, 204, 230), width=1)
        for dy in (-gr * 0.5, 0, gr * 0.5):
            half = math.sqrt(max(gr * gr - dy * dy, 1))
            gd.ellipse([3 + gr - half, 3 + gr + dy - half * 0.42, 3 + gr + half, 3 + gr + dy + half * 0.42],
                       outline=(78, 126, 204, 230), width=1)
        for blob in ([(16, 18), (26, 13), (31, 21), (25, 27), (16, 25)],
                     [(36, 24), (48, 20), (54, 30), (46, 40), (38, 34)],
                     [(22, 42), (32, 46), (30, 55), (20, 50)]):
            gd.polygon(blob, fill=(54, 116, 100, 255))
        gd.pieslice([3, 3, 3 + 2 * gr, 3 + 2 * gr], -90, 90, fill=(0, 0, 0, 80))
        img.paste(gl, (int(gx - gr - 3), int(gy - gr - 3)), gl)
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(176, 184, 196), width=2)
        bx0, bx1, wy0, wy1 = x + 188, x + 204, hy + 14, hy + 72
        for (p0, p1, p2, col) in (((gx + gr - 4, gy - 12), (x + 140, hy + 4), (bx0 - 4, hy + 24), GOLD),
                                  ((gx + gr - 4, gy + 12), (x + 140, hy + 82), (bx0 - 4, hy + 62), TEAL)):
            apts = []
            for s in range(41):
                tt = s / 40
                qx = (1 - tt) ** 2 * p0[0] + 2 * (1 - tt) * tt * p1[0] + tt ** 2 * p2[0]
                qy = (1 - tt) ** 2 * p0[1] + 2 * (1 - tt) * tt * p1[1] + tt ** 2 * p2[1]
                apts.append((qx, qy))
            for s in range(0, 40, 2):
                d.line([apts[s], apts[s + 1]], fill=col, width=2)
            d.polygon([p2, (p2[0] - 9, p2[1] - 5), (p2[0] - 9, p2[1] + 5)], fill=col)
        wl = Image.new("RGBA", (int(bx1 - bx0), int(wy1 - wy0)), (0, 0, 0, 0))
        wld = ImageDraw.Draw(wl)
        wld.rectangle([0, 0, int(bx1 - bx0) - 1, int(wy1 - wy0) - 1], fill=(238, 232, 216, 255))
        for s in range(-int(wy1 - wy0), int(bx1 - bx0) + int(wy1 - wy0), 13):
            wld.line([(s, int(wy1 - wy0)), (s + int(wy1 - wy0), 0)], fill=(224, 82, 74, 255), width=6)
        img.paste(wl, (int(bx0), int(wy0)), wl)
        d.rectangle([bx0, wy0, bx1, wy1], outline=(12, 14, 18), width=1)
        for cxx, cyy in ((bx1 + 14, hy + 58), (bx1 + 44, hy + 58), (bx1 + 29, hy + 44)):
            d.rectangle([cxx, cyy, cxx + 26, cyy + 13], fill=(46, 54, 66), outline=(26, 32, 42), width=1)
            for rk in (6, 13, 20):
                d.line([(cxx + rk, cyy + 2), (cxx + rk, cyy + 11)], fill=(34, 41, 53))
        d.line([(x + 6, hy + 79), (x + pw - 6, hy + 79)], fill=(34, 40, 52), width=1)
    elif i == 1:
        # CHIP SELLOFF: a CPU with circuit traces as the market crashes through
        for cx2, up, hgt in ((x + pw - 96, False, 26), (x + pw - 74, True, 18),
                             (x + pw - 52, False, 30), (x + pw - 30, True, 14)):
            col = (74, 44, 46) if not up else (42, 66, 60)
            btm = hy + 74
            top = btm - hgt
            d.line([(cx2, top - 7), (cx2, btm + 7)], fill=col, width=2)
            d.rectangle([cx2 - 5, top, cx2 + 5, btm], fill=col)
        bx0, by0, bx1, by1 = x + 36, hy + 14, x + 128, hy + 70
        for py in range(by0 + 8, by1 - 4, 9):
            d.rectangle([bx0 - 8, py, bx0, py + 4], fill=(162, 170, 182))
            d.rectangle([bx1, py, bx1 + 8, py + 4], fill=(162, 170, 182))
        for py in (by0 + 8, by0 + 26, by0 + 44):
            d.line([(bx0 - 8, py + 2), (bx0 - 22, py + 2)], fill=(70, 118, 176), width=1)
            d.ellipse([bx0 - 30, py - 4, bx0 - 18, py + 8], outline=(70, 118, 176), width=1)
        for py in (by0 + 17, by0 + 35):
            d.line([(bx1 + 8, py + 2), (bx1 + 20, py + 2)], fill=(70, 118, 176), width=1)
            d.ellipse([bx1 + 16, py - 4, bx1 + 28, py + 8], outline=(70, 118, 176), width=1)
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=7, fill=(38, 46, 60), outline=(92, 106, 128), width=2)
        dx0, dy0, dx1, dy1 = x + 54, hy + 26, x + 110, hy + 58
        d.rounded_rectangle([dx0, dy0, dx1, dy1], radius=4, fill=(18, 24, 34), outline=GOLD, width=2)
        for rr in range(2):
            for cc in range(3):
                qx = dx0 + 8 + cc * 16
                qy = dy0 + 6 + rr * 14
                d.rectangle([qx, qy, qx + 8, qy + 8], fill=(200, 152, 64))
        pts1 = [(x + pw - 14, hy + 8), (x + pw - 64, hy + 26), (x + pw - 96, hy + 17), (x + 152, hy + 70)]
        d.line(pts1, fill=RED, width=3, joint="curve")
        tip, prv = pts1[-1], pts1[-2]
        ux, uy = tip[0] - prv[0], tip[1] - prv[1]
        ln = math.sqrt(ux * ux + uy * uy)
        ux, uy = ux / ln, uy / ln
        b1 = (tip[0] - ux * 15 - uy * 8, tip[1] - uy * 15 + ux * 8)
        b2 = (tip[0] - ux * 15 + uy * 8, tip[1] - uy * 15 - ux * 8)
        d.polygon([tip, b1, b2], fill=RED)
    else:
        # TIANGONG: station with solar panels, capsule on a dashed approach, Earth below
        stars = ((14, 10), (44, 8), (78, 18), (96, 6), (110, 54), (128, 6), (166, 46), (190, 10),
                 (210, 50), (240, 14), (272, 8), (300, 26), (30, 56), (90, 60), (200, 60),
                 (288, 56), (18, 40), (196, 30), (174, 16), (60, 64))
        for si, (sxx, syy) in enumerate(stars):
            sc = (232, 238, 248) if si % 3 else (255, 240, 208)
            d.point((x + sxx, hy + syy), fill=sc)
            d.point((x + sxx + 1, hy + syy + 1), fill=(120, 130, 148))
        el = Image.new("RGBA", (int(ix1 - ix0 + 1), int(iy1 - iy0 + 1)), (0, 0, 0, 0))
        ed = ImageDraw.Draw(el)
        ed.ellipse([-401, 63, pw + 398, 499], fill=(15, 36, 68, 255))
        ed.arc([49, 69, 159, 123], 200, 340, fill=(33, 88, 80, 255), width=7)
        ed.ellipse([-385, 75, pw + 382, 499], outline=(44, 96, 140, 255), width=2)
        ed.ellipse([-401, 63, pw + 398, 499], outline=(62, 156, 143, 255), width=2)
        img.paste(el, (int(ix0), int(iy0)), el)
        sx, sy = x + pw / 2 - 10, hy + 30
        d.line([(sx - 74, sy + 13), (sx + 74, sy + 13)], fill=(132, 140, 152), width=2)
        for tk in range(-70, 70, 14):
            d.line([(sx + tk, sy + 8), (sx + tk + 7, sy + 18)], fill=(98, 106, 118), width=1)
        for px0 in (sx - 116, sx + 74):
            d.rectangle([px0, sy + 4, px0 + 42, sy + 22], fill=(40, 80, 152), outline=(80, 128, 204), width=1)
            for gk in (1, 2, 3):
                d.line([(px0 + gk * 10, sy + 4), (px0 + gk * 10, sy + 22)], fill=(30, 62, 124))
            d.line([(px0, sy + 13), (px0 + 42, sy + 13)], fill=(30, 62, 124))
        d.rounded_rectangle([sx - 40, sy - 8, sx + 8, sy + 12], radius=8,
                            fill=(208, 214, 224), outline=(142, 150, 162), width=1)
        d.rectangle([sx - 36, sy + 4, sx + 4, sy + 7], fill=(198, 84, 74))
        d.rounded_rectangle([sx - 8, sy - 24, sx + 10, sy - 4], radius=7,
                            fill=(192, 198, 210), outline=(142, 150, 162), width=1)
        d.ellipse([sx + 6, sy - 6, sx + 24, sy + 12], fill=(178, 184, 196), outline=(132, 140, 152), width=1)
        d.rectangle([sx + 24, sy - 1, sx + 32, sy + 7], fill=(150, 158, 170))
        for wxx in (sx - 32, sx - 20, sx - 8):
            d.ellipse([wxx, sy - 4, wxx + 5, sy + 1], fill=(26, 36, 50))
        t0, t1, t2 = (x + 12, hy + 68), (x + 28, hy + 64), (x + 78, hy + 57)
        cpts = []
        for s in range(41):
            tt = s / 40
            qx = (1 - tt) ** 2 * t0[0] + 2 * (1 - tt) * tt * t1[0] + tt ** 2 * t2[0]
            qy = (1 - tt) ** 2 * t0[1] + 2 * (1 - tt) * tt * t1[1] + tt ** 2 * t2[1]
            cpts.append((qx, qy))
        for s in range(0, 40, 2):
            d.line([cpts[s], cpts[s + 1]], fill=(150, 114, 56), width=2)
        ccx, ccy = x + 92, hy + 56
        d.polygon([(ccx + 5, ccy - 5), (ccx + 14, ccy), (ccx + 5, ccy + 5)], fill=(230, 234, 242))
        d.rounded_rectangle([ccx - 8, ccy - 5, ccx + 6, ccy + 5], radius=3,
                            fill=(214, 218, 228), outline=(150, 156, 168), width=1)
        d.rectangle([ccx - 14, ccy - 3, ccx - 8, ccy + 3], fill=(168, 174, 186))
        d.rectangle([ccx - 4, ccy - 10, ccx + 4, ccy - 6], fill=(40, 80, 152))
        d.rectangle([ccx - 4, ccy + 6, ccx + 4, ccy + 10], fill=(40, 80, 152))
    # text block
    ty = hy + 92
    nx = chip(d, x + 12, ty, h["kick"], h["kbg"])
    ty += 22
    ty = paragraph(d, (x + 12, ty), h["head"], arial_b(15), CREAM, pw - 24, 19, max_lines=3)
    ty += 3
    ty = paragraph(d, (x + 12, ty), h["dek"], arial(10.5), DIM, pw - 24, 13, max_lines=3)
    ty += 4
    d.line([(x + 12, ty + 2), (x + pw - 12, ty + 2)], fill=LINE)
    d.text((x + 12, ty + 8), "WHY IT MATTERS", font=arial_b(9), fill=GOLD)
    ww = d.textlength("WHY IT MATTERS", font=arial_b(9))
    paragraph(d, (x + 12 + ww + 6, ty + 8), h["why"], arial_b(9), CREAM, pw - 30 - ww, 12, max_lines=2)

# ---------------------------------------------------------------- cards
cards = [
    ("WAR · UKRAINE", RED, "Russian strikes kill 5, cut power in 5 regions",
     "Zaporizhzhia nuclear plant runs on diesel after its 17th grid loss this year."),
    ("WAR · SAUDI ARABIA", RED, "Houthi drones strike Riyadh's PIF Tower again",
     "11 injured in the second hit on Saudi Arabia's tallest tower; coalition says it downed 4 drones over Ras Tanura."),
    ("ENERGY · UK", GOLD, "UK energy price cap to rise 26% in January",
     "Ofgem's typical household bill goes from GBP 1,723 to GBP 2,166 a year."),
    ("DIPLOMACY · SOLOMON ISLANDS", BLUE, "Solomon Islands bans foreign military bases",
     "New treaty with Australia makes Canberra a 'primary security partner': AS$740m over 10 years."),
    ("DISASTER · INDONESIA", GOLD, "9 dead, 17 trapped in flooded West Java gold mine",
     "Rescuers pull bodies from the water-filled, 100-metre unlicensed pit."),
    ("WAR · GAZA", RED, "Israeli strike kills Hamas security chief in Gaza",
     "Abu al-Awf, his wife and two daughters die in the Shati camp airstrike."),
    ("JUSTICE · SOUTH AFRICA", TEAL, "Court lifts 'Farmgate' threat to Ramaphosa",
     "Judges void the 2022 report that had opened the road to impeachment."),
    ("JUSTICE · ISRAEL", TEAL, "Judges urge dropping bribery charges in Netanyahu trial",
     "Bribery cases show 'considerable difficulties'; the PM: 'trial must end'."),
    ("DISASTER · EGYPT", RED, "Fuel tanker fire kills at least 30 near Cairo",
     "The tanker overturned and exploded on the ring road; 14 people hospitalised."),
    ("EUROPE · GERMANY", BLUE, "Merz warns 'Russia wants more than Ukraine'",
     "Moscow is escalating 'on a massive scale', the chancellor says."),
]
cy0 = 446
card_h = 132
card_gap = 10
cols = 5
cw = (W - 2 * mw - (cols - 1) * card_gap) / cols
for i, (kick, kbg, head, dek) in enumerate(cards):
    r, c = divmod(i, cols)
    x = mw + c * (cw + card_gap)
    y = cy0 + r * (card_h + card_gap)
    bg = PANEL if (r + c) % 2 == 0 else PANEL2
    d.rounded_rectangle([x, y, x + cw, y + card_h], radius=5, fill=bg, outline=LINE, width=1)
    d.rectangle([x, y, x + 3, y + card_h], fill=kbg)
    ky = y + 9
    # chip may overflow narrow card: shrink font if needed
    kf = arial_b(8)
    while d.textlength(kick, font=kf) > cw - 20 and kf.size > 6:
        kf = arial_b(kf.size - 1)
    chip(d, x + 10, ky, kick, kbg, fnt=kf)
    ky += 22
    ky = paragraph(d, (x + 10, ky), head, arial_b(12), CREAM, cw - 20, 15, max_lines=3)
    ky += 3
    paragraph(d, (x + 10, ky), dek, arial(9.5), DIM, cw - 20, 12, max_lines=4)

# ---------------------------------------------------------------- in brief
by = cy0 + 2 * (card_h + card_gap) + 6
d.text((mw, by), "IN BRIEF", font=arial_b(12), fill=GOLD)
ib = d.textlength("IN BRIEF", font=arial_b(12))
d.text((mw + ib + 10, by + 2), "THE REST OF WEDNESDAY, IN 28 LINES", font=arial(9), fill=FAINT)
d.line([(mw + 320, by + 9), (W - mw, by + 9)], fill=LINE)
by += 18

brief = [
    ("Pyongyang", "North Korea gives the US envoy 48 hours to leave the country."),
    ("Brussels", "EU proposes a EUR 50bn fund for quantum technology."),
    ("Luxembourg", "EU court orders a new cage-free farming timeline for the bloc."),
    ("Kyiv", "Ukraine seeks EUR 11.5bn in aid for 2027 from donors."),
    ("London", "Eurostar cancels London-Paris-Brussels trains over a strike."),
    ("London", "UK firms warned of a new Russian sabotage campaign."),
    ("Mississippi", "Divers recover 8 bodies after a plane crash off the coast."),
    ("Para, Brazil", "Storms kill 6; 17 missing after floods and landslides."),
    ("Harare", "Court issues an arrest warrant for Mugabe's son."),
    ("Caracas", "11 killed as Maduro loyalists attack opposition polling stations."),
    ("Quito", "Ecuador's Correa posts $8m bail and may walk free."),
    ("Canarias, Spain", "Migrant arrivals break a single-day record for the islands."),
    ("Sydney", "Australia's inflation jumps to 4.9% in October."),
    ("Sydney", "Ex-policeman guilty of murdering his wife; Google fined A$26m."),
    ("Tehran", "Iran will use 'all means' to end the US blockade, it says."),
    ("Damazin, Sudan", "RSF drone attacks kill at least 19 in the east."),
    ("Amman", "ICC prosecutor urges a probe into Gaza ceasefire breaches."),
    ("Warsaw", "Poland to set up a no-fly zone at its Ukraine border."),
    ("Gaza", "Winter rains threaten 1,000 shelter sites, councils warn."),
    ("Mexico City", "Mexico protests US refusal to extradite a former TV host."),
    ("Washington", "FCC clears SpaceX to sell 1 million orbital data terminals."),
    ("Washington", "Hackers expose unclassified CIA data; Russia claims US intel."),
    ("Lisbon", "Champions League: Sporting 2-2 Manchester United."),
    ("Bangkok", "Police drop the case behind a YouTube insult complaint."),
    ("Cartagena", "Police free hostages held in a supermarket siege."),
    ("Brasilia", "US also proposes a 10% tariff on Embraer jets."),
    ("United Nations", "16 days of activism against violence toward women begin."),
    ("Space", "ESA's Hera probe struck by debris DART threw off Dimorphos."),
]
bcols = 4
bcw = (W - 2 * mw - (bcols - 1) * 16) / bcols
row_h = 26
for i, (place, line) in enumerate(brief):
    c, r = i % bcols, i // bcols
    x = mw + c * (bcw + 16)
    y = by + r * row_h
    d.ellipse([x, y + 3, x + 14, y + 17], fill=(38, 46, 56))
    n = str(i + 1)
    nw = d.textlength(n, font=arial_b(8))
    d.text((x + 7 - nw / 2, y + 4), n, font=arial_b(8), fill=GOLD)
    pw2 = d.textlength(place + "  ", font=arial_b(9.5))
    d.text((x + 20, y + 2), place, font=arial_b(9.5), fill=TEAL)
    # two-line fill: line 1 shares the row with the place label, line 2 full width
    rest = bcw - 20
    budget1 = rest - pw2
    ws = line.split()
    l1, l2, k = "", "", 0
    while k < len(ws):
        t = (l1 + " " + ws[k]).strip()
        if d.textlength(t, font=arial(9.5)) <= budget1:
            l1, k = t, k + 1
        else:
            break
    while k < len(ws):
        t = (l2 + " " + ws[k]).strip()
        if d.textlength(t, font=arial(9.5)) <= rest:
            l2, k = t, k + 1
        else:
            break
    if k < len(ws):
        l2 = (l2 + " …").strip()
    d.text((x + 20 + pw2, y + 2), l1, font=arial(9.5), fill=CREAM)
    if l2:
        d.text((x + 20, y + 13), l2, font=arial(9.5), fill=CREAM)

# ---------------------------------------------------------------- bottom bar
fy = by + 7 * row_h + 8
d.rectangle([0, fy, W, fy + 44], fill=(12, 15, 20))
d.line([(0, fy), (W, fy)], fill=GOLD, width=2)
d.text((24, fy + 8), "DATE CHECK", font=arial_b(10), fill=RED)
dc = d.textlength("DATE CHECK", font=arial_b(10))
d.text((24 + dc + 8, fy + 8),
       "Every story above happened or was first reported on Wednesday 25 November 2026.",
       font=arial(9.5), fill=CREAM)
d.text((24, fy + 24),
       "Left out as earlier news: Nvidia reinstates Jensen Huang (Tue 24); the Thanksgiving travel storm (Tue 24).",
       font=arial(9.5), fill=DIM)
# legend
lx = W - 24
for label, col in [("CLAIM", RED), ("REPORTED", GOLD), ("OFFICIAL", TEAL)]:
    tw = d.textlength(label, font=arial_b(9))
    d.rectangle([lx - tw - 16, fy + 8, lx, fy + 24], outline=col, width=1)
    d.text((lx - tw - 8, fy + 11), label, font=arial_b(9), fill=col)
    lx -= tw + 26
d.text((lx - 150, fy + 26), "an authority's own account · outlet's reporting · one side's account",
       font=arial(8.5), fill=FAINT)

# ---------------------------------------------------------------- footer
d.rectangle([0, fy + 44, W, H], fill=(10, 12, 16))
d.text((24, fy + 54),
       "Sources: Reuters · AP · AFP · DW · France 24 · CNBC · Al Jazeera · Yonhap · Ofgem · ESA",
       font=arial(9.5), fill=FAINT)
mark = "for make.fun"
mw2 = d.textlength(mark, font=arial_b(10))
d.rectangle([W - 24 - mw2 - 16, fy + 52, W - 24, fy + 72], fill=RED)
d.text((W - 24 - mw2 - 8, fy + 56), mark, font=arial_b(10), fill=WHITE)

img.save("news.png", "PNG", optimize=True)
print("news.png", img.size, img.mode)
