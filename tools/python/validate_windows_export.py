"""Validate packed resources with existing engine tests; boot EXE separately."""
import hashlib
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GODOT = Path("C:/Program Files/Godot_v4.7.2-stable_win64/Godot_v4.7.2-stable_win64_console.exe")
PACKAGE = ROOT / "builds/Windows/MountainCourtyard.pck"
REPORTS = ROOT / "reports/validation"
STAGING = ROOT / "builds/windows_validation"


def main():
    # Each visual iteration keeps its own evidence rather than overwriting old builds.
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-prefix", default="Windows_Packed")
    parser.add_argument("--profile-route", action="store_true")
    args = parser.parse_args()
    STAGING.mkdir(parents=True, exist_ok=True)
    inventory = STAGING / "inventory.gd"
    inventory.write_text('''extends SceneTree
func files_at(path: String) -> Array[String]:
	var result: Array[String] = []
	var directory := DirAccess.open(path)
	for file in directory.get_files():
		result.append(path.path_join(file))
	for folder in directory.get_directories():
		result.append_array(files_at(path.path_join(folder)))
	return result
func _initialize() -> void:
	var files := files_at("res://")
	var forbidden: Array[String] = []
	var missing: Array[String] = []
	if ResourceLoader.exists("res://scripts/environment/courtyard_atmosphere.gd"):
		for required in ["courtyard_earth_v001.gdshader", "courtyard_stone_v001.gdshader", "courtyard_foliage_v001.gdshader", "courtyard_ridge_v001.gdshader", "ENV_CourtyardGarden_v003_game.glb", "ENV_DistantMountains_v004_game.glb"]:
			if not ResourceLoader.exists("res://assets/game/" + required):
				missing.append(required)
	for file in files:
		if file.begins_with("res://handoff/") or file.begins_with("res://reports/") or file.begins_with("res://tests/") or file.begins_with("res://tools/") or file.begins_with("res://assets/source/") or file.contains("CHAR_001_Qinglan_v003") or file.contains("CHAR_001_Qinglan_v004") or file.contains("CHAR_001_Qinglan_v005"):
			forbidden.append(file)
	print("PACKED_INVENTORY: ", JSON.stringify({"files":files,"forbidden":forbidden,"missing":missing}))
	quit(0 if forbidden.is_empty() and missing.is_empty() else 1)
''', encoding="utf-8")
    tasks = [(inventory, args.report_prefix + "_Inventory")]
    sources = [("test_m1_runtime.gd", "M1"), ("test_playthrough.gd", "Route")]
    if args.profile_route:
        sources.insert(0, ("test_courtyard_look.gd", "Look"))
    for name, label in sources:
        script = STAGING / name
        text = (ROOT / "tests" / name).read_text(encoding="utf-8-sig")
        text = text.replace("res://reports/screenshots/", (ROOT / "reports/screenshots").as_posix() + "/" + args.report_prefix + "_")
        script.write_text(text, encoding="utf-8")
        tasks.append((script, args.report_prefix + "_" + label))
    if args.profile_route:
        profile = STAGING / "profile_route.gd"
        text = (ROOT / "tools/godot/profile_courtyard_route.gd").read_text(encoding="utf-8")
        text = text.replace("res://tests/test_playthrough.gd", (STAGING / "test_playthrough.gd").as_posix())
        text = text.replace("res://reports/validation/Courtyard_Look_v001_Route_Profile.json", (REPORTS / (args.report_prefix + "_Moving_Profile.json")).as_posix())
        profile.write_text(text, encoding="utf-8")
        tasks[-1] = (profile, args.report_prefix + "_Route")
    outcomes = []
    for script, label in tasks:
        command = [str(GODOT), "--main-pack", str(PACKAGE), "--script", str(script)]
        if not label.endswith("_Route"):
            command.append("--headless")
        else:
            command.extend(["--", "--capture-name=Victory_2026-10-26"])
        log = REPORTS / (label + "_2026-10-26.log")
        with log.open("w", encoding="utf-8") as stream:
            result = subprocess.run(command, cwd=STAGING, stdout=stream, stderr=subprocess.STDOUT, timeout=240)
        outcomes.append({"task": label, "exit_code": result.returncode, "log": log.name})
        print(label, result.returncode, flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
    report = {"pck_sha256": hashlib.sha256(PACKAGE.read_bytes()).hexdigest(),
              "method": "Editor loads exported PCK; these are not native EXE input tests", "results": outcomes}
    (REPORTS / (args.report_prefix + "_Validation_2026-10-26.json")).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
