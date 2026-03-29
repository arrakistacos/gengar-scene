#!/usr/bin/env python3
"""
Pikachu Iteration 6
Improvements based on vision analysis:
- Much larger head (60% of body height)
- More circular red cheeks (doubled size)
- Longer, more dramatic lightning bolt tail
- Better ear proportions and black tips
- Camera-friendly proportions for 3/4 view
"""

import struct
import math

def write_glb_header(total_size):
    """Write GLB header"""
    magic = b'glTF'
    version = 2
    return struct.pack('<4sII', magic, version, total_size)

def create_accessor(count, component_type, type_str, byte_offset, buffer_view):
    """Create accessor JSON object"""
    type_components = {
        'SCALAR': 1,
        'VEC2': 2,
        'VEC3': 3,
        'VEC4': 4,
        'MAT2': 4,
        'MAT3': 9,
        'MAT4': 16
    }
    return {
        'bufferView': buffer_view,
        'byteOffset': byte_offset,
        'componentType': component_type,
        'count': count,
        'type': type_str,
        'max': [1.0, 1.0, 1.0] if type_str == 'VEC3' else ([1.0] * type_components[type_str]),
        'min': [-1.0, -1.0, -1.0] if type_str == 'VEC3' else ([-1.0] * type_components[type_str])
    }

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

def create_sphere_vertices(center, radius, segments=8, rings=6):
    """Create vertices for a sphere/cheek"""
    vertices = []
    cx, cy, cz = center
    
    for i in range(rings + 1):
        phi = math.pi * i / rings
        for j in range(segments + 1):
            theta = 2 * math.pi * j / segments
            x = cx + radius * math.sin(phi) * math.cos(theta)
            y = cy + radius * math.cos(phi)
            z = cz + radius * math.sin(phi) * math.sin(theta)
            vertices.append([x, y, z])
    
    return vertices

def create_ear_vertices(base_center, length, width, height, tilt=0.3):
    """Create vertices for an ear with black tip"""
    vertices = []
    bx, by, bz = base_center
    
    # Main ear body
    for i in range(5):  # Height segments
        y = by + length * i / 4
        progress = i / 4
        current_width = width * (1 - progress * 0.6)  # Taper
        current_depth = height * (1 - progress * 0.5)
        
        for j in range(4):  # Cross section
            angle = j * math.pi / 2
            x = bx + current_width * math.cos(angle) * 0.5
            z = bz + current_depth * math.sin(angle) * 0.5 + tilt * y
            vertices.append([x, y, z])
    
    return vertices

def create_lightning_tail_vertices(base_center, length):
    """Create vertices for a dramatic lightning bolt tail"""
    vertices = []
    bx, by, bz = base_center
    
    # Lightning bolt segments with zigzag
    segments = [
        (0, 0, 0),           # Base
        (-0.15, 0.3, 0.1),   # Zig left
        (0.1, 0.5, -0.05),   # Zag right
        (-0.2, 0.7, 0.15),   # Zig left
        (0.15, 0.9, 0),      # Zag right
        (-0.1, 1.1, 0.1),    # Final point
    ]
    
    width = 0.08
    for i, (dx, dy, dz) in enumerate(segments):
        y = by + dy * length
        x = bx + dx
        z = bz + dz
        
        # Create cross-section at each point
        for j in range(4):
            angle = j * math.pi / 2
            vx = x + width * math.cos(angle)
            vz = z + width * math.sin(angle)
            vertices.append([vx, y, vz])
    
    return vertices

def create_pikachu_glb():
    """Create Pikachu GLB with improved proportions"""
    
    # Define colors
    colors = {
        'yellow': [0.98, 0.92, 0.16, 1.0],      # Bright yellow
        'yellow_dark': [0.85, 0.75, 0.05, 1.0], # Shadow yellow
        'black': [0.1, 0.1, 0.1, 1.0],          # Black tips
        'red': [0.9, 0.2, 0.2, 1.0],            # Red cheeks
        'brown': [0.4, 0.25, 0.1, 1.0],         # Brown stripes on back
        'white': [0.95, 0.95, 0.95, 1.0]        # Eyes/teeth
    }
    
    vertices = []
    colors_data = []
    indices = []
    
    current_index = 0
    
    # HEAD - Much larger (60% of total height)
    # Main head sphere
    head_y = 0.8
    head_radius = 0.55
    
    # Simplified head as box for voxel style
    head_verts = create_box_vertices([0, head_y, 0], 1.1, 0.9, 1.0)
    vertices.extend(head_verts)
    colors_data.extend([colors['yellow']] * 24)
    
    # Head faces
    head_indices = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],
        [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]
    ]
    for face in head_indices:
        indices.extend([face[0], face[1], face[2], face[0], face[2], face[3]])
    current_index = len(vertices)
    
    # EARS - Longer, more prominent
    ear_length = 0.7
    ear_base_y = head_y + 0.3
    
    # Left ear
    left_ear_verts = create_box_vertices([-0.4, ear_base_y + ear_length/2, 0.1], 0.15, ear_length, 0.15)
    left_ear_verts = [[x - 0.1, y + 0.15, z] for x, y, z in left_ear_verts]  # Tilt
    vertices.extend(left_ear_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # Right ear
    right_ear_verts = create_box_vertices([0.4, ear_base_y + ear_length/2, 0.1], 0.15, ear_length, 0.15)
    right_ear_verts = [[x + 0.1, y + 0.15, z] for x, y, z in right_ear_verts]  # Tilt
    vertices.extend(right_ear_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # BLACK TIPS on ears
    tip_size = 0.18
    left_tip_verts = create_box_vertices([-0.45, ear_base_y + ear_length + 0.05, 0.12], tip_size, 0.12, tip_size)
    vertices.extend(left_tip_verts)
    colors_data.extend([colors['black']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_tip_verts = create_box_vertices([0.45, ear_base_y + ear_length + 0.05, 0.12], tip_size, 0.12, tip_size)
    vertices.extend(right_tip_verts)
    colors_data.extend([colors['black']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # RED CHEEKS - Much larger and more circular
    cheek_size = 0.22
    left_cheek_verts = create_sphere_vertices([-0.35, head_y - 0.1, 0.55], cheek_size, 8, 6)
    vertices.extend(left_cheek_verts)
    colors_data.extend([colors['red']] * len(left_cheek_verts))
    
    # Cheek faces (simplified)
    for i in range(6):
        for j in range(8):
            v0 = current_index + i * 9 + j
            v1 = current_index + i * 9 + (j + 1) % 9
            v2 = current_index + (i + 1) * 9 + (j + 1) % 9
            v3 = current_index + (i + 1) * 9 + j
            indices.extend([v0, v1, v2, v0, v2, v3])
    current_index = len(vertices)
    
    right_cheek_verts = create_sphere_vertices([0.35, head_y - 0.1, 0.55], cheek_size, 8, 6)
    vertices.extend(right_cheek_verts)
    colors_data.extend([colors['red']] * len(right_cheek_verts))
    for i in range(6):
        for j in range(8):
            v0 = current_index + i * 9 + j
            v1 = current_index + i * 9 + (j + 1) % 9
            v2 = current_index + (i + 1) * 9 + (j + 1) % 9
            v3 = current_index + (i + 1) * 9 + j
            indices.extend([v0, v1, v2, v0, v2, v3])
    current_index = len(vertices)
    
    # BODY - Smaller proportion (40% of height)
    body_y = 0.05
    body_verts = create_box_vertices([0, body_y, 0], 0.6, 0.6, 0.5)
    vertices.extend(body_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # ARMS - Short stubby arms
    arm_verts = create_box_vertices([-0.35, 0.15, 0.35], 0.15, 0.35, 0.15)
    vertices.extend(arm_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_arm_verts = create_box_vertices([0.35, 0.15, 0.35], 0.15, 0.35, 0.15)
    vertices.extend(right_arm_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # FEET
    foot_verts = create_box_vertices([-0.2, -0.35, 0.25], 0.18, 0.15, 0.25)
    vertices.extend(foot_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_foot_verts = create_box_vertices([0.2, -0.35, 0.25], 0.18, 0.15, 0.25)
    vertices.extend(right_foot_verts)
    colors_data.extend([colors['yellow']] * 24)
    for face in head_indices:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # TAIL - Dramatic lightning bolt
    tail_length = 1.2
    tail_segments = [
        [0, -0.1, -0.3],      # Base
        [-0.1, 0.15, -0.35],  # Step 1
        [0.05, 0.4, -0.4],    # Step 2
        [-0.15, 0.65, -0.45], # Step 3
        [0.1, 0.9, -0.5],     # Step 4
        [-0.05, 1.15, -0.55], # Tip
    ]
    
    tail_width = 0.12
    for i, (x, y, z) in enumerate(tail_segments):
        segment_verts = create_box_vertices([x, y, z], tail_width * (1 - i * 0.1), 0.2, tail_width * (1 - i * 0.1))
        vertices.extend(segment_verts)
        colors_data.extend([colors['yellow']] * 24)
        for face in head_indices:
            indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                           current_index + face[0], current_index + face[2], current_index + face[3]])
        current_index = len(vertices)
    
    # Flatten vertices
    flat_vertices = []
    for v in vertices:
        flat_vertices.extend(v)
    
    flat_colors = []
    for c in colors_data:
        flat_colors.extend(c)
    
    # Calculate buffer sizes
    vertices_bytes = struct.pack('<' + 'f' * len(flat_vertices), *flat_vertices)
    colors_bytes = struct.pack('<' + 'f' * len(flat_colors), *flat_colors)
    indices_bytes = struct.pack('<' + 'H' * len(indices), *indices)
    
    # Align to 4 bytes
    def pad4(data):
        while len(data) % 4 != 0:
            data += b'\x00'
        return data
    
    vertices_bytes = pad4(vertices_bytes)
    colors_bytes = pad4(colors_bytes)
    indices_bytes = pad4(indices_bytes)
    
    # Create JSON
    import json
    
    gltf = {
        'asset': {'version': '2.0', 'generator': 'pikachu_iter6.py'},
        'scene': 0,
        'scenes': [{'nodes': [0]}],
        'nodes': [{'mesh': 0}],
        'meshes': [{
            'primitives': [{
                'attributes': {
                    'POSITION': 0,
                    'COLOR_0': 1
                },
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
            {'bufferView': 0, 'byteOffset': 0, 'componentType': 5126, 'count': len(vertices), 'type': 'VEC3', 'max': [1, 2, 1], 'min': [-1, -1, -1]},
            {'bufferView': 1, 'byteOffset': 0, 'componentType': 5126, 'count': len(colors_data), 'type': 'VEC4'},
            {'bufferView': 2, 'byteOffset': 0, 'componentType': 5123, 'count': len(indices), 'type': 'SCALAR'}
        ],
        'materials': [{
            'pbrMetallicRoughness': {
                'metallicFactor': 0.0,
                'roughnessFactor': 0.8
            }
        }]
    }
    
    json_str = json.dumps(gltf)
    json_bytes = json_str.encode('utf-8')
    json_bytes = pad4(json_bytes)
    
    # Build GLB
    json_chunk = struct.pack('<I', len(json_bytes)) + struct.pack('<I', 0x4E4F534A) + json_bytes
    bin_chunk = struct.pack('<I', len(vertices_bytes) + len(colors_bytes) + len(indices_bytes)) + struct.pack('<I', 0x004E4942) + vertices_bytes + colors_bytes + indices_bytes
    
    total_size = 12 + len(json_chunk) + len(bin_chunk)
    
    glb = write_glb_header(total_size) + json_chunk + bin_chunk
    
    return glb

if __name__ == '__main__':
    glb_data = create_pikachu_glb()
    with open('pikachu_iter6.glb', 'wb') as f:
        f.write(glb_data)
    print(f"Created pikachu_iter6.glb ({len(glb_data)} bytes)")
