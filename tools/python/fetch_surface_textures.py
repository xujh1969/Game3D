"""Offline PBR preparation. Powered by Poly Haven: https://polyhaven.com"""
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HEADER={"User-Agent":"MountainCourtyard/0.1 (github.com/xujh1969/Game3D; local asset preparation)"}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADER),timeout=30) as response:
        return response.read()


def main():
    for asset in ["brown_mud_02","plastered_wall_02"]:
        folder=ROOT/"assets/source/third_party"/asset
        folder.mkdir(parents=True,exist_ok=True)
        for kind in ["info","files"]:
            path=folder/(kind+".json")
            if not path.exists():
                path.write_bytes(fetch(f"https://api.polyhaven.com/{kind}/{asset}"))
        files=json.loads((folder/"files.json").read_text(encoding="utf-8"))
        info=json.loads((folder/"info.json").read_text(encoding="utf-8"))
        records=[]
        for channel in ["Diffuse","Rough","nor_gl"]:
            item=files[channel]["1k"]["png"]
            name=item["url"].rsplit("/",1)[1]
            target=folder/name
            if not target.exists():
                content=fetch(item["url"])
                if hashlib.md5(content).hexdigest()!=item["md5"]:
                    raise ValueError("Downloaded source hash mismatch: "+name)
                target.write_bytes(content)
            if hashlib.md5(target.read_bytes()).hexdigest()!=item["md5"]:
                raise ValueError("Existing source hash mismatch: "+name)
            records.append({"channel":channel,"file":name,"url":item["url"],"md5":item["md5"],"source":"https://polyhaven.com/a/"+asset,"license":"CC0","authors":info.get("authors"),"date":"2026-10-22"})
            print("VERIFIED: "+name,flush=True)
        (folder/"provenance.json").write_text(json.dumps(records,indent=2),encoding="utf-8")


if __name__=="__main__":
    main()
