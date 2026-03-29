#!/usr/bin/env python3
"""
Extract text from Google Lens results using OCR
Then use that to ask questions
"""

import subprocess
import time
import os

def main():
    # Open Google Lens with the rendered image
    print("Opening Google Lens with rendered model...")
    
    # Use xdotool to navigate
    env = {'DISPLAY': ':0', 'HOME': '/home/freeman'}
    
    # Open Google Lens
    subprocess.Popen(
        ['google-chrome', 'https://lens.google.com'],
        env=env
    )
    
    time.sleep(4)
    
    # Click upload area (center of page)
    subprocess.run(['xdotool', 'mousemove', '960', '540', 'click', '1'], env=env)
    time.sleep(2)
    
    # Type file path
    file_path = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png'
    subprocess.run(['xdotool', 'type', file_path], env=env)
    subprocess.run(['xdotool', 'key', 'Return'], env=env)
    
    print("Waiting for Lens analysis...")
    time.sleep(12)
    
    # Screenshot
    subprocess.run(['scrot', '/home/freeman/.openclaw/workspace/gengar-project/lens_with_analysis.png'], env=env)
    
    print("Screenshot saved. Now extracting text with OCR...")
    
    # Try to extract text from the screenshot
    result = subprocess.run(
        ['tesseract', '/home/freeman/.openclaw/workspace/gengar-project/lens_with_analysis.png', 
         '/home/freeman/.openclaw/workspace/gengar-project/lens_extracted', '-l', 'eng'],
        capture_output=True, text=True
    )
    
    # Read extracted text
    if os.path.exists('/home/freeman/.openclaw/workspace/gengar-project/lens_extracted.txt'):
        with open('/home/freeman/.openclaw/workspace/gengar-project/lens_extracted.txt', 'r') as f:
            text = f.read()
        
        print("\n" + "="*60)
        print("EXTRACTED TEXT FROM GOOGLE LENS:")
        print("="*60)
        print(text)
        print("="*60)
        
        # Now use this text to search
        if text.strip():
            print("\nSearching Google with this information...")
            search_query = f"What is this Pokemon character? {text[:100]}"
            subprocess.Popen(
                ['google-chrome', f'https://google.com/search?q={search_query}'],
                env=env
            )
    else:
        print("No text extracted")

if __name__ == "__main__":
    main()
