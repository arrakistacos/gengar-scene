#!/usr/bin/env python3
"""
OpenCV-based visual automation for Google Lens
Uses template matching to find UI elements
"""

import cv2
import numpy as np
import subprocess
import time
import os

def take_screenshot():
    """Take screenshot using xwd and convert"""
    os.system('export DISPLAY=:0 && xwd -root -out /tmp/screen.xwd 2>/dev/null')
    os.system('convert /tmp/screen.xwd /tmp/screenshot.png 2>/dev/null')
    if os.path.exists('/tmp/screenshot.png'):
        return cv2.imread('/tmp/screenshot.png')
    return None

def find_and_click(template_path, confidence=0.7):
    """Find template on screen and click it"""
    screenshot = take_screenshot()
    if screenshot is None:
        print("Failed to take screenshot")
        return False
    
    template = cv2.imread(template_path)
    if template is None:
        print(f"Template not found: {template_path}")
        return False
    
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= confidence:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        
        print(f"Found at ({center_x}, {center_y}) with confidence {max_val:.2f}")
        
        # Click using xdotool
        os.system(f'xdotool mousemove {center_x} {center_y} click 1')
        return True
    else:
        print(f"Not found (confidence: {max_val:.2f})")
        return False

def main():
    print("Opening Google Lens...")
    os.system('export DISPLAY=:0 && google-chrome "https://lens.google.com" &')
    time.sleep(5)
    
    print("Taking screenshot to find upload button...")
    screenshot = take_screenshot()
    
    if screenshot is not None:
        # Save screenshot for manual inspection
        cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/screen_before.png', screenshot)
        print("Screenshot saved to screen_before.png")
        
        # Look for common upload button patterns
        # Since we don't have a template, let's try clicking known coordinates
        # Google Lens upload button is usually in the center
        print("Attempting to click upload button...")
        
        # Try clicking on camera icon area (usually center of page)
        os.system('export DISPLAY=:0 && xdotool mousemove 960 540 click 1')
        time.sleep(2)
        
        # Type the file path
        file_path = "/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"
        os.system(f'xdotool type "{file_path}"')
        time.sleep(1)
        os.system('xdotool key Return')
        
        print("Waiting for analysis...")
        time.sleep(15)
        
        # Take final screenshot
        final = take_screenshot()
        if final is not None:
            cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/lens_opencv.png', final)
            print("Final screenshot saved to lens_opencv.png")
        
        print("Done!")
    else:
        print("Failed to take screenshot - check X11 display")

if __name__ == "__main__":
    main()
