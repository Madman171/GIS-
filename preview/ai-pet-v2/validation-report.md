# Spirit Pix V2 validation report

Generated locally with Blender 5.2.3.

## Export checks

- GLB loads successfully through Blender's glTF importer.
- Draco compression is enabled.
- Named animation clips are exported through NLA strips: `Idle`, `Hover`,
  `Wave`, `Think`, `Talk`, and `Happy`.
- The GLB is kept separate from `frontend/public/assets/ai-pet/`, so the
  production website remains unchanged.
- The Blender source opens independently and contains the editable materials,
  meshes, armature, and animation actions.

## Visual checks

- Full character fits inside the preview frame.
- Camera is front-facing and orthographic for a reference-style plate.
- White studio card is used only by the preview renderer; the GLB has no
  baked background.
- Four translucent wing meshes and four decorative aqua motes are present.
