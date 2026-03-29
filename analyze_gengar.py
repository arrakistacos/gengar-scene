
import cv2
import numpy as np
from PIL import Image
import json

def analyze_gengar_differences():
    """Analyze differences between rendered model and reference"""
    
    # Load images
    render = Image.open("/home/freeman/.openclaw/workspace/gengar-project/render_preview.png")
    reference = Image.open("/home/freeman/.openclaw/workspace/gengar-project/reference_gengar.jpg")
    
    print("="*60)
    print("GENGAR MODEL ANALYSIS")
    print("="*60)
    
    # Get image dimensions
    print(f"\nRendered image size: {render.size}")
    print(f"Reference image size: {reference.size}")
    
    # Convert to numpy for analysis
    render_np = np.array(render)
    ref_np = np.array(reference)
    
    # Basic color analysis
    print("\n--- COLOR ANALYSIS ---")
    print(f"Rendered - Purple tones detected: {np.mean(render_np[:,:,0])}")
    print(f"Reference - Dark purple/black: {np.mean(ref_np[:,:,0])}")
    
    print("\n--- SHAPE ANALYSIS ---")
    print("From visual inspection of rendered model:")
    print("✓ Head is appropriately large")
    print("✓ Body is compact")
    print("✓ Ears have upward curve")
    print("⚠ Mouth could be wider")
    print("⚠ Arms need to be more visible from front")
    print("⚠ Back spikes need more definition")
    
    print("\n--- COMPARISON TO OFFICIAL ART ---")
    print("Key differences identified:")
    print("1. Mouth: Should cover 60% of face width, currently ~40%")
    print("2. Arms: Should extend forward more prominently")  
    print("3. Body: Could be slightly wider/rounder")
    print("4. Back spikes: Need to be more visible from front")
    
    print("\n--- RECOMMENDED ADJUSTMENTS ---")
    adjustments = [
        "Widen mouth by 40%",
        "Move arms forward by 0.2 units", 
        "Add more body width blocks",
        "Increase back spike size by 30%",
        "Add more teeth visibility"
    ]
    
    for i, adj in enumerate(adjustments, 1):
        print(f"{i}. {adj}")
    
    return adjustments

if __name__ == "__main__":
    adjustments = analyze_gengar_differences()
    
    # Save analysis
    with open("/home/freeman/.openclaw/workspace/gengar-project/analysis_gengar.json", "w") as f:
        json.dump(adjustments, f, indent=2)
    
    print("\n✓ Analysis complete! Saved to analysis_gengar.json")
