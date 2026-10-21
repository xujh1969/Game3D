"""Offline preparation only. Powered by Poly Haven: https://polyhaven.com"""
import hashlib
import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[2]
destination = root / "assets/source/third_party/rock_moss_set_01"
metadata = json.loads((destination / "files.json").read_text(encoding="utf-8"))
entry = metadata["gltf"]["1k"]["gltf"]
files = {"rock_moss_set_01_1k.gltf": entry, **entry["include"]}
records = []
for name, item in files.items():
    target = (destination / name).resolve()
    if not target.is_relative_to(destination.resolve()):
        raise ValueError("Asset file escaped source directory")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        request = urllib.request.Request(item["url"], headers={"User-Agent": "MountainCourtyard/0.1 (github.com/xujh1969/Game3D)"})
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()
        if hashlib.md5(content).hexdigest() != item["md5"]:
            raise ValueError("Source checksum mismatch: " + name)
        target.write_bytes(content)
    if hashlib.md5(target.read_bytes()).hexdigest() != item["md5"]:
        raise ValueError("Existing source checksum mismatch: " + name)
    records.append({"file": name, "url": item["url"], "md5": item["md5"], "license": "CC0", "author": "Kless Gyzen", "source": "https://polyhaven.com/a/rock_moss_set_01", "date": "2026-10-22"})
    print("VERIFIED: " + name)
(destination / "provenance.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
