import os, glob, re
from datetime import datetime

base_url = "https://mercy-og.github.io/Mercyportfolio"

seo_data = {
    "index.html": {
        "title": "Mercy Ogunwale — Public Health Researcher & Founder",
        "desc": "Mercy Ogunwale is a public health researcher, founder of EPIX Initiative, and educator working at the intersection of evidence and community health in Nigeria."
    },
    "about.html": {
        "title": "About — Mercy Ogunwale",
        "desc": "Learn about Mercy Ogunwale, a dedicated public health researcher and founder of EPIX Initiative, committed to improving community health through evidence-driven solutions."
    },
    "research.html": {
        "title": "Research — Mercy Ogunwale",
        "desc": "Explore the research, peer-reviewed publications, and ongoing public health studies conducted by Mercy Ogunwale, focusing on digital health, HIV/AIDS, and adolescents."
    },
    "projects.html": {
        "title": "Projects — Mercy Ogunwale",
        "desc": "Discover the impactful public health projects led by Mercy Ogunwale, including the Adolescent NCD Watch and initiatives combating health misinformation in Nigeria."
    },
    "epix.html": {
        "title": "EPIX Initiative — Mercy Ogunwale",
        "desc": "The EPIX Initiative, founded by Mercy Ogunwale, is dedicated to training the next generation of African health researchers and developing critical digital health tools."
    },
    "work-with-me.html": {
        "title": "Work With Me — Mercy Ogunwale",
        "desc": "Collaborate with Mercy Ogunwale or access the CeeWriting Service for professional academic and research writing, grant proposals, CVs, and copywriting."
    },
    "gallery.html": {
        "title": "Gallery — Mercy Ogunwale",
        "desc": "View the photo gallery of Mercy Ogunwale, capturing moments from public health outreach, conferences, and community engagement across Nigeria."
    },
    "adolescent-ncd-watch.html": {
        "title": "Adolescent NCD Watch — Mercy Ogunwale",
        "desc": "The Adolescent NCD Watch is a digital health intervention designed to tackle non-communicable diseases among young populations in Nigeria."
    },
    "nigeria_hiv_dashboard.html": {
        "title": "Understanding Nigeria's HIV Epidemic — Dashboard",
        "desc": "An interactive dashboard exploring Nigeria's HIV epidemic, highlighting data, gaps, and advocacy efforts to improve health outcomes."
    },
    "epix_playbook_v2.html": {
        "title": "Playbook 01: Mute Notifications, Not Your Pain | EPIX",
        "desc": "Playbook 01: Mute Notifications, Not Your Pain. An interactive health education playbook by the EPIX Initiative covering puberty, mental health, and digital wellness."
    },
    "echoes.html": {
        "title": "Echoes by EPIX",
        "desc": "Echoes by EPIX: Real stories and insights from the frontlines of public health and youth advocacy."
    }
}

html_files = glob.glob('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/*.html')
today = datetime.today().strftime('%Y-%m-%d')

# 1. Generate Sitemap
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for f in html_files:
    filename = os.path.basename(f)
    priority = "1.0" if filename == "index.html" else "0.8"
    sitemap_content += f'''  <url>
    <loc>{base_url}/{filename}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>\n'''
sitemap_content += '</urlset>'

with open('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_content)
print("Generated sitemap.xml")

# 2. Generate robots.txt
robots_content = f'''User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
'''
with open('C:/Users/lenovo/.gemini/antigravity/scratch/mercy-portfolio/robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("Generated robots.txt")

# 3. Inject SEO tags into HTML
for f in html_files:
    filename = os.path.basename(f)
    if filename not in seo_data:
        continue
        
    data = seo_data[filename]
    title = data['title']
    desc = data['desc']
    url = f"{base_url}/{filename}"
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove existing <title>
    content = re.sub(r'<title>.*?</title>', '', content, flags=re.IGNORECASE)
    # Remove existing <meta name="description"...>
    content = re.sub(r'<meta[^>]*name=["\']description["\'][^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta[^>]*content=["\'][^"\']*["\'][^>]*name=["\']description["\'][^>]*>', '', content, flags=re.IGNORECASE)
    # Remove existing canonical
    content = re.sub(r'<link[^>]*rel=["\']canonical["\'][^>]*>', '', content, flags=re.IGNORECASE)
    # Remove existing OG tags just in case
    content = re.sub(r'<meta[^>]*property=["\']og:[^>]*>', '', content, flags=re.IGNORECASE)

    # Build the ultimate SEO block
    seo_block = f'''
    <!-- Primary Meta Tags -->
    <title>{title}</title>
    <meta name="title" content="{title}">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{base_url}/assets/images/mercy-portrait.png">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{url}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{desc}">
    <meta property="twitter:image" content="{base_url}/assets/images/mercy-portrait.png">
    '''
    
    if '<head>' in content:
        content = content.replace('<head>', '<head>' + seo_block)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Injected SEO tags into {filename}")
    else:
        print(f"Warning: No <head> found in {filename}")

