#!/usr/bin/env python3
"""
Simplified Google Lens automation
Focus: Upload image, wait for analysis, capture result screenshot
Skips AI question (may not be available)
Uses window-activated Chrome for better visibility
"""

import subprocess
import time
import os
from pathlib import Path

# Configuration
IMAGE_PATH = "/mnt/c/Users/arrak/Documents/dev/gengar-project/pikachu_iter5.png"
OUTPUT_DIR = "/mnt/c/Users/arrak/Documents/dev/gengar-project/"

print("="*60)
print("Google Lens Automation - Simplified")
print("="*60)

os.environ['DISPLAY'] = ':0'
os.environ['HOME'] = '/home/freeman'

# Step 1: Open Chrome
print("\n[1/6] Opening Chrome...")
subprocess.Popen(
    ['google-chrome', 'https://images.google.com'],
    env={'DISPLAY': ':0', 'HOME': '/home/freeman'},
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(6)

# Step 2: Wait for Chrome to be ready
print("[2/6] Focusing Chrome window...")
subprocess.run(['xdotool', 'search', '--name', 'chrome', 'windowactivate'], timeout=3)
time.sleep(2)

# Step 3: Click camera icon
print("[3/6] Clicking camera icon...")
subprocess.run(['xdotool', 'mousemove', '900', '100'], timeout=2)
time.sleep(0.3)
subprocess.run(['xdotool', 'click', '1'], timeout=2)
print("Clicked camera icon (900, 100)")
time.sleep(3)

# Step 4: Click upload dialog
print("[4/6] Opening upload dialog...")
subprocess.run(['xdotool', 'mousemove', '960', '540'], timeout=2)
time.sleep(0.3)
subprocess.run(['xdotool', 'click', '1'], timeout=2)
time.sleep(2)

# Step 5: Upload file
print("[5/6] Uploading image...")
subprocess.run(['xdotool', 'key', 'ctrl+a'], timeout=2)
time.sleep(0.3)
subprocess.run(['xdotool', 'type', IMAGE_PATH], timeout=3)
time.sleep(0.5)
subprocess.run(['xdotool', 'key', 'Return'], timeout=2)
print(f"Uploaded: {Path(IMAGE_PATH).name}")
time.sleep(15)  # Wait for analysis

# Step 6: Capture results
print("[6/6] Capturing results...")
for i in range(1, 4):
    # Activate Chrome before screenshot
    subprocess.run(['xdotool', 'search', '--name', 'chrome', 'windowactivate'], timeout=3)
    time.sleep(1)
    
    filename = f"{OUTPUT_DIR}lens_result_{i}.png"
    subprocess.run(['scrot', '-u', filename], timeout=5)  # -u = focused window only
    print(f"Screenshot {i}: {filename}")
    time.sleep(3)

print("\n" + "="*60)
print("COMPLETE!")
print("="*60)
print(f"\nCheck screenshots in: {OUTPUT_DIR}")
print("Files: lens_result_1.png, lens_result_2.png, lens_result_3.png")
print("\nNote: scrot -u captures only the focused window")
