import os, glob

fixes = {
    'â€”': '—',
    'â€“': '–',
    'â€™': '’',
    'â€˜': '‘',
    'â€œ': '“',
    'â€': '”',
    'â€¦': '…',
    'Ã©': 'é'
}

html_files = glob.glob('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for bad, good in fixes.items():
        content = content.replace(bad, good)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed encoding issues in {os.path.basename(filepath)}')
