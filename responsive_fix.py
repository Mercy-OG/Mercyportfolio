import os

workspace = r"c:\Users\lenovo\.gemini\antigravity\scratch\mercy-portfolio"
index_path = os.path.join(workspace, "index.html")
css_path = os.path.join(workspace, "css", "style.css")

# 1. Update index.html
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix right side hero centering
html = html.replace('style="max-width:400px;width:100%;"', 'class="hero-right-img"')

# Fix Research Interests hardcoded grid
html = html.replace('<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:1.5rem;">', '<div class="bento-research">')
html = html.replace('<div style="display:grid;grid-template-rows:repeat(3,1fr);gap:1.5rem;">', '<div class="bento-research-col">')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Add the new classes right before /* ── RESPONSIVE ── */
responsive_marker = "/* ── RESPONSIVE ── */"
new_css = """
.hero-right-img {
  max-width: 400px;
  width: 100%;
}
.bento-research {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.5rem;
}
.bento-research-col {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  gap: 1.5rem;
}

"""

if ".bento-research {" not in css:
    css = css.replace(responsive_marker, new_css + responsive_marker)

# Update responsive section for the new classes and hero improvements
responsive_css_old = """@media(max-width:1024px){
  .hero-inner{grid-template-columns:1fr;gap:3rem}
  .hero-card{display:none}
  .stat-strip{grid-template-columns:repeat(2,1fr)}
  .bento-4{grid-template-columns:repeat(2,1fr)}
}"""

responsive_css_new = """@media(max-width:1024px){
  .hero-inner{grid-template-columns:1fr;gap:3rem;text-align:center;}
  .hero-left { display: flex; flex-direction: column; align-items: center; }
  .hero-subtitle { justify-content: center; }
  .hero-actions { justify-content: center; }
  .hero-right-img { margin: 0 auto; }
  .hero-card{display:none}
  .stat-strip{grid-template-columns:repeat(2,1fr)}
  .bento-4{grid-template-columns:repeat(2,1fr)}
  .bento-research { grid-template-columns: 1fr; }
  .bento-research-col { grid-template-rows: auto; }
}"""

css = css.replace(responsive_css_old, responsive_css_new)

# Add some extra mobile paddings
mobile_old = """@media(max-width:768px){
  section{padding:4rem 0}"""
mobile_new = """@media(max-width:768px){
  section{padding:3.5rem 0}
  .wrap { padding: 0 1.5rem; }
  .hero { padding-top: 120px; }"""
  
if ".wrap { padding: 0 1.5rem;" not in css:
    css = css.replace(mobile_old, mobile_new)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Responsive updates applied!")
