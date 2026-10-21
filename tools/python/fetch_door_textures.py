"""Download the verified CC0 Fine Grained Wood maps; preserve valid local copies."""
import hashlib
import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[2]
destination = root / "assets/source/third_party/fine_grained_wood"
destination.mkdir(parents=True, exist_ok=True)
# Filenames and hashes verified against the public Poly Haven files API on 2026-10-22.
files = [
    ("Diffuse", "col", "ae1bae182e4b3fb6f97a6014c5dd3667"),
    ("Rough", "rough", "c1b63d1d9092c6bcd524c2ae690cca83"),
    ("nor_gl", "nor_gl", "35c4f86b7fbd91eba54a4d6e88fb16d7"),
]
records = []
for channel, suffix, checksum in files:
    url = "https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/fine_grained_wood/fine_grained_wood_" + suffix + "_1k.png"
    data = {"url": url, "md5": checksum}
    target = destination / data["url"].rsplit("/", 1)[1]
    if target.exists() and hashlib.md5(target.read_bytes()).hexdigest() != data["md5"]:
        raise ValueError("Existing texture differs from source: " + str(target))
    if not target.exists():
        with urllib.request.urlopen(data["url"], timeout=20) as response:
            content = response.read()
        if hashlib.md5(content).hexdigest() != data["md5"]:
            raise ValueError("Downloaded texture checksum differs from metadata")
        target.write_bytes(content)
    records.append({"map": channel, "file": target.name, "url": data["url"], "md5": data["md5"], "license": "CC0", "source": "https://polyhaven.com/a/fine_grained_wood", "author": "Rob Tuytel", "date": "2026-10-22"})
    print("VERIFIED: " + target.name)
(destination / "provenance.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
