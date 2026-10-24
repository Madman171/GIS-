"""Build the Spirit Pix V2 preview model used by the GIS knowledge platform.

This is intentionally procedural so the model can be rebuilt after a Blender
upgrade without relying on an opaque source file.  The target is the supplied
reference: a compact pastel-blue fairy mascot with a large layered bob, huge
navy-blue eyes, short rounded limbs and four translucent wings.  The script
also exports named NLA clips for the web state machine.

Run with:
  blender -b --python tools/build_ai_pet.py -- --output preview/spirit_pix_v2.glb --blend-output preview/spirit_pix_v2.blend
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--blend-output")
    return parser.parse_args(argv)


def set_input(node, name: str, value) -> None:
    socket = node.inputs.get(name)
    if socket is not None:
        socket.default_value = value


def material(name: str, color, *, roughness=0.6, metallic=0.0, alpha=1.0, transmission=0.0, emission=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, alpha)
    nodes = mat.node_tree.nodes
    nodes.clear()
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    output = nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    set_input(shader, "Base Color", (*color, alpha))
    set_input(shader, "Roughness", roughness)
    set_input(shader, "Metallic", metallic)
    set_input(shader, "Alpha", alpha)
    set_input(shader, "Transmission Weight", transmission)
    set_input(shader, "Transmission", transmission)
    if emission:
        set_input(shader, "Emission Color", (*emission, 1.0))
        set_input(shader, "Emission Strength", 0.35)
    if alpha < 1.0:
        # Blender 4/5 renamed blend_method to surface_render_method.
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "DITHERED"
        elif hasattr(mat, "blend_method"):
            mat.blend_method = "BLEND"
        mat.use_screen_refraction = True if hasattr(mat, "use_screen_refraction") else False
    return mat


def assign(obj, mat) -> None:
    obj.data.materials.append(mat)


def smooth(obj) -> None:
    if hasattr(obj.data, "polygons"):
        for poly in obj.data.polygons:
            poly.use_smooth = True


def sphere(name, location, scale, mat, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    smooth(obj)
    return obj


def rounded_cube(name, location, scale, mat, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    modifier = obj.modifiers.new("soft rounded edges", "BEVEL")
    modifier.width = bevel
    modifier.segments = 4
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    assign(obj, mat)
    smooth(obj)
    return obj


def cylinder(name, location, radius, depth, mat, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=20,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    smooth(obj)
    bevel = obj.modifiers.new("soft edges", "BEVEL")
    bevel.width = radius * 0.35
    bevel.segments = 3
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    return obj


def polygon(name, points, depth, mat):
    """Create a thin, bevelled polygon for ears and translucent wings."""
    verts = [(x, -depth / 2, z) for x, z in points]
    verts += [(x, depth / 2, z) for x, z in points]
    n = len(points)
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    for index in range(n):
        nxt = (index + 1) % n
        faces.append((index, nxt, n + nxt, n + index))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    assign(obj, mat)
    bevel = obj.modifiers.new("soft silhouette", "BEVEL")
    bevel.width = min(depth * 0.35, 0.025)
    bevel.segments = 2
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    smooth(obj)
    obj.select_set(False)
    return obj


def smile(name, mat):
    curve = bpy.data.curves.new(name + "Curve", "CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = 0.012
    curve.bevel_resolution = 3
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(2)
    for point, co in zip(spline.bezier_points, [(-0.10, 0, 0.0), (0, 0, -0.045), (0.10, 0, 0.0)]):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = (0, -0.78, 1.18)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    assign(obj, mat)
    obj.select_set(False)
    return obj


def create_bone(edit_bones, name, head, tail, parent=None):
    bone = edit_bones.new(name)
    bone.head = head
    bone.tail = tail
    if parent:
        bone.parent = edit_bones.get(parent)
    return bone


def create_rig():
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    armature = bpy.context.object
    armature.name = "SpiritPetRig"
    armature.data.name = "SpiritPetRig"
    edit_bones = armature.data.edit_bones
    default = edit_bones.get("Bone")
    if default:
        edit_bones.remove(default)
    create_bone(edit_bones, "root", (0, 0, 0), (0, 0, 0.55))
    create_bone(edit_bones, "spine", (0, 0, 0.45), (0, 0, 1.10), "root")
    create_bone(edit_bones, "head", (0, 0, 1.10), (0, 0, 1.75), "spine")
    create_bone(edit_bones, "arm.L", (-0.40, 0, 1.00), (-0.62, 0, 0.56), "spine")
    create_bone(edit_bones, "arm.R", (0.40, 0, 1.00), (0.62, 0, 0.56), "spine")
    create_bone(edit_bones, "leg.L", (-0.18, 0, 0.45), (-0.18, 0, 0.02), "root")
    create_bone(edit_bones, "leg.R", (0.18, 0, 0.45), (0.18, 0, 0.02), "root")
    create_bone(edit_bones, "wing.L", (-0.48, 0.08, 1.05), (-0.95, 0.08, 1.20), "spine")
    create_bone(edit_bones, "wing.R", (0.48, 0.08, 1.05), (0.95, 0.08, 1.20), "spine")
    bpy.ops.object.mode_set(mode="OBJECT")
    return armature


def parent_to_bone(obj, armature, bone_name):
    world = obj.matrix_world.copy()
    obj.parent = armature
    obj.parent_type = "BONE"
    obj.parent_bone = bone_name
    obj.matrix_world = world


def make_action(armature, name, frames, configure):
    action = bpy.data.actions.new(name)
    action.use_fake_user = True
    armature.animation_data_create()
    armature.animation_data.action = action
    configure(armature, frames)
    armature.animation_data.action = None
    track = armature.animation_data.nla_tracks.new()
    track.name = name
    strip = track.strips.new(name, 1, action)
    strip.frame_end = frames
    strip.action_frame_start = 1
    strip.action_frame_end = frames
    strip.extrapolation = "NOTHING"
    return action


def key_pose(armature, bone_name, frame, *, rotation=None, location=None):
    bone = armature.pose.bones[bone_name]
    bone.rotation_mode = "XYZ"
    if rotation is not None:
        bone.rotation_euler = rotation
        bone.keyframe_insert("rotation_euler", frame=frame)
    if location is not None:
        bone.location = location
        bone.keyframe_insert("location", frame=frame)


def create_animations(armature):
    def idle(rig, frames):
        for frame, z, yaw in [(1, 0.00, -0.025), (30, 0.045, 0.025), (60, 0.00, -0.025)]:
            key_pose(rig, "root", frame, location=(0, 0, z))
            key_pose(rig, "head", frame, rotation=(0, yaw, 0))
        for frame, angle in [(1, -0.03), (30, 0.04), (60, -0.03)]:
            key_pose(rig, "wing.L", frame, rotation=(0, angle, -0.04))
            key_pose(rig, "wing.R", frame, rotation=(0, -angle, 0.04))

    def hover(rig, frames):
        for frame, z in [(1, 0.00), (20, 0.08), (40, 0.00)]:
            key_pose(rig, "root", frame, location=(0, 0, z))

    def wave(rig, frames):
        for frame, angle in [(1, 0.0), (12, -0.35), (24, 0.30), (36, -0.25), (48, 0.0)]:
            key_pose(rig, "arm.R", frame, rotation=(angle, 0, -0.18))
            key_pose(rig, "root", frame, location=(0, 0, 0.02 if frame not in (1, 48) else 0.0))

    def think(rig, frames):
        for frame, angle in [(1, 0.0), (20, 0.18), (45, 0.0)]:
            key_pose(rig, "head", frame, rotation=(0.0, 0.0, angle))
            key_pose(rig, "root", frame, location=(0, 0, 0.02 if frame == 20 else 0.0))

    def talk(rig, frames):
        for frame, angle in [(1, 0.0), (8, 0.04), (16, -0.035), (24, 0.0)]:
            key_pose(rig, "head", frame, rotation=(angle, 0.0, 0.0))

    def happy(rig, frames):
        for frame, z, roll in [(1, 0.0, 0.0), (10, 0.10, -0.08), (20, 0.0, 0.08), (30, 0.08, -0.05), (40, 0.0, 0.0)]:
            key_pose(rig, "root", frame, location=(0, 0, z), rotation=(0, 0, roll) if False else None)
            key_pose(rig, "wing.L", frame, rotation=(0, -0.12, -0.12))
            key_pose(rig, "wing.R", frame, rotation=(0, 0.12, 0.12))

    make_action(armature, "Idle", 60, idle)
    make_action(armature, "Hover", 40, hover)
    make_action(armature, "Wave", 48, wave)
    make_action(armature, "Think", 45, think)
    make_action(armature, "Talk", 24, talk)
    make_action(armature, "Happy", 40, happy)


def build(output_path: Path, blend_output: Path | None = None) -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)

    skin = material("peach skin", (1.0, 0.84, 0.78), roughness=0.62, emission=(0.08, 0.025, 0.018))
    ear_inner = material("ear inner pink", (1.0, 0.48, 0.52), roughness=0.72)
    hair = material("periwinkle blue hair", (0.11, 0.34, 0.86), roughness=0.40, emission=(0.02, 0.06, 0.18))
    hair_light = material("soft blue hair highlights", (0.16, 0.42, 0.92), roughness=0.30, emission=(0.015, 0.045, 0.16))
    cloth = material("powder blue romper", (0.34, 0.66, 0.96), roughness=0.70)
    collar = material("collar blue", (0.26, 0.55, 0.90), roughness=0.48)
    boot = material("pale blue boots", (0.24, 0.55, 0.92), roughness=0.42)
    boot_sole = material("white boot soles", (0.92, 0.97, 1.0), roughness=0.28)
    eye_outer = material("deep navy eye", (0.015, 0.045, 0.18), roughness=0.16, emission=(0.01, 0.02, 0.10))
    iris = material("cobalt iris", (0.03, 0.28, 0.86), roughness=0.14, emission=(0.02, 0.10, 0.32))
    iris_glow = material("iris aqua glow", (0.18, 0.65, 1.0), roughness=0.12, emission=(0.10, 0.40, 0.78))
    highlight = material("eye highlight", (1.0, 1.0, 1.0), roughness=0.04, emission=(0.8, 0.9, 1.0))
    blush = material("soft cheek blush", (1.0, 0.34, 0.43), roughness=0.74, alpha=0.68)
    mouth_mat = material("warm smile", (0.70, 0.22, 0.28), roughness=0.58)
    wing = material("milky translucent wings", (0.55, 0.90, 1.0), roughness=0.18, alpha=0.31, transmission=0.30, emission=(0.08, 0.28, 0.56))
    orb_mat = material("magic aqua orbs", (0.25, 0.84, 1.0), roughness=0.08, alpha=0.78, emission=(0.15, 0.62, 1.0))

    objects_by_bone = {"root": [], "spine": [], "head": [], "arm.L": [], "arm.R": [], "leg.L": [], "leg.R": [], "wing.L": [], "wing.R": []}

    # Compact mascot body: one soft oval romper, short limbs, and chunky boots.
    objects_by_bone["spine"].append(sphere("body", (0, 0, 0.76), (0.52, 0.38, 0.64), cloth, segments=32, rings=20))
    objects_by_bone["spine"].append(sphere("neck", (0, -0.01, 1.28), (0.17, 0.15, 0.12), skin))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.045, major_segments=28, minor_segments=10, location=(0, -0.015, 1.31), rotation=(0, 0, 0))
    collar_obj = bpy.context.object
    collar_obj.name = "round collar"
    assign(collar_obj, collar)
    smooth(collar_obj)
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        objects_by_bone[f"arm.{suffix}"].append(sphere(f"arm.{suffix}", (side * 0.50, -0.01, 0.82), (0.12, 0.13, 0.32), skin, segments=20, rings=14))
        objects_by_bone[f"arm.{suffix}"].append(sphere(f"hand.{suffix}", (side * 0.54, -0.02, 0.57), (0.13, 0.13, 0.15), skin, segments=20, rings=14))
        objects_by_bone[f"leg.{suffix}"].append(cylinder(f"leg.{suffix}", (side * 0.18, 0, 0.27), 0.115, 0.40, skin))
        objects_by_bone[f"leg.{suffix}"].append(rounded_cube(f"boot.{suffix}", (side * 0.18, -0.10, -0.02), (0.20, 0.25, 0.15), boot, bevel=0.10))
        objects_by_bone[f"leg.{suffix}"].append(rounded_cube(f"sole.{suffix}", (side * 0.18, -0.13, -0.16), (0.20, 0.25, 0.035), boot_sole, bevel=0.025))

    # Large face and layered blue bob. The overlapping soft lobes match the
    # supplied illustration's silhouette much more closely than a single cap.
    objects_by_bone["head"].append(sphere("head", (0, 0, 1.62), (0.78, 0.62, 0.72), skin, segments=32, rings=22))
    objects_by_bone["head"].append(sphere("hair cap", (0, 0.04, 1.79), (0.86, 0.66, 0.82), hair, segments=32, rings=22))
    back_locks = [(-0.64, 1.56, 0.25, 0.53), (0.64, 1.56, 0.25, 0.53), (-0.70, 1.30, 0.20, 0.38), (0.70, 1.30, 0.20, 0.38)]
    for index, (x, z, sx, sz) in enumerate(back_locks):
        lock = sphere(f"back hair lock.{index}", (x, 0.04, z), (sx, 0.56, sz), hair_light if index in (2, 3) else hair, segments=24, rings=16)
        lock.rotation_euler.y = (-0.18 if x < 0 else 0.18)
        objects_by_bone["head"].append(lock)
    bangs = [(-0.52, 1.66, 0.25, 0.40), (-0.29, 1.76, 0.27, 0.50), (0.0, 1.80, 0.29, 0.55), (0.29, 1.76, 0.27, 0.50), (0.52, 1.66, 0.25, 0.40)]
    for index, (x, z, sx, sz) in enumerate(bangs):
        bang = sphere(f"front bang.{index}", (x, -0.59, z), (sx, 0.17, sz), hair_light if index in (1, 2, 3) else hair, segments=24, rings=16)
        bang.rotation_euler.y = (-0.14 if x < 0 else 0.14) if x else 0
        objects_by_bone["head"].append(bang)
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        outer_ear = polygon(f"ear.{suffix}", [(side * 0.62, 1.57), (side * 0.98, 1.76), (side * 0.73, 1.37)], 0.09, skin)
        outer_ear.location.y = 0.01
        objects_by_bone["head"].append(outer_ear)
        inner = polygon(f"ear inner.{suffix}", [(side * 0.69, 1.57), (side * 0.87, 1.69), (side * 0.75, 1.48)], 0.095, ear_inner)
        inner.location.y = -0.055
        objects_by_bone["head"].append(inner)
        x = side * 0.30
        objects_by_bone["head"].append(sphere(f"eye outer.{suffix}", (x, -0.69, 1.59), (0.235, 0.105, 0.285), eye_outer, segments=24, rings=18))
        objects_by_bone["head"].append(sphere(f"iris.{suffix}", (x, -0.785, 1.55), (0.17, 0.045, 0.215), iris, segments=24, rings=18))
        objects_by_bone["head"].append(sphere(f"iris glow.{suffix}", (x, -0.825, 1.47), (0.13, 0.025, 0.10), iris_glow, segments=20, rings=14))
        objects_by_bone["head"].append(sphere(f"highlight big.{suffix}", (x - side * 0.065, -0.85, 1.68), (0.055, 0.025, 0.07), highlight, segments=16, rings=12))
        objects_by_bone["head"].append(sphere(f"highlight small.{suffix}", (x + side * 0.055, -0.85, 1.60), (0.025, 0.018, 0.032), highlight, segments=12, rings=8))
        objects_by_bone["head"].append(sphere(f"blush.{suffix}", (side * 0.47, -0.70, 1.32), (0.13, 0.035, 0.065), blush, segments=18, rings=12))
    objects_by_bone["head"].append(sphere("small nose", (0, -0.80, 1.39), (0.065, 0.040, 0.045), skin, segments=16, rings=10))
    objects_by_bone["head"].append(smile("smile", mouth_mat))

    # Four soft wings behind the body, each with a distinct silhouette.
    wing_shapes = [
        [(-0.48, 1.12), (-0.88, 1.48), (-1.28, 1.32), (-1.02, 0.90), (-0.60, 0.82)],
        [(-0.46, 0.96), (-0.84, 0.84), (-1.20, 0.45), (-0.72, 0.56), (-0.44, 0.76)],
    ]
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        for index, shape in enumerate(wing_shapes):
            mirrored = [(x * side, z) for x, z in shape]
            obj = polygon(f"wing.{suffix}.{index}", mirrored, 0.035, wing)
            obj.location.y = 0.18
            objects_by_bone[f"wing.{suffix}"].append(obj)

    # Small glowing motes are part of the supplied illustrated character plate.
    for index, (x, z, radius) in enumerate([(-1.16, 1.38, 0.075), (1.18, 1.70, 0.09), (0.98, 0.12, 0.045), (-1.02, 0.08, 0.055)]):
        objects_by_bone["root"].append(sphere(f"magic mote.{index}", (x, 0.05, z), (radius, radius, radius), orb_mat, segments=16, rings=10))

    armature = create_rig()
    # Keep render meshes in world space.  Bone-parented rigid meshes export
    # correctly in Blender but are interpreted differently by some GLTFLoader
    # versions, which can collapse the character in the browser.  The armature
    # and its named clips remain in the GLB for future skinned animation; the
    # web state machine controls the visible rigid parts directly for now.
    create_animations(armature)

    # Use NLA strips so every named action is available to GLTFLoader.
    armature.animation_data.action = None
    for track in armature.animation_data.nla_tracks:
        for strip in track.strips:
            strip.action_frame_start = 1
            strip.action_frame_end = strip.frame_end

    output_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in list(bpy.context.scene.objects):
        if obj.type in {"MESH", "ARMATURE"}:
            obj.select_set(True)
    bpy.context.view_layer.objects.active = armature
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(output_path),
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_materials="EXPORT",
            export_animations=True,
            export_nla_strips=True,
            export_def_bones=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
        )
    except TypeError:
        bpy.ops.export_scene.gltf(
            filepath=str(output_path),
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_materials="EXPORT",
            export_animations=True,
            export_nla_strips=True,
        )
    if blend_output:
        blend_path = blend_output.resolve()
        blend_path.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
        print(f"Saved Blender source {blend_path}")
    print(f"Exported {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    args = parse_args()
    build(Path(args.output).resolve(), Path(args.blend_output).resolve() if args.blend_output else None)
