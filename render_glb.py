#!/usr/bin/env python3
"""Render GLB file to PNG using Blender"""

import bpy
import sys
import os

def render_glb(input_path, output_path):
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import GLB
    bpy.ops.import_scene.gltf(filepath=input_path)

    # Set up camera
    bpy.ops.object.camera_add(location=(0, -5, 2))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0)

    # Point camera at origin (approximate center of model)
    bpy.ops.object.select_all(action='DESELECT')
    camera.select_set(True)
    bpy.context.view_layer.objects.active = camera
    bpy.ops.object.constraint_add(type='TRACK_TO')
    constraint = camera.constraints["Track To"]
    constraint.target = None  # We'll set this to look at the imported model

    # Set as active camera
    bpy.context.scene.camera = camera

    # Set up lighting
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3

    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.data.energy = 1.5

    # Set render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.resolution_percentage = 100

    # Set output
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Render
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: blender -b -P render_glb.py -- <input.glb> <output.png>")
        sys.exit(1)

    # Blender passes args after --
    input_file = sys.argv[-2]
    output_file = sys.argv[-1]

    render_glb(input_file, output_file)
