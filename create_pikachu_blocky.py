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

def create_blocky_pikachu():
    """Create a Minecraft-style blocky Pikachu"""
    
    # Colors
    yellow = (0.98, 0.88, 0.15, 1.0)
    brown = (0.42, 0.28, 0.16, 1.0)
    red = (0.92, 0.18, 0.12, 1.0)
    black = (0.03, 0.03, 0.03, 1.0)
    white = (0.98, 0.98, 0.98, 1.0)
    
    yellow_mat = create_material("Yellow", yellow)
    brown_mat = create_material("Brown", brown)
    red_mat = create_material("Red", red)
    black_mat = create_material("Black", black)
    white_mat = create_material("White", white)
    
    block_size = 0.25
    
    # === BODY (Pear shape - wider at bottom) ===
    body_blocks = [
        # Lower body (wider)
        (0, 0, -0.5), (0.25, 0, -0.5), (-0.25, 0, -0.5),
        (0, 0.25, -0.5), (0, -0.25, -0.5),
        (0.25, 0.25, -0.5), (0.25, -0.25, -0.5), (-0.25, 0.25, -0.5), (-0.25, -0.25, -0.5),
        # Mid body
        (0, 0, -0.25), (0.25, 0, -0.25), (-0.25, 0, -0.25),
        (0, 0.25, -0.25), (0, -0.25, -0.25),
        # Upper body
        (0, 0, 0), (0.25, 0, 0), (-0.25, 0, 0),
        (0, 0.25, 0), (0, -0.25, 0),
        # Chest
        (0, 0, 0.25), (0.25, 0, 0.25), (-0.25, 0, 0.25),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", block_size, pos, yellow_mat)
    
    # === HEAD (Larger than body) ===
    head_blocks = [
        # Lower head
        (0, 0, 0.7), (0.25, 0, 0.7), (-0.25, 0, 0.7),
        (0, 0.25, 0.7), (0, -0.25, 0.7),
        (0.25, 0.25, 0.7), (0.25, -0.25, 0.7), (-0.25, 0.25, 0.7), (-0.25, -0.25, 0.7),
        # Mid head
        (0, 0, 0.95), (0.25, 0, 0.95), (-0.25, 0, 0.95),
        (0, 0.25, 0.95), (0, -0.25, 0.95),
        (0.25, 0.25, 0.95), (0.25, -0.25, 0.95), (-0.25, 0.25, 0.95), (-0.25, -0.25, 0.95),
        # Upper head
        (0, 0, 1.2), (0.25, 0, 1.2), (-0.25, 0, 1.2),
        (0, 0.25, 1.2), (0, -0.25, 1.2),
        # Top
        (0, 0, 1.45), (0.25, 0, 1.45), (-0.25, 0, 1.45),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", block_size, pos, yellow_mat)
    
    # === EARS (Long blocky ears) ===
    # Left ear
    left_ear = [
        (-0.5, 0, 1.7), (-0.7, 0.05, 1.9), (-0.9, 0.1, 2.1),
        (-1.1, 0.15, 2.3), (-1.3, 0.2, 2.5), (-1.5, 0.25, 2.7),
    ]
    for i, pos in enumerate(left_ear):
        create_box(f"LeftEar_{i}", block_size * 0.8, pos, yellow_mat)
    
    # Left ear tip (black)
    create_box("LeftEarTip", block_size * 0.7, (-1.65, 0.3, 2.85), black_mat)
    
    # Right ear
    right_ear = [
        (0.5, 0, 1.7), (0.7, 0.05, 1.9), (0.9, 0.1, 2.1),
        (1.1, 0.15, 2.3), (1.3, 0.2, 2.5), (1.5, 0.25, 2.7),
    ]
    for i, pos in enumerate(right_ear):
        create_box(f"RightEar_{i}", block_size * 0.8, pos, yellow_mat)
    
    # Right ear tip (black)
    create_box("RightEarTip", block_size * 0.7, (1.65, 0.3, 2.85), black_mat)
    
    # === ARMS (Short stubby blocks) ===
    # Left arm
    left_arm = [(-0.6, 0.1, 0.1), (-0.85, 0.15, 0.3)]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", block_size * 0.7, pos, yellow_mat)
    
    # Right arm
    right_arm = [(0.6, 0.1, 0.1), (0.85, 0.15, 0.3)]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", block_size * 0.7, pos, yellow_mat)
    
    # === FEET (Small blocks) ===
    # Left foot
    left_foot = [(-0.4, 0.2, -0.75), (-0.4, 0.4, -0.95)]
    for i, pos in enumerate(left_foot):
        create_box(f"LeftFoot_{i}", block_size * 0.7, pos, yellow_mat)
    
    # Right foot
    right_foot = [(0.4, 0.2, -0.75), (0.4, 0.4, -0.95)]
    for i, pos in enumerate(right_foot):
        create_box(f"RightFoot_{i}", block_size * 0.7, pos, yellow_mat)
    
    # === TAIL (Lightning bolt shape with blocks) ===
    tail = [
        (0, -0.5, -0.25), (0, -0.7, -0.1), (0, -0.85, 0.1),
        (0, -0.95, 0.35), (0, -1.05, 0.6), (0, -1.15, 0.9),
    ]
    for i, pos in enumerate(tail):
        create_box(f"Tail_{i}", block_size * 0.7, pos, yellow_mat)
    
    # === CHEEKS (Red squares) ===
    create_box("LeftCheek", block_size * 0.6, (-0.35, 0.35, 0.85), red_mat)
    create_box("RightCheek", block_size * 0.6, (0.35, 0.35, 0.85), red_mat)
    
    # === EYES (Black blocks) ===
    create_box("LeftEye", block_size * 0.45, (-0.25, 0.25, 1.1), black_mat)
    create_box("RightEye", block_size * 0.45, (0.25, 0.25, 1.1), black_mat)
    
    # === EYE HIGHLIGHTS (Tiny white blocks) ===
    create_box("LeftHighlight", block_size * 0.2, (-0.2, 0.28, 1.15), white_mat)
    create_box("RightHighlight", block_size * 0.2, (0.3, 0.28, 1.15), white_mat)
    
    # === NOSE (Tiny black block) ===
    create_box("Nose", block_size * 0.25, (0, 0.38, 0.95), black_mat)
    
    # === MOUTH (Small curved black blocks) ===
    create_box("Mouth", block_size * 0.3, (0, 0.4, 0.85), black_mat)
    create_box("MouthLeft", block_size * 0.2, (-0.15, 0.38, 0.87), black_mat)
    create_box("MouthRight", block_size * 0.2, (0.15, 0.38, 0.87), black_mat)
    
    # === BODY STRIPES (Brown blocks on back) ===
    create_box("Stripe1", block_size * 0.5, (0, -0.4, -0.25), brown_mat)
    create_box("Stripe2", block_size * 0.45, (0, -0.45, -0.5), brown_mat)
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3
    sun.data.color = (1.0, 0.98, 0.95)
    
    bpy.ops.object.light_add(type='SUN', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.data.energy = 2
    fill.data.color = (0.95, 0.95, 1.0)
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.object.camera_add(location=(0, -5, 1.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(70), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Blocky Pikachu created!")
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
    create_blocky_pikachu()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/pikachu.glb")
    print("Done!")
