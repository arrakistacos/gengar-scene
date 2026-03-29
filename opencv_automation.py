#!/usr/bin/env python3
"""
OpenCV-based visual automation for Google Lens
Replaces SikuliX with Python + OpenCV + xdotool
Runs in WSL, controls Chrome on Windows desktop
"""

import cv2
import numpy as np
import subprocess
import time
import os
import re
from pathlib import Path

# Configuration
CHROME_URL = "https://www.google.com"
IMAGE_TO_ANALYZE = "/mnt/c/Users/arrak/Documents/dev/gengar-project/pikachu_iter5.png"
OUTPUT_HTML = "/mnt/c/Users/arrak/Documents/dev/gengar-project/lens_page_source.html"
OUTPUT_TEXT = "/mnt/c/Users/arrak/Documents/dev/gengar-project/ai_analysis.txt"

# AI Question to ask
PROMPT_QUESTION = "What is wrong with this Pikachu 3D model? How can I improve it to look more accurate?"

# Template images (reference screenshots of UI elements)
TEMPLATE_DIR = "/mnt/c/Users/arrak/Documents/dev/gengar-project/chrome_upload_image.sikuli/"

class VisualAutomation:
    """OpenCV-based visual automation controller"""
    
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self._detect_screen_size()
        
    def _detect_screen_size(self):
        """Try to detect actual screen size"""
        try:
            # Try using xrandr
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if '*' in line:  # Current resolution has *
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
    
    def find_template(self, template_path, screenshot_path="screenshot.png", threshold=0.7):
        """Find template image on screen using OpenCV template matching"""
        
        # Take fresh screenshot
        screenshot = self.screenshot(screenshot_path)
        if screenshot is None:
            return None
        
        # Load template
        template = cv2.imread(template_path)
        if template is None:
            print(f"Could not load template: {template_path}")
            return None
        
        # Template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"Template match score: {max_val:.3f} (threshold: {threshold})")
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            # Draw debug image
            debug = screenshot.copy()
            cv2.rectangle(debug, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.circle(debug, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.imwrite(f"match_debug_{Path(template_path).stem}.png", debug)
            
            return (center_x, center_y, max_val)
        
        return None
    
    def click(self, x, y, clicks=1):
        """Click at screen coordinates using xdotool"""
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
    
    def double_click(self, x, y):
        """Double-click at coordinates"""
        return self.click(x, y, clicks=2)
    
    def type_text(self, text):
        """Type text using xdotool"""
        os.environ['DISPLAY'] = ':0'
        try:
            # Escape special characters
            safe_text = text.replace('"', '\\"')
            subprocess.run(['xdotool', 'type', '--', text], check=True, timeout=5)
            print(f"Typed: {text[:50]}...")
            return True
        except Exception as e:
            print(f"Type failed: {e}")
            return False
    
    def key_combo(self, *keys):
        """Press key combination using xdotool"""
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
        """Wait for specified seconds"""
        print(f"Waiting {seconds}s...")
        time.sleep(seconds)
    
    def find_and_click(self, template_path, threshold=0.7, retries=3):
        """Find template and click it, with retries"""
        for i in range(retries):
            print(f"Looking for {Path(template_path).name} (attempt {i+1}/{retries})...")
            result = self.find_template(template_path, threshold=threshold)
            if result:
                x, y, score = result
                return self.click(x, y)
            time.sleep(1)
        return False

def open_chrome():
    """Open Chrome with Google"""
    print("Opening Chrome...")
    os.environ['DISPLAY'] = ':0'
    os.environ['HOME'] = '/home/freeman'
    
    # Launch Chrome
    subprocess.Popen(
        ['google-chrome', CHROME_URL],
        env={'DISPLAY': ':0', 'HOME': '/home/freeman'},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Chrome launched, waiting 5s for load...")
    time.sleep(5)

def scrape_page_source():
    """Scrape Chrome page source using Ctrl+U"""
    print("Scraping page source...")
    
    # Use xdotool to send Ctrl+U
    os.environ['DISPLAY'] = ':0'
    subprocess.run(['xdotool', 'key', 'ctrl+u'], check=False, timeout=2)
    time.sleep(2)
    
    # Select all and copy
    subprocess.run(['xdotool', 'key', 'ctrl+a'], check=False, timeout=2)
    time.sleep(0.5)
    subprocess.run(['xdotool', 'key', 'ctrl+c'], check=False, timeout=2)
    time.sleep(0.5)
    
    # Close source tab (Ctrl+W)
    subprocess.run(['xdotool', 'key', 'ctrl+w'], check=False, timeout=2)
    time.sleep(1)
    
    # Try to get clipboard content using xclip or similar
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                               capture_output=True, text=True, timeout=3)
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except:
        pass
    
    # Fallback: save screenshot of source page
    print("Clipboard access failed, taking screenshot...")
    auto = VisualAutomation()
    auto.screenshot("page_source_screenshot.png")
    return ""

def extract_ai_descriptions(html_content):
    """Extract AI analysis from HTML"""
    descriptions = []
    
    patterns = [
        r'"([^"]*(?:similar|match|look like|resembles)[^"]*)"',
        r'"([^"]*(?:anime|cartoon|character|pokemon|pikachu)[^"]*)"',
        r'"([^"]*(?:yellow|purple|ghost|mouse|figure)[^"]*)"',
        r'"description":\s*"([^"]+)"',
        r'"text":\s*"([^"]+)"',
        r'<div[^\u003e]*\u003e([^\u003c]*(?:Visual matches|Best guess|About this image)[^\u003c]*)\u003c/div\u003e',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            if len(match) > 10 and match not in descriptions:
                descriptions.append(match)
    
    return descriptions[:10]

def main():
    """Main automation workflow"""
    print("="*60)
    print("OpenCV Visual Automation for Google Lens")
    print("="*60)
    print(f"\nAnalyzing: {IMAGE_TO_ANALYZE}")
    print(f"Question: {PROMPT_QUESTION}")
    
    # Initialize automation
    auto = VisualAutomation()
    
    # Step 1: Open Chrome
    print("\n" + "-"*60)
    print("Step 1: Opening Chrome...")
    print("-"*60)
    open_chrome()
    
    # Step 2: Navigate to Google Images
    print("\n" + "-"*60)
    print("Step 2: Navigating to Google Images...")
    print("-"*60)
    auto.click(960, 200)  # Click search bar (center, top)
    auto.wait(1)
    auto.type_text("images.google.com")
    auto.key_combo('Return')
    auto.wait(4)
    
    # Step 3: Find and click camera icon
    print("\n" + "-"*60)
    print("Step 3: Looking for camera icon...")
    print("-"*60)
    
    camera_templates = [
        os.path.join(TEMPLATE_DIR, "camera_icon.png"),
        os.path.join(TEMPLATE_DIR, "1774757692659.png"),
    ]
    
    camera_found = False
    for template in camera_templates:
        if os.path.exists(template):
            if auto.find_and_click(template, threshold=0.6, retries=2):
                camera_found = True
                break
    
    if not camera_found:
        print("Camera icon not found by image, trying position...")
        auto.click(900, 150)  # Approximate camera position
    
    auto.wait(3)
    
    # Step 4: Click upload area
    print("\n" + "-"*60)
    print("Step 4: Clicking upload area...")
    print("-"*60)
    
    upload_templates = [
        os.path.join(TEMPLATE_DIR, "1774757741443.png"),
        os.path.join(TEMPLATE_DIR, "1774757755151.png"),
    ]
    
    upload_found = False
    for template in upload_templates:
        if os.path.exists(template):
            if auto.find_and_click(template, threshold=0.6, retries=2):
                upload_found = True
                break
    
    if not upload_found:
        print("Upload area not found, using keyboard...")
        auto.key_combo('Tab')
        auto.wait(0.5)
        auto.key_combo('space')
    
    auto.wait(2)
    
    # Step 5: Enter file path
    print("\n" + "-"*60)
    print("Step 5: Entering file path...")
    print("-"*60)
    
    # Click on file input
    file_input_templates = [
        os.path.join(TEMPLATE_DIR, "1774758666157.png"),
    ]
    
    for template in file_input_templates:
        if os.path.exists(template):
            auto.find_and_click(template, threshold=0.6, retries=2)
            break
    
    auto.wait(1)
    auto.key_combo('ctrl', 'a')  # Select all
    auto.wait(0.3)
    auto.type_text(IMAGE_TO_ANALYZE)
    auto.wait(0.5)
    auto.key_combo('Return')
    print(f"✓ Uploaded: {IMAGE_TO_ANALYZE}")
    
    # Step 6: Wait for analysis
    print("\n" + "-"*60)
    print("Step 6: Waiting for Google Lens analysis...")
    print("-"*60)
    auto.wait(12)
    print("✓ Analysis complete")
    
    # Step 7: Ask AI question
    print("\n" + "-"*60)
    print("Step 7: Asking AI question...")
    print(f"Q: {PROMPT_QUESTION}")
    print("-"*60)
    
    # Try to find AI input field (various positions)
    ai_positions = [(960, 900), (960, 950), (800, 900)]
    for x, y in ai_positions:
        auto.click(x, y)
        auto.wait(0.5)
    
    auto.type_text(PROMPT_QUESTION)
    auto.wait(0.5)
    auto.key_combo('Return')
    print("✓ Question submitted")
    
    # Wait for AI response
    auto.wait(15)
    
    # Step 8: Scrape page source
    print("\n" + "-"*60)
    print("Step 8: Scraping page source...")
    print("-"*60)
    html_content = scrape_page_source()
    
    if html_content:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML saved: {OUTPUT_HTML}")
        
        # Extract AI descriptions
        descriptions = extract_ai_descriptions(html_content)
        
        # Save analysis
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
        print(f"\n📄 HTML: {OUTPUT_HTML}")
        print(f"📝 Analysis: {OUTPUT_TEXT}")
        print("\nAI Descriptions found:")
        print("-"*60)
        for i, desc in enumerate(descriptions[:5], 1):
            print(f"{i}. {desc[:100]}...")
    else:
        print("⚠ Could not extract page source, taking final screenshot...")
        auto.screenshot("final_screenshot.png")
        print("✓ Screenshot saved: final_screenshot.png")
    
    print("\n" + "="*60)
    print("AUTOMATION COMPLETE!")
    print("="*60)
    print("\nNext: Review the AI analysis and update your 3D model")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAutomation cancelled by user")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
