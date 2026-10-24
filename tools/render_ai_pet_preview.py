import argparse
import math
import bpy
from mathutils import Vector

argv = __import__('sys').argv
argv = argv[argv.index('--') + 1:] if '--' in argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--blend-output')
args = parser.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=args.input)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 500
scene.render.resolution_y = 560
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = args.output
if scene.world is None:
    scene.world = bpy.data.worlds.new('PreviewWorld')
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get('Background')
if background:
    background.inputs['Color'].default_value = (0.97, 0.98, 1.0, 1.0)
    background.inputs['Strength'].default_value = 0.32
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'Medium High Contrast'

camera_data = bpy.data.cameras.new('PreviewCamera')
camera = bpy.data.objects.new('PreviewCamera', camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
camera.data.type = 'ORTHO'

meshes = [obj for obj in scene.objects if obj.type == 'MESH']
corners = []
for obj in meshes:
    corners.extend([obj.matrix_world @ Vector(corner) for corner in obj.bound_box])
if not corners:
    raise RuntimeError('The imported GLB has no mesh objects to render')
min_x = min(point.x for point in corners)
max_x = max(point.x for point in corners)
min_y = min(point.y for point in corners)
max_y = max(point.y for point in corners)
min_z = min(point.z for point in corners)
max_z = max(point.z for point in corners)
center = Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2))
width = max_x - min_x
depth = max_y - min_y
height = max_z - min_z
scale_factor = max(width, height) / 2.5
light_scale = max(scale_factor * scale_factor, 0.02)
camera.data.ortho_scale = max(width, height) * 1.28
camera_distance = max(depth * 12.0, max(width, height) * 10.0, 1.0)
camera.location = (center.x, center.y - camera_distance, center.z)
camera.rotation_euler = (center - camera.location).to_track_quat('-Z', 'Y').to_euler()

for name, location, energy, color, size in [
    ('Key', (center.x + width * 3.0, center.y - camera_distance * 0.6, center.z + height * 3.0), 340 * light_scale, (1.0, 0.95, 0.9), max(width, height) * 2.5),
    ('Fill', (center.x - width * 3.0, center.y - camera_distance * 0.4, center.z + height), 180 * light_scale, (0.45, 0.75, 1.0), max(width, height) * 2.0),
    ('Rim', (center.x, center.y + camera_distance * 0.4, center.z + height * 3.0), 380 * light_scale, (0.25, 0.65, 1.0), max(width, height) * 2.0),
]:
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = energy
    data.color = color
    data.shape = 'DISK'
    data.size = size
    lamp = bpy.data.objects.new(name, data)
    scene.collection.objects.link(lamp)
    lamp.location = location
    lamp.rotation_euler = (center - lamp.location).to_track_quat('-Z', 'Y').to_euler()

# A clean white studio card keeps the preview close to the supplied reference
# while leaving the exported GLB itself background-free.
bpy.ops.mesh.primitive_plane_add(size=max(width, height) * 20.0, location=(center.x, max_y + depth * 2.0, center.z), rotation=(math.pi / 2, 0, 0))
card = bpy.context.object
card.name = 'white preview card'
card_mat = bpy.data.materials.new('white preview card material')
card_mat.use_nodes = True
nodes = card_mat.node_tree.nodes
nodes.clear()
emission = nodes.new('ShaderNodeEmission')
emission.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
emission.inputs['Strength'].default_value = 0.65
output = nodes.new('ShaderNodeOutputMaterial')
card_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
card.data.materials.append(card_mat)

bpy.ops.render.render(write_still=True)
if args.blend_output:
    bpy.ops.wm.save_as_mainfile(filepath=args.blend_output)
