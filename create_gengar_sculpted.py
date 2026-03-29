import bpy
import bmesh
import math
from mathutils import Vector

def clear_scene():
    """Clear the scene of all objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, roughness=0.5, subsurface=0.0):
    """Create a material with the given color."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Add Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    # Set base color
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    
    if subsurface > 0:
        # In Blender 4.x, check for subsurface inputs
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = subsurface
        if 'Subsurface Color' in bsdf.inputs:
            bsdf.inputs['Subsurface Color'].default_value = color
    
    # Connect nodes
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

def create_sculpted_gengar():
    """Create a Gengar using metaballs for organic sculpting effect."""
    
    # Colors (RGBA)
    purple = (0.4, 0.2, 0.5, 1.0)
    dark_purple = (0.25, 0.15, 0.35, 1.0)
    red = (0.9, 0.1, 0.15, 1.0)
    white = (0.95, 0.95, 0.95, 1.0)
    pink = (0.95, 0.4, 0.6, 1.0)
    black = (0.05, 0.05, 0.05, 1.0)
    
    # Create materials
    purple_mat = create_material("Purple", purple, roughness=0.3, subsurface=0.1)
    dark_purple_mat = create_material("DarkPurple", dark_purple, roughness=0.4)
    red_mat = create_material("Red", red, roughness=0.2, subsurface=0.2)
    white_mat = create_material("White", white, roughness=0.2)
    pink_mat = create_material("Pink", pink, roughness=0.3, subsurface=0.3)
    black_mat = create_material("Black", black, roughness=0.1)
    
    # === METABALL BODY ===
    # Create the main metaball for the body
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 1.0))
    body_mball = bpy.context.active_object
    body_mball.name = "Gengar_Body"
    body_mball.data.resolution = 0.08  # Higher resolution for smoother surface
    
    # Main body mass (large, slightly flattened)
    create_metaball_element(body_mball.data, 0, 0, 0, 1.2)
    create_metaball_element(body_mball.data, 0, 0, 0.5, 1.0)
    create_metaball_element(body_mball.data, 0, 0, -0.3, 1.0)
    
    # Left ear - merged with body
    create_metaball_element(body_mball.data, -0.7, 0, 0.9, 0.6)
    create_metaball_element(body_mball.data, -0.9, 0.2, 1.3, 0.4)
    create_metaball_element(body_mball.data, -1.1, 0.4, 1.6, 0.3)
    
    # Right ear - merged with body
    create_metaball_element(body_mball.data, 0.7, 0, 0.9, 0.6)
    create_metaball_element(body_mball.data, 0.9, 0.2, 1.3, 0.4)
    create_metaball_element(body_mball.data, 1.1, 0.4, 1.6, 0.3)
    
    # Back spike
    create_metaball_element(body_mball.data, 0, -0.9, 0.5, 0.5)
    
    # Arms - organic extensions of body
    create_metaball_element(body_mball.data, -0.8, 0, 0.2, 0.5)
    create_metaball_element(body_mball.data, -1.1, 0.1, 0.6, 0.35)
    create_metaball_element(body_mball.data, -1.3, 0.2, 0.9, 0.25)
    
    create_metaball_element(body_mball.data, 0.8, 0, 0.2, 0.5)
    create_metaball_element(body_mball.data, 1.1, 0.1, 0.6, 0.35)
    create_metaball_element(body_mball.data, 1.3, 0.2, 0.9, 0.25)
    
    # Legs
    create_metaball_element(body_mball.data, -0.4, 0, -0.8, 0.45)
    create_metaball_element(body_mball.data, 0.4, 0, -0.8, 0.45)
    
    # Apply material to metaball
    body_mball.data.materials.append(purple_mat)
    
    # Convert metaball to mesh for better control
    bpy.context.view_layer.objects.active = body_mball
    bpy.ops.object.convert(target='MESH')
    body_mesh = bpy.context.active_object
    body_mesh.name = "Gengar_Body_Mesh"
    
    # Add subdivision and smooth shading
    subsurf = body_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3
    
    bpy.ops.object.shade_smooth()
    
    # === MOUTH CAVITY (Negative space) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0.6, 0.3))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.3, 0.5, 1.0)
    mouth.data.materials.append(dark_purple_mat)
    
    # === TONGUE ===
    # Use metaballs for organic tongue
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0.7, -0.1))
    tongue_mball = bpy.context.active_object
    tongue_mball.name = "Tongue"
    tongue_mball.data.resolution = 0.1
    
    create_metaball_element(tongue_mball.data, 0, 0, 0, 0.3)
    create_metaball_element(tongue_mball.data, 0, 0.1, -0.3, 0.28)
    create_metaball_element(tongue_mball.data, 0, 0.2, -0.5, 0.25)
    create_metaball_element(tongue_mball.data, 0, 0.35, -0.65, 0.2)
    
    tongue_mball.data.materials.append(pink_mat)
    
    bpy.context.view_layer.objects.active = tongue_mball
    bpy.ops.object.convert(target='MESH')
    tongue_mesh = bpy.context.active_object
    tongue_mesh.name = "Tongue_Mesh"
    
    subsurf_tongue = tongue_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf_tongue.levels = 2
    bpy.ops.object.shade_smooth()
    
    # === EYES ===
    # Eye whites - oval shapes
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(-0.35, 0.5, 0.5))
    left_eye_white = bpy.context.active_object
    left_eye_white.name = "Left_Eye_White"
    left_eye_white.scale = (0.6, 0.4, 1.2)
    left_eye_white.data.materials.append(white_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(0.35, 0.5, 0.5))
    right_eye_white = bpy.context.active_object
    right_eye_white.name = "Right_Eye_White"
    right_eye_white.scale = (0.6, 0.4, 1.2)
    right_eye_white.data.materials.append(white_mat)
    bpy.ops.object.shade_smooth()
    
    # Red irises
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.35, 0.52, 0.65))
    left_iris = bpy.context.active_object
    left_iris.name = "Left_Iris"
    left_iris.scale = (0.8, 0.8, 0.3)
    left_iris.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0.35, 0.52, 0.65))
    right_iris = bpy.context.active_object
    right_iris.name = "Right_Iris"
    right_iris.scale = (0.8, 0.8, 0.3)
    right_iris.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    # Black pupils
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-0.35, 0.53, 0.75))
    left_pupil = bpy.context.active_object
    left_pupil.name = "Left_Pupil"
    left_pupil.scale = (1, 1, 0.5)
    left_pupil.data.materials.append(black_mat)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0.35, 0.53, 0.75))
    right_pupil = bpy.context.active_object
    right_pupil.name = "Right_Pupil"
    right_pupil.scale = (1, 1, 0.5)
    right_pupil.data.materials.append(black_mat)
    
    # === TEETH ===
    for i in range(4):
        x_pos = -0.22 + (i * 0.15)
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.04, 
            depth=0.12, 
            location=(x_pos, 0.65, 0.35),
            rotation=(math.radians(-15), 0, 0)
        )
        tooth = bpy.context.active_object
        tooth.name = f"Tooth_{i}"
        tooth.data.materials.append(white_mat)
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Three-point lighting
    bpy.ops.object.light_add(type='AREA', location=(3, 2, 4))
    key_light = bpy.context.active_object
    key_light.data.energy = 250
    key_light.data.color = (1.0, 0.9, 1.0)
    key_light.scale = (2, 2, 2)
    
    bpy.ops.object.light_add(type='AREA', location=(-3, 1, 3))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 120
    fill_light.data.color = (1.0, 0.85, 0.9)
    fill_light.scale = (2, 2, 2)
    
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 2))
    back_light = bpy.context.active_object
    back_light.data.energy = 180
    back_light.data.color = (0.8, 0.9, 1.0)
    back_light.scale = (3, 3, 3)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4, 1.0))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(90), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Sculpted Gengar created successfully!")
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

# Main execution
if __name__ == "__main__":
    clear_scene()
    create_sculpted_gengar()
    
    output_path = "/home/freeman/.openclaw/workspace/gengar-project/gengar_sculpted.glb"
    export_gltf(output_path)
    print("Done!")
