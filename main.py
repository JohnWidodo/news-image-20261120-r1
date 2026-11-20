#!/usr/bin/env python3
"""news-image-20261120 r1 — front page padat: hero GTA VI + 6 kartu + ticker.

Self-build (tanpa driver Codex). Programatis murni dengan PIL; deterministik:
tanpa random, tanpa waktu, tanpa network. Menulis SATU gambar ke
$MAKEFUN_OUTPUT_DIR/entry.png (atau /output/entry.png).
Judul entry: "Friday 20 November 2026 — The World in One Day".
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 244, 236)
INK = (20, 20, 20)
RED = (166, 30, 30)
AMBER = (232, 163, 61)
DARK = (13, 46, 46)
LIGHT = (235, 230, 218)
GREY = (110, 105, 95)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
BORDER = (200, 194, 182)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, f, width):
    """Bungkus teks ke baris-baris yang muat dalam `width` piksel."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textbbox((0, 0), t, font=f)[2] <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_hero(d, x0, y0, x1, y1):
    """Skyline Vice City neon — empat tone + urutan pelukis (belakang ke depan)."""
    w, h = x1 - x0, y1 - y0
    # Langit: 6 pita gradien ungu -> magenta -> oranye (horizon).
    sky = [(43, 16, 66), (74, 22, 92), (122, 32, 110), (178, 44, 104),
           (224, 84, 84), (245, 150, 92)]
    for i, c in enumerate(sky):
        d.rectangle([x0, y0 + i * h // 6, x1, y0 + (i + 1) * h // 6 + 1], fill=c)
    # Matahari.
    cx, cy, r = x0 + int(w * 0.68), y0 + int(h * 0.42), 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 130))
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], outline=(255, 214, 130), width=2)
    # Skyline belakang (ungu gelap).
    back = [(0.00, 0.30, 0.52), (0.06, 0.18, 0.60), (0.13, 0.38, 0.55),
            (0.22, 0.24, 0.62), (0.30, 0.42, 0.50), (0.38, 0.28, 0.58),
            (0.47, 0.34, 0.56), (0.55, 0.22, 0.62), (0.62, 0.40, 0.54),
            (0.70, 0.26, 0.60), (0.78, 0.36, 0.56), (0.86, 0.24, 0.62),
            (0.93, 0.32, 0.58)]
    base = y0 + int(h * 0.78)
    for fx, fw, fh in back:
        bx = x0 + int(fx * w)
        bw = int(fw * w)
        d.rectangle([bx, base - int(fh * h * 0.55), bx + bw, base], fill=(58, 24, 78))
    # Menara runcing.
    for fx, fh in [(0.17, 0.72), (0.83, 0.68)]:
        tx = x0 + int(fx * w)
        d.polygon([(tx - 16, base), (tx, base - int(fh * h * 0.55)), (tx + 16, base)],
                  fill=(58, 24, 78))
    # Skyline depan (hampir hitam) + jendela cyan/pink.
    front = [(0.00, 0.16, 0.34), (0.10, 0.12, 0.42), (0.20, 0.20, 0.30),
             (0.34, 0.14, 0.46), (0.46, 0.18, 0.36), (0.58, 0.12, 0.44),
             (0.68, 0.20, 0.32), (0.82, 0.14, 0.42), (0.92, 0.08, 0.36)]
    for i, (fx, fw, fh) in enumerate(front):
        bx = x0 + int(fx * w)
        bw = int(fw * w)
        top = base - int(fh * h * 0.42)
        d.rectangle([bx, top, bx + bw, base], fill=(24, 10, 34))
        for wy in range(top + 10, base - 8, 16):
            for wx in range(bx + 8, bx + bw - 6, 18):
                if (wx + wy + i * 7) % 3 == 0:
                    d.rectangle([wx, wy, wx + 5, wy + 7],
                                fill=(0, 229, 255) if (wx // 18) % 2 else (255, 92, 168))
    # Jalan basah + refleksi neon (streak tipis, bukan balok).
    d.rectangle([x0, base, x1, y1], fill=(16, 8, 26))
    for i, c in enumerate([(255, 92, 168), (0, 229, 255), (255, 214, 130)]):
        rx = x0 + int(w * (0.20 + 0.30 * i))
        d.rectangle([rx, base + 6, rx + 5, y1 - 8], fill=c)
    # Palem kiri-kanan: batang + kipas frond menjuntai (pendek, di dalam hero).
    for px, flip in [(x0 + 30, 1), (x1 - 30, -1)]:
        tx, ty = px + flip * 12, y0 + int(h * 0.50)
        d.line([(px, base), (tx, ty)], fill=(30, 16, 40), width=6)
        for k in range(5):
            ex = tx + flip * int(30 - abs(k - 2) * 8)
            ey = ty + 12 + k * 7
            d.line([(tx, ty), (ex, ey)], fill=(24, 90, 60), width=4)
    # Mobil sport siluet magenta + kaca + lampu.
    mx, my = x0 + int(w * 0.44), y1 - 30
    d.polygon([(mx - 78, my), (mx - 58, my - 18), (mx - 20, my - 26),
               (mx + 34, my - 24), (mx + 76, my - 8), (mx + 78, my)],
              fill=(214, 38, 120))
    d.polygon([(mx - 46, my - 16), (mx - 16, my - 21), (mx + 22, my - 20),
               (mx + 40, my - 10)], fill=(120, 220, 235))
    d.ellipse([mx - 52, my - 4, mx - 30, my + 16], fill=(12, 8, 20))
    d.ellipse([mx + 34, my - 4, mx + 56, my + 16], fill=(12, 8, 20))
    d.ellipse([mx + 70, my - 10, mx + 82, my + 0], fill=(255, 240, 160))


def draw_bar_chart(d, x0, y0, x1, y1):
    """Mini bar chart: GTA V day-1 $0.8bn (2013) vs GTA VI ~$2.36bn (est.).
    Label di kiri bar, nilai di kanan bar — tidak ada teks yang keluar strip."""
    d.text((x0, y0), "DAY-1 SALES, $BN", font=font(SANS_B, 11), fill=AMBER)
    labels = [("GTA V 2013", 0.8, (150, 150, 150)), ("GTA VI 2026*", 2.36, AMBER)]
    lab_w = 96
    for i, (lab, val, col) in enumerate(labels):
        yy = y0 + 20 + i * 26
        d.text((x0, yy + 1), lab, font=font(SANS_B, 11), fill=LIGHT)
        bar_x = x0 + lab_w
        bar_w = int(130 * val / 2.5)
        d.rectangle([bar_x, yy, bar_x + bar_w, yy + 15], fill=col)
        d.text((bar_x + bar_w + 5, yy + 1), f"${val}bn", font=font(SANS_B, 12), fill=WHITE)


CARDS = [
    ("CYCLONE  •  INDIA", "Akvan slams India's east coast",
     "Landfall near Gopalpur at noon; 300,000+ evacuated, 423 rescue teams out, "
     "69 trains cancelled. Winds 90–100 km/h, gusts to 110."),
    ("SHENZHEN  •  DIPLOMACY", "Three powers sign peace declaration",
     "Trump, Xi and Putin pledge 'a nuclear war cannot be won and must never be "
     "fought'. The text says nothing on Ukraine or Iran."),
    ("CRICKET  •  WELLINGTON", "Phillips 118 makes history",
     "First player with centuries in all three formats against India in one "
     "calendar year. New Zealand 317/6 at lunch, day two; Nicholls 146*."),
    ("BRUSSELS  •  EUROPE", "EU summons Russian envoy",
     "After Kyiv strikes damage the Austrian and Dutch embassies. No staff hurt; "
     "windows shattered, cars wrecked, cathedral hit."),
    ("THE HAGUE  •  JUSTICE", "World reacts to ICJ genocide ruling",
     "A day after the court found Myanmar responsible over the Rohingya, leaders "
     "welcome the verdict and press for reparations."),
    ("WASHINGTON  •  USA", "Trump to brief press at noon",
     "News conference in Washington on Friday, capping a three-day Asia swing "
     "that ended with the Shenzhen declaration."),
]


def draw_card(d, x0, y0, x1, y1, kicker, headline, deck):
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=1)
    d.rectangle([x0, y0, x0 + 5, y1], fill=RED)
    d.text((x0 + 16, y0 + 12), kicker, font=font(SANS_B, 13), fill=RED)
    lines = wrap(d, headline, font(SERIF_B, 21), (x1 - x0) - 32)
    yy = y0 + 34
    for ln in lines[:2]:
        d.text((x0 + 16, yy), ln, font=font(SERIF_B, 21), fill=INK)
        yy += 25
    dlines = wrap(d, deck, font(SANS, 14), (x1 - x0) - 32)
    for ln in dlines[:3]:
        d.text((x0 + 16, yy + 4), ln, font=font(SANS, 14), fill=(60, 58, 52))
        yy += 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Garis merah atas.
    d.rectangle([0, 0, W, 8], fill=RED)
    # Masthead.
    d.text((24, 18), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52), fill=INK)
    d.text((24, 76), "FRIDAY  20  NOVEMBER  2026", font=font(SANS_B, 17), fill=RED)
    d.text((700, 78), "7 STORIES  •  ONE PAGE", font=font(SANS_B, 15), fill=GREY)
    d.line([(24, 104), (1000, 104)], fill=INK, width=2)
    # Ticker merah (ukuran huruf menyesuaikan sampai muat 976px).
    d.rectangle([0, 110, W, 138], fill=RED)
    ticker = ("AKVAN LANDFALL AT NOON   •   GTA VI $2.36BN IN A DAY   •   "
              "SHENZHEN PEACE PACT   •   PHILLIPS 118   •   EU SUMMONS ENVOY")
    tsize = 15
    while tsize > 10 and d.textbbox((0, 0), ticker, font=font(SANS_B, tsize))[2] > 976:
        tsize -= 1
    d.text((24, 118), ticker, font=font(SANS_B, tsize), fill=WHITE)
    # Hero.
    draw_hero(d, 24, 146, 1000, 352)
    # Strip headline gelap.
    d.rectangle([24, 360, 1000, 452], fill=DARK)
    d.text((40, 370), "GAMES  •  GLOBAL", font=font(SANS_B, 15), fill=AMBER)
    d.text((40, 388), "VICE CITY'S $2.36BN DAY", font=font(SERIF_B, 36), fill=WHITE)
    d.text((40, 430), "GTA VI sales pass $2bn in under 24 hours — Sensor Tower estimate.",
           font=font(SANS, 14), fill=LIGHT)
    draw_bar_chart(d, 700, 370, 984, 440)
    # Grid kartu 2 x 3.
    gx0, gy0, gx1 = 24, 464, 1000
    cw = (gx1 - gx0 - 12) // 2
    ch = 160
    for i, (kick, head, deck) in enumerate(CARDS):
        cx = gx0 + (i % 2) * (cw + 12)
        cy = gy0 + (i // 2) * (ch + 12)
        draw_card(d, cx, cy, cx + cw, cy + ch, kick, head, deck)
    # Footer.
    fy = 972
    d.line([(24, fy), (1000, fy)], fill=INK, width=2)
    d.text((24, fy + 10),
           "Sources: Sensor Tower via Deadline; India Meteorological Dept; AP/Reuters; ICC. "
           "Figures as reported 20 Nov 2026.",
           font=font(SANS, 11), fill=GREY)
    d.text((24, fy + 28), "FRIDAY 20 NOVEMBER 2026  •  THE WORLD IN ONE DAY",
           font=font(SANS_B, 12), fill=INK)
    d.text((820, fy + 28), "*estimate", font=font(SANS, 11), fill=GREY)
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "JPEG", quality=91)


if __name__ == "__main__":
    main()
