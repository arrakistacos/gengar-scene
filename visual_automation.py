#!/usr/bin/env python3
"""
Image-based visual automation - find and click camera icon
Uses OpenCV to find the camera icon on screen
"""

import cv2
import numpy as np
import subprocess
import time
import os

def take_screenshot(filename):
    """Take screenshot"""
    os.environ['DISPLAY'] = ':0'
    subprocess.run(['scrot', filename], check=False)
    return os.path.exists(filename)

def find_template_on_screen(template_path, screenshot_path, threshold=0.8):
    """Find a template image on the screen using OpenCV"""
    
    # Take current screenshot
    take_screenshot(screenshot_path)
    
    # Read images
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)
    
    if screenshot is None or template is None:
        print(f"Could not load images")
        return None
    
    # Template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Template match score: {max_val:.2f}")
    
    if max_val >= threshold:
        # Get center of matched area
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        
        # Draw rectangle on debug image
        debug_img = screenshot.copy()
        cv2.rectangle(debug_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
        cv2.circle(debug_img, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/match_debug.png', debug_img)
        
        return (center_x, center_y)
    
    return None

def click_at(x, y):
    """Click at coordinates"""
    os.environ['DISPLAY'] = ':0'
    subprocess.run(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])
    print(f"Clicked at ({x}, {y})")

def main():
    """Main automation flow"""
    
    # Take a screenshot first to see the screen
    print("Taking initial screenshot...")
    take_screenshot('/home/freeman/.openclaw/workspace/gengar-project/screen_init.png')
    print("Screenshot saved: screen_init.png")
    
    # Let's try finding the camera icon by analyzing the screenshot
    # The camera icon is typically a small camera symbol in the search bar
    
    # For now, let's try clicking at known positions where the camera icon might be
    # Based on Google Images layout
    
    print("\nTrying camera icon positions...")
    
    # Common positions for Google Images camera icon
    camera_positions = [
        (850, 100),  # Top right of search bar
        (900, 100),
        (950, 100),
        (880, 120),
        (920, 120),
        (890, 130),
        (830, 110),
    ]
    
    for i, (x, y) in enumerate(camera_positions):
        print(f"\nTrying position {i+1}: ({x}, {y})")
        click_at(x, y)
        time.sleep(2)
        
        # Take screenshot to see result
        take_screenshot(f'/home/freeman/.openclaw/workspace/gengar-project/click_attempt_{i+1}.png')
        print(f"Screenshot: click_attempt_{i+1}.png")
    
    print("\nDone testing positions!")
    print("Check screenshots to see which position worked")

if __name__ == "__main__":
    main()
