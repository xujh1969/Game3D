# Independent review / courtyard look v001

Read-only review by courtyard_review under requesting-code-review. No remaining Critical or Important findings after fixes. No reviewer GPU execution or file mutations.

- New GLB indices valid, positions/normals finite, normals unit length, no external buffer/image dependencies.
- Minor pebble seam found in v002: ring perturbation was not periodic and pole height changed with azimuth. Source corrected and v003 retained separately; sampled pebble has42 triangles,0 open edges,0 nonmanifold edges. v001/v002 preserved.
- Added headless rejection to moving GPU profiler and verified expected exit1; source assumptions cannot be reported as measured GPU FPS.
- Actual primary PCK checks discovered missing preload dependencies. The earlier source-only inference that preload guarantees selected-scene export was too strong. Export now explicitly includes4 shaders and2 new GLBs with resources mode. Reviewer inspected actual189-file inventory with missing=[]/forbidden=[] and18 Look checks passing; final build repeated these checks.
- Six outer bamboo root centers outside the30m playable boundary. One canopy can overhang the wall by about.56m at1.79–4.30m height; no new trunk collider crosses the route. Natural canopy overhang retained.
- No baked GI claim: existing architecture lacks UV2. Preserve startup and moving long-frame evidence; average FPS is not stability acceptance.
