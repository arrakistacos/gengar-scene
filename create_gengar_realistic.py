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

def create_realistic_gengar():
    """Create a more realistic Gengar based on official artwork."""
    
    # More accurate colors
    purple = (0.35, 0.18, 0.48, 1.0)  # Deeper purple
    dark_purple = (0.18, 0.12, 0.28, 1.0)  # Darker for mouth
    red = (0.95, 0.08, 0.12, 1.0)  # Bright red eyes
    white = (0.98, 0.98, 0.98, 1.0)
    pink = (0.95, 0.45, 0.65, 1.0)  # Tongue pink
    black = (0.02, 0.02, 0.02, 1.0)
    
    purple_mat = create_material("Purple", purple, roughness=0.35, subsurface=0.15)
    dark_purple_mat = create_material("DarkPurple", dark_purple, roughness=0.5)
    red_mat = create_material("Red", red, roughness=0.2, subsurface=0.3)
    white_mat = create_material("White", white, roughness=0.2)
    pink_mat = create_material("Pink", pink, roughness=0.35, subsurface=0.25)
    black_mat = create_material("Black", black, roughness=0.1)
    
    # === MAIN BODY ===
    # Gengar has a round, plump body with tapering
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 1.0))
    body_mball = bpy.context.active_object
    body_mball.name = "Gengar_Body"
    body_mball.data.resolution = 0.06  # Higher resolution
    
    # Main body - wider at bottom, tapering up
    create_metaball_element(body_mball.data, 0, 0, -0.3, 1.3)  # Wide base
    create_metaball_element(body_mball.data, 0, 0, 0.1, 1.25)
    create_metaball_element(body_mball.data, 0, 0, 0.5, 1.15)
    create_metaball_element(body_mball.data, 0, 0, 0.9, 1.0)   # Chest area
    
    # Shoulders/upper body
    create_metaball_element(body_mball.data, -0.6, 0, 0.7, 0.7)
    create_metaball_element(body_mball.data, 0.6, 0, 0.7, 0.7)
    
    # Left ear - long, curved, pointed
    create_metaball_element(body_mball.data, -0.7, 0, 1.3, 0.5)
    create_metaball_element(body_mball.data, -0.85, 0.1, 1.65, 0.4)
    create_metaball_element(body_mball.data, -1.0, 0.2, 1.95, 0.32)
    create_metaball_element(body_mball.data, -1.15, 0.35, 2.2, 0.25)
    create_metaball_element(body_mball.data, -1.3, 0.5, 2.45, 0.18)
    
    # Right ear
    create_metaball_element(body_mball.data, 0.7, 0, 1.3, 0.5)
    create_metaball_element(body_mball.data, 0.85, 0.1, 1.65, 0.4)
    create_metaball_element(body_mball.data, 1.0, 0.2, 1.95, 0.32)
    create_metaball_element(body_mball.data, 1.15, 0.35, 2.2, 0.25)
    create_metaball_element(body_mball.data, 1.3, 0.5, 2.45, 0.18)
    
    # Back spikes (Gengar has 3-4 spikes on back)
    create_metaball_element(body_mball.data, 0, -1.0, 0.5, 0.45)
    create_metaball_element(body_mball.data, 0, -1.2, 0.8, 0.35)
    create_metaball_element(body_mball.data, -0.3, -0.9, 0.3, 0.35)
    create_metaball_element(body_mball.data, 0.3, -0.9, 0.3, 0.35)
    
    # Left arm - short, stubby
    create_metaball_element(body_mball.data, -0.9, 0.1, 0.1, 0.45)
    create_metaball_element(body_mball.data, -1.2, 0.15, 0.35, 0.35)
    create_metaball_element(body_mball.data, -1.45, 0.2, 0.6, 0.28)
    
    # Right arm
    create_metaball_element(body_mball.data, 0.9, 0.1, 0.1, 0.45)
    create_metaball_element(body_mball.data, 1.2, 0.15, 0.35, 0.35)
    create_metaball_element(body_mball.data, 1.45, 0.2, 0.6, 0.28)
    
    # Left leg - short
    create_metaball_element(body_mball.data, -0.5, 0, -0.8, 0.5)
    create_metaball_element(body_mball.data, -0.5, 0.15, -1.0, 0.4)
    
    # Right leg
    create_metaball_element(body_mball.data, 0.5, 0, -0.8, 0.5)
    create_metaball_element(body_mball.data, 0.5, 0.15, -1.0, 0.4)
    
    body_mball.data.materials.append(purple_mat)
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = body_mball
    bpy.ops.object.convert(target='MESH')
    body_mesh = bpy.context.active_object
    body_mesh.name = "Gengar_Body_Mesh"
    
    subsurf = body_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4
    bpy.ops.object.shade_smooth()
    
    # === MOUTH CAVITY ===
    # Wide grin shape
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(0, 0.65, 0.35))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.4, 0.6, 1.0)
    mouth.rotation_euler = (math.radians(10), 0, 0)
    mouth.data.materials.append(dark_purple_mat)
    bpy.ops.object.shade_smooth()
    
    # === TONGUE ===
    # Long, curved tongue sticking out
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0.8, 0.1))
    tongue_mball = bpy.context.active_object
    tongue_mball.name = "Tongue"
    tongue_mball.data.resolution = 0.08
    
    create_metaball_element(tongue_mball.data, 0, 0, 0, 0.28)
    create_metaball_element(tongue_mball.data, 0, 0.05, -0.2, 0.26)
    create_metaball_element(tongue_mball.data, 0, 0.12, -0.4, 0.24)
    create_metaball_element(tongue_mball.data, 0, 0.22, -0.6, 0.22)
    create_metaball_element(tongue_mball.data, 0, 0.35, -0.75, 0.18)
    create_metaball_element(tongue_mball.data, 0, 0.5, -0.85, 0.14)
    
    tongue_mball.data.materials.append(pink_mat)
    
    bpy.context.view_layer.objects.active = tongue_mball
    bpy.ops.object.convert(target='MESH')
    tongue_mesh = bpy.context.active_object
    tongue_mesh.name = "Tongue_Mesh"
    
    subsurf_tongue = tongue_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf_tongue.levels = 2
    bpy.ops.object.shade_smooth()
    
    # === EYES ===
    # Gengar has narrow, slanted eyes with ovular whites
    # Left eye white - slanted shape
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(-0.32, 0.55, 0.6))
    left_eye_white = bpy.context.active_object
    left_eye_white.name = "Left_Eye_White"
    left_eye_white.scale = (0.9, 0.35, 1.3)
    left_eye_white.rotation_euler = (math.radians(-5), 0, math.radians(-10))
    left_eye_white.data.materials.append(white_mat)
    bpy.ops.object.shade_smooth()
    
    # Right eye white
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(0.32, 0.55, 0.6))
    right_eye_white = bpy.context.active_object
    right_eye_white.name = "Right_Eye_White"
    right_eye_white.scale = (0.9, 0.35, 1.3)
    right_eye_white.rotation_euler = (math.radians(-5), 0, math.radians(10))
    right_eye_white.data.materials.append(white_mat)
    bpy.ops.object.shade_smooth()
    
    # Red irises - small, centered
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.32, 0.58, 0.75))
    left_iris = bpy.context.active_object
    left_iris.name = "Left_Iris"
    left_iris.scale = (0.8, 0.6, 0.4)
    left_iris.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0.32, 0.58, 0.75))
    right_iris = bpy.context.active_object
    right_iris.name = "Right_Iris"
    right_iris.scale = (0.8, 0.6, 0.4)
    right_iris.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    # Black pupils - tiny, menacing
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-0.32, 0.6, 0.85))
    left_pupil = bpy.context.active_object
    left_pupil.name = "Left_Pupil"
    left_pupil.scale = (1, 1, 0.5)
    left_pupil.data.materials.append(black_mat)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0.32, 0.6, 0.85))
    right_pupil = bpy.context.active_object
    right_pupil.name = "Right_Pupil"
    right_pupil.scale = (1, 1, 0.5)
    right_pupil.data.materials.append(black_mat)
    
    # === TEETH ===
    # Small pointed teeth along the grin
    tooth_positions = [
        (-0.4, 0.7, 0.45), (-0.2, 0.72, 0.5), (0, 0.73, 0.52), 
        (0.2, 0.72, 0.5), (0.4, 0.7, 0.45)
    ]
    
    for i, pos in enumerate(tooth_positions):
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.04, depth=0.12, location=pos,
            rotation=(math.radians(-20), 0, 0)
        )
        tooth = bpy.context.active_object
        tooth.name = f"Tooth_{i}"
        tooth.data.materials.append(white_mat)
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Key light (soft purple)
    bpy.ops.object.light_add(type='AREA', location=(3, 2, 5))
    key_light = bpy.context.active_object
    key_light.data.energy = 300
    key_light.data.color = (1.0, 0.9, 1.0)
    key_light.scale = (2, 2, 2)
    
    # Fill light (warm)
    bpy.ops.object.light_add(type='AREA', location=(-3, 1, 4))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 150
    fill_light.data.color = (1.0, 0.88, 0.92)
    fill_light.scale = (2, 2, 2)
    
    # Rim light (cyan)
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 2))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 200
    rim_light.data.color = (0.75, 0.9, 1.0)
    rim_light.scale = (3, 3, 3)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4.5, 1.2))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(85), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Realistic Gengar created!")
    return camera

def export_gltf(filepath):
    """Export the scene as GLTF."""
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
    create_realistic_gengar()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/gengar_realistic.glb")
    print("Done!")
