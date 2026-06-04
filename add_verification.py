import os, glob

html_files = glob.glob('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/*.html')

tags_to_add = """<meta name="google-site-verification" content="EeQFnVjDdvsdZPBnb-laEnV4lSJLQq3MkL9d2OUmkxM" />
<meta name="msvalidate.01" content="8967B07B23704F7994FA081CCEC551B5" />"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "google-site-verification" in content:
        print(f"Skipping {os.path.basename(filepath)}, already contains verification tags.")
        continue
        
    # Find the <head> tag and inject right after it
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n{tags_to_add}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Added verification tags to {os.path.basename(filepath)}')
    else:
        print(f'Warning: No <head> tag found in {os.path.basename(filepath)}')
