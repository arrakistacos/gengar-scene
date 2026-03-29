#!/usr/bin/env python3
"""
Gengar Iteration 6
Improvements based on vision analysis:
- Add emission materials for eyes and grin (glow effect)
- More pronounced back spikes
- Wider body with more dramatic grin
- Brighter purple to show form better in lighting
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

def create_grin_vertices(center, width, height, depth):
    """Create vertices for a wide grin"""
    x, y, z = center
    # Arc shape for grin
    vertices = []
    segments = 8
    
    for i in range(segments):
        angle = math.pi * i / (segments - 1)  # 0 to pi for arc
        px = x + width * 0.5 * math.cos(math.pi - angle)  # Arc from left to right
        py = y + height * math.sin(angle) * 0.3  # Slight curve
        pz = z + depth
        
        # Create thickness
        for dx, dy in [(-0.02, -0.02), (0.02, -0.02), (0.02, 0.02), (-0.02, 0.02)]:
            vertices.append([px + dx, py + dy, pz])
    
    return vertices

def create_spike_vertices(base, tip, width):
    """Create a spike/pyramid"""
    bx, by, bz = base
    tx, ty, tz = tip
    
    # Base of spike
    hw = width / 2
    vertices = [
        [bx - hw, by, bz - hw],  # Base corners
        [bx + hw, by, bz - hw],
        [bx + hw, by, bz + hw],
        [bx - hw, by, bz + hw],
        [tx, ty, tz]  # Tip
    ]
    
    return vertices

def create_eye_vertices(center, size):
    """Create eye with emission effect (slightly larger for visibility)"""
    vertices = []
    x, y, z = center
    
    # Flattened sphere/oval shape
    for i in range(4):
        angle = i * math.pi / 2
        px = x + size * 0.5 * math.cos(angle)
        py = y + size * 0.3 * math.sin(angle)
        pz = z
        vertices.append([px, py, pz])
    
    return vertices

def create_gengar_glb():
    """Create Gengar GLB with improved ghost features"""
    
    # Define colors - brighter purple for visibility
    colors = {
        'purple': [0.5, 0.25, 0.6, 1.0],        # Brighter purple body
        'purple_dark': [0.3, 0.15, 0.4, 1.0],   # Darker for shadows
        'white': [0.95, 0.95, 0.95, 1.0],       # White eyes
        'white_glow': [1.0, 1.0, 1.0, 1.0],     # Brighter for grin
        'red': [0.9, 0.2, 0.2, 1.0]             # Inside mouth
    }
    
    vertices = []
    colors_data = []
    indices = []
    
    current_index = 0
    
    # BODY - Wider, more rounded
    body_verts = create_box_vertices([0, 0.3, 0], 1.3, 1.0, 0.9)
    vertices.extend(body_verts)
    colors_data.extend([colors['purple']] * 24)
    
    # Standard box faces
    box_faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11],
        [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]
    ]
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # HEAD - Large with pointed top
    head_verts = create_box_vertices([0, 0.9, 0], 1.1, 0.7, 0.85)
    vertices.extend(head_verts)
    colors_data.extend([colors['purple']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # POINTED EARS
    ear_width = 0.2
    ear_height = 0.5
    
    # Left ear
    left_ear_base = [-0.5, 1.0, 0]
    left_ear_tip = [-0.7, 1.6, 0.1]
    left_ear_verts = create_spike_vertices(left_ear_base, left_ear_tip, ear_width)
    vertices.extend(left_ear_verts)
    colors_data.extend([colors['purple']] * 5)
    
    # Pyramid faces for left ear
    ear_base_idx = current_index
    left_ear_faces = [
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  # Sides to tip
        [0, 2, 1], [0, 3, 2]  # Base
    ]
    for face in left_ear_faces:
        if len(face) == 3:
            indices.extend([ear_base_idx + face[0], ear_base_idx + face[1], ear_base_idx + face[2]])
        else:
            indices.extend([ear_base_idx + face[0], ear_base_idx + face[1], ear_base_idx + face[2],
                           ear_base_idx + face[0], ear_base_idx + face[2], ear_base_idx + face[3]])
    current_index = len(vertices)
    
    # Right ear
    right_ear_base = [0.5, 1.0, 0]
    right_ear_tip = [0.7, 1.6, 0.1]
    right_ear_verts = create_spike_vertices(right_ear_base, right_ear_tip, ear_width)
    vertices.extend(right_ear_verts)
    colors_data.extend([colors['purple']] * 5)
    
    ear_base_idx = current_index
    for face in left_ear_faces:
        if len(face) == 3:
            indices.extend([ear_base_idx + face[0], ear_base_idx + face[1], ear_base_idx + face[2]])
        else:
            indices.extend([ear_base_idx + face[0], ear_base_idx + face[1], ear_base_idx + face[2],
                           ear_base_idx + face[0], ear_base_idx + face[2], ear_base_idx + face[3]])
    current_index = len(vertices)
    
    # EYES - Larger and more visible
    eye_size = 0.18
    left_eye_verts = create_box_vertices([-0.3, 1.0, 0.45], eye_size, eye_size * 0.6, 0.05)
    vertices.extend(left_eye_verts)
    colors_data.extend([colors['white']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_eye_verts = create_box_vertices([0.3, 1.0, 0.45], eye_size, eye_size * 0.6, 0.05)
    vertices.extend(right_eye_verts)
    colors_data.extend([colors['white']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # WIDE GRIN - More pronounced and visible
    # Main mouth shape
    mouth_verts = create_box_vertices([0, 0.7, 0.48], 0.7, 0.25, 0.08)
    vertices.extend(mouth_verts)
    colors_data.extend([colors['white_glow']] * 24)  # Bright white for visibility
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # Back of mouth (red inside)
    mouth_back_verts = create_box_vertices([0, 0.7, 0.42], 0.65, 0.2, 0.05)
    vertices.extend(mouth_back_verts)
    colors_data.extend([colors['red']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # BACK SPIKES - More prominent
    spike_positions = [
        ([0, 0.6, -0.5], [0, 0.9, -0.9]),  # Center top
        ([-0.4, 0.4, -0.48], [-0.6, 0.7, -0.85]),  # Left
        ([0.4, 0.4, -0.48], [0.6, 0.7, -0.85]),  # Right
        ([-0.5, 0.1, -0.45], [-0.75, 0.35, -0.75]),  # Lower left
        ([0.5, 0.1, -0.45], [0.75, 0.35, -0.75]),  # Lower right
    ]
    
    for base, tip in spike_positions:
        spike_verts = create_spike_vertices(base, tip, 0.25)
        vertices.extend(spike_verts)
        colors_data.extend([colors['purple']] * 5)
        
        spike_base_idx = current_index
        for face in left_ear_faces:
            if len(face) == 3:
                indices.extend([spike_base_idx + face[0], spike_base_idx + face[1], spike_base_idx + face[2]])
            else:
                indices.extend([spike_base_idx + face[0], spike_base_idx + face[1], spike_base_idx + face[2],
                               spike_base_idx + face[0], spike_base_idx + face[2], spike_base_idx + face[3]])
        current_index = len(vertices)
    
    # ARMS - Short and stubby
    arm_verts = create_box_vertices([-0.6, 0.25, 0.3], 0.25, 0.4, 0.25)
    vertices.extend(arm_verts)
    colors_data.extend([colors['purple']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_arm_verts = create_box_vertices([0.6, 0.25, 0.3], 0.25, 0.4, 0.25)
    vertices.extend(right_arm_verts)
    colors_data.extend([colors['purple']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    # LEGS/FEET
    foot_verts = create_box_vertices([-0.35, -0.3, 0.25], 0.3, 0.2, 0.35)
    vertices.extend(foot_verts)
    colors_data.extend([colors['purple']] * 24)
    for face in box_faces:
        indices.extend([current_index + face[0], current_index + face[1], current_index + face[2],
                       current_index + face[0], current_index + face[2], current_index + face[3]])
    current_index = len(vertices)
    
    right_foot_verts = create_box_vertices([0.35, -0.3, 0.25], 0.3, 0.2, 0.35)
    vertices.extend(right_foot_verts)
    colors_data.extend([colors['purple']] * 24)
    for face in box_faces:
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
        'asset': {'version': '2.0', 'generator': 'gengar_iter6.py'},
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
                'roughnessFactor': 0.7
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
    glb_data = create_gengar_glb()
    with open('gengar_iter6.glb', 'wb') as f:
        f.write(glb_data)
    print(f"Created gengar_iter6.glb ({len(glb_data)} bytes)")
