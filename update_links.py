import os, glob, re

# Update ceewriting links globally
html_files = glob.glob('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update Footer link
    content = content.replace('<a href="work-with-me.html">CeeWriting Service</a>', '<a href="https://ceewriting.com" target="_blank">CeeWriting Service</a>')
    
    # Update button on work-with-me.html
    content = content.replace('<a class="btn btn-primary" href="#"><i class="fa-solid fa-arrow-up-right-from-square"></i> Visit \nCeeWriting Service</a>', '<a class="btn btn-primary" href="https://ceewriting.com" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i> Visit \nCeeWriting Service</a>')
    content = content.replace('<a class="btn btn-primary" href="#"><i class="fa-solid fa-arrow-up-right-from-square"></i> Visit CeeWriting Service</a>', '<a class="btn btn-primary" href="https://ceewriting.com" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i> Visit CeeWriting Service</a>')
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated ceewriting links in {os.path.basename(filepath)}')

# Update research.html specifically for the "Click to view" links
research_path = 'C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/research.html'
with open(research_path, 'r', encoding='utf-8') as f:
    r_content = f.read()

# Add to Project Shield Final Report
r_content = r_content.replace(
    '<p style="font-size:.9rem;color:var(--ink-3);">A comprehensive independent report detailing the outcomes and impact of Project Shield.</p>\n</div>',
    '<p style="font-size:.9rem;color:var(--ink-3);margin-bottom:.8rem;">A comprehensive independent report detailing the outcomes and impact of Project Shield.</p>\n<div class="pub-meta">\n  <span><a href="ProjectShield_Final.pdf" target="_blank" style="color:var(--teal); font-weight:600;"><i class="fa-solid fa-file-pdf"></i> Click to View Full PDF</a></span>\n</div>\n</div>'
)

# Add to Playbook 01
r_content = r_content.replace(
    '<p style="font-size:.88rem;color:var(--ink-3);">An interactive web-based playbook covering key adolescent health topics including puberty, mental health, and digital wellness.</p>\n</div>',
    '<p style="font-size:.88rem;color:var(--ink-3);margin-bottom:.8rem;">An interactive web-based playbook covering key adolescent health topics including puberty, mental health, and digital wellness.</p>\n<div class="pub-meta">\n  <span><a href="epix_playbook_v2.html" target="_blank" style="color:var(--teal); font-weight:600;"><i class="fa-solid fa-laptop-code"></i> Click to View Interactive Playbook</a></span>\n</div>\n</div>'
)

# Add to EPIX Brochure
r_content = r_content.replace(
    '<p style="font-size:.88rem;color:var(--ink-3);">An instructional flyer and brochure used during outreach programs to teach communities the process of making soap.</p>\n</div>',
    '<p style="font-size:.88rem;color:var(--ink-3);margin-bottom:.8rem;">An instructional flyer and brochure used during outreach programs to teach communities the process of making soap.</p>\n<div class="pub-meta">\n  <span><a href="Designed by EPIX Bronchure.pdf" target="_blank" style="color:var(--teal); font-weight:600;"><i class="fa-solid fa-file-pdf"></i> Click to View PDF Brochure</a></span>\n</div>\n</div>'
)

with open(research_path, 'w', encoding='utf-8') as f:
    f.write(r_content)
print("Added explicit 'Click to view' links in research.html")
