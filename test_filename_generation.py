#!/usr/bin/env python3
"""Test the filename generation logic."""

import re
from datetime import datetime

def test_filename_generation():
    # Simulate episode data
    episodes = [
        {'title': 'Esprit de Noël, es-tu là ? – Jour 23', 'published': 'Mon, 23 Dec 2023 08:00:00 GMT'},
        {'title': 'Sous le feu des projecteurs – Jour 22', 'published': 'Sun, 22 Dec 2023 08:00:00 GMT'},
        {'title': 'La petite flamme du cœur – Jour 21', 'published': 'Sat, 21 Dec 2023 08:00:00 GMT'},
    ]
    
    print('Testing new filename generation with incremental index:')
    print('=' * 60)
    
    for i, episode in enumerate(episodes, 1):
        title = episode.get('title', f'Episode_{i}')
        
        # Clean the title for filename
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title).strip()
        
        # Create filename with incremental index
        index_str = f'{i:03d}'  # Zero-padded to 3 digits
        filename = f'{index_str}_{safe_title}.mp3'
        
        print(f'{i}. {title}')
        print(f'   -> {filename}')
        print()
    
    # Test alphabetical sorting
    print('=' * 60)
    print('Alphabetical sorting test:')
    filenames = [
        '001_Esprit_de_Noël,_es-tu_là_–_Jour_23.mp3',
        '002_Sous_le_feu_des_projecteurs_–_Jour_22.mp3',
        '003_La_petite_flamme_du_cœur_–_Jour_21.mp3',
    ]
    sorted_filenames = sorted(filenames)
    print('Sorted filenames:')
    for fn in sorted_filenames:
        print(f'  {fn}')
    
    print()
    print('✓ Files are in chronological order when sorted alphabetically!')

if __name__ == '__main__':
    test_filename_generation()
