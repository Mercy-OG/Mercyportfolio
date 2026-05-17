import os
import glob

workspace = r"c:\Users\lenovo\.gemini\antigravity\scratch\mercy-portfolio"
html_files = glob.glob(os.path.join(workspace, "*.html"))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add Favicon
    if 'rel="icon"' not in html:
        html = html.replace('</head>', '  <link rel="icon" type="image/png" href="assets/images/mercy-portrait.png">\n</head>')
    
    # 2. Update Logo (both Header and Footer)
    html = html.replace('<span class="logo-dot"></span>', '<img src="assets/images/mercy-portrait.png" class="logo-img" alt="Mercy Ogunwale">')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

# 3. Add CSS for logo-img
css_path = os.path.join(workspace, "css", "style.css")
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

if '.logo-img' not in css:
    css_addition = """
.logo-img {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--teal);
  box-shadow: 0 0 0 2px rgba(255,107,0,0.2);
}
"""
    # Find .logo-dot and append after it
    css = css.replace('.logo-dot{', css_addition + '.logo-dot{')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)

print("Favicon and Logo updated successfully!")
