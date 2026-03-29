#!/usr/bin/env python3
import subprocess
import time
import os

# Set display
os.environ['DISPLAY'] = ':0'

# Convert image to data URI would be complex, let's try file:// URL
gengar_path = "/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"
file_url = f"file://{gengar_path}"

# Try opening the image directly in Chrome, then we'll navigate to Lens
subprocess.Popen([
    'google-chrome', 
    file_url
], env={'DISPLAY': ':0', 'HOME': os.environ.get('HOME', '/home/freeman')})

time.sleep(3)

print(f"Opened {file_url}")
print("Now opening Google Lens...")

# Open Google Lens in same window
time.sleep(2)
subprocess.Popen([
    'google-chrome', 
    'https://lens.google.com'
], env={'DISPLAY': ':0', 'HOME': os.environ.get('HOME', '/home/freeman')})

time.sleep(5)

# Now try to interact using xdotool with proper env
env = {'DISPLAY': ':0'}

# Try to find Chrome window and click upload
subprocess.run(['xdotool', 'search', '--class', 'chrome', 'windowactivate'], env=env)
time.sleep(1)

# Move to upload button and click
subprocess.run(['xdotool', 'mousemove', '960', '540'], env=env)
subprocess.run(['xdotool', 'click', '1'], env=env)

time.sleep(2)

# Type path
subprocess.run(['xdotool', 'type', gengar_path], env=env)
subprocess.run(['xdotool', 'key', 'Return'], env=env)

time.sleep(10)

print("Google Lens should have the image now")
