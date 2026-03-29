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

def create_pikachu_iter5():
    """Iteration 5: FINAL - Balanced proportions based on all iterations"""
    
    yellow = (0.98, 0.88, 0.15, 1.0)
    brown = (0.42, 0.28, 0.16, 1.0)
    red = (0.95, 0.15, 0.1, 1.0)
    black = (0.05, 0.05, 0.05, 1.0)
    white = (0.98, 0.98, 0.98, 1.0)
    
    yellow_mat = create_material("Yellow", yellow)
    brown_mat = create_material("Brown", brown)
    red_mat = create_material("Red", red)
    black_mat = create_material("Black", black)
    white_mat = create_material("White", white)
    
    # HEAD - balanced size
    head_blocks = [
        (0, 0, 0), (0.38, 0, 0), (-0.38, 0, 0),
        (0, 0.38, 0), (0, -0.38, 0),
        (0.38, 0.38, 0), (0.38, -0.38, 0), (-0.38, 0.38, 0), (-0.38, -0.38, 0),
        (0, 0, 0.45), (0.42, 0, 0.45), (-0.42, 0, 0.45),
        (0, 0.42, 0.45), (0, -0.42, 0.45),
        (0.42, 0.42, 0.45), (0.42, -0.42, 0.45), (-0.42, 0.42, 0.45), (-0.42, -0.42, 0.45),
        (0, 0, 0.9), (0.42, 0, 0.9), (-0.42, 0, 0.9),
        (0, 0.42, 0.9), (0, -0.42, 0.9),
        (0.42, 0.42, 0.9), (0.42, -0.42, 0.9), (-0.42, 0.42, 0.9), (-0.42, -0.42, 0.9),
        (0, 0, 1.35), (0.38, 0, 1.35), (-0.38, 0, 1.35),
        (0, 0.38, 1.35), (0, -0.38, 1.35),
    ]
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.48, pos, yellow_mat)
    
    # EARS - balanced length
    left_ear = [
        (-0.62, 0, 1.65), (-0.8, 0, 2.0), (-0.98, 0, 2.35),
        (-1.16, 0, 2.65), (-1.35, 0, 2.9), (-1.55, 0, 3.1),
        (-1.78, 0, 3.25), (-2.0, 0, 3.35), (-2.25, 0, 3.4),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.38 - (i * 0.038)
        create_box(f"LeftEar_{i}", scale, pos, yellow_mat)
    create_box("LeftEarTip", 0.19, (-2.55, 0, 3.4), black_mat)
    
    right_ear = [
        (0.62, 0, 1.65), (0.8, 0, 2.0), (0.98, 0, 2.35),
        (1.16, 0, 2.65), (1.35, 0, 2.9), (1.55, 0, 3.1),
        (1.78, 0, 3.25), (2.0, 0, 3.35), (2.25, 0, 3.4),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.38 - (i * 0.038)
        create_box(f"RightEar_{i}", scale, pos, yellow_mat)
    create_box("RightEarTip", 0.19, (2.55, 0, 3.4), black_mat)
    
    # BODY - compact
    body_blocks = [
        (0, 0, -0.55), (0.3, 0, -0.55), (-0.3, 0, -0.55),
        (0, 0.3, -0.55), (0, -0.3, -0.55),
        (0, 0, -1.05), (0.26, 0, -1.05), (-0.26, 0, -1.05),
        (0, 0.26, -1.05), (0, -0.26, -1.05),
        (0, 0, -1.5), (0.2, 0, -1.5), (-0.2, 0, -1.5),
    ]
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.42, pos, yellow_mat)
    
    # CHEEKS - perfect size
    create_box("LeftCheek", 0.38, (-0.52, 0.45, 0.45), red_mat)
    create_box("RightCheek", 0.38, (0.52, 0.45, 0.45), red_mat)
    
    # ARMS - visible
    left_arm = [(-0.75, 0.28, -0.35), (-1.08, 0.5, -0.25)]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.24, pos, yellow_mat)
    right_arm = [(0.75, 0.28, -0.35), (1.08, 0.5, -0.25)]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.24, pos, yellow_mat)
    
    # FEET
    left_foot = [(-0.38, 0.32, -1.6), (-0.38, 0.55, -1.8)]
    for i, pos in enumerate(left_foot):
        create_box(f"LeftFoot_{i}", 0.27, pos, yellow_mat)
    right_foot = [(0.38, 0.32, -1.6), (0.38, 0.55, -1.8)]
    for i, pos in enumerate(right_foot):
        create_box(f"RightFoot_{i}", 0.27, pos, yellow_mat)
    
    # LIGHTNING TAIL
    tail = [
        (0, -0.52, -1.25), (0, -0.8, -0.9), (0, -1.0, -0.45),
        (0, -1.16, 0.02), (0, -1.28, 0.52), (0, -1.38, 1.08),
        (0, -1.45, 1.65), (0, -1.5, 2.2),
    ]
    for i, pos in enumerate(tail):
        create_box(f"Tail_{i}", 0.24, pos, yellow_mat)
    
    # STRIPES
    create_box("Stripe1", 0.16, (0, -0.52, -0.85), brown_mat)
    create_box("Stripe2", 0.13, (0, -0.56, -1.25), brown_mat)
    
    # FACE - balanced
    create_box("LeftEye", 0.26, (-0.4, 0.42, 0.7), black_mat)
    create_box("RightEye", 0.26, (0.4, 0.42, 0.7), black_mat)
    create_box("LeftHighlight", 0.11, (-0.33, 0.5, 0.82), white_mat)
    create_box("RightHighlight", 0.11, (0.48, 0.5, 0.82), white_mat)
    create_box("Nose", 0.11, (0, 0.52, 0.5), black_mat)
    create_box("Mouth", 0.14, (0, 0.58, 0.22), black_mat)
    
    # LIGHTING
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
    sun = bpy.context.active_object
    sun.data.energy = 5
    
    bpy.ops.object.light_add(type='SUN', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.data.energy = 3
    
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.9, 0.9, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 0.5
    
    # CAMERA
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.object.camera_add(location=(0, -8, 0.25))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(90), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("✓ Pikachu Iteration 5 (FINAL) complete!")
    return camera

def export_and_render():
    bpy.ops.export_scene.gltf(
        filepath="/home/freeman/.openclaw/workspace/gengar-project/pikachu.glb",
        export_format='GLB',
        export_yup=True,
        export_materials='EXPORT',
        export_cameras=True,
        export_lights=True
    )
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.filepath = "/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png"
    bpy.ops.render.render(write_still=True)
    print("✓ Iteration 5 (FINAL) complete!")

if __name__ == "__main__":
    clear_scene()
    create_pikachu_iter5()
    export_and_render()
