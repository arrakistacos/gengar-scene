#!/usr/bin/env python3
"""
OpenCV + scrot visual automation for Google Lens
"""

import cv2
import numpy as np
import subprocess
import time
import os

def take_screenshot():
    """Take screenshot using scrot"""
    result = subprocess.run(['scrot', '/tmp/screenshot.png'], capture_output=True)
    if result.returncode == 0 and os.path.exists('/tmp/screenshot.png'):
        img = cv2.imread('/tmp/screenshot.png')
        return img
    return None

def click(x, y):
    """Click at coordinates"""
    subprocess.run(['xdotool', 'mousemove', str(x), str(y), 'click', '1'])

def type_text(text):
    """Type text"""
    subprocess.run(['xdotool', 'type', text])

def press_key(key):
    """Press key"""
    subprocess.run(['xdotool', 'key', key])

def find_button_by_color(screenshot, target_color, tolerance=30):
    """Find button by color matching"""
    # Convert to HSV for better color matching
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    
    # Define color range
    target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
    lower = np.array([max(0, target_hsv[0] - tolerance), 50, 50])
    upper = np.array([min(180, target_hsv[0] + tolerance), 255, 255])
    
    # Create mask
    mask = cv2.inRange(hsv, lower, upper)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get largest contour
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 100:
            M = cv2.moments(largest)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy)
    
    return None

def main():
    print("=" * 60)
    print("Google Lens Visual Automation")
    print("=" * 60)
    
    # Open Google Lens
    print("\n[1/5] Opening Google Lens...")
    subprocess.Popen(
        ['google-chrome', 'https://lens.google.com'],
        env={'DISPLAY': ':0', 'HOME': '/home/freeman'}
    )
    time.sleep(6)
    
    # Take screenshot
    print("[2/5] Taking screenshot...")
    screenshot = take_screenshot()
    if screenshot is None:
        print("ERROR: Failed to take screenshot")
        return
    
    # Save initial screenshot
    cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/screen_initial.png', screenshot)
    print(f"      Screenshot saved ({screenshot.shape[1]}x{screenshot.shape[0]})")
    
    # Click on upload area (Google Lens has camera icon in center)
    print("[3/5] Clicking upload area...")
    center_x = screenshot.shape[1] // 2
    center_y = screenshot.shape[0] // 2
    click(center_x, center_y)
    time.sleep(2)
    
    # Type file path
    print("[4/5] Typing file path...")
    file_path = "/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png"
    type_text(file_path)
    time.sleep(1)
    press_key('Return')
    
    # Wait for analysis
    print("[5/5] Waiting for analysis (15s)...")
    time.sleep(15)
    
    # Take final screenshot
    final = take_screenshot()
    if final is not None:
        cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/lens_results.png', final)
        print("\n✓ Final screenshot saved to: lens_results.png")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
