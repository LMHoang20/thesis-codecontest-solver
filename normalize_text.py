import json
import os
import unicodedata

unicodes = {'≤', '\u200b', 'П', '»', '→', '…', '⌈', 'Ω', 'ö', 'а', 'ε', '\u2002', '∈', '×', '⌊', '\xa0', '⌉', '⋅', '∞', '，', '≥', '—', '•', 'α', '·', '≠', 'Σ', '−', '≈', '\u2009', '’', 'Δ', '«', '⌋', '–', 'π', '←', '±', 'φ', '↔', '≡', 'С', '‘', '”', 'ρ', '“', '′'}
for c in unicodes:
    nc = unicodedata.normalize('NFKD', c)
    if c != nc:
        print(c, nc)
print('meow')
print('\u200b', unicodedata.normalize('NFKD', '\u200b'))
print('\u2002', unicodedata.normalize('NFKD', '\u2002'))
print('\xa0', unicodedata.normalize('NFKD', '\xa0'))
print('\u2009', unicodedata.normalize('NFKD', '\u2009'))
print('meow')
def normalize_text(text):
    ascii_char = [char for char in text if ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z')]
    return ''.join(ascii_char)

with open('data/leetcode/256.json', 'r') as f:
    problem = json.load(f)
    solution = problem['solution']
    print(normalize_text(solution))

print()
with open('data/md/256.md', 'r') as f:
    content = f.read()
    print(normalize_text(content))

print(normalize_text(solution) in normalize_text(content))