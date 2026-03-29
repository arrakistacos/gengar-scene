import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_box(name, size, location, material=None):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def create_refined_gengar():
    """Refined Gengar based on official Sugimori art"""
    
    purple = (0.42, 0.22, 0.52, 1.0)
    dark_purple = (0.18, 0.12, 0.28, 1.0)
    red = (0.9, 0.08, 0.12, 1.0)
    white = (0.95, 0.95, 0.95, 1.0)
    pink = (0.95, 0.4, 0.6, 1.0)
    black = (0.02, 0.02, 0.02, 1.0)
    
    purple_mat = create_material("Purple", purple)
    dark_purple_mat = create_material("DarkPurple", dark_purple)
    red_mat = create_material("Red", red)
    white_mat = create_material("White", white)
    pink_mat = create_material("Pink", pink)
    black_mat = create_material("Black", black)
    
    # === REFINEMENT 1: BODY - More spherical/round ===
    # Core round body (Sugimori Gengar is very round)
    body_blocks = [
        # Center mass - very round
        (0, 0, 0), (0.25, 0, 0), (-0.25, 0, 0),
        (0, 0.25, 0), (0, -0.25, 0),
        (0.25, 0.25, 0), (0.25, -0.25, 0), (-0.25, 0.25, 0), (-0.25, -0.25, 0),
        # Upper body (merges with head)
        (0, 0, 0.35), (0.25, 0, 0.35), (-0.25, 0, 0.35),
        (0, 0.25, 0.35), (0, -0.25, 0.35),
        (0.25, 0.25, 0.35), (0.25, -0.25, 0.35), (-0.25, 0.25, 0.35), (-0.25, -0.25, 0.35),
        # Lower body (wider base)
        (0, 0, -0.35), (0.25, 0, -0.35), (-0.25, 0, -0.35),
        (0, 0.25, -0.35), (0, -0.25, -0.35),
        (0.25, 0.25, -0.35), (0.25, -0.25, -0.35), (-0.25, 0.25, -0.35), (-0.25, -0.25, -0.35),
        # Bottom
        (0, 0, -0.6), (0.2, 0, -0.6), (-0.2, 0, -0.6),
        (0, 0.2, -0.6), (0, -0.2, -0.6),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.28, pos, purple_mat)
    
    # === REFINEMENT 2: HEAD - Large, merges with body ===
    head_blocks = [
        # Large round head
        (0, 0, 0.75), (0.25, 0, 0.75), (-0.25, 0, 0.75),
        (0, 0.25, 0.75), (0, -0.25, 0.75),
        (0.25, 0.25, 0.75), (0.25, -0.25, 0.75), (-0.25, 0.25, 0.75), (-0.25, -0.25, 0.75),
        # Upper head
        (0, 0, 1.05), (0.25, 0, 1.05), (-0.25, 0, 1.05),
        (0, 0.25, 1.05), (0, -0.25, 1.05),
        (0.25, 0.25, 1.05), (0.25, -0.25, 1.05), (-0.25, 0.25, 1.05), (-0.25, -0.25, 1.05),
        # Top of head
        (0, 0, 1.3), (0.2, 0, 1.3), (-0.2, 0, 1.3),
        (0, 0.2, 1.3), (0, -0.2, 1.3),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.28, pos, purple_mat)
    
    # === REFINEMENT 3: EARS - Long, pointed, curving back ===
    # Left ear - curves backward
    left_ear = [
        (-0.45, 0.1, 1.55), (-0.65, 0.15, 1.8), (-0.85, 0.22, 2.05),
        (-1.05, 0.28, 2.25), (-1.2, 0.35, 2.4), (-1.35, 0.42, 2.5),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.22 - (i * 0.025)  # Tapering
        create_box(f"LeftEar_{i}", scale, pos, purple_mat)
    
    # Right ear
    right_ear = [
        (0.45, 0.1, 1.55), (0.65, 0.15, 1.8), (0.85, 0.22, 2.05),
        (1.05, 0.28, 2.25), (1.2, 0.35, 2.4), (1.35, 0.42, 2.5),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.22 - (i * 0.025)
        create_box(f"RightEar_{i}", scale, pos, purple_mat)
    
    # === REFINEMENT 4: ARMS - Short, stubby with pointed fingers ===
    # Left arm
    left_arm = [
        (-0.6, 0.1, 0.1),  # Shoulder
        (-0.85, 0.15, 0.3),  # Elbow
        (-1.05, 0.22, 0.45),  # Hand base
        (-1.2, 0.28, 0.55), (-1.25, 0.35, 0.6),  # Pointed fingers
    ]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.2, pos, purple_mat)
    
    # Right arm
    right_arm = [
        (0.6, 0.1, 0.1),
        (0.85, 0.15, 0.3),
        (1.05, 0.22, 0.45),
        (1.2, 0.28, 0.55), (1.25, 0.35, 0.6),
    ]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.2, pos, purple_mat)
    
    # === REFINEMENT 5: LEGS - Short stubs ===
    # Left leg
    left_leg = [(-0.35, 0, -0.85), (-0.35, 0.15, -1.05)]
    for i, pos in enumerate(left_leg):
        create_box(f"LeftLeg_{i}", 0.22, pos, purple_mat)
    
    # Right leg
    right_leg = [(0.35, 0, -0.85), (0.35, 0.15, -1.05)]
    for i, pos in enumerate(right_leg):
        create_box(f"RightLeg_{i}", 0.22, pos, purple_mat)
    
    # === BACK SPIKES - Spiky hair ===
    back_spikes = [
        (0, -0.45, 0.2), (0.2, -0.5, 0.1), (-0.2, -0.5, 0.1),
        (0, -0.55, 0.5), (0.15, -0.58, 0.4), (-0.15, -0.58, 0.4),
        (0, -0.5, 0.8), (0.1, -0.52, 0.75), (-0.1, -0.52, 0.75),
    ]
    for i, pos in enumerate(back_spikes):
        create_box(f"Spike_{i}", 0.15, pos, purple_mat)
    
    # === FACE - Wide grin (half the face) ===
    # Dark mouth area - takes up most of front
    mouth_blocks = [
        (0, 0.45, 0.95), (0.2, 0.45, 0.95), (-0.2, 0.45, 0.95),
        (0, 0.48, 0.75), (0.25, 0.48, 0.75), (-0.25, 0.48, 0.75),
        (0, 0.5, 0.55), (0.2, 0.5, 0.55), (-0.2, 0.5, 0.55),
    ]
    for i, pos in enumerate(mouth_blocks):
        create_box(f"Mouth_{i}", 0.25, pos, dark_purple_mat)
    
    # === TONGUE - Pink, sticking out ===
    tongue_blocks = [
        (0, 0.55, 0.45), (0, 0.58, 0.25), (0, 0.6, 0.05),
        (0, 0.62, -0.15),
    ]
    for i, pos in enumerate(tongue_blocks):
        create_box(f"Tongue_{i}", 0.18, pos, pink_mat)
    
    # === EYES - Small, red, slit pupils ===
    # Eye whites (small)
    create_box("LeftEyeWhite", 0.15, (-0.22, 0.38, 1.15), white_mat)
    create_box("RightEyeWhite", 0.15, (0.22, 0.38, 1.15), white_mat)
    
    # Red pupils
    create_box("LeftIris", 0.1, (-0.22, 0.42, 1.2), red_mat)
    create_box("RightIris", 0.1, (0.22, 0.42, 1.2), red_mat)
    
    # Black slit pupils
    create_box("LeftPupil", 0.05, (-0.22, 0.44, 1.25), black_mat)
    create_box("RightPupil", 0.05, (0.22, 0.44, 1.25), black_mat)
    
    # === TEETH - Small pointed blocks ===
    teeth_pos = [
        (-0.25, 0.52, 0.7), (-0.1, 0.54, 0.7), (0.1, 0.54, 0.7), (0.25, 0.52, 0.7),
        (-0.15, 0.55, 0.5), (0, 0.56, 0.5), (0.15, 0.55, 0.5),
    ]
    for i, pos in enumerate(teeth_pos):
        create_box(f"Tooth_{i}", 0.1, pos, white_mat)
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3
    sun.data.color = (1.0, 0.95, 1.0)
    
    bpy.ops.object.light_add(type='SUN', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.data.energy = 2
    fill.data.color = (0.9, 0.9, 1.0)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.object.camera_add(location=(0, -5, 0.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(80), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Refined Gengar (v1) created!")
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
    create_refined_gengar()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/gengar.glb")
    print("Refinement 1 complete!")
