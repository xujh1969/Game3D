"""Structural checks on the exported, self-contained door GLB."""
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets/game/ARCH_003_DoorSong_v003_game.glb"


class DoorAssetTest(unittest.TestCase):
    def test_export_contract(self):
        self.assertTrue(ASSET.is_file(), "Door GLB has not been produced")
        raw = ASSET.read_bytes()
        magic, version, length = struct.unpack_from("<III", raw)
        self.assertEqual((magic, version, length), (0x46546C67, 2, len(raw)))
        chunk_length = struct.unpack_from("<I", raw, 12)[0]
        data = json.loads(raw[20:20 + chunk_length])
        nodes = {node.get("name"): node for node in data["nodes"]}
        for name, x in [("LeafLeft", -1), ("LeafRight", 1)]:
            self.assertIn(name, nodes)
            self.assertAlmostEqual(nodes[name]["translation"][0], x, places=4)
        self.assertIn("DoorFrame", nodes)
        self.assertFalse(data.get("cameras"), "Presentation camera must not be exported")
        self.assertGreaterEqual(len(data.get("images", [])), 3)
        for image in data["images"]:
            self.assertIn("bufferView", image, "GLB textures must be embedded")
        triangles = 0
        for mesh in data["meshes"]:
            for primitive in mesh["primitives"]:
                self.assertIn("NORMAL", primitive["attributes"])
                self.assertIn("TEXCOORD_0", primitive["attributes"])
                triangles += data["accessors"][primitive["indices"]]["count"] // 3
        self.assertLessEqual(triangles, 10000)
        self.assertTrue((ROOT / "assets/source/ARCH_003_DoorSong_v003.blend").is_file())
        print("DOOR_ASSET: triangles=", triangles, "embedded_images=", len(data["images"]))


if __name__ == "__main__":
    unittest.main()
