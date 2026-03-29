#!/usr/bin/env python3
"""
OpenCV Visual Automation v2 - Capture fresh reference images first
Then use those to match against current screen
"""

import cv2
import numpy as np
import subprocess
import time
import os
import re
from pathlib import Path
import json

# Configuration
CHROME_URL = "https://www.google.com"
IMAGE_TO_ANALYZE = "/mnt/c/Users/arrak/Documents/dev/gengar-project/pikachu_iter5.png"
OUTPUT_HTML = "/mnt/c/Users/arrak/Documents/dev/gengar-project/lens_page_source.html"
OUTPUT_TEXT = "/mnt/c/Users/arrak/Documents/dev/gengar-project/ai_analysis.txt"

# AI Question to ask
PROMPT_QUESTION = "What is wrong with this Pikachu 3D model? How can I improve it to look more accurate?"

class VisualAutomation:
    """OpenCV-based visual automation controller"""
    
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.captured_refs = {}
        self._detect_screen_size()
        
    def _detect_screen_size(self):
        """Try to detect actual screen size"""
        try:
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if '*' in line:
                    match = re.search(r'(\d+)x(\d+)', line)
                    if match:
                        self.screen_width = int(match.group(1))
                        self.screen_height = int(match.group(2))
                        break
        except:
            pass
        print(f"Screen size: {self.screen_width}x{self.screen_height}")
    
    def screenshot(self, filename="screenshot.png"):
        """Take screenshot using scrot"""
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['scrot', filename], check=True, timeout=5)
            return cv2.imread(filename)
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def capture_reference_region(self, name, x, y, w, h):
        """Capture a specific region as reference image"""
        img = self.screenshot("temp_capture.png")
        if img is not None:
            region = img[y:y+h, x:x+w]
            filename = f"ref_{name}.png"
            cv2.imwrite(filename, region)
            self.captured_refs[name] = filename
            print(f"Captured reference: {name} at ({x}, {y}, {w}, {h})")
            return filename
        return None
    
    def find_template(self, template_path, screenshot_path="screenshot.png", threshold=0.7):
        """Find template image on screen using OpenCV template matching"""
        
        screenshot = self.screenshot(screenshot_path)
        if screenshot is None:
            return None
        
        template = cv2.imread(template_path)
        if template is None:
            print(f"Could not load template: {template_path}")
            return None
        
        # Multi-scale matching
        scales = [1.0, 0.9, 1.1, 0.8, 1.2]
        best_result = None
        best_scale = 1.0
        
        for scale in scales:
            scaled_template = cv2.resize(template, None, fx=scale, fy=scale)
            if scaled_template.shape[0] > screenshot.shape[0] or scaled_template.shape[1] > screenshot.shape[1]:
                continue
                
            result = cv2.matchTemplate(screenshot, scaled_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if best_result is None or max_val > best_result[2]:
                best_result = (max_loc[0], max_loc[1], max_val, scale)
        
        if best_result and best_result[2] >= threshold:
            x, y, score, scale = best_result
            h, w = template.shape[:2]
            center_x = int(x + (w * scale) // 2)
            center_y = int(y + (h * scale) // 2)
            
            # Draw debug image
            debug = screenshot.copy()
            cv2.rectangle(debug, (x, y), (int(x + w*scale), int(y + h*scale)), (0, 255, 0), 2)
            cv2.circle(debug, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.imwrite(f"match_debug_{Path(template_path).stem}.png", debug)
            
            return (center_x, center_y, score, scale)
        
        return None
    
    def click(self, x, y, clicks=1):
        """Click at screen coordinates"""
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True, timeout=2)
            time.sleep(0.2)
            for _ in range(clicks):
                subprocess.run(['xdotool', 'click', '1'], check=True, timeout=2)
                time.sleep(0.1)
            print(f"Clicked at ({x}, {y})")
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False
    
    def type_text(self, text):
        """Type text"""
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['xdotool', 'type', '--', text], check=True, timeout=5)
            print(f"Typed: {text[:50]}...")
            return True
        except Exception as e:
            print(f"Type failed: {e}")
            return False
    
    def key_combo(self, *keys):
        """Press key combination"""
        os.environ['DISPLAY'] = ':0'
        try:
            key_str = '+'.join(keys)
            subprocess.run(['xdotool', 'key', key_str], check=True, timeout=2)
            print(f"Pressed: {key_str}")
            return True
        except Exception as e:
            print(f"Key combo failed: {e}")
            return False
    
    def wait(self, seconds):
        """Wait"""
        print(f"Waiting {seconds}s...")
        time.sleep(seconds)
    
    def click_at_percentage(self, px, py):
        """Click at percentage of screen size"""
        x = int(self.screen_width * px)
        y = int(self.screen_height * py)
        return self.click(x, y)

def capture_fresh_references(auto):
    """Capture fresh reference images at current screen resolution"""
    print("\n" + "="*60)
    print("CAPTURING FRESH REFERENCE IMAGES")
    print("="*60)
    print("\nChrome should be open to Google Images...")
    print("You have 5 seconds to make sure the page is loaded")
    auto.wait(5)
    
    refs = {}
    
    # Take full screenshot
    print("\nTaking reference screenshots...")
    auto.screenshot("google_images_full.png")
    
    # Capture camera icon area (usually top-right of search bar)
    # These are approximate positions - adjust as needed
    print("\nCapturing UI elements...")
    print("Note: Edit these coordinates if elements are in different positions")
    
    # Camera icon - typically in the search bar area
    refs['camera'] = auto.capture_reference_region('camera', 850, 100, 100, 100)
    
    # Upload dialog button area
    refs['upload_btn'] = auto.capture_reference_region('upload', 800, 500, 200, 100)
    
    # File input area
    refs['file_input'] = auto.capture_reference_region('file_input', 700, 550, 400, 50)
    
    # Save reference metadata
    with open('reference_coords.json', 'w') as f:
        json.dump(refs, f, indent=2)
    
    print("\n✓ Reference images captured!")
    print("Files: ref_camera.png, ref_upload.png, ref_file_input.png")
    return refs

def open_chrome():
    """Open Chrome"""
    print("Opening Chrome...")
    os.environ['DISPLAY'] = ':0'
    os.environ['HOME'] = '/home/freeman'
    
    subprocess.Popen(
        ['google-chrome', CHROME_URL],
        env={'DISPLAY': ':0', 'HOME': '/home/freeman'},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Chrome launched, waiting 5s...")
    time.sleep(5)

def scrape_with_xclip():
    """Scrape page source using xclip"""
    print("Scraping page source...")
    
    os.environ['DISPLAY'] = ':0'
    
    # Ctrl+U for page source
    subprocess.run(['xdotool', 'key', 'ctrl+u'], check=False, timeout=2)
    time.sleep(2)
    
    # Select all
    subprocess.run(['xdotool', 'key', 'ctrl+a'], check=False, timeout=2)
    time.sleep(0.5)
    
    # Copy
    subprocess.run(['xdotool', 'key', 'ctrl+c'], check=False, timeout=2)
    time.sleep(0.5)
    
    # Close tab
    subprocess.run(['xdotool', 'key', 'ctrl+w'], check=False, timeout=2)
    time.sleep(1)
    
    # Get from clipboard using xclip
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout
    except Exception as e:
        print(f"xclip failed: {e}")
    
    return ""

def extract_ai_descriptions(html_content):
    """Extract AI analysis"""
    descriptions = []
    
    patterns = [
        r'"([^"]*(?:similar|match|look like|resembles)[^"]*)"',
        r'"([^"]*(?:anime|cartoon|character|pokemon|pikachu)[^"]*)"',
        r'"([^"]*(?:yellow|purple|ghost|mouse|figure)[^"]*)"',
        r'"description":\s*"([^"]+)"',
        r'"text":\s*"([^"]+)"',
        r'\u003cdiv[^\u003e]*\u003e([^\u003c]*(?:Visual matches|Best guess|About this image)[^\u003c]*)\u003c/div\u003e',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if len(match) > 10 and match not in descriptions:
                descriptions.append(match)
    
    return descriptions[:10]

def main():
    """Main workflow"""
    print("="*60)
    print("OpenCV Visual Automation v2")
    print("="*60)
    
    auto = VisualAutomation()
    
    # Ask if we need to capture fresh references
    print("\nDo you want to:")
    print("1. Capture fresh reference images (run this first)")
    print("2. Run automation with existing references")
    print("\nAssuming option 2 (run automation)...")
    
    # Step 1: Open Chrome
    print("\n" + "-"*60)
    print("Step 1: Opening Chrome...")
    print("-"*60)
    open_chrome()
    
    # Step 2: Navigate to Google Images
    print("\n" + "-"*60)
    print("Step 2: Navigating to Google Images...")
    print("-"*60)
    auto.click_at_percentage(0.5, 0.28)  # Search bar
    auto.wait(1)
    auto.type_text("images.google.com")
    auto.key_combo('Return')
    auto.wait(5)
    
    # Step 3: Click camera icon by position
    print("\n" + "-"*60)
    print("Step 3: Clicking camera icon...")
    print("-"*60)
    # Camera icon is typically at ~70% from left, ~14% from top
    auto.click_at_percentage(0.7, 0.14)
    auto.wait(3)
    
    # Step 4: Click upload area
    print("\n" + "-"*60)
    print("Step 4: Clicking upload area...")
    print("-"*60)
    # Center of screen
    auto.click_at_percentage(0.5, 0.5)
    auto.wait(2)
    
    # Step 5: Type file path
    print("\n" + "-"*60)
    print("Step 5: Entering file path...")
    print("-"*60)
    auto.key_combo('ctrl', 'a')
    auto.wait(0.3)
    auto.type_text(IMAGE_TO_ANALYZE)
    auto.wait(0.5)
    auto.key_combo('Return')
    print(f"✓ Uploaded: {IMAGE_TO_ANALYZE}")
    auto.wait(12)
    
    # Step 6: Ask AI question
    print("\n" + "-"*60)
    print("Step 6: Asking AI question...")
    print(f"Q: {PROMPT_QUESTION}")
    print("-"*60)
    
    # Try clicking at bottom where AI input typically is
    auto.click_at_percentage(0.5, 0.85)
    auto.wait(1)
    auto.type_text(PROMPT_QUESTION)
    auto.wait(0.5)
    auto.key_combo('Return')
    print("✓ Question submitted")
    auto.wait(15)
    
    # Step 7: Scrape page source
    print("\n" + "-"*60)
    print("Step 7: Scraping page source...")
    print("-"*60)
    html_content = scrape_with_xclip()
    
    if html_content:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML saved: {OUTPUT_HTML}")
        
        descriptions = extract_ai_descriptions(html_content)
        
        with open(OUTPUT_TEXT, 'w', encoding='utf-8') as f:
            f.write("AI ANALYSIS RESULTS\n")
            f.write("="*60 + "\n\n")
            f.write(f"Question: {PROMPT_QUESTION}\n\n")
            f.write("AI Response:\n")
            f.write("-"*60 + "\n")
            for i, desc in enumerate(descriptions, 1):
                f.write(f"{i}. {desc}\n")
        
        print(f"✓ Analysis saved: {OUTPUT_TEXT}")
        
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE!")
        print("="*60)
        for i, desc in enumerate(descriptions[:5], 1):
            print(f"{i}. {desc[:100]}...")
    else:
        print("⚠ Could not extract HTML")
        auto.screenshot("final_screenshot.png")
        print("✓ Screenshot saved: final_screenshot.png")
    
    print("\n" + "="*60)
    print("AUTOMATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
