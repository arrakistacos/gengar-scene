import bpy
import math
import os

def render_model(output_path="/home/freeman/.openclaw/workspace/gengar-project/render_preview.png"):
    """Render the current scene to an image file"""
    
    # Set up render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32  # Lower for faster preview
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    
    # Render
    bpy.ops.render.render(write_still=True)
    print(f"Rendered to {output_path}")
    return output_path

# Render current scene
render_model()
