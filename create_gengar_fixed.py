import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_material(name, color, roughness=0.5, emission=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    
    # Add emission for glow/better visibility
    if emission > 0:
        # In newer Blender, Emission is a socket on the BSDF
        if 'Emission' in bsdf.inputs:
            bsdf.inputs['Emission'].default_value = (*color[:3], emission)
        elif 'Emission Strength' in bsdf.inputs:
            # Try different naming
            bsdf.inputs['Emission Strength'].default_value = emission
    
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_box(name, size, location, material=None):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def create_gengar_fixed():
    """Gengar with proper lighting and camera setup"""
    
    # Brighter colors for visibility
    purple = (0.55, 0.3, 0.7, 1.0)  # Lighter purple
    dark_purple = (0.3, 0.18, 0.45, 1.0)  # Darker but not black
    red = (0.95, 0.15, 0.15, 1.0)  # Bright red
    white = (0.98, 0.98, 0.98, 1.0)
    pink = (0.98, 0.5, 0.7, 1.0)
    black = (0.1, 0.1, 0.1, 1.0)  # Not pure black
    
    purple_mat = create_material("Purple", purple)
    dark_purple_mat = create_material("DarkPurple", dark_purple)
    red_mat = create_material("Red", red)  # Bright color
    white_mat = create_material("White", white)
    pink_mat = create_material("Pink", pink)
    black_mat = create_material("Black", black)
    
    # BODY - wider, rounder
    body_blocks = [
        (0, 0, -0.2), (0.35, 0, -0.2), (-0.35, 0, -0.2),
        (0, 0.3, -0.2), (0, -0.3, -0.2),
        (0.35, 0.3, -0.2), (0.35, -0.3, -0.2), (-0.35, 0.3, -0.2), (-0.35, -0.3, -0.2),
        (0, 0, -0.55), (0.32, 0, -0.55), (-0.32, 0, -0.55),
        (0, 0.3, -0.55), (0, -0.3, -0.55),
        (0, 0, -0.85), (0.28, 0, -0.85), (-0.28, 0, -0.85),
    ]
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.35, pos, purple_mat)
    
    # HEAD - massive
    head_blocks = [
        (0, 0, 0.2), (0.4, 0, 0.2), (-0.4, 0, 0.2),
        (0, 0.38, 0.2), (0, -0.38, 0.2),
        (0.4, 0.38, 0.2), (0.4, -0.38, 0.2), (-0.4, 0.38, 0.2), (-0.4, -0.38, 0.2),
        (0, 0, 0.6), (0.4, 0, 0.6), (-0.4, 0, 0.6),
        (0, 0.38, 0.6), (0, -0.38, 0.6),
        (0.4, 0.38, 0.6), (0.4, -0.38, 0.6), (-0.4, 0.38, 0.6), (-0.4, -0.38, 0.6),
        (0, 0, 1.0), (0.4, 0, 1.0), (-0.4, 0, 1.0),
        (0, 0.38, 1.0), (0, -0.38, 1.0),
        (0, 0, 1.35), (0.35, 0, 1.35), (-0.35, 0, 1.35),
    ]
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.4, pos, purple_mat)
    
    # EARS - tall, point up then curve back
    left_ear = [
        (-0.65, 0.15, 1.6), (-0.8, 0.25, 1.9), (-0.95, 0.38, 2.2),
        (-1.15, 0.55, 2.5), (-1.4, 0.78, 2.75), (-1.7, 1.08, 2.9),
        (-2.0, 1.45, 3.0), (-2.25, 1.85, 2.95),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.35 - (i * 0.04)
        create_box(f"LeftEar_{i}", scale, pos, purple_mat)
    
    right_ear = [
        (0.65, 0.15, 1.6), (0.8, 0.25, 1.9), (0.95, 0.38, 2.2),
        (1.15, 0.55, 2.5), (1.4, 0.78, 2.75), (1.7, 1.08, 2.9),
        (2.0, 1.45, 3.0), (2.25, 1.85, 2.95),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.35 - (i * 0.04)
        create_box(f"RightEar_{i}", scale, pos, purple_mat)
    
    # ARMS - forward, visible
    left_arm = [
        (-0.75, 0.35, -0.1), (-1.1, 0.6, 0.05), (-1.45, 0.85, 0.2),
        (-1.75, 1.05, 0.35),
    ]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.28, pos, purple_mat)
    
    right_arm = [
        (0.75, 0.35, -0.1), (1.1, 0.6, 0.05), (1.45, 0.85, 0.2),
        (1.75, 1.05, 0.35),
    ]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.28, pos, purple_mat)
    
    # LEGS
    left_leg = [(-0.45, 0, -1.1), (-0.45, 0.15, -1.35)]
    for i, pos in enumerate(left_leg):
        create_box(f"LeftLeg_{i}", 0.28, pos, purple_mat)
    
    right_leg = [(0.45, 0, -1.1), (0.45, 0.15, -1.35)]
    for i, pos in enumerate(right_leg):
        create_box(f"RightLeg_{i}", 0.28, pos, purple_mat)
    
    # BACK SPIKES
    back_spikes = [
        (0, -0.48, 0.1), (0.25, -0.55, 0), (-0.25, -0.55, 0),
        (0, -0.62, 0.5), (0.18, -0.65, 0.4), (-0.18, -0.65, 0.4),
        (0, -0.55, 1.0), (0.12, -0.58, 0.95), (-0.12, -0.58, 0.95),
    ]
    for i, pos in enumerate(back_spikes):
        create_box(f"Spike_{i}", 0.2, pos, purple_mat)
    
    # MOUTH - very wide
    mouth_blocks = [
        (0, 0.65, 1.05), (0.38, 0.65, 1.05), (-0.38, 0.65, 1.05),
        (0, 0.72, 0.7), (0.45, 0.72, 0.7), (-0.45, 0.72, 0.7),
        (0, 0.78, 0.38), (0.4, 0.78, 0.38), (-0.4, 0.78, 0.38),
        (0, 0.85, 0.08), (0.3, 0.85, 0.08), (-0.3, 0.85, 0.08),
    ]
    for i, pos in enumerate(mouth_blocks):
        create_box(f"Mouth_{i}", 0.4, pos, dark_purple_mat)
    
    # TONGUE
    tongue_blocks = [
        (0, 0.88, -0.15), (0, 0.92, -0.45),
        (0, 0.95, -0.7), (0, 0.98, -0.9),
    ]
    for i, pos in enumerate(tongue_blocks):
        create_box(f"Tongue_{i}", 0.25, pos, pink_mat)
    
    # EYES - glowing red
    create_box("LeftEyeWhite", 0.2, (-0.35, 0.55, 1.35), white_mat)
    create_box("RightEyeWhite", 0.2, (0.35, 0.55, 1.35), white_mat)
    create_box("LeftIris", 0.14, (-0.35, 0.6, 1.45), red_mat)
    create_box("RightIris", 0.14, (0.35, 0.6, 1.45), red_mat)
    create_box("LeftPupil", 0.08, (-0.35, 0.65, 1.55), black_mat)
    create_box("RightPupil", 0.08, (0.35, 0.65, 1.55), black_mat)
    
    # TEETH
    teeth_pos = [
        (-0.38, 0.82, 0.9), (-0.18, 0.85, 0.9), (0.18, 0.85, 0.9), (0.38, 0.82, 0.9),
        (-0.28, 0.88, 0.58), (0, 0.9, 0.58), (0.28, 0.88, 0.58),
        (-0.18, 0.92, 0.28), (0.18, 0.92, 0.28),
    ]
    for i, pos in enumerate(teeth_pos):
        create_box(f"Tooth_{i}", 0.14, pos, white_mat)
    
    # === LIGHTING - Bright studio setup ===
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()
    
    # Key light - front
    bpy.ops.object.light_add(type='AREA', location=(0, -8, 3))
    key = bpy.context.active_object
    key.data.energy = 1500
    key.data.size = 10
    key.rotation_euler = (math.radians(70), 0, 0)
    
    # Fill light - from left
    bpy.ops.object.light_add(type='AREA', location=(-8, -4, 2))
    fill = bpy.context.active_object
    fill.data.energy = 800
    fill.data.size = 8
    fill.rotation_euler = (math.radians(45), 0, math.radians(30))
    
    # Rim light - from back right
    bpy.ops.object.light_add(type='AREA', location=(6, 4, 4))
    rim = bpy.context.active_object
    rim.data.energy = 600
    rim.data.size = 6
    rim.rotation_euler = (math.radians(-30), 0, math.radians(-45))
    
    # World background - white
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.9, 0.9, 0.95, 1.0)
    bg.inputs['Strength'].default_value = 0.5
    
    # === CAMERA - Front view ===
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete()
    bpy.ops.object.camera_add(location=(0, -7, 0.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(88), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Fixed Gengar created with proper lighting!")
    return camera

def export_and_render():
    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath="/home/freeman/.openclaw/workspace/gengar-project/gengar.glb",
        export_format='GLB',
        export_yup=True,
        export_materials='EXPORT',
        export_cameras=True,
        export_lights=True,
        export_apply=True
    )
    print("Exported gengar.glb")
    
    # Render with good settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    scene.render.filepath = "/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png"
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False  # White background
    
    bpy.ops.render.render(write_still=True)
    print("Rendered to render_fixed.png")

if __name__ == "__main__":
    clear_scene()
    create_gengar_fixed()
    export_and_render()
    print("Complete!")
