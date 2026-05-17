import os
import glob

html_files = glob.glob(r"c:\Users\lenovo\.gemini\antigravity\scratch\mercy-portfolio\*.html")

for html_path in html_files:
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace inline teal/blue rgba with orange rgba
    html = html.replace('rgba(13,148,136,', 'rgba(255,107,0,')
    html = html.replace('rgba(2,132,199,', 'rgba(255,140,51,')
    html = html.replace('rgba(245,158,11,', 'rgba(255,107,0,') # amber

    # Replace inline colors
    html = html.replace('color:var(--ink-3)', 'color:var(--ink-3)') # stays same
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
print(f"Updated {len(html_files)} HTML files.")
