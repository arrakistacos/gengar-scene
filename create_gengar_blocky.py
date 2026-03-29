import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.8
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_box(name, size, location, material=None):
    """Create a cube/box like Minecraft blocks"""
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def create_blocky_gengar():
    """Create a Minecraft-style blocky Gengar"""
    
    # Colors
    purple = (0.4, 0.2, 0.5, 1.0)
    dark_purple = (0.2, 0.1, 0.3, 1.0)
    red = (0.9, 0.1, 0.15, 1.0)
    white = (0.95, 0.95, 0.95, 1.0)
    pink = (0.95, 0.4, 0.6, 1.0)
    black = (0.05, 0.05, 0.05, 1.0)
    
    purple_mat = create_material("Purple", purple)
    dark_purple_mat = create_material("DarkPurple", dark_purple)
    red_mat = create_material("Red", red)
    white_mat = create_material("White", white)
    pink_mat = create_material("Pink", pink)
    black_mat = create_material("Black", black)
    
    block_size = 0.3
    
    # === MAIN BODY ===
    # Core body blocks (center mass)
    body_blocks = [
        # Center column
        (0, 0, 0), (0, 0, 1), (0, 0, -1),
        (0, 0.3, 0), (0, 0.3, 1), (0, 0.3, -1),
        (0, -0.3, 0), (0, -0.3, 1), (0, -0.3, -1),
        # Wider mid section
        (0.3, 0, 0), (0.3, 0.3, 0), (0.3, -0.3, 0),
        (-0.3, 0, 0), (-0.3, 0.3, 0), (-0.3, -0.3, 0),
        (0.3, 0, 1), (-0.3, 0, 1),
        (0.3, 0, -1), (-0.3, 0, -1),
        # Bottom wider
        (0, 0, -1.3), (0.3, 0, -1.3), (-0.3, 0, -1.3),
        (0, 0.3, -1.3), (0, -0.3, -1.3),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", block_size, pos, purple_mat)
    
    # === HEAD ===
    head_blocks = [
        (0, 0, 1.6), (0.3, 0, 1.6), (-0.3, 0, 1.6),
        (0, 0.3, 1.6), (0, -0.3, 1.6),
        (0.3, 0.3, 1.6), (0.3, -0.3, 1.6), (-0.3, 0.3, 1.6), (-0.3, -0.3, 1.6),
        (0, 0, 1.9), (0.3, 0, 1.9), (-0.3, 0, 1.9),
        (0, 0.3, 1.9), (0, -0.3, 1.9),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", block_size, pos, purple_mat)
    
    # === EARS (Blocky spikes) ===
    # Left ear
    left_ear = [
        (-0.6, 0.1, 2.2), (-0.9, 0.2, 2.5), (-1.2, 0.35, 2.8),
        (-1.4, 0.5, 3.0), (-1.5, 0.6, 3.1),
    ]
    for i, pos in enumerate(left_ear):
        create_box(f"LeftEar_{i}", block_size * 0.8, pos, purple_mat)
    
    # Right ear
    right_ear = [
        (0.6, 0.1, 2.2), (0.9, 0.2, 2.5), (1.2, 0.35, 2.8),
        (1.4, 0.5, 3.0), (1.5, 0.6, 3.1),
    ]
    for i, pos in enumerate(right_ear):
        create_box(f"RightEar_{i}", block_size * 0.8, pos, purple_mat)
    
    # === ARMS (Blocky stubs) ===
    # Left arm
    left_arm = [(-0.8, 0.1, 0.3), (-1.1, 0.15, 0.6), (-1.4, 0.2, 0.9)]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", block_size * 0.7, pos, purple_mat)
    
    # Right arm
    right_arm = [(0.8, 0.1, 0.3), (1.1, 0.15, 0.6), (1.4, 0.2, 0.9)]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", block_size * 0.7, pos, purple_mat)
    
    # === LEGS ===
    # Left leg
    left_leg = [(-0.5, 0, -1.6), (-0.5, 0.1, -1.9)]
    for i, pos in enumerate(left_leg):
        create_box(f"LeftLeg_{i}", block_size * 0.8, pos, purple_mat)
    
    # Right leg
    right_leg = [(0.5, 0, -1.6), (0.5, 0.1, -1.9)]
    for i, pos in enumerate(right_leg):
        create_box(f"RightLeg_{i}", block_size * 0.8, pos, purple_mat)
    
    # === BACK SPIKES ===
    back_spikes = [
        (0, -0.6, 0), (0, -0.9, 0.3), (0.3, -0.75, 0), (-0.3, -0.75, 0),
    ]
    for i, pos in enumerate(back_spikes):
        create_box(f"Spike_{i}", block_size * 0.6, pos, purple_mat)
    
    # === MOUTH (Dark opening) ===
    mouth_blocks = [
        (0, 0.45, 1.4), (0.2, 0.45, 1.4), (-0.2, 0.45, 1.4),
        (0, 0.5, 1.2), (0.2, 0.5, 1.2), (-0.2, 0.5, 1.2),
    ]
    for i, pos in enumerate(mouth_blocks):
        create_box(f"Mouth_{i}", block_size * 0.9, pos, dark_purple_mat)
    
    # === TONGUE (Pink block) ===
    tongue_blocks = [
        (0, 0.55, 1.0), (0, 0.6, 0.7), (0, 0.65, 0.4),
        (0, 0.7, 0.1), (0, 0.75, -0.2),
    ]
    for i, pos in enumerate(tongue_blocks):
        create_box(f"Tongue_{i}", block_size * 0.6, pos, pink_mat)
    
    # === EYES ===
    # Eye whites (slanted blocks)
    create_box("LeftEyeWhite", block_size * 0.5, (-0.3, 0.35, 1.7), white_mat)
    create_box("RightEyeWhite", block_size * 0.5, (0.3, 0.35, 1.7), white_mat)
    
    # Red pupils
    create_box("LeftIris", block_size * 0.3, (-0.3, 0.4, 1.8), red_mat)
    create_box("RightIris", block_size * 0.3, (0.3, 0.4, 1.8), red_mat)
    
    # Black pupils
    create_box("LeftPupil", block_size * 0.15, (-0.3, 0.42, 1.85), black_mat)
    create_box("RightPupil", block_size * 0.15, (0.3, 0.42, 1.85), black_mat)
    
    # === TEETH (Tiny white blocks) ===
    teeth_pos = [
        (-0.3, 0.5, 1.3), (-0.1, 0.52, 1.3), (0.1, 0.52, 1.3), (0.3, 0.5, 1.3)
    ]
    for i, pos in enumerate(teeth_pos):
        create_box(f"Tooth_{i}", block_size * 0.25, pos, white_mat)
    
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
    bpy.ops.object.camera_add(location=(0, -5, 1.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(75), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Blocky Gengar created!")
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
    create_blocky_gengar()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/gengar.glb")
    print("Done!")
