#!/usr/bin/env python3
"""
Analyze rendered model using Google Cloud Vision API
Compare with official Pokemon reference
"""

import os
import json
from google.cloud import vision
from google.oauth2 import service_account

def analyze_image(image_path):
    """Analyze image using Google Cloud Vision"""
    
    # Set up credentials
    credentials = service_account.Credentials.from_service_account_file(
        '/home/freeman/openclaw-sa-key.json'
    )
    
    client = vision.ImageAnnotatorClient(credentials=credentials)
    
    # Load image
    with open(image_path, 'rb') as f:
        content = f.read()
    
    image = vision.Image(content=content)
    
    # Perform label detection
    print("Analyzing image with Google Vision API...")
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    print("\n" + "="*60)
    print("VISION API ANALYSIS - DETECTED LABELS:")
    print("="*60)
    
    detected = []
    for label in labels[:15]:  # Top 15 labels
        print(f"  {label.description}: {label.score:.2%}")
        detected.append({
            'description': label.description,
            'score': label.score
        })
    
    # Check for Pokemon-related terms
    pokemon_terms = ['cartoon', 'toy', 'figurine', 'gaming', 'character', 
                     'ghost', 'purple', 'monster', 'creature']
    
    pokemon_score = 0
    for label in labels:
        if any(term in label.description.lower() for term in pokemon_terms):
            pokemon_score += label.score
    
    print("\n" + "="*60)
    print(f"POKEMON-LIKE SCORE: {pokemon_score:.2f}")
    print("="*60)
    
    # Try web detection for similar images
    print("\nSearching for similar images...")
    web_response = client.web_detection(image=image)
    web_detections = web_response.web_detection
    
    print("\n" + "="*60)
    print("SIMILAR IMAGES FOUND:")
    print("="*60)
    
    if web_detections.web_entities:
        for entity in web_detections.web_entities[:10]:
            print(f"  {entity.description}: {entity.score:.2%}")
    
    # Save results
    results = {
        'labels': detected,
        'pokemon_score': pokemon_score,
        'web_entities': [{'description': e.description, 'score': e.score} 
                        for e in web_detections.web_entities[:10]] if web_detections.web_entities else []
    }
    
    with open('/home/freeman/.openclaw/workspace/gengar-project/vision_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Analysis saved to: vision_analysis.json")
    
    return results

def compare_to_reference(render_analysis, reference_path):
    """Compare render to reference image"""
    print("\n" + "="*60)
    print("COMPARING TO OFFICIAL GENGAR REFERENCE...")
    print("="*60)
    
    credentials = service_account.Credentials.from_service_account_file(
        '/home/freeman/openclaw-sa-key.json'
    )
    client = vision.ImageAnnotatorClient(credentials=credentials)
    
    # Analyze reference
    with open(reference_path, 'rb') as f:
        content = f.read()
    
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    ref_labels = response.label_annotations
    
    print("\nReference image labels:")
    for label in ref_labels[:10]:
        print(f"  {label.description}: {label.score:.2%}")
    
    # Compare
    render_desc = {l['description'].lower() for l in render_analysis['labels']}
    ref_desc = {l.description.lower() for l in ref_labels[:15]}
    
    overlap = render_desc.intersection(ref_desc)
    
    print("\n" + "="*60)
    print("COMPARISON RESULTS:")
    print("="*60)
    print(f"Common terms: {len(overlap)}")
    for term in list(overlap)[:10]:
        print(f"  ✓ {term}")
    
    similarity = len(overlap) / max(len(render_desc), len(ref_desc))
    print(f"\nSimilarity score: {similarity:.1%}")

if __name__ == "__main__":
    # Analyze the rendered model
    render_path = '/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png'
    ref_path = '/home/freeman/.openclaw/workspace/gengar-project/reference_gengar.jpg'
    
    analysis = analyze_image(render_path)
    compare_to_reference(analysis, ref_path)
    
    print("\n" + "="*60)
    print("VISION ANALYSIS COMPLETE")
    print("="*60)
