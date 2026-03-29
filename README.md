# 🎮 Pokemon Pastel Scene 💜⚡

A procedurally generated 3D Pokemon scene featuring Gengar and Pikachu, created with Blender and displayed in a pastel-themed Three.js interactive viewer.

## 🎨 Features

- **Multiple Pokemon Models**: Switch between Gengar and Pikachu with one click
- **Procedural 3D Models**: All models created entirely with Blender Python scripting
- **Themed Color Palettes**: Each Pokemon has unique pastel backgrounds and lighting
  - **Gengar**: Purple/blue/pink spooky pastels
  - **Pikachu**: Yellow/gold/lemon cheerful pastels
- **Interactive Controls**:
  - 🔄 **Switch Pokemon** - Toggle between Gengar and Pikachu
  - ⏯️ **Pause/Rotate** - Control auto-rotation
  - 🎨 **New Colors** - Cycle through themed backgrounds
  - 📷 **Reset View** - Return to default camera position
- **OrbitControls**: Click and drag to rotate, scroll to zoom, right-click to pan
- **Smooth Animations**: Floating, rotating models with particle sparkles
- **Dynamic Lighting**: Pokemon-specific lighting that matches their theme

## 🛠️ Tech Stack

- **Blender 4.2.3** - 3D modeling and GLTF export (procedural Python generation)
- **Three.js** - WebGL rendering with shadows, lighting, and particle effects
- **GitHub Pages** - Static hosting

## 🚀 Live Demo

**Visit the scene**: https://arrakistacos.github.io/gengar-scene

## 📁 Files

| File | Description |
|------|-------------|
| `index.html` | The Three.js web viewer with scene switching |
| `gengar.glb` | Gengar 3D model (GLTF binary) |
| `pikachu.glb` | Pikachu 3D model (GLTF binary) |
| `create_gengar.py` | Blender Python script for Gengar |
| `create_pikachu.py` | Blender Python script for Pikachu |
| `enable_addon.py` | Blender MCP addon enabler |

## 🎮 How to Use

1. **Open the live demo** in your browser
2. **Click "🔄 Switch Pokemon"** to toggle between Gengar and Pikachu
3. **Each Pokemon has unique**:
   - Color themes (4 per Pokemon)
   - Lighting setup
   - Entrance animation
4. **Interact**:
   - Orbit: Click + drag
   - Zoom: Scroll
   - Pan: Right-click + drag

## 🎭 Pokemon Details

### 👻 Gengar
- Purple rounded body with tongue out
- Red eyes, pointy ears
- Spooky pastel color palette
- Floats ominously with ghost particles

### ⚡ Pikachu  
- Yellow body with black ear tips
- Red cheeks, lightning tail
- Cheerful golden color palette
- Electric spark particle effects

## 📝 License

Created with 💜 by AI (OpenClaw + Blender + Three.js)

Pokemon, Gengar, and Pikachu are trademarks of Nintendo/The Pokemon Company.
This is a fan-made project for demonstration purposes.