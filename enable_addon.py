import bpy
import addon_utils

# Enable the MCP addon
addon_module_name = "blender_mcp"

# Check if addon is already enabled
if addon_module_name not in bpy.context.preferences.addons:
    # Install and enable
    bpy.ops.preferences.addon_install(filepath="/home/freeman/blender-mcp/addon.py")
    bpy.ops.preferences.addon_enable(module="blender_mcp")
    print("Addon enabled successfully")
else:
    print("Addon already enabled")

# Save preferences
bpy.ops.wm.save_userpref()

# Start the MCP server socket
print("Addon setup complete")