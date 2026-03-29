import bpy
import bmesh
import math
from mathutils import Vector

def clear_scene():
    """Clear the scene of all objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, roughness=0.5, subsurface=0.0, emission=0.0):
    """Create a material with the given color."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    
    if subsurface > 0:
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = subsurface
        if 'Subsurface Color' in bsdf.inputs:
            bsdf.inputs['Subsurface Color'].default_value = color
    
    if emission > 0:
        bsdf.inputs['Emission Strength'].default_value = emission
        bsdf.inputs['Emission Color'].default_value = color
    
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_metaball_element(mball, x, y, z, radius, negative=False):
    """Add an element to a metaball object."""
    element = mball.elements.new()
    element.co = (x, y, z)
    element.radius = radius
    element.type = 'BALL'
    if negative:
        element.negative = True
    return element

def create_realistic_pikachu():
    """Create a realistic Pikachu based on official artwork."""
    
    # Accurate Pikachu colors
    yellow = (0.98, 0.88, 0.15, 1.0)
    orange_yellow = (0.95, 0.75, 0.12, 1.0)
    brown = (0.42, 0.28, 0.16, 1.0)
    red = (0.92, 0.18, 0.12, 1.0)
    black = (0.03, 0.03, 0.03, 1.0)
    white = (0.98, 0.98, 0.98, 1.0)
    
    yellow_mat = create_material("Yellow", yellow, roughness=0.38, subsurface=0.12)
    brown_mat = create_material("Brown", brown, roughness=0.5)
    red_mat = create_material("Red", red, roughness=0.32, subsurface=0.25)
    black_mat = create_material("Black", black, roughness=0.1)
    white_mat = create_material("White", white, roughness=0.2)
    
    # === BODY ===
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 0.9))
    body_mball = bpy.context.active_object
    body_mball.name = "Pikachu_Body"
    body_mball.data.resolution = 0.06
    
    # Lower body
    create_metaball_element(body_mball.data, 0, 0, -0.25, 0.95)
    create_metaball_element(body_mball.data, 0, 0, 0.0, 0.92)
    create_metaball_element(body_mball.data, 0, 0, 0.25, 0.85)
    create_metaball_element(body_mball.data, 0, 0, 0.5, 0.78)
    create_metaball_element(body_mball.data, 0, 0, 0.75, 0.72)
    
    # Shoulders
    create_metaball_element(body_mball.data, -0.5, 0, 0.55, 0.55)
    create_metaball_element(body_mball.data, 0.5, 0, 0.55, 0.55)
    
    # HEAD
    create_metaball_element(body_mball.data, 0, 0, 1.05, 0.85)
    create_metaball_element(body_mball.data, 0, 0, 1.3, 0.82)
    create_metaball_element(body_mball.data, 0, 0, 1.55, 0.78)
    create_metaball_element(body_mball.data, 0, 0, 1.75, 0.7)
    
    # Left ear
    create_metaball_element(body_mball.data, -0.45, 0, 2.15, 0.28)
    create_metaball_element(body_mball.data, -0.6, 0, 2.4, 0.24)
    create_metaball_element(body_mball.data, -0.75, 0.05, 2.65, 0.2)
    create_metaball_element(body_mball.data, -0.9, 0.1, 2.9, 0.16)
    create_metaball_element(body_mball.data, -1.05, 0.15, 3.15, 0.13)
    create_metaball_element(body_mball.data, -1.2, 0.2, 3.4, 0.1)
    
    # Right ear
    create_metaball_element(body_mball.data, 0.45, 0, 2.15, 0.28)
    create_metaball_element(body_mball.data, 0.6, 0, 2.4, 0.24)
    create_metaball_element(body_mball.data, 0.75, 0.05, 2.65, 0.2)
    create_metaball_element(body_mball.data, 0.9, 0.1, 2.9, 0.16)
    create_metaball_element(body_mball.data, 1.05, 0.15, 3.15, 0.13)
    create_metaball_element(body_mball.data, 1.2, 0.2, 3.4, 0.1)
    
    # Arms
    create_metaball_element(body_mball.data, -0.6, 0, 0.15, 0.32)
    create_metaball_element(body_mball.data, -0.85, 0.1, 0.3, 0.26)
    create_metaball_element(body_mball.data, 0.6, 0, 0.15, 0.32)
    create_metaball_element(body_mball.data, 0.85, 0.1, 0.3, 0.26)
    
    # Feet
    create_metaball_element(body_mball.data, -0.4, 0.15, -0.6, 0.35)
    create_metaball_element(body_mball.data, -0.4, 0.35, -0.8, 0.28)
    create_metaball_element(body_mball.data, 0.4, 0.15, -0.6, 0.35)
    create_metaball_element(body_mball.data, 0.4, 0.35, -0.8, 0.28)
    
    # Tail
    create_metaball_element(body_mball.data, 0, -0.7, -0.1, 0.35)
    create_metaball_element(body_mball.data, 0, -0.9, 0.15, 0.3)
    create_metaball_element(body_mball.data, 0, -1.05, 0.45, 0.28)
    create_metaball_element(body_mball.data, 0, -1.15, 0.75, 0.32)
    create_metaball_element(body_mball.data, 0, -1.2, 1.05, 0.35)
    create_metaball_element(body_mball.data, 0, -1.25, 1.35, 0.4)
    
    body_mball.data.materials.append(yellow_mat)
    
    bpy.context.view_layer.objects.active = body_mball
    bpy.ops.object.convert(target='MESH')
    body_mesh = bpy.context.active_object
    body_mesh.name = "Pikachu_Body_Mesh"
    
    subsurf = body_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4
    bpy.ops.object.shade_smooth()
    
    # === EAR TIPS ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(-1.3, 0.25, 3.55))
    left_tip = bpy.context.active_object
    left_tip.name = "Left_Ear_Tip"
    left_tip.scale = (0.8, 0.5, 1.2)
    left_tip.rotation_euler = (math.radians(15), 0, math.radians(-15))
    left_tip.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(1.3, 0.25, 3.55))
    right_tip = bpy.context.active_object
    right_tip.name = "Right_Ear_Tip"
    right_tip.scale = (0.8, 0.5, 1.2)
    right_tip.rotation_euler = (math.radians(15), 0, math.radians(15))
    right_tip.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    # === CHEEKS ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(-0.38, 0.42, 1.1))
    left_cheek = bpy.context.active_object
    left_cheek.name = "Left_Cheek"
    left_cheek.scale = (1.1, 0.7, 0.9)
    left_cheek.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0.38, 0.42, 1.1))
    right_cheek = bpy.context.active_object
    right_cheek.name = "Right_Cheek"
    right_cheek.scale = (1.1, 0.7, 0.9)
    right_cheek.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    # === EYES ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(-0.28, 0.28, 1.35))
    left_eye = bpy.context.active_object
    left_eye.name = "Left_Eye"
    left_eye.scale = (0.9, 1, 0.35)
    left_eye.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(0.28, 0.28, 1.35))
    right_eye = bpy.context.active_object
    right_eye.name = "Right_Eye"
    right_eye.scale = (0.9, 1, 0.35)
    right_eye.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    # === EYE HIGHLIGHTS ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(-0.22, 0.32, 1.42))
    left_highlight = bpy.context.active_object
    left_highlight.name = "Left_Highlight"
    left_highlight.scale = (1, 1, 0.5)
    left_highlight.data.materials.append(white_mat)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0.34, 0.32, 1.42))
    right_highlight = bpy.context.active_object
    right_highlight.name = "Right_Highlight"
    right_highlight.scale = (1, 1, 0.5)
    right_highlight.data.materials.append(white_mat)
    
    # === NOSE ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(0, 0.42, 1.25))
    nose = bpy.context.active_object
    nose.name = "Nose"
    nose.scale = (1, 0.6, 1)
    nose.data.materials.append(black_mat)
    
    # === MOUTH ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0, 0.45, 1.15))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.3, 0.3, 0.5)
    mouth.data.materials.append(black_mat)
    
    # === BODY STRIPES ===
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.6, location=(0, -0.7, 0.35), rotation=(math.radians(90), 0, 0))
    stripe1 = bpy.context.active_object
    stripe1.name = "Stripe1"
    stripe1.scale = (1.2, 0.25, 1)
    stripe1.data.materials.append(brown_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.5, location=(0, -0.75, 0.05), rotation=(math.radians(90), 0, 0))
    stripe2 = bpy.context.active_object
    stripe2.name = "Stripe2"
    stripe2.scale = (1.1, 0.2, 1)
    stripe2.data.materials.append(brown_mat)
    bpy.ops.object.shade_smooth()
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    bpy.ops.object.light_add(type='AREA', location=(3, 3, 6))
    key_light = bpy.context.active_object
    key_light.data.energy = 350
    key_light.data.color = (1.0, 0.95, 0.85)
    key_light.scale = (3, 3, 3)
    
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 5))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 200
    fill_light.data.color = (1.0, 0.92, 0.95)
    fill_light.scale = (3, 3, 3)
    
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 4))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 250
    rim_light.data.color = (0.9, 0.95, 1.0)
    rim_light.scale = (4, 4, 4)
    
    bpy.ops.object.light_add(type='AREA', location=(0, 0, -1))
    bounce = bpy.context.active_object
    bounce.data.energy = 120
    bounce.data.color = (1.0, 0.95, 0.9)
    bounce.scale = (5, 5, 5)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4.2, 1.8))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(70), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Realistic Pikachu created!")
    return camera

def export_gltf(filepath):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_yup=True,
        export_materials='EXPORT',
        export_cameras=True,
        export_lights=True,
        export_apply=True
    )
    print(f"Exported to {filepath}")

if __name__ == "__main__":
    clear_scene()
    create_realistic_pikachu()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/pikachu_realistic.glb")
    print("Done!")
