import bpy
import os

# Clear and create simple test scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object

# Add material
mat = bpy.data.materials.new(name="Test")
mat.use_nodes = True
mat.node_tree.nodes.clear()
bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
bsdf.inputs['Base Color'].default_value = (0.5, 0.2, 0.8, 1.0)
mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
cube.data.materials.append(mat)

# Simple lighting
bpy.ops.object.select_by_type(type='LIGHT')
bpy.ops.object.delete()

bpy.ops.object.light_add(type='SUN', location=(0, -10, 10))
sun = bpy.context.active_object
sun.data.energy = 5

# Camera
bpy.ops.object.select_by_type(type='CAMERA')
bpy.ops.object.delete()
bpy.ops.object.camera_add(location=(0, -8, 0))
camera = bpy.context.active_object
camera.rotation_euler = (1.5708, 0, 3.14159)  # Look at origin
bpy.context.scene.camera = camera

# Simple render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.filepath = "/home/freeman/.openclaw/workspace/gengar-project/test_render.png"
scene.render.image_settings.file_format = 'PNG'

print(f"Camera location: {camera.location}")
print(f"Camera rotation: {camera.rotation_euler}")
print(f"Cube location: {cube.location}")
print(f"Objects in scene: {[obj.name for obj in bpy.context.scene.objects]}")

bpy.ops.render.render(write_still=True)
print("Test render saved")
