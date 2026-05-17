import os
import shutil
from bs4 import BeautifulSoup

# 1. Update css/style.css with elegant typography for hero
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add Playfair Display import
if 'Playfair+Display' not in css:
    css = css.replace("@import url('https://fonts.googleapis.com/css2?family=Outfit", "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Outfit")

# Update .hero-title
css = css.replace(".hero-title{font-size:clamp(2.8rem,5.5vw,4.8rem);letter-spacing:-2px;margin-bottom:1.5rem;line-height:1.05}", ".hero-title{font-family:'Playfair Display',serif;font-size:clamp(3.5rem,7vw,5.5rem);font-weight:600;letter-spacing:-1px;margin-bottom:1.5rem;line-height:1.1;font-style:italic}")
# Let's make sure the grad still looks good, actually maybe the font-style italic would be elegant.

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Extract About section from index.html to about.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_soup = BeautifulSoup(f.read(), 'html.parser')

about_section = index_soup.find('h2', string=lambda t: t and 'Bridging Knowledge and Action' in t)
if about_section:
    about_section = about_section.find_parent('section')

# Create about.html based on projects.html layout
with open('projects.html', 'r', encoding='utf-8') as f:
    about_soup = BeautifulSoup(f.read(), 'html.parser')

about_soup.title.string = "About — Mercy Ogunwale"
# Remove all sections between header and footer in about.html
for tag in about_soup.find_all('section') + about_soup.find_all('div', class_='page-hero'):
    tag.decompose()

# Insert about_section right after header
hdr = about_soup.find('header')
if about_section and hdr:
    new_about_section = BeautifulSoup(str(about_section), 'html.parser')
    hdr.insert_after(new_about_section)
    # Remove about_section from index.html
    about_section.decompose()

# Update active nav link
for a in about_soup.find_all('a', class_='active'):
    a['class'] = [c for c in a.get('class', []) if c != 'active']
about_nav_link = about_soup.find('nav', id='navLinks').find('a', href='about.html')
if about_nav_link:
    about_nav_link['class'] = about_nav_link.get('class', []) + ['active']

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(str(about_soup))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(index_soup))

# 3. Apply Index.html Content Replacements
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Header / Professional Titles
# Old:
# <span>Founder, EPIX Initiative</span><span class="sep">·</span>
# <span>Educator</span><span class="sep">·</span><span>Researcher</span>
# New:
# <span>BSc Public Health, First Class, Lead City University 2024</span><span class="sep">·</span>
# <span>Founder, EPIX Initiative</span><span class="sep">·</span>
# <span>Founder, Cee Writing Service</span><span class="sep">·</span>
# <span>Public Health Educator & Career Coach</span>

titles_old = """<span>Founder, EPIX Initiative</span><span class="sep">·</span>
<span>Educator</span><span class="sep">·</span><span>Researcher</span>"""
titles_old_soup_str = """<span>Founder, EPIX Initiative</span><span class="sep">·</span>
<span>Educator</span><span class="sep">·</span><span>Researcher</span>"""

soup = BeautifulSoup(index_html, 'html.parser')

hero_subtitle = soup.find('div', class_='hero-subtitle')
if hero_subtitle:
    hero_subtitle.clear()
    hero_subtitle.append(BeautifulSoup("""<span>BSc Public Health, First Class, Lead City University 2024</span><span class="sep">·</span>
<span>Founder, EPIX Initiative</span><span class="sep">·</span>
<span>Founder, Cee Writing Service</span><span class="sep">·</span>
<span>Public Health Educator &amp; Career Coach</span>""", 'html.parser'))

# Hero Bio
hero_hook = soup.find('p', class_='hero-hook-text')
if hero_hook:
    hero_hook.string = "Mercy Ogunwale is a public health professional driven by the belief that the right information reaching the right person can transform community health. She holds a First Class BSc in Public Health from Lead City University and is the founder of EPIX Initiative and Cee Writing Service. She pays rapt attention to everyone she meets, knowing that profound knowledge often comes from unexpected places."

# Research Interests (flat list of 4)
# We will replace the bento-research div
bento_research = soup.find('div', class_='bento-research')
if bento_research:
    new_bento = BeautifulSoup("""<div class="bento bento-2">
      <div class="bento-item reveal" style="padding:1.8rem;display:flex;align-items:center;gap:1.2rem;">
        <div class="i-icon i-teal" style="margin-bottom:0;flex-shrink:0;"><i class="fa-solid fa-virus"></i></div>
        <div><h3 style="margin-bottom:0;">Noncommunicable Diseases</h3></div>
      </div>
      <div class="bento-item reveal" style="padding:1.8rem;display:flex;align-items:center;gap:1.2rem;">
        <div class="i-icon i-amber" style="margin-bottom:0;flex-shrink:0;"><i class="fa-solid fa-people-group"></i></div>
        <div><h3 style="margin-bottom:0;">Adolescent Health</h3></div>
      </div>
      <div class="bento-item reveal" style="padding:1.8rem;display:flex;align-items:center;gap:1.2rem;">
        <div class="i-icon i-blue" style="margin-bottom:0;flex-shrink:0;"><i class="fa-solid fa-mobile-screen-button"></i></div>
        <div><h3 style="margin-bottom:0;">Digital Health Interventions</h3></div>
      </div>
      <div class="bento-item reveal" style="padding:1.8rem;display:flex;align-items:center;gap:1.2rem;">
        <div class="i-icon i-green" style="margin-bottom:0;flex-shrink:0;"><i class="fa-solid fa-flask"></i></div>
        <div><h3 style="margin-bottom:0;">Public Health Research &amp; Development</h3></div>
      </div>
    </div>""", 'html.parser')
    bento_research.replace_with(new_bento)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))


# 4. Apply Research.html Content Replacements
with open('research.html', 'r', encoding='utf-8') as f:
    res_soup = BeautifulSoup(f.read(), 'html.parser')

lead_p = res_soup.find('p', class_='lead')
if lead_p:
    lead_p.string = "I actively contribute to public health literature through continuous research and publication. Below is a record of my conducted studies, authored papers, and ongoing research inquiries."

# Publications Section
pubs_container = res_soup.find('h2', string='Publications & Manuscripts').find_next_sibling('div')
if pubs_container:
    new_pubs = BeautifulSoup("""<div style="display:flex;flex-direction:column;gap:1.2rem;">
      <div class="pub reveal">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap;">
          <div style="flex:1;">
            <p style="font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--teal);margin-bottom:.5rem;">Peer Reviewed Paper</p>
            <h3 style="font-size:1.15rem;margin-bottom:.4rem;">Health provider perspectives on differentiated service delivery for HIV in Oyo State, Nigeria: Exploring the experiences of service providers from a demand perspective.</h3>
            <div class="pub-meta">
              <span><i class="fa-solid fa-book-open"></i> BMC Health Services Research</span>
              <span><i class="fa-solid fa-calendar"></i> 2025</span>
              <span><i class="fa-solid fa-user-pen"></i> Co Author</span>
            </div>
          </div>
          <span class="tag tag-green">Published</span>
        </div>
      </div>
      <div class="pub reveal">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap;">
          <div style="flex:1;">
            <p style="font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--teal);margin-bottom:.5rem;">Peer Reviewed Paper</p>
            <h3 style="font-size:1.15rem;margin-bottom:.4rem;">Therapeutic Potentials of Phytochemicals in Combatting Antimicrobial Resistance (AMR).</h3>
            <div class="pub-meta">
              <span><i class="fa-solid fa-book-open"></i> Asian Journal of Research in Biochemistry</span>
              <span><i class="fa-solid fa-calendar"></i> 2025</span>
              <span><i class="fa-solid fa-user-pen"></i> Co Author</span>
            </div>
          </div>
          <span class="tag tag-green">Published</span>
        </div>
      </div>
      <div class="pub reveal">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;flex-wrap:wrap;">
          <div style="flex:1;">
            <p style="font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--amber);margin-bottom:.5rem;">Manuscript</p>
            <h3 style="font-size:1.15rem;margin-bottom:.4rem;">Generative AI Overreliance and Early Onset Hypertension: A Comparative Analysis of Cognitive Emotional Burden in Young Adults Versus Elderly Populations</h3>
            <div class="pub-meta">
              <span><i class="fa-solid fa-book-open"></i> Target Journal to be decided</span>
              <span><i class="fa-solid fa-user-pen"></i> Author</span>
            </div>
          </div>
          <span class="tag tag-amber">Under Review</span>
        </div>
      </div>
    </div>""", 'html.parser')
    pubs_container.replace_with(new_pubs)


# Conferences Section
conf_container = res_soup.find('h2', string='Conferences & Competitions').find_next_sibling('div')
if conf_container:
    new_conf = BeautifulSoup("""<div style="display:flex;flex-direction:column;gap:1.2rem;margin-top:2rem;">
      <div class="conf-row reveal">
        <div class="conf-ico i-blue"><i class="fa-solid fa-microphone-lines"></i></div>
        <div style="flex:1;">
          <p style="font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--blue);margin-bottom:.4rem;">Conference</p>
          <h3 style="font-size:1.15rem;margin-bottom:.5rem;">Mapping Ethical Landscapes: A study on Ethical Guidelines in Africa</h3>
          <p style="font-size:.9rem;color:var(--ink-3);margin-bottom:.4rem;"><i class="fa-solid fa-location-dot"></i> Nigeria Institute of Medical Research, Lagos State, Dec 2023 &nbsp;·&nbsp; <strong>Role:</strong> Presenter</p>
          <p style="font-size:.88rem;color:var(--ink-4);">Delivered a presentation on ethical guidelines within the African medical landscape.</p>
        </div>
      </div>
      <div class="conf-row reveal">
        <div class="conf-ico i-amber"><i class="fa-solid fa-trophy"></i></div>
        <div style="flex:1;">
          <p style="font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:var(--amber);margin-bottom:.4rem;">Competition</p>
          <h3 style="font-size:1.15rem;margin-bottom:.5rem;">SI TEST 4YBY MEGA DESIGNATHON</h3>
          <p style="font-size:.9rem;color:var(--ink-3);margin-bottom:.4rem;"><i class="fa-solid fa-calendar"></i> 2024 &nbsp;·&nbsp; Team of Four</p>
          <p style="font-size:.88rem;color:var(--ink-3);">Developed a solution aimed at reducing HIV among at risk populations.</p>
        </div>
      </div>
    </div>""", 'html.parser')
    conf_container.replace_with(new_conf)

with open('research.html', 'w', encoding='utf-8') as f:
    f.write(str(res_soup))

print("Applied updates successfully.")
