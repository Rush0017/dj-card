"""Generate vCards (CRLF per RFC), QR SVGs and home-screen icons for the DJ cards."""
import segno
from PIL import Image, ImageDraw

BASE = r"C:\Users\mihel\dj-card"

CARDS = {
    "lorenzo": {
        "fn": "Lorenzo Pizzinini",
        "n": "Pizzinini;Lorenzo;;;",
        "email": "lorenzo@datajockey.us",
        "tel": "+393921299670",
        "url": "https://rush0017.github.io/dj-card/",
        "setup_url": "https://rush0017.github.io/dj-card/setup.html",
        "vcf_path": rf"{BASE}\lorenzo.vcf",
        "qr_path": rf"{BASE}\qr-lorenzo.svg",
        "qr_setup_path": rf"{BASE}\qr-setup-lorenzo.svg",
        "icon_path": rf"{BASE}\apple-touch-icon.png",
    },
    "sean": {
        "fn": "Sean Mihelich",
        "n": "Mihelich;Sean;;;",
        "email": "sean@datajockey.us",
        "tel": "+14147503617",
        "url": "https://rush0017.github.io/dj-card/sean/",
        "setup_url": "https://rush0017.github.io/dj-card/sean/setup.html",
        "vcf_path": rf"{BASE}\sean\sean.vcf",
        "qr_path": rf"{BASE}\sean\qr-sean.svg",
        "qr_setup_path": rf"{BASE}\qr-setup-sean.svg",
        "icon_path": rf"{BASE}\sean\apple-touch-icon.png",
    },
}

for key, c in CARDS.items():
    vcard = "\r\n".join([
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{c['n']}",
        f"FN:{c['fn']}",
        "ORG:Data Jockey",
        "TITLE:Co-Founder",
        f"EMAIL;TYPE=INTERNET,WORK:{c['email']}",
        f"TEL;TYPE=CELL,VOICE:{c['tel']}",
        "URL:https://datajockey.us",
        "END:VCARD",
    ]) + "\r\n"
    with open(c["vcf_path"], "wb") as f:
        f.write(vcard.encode("utf-8"))

    qr = segno.make(c["url"], error="q")
    qr.save(c["qr_path"], kind="svg", dark="#171009", light=None,
            border=0, scale=10)

    # QR pointing at the owner's one-time setup page (scanned off a screen)
    qr_setup = segno.make(c["setup_url"], error="q")
    qr_setup.save(c["qr_setup_path"], kind="svg", dark="#171009", light=None,
                  border=0, scale=10)

    # 180x180 home-screen icon: DJ logomark on ink, drawn at 4x then downsampled
    S, F = 180, 4
    img = Image.new("RGB", (S * F, S * F), "#171009")
    d = ImageDraw.Draw(img)
    # logomark authored on a 48u grid; drawn on a 60u grid and re-centred so it
    # sits inside the safe area once iOS rounds the icon corners
    u = S * F / 60.0
    ox, oy = 5.75 * u, 6 * u
    cx, cy, r = 21 * u + ox, 24 * u + oy, 12.5 * u
    d.ellipse([cx - r, cy - r, cx + r, cy + r],
              outline="#d4a853", width=int(2.6 * u))
    r2 = 7 * u
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2],
              outline="#8a6a2a", width=int(1.1 * u))
    d.polygon([(27 * u + ox, 15.5 * u + oy), (40 * u + ox, 24 * u + oy),
               (27 * u + ox, 32.5 * u + oy)], fill="#c4652a")
    img.resize((S, S), Image.LANCZOS).save(c["icon_path"], "PNG")

    print(key, "->", c["vcf_path"], c["qr_path"],
          c["qr_setup_path"], c["icon_path"])
