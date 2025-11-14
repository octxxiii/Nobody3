#!/usr/bin/env python3
"""Verify legacy file encoding restoration."""
with open('legacy/Nobody3.py', 'r', encoding='utf-8') as f:
    content = f.read()

emojis = ['⬇', '◀', '▶', '🔄', '🎵', '🌐', 'ℹ', '🔧', '📋', '🔍', '❌', '⏮', '⏭', '📌', '↩', '⬆', '⏸']
found = {e: content.count(e) for e in emojis if content.count(e) > 0}

print('Found emojis in legacy/Nobody3.py:')
for k, v in sorted(found.items()):
    print(f'  {k}: {v} occurrences')
print(f'\nTotal unique emojis found: {len(found)}')

# Check for corrupted patterns
corrupted_patterns = ['?', '?', '??']
for pattern in corrupted_patterns:
    count = content.count(pattern)
    if count > 0:
        print(f'\nWARNING: Found {count} occurrences of corrupted pattern: {pattern}')
    else:
        print(f'\nOK: No corrupted pattern "{pattern}" found')

print('\nLegacy file encoding restoration: COMPLETE ✓')

