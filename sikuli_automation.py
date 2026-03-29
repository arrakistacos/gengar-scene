#!/usr/bin/env python3
"""
SikuliX-based visual automation for Google Lens
Uses screen capture and image matching to find elements
"""

import subprocess
import time
import os

def run_command(cmd, timeout=10):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, timeout=timeout, 
                               capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

def screenshot(filename):
    """Take a screenshot"""
    os.environ['DISPLAY'] = ':0'
    run_command(f'scrot {filename}')
    return os.path.exists(filename)

def click_at(x, y):
    """Click at screen coordinates"""
    os.environ['DISPLAY'] = ':0'
    run_command(f'xdotool mousemove {x} {y} click 1')
    print(f"Clicked at ({x}, {y})")

def type_text(text):
    """Type text"""
    os.environ['DISPLAY'] = ':0'
    run_command(f'xdotool type "{text}"')

def press_key(key):
    """Press a key"""
    os.environ['DISPLAY'] = ':0'
    run_command(f'xdotool key {key}')

def open_chrome_with_google_images():
    """Open Chrome and navigate to Google Images"""
    print("Opening Chrome with Google Images...")
    os.environ['DISPLAY'] = ':0'
    os.environ['HOME'] = '/home/freeman'
    
    # Launch Chrome
    subprocess.Popen(
        ['google-chrome', 'https://images.google.com'],
        env={'DISPLAY': ':0', 'HOME': '/home/freeman'},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)
    print("Chrome opened")

def automate_google_lens():
    """Automate Google Lens using visual coordinates"""
    
    # Take initial screenshot
    print("Taking initial screenshot...")
    screenshot('/home/freeman/.openclaw/workspace/gengar-project/initial.png')
    
    # Open Chrome
    open_chrome_with_google_images()
    
    time.sleep(3)
    
    # Take screenshot to see current state
    screenshot('/home/freeman/.openclaw/workspace/gengar-project/chrome_open.png')
    print("Screenshot saved: chrome_open.png")
    
    # Click on camera icon (typical position in Google Images search bar)
    # Camera icon is usually at top right of search bar
    print("Clicking camera icon...")
    click_at(900, 150)  # Approximate position
    time.sleep(2)
    
    screenshot('/home/freeman/.openclaw/workspace/gengar-project/after_camera.png')
    print("Screenshot saved: after_camera.png")
    
    # Try clicking at different positions to find upload dialog
    positions = [
        (960, 600),  # Center
        (800, 500),  # Upload area
        (1000, 500),
    ]
    
    for x, y in positions:
        print(f"Trying click at ({x}, {y})...")
        click_at(x, y)
        time.sleep(1)
        screenshot(f'/home/freeman/.openclaw/workspace/gengar-project/click_{x}_{y}.png')
    
    print("\nAutomation complete!")
    print("Check screenshots to see results")

if __name__ == "__main__":
    automate_google_lens()
