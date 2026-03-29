#!/usr/bin/env python3
"""Extract text from Google Lens results using OCR"""

import cv2
import numpy as np
import pytesseract
import json

def analyze_lens_results():
    # Load the screenshot
    img = cv2.imread('/home/freeman/.openclaw/workspace/gengar-project/lens_results.png')
    if img is None:
        print("ERROR: Could not load lens_results.png")
        return
    
    # Convert to RGB for OCR
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Try to extract text
    try:
        text = pytesseract.image_to_string(rgb)
        print("\n" + "="*60)
        print("EXTRACTED TEXT FROM GOOGLE LENS:")
        print("="*60)
        print(text)
        print("="*60)
        
        # Save to file
        with open('/home/freeman/.openclaw/workspace/gengar-project/lens_text.txt', 'w') as f:
            f.write(text)
        
        print("\n✓ Text saved to: lens_text.txt")
        
    except Exception as e:
        print(f"OCR error: {e}")
        print("Trying alternative approach...")
        
        # Look for text-like regions
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Save processed image for manual inspection
        cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/lens_processed.png', thresh)
        print("Processed image saved to: lens_processed.png")

if __name__ == "__main__":
    analyze_lens_results()
