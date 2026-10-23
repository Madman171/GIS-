"""Build the production AI pet GLB used by the GIS knowledge platform.

This is intentionally procedural so the model can be rebuilt after a Blender
upgrade without relying on an opaque source file.  The target is a small,
stylised blue-haired fairy: rounded proportions, expressive eyes, translucent
wings and a light blue outfit.  The script also exports named NLA clips for the
web state machine (Idle, Hover, Wave, Think, Talk and Happy).

Run with:
  blender -b --python tools/build_ai_pet.py -- --output frontend/public/assets/ai-pet/spirit_pix.glb
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


def build(output_path: Path) -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)

    skin = material("skin", (0.98, 0.66, 0.62), roughness=0.58)
    hair = material("blue hair", (0.12, 0.38, 0.88), roughness=0.42)
    hair_light = material("hair highlights", (0.30, 0.66, 1.0), roughness=0.34, emission=(0.04, 0.14, 0.38))
    cloth = material("sky blue outfit", (0.30, 0.62, 0.98), roughness=0.68)
    boot = material("blue boots", (0.10, 0.30, 0.76), roughness=0.45)
    eye_white = material("eye white", (1.0, 1.0, 1.0), roughness=0.18)
    iris = material("ocean iris", (0.04, 0.24, 0.72), roughness=0.18, emission=(0.01, 0.06, 0.20))
    highlight = material("eye highlight", (1.0, 1.0, 1.0), roughness=0.05, emission=(0.6, 0.8, 1.0))
    blush = material("soft blush", (1.0, 0.38, 0.48), roughness=0.75, alpha=0.78)
    mouth_mat = material("smile", (0.64, 0.16, 0.25), roughness=0.6)
    wing = material("translucent wings", (0.38, 0.86, 1.0), roughness=0.2, alpha=0.34, transmission=0.25, emission=(0.05, 0.18, 0.35))

    objects_by_bone = {"root": [], "spine": [], "head": [], "arm.L": [], "arm.R": [], "leg.L": [], "leg.R": [], "wing.L": [], "wing.R": []}

    # Body and clothing.
    objects_by_bone["spine"].append(sphere("body", (0, 0, 0.78), (0.48, 0.35, 0.62), cloth))
    objects_by_bone["spine"].append(sphere("neck", (0, -0.01, 1.24), (0.16, 0.14, 0.13), skin))
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        objects_by_bone[f"arm.{suffix}"].append(cylinder(f"sleeve.{suffix}", (side * 0.47, 0, 0.89), 0.105, 0.50, cloth, rotation=(0, side * -0.22, side * 0.10)))
        objects_by_bone[f"arm.{suffix}"].append(sphere(f"hand.{suffix}", (side * 0.58, -0.01, 0.58), (0.12, 0.12, 0.16), skin))
        objects_by_bone[f"leg.{suffix}"].append(cylinder(f"leg.{suffix}", (side * 0.18, 0, 0.30), 0.115, 0.45, skin))
        objects_by_bone[f"leg.{suffix}"].append(rounded_cube(f"boot.{suffix}", (side * 0.18, -0.07, -0.02), (0.18, 0.22, 0.12), boot, bevel=0.08))

    # Head, face and hair.
    objects_by_bone["head"].append(sphere("head", (0, 0, 1.55), (0.73, 0.60, 0.69), skin))
    objects_by_bone["head"].append(sphere("hair cap", (0, 0.03, 1.69), (0.78, 0.64, 0.73), hair))
    bangs = [(-0.46, 1.63, 0.24, 0.36), (-0.20, 1.74, 0.25, 0.43), (0.10, 1.75, 0.26, 0.46), (0.40, 1.64, 0.24, 0.36)]
    for index, (x, z, sx, sz) in enumerate(bangs):
        objects_by_bone["head"].append(sphere(f"bang.{index}", (x, -0.56, z), (sx, 0.15, sz), hair_light if index == 1 else hair, segments=20, rings=12))
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        objects_by_bone["head"].append(polygon(f"ear.{suffix}", [(side * 0.55, 1.54), (side * 0.88, 1.72), (side * 0.68, 1.34)], 0.08, skin))
        x = side * 0.285
        objects_by_bone["head"].append(sphere(f"eye.{suffix}", (x, -0.66, 1.56), (0.205, 0.10, 0.245), eye_white))
        objects_by_bone["head"].append(sphere(f"iris.{suffix}", (x, -0.755, 1.54), (0.145, 0.045, 0.18), iris))
        objects_by_bone["head"].append(sphere(f"highlight.{suffix}", (x - side * 0.045, -0.805, 1.62), (0.042, 0.025, 0.055), highlight))
        objects_by_bone["head"].append(sphere(f"blush.{suffix}", (side * 0.39, -0.68, 1.29), (0.11, 0.03, 0.06), blush, segments=16, rings=10))
    objects_by_bone["head"].append(sphere("nose", (0, -0.76, 1.36), (0.055, 0.035, 0.042), skin, segments=16, rings=10))
    objects_by_bone["head"].append(smile("smile", mouth_mat))

    # Four soft wings behind the body, each with a distinct silhouette.
    wing_shapes = [
        [(-0.48, 1.08), (-0.86, 1.42), (-1.26, 1.30), (-0.98, 0.88), (-0.58, 0.78)],
        [(-0.45, 0.98), (-0.83, 0.88), (-1.17, 0.48), (-0.72, 0.52), (-0.45, 0.76)],
    ]
    for side in (-1, 1):
        suffix = "L" if side < 0 else "R"
        for index, shape in enumerate(wing_shapes):
            mirrored = [(x * side, z) for x, z in shape]
            obj = polygon(f"wing.{suffix}.{index}", mirrored, 0.035, wing)
            obj.location.y = 0.18
            objects_by_bone[f"wing.{suffix}"].append(obj)

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
    print(f"Exported {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    args = parse_args()
    build(Path(args.output).resolve())
