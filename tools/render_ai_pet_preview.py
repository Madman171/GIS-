import argparse
import math
import bpy
from mathutils import Vector

argv = __import__('sys').argv
argv = argv[argv.index('--') + 1:] if '--' in argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
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
camera.data.ortho_scale = 3.35
camera.location = (0, -6.2, 1.18)
camera.rotation_euler = (Vector((0, 0, 1.18)) - camera.location).to_track_quat('-Z', 'Y').to_euler()

for name, location, energy, color, size in [
    ('Key', (2.5, -3.5, 4.5), 340, (1.0, 0.95, 0.9), 4.0),
    ('Fill', (-3.0, -2.0, 2.0), 180, (0.45, 0.75, 1.0), 3.0),
    ('Rim', (0, 2.0, 3.5), 380, (0.25, 0.65, 1.0), 3.0),
]:
    data = bpy.data.lights.new(name, 'AREA')
    data.energy = energy
    data.color = color
    data.shape = 'DISK'
    data.size = size
    lamp = bpy.data.objects.new(name, data)
    scene.collection.objects.link(lamp)
    lamp.location = location
    lamp.rotation_euler = (Vector((0, 0, 0.8)) - lamp.location).to_track_quat('-Z', 'Y').to_euler()

# A clean white studio card keeps the preview close to the supplied reference
# while leaving the exported GLB itself background-free.
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 1.1, 1.2), rotation=(math.pi / 2, 0, 0))
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
