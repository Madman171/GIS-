import argparse
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
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = args.output

camera_data = bpy.data.cameras.new('PreviewCamera')
camera = bpy.data.objects.new('PreviewCamera', camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
camera.location = (0, -5.4, 0.12)
camera.data.lens = 58
camera.rotation_euler = (Vector((0, 0, 0.05)) - camera.location).to_track_quat('-Z', 'Y').to_euler()

for name, location, energy, color, size in [
    ('Key', (2.5, -3.5, 4.5), 700, (1.0, 0.95, 0.9), 4.0),
    ('Fill', (-3.0, -2.0, 2.0), 450, (0.45, 0.75, 1.0), 3.0),
    ('Rim', (0, 2.0, 3.5), 800, (0.25, 0.65, 1.0), 3.0),
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

bpy.ops.render.render(write_still=True)
