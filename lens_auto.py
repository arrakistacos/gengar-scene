#!/usr/bin/env python3
import subprocess
import time
import os

# Open Google Lens
subprocess.Popen([
    'google-chrome', 
    '--new-window',
    'https://lens.google.com'
], env={'DISPLAY': ':0'})

time.sleep(4)

# Use xdotool to interact
# Click upload button area
subprocess.run(['xdotool', 'mousemove', '960', '540'])
subprocess.run(['xdotool', 'click', '1'])

time.sleep(2)

# Type file path
file_path = "/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"
subprocess.run(['xdotool', 'type', file_path])
time.sleep(1)
subprocess.run(['xdotool', 'key', 'Return'])

# Wait for analysis
time.sleep(12)

# Use Python to capture screen
try:
    from PIL import ImageGrab
    screenshot = ImageGrab.grab()
    screenshot.save('/home/freeman/.openclaw/workspace/gengar-project/lens_results.png')
    print("Screenshot saved to lens_results.png")
except ImportError:
    print("PIL not available for screenshot")

print("Analysis complete")
