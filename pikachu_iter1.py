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

def create_pikachu_iter1():
    """Iteration 1: Based on Google description
    - Yellow rodent
    - Large head, small body  
    - Pointy ears with black tips
    - Red circles on cheeks
    - Lightning bolt tail
    - Brown stripes on back
    - Small arms and feet
    """
    
    # Colors
    yellow = (0.98, 0.88, 0.15, 1.0)
    brown = (0.42, 0.28, 0.16, 1.0)
    red = (0.92, 0.18, 0.12, 1.0)
    black = (0.08, 0.08, 0.08, 1.0)
    white = (0.98, 0.98, 0.98, 1.0)
    
    yellow_mat = create_material("Yellow", yellow)
    brown_mat = create_material("Brown", brown)
    red_mat = create_material("Red", red)
    black_mat = create_material("Black", black)
    white_mat = create_material("White", white)
    
    # LARGE HEAD (40% of height)
    head_blocks = [
        # Lower head
        (0, 0, 0.4), (0.3, 0, 0.4), (-0.3, 0, 0.4),
        (0, 0.3, 0.4), (0, -0.3, 0.4),
        (0.3, 0.3, 0.4), (0.3, -0.3, 0.4), (-0.3, 0.3, 0.4), (-0.3, -0.3, 0.4),
        # Mid head
        (0, 0, 0.8), (0.35, 0, 0.8), (-0.35, 0, 0.8),
        (0, 0.35, 0.8), (0, -0.35, 0.8),
        (0.35, 0.35, 0.8), (0.35, -0.35, 0.8), (-0.35, 0.35, 0.8), (-0.35, -0.35, 0.8),
        # Upper head
        (0, 0, 1.2), (0.35, 0, 1.2), (-0.35, 0, 1.2),
        (0, 0.35, 1.2), (0, -0.35, 1.2),
        (0.35, 0.35, 1.2), (0.35, -0.35, 1.2), (-0.35, 0.35, 1.2), (-0.35, -0.35, 1.2),
        # Top
        (0, 0, 1.6), (0.3, 0, 1.6), (-0.3, 0, 1.6),
        (0, 0.3, 1.6), (0, -0.3, 1.6),
    ]
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.4, pos, yellow_mat)
    
    # POINTY EARS with black tips
    # Left ear
    left_ear = [
        (-0.55, 0, 1.85), (-0.7, 0, 2.2), (-0.85, 0, 2.55),
        (-1.0, 0, 2.85), (-1.15, 0, 3.1), (-1.3, 0, 3.3),
        (-1.45, 0, 3.45), (-1.6, 0, 3.55),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.3 - (i * 0.03)
        create_box(f"LeftEar_{i}", scale, pos, yellow_mat)
    # Black tip
    create_box("LeftEarTip", 0.15, (-1.75, 0, 3.65), black_mat)
    
    # Right ear
    right_ear = [
        (0.55, 0, 1.85), (0.7, 0, 2.2), (0.85, 0, 2.55),
        (1.0, 0, 2.85), (1.15, 0, 3.1), (1.3, 0, 3.3),
        (1.45, 0, 3.45), (1.6, 0, 3.55),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.3 - (i * 0.03)
        create_box(f"RightEar_{i}", scale, pos, yellow_mat)
    # Black tip
    create_box("RightEarTip", 0.15, (1.75, 0, 3.65), black_mat)
    
    # SMALL BODY (pear shape, narrower than head)
    body_blocks = [
        (0, 0, 0), (0.25, 0, 0), (-0.25, 0, 0),
        (0, 0.25, 0), (0, -0.25, 0),
        (0, 0, -0.4), (0.25, 0, -0.4), (-0.25, 0, -0.4),
        (0, 0.25, -0.4), (0, -0.25, -0.4),
        (0, 0, -0.8), (0.22, 0, -0.8), (-0.22, 0, -0.8),
        (0, 0.22, -0.8), (0, -0.22, -0.8),
    ]
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.35, pos, yellow_mat)
    
    # RED CHEEKS (circular, prominent)
    create_box("LeftCheek", 0.28, (-0.45, 0.38, 0.9), red_mat)
    create_box("RightCheek", 0.28, (0.45, 0.38, 0.9), red_mat)
    
    # SMALL ARMS
    left_arm = [(-0.6, 0.15, 0), (-0.85, 0.35, 0.1)]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.18, pos, yellow_mat)
    
    right_arm = [(0.6, 0.15, 0), (0.85, 0.35, 0.1)]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.18, pos, yellow_mat)
    
    # SMALL FEET
    left_foot = [(-0.35, 0.2, -1.0), (-0.35, 0.35, -1.2)]
    for i, pos in enumerate(left_foot):
        create_box(f"LeftFoot_{i}", 0.2, pos, yellow_mat)
    
    right_foot = [(0.35, 0.2, -1.0), (0.35, 0.35, -1.2)]
    for i, pos in enumerate(right_foot):
        create_box(f"RightFoot_{i}", 0.2, pos, yellow_mat)
    
    # LIGHTNING BOLT TAIL (zigzag shape going up)
    tail = [
        (0, -0.45, -0.5), (0, -0.7, -0.3), (0, -0.9, 0),
        (0, -1.05, 0.4), (0, -1.15, 0.85), (0, -1.2, 1.35),
        (0, -1.25, 1.9), (0, -1.3, 2.4),
    ]
    for i, pos in enumerate(tail):
        create_box(f"Tail_{i}", 0.18, pos, yellow_mat)
    
    # BROWN STRIPES on back
    create_box("Stripe1", 0.12, (0, -0.42, -0.2), brown_mat)
    create_box("Stripe2", 0.1, (0, -0.48, -0.55), brown_mat)
    
    # FACE - Black eyes with white highlights
    create_box("LeftEye", 0.18, (-0.28, 0.35, 1.1), black_mat)
    create_box("RightEye", 0.18, (0.28, 0.35, 1.1), black_mat)
    create_box("LeftHighlight", 0.08, (-0.24, 0.4, 1.18), white_mat)
    create_box("RightHighlight", 0.08, (0.32, 0.4, 1.18), white_mat)
    
    # Small nose and mouth
    create_box("Nose", 0.08, (0, 0.42, 0.95), black_mat)
    create_box("Mouth", 0.1, (0, 0.45, 0.75), black_mat)
    
    # === LIGHTING ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Bright studio lighting
    bpy.ops.object.light_add(type='AREA', location=(0, -8, 4))
    key = bpy.context.active_object
    key.data.energy = 2000
    key.data.size = 12
    key.rotation_euler = (math.radians(70), 0, 0)
    
    # Fill from left
    bpy.ops.object.light_add(type='AREA', location=(-8, -4, 3))
    fill = bpy.context.active_object
    fill.data.energy = 1000
    fill.data.size = 10
    fill.rotation_euler = (math.radians(45), 0, math.radians(30))
    
    # White background
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.95, 0.95, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 0.6
    
    # === CAMERA ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.object.camera_add(location=(0, -7, 0.8))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(82), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("✓ Pikachu Iteration 1 created!")
    return camera

def export_and_render():
    # Export
    bpy.ops.export_scene.gltf(
        filepath="/home/freeman/.openclaw/workspace/gengar-project/pikachu.glb",
        export_format='GLB',
        export_yup=True,
        export_materials='EXPORT',
        export_cameras=True,
        export_lights=True
    )
    print("Exported pikachu.glb")
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.filepath = "/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter1.png"
    scene.render.image_settings.file_format = 'PNG'
    
    bpy.ops.render.render(write_still=True)
    print("Rendered to pikachu_iter1.png")

if __name__ == "__main__":
    clear_scene()
    create_pikachu_iter1()
    export_and_render()
    print("\n✓ Iteration 1 complete!")
