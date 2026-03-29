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

def create_gengar_iteration6():
    """Iteration 6: Fixed based on image analysis"""
    
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
    
    # === FIX 1: WIDER BODY ===
    body_blocks = [
        (0, 0, -0.2), (0.3, 0, -0.2), (-0.3, 0, -0.2),
        (0, 0.28, -0.2), (0, -0.28, -0.2),
        (0.3, 0.28, -0.2), (0.3, -0.28, -0.2), (-0.3, 0.28, -0.2), (-0.3, -0.28, -0.2),
        (0, 0, -0.5), (0.28, 0, -0.5), (-0.28, 0, -0.5),
        (0, 0.28, -0.5), (0, -0.28, -0.5),
        (0.28, 0.28, -0.5), (0.28, -0.28, -0.5), (-0.28, 0.28, -0.5), (-0.28, -0.28, -0.5),
        (0, 0, -0.75), (0.22, 0, -0.75), (-0.22, 0, -0.75),
        (0, 0.22, -0.75), (0, -0.22, -0.75),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.3, pos, purple_mat)
    
    # === LARGE HEAD ===
    head_blocks = [
        (0, 0, 0.15), (0.35, 0, 0.15), (-0.35, 0, 0.15),
        (0, 0.35, 0.15), (0, -0.35, 0.15),
        (0.35, 0.35, 0.15), (0.35, -0.35, 0.15), (-0.35, 0.35, 0.15), (-0.35, -0.35, 0.15),
        (0, 0, 0.5), (0.35, 0, 0.5), (-0.35, 0, 0.5),
        (0, 0.35, 0.5), (0, -0.35, 0.5),
        (0.35, 0.35, 0.5), (0.35, -0.35, 0.5), (-0.35, 0.35, 0.5), (-0.35, -0.35, 0.5),
        (0, 0, 0.85), (0.35, 0, 0.85), (-0.35, 0, 0.85),
        (0, 0.35, 0.85), (0, -0.35, 0.85),
        (0.35, 0.35, 0.85), (0.35, -0.35, 0.85), (-0.35, 0.35, 0.85), (-0.35, -0.35, 0.85),
        (0, 0, 1.15), (0.28, 0, 1.15), (-0.28, 0, 1.15),
        (0, 0.28, 1.15), (0, -0.28, 1.15),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.32, pos, purple_mat)
    
    # === EARS: Iconic upward curve ===
    left_ear = [
        (-0.6, 0.12, 1.4), (-0.7, 0.2, 1.7), (-0.82, 0.3, 2.0),
        (-0.98, 0.45, 2.25), (-1.18, 0.65, 2.45), (-1.42, 0.9, 2.55),
        (-1.68, 1.2, 2.55), (-1.92, 1.55, 2.45),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.3 - (i * 0.03)
        create_box(f"LeftEar_{i}", scale, pos, purple_mat)
    
    right_ear = [
        (0.6, 0.12, 1.4), (0.7, 0.2, 1.7), (0.82, 0.3, 2.0),
        (0.98, 0.45, 2.25), (1.18, 0.65, 2.45), (1.42, 0.9, 2.55),
        (1.68, 1.2, 2.55), (1.92, 1.55, 2.45),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.3 - (i * 0.03)
        create_box(f"RightEar_{i}", scale, pos, purple_mat)
    
    # === FIX 2: ARMS MORE FORWARD ===
    left_arm = [
        (-0.68, 0.35, -0.05), (-0.95, 0.55, 0.05), (-1.22, 0.75, 0.18),
        (-1.45, 0.92, 0.32),
    ]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.22, pos, purple_mat)
    
    right_arm = [
        (0.68, 0.35, -0.05), (0.95, 0.55, 0.05), (1.22, 0.75, 0.18),
        (1.45, 0.92, 0.32),
    ]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.22, pos, purple_mat)
    
    # === LEGS ===
    left_leg = [(-0.38, 0, -1.0), (-0.38, 0.12, -1.2)]
    for i, pos in enumerate(left_leg):
        create_box(f"LeftLeg_{i}", 0.24, pos, purple_mat)
    
    right_leg = [(0.38, 0, -1.0), (0.38, 0.12, -1.2)]
    for i, pos in enumerate(right_leg):
        create_box(f"RightLeg_{i}", 0.24, pos, purple_mat)
    
    # === FIX 3: BIGGER BACK SPIKES ===
    back_spikes = [
        (0, -0.45, 0), (0.22, -0.52, -0.1), (-0.22, -0.52, -0.1),
        (0, -0.58, 0.35), (0.18, -0.62, 0.25), (-0.18, -0.62, 0.25),
        (0, -0.52, 0.8), (0.12, -0.55, 0.75), (-0.12, -0.55, 0.75),
        (0, -0.4, 1.1), (0.08, -0.42, 1.08), (-0.08, -0.42, 1.08),
    ]
    for i, pos in enumerate(back_spikes):
        create_box(f"Spike_{i}", 0.18, pos, purple_mat)
    
    # === FIX 4: MUCH WIDER MOUTH ===
    mouth_blocks = [
        (0, 0.6, 1.0), (0.32, 0.6, 1.0), (-0.32, 0.6, 1.0),
        (0, 0.65, 0.7), (0.38, 0.65, 0.7), (-0.38, 0.65, 0.7),
        (0, 0.7, 0.42), (0.35, 0.7, 0.42), (-0.35, 0.7, 0.42),
        (0, 0.75, 0.15), (0.28, 0.75, 0.15), (-0.28, 0.75, 0.15),
    ]
    for i, pos in enumerate(mouth_blocks):
        create_box(f"Mouth_{i}", 0.35, pos, dark_purple_mat)
    
    # === TONGUE ===
    tongue_blocks = [
        (0, 0.78, 0.05), (0, 0.82, -0.18),
        (0, 0.85, -0.38), (0, 0.88, -0.5),
    ]
    for i, pos in enumerate(tongue_blocks):
        create_box(f"Tongue_{i}", 0.2, pos, pink_mat)
    
    # === EYES ===
    create_box("LeftEyeWhite", 0.16, (-0.3, 0.5, 1.25), white_mat)
    create_box("RightEyeWhite", 0.16, (0.3, 0.5, 1.25), white_mat)
    
    create_box("LeftIris", 0.11, (-0.3, 0.55, 1.32), red_mat)
    create_box("RightIris", 0.11, (0.3, 0.55, 1.32), red_mat)
    
    create_box("LeftPupil", 0.055, (-0.3, 0.58, 1.4), black_mat)
    create_box("RightPupil", 0.055, (0.3, 0.58, 1.4), black_mat)
    
    # === FIX 5: MORE VISIBLE TEETH ===
    teeth_pos = [
        (-0.35, 0.72, 0.85), (-0.15, 0.75, 0.85), (0.15, 0.75, 0.85), (0.35, 0.72, 0.85),
        (-0.25, 0.78, 0.58), (0, 0.8, 0.58), (0.25, 0.78, 0.58),
        (-0.15, 0.85, 0.32), (0.15, 0.85, 0.32),
    ]
    for i, pos in enumerate(teeth_pos):
        create_box(f"Tooth_{i}", 0.12, pos, white_mat)
    
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
    bpy.ops.object.camera_add(location=(0, -5.5, 0.4))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(85), 0, math.radians(180))
    bpy.context.scene.camera = camera
    
    print("Gengar Iteration 6 created with fixes!")
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

def render_model(output_path="/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"):
    """Render the current scene"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    
    bpy.ops.render.render(write_still=True)
    print(f"Rendered to {output_path}")
    return output_path

if __name__ == "__main__":
    clear_scene()
    create_gengar_iteration6()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/gengar.glb")
    render_model()
    print("Iteration 6 complete!")
