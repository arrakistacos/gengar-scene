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

def create_refined_gengar_v3():
    """Refinement 3: Ears pointing UP then back, arms more forward"""
    
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
    
    # === REFINEMENT 3: COMPACT ROUND BODY ===
    body_blocks = [
        (0, 0, -0.15), (0.25, 0, -0.15), (-0.25, 0, -0.15),
        (0, 0.25, -0.15), (0, -0.25, -0.15),
        (0.25, 0.25, -0.15), (0.25, -0.25, -0.15), (-0.25, 0.25, -0.15), (-0.25, -0.25, -0.15),
        (0, 0, -0.45), (0.25, 0, -0.45), (-0.25, 0, -0.45),
        (0, 0.25, -0.45), (0, -0.25, -0.45),
        (0.25, 0.25, -0.45), (0.25, -0.25, -0.45), (-0.25, 0.25, -0.45), (-0.25, -0.25, -0.45),
        (0, 0, -0.7), (0.2, 0, -0.7), (-0.2, 0, -0.7),
        (0, 0.2, -0.7), (0, -0.2, -0.7),
    ]
    
    for i, pos in enumerate(body_blocks):
        create_box(f"Body_{i}", 0.28, pos, purple_mat)
    
    # === REFINEMENT 3: VERY LARGE HEAD ===
    head_blocks = [
        (0, 0, 0.2), (0.3, 0, 0.2), (-0.3, 0, 0.2),
        (0, 0.3, 0.2), (0, -0.3, 0.2),
        (0.3, 0.3, 0.2), (0.3, -0.3, 0.2), (-0.3, 0.3, 0.2), (-0.3, -0.3, 0.2),
        (0, 0, 0.55), (0.3, 0, 0.55), (-0.3, 0, 0.55),
        (0, 0.3, 0.55), (0, -0.3, 0.55),
        (0.3, 0.3, 0.55), (0.3, -0.3, 0.55), (-0.3, 0.3, 0.55), (-0.3, -0.3, 0.55),
        (0, 0, 0.9), (0.3, 0, 0.9), (-0.3, 0, 0.9),
        (0, 0.3, 0.9), (0, -0.3, 0.9),
        (0.3, 0.3, 0.9), (0.3, -0.3, 0.9), (-0.3, 0.3, 0.9), (-0.3, -0.3, 0.9),
        (0, 0, 1.2), (0.25, 0, 1.2), (-0.25, 0, 1.2),
        (0, 0.25, 1.2), (0, -0.25, 1.2),
    ]
    
    for i, pos in enumerate(head_blocks):
        create_box(f"Head_{i}", 0.3, pos, purple_mat)
    
    # === REFINEMENT 3: EARS - Point UP first, then curve back ===
    left_ear = [
        (-0.5, 0.1, 1.45), (-0.6, 0.15, 1.75), (-0.7, 0.22, 2.0),
        (-0.85, 0.3, 2.2), (-1.05, 0.4, 2.35), (-1.3, 0.55, 2.45),
        (-1.55, 0.75, 2.5), (-1.75, 1.0, 2.45),
    ]
    for i, pos in enumerate(left_ear):
        scale = 0.26 - (i * 0.025)
        create_box(f"LeftEar_{i}", scale, pos, purple_mat)
    
    right_ear = [
        (0.5, 0.1, 1.45), (0.6, 0.15, 1.75), (0.7, 0.22, 2.0),
        (0.85, 0.3, 2.2), (1.05, 0.4, 2.35), (1.3, 0.55, 2.45),
        (1.55, 0.75, 2.5), (1.75, 1.0, 2.45),
    ]
    for i, pos in enumerate(right_ear):
        scale = 0.26 - (i * 0.025)
        create_box(f"RightEar_{i}", scale, pos, purple_mat)
    
    # === REFINEMENT 3: ARMS - More forward/visible ===
    left_arm = [
        (-0.6, 0.2, 0), (-0.85, 0.35, 0.1), (-1.1, 0.5, 0.25),
        (-1.3, 0.65, 0.4),
    ]
    for i, pos in enumerate(left_arm):
        create_box(f"LeftArm_{i}", 0.18, pos, purple_mat)
    
    right_arm = [
        (0.6, 0.2, 0), (0.85, 0.35, 0.1), (1.1, 0.5, 0.25),
        (1.3, 0.65, 0.4),
    ]
    for i, pos in enumerate(right_arm):
        create_box(f"RightArm_{i}", 0.18, pos, purple_mat)
    
    # === LEGS ===
    left_leg = [(-0.35, 0, -0.95), (-0.35, 0.1, -1.15)]
    for i, pos in enumerate(left_leg):
        create_box(f"LeftLeg_{i}", 0.2, pos, purple_mat)
    
    right_leg = [(0.35, 0, -0.95), (0.35, 0.1, -1.15)]
    for i, pos in enumerate(right_leg):
        create_box(f"RightLeg_{i}", 0.2, pos, purple_mat)
    
    # === BACK SPIKES ===
    back_spikes = [
        (0, -0.4, 0), (0.2, -0.45, -0.1), (-0.2, -0.45, -0.1),
        (0, -0.5, 0.35), (0.15, -0.52, 0.25), (-0.15, -0.52, 0.25),
        (0, -0.45, 0.75), (0.1, -0.47, 0.7), (-0.1, -0.47, 0.7),
    ]
    for i, pos in enumerate(back_spikes):
        create_box(f"Spike_{i}", 0.14, pos, purple_mat)
    
    # === WIDE MOUTH ===
    mouth_blocks = [
        (0, 0.52, 1.05), (0.25, 0.52, 1.05), (-0.25, 0.52, 1.05),
        (0, 0.54, 0.78), (0.3, 0.54, 0.78), (-0.3, 0.54, 0.78),
        (0, 0.57, 0.52), (0.25, 0.57, 0.52), (-0.25, 0.57, 0.52),
        (0, 0.6, 0.28), (0.2, 0.6, 0.28), (-0.2, 0.6, 0.28),
    ]
    for i, pos in enumerate(mouth_blocks):
        create_box(f"Mouth_{i}", 0.27, pos, dark_purple_mat)
    
    # === TONGUE ===
    tongue_blocks = [
        (0, 0.64, 0.18), (0, 0.67, -0.02),
        (0, 0.7, -0.22), (0, 0.72, -0.37),
    ]
    for i, pos in enumerate(tongue_blocks):
        create_box(f"Tongue_{i}", 0.16, pos, pink_mat)
    
    # === EYES ===
    create_box("LeftEyeWhite", 0.14, (-0.25, 0.44, 1.3), white_mat)
    create_box("RightEyeWhite", 0.14, (0.25, 0.44, 1.3), white_mat)
    
    create_box("LeftIris", 0.09, (-0.25, 0.48, 1.35), red_mat)
    create_box("RightIris", 0.09, (0.25, 0.48, 1.35), red_mat)
    
    create_box("LeftPupil", 0.045, (-0.25, 0.5, 1.4), black_mat)
    create_box("RightPupil", 0.045, (0.25, 0.5, 1.4), black_mat)
    
    # === TEETH ===
    teeth_pos = [
        (-0.28, 0.6, 0.95), (-0.12, 0.62, 0.95), (0.12, 0.62, 0.95), (0.28, 0.6, 0.95),
        (-0.18, 0.64, 0.7), (0, 0.65, 0.7), (0.18, 0.64, 0.7),
        (-0.1, 0.67, 0.45), (0.1, 0.67, 0.45),
    ]
    for i, pos in enumerate(teeth_pos):
        create_box(f"Tooth_{i}", 0.09, pos, white_mat)
    
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
    
    print("Refined Gengar (v3) created!")
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
    create_refined_gengar_v3()
    export_gltf("/home/freeman/.openclaw/workspace/gengar-project/gengar.glb")
    print("Refinement 3 complete!")
