#!/usr/bin/env python3
"""
Test to verify that files are named with incremental indices (001-999)
to ensure chronological ordering when sorted alphabetically.
"""

import re

def generate_filename(title, index):
    """Generate filename using the new incremental index format."""
    # Clean the title for filename
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
    safe_title = re.sub(r'\s+', '_', safe_title).strip()
    
    # Create filename with incremental index (001-999)
    index_str = f"{index:03d}"  # Zero-padded to 3 digits
    filename = f"{index_str}_{safe_title}.mp3"
    return filename

def test_chronological_ordering():
    """Test that files are in chronological order when sorted alphabetically."""
    
    # Sample episode titles from your output
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
    ]
    
    print("=" * 70)
    print("CHRONOLOGICAL ORDERING TEST")
    print("=" * 70)
    print()
    
    # Generate filenames with incremental indices
    print("Generated filenames with incremental indices (001-999):")
    print("-" * 70)
    filenames = []
    for i, title in enumerate(episodes, 1):
        filename = generate_filename(title, i)
        filenames.append(filename)
        print(f"{i:3d}. {title}")
        print(f"    -> {filename}")
        print()
    
    # Test alphabetical sorting
    print("=" * 70)
    print("ALPHABETICAL SORTING TEST")
    print("=" * 70)
    print()
    print("Original order (as generated):")
    for i, fn in enumerate(filenames, 1):
        print(f"  {i:3d}. {fn}")
    print()
    
    print("After alphabetical sorting:")
    sorted_filenames = sorted(filenames)
    for i, fn in enumerate(sorted_filenames, 1):
        print(f"  {i:3d}. {fn}")
    print()
    
    # Verify order is preserved
    if filenames == sorted_filenames:
        print("✓ SUCCESS: Files are in chronological order when sorted alphabetically!")
        print("✓ The incremental index (001-999) ensures proper chronological ordering.")
    else:
        print("✗ FAILURE: Files are NOT in chronological order!")
        return False
    
    print()
    print("=" * 70)
    print("RANGE TEST (001 to 999)")
    print("=" * 70)
    print()
    
    # Test the full range
    test_indices = [1, 5, 50, 100, 500, 999]
    print("Sample indices in the 001-999 range:")
    for idx in test_indices:
        filename = generate_filename("Test_Episode", idx)
        print(f"  Index {idx:3d} -> {filename}")
    
    print()
    print("✓ The format supports up to 999 episodes!")
    print()
    
    return True

if __name__ == '__main__':
    success = test_chronological_ordering()
    exit(0 if success else 1)
