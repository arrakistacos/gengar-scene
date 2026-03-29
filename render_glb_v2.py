#!/usr/bin/env python3
"""Render GLB file to PNG using Blender - V2 with improved lighting and camera"""

import bpy
import sys
import os
import math
from mathutils import Vector

def render_glb(input_path, output_path):
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import GLB
    bpy.ops.import_scene.gltf(filepath=input_path)
    
    # Get imported objects (find mesh objects)
    imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    if imported_objects:
        # Calculate bounding box center
        min_coord = [float('inf')] * 3
        max_coord = [float('-inf')] * 3
        for obj in imported_objects:
            for vertex in obj.bound_box:
                world_coord = obj.matrix_world @ Vector(vertex)
                for i in range(3):
                    min_coord[i] = min(min_coord[i], world_coord[i])
                    max_coord[i] = max(max_coord[i], world_coord[i])
        
        center = [(min_coord[i] + max_coord[i]) / 2 for i in range(3)]
        size = max(max_coord[i] - min_coord[i] for i in range(3))
    else:
        center = [0, 0, 0]
        size = 2

    # Set up camera - eye level, slightly angled
    camera_distance = size * 2.5
    camera_height = center[2] + size * 0.3  # Eye level
    
    bpy.ops.object.camera_add(location=(center[0] + camera_distance * 0.7, center[1] - camera_distance, camera_height))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.6)  # Angled to show more of the model
    bpy.context.scene.camera = camera

    # Add Track To constraint to look at center
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
    target = bpy.context.active_object
    
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Lighting setup - 3-point lighting
    # Key light (main)
    bpy.ops.object.light_add(type='AREA', location=(center[0] + size * 2, center[1] - size * 2, center[2] + size * 2))
    key = bpy.context.active_object
    key.data.energy = 150
    key.data.size = size
    
    # Fill light (softer, from opposite side)
    bpy.ops.object.light_add(type='AREA', location=(center[0] - size * 2, center[1] - size, center[2] + size * 0.5))
    fill = bpy.context.active_object
    fill.data.energy = 75
    fill.data.size = size * 1.5
    
    # Rim light (from behind for silhouette)
    bpy.ops.object.light_add(type='AREA', location=(center[0], center[1] + size * 2, center[2] + size))
    rim = bpy.context.active_object
    rim.data.energy = 100
    rim.data.size = size

    # Set render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.resolution_percentage = 100

    # Set output
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    # Transparent background
    bpy.context.scene.render.film_transparent = True

    # Render
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: blender -b -P render_glb_v2.py -- <input.glb> <output.png>")
        sys.exit(1)

    input_file = sys.argv[-2]
    output_file = sys.argv[-1]
    render_glb(input_file, output_file)
