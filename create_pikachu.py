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
    
    # Connect nodes
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_sphere(name, radius=1.0, location=(0, 0, 0), scale=(1, 1, 1)):
    """Create a sphere."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_cylinder(name, radius=0.5, depth=1.0, location=(0, 0, 0), rotation=(0, 0, 0)):
    """Create a cylinder."""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_cone(name, radius1=0.5, depth=1.0, location=(0, 0, 0), rotation=(0, 0, 0)):
    """Create a cone."""
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_pikachu():
    """Create a Pikachu Pokemon model."""
    
    # Colors (RGBA)
    yellow = (0.98, 0.85, 0.2, 1.0)  # Pikachu yellow
    dark_yellow = (0.85, 0.7, 0.1, 1.0)  # Darker yellow for stripes
    brown = (0.4, 0.25, 0.15, 1.0)  # Brown stripes
    red = (0.9, 0.15, 0.1, 1.0)  # Cheeks
    black = (0.05, 0.05, 0.05, 1.0)  # Eyes, nose, mouth
    white = (0.95, 0.95, 0.95, 1.0)  # Eye highlights
    
    # Create materials
    yellow_mat = create_material("Yellow", yellow, roughness=0.4)
    dark_yellow_mat = create_material("DarkYellow", dark_yellow, roughness=0.4)
    brown_mat = create_material("Brown", brown, roughness=0.6)
    red_mat = create_material("Red", red, roughness=0.3)
    black_mat = create_material("Black", black, roughness=0.1)
    white_mat = create_material("White", white, roughness=0.2)
    
    # === BODY ===
    # Main body (pear shape - larger at bottom)
    body = create_sphere("Pikachu_Body", radius=0.7, location=(0, 0, 0.8), scale=(1, 0.9, 1.1))
    body.data.materials.append(yellow_mat)
    
    # === HEAD ===
    # Head (larger sphere)
    head = create_sphere("Pikachu_Head", radius=0.65, location=(0, 0, 1.9), scale=(1.05, 1, 1))
    head.data.materials.append(yellow_mat)
    
    # === EARS ===
    # Left ear (long, pointed)
    left_ear = create_cone("Left_Ear", radius1=0.18, depth=1.4,
                           location=(-0.45, 0, 2.6),
                           rotation=(0, math.radians(30), math.radians(-25)))
    left_ear.data.materials.append(yellow_mat)
    
    # Left ear tip (black)
    left_ear_tip = create_cone("Left_Ear_Tip", radius1=0.18, depth=0.35,
                               location=(-0.8, 0, 3.3),
                               rotation=(0, math.radians(30), math.radians(-25)))
    left_ear_tip.data.materials.append(black_mat)
    
    # Right ear
    right_ear = create_cone("Right_Ear", radius1=0.18, depth=1.4,
                            location=(0.45, 0, 2.6),
                            rotation=(0, math.radians(-30), math.radians(25)))
    right_ear.data.materials.append(yellow_mat)
    
    # Right ear tip (black)
    right_ear_tip = create_cone("Right_Ear_Tip", radius1=0.18, depth=0.35,
                                location=(0.8, 0, 3.3),
                                rotation=(0, math.radians(-30), math.radians(25)))
    right_ear_tip.data.materials.append(black_mat)
    
    # === ARMS ===
    # Left arm (small, stubby)
    left_arm = create_sphere("Left_Arm", radius=0.22, location=(-0.5, 0.2, 1.3), scale=(0.8, 1.2, 0.8))
    left_arm.data.materials.append(yellow_mat)
    
    # Right arm
    right_arm = create_sphere("Right_Arm", radius=0.22, location=(0.5, 0.2, 1.3), scale=(0.8, 1.2, 0.8))
    right_arm.data.materials.append(yellow_mat)
    
    # === LEGS ===
    # Left leg
    left_leg = create_sphere("Left_Leg", radius=0.25, location=(-0.35, 0.1, 0.3), scale=(0.9, 1.1, 1))
    left_leg.data.materials.append(yellow_mat)
    
    # Right leg
    right_leg = create_sphere("Right_Leg", radius=0.25, location=(0.35, 0.1, 0.3), scale=(0.9, 1.1, 1))
    right_leg.data.materials.append(yellow_mat)
    
    # === FEET ===
    # Left foot
    left_foot = create_sphere("Left_Foot", radius=0.15, location=(-0.35, 0.3, 0.05), scale=(0.8, 1.5, 0.5))
    left_foot.data.materials.append(yellow_mat)
    
    # Right foot
    right_foot = create_sphere("Right_Foot", radius=0.15, location=(0.35, 0.3, 0.05), scale=(0.8, 1.5, 0.5))
    right_foot.data.materials.append(yellow_mat)
    
    # === TAIL ===
    # Tail base
    tail_base = create_sphere("Tail_Base", radius=0.25, location=(0, -0.7, 0.8), scale=(0.6, 1, 0.6))
    tail_base.data.materials.append(yellow_mat)
    
    # Middle tail section
    tail_mid = create_sphere("Tail_Mid", radius=0.2, location=(0, -0.9, 1.2), scale=(0.7, 1.2, 0.7))
    tail_mid.data.materials.append(brown_mat)
    
    # Upper tail section
    tail_upper = create_sphere("Tail_Upper", radius=0.18, location=(0, -1.0, 1.6), scale=(0.8, 1.3, 0.8))
    tail_upper.data.materials.append(yellow_mat)
    
    # Lightning bolt tip
    tail_tip = create_cone("Tail_Tip", radius1=0.35, depth=0.8,
                           location=(0, -1.1, 2.1),
                           rotation=(0, 0, math.radians(180)))
    tail_tip.data.materials.append(yellow_mat)
    tail_tip.scale = (0.6, 0.3, 1)
    
    # === FACE ===
    # Cheeks (red circles)
    left_cheek = create_sphere("Left_Cheek", radius=0.15,
                               location=(-0.35, 0.55, 1.7),
                               scale=(1, 0.5, 0.5))
    left_cheek.data.materials.append(red_mat)
    
    right_cheek = create_sphere("Right_Cheek", radius=0.15,
                                location=(0.35, 0.55, 1.7),
                                scale=(1, 0.5, 0.5))
    right_cheek.data.materials.append(red_mat)
    
    # === EYES ===
    # Eye whites (not really visible but for completeness)
    # Black eyes (typical Pikachu eyes)
    left_eye = create_sphere("Left_Eye", radius=0.12,
                             location=(-0.28, 0.35, 2.15),
                             scale=(0.8, 1, 0.3))
    left_eye.data.materials.append(black_mat)
    
    right_eye = create_sphere("Right_Eye", radius=0.12,
                              location=(0.28, 0.35, 2.15),
                              scale=(0.8, 1, 0.3))
    right_eye.data.materials.append(black_mat)
    
    # Eye highlights (small white circles)
    left_highlight = create_sphere("Left_Highlight", radius=0.04,
                                   location=(-0.24, 0.4, 2.2),
                                   scale=(1, 1, 0.5))
    left_highlight.data.materials.append(white_mat)
    
    right_highlight = create_sphere("Right_Highlight", radius=0.04,
                                    location=(0.32, 0.4, 2.2),
                                    scale=(1, 1, 0.5))
    right_highlight.data.materials.append(white_mat)
    
    # === NOSE ===
    nose = create_sphere("Nose", radius=0.03,
                         location=(0, 0.5, 2.0),
                         scale=(0.8, 0.5, 1))
    nose.data.materials.append(black_mat)
    
    # === MOUTH ===
    # Small smile
    mouth = create_sphere("Mouth", radius=0.06,
                          location=(0, 0.52, 1.85),
                          scale=(1.2, 0.3, 0.5))
    mouth.data.materials.append(black_mat)
    
    # === BODY STRIPES ===
    # Brown stripes on back
    stripe1 = create_cylinder("Stripe1", radius=0.1, depth=0.6,
                              location=(0, -0.65, 1.2),
                              rotation=(math.radians(90), 0, 0))
    stripe1.data.materials.append(brown_mat)
    
    stripe2 = create_cylinder("Stripe2", radius=0.08, depth=0.5,
                              location=(0, -0.7, 0.9),
                              rotation=(math.radians(90), 0, 0))
    stripe2.data.materials.append(brown_mat)
    
    # === LIGHTING ===
    # Remove default light
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Bright, cheerful lighting for Pikachu
    # Key light (warm yellow)
    bpy.ops.object.light_add(type='AREA', location=(3, 3, 5))
    key_light = bpy.context.active_object
    key_light.data.energy = 250
    key_light.data.color = (1.0, 0.95, 0.8)  # Warm yellow
    key_light.scale = (3, 3, 3)
    
    # Fill light (soft pink)
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 4))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 150
    fill_light.data.color = (1.0, 0.9, 0.95)  # Soft pink
    fill_light.scale = (3, 3, 3)
    
    # Rim light (blue for contrast)
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 3))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 180
    rim_light.data.color = (0.85, 0.9, 1.0)  # Light blue
    rim_light.scale = (4, 4, 4)
    
    # Bounce light from below
    bpy.ops.object.light_add(type='AREA', location=(0, 0, -2))
    bounce_light = bpy.context.active_object
    bounce_light.data.energy = 100
    bounce_light.data.color = (1.0, 0.95, 0.85)
    bounce_light.scale = (5, 5, 5)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4, 2))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(75), 0, math.radians(180))
    
    bpy.context.scene.camera = camera
    
    print("Pikachu created successfully!")
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
    create_pikachu()
    
    # Export to GLTF
    output_path = "/home/freeman/.openclaw/workspace/gengar-project/pikachu.glb"
    export_gltf(output_path)
    
    print("Done!")