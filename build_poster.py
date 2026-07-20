"""Generate iOS Contact Poster images for the DJ digital cards.

NameDrop shares name + selected phone/email + the Contact Poster. The poster is
the only part that carries brand design, so this renders a Data Jockey poster
each owner sets under Contacts -> My Card -> Contact Photo & Poster.

iOS overlays the person's name across the TOP of the poster, so the upper band
is deliberately left empty.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\mihel\dj-card"
W, H = 1290, 2796           # iPhone 15/16 Pro portrait
NAME_BAND = 0.30            # top fraction reserved for the iOS name overlay

INK = (13, 9, 4)
GOLD = (212, 168, 83)
GOLD_LT = (240, 220, 174)
ORANGE = (196, 101, 42)
MUTED = (154, 143, 128)

FONT_SERIF = r"C:\Windows\Fonts\georgia.ttf"
FONT_SANS_B = r"C:\Windows\Fonts\arialbd.ttf"

POSTERS = {
    "lorenzo": {"role": "Co-Founder", "out": rf"{BASE}\poster-lorenzo.png"},
    "sean": {"role": "Co-Founder", "out": rf"{BASE}\poster-sean.png"},
}


def background():
    """Ink base with a gold glow behind the mark and a warm bloom low-right."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    img[:] = INK

    def glow(cx, cy, rx, ry, color, strength):
        d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        a = np.clip(1.0 - d, 0, 1) ** 1.7 * strength
        for i in range(3):
            img[:, :, i] += a * color[i]

    glow(W * 0.5, H * 0.44, W * 0.72, H * 0.20, GOLD, 0.15)
    glow(W * 0.92, H * 1.03, W * 0.6, H * 0.20, ORANGE, 0.13)
    glow(W * 0.5, H * -0.05, W * 0.8, H * 0.14, GOLD, 0.07)

    rng = np.random.default_rng(7)
    img += rng.normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def tracked(draw, text, font, cx, y, spacing, fill):
    """Draw letterspaced text centred on cx; returns the height drawn."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing
    return font.getbbox(text)[3]


def logomark(img, cx, cy, size):
    """DJ mark (ring + play triangle), supersampled for clean edges."""
    F = 4
    layer = Image.new("RGBA", (size * F, size * F), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    u = size * F / 48.0
    mx, my, r = 21 * u, 24 * u, 12.5 * u
    d.ellipse([mx - r, my - r, mx + r, my + r],
              outline=GOLD + (255,), width=int(2.6 * u))
    r2 = 7 * u
    d.ellipse([mx - r2, my - r2, mx + r2, my + r2],
              outline=GOLD + (140,), width=max(1, int(1.1 * u)))
    d.ellipse([mx - 2.2 * u, my - 2.2 * u, mx + 2.2 * u, my + 2.2 * u],
              fill=GOLD + (255,))
    d.polygon([(27 * u, 15.5 * u), (40 * u, 24 * u), (27 * u, 32.5 * u)],
              fill=ORANGE + (255,))
    layer = layer.resize((size, size), Image.LANCZOS)
    img.paste(layer, (int(cx - size / 2), int(cy - size / 2)), layer)


for key, cfg in POSTERS.items():
    img = background()
    d = ImageDraw.Draw(img)
    cx = W / 2

    f_kicker = ImageFont.truetype(FONT_SANS_B, 46)
    f_role = ImageFont.truetype(FONT_SERIF, 62)
    f_site = ImageFont.truetype(FONT_SANS_B, 40)

    # mark sits below the reserved name band
    mark_cy = H * NAME_BAND + H * 0.20
    logomark(img, cx, mark_cy, int(W * 0.42))

    y = mark_cy + W * 0.30
    tracked(d, "DATA JOCKEY", f_kicker, cx, y, 20, GOLD)

    y += 150
    d.line([(cx - 150, y), (cx + 150, y)], fill=GOLD + (0,), width=2)
    d.line([(cx - 150, y), (cx + 150, y)], fill=(90, 72, 36), width=2)

    y += 70
    role = cfg["role"]
    d.text((cx - d.textlength(role, font=f_role) / 2, y), role,
           font=f_role, fill=GOLD_LT)

    # footer
    fy = H - 260
    tracked(d, "AI AUTOMATION FOR REAL BUSINESSES", f_site, cx, fy, 8, MUTED)
    fy += 90
    tracked(d, "DATAJOCKEY.US", f_site, cx, fy, 12, GOLD)

    img.save(cfg["out"], "PNG")
    print(key, "->", cfg["out"], img.size)
