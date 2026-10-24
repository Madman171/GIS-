# Spirit Pix V2 — Lux3D preview

This directory contains the standalone, local approval preview for the AI pet
redesign. The approved Lux3D image-to-3D task was imported into Blender 5.2.3
and rendered locally. It is not wired into the production frontend and is not
part of a deployment.

Files:

- `lux3d_spirit_pix_v2.glb` — Lux3D-generated GLB (task `4342477`).
- `lux3d_spirit_pix_v2-blender.blend` — Blender 5.2.3 scene after GLB import.
- `lux3d_spirit_pix_v2-render.png` — local Blender approval render.
- `preview.html` — self-contained offline Lux3D viewer.
- `lux3d_spirit_pix_v2-refined.glb` — local refinement pass with a rounder face,
  smile, eye catchlights, and finger-pad details.
- `lux3d_spirit_pix_v2-refined-blender.blend` — Blender scene for the refined
  asset.
- `lux3d_spirit_pix_v2-refined-render.png` — refined approval render.
- `preview-refined.html` — offline viewer for the refined asset.
- `lux3d-refined-delivery.json` — refined asset validation manifest.
- `lux3d-delivery.json` — secret-free artifact manifest and SHA-256 digest.
- `lux3d-attempt.json` — local generation record (no API key).
- `spirit_pix_v2.blend` / `spirit_pix_v2.glb` — earlier procedural fallback,
  retained for comparison only.
- `validation-report.md` — export, import, and visual checks.

The model follows the supplied reference plate: large layered blue bob, peach
face, navy eyes with blue highlights, pointed ears, powder-blue romper, short
limbs, chunky blue boots, four translucent wings, and small aqua motes.
