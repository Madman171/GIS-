"""Local Blender refinement pass for the Lux3D Spirit Pix preview.

This deliberately stays offline: it edits the downloaded GLB scene and does
not call Lux3D or touch the production frontend.
"""

import argparse
import math
import sys

import bpy
from mathutils import Vector


def parse_args():
    raw = sys.argv
    if "--" in raw:
        raw = raw[raw.index("--") + 1 :]
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--blend-output", required=True)
    parser.add_argument("--glb-output", required=True)
    return parser.parse_args(raw)


def material(name, color, metallic=0.0, roughness=0.35):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def add_uv_sphere(name, location, scale, mat, segments=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def add_smile(mat):
    curve = bpy.data.curves.new("gentle smiling mouth", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 12
    curve.bevel_depth = 0.00075
    curve.bevel_resolution = 4
    spline = curve.splines.new("BEZIER")
    points = [(-0.0048, -0.0630, 0.0080), (-0.0023, -0.0635, 0.0062),
              (0.0, -0.0636, 0.0057), (0.0023, -0.0635, 0.0062),
              (0.0048, -0.0630, 0.0080)]
    spline.bezier_points.add(len(points) - 1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new("smile overlay", curve)
    bpy.context.scene.collection.objects.link(obj)
    curve.materials.append(mat)
    return obj


def add_finger_details(skin):
    # Small rounded finger pads are intentionally subtle and remain separate
    # objects so they can be adjusted later without sculpting the source mesh.
    for side in (-1, 1):
        for index, (dx, dz) in enumerate(((0.0, 0.0), (0.0017, -0.0009), (-0.0017, -0.0009))):
            x = side * (0.0285 + dx * side)
            z = -0.0375 + dz
            pad = add_uv_sphere(
                f"hand {side:+d} finger pad {index + 1}",
                (x, -0.0577, z),
                (0.00135, 0.00055, 0.00225),
                skin,
                segments=16,
                rings=8,
            )
            pad.rotation_euler[1] = side * math.radians(10)


def main():
    args = parse_args()
    bpy.ops.wm.open_mainfile(filepath=args.input)
    character = bpy.data.objects.get("geometry_0")
    if character is None or character.type != "MESH":
        raise RuntimeError("Lux3D scene does not contain geometry_0 mesh")

    # Preserve the soft toy-like shading on the base mesh while keeping its
    # original geometry and materials intact.
    for polygon in character.data.polygons:
        polygon.use_smooth = True

    # Round and slightly soften the head silhouette. The body and wings are
    # below this band, so the operation only affects the head/hair region.
    for vertex in character.data.vertices:
        if vertex.co.z > 0.014:
            vertex.co.x *= 1.050
            vertex.co.y *= 1.020

    skin = material("refinement skin", (0.98, 0.60, 0.60), roughness=0.28)
    mouth = material("warm smile", (0.30, 0.06, 0.10), roughness=0.30)
    white = material("eye catchlight", (1.0, 0.98, 0.96), roughness=0.12)
    # The Lux3D eye material already contains the blue gradient and base
    # reflections. Keep only one restrained catchlight per eye for a clean face.
    for side in (-1, 1):
        add_uv_sphere(
            f"eye {side:+d} large catchlight",
            (side * 0.0182, -0.0630, 0.0205),
            (0.0018, 0.00055, 0.0018),
            white,
        )

    add_smile(mouth)
    add_finger_details(skin)

    # Preserve the editable refinement scene with the studio camera/lights.
    bpy.ops.wm.save_as_mainfile(filepath=args.blend_output)

    # Export only character geometry and refinement overlays to GLB.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE"} and obj.name not in {"white preview card", "Plane"}:
            obj.select_set(True)
    bpy.context.view_layer.objects.active = character
    bpy.ops.export_scene.gltf(
        filepath=args.glb_output,
        export_format="GLB",
        use_selection=True,
        export_cameras=False,
        export_lights=False,
        export_apply=True,
    )


if __name__ == "__main__":
    main()
