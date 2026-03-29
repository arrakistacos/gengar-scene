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

def create_sculpted_pikachu():
    """Create a Pikachu using metaballs for organic sculpting effect."""
    
    # Colors (RGBA)
    yellow = (0.98, 0.85, 0.2, 1.0)
    dark_yellow = (0.85, 0.7, 0.1, 1.0)
    brown = (0.4, 0.25, 0.15, 1.0)
    red = (0.9, 0.15, 0.1, 1.0)
    black = (0.05, 0.05, 0.05, 1.0)
    white = (0.95, 0.95, 0.95, 1.0)
    
    # Create materials
    yellow_mat = create_material("Yellow", yellow, roughness=0.4, subsurface=0.1)
    dark_yellow_mat = create_material("DarkYellow", dark_yellow, roughness=0.4)
    brown_mat = create_material("Brown", brown, roughness=0.6)
    red_mat = create_material("Red", red, roughness=0.3, subsurface=0.2)
    black_mat = create_material("Black", black, roughness=0.1)
    white_mat = create_material("White", white, roughness=0.2)
    
    # === METABALL BODY ===
    bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 0.8))
    body_mball = bpy.context.active_object
    body_mball.name = "Pikachu_Body"
    body_mball.data.resolution = 0.08
    
    # Main body (pear shape - wider at bottom)
    create_metaball_element(body_mball.data, 0, 0, -0.2, 0.9)
    create_metaball_element(body_mball.data, 0, 0, 0.1, 0.85)
    create_metaball_element(body_mball.data, 0, 0, 0.4, 0.75)
    
    # Head - merged with body
    create_metaball_element(body_mball.data, 0, 0, 0.7, 0.8)
    create_metaball_element(body_mball.data, 0, 0, 0.95, 0.75)
    create_metaball_element(body_mball.data, 0, 0, 1.15, 0.7)
    
    # Left ear - long and pointed (built with overlapping spheres)
    create_metaball_element(body_mball.data, -0.35, 0, 1.5, 0.25)
    create_metaball_element(body_mball.data, -0.5, 0, 1.75, 0.22)
    create_metaball_element(body_mball.data, -0.7, 0, 2.0, 0.18)
    create_metaball_element(body_mball.data, -0.9, 0, 2.3, 0.14)
    create_metaball_element(body_mball.data, -1.1, 0, 2.6, 0.12)
    
    # Right ear
    create_metaball_element(body_mball.data, 0.35, 0, 1.5, 0.25)
    create_metaball_element(body_mball.data, 0.5, 0, 1.75, 0.22)
    create_metaball_element(body_mball.data, 0.7, 0, 2.0, 0.18)
    create_metaball_element(body_mball.data, 0.9, 0, 2.3, 0.14)
    create_metaball_element(body_mball.data, 1.1, 0, 2.6, 0.12)
    
    # Left arm
    create_metaball_element(body_mball.data, -0.55, 0, 0.3, 0.25)
    create_metaball_element(body_mball.data, -0.75, 0.1, 0.5, 0.2)
    
    # Right arm
    create_metaball_element(body_mball.data, 0.55, 0, 0.3, 0.25)
    create_metaball_element(body_mball.data, 0.75, 0.1, 0.5, 0.2)
    
    # Left leg
    create_metaball_element(body_mball.data, -0.4, 0, -0.5, 0.3)
    create_metaball_element(body_mball.data, -0.4, 0.2, -0.7, 0.25)
    
    # Right leg
    create_metaball_element(body_mball.data, 0.4, 0, -0.5, 0.3)
    create_metaball_element(body_mball.data, 0.4, 0.2, -0.7, 0.25)
    
    # Tail base
    create_metaball_element(body_mball.data, 0, -0.7, -0.1, 0.25)
    create_metaball_element(body_mball.data, 0, -0.85, 0.15, 0.22)
    create_metaball_element(body_mball.data, 0, -0.95, 0.45, 0.2)
    create_metaball_element(body_mball.data, 0, -1.05, 0.75, 0.22)
    create_metaball_element(body_mball.data, 0, -1.1, 1.1, 0.25)
    
    # Apply material
    body_mball.data.materials.append(yellow_mat)
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = body_mball
    bpy.ops.object.convert(target='MESH')
    body_mesh = bpy.context.active_object
    body_mesh.name = "Pikachu_Body_Mesh"
    
    # Add subdivision
    subsurf = body_mesh.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3
    bpy.ops.object.shade_smooth()
    
    # === EAR TIPS (Black) ===
    # Left ear tip
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(-1.15, 0, 2.75))
    left_tip = bpy.context.active_object
    left_tip.name = "Left_Ear_Tip"
    left_tip.scale = (1, 0.6, 1.5)
    left_tip.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    # Right ear tip
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(1.15, 0, 2.75))
    right_tip = bpy.context.active_object
    right_tip.name = "Right_Ear_Tip"
    right_tip.scale = (1, 0.6, 1.5)
    right_tip.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    # === CHEEKS (Red) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(-0.3, 0.45, 0.85))
    left_cheek = bpy.context.active_object
    left_cheek.name = "Left_Cheek"
    left_cheek.scale = (1.2, 0.6, 0.8)
    left_cheek.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0.3, 0.45, 0.85))
    right_cheek = bpy.context.active_object
    right_cheek.name = "Right_Cheek"
    right_cheek.scale = (1.2, 0.6, 0.8)
    right_cheek.data.materials.append(red_mat)
    bpy.ops.object.shade_smooth()
    
    # === EYES (Black) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-0.22, 0.3, 1.05))
    left_eye = bpy.context.active_object
    left_eye.name = "Left_Eye"
    left_eye.scale = (0.8, 1, 0.3)
    left_eye.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0.22, 0.3, 1.05))
    right_eye = bpy.context.active_object
    right_eye.name = "Right_Eye"
    right_eye.scale = (0.8, 1, 0.3)
    right_eye.data.materials.append(black_mat)
    bpy.ops.object.shade_smooth()
    
    # === EYE HIGHLIGHTS (White) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(-0.18, 0.35, 1.1))
    left_highlight = bpy.context.active_object
    left_highlight.name = "Left_Highlight"
    left_highlight.data.materials.append(white_mat)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0.26, 0.35, 1.1))
    right_highlight = bpy.context.active_object
    right_highlight.name = "Right_Highlight"
    right_highlight.data.materials.append(white_mat)
    
    # === NOSE (Black) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(0, 0.45, 0.95))
    nose = bpy.context.active_object
    nose.name = "Nose"
    nose.scale = (0.8, 0.5, 1)
    nose.data.materials.append(black_mat)
    
    # === MOUTH (Black) ===
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(0, 0.48, 0.85))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.5, 0.4, 0.8)
    mouth.data.materials.append(black_mat)
    
    # === BODY STRIPES (Brown) ===
    # Stripe 1
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.5, location=(0, -0.65, 0.3), rotation=(math.radians(90), 0, 0))
    stripe1 = bpy.context.active_object
    stripe1.name = "Stripe1"
    stripe1.scale = (1, 0.3, 1)
    stripe1.data.materials.append(brown_mat)
    bpy.ops.object.shade_smooth()
    
    # Stripe 2
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.4, location=(0, -0.7, 0), rotation=(math.radians(90), 0, 0))
    stripe2 = bpy.context.active_object
    stripe2.name = "Stripe2"
    stripe2.scale = (1, 0.25, 1)
    stripe2.data.materials.append(brown_mat)
    bpy.ops.object.shade_smooth()
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Bright, cheerful lighting
    bpy.ops.object.light_add(type='AREA', location=(3, 3, 5))
    key_light = bpy.context.active_object
    key_light.data.energy = 280
    key_light.data.color = (1.0, 0.95, 0.8)
    key_light.scale = (3, 3, 3)
    
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 4))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 160
    fill_light.data.color = (1.0, 0.9, 0.95)
    fill_light.scale = (3, 3, 3)
    
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 3))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 200
    rim_light.data.color = (0.85, 0.9, 1.0)
    rim_light.scale = (4, 4, 4)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4, 1.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(75), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Sculpted Pikachu created successfully!")
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
    create_sculpted_pikachu()
    
    output_path = "/home/freeman/.openclaw/workspace/gengar-project/pikachu_sculpted.glb"
    export_gltf(output_path)
    print("Done!")
