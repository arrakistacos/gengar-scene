#!/usr/bin/env python3
"""
OpenCV Visual Automation v3 - Uses OCR to read screen text
Captures screenshot of results and extracts text using Tesseract
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
OUTPUT_TEXT = "/mnt/c/Users/arrak/Documents/dev/gengar-project/ai_analysis.txt"

# AI Question to ask
PROMPT_QUESTION = "What is wrong with this Pikachu 3D model? How can I improve it to look more accurate?"

class VisualAutomation:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self._detect_screen_size()
        
    def _detect_screen_size(self):
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
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['scrot', filename], check=True, timeout=5)
            return cv2.imread(filename)
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def click_at_percentage(self, px, py):
        x = int(self.screen_width * px)
        y = int(self.screen_height * py)
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=True, timeout=2)
            time.sleep(0.2)
            subprocess.run(['xdotool', 'click', '1'], check=True, timeout=2)
            print(f"Clicked at ({x}, {y}) [{px*100:.0f}%, {py*100:.0f}%]")
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False
    
    def type_text(self, text):
        os.environ['DISPLAY'] = ':0'
        try:
            subprocess.run(['xdotool', 'type', '--', text], check=True, timeout=5)
            print(f"Typed: {text[:60]}...")
            return True
        except Exception as e:
            print(f"Type failed: {e}")
            return False
    
    def key_combo(self, *keys):
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
        print(f"Waiting {seconds}s...")
        time.sleep(seconds)
    
    def extract_text_with_ocr(self, image_path):
        """Extract text from image using Tesseract OCR"""
        try:
            # Run tesseract
            result = subprocess.run(
                ['tesseract', image_path, 'stdout', '-l', 'eng'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return result.stdout
        except Exception as e:
            print(f"OCR failed: {e}")
        return ""

def open_chrome():
    print("Opening Chrome...")
    os.environ['DISPLAY'] = ':0'
    os.environ['HOME'] = '/home/freeman'
    subprocess.Popen(
        ['google-chrome', CHROME_URL],
        env={'DISPLAY': ':0', 'HOME': '/home/freeman'},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)

def main():
    print("="*60)
    print("OpenCV Visual Automation v3 with OCR")
    print("="*60)
    
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
    auto.click_at_percentage(0.5, 0.28)
    auto.wait(1)
    auto.type_text("images.google.com")
    auto.key_combo('Return')
    auto.wait(5)
    
    # Step 3: Click camera icon
    print("\n" + "-"*60)
    print("Step 3: Clicking camera icon...")
    print("-"*60)
    auto.click_at_percentage(0.7, 0.14)
    auto.wait(3)
    
    # Step 4: Click upload area
    print("\n" + "-"*60)
    print("Step 4: Clicking upload area...")
    print("-"*60)
    auto.click_at_percentage(0.5, 0.5)
    auto.wait(2)
    
    # Step 5: Upload image
    print("\n" + "-"*60)
    print("Step 5: Uploading image...")
    print("-"*60)
    auto.key_combo('ctrl', 'a')
    auto.wait(0.3)
    auto.type_text(IMAGE_TO_ANALYZE)
    auto.wait(0.5)
    auto.key_combo('Return')
    print(f"✓ Uploaded")
    auto.wait(12)
    
    # Step 6: Ask AI question
    print("\n" + "-"*60)
    print("Step 6: Asking AI question...")
    print("-"*60)
    auto.click_at_percentage(0.5, 0.85)
    auto.wait(1)
    auto.type_text(PROMPT_QUESTION)
    auto.wait(0.5)
    auto.key_combo('Return')
    print("✓ Question submitted")
    auto.wait(20)  # Longer wait for AI to generate
    
    # Step 7: Take screenshot of results
    print("\n" + "-"*60)
    print("Step 7: Capturing results...")
    print("-"*60)
    
    # Take multiple screenshots to capture all content
    screenshots = []
    for i in range(3):
        filename = f"/mnt/c/Users/arrak/Documents/dev/gengar-project/lens_results_{i+1}.png"
        auto.screenshot(filename)
        screenshots.append(filename)
        print(f"✓ Screenshot {i+1}: {filename}")
        auto.wait(2)
    
    # Step 8: Extract text with OCR
    print("\n" + "-"*60)
    print("Step 8: Extracting text with OCR...")
    print("-"*60)
    
    all_text = []
    for screenshot in screenshots:
        text = auto.extract_text_with_ocr(screenshot)
        if text:
            all_text.append(text)
            print(f"\n--- Text from {Path(screenshot).name} ---")
            print(text[:500])
    
    # Step 9: Save combined results
    print("\n" + "-"*60)
    print("Step 9: Saving results...")
    print("-"*60)
    
    with open(OUTPUT_TEXT, 'w', encoding='utf-8') as f:
        f.write("AI ANALYSIS RESULTS (OCR Extracted)\n")
        f.write("="*60 + "\n\n")
        f.write(f"Question: {PROMPT_QUESTION}\n\n")
        f.write("Extracted Text:\n")
        f.write("-"*60 + "\n\n")
        
        for i, text in enumerate(all_text, 1):
            f.write(f"\n--- Screenshot {i} ---\n")
            f.write(text)
            f.write("\n")
    
    print(f"✓ Results saved: {OUTPUT_TEXT}")
    
    # Step 10: Look for key information
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    
    combined_text = "\n".join(all_text)
    
    # Look for specific keywords
    keywords = ['pikachu', 'pokemon', 'yellow', 'cartoon', 'character', 'anime', 
                'similar', 'match', 'visual', 'guess', 'description', '3d', 'model']
    
    print("\nRelevant keywords found:")
    found_keywords = []
    for keyword in keywords:
        if keyword.lower() in combined_text.lower():
            found_keywords.append(keyword)
    
    if found_keywords:
        print(", ".join(found_keywords))
    else:
        print("(No keywords found - review screenshots manually)")
    
    print(f"\n📄 Full results: {OUTPUT_TEXT}")
    print("📸 Screenshots:")
    for s in screenshots:
        print(f"   - {s}")
    
    print("\n" + "="*60)
    print("Next: Review screenshots and OCR text for AI feedback")
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
