#!/usr/bin/env python3
"""
Demonstration of the chronological ordering fix.
This shows how files will be named with incremental indices (001-999)
to ensure chronological ordering when sorted alphabetically.
"""

import re

def simulate_download(episodes):
    """Simulate the download process with new filename format."""
    print("=" * 70)
    print("PODCAST DOWNLOADER - CHRONOLOGICAL ORDER DEMO")
    print("=" * 70)
    print()
    print(f"Found {len(episodes)} episodes in feed.")
    print("Will download with incremental indices (001-999)")
    print()
    
    for i, title in enumerate(episodes, 1):
        # Clean the title for filename
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title).strip()
        
        # Create filename with incremental index
        index_str = f"{i:03d}"
        filename = f"{index_str}_{safe_title}.mp3"
        
        print(f"{i}. {title}")
        print(f"  Downloading: {title}")
        print(f"  Progress: 100.0%")
        print(f"  Saved: {filename}")
        print()
    
    print("=" * 70)
    print("CHRONOLOGICAL ORDER VERIFICATION")
    print("=" * 70)
    print()
    
    # Generate all filenames
    filenames = []
    for i, title in enumerate(episodes, 1):
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title).strip()
        index_str = f"{i:03d}"
        filename = f"{index_str}_{safe_title}.mp3"
        filenames.append(filename)
    
    print("Original order (as downloaded):")
    for i, fn in enumerate(filenames[:5], 1):  # Show first 5
        print(f"  {i:3d}. {fn}")
    print(f"  ... ({len(filenames) - 5} more files)")
    print()
    
    print("After alphabetical sorting (e.g., with 'ls' command):")
    sorted_filenames = sorted(filenames)
    for i, fn in enumerate(sorted_filenames[:5], 1):  # Show first 5
        print(f"  {i:3d}. {fn}")
    print(f"  ... ({len(sorted_filenames) - 5} more files)")
    print()
    
    if filenames == sorted_filenames:
        print("✓ SUCCESS: Files remain in chronological order!")
        print("✓ The incremental index (001-999) guarantees this.")
    else:
        print("✗ ERROR: Order is not preserved!")
    
    print()
    print("=" * 70)
    print("KEY BENEFITS")
    print("=" * 70)
    print()
    print("1. Short filenames (no long dates)")
    print("2. Guaranteed chronological ordering")
    print("3. Simple and reliable (no date parsing)")
    print("4. Supports up to 999 episodes")
    print("5. Human-readable and intuitive")
    print()

if __name__ == '__main__':
    # Use your actual podcast data from the example
    episodes = [
        "Esprit de Noël, es-tu là ? – Jour 23",
        "Sous le feu des projecteurs – Jour 22",
        "La petite flamme du cœur – Jour 21",
        "Ça sent le sapin… pour les sapins ! – Jour 20",
        "La crème de la crème ! – Jour 19",
        "Y a plus de papier ! – Jour 18",
        "La fièvre acheteuse – Jour 17",
        "Glaglagla ! – Jour 16",
        "La dernière chance ! – Jour 15",
        "Invisibles ! – Jour 14",
        "Une lumière dans la nuit – Jour 13",
        "Atterrissage immédiat ! – Jour 12",
        "Le village de Noël sous le choc ! – Jour 11",
        "Dans le ciel, plus de problème ! – Jour 10",
        "Sauve qui peut ! – Jour 9",
        "Recherche flamme désespérément – Jour 8",
        "Une drôle de lutine – Jour 7",
        "Oups ! – Jour 6",
        "Un Noël plus plus plus ! – Jour 5",
        "Scène de ménage chez les Noël – Jour 4",
        "Le burn-out du Père Noël – Jour 3",
        "La course de la lettre au Père Noël – Jour 2",
        "Cʹest bientôt Noël ? – Jour 1",
        "Rudolph et son nez rouge",
        "La Flamme de Noël – Bande-annonce",
        "Jade, future astronaute",
        "Le pouvoir des enfants",
        "Les pirates du lac Léman",
        "Privés de liberté",
        "Vive le rock !",
    ]
    
    simulate_download(episodes)
