import os
import glob

workspace = r"c:\Users\lenovo\.gemini\antigravity\scratch\mercy-portfolio"
files = {
    "research.html": "hero_bg_research.png",
    "projects.html": "hero_bg_projects.png",
    "epix.html": "hero_bg_epix.png",
    "work-with-me.html": "hero_bg_work.png"
}

for fname, imgname in files.items():
    path = os.path.join(workspace, fname)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if already added
    if 'page-hero-bg-img' not in html:
        bg_html = f'\n  <div class="page-hero-bg-img" style="background-image:url(\'assets/images/{imgname}\');"></div>'
        html = html.replace('<div class="page-hero">', f'<div class="page-hero">{bg_html}')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {fname}")
