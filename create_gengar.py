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
        bsdf.inputs['Subsurface Weight'].default_value = subsurface
        # Subsurface color is typically Base Color in newer Blender versions
    
    # Connect nodes
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_rounded_cube(name, radius=1.0, location=(0, 0, 0), scale=(1, 1, 1)):
    """Create a rounded cube using subdivision modifier."""
    bpy.ops.mesh.primitive_cube_add(size=2*radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    
    # Add subdivision surface modifier
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURFACE')
    subsurf.levels = 3
    subsurf.render_levels = 4
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_sphere(name, radius=1.0, location=(0, 0, 0), scale=(1, 1, 1)):
    """Create a sphere."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_cone(name, radius=0.5, depth=1.0, location=(0, 0, 0), rotation=(0, 0, 0)):
    """Create a cone for ears/spikes."""
    bpy.ops.mesh.primitive_cone_add(radius1=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    
    # Shade smooth
    bpy.ops.object.shade_smooth()
    
    return obj

def create_gengar():
    """Create a Gengar Pokemon model."""
    
    # Colors (RGBA)
    purple = (0.4, 0.2, 0.5, 1.0)  # Main body purple
    dark_purple = (0.25, 0.15, 0.35, 1.0)  # Darker for inner mouth
    red = (0.9, 0.1, 0.15, 1.0)  # Eyes
    white = (0.95, 0.95, 0.95, 1.0)  # Eyes sclera/teeth
    pink = (0.95, 0.4, 0.6, 1.0)  # Tongue
    black = (0.05, 0.05, 0.05, 1.0)  # Pupils
    
    # Create materials
    purple_mat = create_material("Purple", purple, roughness=0.3)
    dark_purple_mat = create_material("DarkPurple", dark_purple, roughness=0.4)
    red_mat = create_material("Red", red, roughness=0.2, subsurface=0.1)
    white_mat = create_material("White", white, roughness=0.2)
    pink_mat = create_material("Pink", pink, roughness=0.3, subsurface=0.2)
    black_mat = create_material("Black", black, roughness=0.1)
    
    # === MAIN BODY ===
    # Create main body (slightly flattened sphere)
    body = create_sphere("Gengar_Body", radius=1.0, location=(0, 0, 1.2), scale=(1, 0.85, 1))
    body.data.materials.append(purple_mat)
    
    # === SPIKES/EARS ===
    # Left ear (spike)
    left_ear = create_cone("Left_Ear", radius=0.35, depth=1.2, 
                           location=(-0.6, 0.3, 1.9), 
                           rotation=(math.radians(-30), 0, math.radians(-40)))
    left_ear.data.materials.append(purple_mat)
    
    # Right ear (spike)
    right_ear = create_cone("Right_Ear", radius=0.35, depth=1.2,
                            location=(0.6, 0.3, 1.9),
                            rotation=(math.radians(-30), 0, math.radians(40)))
    right_ear.data.materials.append(purple_mat)
    
    # Back spikes (smaller cones on back)
    back_spike1 = create_cone("Back_Spike1", radius=0.25, depth=0.8,
                              location=(0, -0.9, 1.5),
                              rotation=(math.radians(60), 0, 0))
    back_spike1.data.materials.append(purple_mat)
    
    # === ARMS ===
    # Left arm (curved, going up)
    left_arm = create_sphere("Left_Arm", radius=0.35, location=(-0.9, 0.1, 0.8), scale=(0.8, 0.5, 1.2))
    left_arm.data.materials.append(purple_mat)
    
    # Right arm
    right_arm = create_sphere("Right_Arm", radius=0.35, location=(0.9, 0.1, 0.8), scale=(0.8, 0.5, 1.2))
    right_arm.data.materials.append(purple_mat)
    
    # Left hand (pointed)
    left_hand = create_cone("Left_Hand", radius=0.25, depth=0.6,
                            location=(-1.3, 0.1, 1.4),
                            rotation=(0, math.radians(40), 0))
    left_hand.data.materials.append(purple_mat)
    
    # Right hand
    right_hand = create_cone("Right_Hand", radius=0.25, depth=0.6,
                             location=(1.3, 0.1, 1.4),
                             rotation=(0, math.radians(-40), 0))
    right_hand.data.materials.append(purple_mat)
    
    # === LEGS ===
    # Left leg (stubby)
    left_leg = create_sphere("Left_Leg", radius=0.3, location=(-0.4, -0.1, 0.3), scale=(0.7, 0.8, 1.2))
    left_leg.data.materials.append(purple_mat)
    
    # Right leg
    right_leg = create_sphere("Right_Leg", radius=0.3, location=(0.4, -0.1, 0.3), scale=(0.7, 0.8, 1.2))
    right_leg.data.materials.append(purple_mat)
    
    # === FACE ===
    # Create the face area with mouth and eyes
    # Main mouth (dark opening)
    mouth = create_sphere("Mouth", radius=0.45, location=(0, 0.75, 1.1), scale=(1.2, 0.4, 0.8))
    mouth.data.materials.append(dark_purple_mat)
    
    # === TONGUE (THE KEY FEATURE!) ===
    # Main tongue body (curved, sticking out)
    tongue_main = create_sphere("Tongue_Main", radius=0.25, 
                                 location=(0, 0.85, 1.0), 
                                 scale=(0.6, 0.3, 1.8))
    tongue_main.rotation_euler = (math.radians(20), 0, 0)
    tongue_main.data.materials.append(pink_mat)
    
    # Tongue tip (slightly larger)
    tongue_tip = create_sphere("Tongue_Tip", radius=0.28,
                               location=(0, 1.0, 0.4),
                               scale=(0.7, 0.35, 0.6))
    tongue_tip.data.materials.append(pink_mat)
    
    # === EYES ===
    # Eye whites (large, ovular)
    left_eye_white = create_sphere("Left_Eye_White", radius=0.22,
                                   location=(-0.35, 0.6, 1.35),
                                   scale=(0.5, 0.3, 1.2))
    left_eye_white.data.materials.append(white_mat)
    
    right_eye_white = create_sphere("Right_Eye_White", radius=0.22,
                                    location=(0.35, 0.6, 1.35),
                                    scale=(0.5, 0.3, 1.2))
    right_eye_white.data.materials.append(white_mat)
    
    # Red irises
    left_iris = create_sphere("Left_Iris", radius=0.12,
                              location=(-0.35, 0.62, 1.45),
                              scale=(0.8, 0.8, 0.5))
    left_iris.data.materials.append(red_mat)
    
    right_iris = create_sphere("Right_Iris", radius=0.12,
                               location=(0.35, 0.62, 1.45),
                               scale=(0.8, 0.8, 0.5))
    right_iris.data.materials.append(red_mat)
    
    # Black pupils (small, menacing)
    left_pupil = create_sphere("Left_Pupil", radius=0.06,
                               location=(-0.35, 0.63, 1.52),
                               scale=(1, 1, 0.5))
    left_pupil.data.materials.append(black_mat)
    
    right_pupil = create_sphere("Right_Pupil", radius=0.06,
                                location=(0.35, 0.63, 1.52),
                                scale=(1, 1, 0.5))
    right_pupil.data.materials.append(black_mat)
    
    # === TEETH ===
    # Small pointed teeth
    for i in range(4):
        x_pos = -0.25 + (i * 0.17)
        tooth = create_cone(f"Tooth_{i}", radius=0.05, depth=0.15,
                          location=(x_pos, 0.82, 1.25),
                          rotation=(math.radians(-10), 0, 0))
        tooth.data.materials.append(white_mat)
    
    # === LIGHTING ===
    # Remove default light
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Add three-point lighting (pastel style)
    # Key light (soft purple tint)
    bpy.ops.object.light_add(type='AREA', location=(3, 2, 4))
    key_light = bpy.context.active_object
    key_light.data.energy = 200
    key_light.data.color = (1.0, 0.9, 1.0)  # Slight purple tint
    key_light.scale = (2, 2, 2)
    
    # Fill light (warm pink)
    bpy.ops.object.light_add(type='AREA', location=(-3, 1, 3))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 100
    fill_light.data.color = (1.0, 0.85, 0.9)  # Pink tint
    fill_light.scale = (2, 2, 2)
    
    # Back light (cyan rim light for spooky effect)
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 2))
    back_light = bpy.context.active_object
    back_light.data.energy = 150
    back_light.data.color = (0.8, 0.9, 1.0)  # Cyan tint
    back_light.scale = (3, 3, 3)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    
    bpy.ops.object.camera_add(location=(0, -4, 1.2))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(90), 0, math.radians(180))
    
    bpy.context.scene.camera = camera
    
    # Set viewport to camera view
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.region_3d.view_perspective = 'CAMERA'
    
    print("Gengar created successfully!")
    return camera

def export_gltf(filepath):
    """Export the scene as GLTF."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',  # Single binary file
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
    create_gengar()
    
    # Export to GLTF
    output_path = "/home/freeman/.openclaw/workspace/gengar-project/gengar.glb"
    export_gltf(output_path)
    
    print("Done!")