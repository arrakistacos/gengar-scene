#!/usr/bin/env python3
"""Analyze what's actually in the rendered image"""

import cv2
import numpy as np

def analyze_render(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        print("ERROR: Could not load image")
        return
    
    print(f"Image size: {img.shape}")
    
    # Check if it has alpha channel
    if len(img.shape) == 3 and img.shape[2] == 4:
        # RGBA image
        b, g, r, a = cv2.split(img)
        
        print(f"\nAlpha channel stats:")
        print(f"  Mean: {np.mean(a):.2f}")
        print(f"  Min: {np.min(a)}")
        print(f"  Max: {np.max(a)}")
        
        # Check RGB channels (ignore transparent pixels)
        mask = a > 0
        if np.any(mask):
            rgb_pixels = img[mask]
            print(f"\nNon-transparent pixels: {np.sum(mask)}")
            print(f"RGB mean: {np.mean(rgb_pixels[:, :3]):.2f}")
            print(f"RGB std: {np.std(rgb_pixels[:, :3]):.2f}")
        else:
            print("\nWARNING: All pixels are transparent!")
    else:
        # RGB image
        print(f"RGB mean: {np.mean(img):.2f}")
        print(f"RGB std: {np.std(img):.2f}")
    
    # Check for mostly white background
    gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    white_pixels = np.sum(gray > 240)
    total_pixels = gray.size
    
    print(f"\nPixel analysis:")
    print(f"  White-ish pixels (>240): {white_pixels} ({100*white_pixels/total_pixels:.1f}%)")
    print(f"  Dark pixels (<50): {np.sum(gray < 50)} ({100*np.sum(gray < 50)/total_pixels:.1f}%)")
    
    # Save a diagnostic version
    cv2.imwrite('/home/freeman/.openclaw/workspace/gengar-project/render_diagnostic.jpg', 
                img[:, :, :3], [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"\nSaved diagnostic JPEG to: render_diagnostic.jpg")

if __name__ == "__main__":
    analyze_render('/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png')
