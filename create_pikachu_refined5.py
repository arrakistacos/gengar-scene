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

def create_refined_pikachu_v5():
    """Final refined Pikachu after 5 iterations based on official art"""
    
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
    
    block_size = 0.22
    
    # === FINAL BODY: Pear shape, compact ===
    body_blocks = [
        # Lower body (wider)
        (0, 0, -0.4), (0.22, 0, -0.4), (-0.22, 0, -0.4),
        (0, 0.22, -0.4), (0, -0.22, -0.4),
        (0.22, 0.22, -0.4), (0.22, -0.22, -0.4), (-0.22, 0.22, -0.4), (-0.22, -0.22, -0.4),
        # Mid body
        (0, 0, -0.15), (0.22, 0, -0.15), (-0.22, 0, -0.15),
        (0, 0.22, -0.15), (0, -0.22, -0.15),
        # Upper body
        (0, 0, 0.1), (0.2, 0, 0.1), (-0.2, 0, 0.1),
        (0, 0.2, 0.1), (0, -0.2, 0.1),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", block_size, pos, yellow_mat)
    
    # === FINAL HEAD: Very large, 40% of height ===
    head_blocks = [
        # Lower head
        (0, 0, 0.45), (0.25, 0, 0.45), (-0.25, 0, 0.45),
        (0, 0.25, 0.45), (0, -0.25, 0.45),
        (0.25, 0.25, 0.45), (0.25, -0.25, 0.45), (-0.25, 0.25, 0.45), (-0.25, -0.25, 0.45),
        # Mid head
        (0, 0, 0.75), (0.28, 0, 0.75), (-0.28, 0, 0.75),
        (0, 0.28, 0.75), (0, -0.28, 0.75),
        (0.28, 0.28, 0.75), (0.28, -0.28, 0.75), (-0.28, 0.28, 0.75), (-0.28, -0.28, 0.75),
        # Upper head
        (0, 0, 1.05), (0.28, 0, 1.05), (-0.28, 0, 1.05),
        (0, 0.28, 1.05), (0, -0.28, 1.05),
        (0.28, 0.28, 1.05), (0.28, -0.28, 1.05), (-0.28, 0.28, 1.05), (-0.28, -0.28, 1.05),
        # Top
        (0, 0, 1.35), (0.25, 0, 1.35), (-0.25, 0, 1.35),
        (0, 0.25, 1.35), (0, -0.25, 1.35),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", block_size * 1.1, pos, yellow_mat)
    
    # === FINAL EARS: Long, tall, black tips ===
    # Left ear - extends above head
    left_ear = [
        (-0.45, 0, 1.6), (-0.6, 0, 1.85), (-0.75, 0, 2.1),
        (-0.9, 0, 2.35), (-1.05, 0, 2.6), (-1.2, 0, 2.85),
        (-1.35, 0, 3.1), (-1.5, 0, 3.35),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.2 - (i * 0.015)
        create_box(f"LeftEar_{i}", scale, pos, yellow_mat)
    
    # Left ear tip (black)
    create_box("LeftEarTip", 0.16, (-1.65, 0, 3.6), black_mat)
    
    # Right ear
    right_ear = [
        (0.45, 0, 1.6), (0.6, 0, 1.85), (0.75, 0, 2.1),
        (0.9, 0, 2.35), (1.05, 0, 2.6), (1.2, 0, 2.85),
        (1.35, 0, 3.1), (1.5, 0, 3.35),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.2 - (i * 0.015)
        create_box(f"RightEar_{i}", scale, pos, yellow_mat)
    
    # Right ear tip (black)
    create_box("RightEarTip", 0.16, (1.65, 0, 3.6), black_mat)
    
    # === ARMS: Short stubs ===
    left_arm = [(-0.55, 0.1, 0), (-0.78, 0.2, 0.1)]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.18, pos, yellow_mat)
    
    right_arm = [(0.55, 0.1, 0), (0.78, 0.2, 0.1)]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.18, pos, yellow_mat)
    
    # === FEET: Small and round ===
    left_foot = [(-0.35, 0.15, -0.65), (-0.35, 0.3, -0.85)]
    for i, pos in enumerate(left_foot):
        create_box(f"LeftFoot_{i}", 0.18, pos, yellow_mat)
    
    right_foot = [(0.35, 0.15, -0.65), (0.35, 0.3, -0.85)]
    for i, pos in enumerate(right_foot):
        create_box(f"RightFoot_{i}", 0.18, pos, yellow_mat)
    
    # === TAIL: Lightning bolt shape ===
    tail = [
        (0, -0.35, -0.35), (0, -0.5, -0.2), (0, -0.65, 0),
        (0, -0.78, 0.25), (0, -0.88, 0.55), (0, -0.95, 0.9),
        (0, -1.0, 1.25), (0, -1.05, 1.6),
    ]
    for i, pos in enumerate(tail):
        create_box(f"Tail_{i}", 0.16, pos, yellow_mat)
    
    # === CHEEKS: Large red circles ===
    create_box("LeftCheek", 0.22, (-0.38, 0.32, 0.65), red_mat)
    create_box("RightCheek", 0.22, (0.38, 0.32, 0.65), red_mat)
    
    # === EYES: Black, ovular, with highlights ===
    create_box("LeftEye", 0.14, (-0.22, 0.22, 0.92), black_mat)
    create_box("RightEye", 0.14, (0.22, 0.22, 0.92), black_mat)
    
    # Eye highlights
    create_box("LeftHighlight", 0.06, (-0.18, 0.26, 0.98), white_mat)
    create_box("RightHighlight", 0.06, (0.26, 0.26, 0.98), white_mat)
    
    # === NOSE: Tiny black dot ===
    create_box("Nose", 0.06, (0, 0.32, 0.78), black_mat)
    
    # === MOUTH: Small smile ===
    create_box("Mouth", 0.08, (0, 0.35, 0.7), black_mat)
    create_box("MouthLeft", 0.05, (-0.08, 0.33, 0.72), black_mat)
    create_box("MouthRight", 0.05, (0.08, 0.33, 0.72), black_mat)
    
    # === BODY STRIPES: Brown horizontal ===
    create_box("Stripe1", 0.12, (0, -0.35, -0.15), brown_mat)
    create_box("Stripe2", 0.1, (0, -0.4, -0.4), brown_mat)
    
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
    bpy.ops.object.camera_add(location=(0, -5, 0.8))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(75), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Refined Pikachu (v5 FINAL) created!")
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
    create_refined_pikachu_v5()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/pikachu.glb")
    print("Pikachu refinement 5 (FINAL) complete!")
