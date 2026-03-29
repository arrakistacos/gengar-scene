#!/usr/bin/env python3
"""
Pikachu Iteration 7
Improvements based on expected vision feedback:
- Even MORE pronounced head (65% of height)
- Wider face for better recognition
- More dramatic lightning tail with sharper angles
- Rounder cheeks as actual spheres
"""

import struct
import math

def write_glb_header(total_size):
    """Write GLB header"""
    magic = b'glTF'
    version = 2
    return struct.pack('<4sII', magic, version, total_size)

def create_box_vertices(center, size_x, size_y, size_z):
    """Create vertices for a box"""
    x, y, z = center
    hx, hy, hz = size_x / 2, size_y / 2, size_z / 2
    
    vertices = [
        # Front face
        [x - hx, y - hy, z + hz], [x + hx, y - hy, z + hz], [x + hx, y + hy, z + hz], [x - hx, y + hy, z + hz],
        # Back face  
        [x - hx, y - hy, z - hz], [x - hx, y + hy, z - hz], [x + hx, y + hy, z - hz], [x + hx, y - hy, z - hz],
        # Top face
        [x - hx, y + hy, z - hz], [x - hx, y + hy, z + hz], [x + hx, y + hy, z + hz], [x + hx, y + hy, z - hz],
        # Bottom face
        [x - hx, y - hy, z - hz], [x + hx, y - hy, z - hz], [x + hx, y - hy, z + hz], [x - hx, y - hy, z + hz],
        # Right face
        [x + hx, y - hy, z - hz], [x + hx, y + hy, z - hz], [x + hx, y + hy, z + hz], [x + hx, y - hy, z + hz],
        # Left face
        [x - hx, y - hy, z - hz], [x - hx, y - hy, z + hz], [x - hx, y + hy, z + hz], [x - hx, y + hy, z - hz]
    ]
    return vertices

def create_sphere_vertices(center, radius, u_segments=12, v_segments=8):
    """Create vertices for a proper sphere"""
    cx, cy, cz = center
    vertices = []
    
    for i in range(v_segments + 1):
        v = i / v_segments
        phi = v * math.pi
        
        for j in range(u_segments + 1):
            u = j / u_segments
            theta = u * 2 * math.pi
            
            x = cx + radius * math.sin(phi) * math.cos(theta)
            y = cy + radius * math.cos(phi)
            z = cz + radius * math.sin(phi) * math.sin(theta)
            vertices.append([x, y, z])
    
    return vertices

def create_sphere_faces(start_index, u_segments=12, v_segments=8):
    """Create faces for sphere"""
    indices = []
    
    for i in range(v_segments):
        for j in range(u_segments):
            p0 = start_index + i * (u_segments + 1) + j
            p1 = start_index + i * (u_segments + 1) + (j + 1)
            p2 = start_index + (i + 1) * (u_segments + 1) + (j + 1)
            p3 = start_index + (i + 1) * (u_segments + 1) + j
            
            indices.extend([p0, p1, p2, p0, p2, p3])
    
    return indices

def create_pikachu_glb():
    """Create Pikachu GLB with maximum recognizability"""
    
    colors = {
        'yellow': [0.98, 0.92, 0.16, 1.0],
        'yellow_dark': [0.85, 0.75, 0.05, 1.0],
        'black': [0.08, 0.08, 0.08, 1.0],
        'red': [0.95, 0.15, 0.15, 1.0],
        'brown': [0.45, 0.28, 0.12, 1.0],
    }
    
    vertices = []
    colors_data = []
    indices = []
    current_index = 0
    
    # HUGE HEAD (65% of height) - Wider for cuteness
    head_verts = create_box_vertices([0, 0.85, 0], 1.2, 0.95, 1.05)
    vertices.extend(head_verts)
    colors_data.extend([colors['yellow']] * 24)
    
    box_faces = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],
                 [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]
    
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # LONG EARS - More prominent
    ear_length = 0.8
    ear_base_y = 1.15
    
    # Left ear
    for i in range(4):
        y = ear_base_y + ear_length * i / 3
        width = 0.18 - i * 0.03
        ear_seg = create_box_vertices([-0.45 - i*0.02, y, 0.05], width, ear_length/4 + 0.05, width)
        vertices.extend(ear_seg)
        colors_data.extend([colors['yellow']] * 24)
        for face in box_faces:
            indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                           current_index + face[0], current_index + face[2], current_index + face[3]])
        current_index = len(vertices)
    
    # Right ear
    for i in range(4):
        y = ear_base_y + ear_length * i / 3
        width = 0.18 - i * 0.03
        ear_seg = create_box_vertices([0.45 + i*0.02, y, 0.05], width, ear_length/4 + 0.05, width)
        vertices.extend(ear_seg)
        colors_data.extend([colors['yellow']] * 24)
        for face in box_faces:
            indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                           current_index + face[0], current_index + face[2], current_index + face[3]])
        current_index = len(vertices)
    
    # BLACK TIPS - Larger and more visible
    tip_y = ear_base_y + ear_length + 0.05
    left_tip = create_box_vertices([-0.51, tip_y, 0.06], 0.15, 0.15, 0.15)
    vertices.extend(left_tip)
    colors_data.extend([colors['black']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_tip = create_box_vertices([0.51, tip_y, 0.06], 0.15, 0.15, 0.15)
    vertices.extend(right_tip)
    colors_data.extend([colors['black']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # HUGE ROUND CHEEKS - Proper spheres
    cheek_radius = 0.25
    cheek_z = 0.6
    
    left_cheek = create_sphere_vertices([-0.38, 0.75, cheek_z], cheek_radius, 12, 8)
    left_cheek_idx = current_index
    vertices.extend(left_cheek)
    colors_data.extend([colors['red']] * len(left_cheek))
    indices.extend(create_sphere_faces(left_cheek_idx, 12, 8))
    current_index = len(vertices)
    
    right_cheek = create_sphere_vertices([0.38, 0.75, cheek_z], cheek_radius, 12, 8)
    right_cheek_idx = current_index
    vertices.extend(right_cheek)
    colors_data.extend([colors['red']] * len(right_cheek))
    indices.extend(create_sphere_faces(right_cheek_idx, 12, 8))
    current_index = len(vertices)
    
    # TINY BODY (35% of height)
    body_verts = create_box_vertices([0, 0.0, 0], 0.55, 0.55, 0.45)
    vertices.extend(body_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # STUBBY ARMS
    arm_verts = create_box_vertices([-0.32, 0.08, 0.32], 0.14, 0.3, 0.14)
    vertices.extend(arm_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_arm_verts = create_box_vertices([0.32, 0.08, 0.32], 0.14, 0.3, 0.14)
    vertices.extend(right_arm_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # FEET
    foot_verts = create_box_vertices([-0.18, -0.32, 0.22], 0.16, 0.12, 0.22)
    vertices.extend(foot_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_foot_verts = create_box_vertices([0.18, -0.32, 0.22], 0.16, 0.12, 0.22)
    vertices.extend(right_foot_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # DRAMATIC LIGHTNING BOLT TAIL - Sharper angles, more visible
    tail_segments = [
        ([0, -0.1, -0.28], 0.15),      # Base
        ([-0.15, 0.12, -0.35], 0.14),  # Sharp left
        ([0.12, 0.38, -0.42], 0.12),   # Sharp right
        ([-0.18, 0.68, -0.52], 0.10),  # Sharp left up
        ([0.15, 1.0, -0.58], 0.08),    # Sharp right
        ([-0.08, 1.35, -0.65], 0.06),  # Tip
    ]
    
    for pos, size in tail_segments:
        tail_verts = create_box_vertices(pos, size, size * 1.5, size)
        vertices.extend(tail_verts)
        colors_data.extend([colors['yellow']] * 24)
        for face in box_faces:
            indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                           current_index + face[0], current_index + face[2], current_index + face[3]])
        current_index = len(vertices)
    
    # BROWN STRIPES ON BACK
    stripe_verts = create_box_vertices([0, 0.1, -0.25], 0.35, 0.08, 0.05)
    vertices.extend(stripe_verts)
    colors_data.extend([colors['brown']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    stripe2_verts = create_box_vertices([0, -0.05, -0.23], 0.25, 0.06, 0.05)
    vertices.extend(stripe2_verts)
    colors_data.extend([colors['brown']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # Flatten data
    flat_vertices = []
    for v in vertices:
        flat_vertices.extend(v)
    
    flat_colors = []
    for c in colors_data:
        flat_colors.extend(c)
    
    vertices_bytes = struct.pack('<' + 'f' * len(flat_vertices), *flat_vertices)
    colors_bytes = struct.pack('<' + 'f' * len(flat_colors), *flat_colors)
    indices_bytes = struct.pack('<' + 'H' * len(indices), *indices)
    
    def pad4(data):
        while len(data) % 4 != 0:
            data += b'\x00'
        return data
    
    vertices_bytes = pad4(vertices_bytes)
    colors_bytes = pad4(colors_bytes)
    indices_bytes = pad4(indices_bytes)
    
    import json
    
    gltf = {
        'asset': {'version': '2.0', 'generator': 'pikachu_iter7.py'},
        'scene': 0,
        'scenes': [{'nodes': [0]}],
        'nodes': [{'mesh': 0}],
        'meshes': [{
            'primitives': [{
                'attributes': {'POSITION': 0, 'COLOR_0': 1},
                'indices': 2,
                'mode': 4
            }]
        }],
        'buffers': [{'byteLength': len(vertices_bytes) + len(colors_bytes) + len(indices_bytes)}],
        'bufferViews': [
            {'buffer': 0, 'byteOffset': 0, 'byteLength': len(vertices_bytes), 'target': 34962},
            {'buffer': 0, 'byteOffset': len(vertices_bytes), 'byteLength': len(colors_bytes), 'target': 34962},
            {'buffer': 0, 'byteOffset': len(vertices_bytes) + len(colors_bytes), 'byteLength': len(indices_bytes), 'target': 34963}
        ],
        'accessors': [
            {'bufferView': 0, 'byteOffset': 0, 'componentType': 5126, 'count': len(vertices), 'type': 'VEC3', 'max': [1.5, 2.5, 1], 'min': [-1.5, -1, -1]},
            {'bufferView': 1, 'byteOffset': 0, 'componentType': 5126, 'count': len(colors_data), 'type': 'VEC4'},
            {'bufferView': 2, 'byteOffset': 0, 'componentType': 5123, 'count': len(indices), 'type': 'SCALAR'}
        ],
        'materials': [{'pbrMetallicRoughness': {'metallicFactor': 0.0, 'roughnessFactor': 0.7}}]
    }
    
    json_str = json.dumps(gltf)
    json_bytes = json_str.encode('utf-8')
    json_bytes = pad4(json_bytes)
    
    json_chunk = struct.pack('<I', len(json_bytes)) + struct.pack('<I', 0x4E4F534A) + json_bytes
    bin_chunk = struct.pack('<I', len(vertices_bytes) + len(colors_bytes) + len(indices_bytes)) + struct.pack('<I', 0x004E4942) + vertices_bytes + colors_bytes + indices_bytes
    
    total_size = 12 + len(json_chunk) + len(bin_chunk)
    
    glb = write_glb_header(total_size) + json_chunk + bin_chunk
    return glb

if __name__ == '__main__':
    glb_data = create_pikachu_glb()
    with open('pikachu_iter7.glb', 'wb') as f:
        f.write(glb_data)
    print(f"Created pikachu_iter7.glb ({len(glb_data)} bytes)")
