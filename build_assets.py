"""Generate vCards (CRLF per RFC) and QR SVGs for the DJ digital cards."""
import segno

BASE = r"C:\Users\mihel\dj-card"

CARDS = {
    "lorenzo": {
        "fn": "Lorenzo Pizzinini",
        "n": "Pizzinini;Lorenzo;;;",
        "email": "lorenzo@datajockey.us",
        "url": "https://rush0017.github.io/dj-card/",
        "vcf_path": rf"{BASE}\lorenzo.vcf",
        "qr_path": rf"{BASE}\qr-lorenzo.svg",
    },
    "sean": {
        "fn": "Sean Mihelich",
        "n": "Mihelich;Sean;;;",
        "email": "sean@datajockey.us",
        "url": "https://rush0017.github.io/dj-card/sean/",
        "vcf_path": rf"{BASE}\sean\sean.vcf",
        "qr_path": rf"{BASE}\sean\qr-sean.svg",
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
        "URL:https://datajockey.us",
        "END:VCARD",
    ]) + "\r\n"
    with open(c["vcf_path"], "wb") as f:
        f.write(vcard.encode("utf-8"))

    qr = segno.make(c["url"], error="q")
    qr.save(c["qr_path"], kind="svg", dark="#171009", light=None,
            border=0, scale=10)
    print(key, "->", c["vcf_path"], c["qr_path"])
