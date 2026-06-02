import re
import os

with open('playbook_clean.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Split by page divs and capture their attributes
parts = re.split(r'<div class="page"([^>]*)>', content)

print(f"Split results size: {len(parts)}")

# parts[0] is everything before the first page div (head and style)
# parts[1] is page 1 attributes, parts[2] is page 1 body
# parts[3] is page 2 attributes, parts[4] is page 2 body
# ...
# For 16 pages, we should have 1 + 2*16 = 33 parts.

# Let's verify:
num_pages = (len(parts) - 1) // 2
print(f"Number of parsed pages: {num_pages}")

# Clean up styles inside parts[0]
head_part = parts[0]

# We will construct a new stylesheet at the end of parts[0]'s style block
# Let's find where </style> is in head_part
style_end_idx = head_part.find('</style>')

new_css = """
/* ── BOOK SPREAD VIEWPORT & CONTROLS ── */
body {
  background: #ccd5d0;
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
}

/* Toolbar Header */
.book-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: rgba(13, 61, 42, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(200, 168, 75, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  z-index: 1000;
  color: white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.tb-left, .tb-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.tb-center {
  display: flex;
  gap: 8px;
}
.tb-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #e8f2ec;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  transition: all 0.2s ease;
}
.tb-btn:hover {
  background: rgba(200, 168, 75, 0.15);
  border-color: var(--gold);
  color: white;
}
.tb-btn.active {
  background: var(--gold);
  color: var(--green);
  border-color: var(--gold);
  font-weight: 600;
}
.tb-page-info {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  color: var(--gold-light);
  margin-right: 12px;
}

/* Book Spread Container */
.book-container {
  margin-top: 60px;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: calc(100vh - 60px);
}

.spread-wrapper {
  display: none;
  justify-content: center;
  position: relative;
  transition: opacity 0.3s ease;
}
.spread-wrapper.active {
  display: flex;
}

/* Pages in Spreads */
.page {
  margin: 0;
  width: 794px;
  height: 1123px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
  transition: transform 0.2s ease;
}

/* Left/Right Book Page Styling */
.page.left-page {
  border-radius: 6px 0 0 6px;
  box-shadow: -15px 15px 40px rgba(0,0,0,0.1);
  border-right: 1px solid rgba(0,0,0,0.05);
}
.page.right-page {
  border-radius: 0 6px 6px 0;
  box-shadow: 15px 15px 40px rgba(0,0,0,0.1);
}
.page.cover-page {
  border-radius: 6px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.18);
}

/* Fold Shadow Seam Overlay */
.spread-wrapper::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 24px;
  transform: translateX(-50%);
  background: linear-gradient(to right, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,0) 75%, rgba(0,0,0,0.15) 100%);
  z-index: 10;
  pointer-events: none;
}
/* Disable seam for single page cover/back-cover */
.spread-wrapper.single::after {
  display: none;
}

/* ── IMAGE WRAPPERS FOR PINTEREST STYLE LOOK ── */
.playbook-img-card {
  margin: 14px 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--gray-2);
  background: var(--white);
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.playbook-img-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}
.playbook-img-card .img-caption {
  padding: 10px 14px;
  font-size: 8.5px;
  color: var(--muted);
  font-family: 'Space Grotesk', sans-serif;
  letter-spacing: 0.05em;
  background: var(--off);
  border-top: 0.5px solid var(--gray-2);
  line-height: 1.4;
}

/* Single Mode Stacking styling */
.book-container.single-mode .spread-wrapper {
  display: flex !important;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
}
.book-container.single-mode .spread-wrapper::after {
  display: none;
}
.book-container.single-mode .page {
  border-radius: 6px;
  margin-bottom: 20px;
}

/* ── RESPONSIVE SCALING ── */
@media (max-width: 1650px) {
  .spread-wrapper {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
  .spread-wrapper::after {
    display: none;
  }
  .page.left-page, .page.right-page {
    border-radius: 6px;
  }
  /* Fallback spread alignment */
  .book-container:not(.single-mode) .spread-wrapper.active {
    display: flex;
  }
}

@media (max-width: 840px) {
  .book-toolbar {
    padding: 0 12px;
    height: 50px;
  }
  .book-container {
    margin-top: 50px;
    padding: 20px 10px;
  }
  .page {
    width: 100%;
    max-width: 500px;
    height: auto;
    min-height: 700px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
  }
  .tb-btn {
    padding: 6px 10px;
    font-size: 11px;
  }
  .tb-page-info {
    font-size: 11px;
    margin-right: 4px;
  }
  .pad {
    padding: 24px 20px;
  }
  .rh {
    padding: 12px 20px;
  }
  .rf {
    padding: 0 20px;
    position: relative;
    margin-top: 20px;
  }
}
"""

cleaned_head = head_part[:style_end_idx] + new_css + head_part[style_end_idx:]

# Parse pages
pages = []
for i in range(1, len(parts), 2):
    attrs = parts[i]
    body = parts[i+1]
    
    # We clean base64 image placeholders in attributes and body
    body_cleaned = body.replace('[BASE64_IMAGE_DATA]', 'assets/images/epix-logo.png')
    
    pages.append({
        'index': (i + 1) // 2,
        'attrs': attrs,
        'body': body_cleaned
    })

print(f"Processed {len(pages)} pages.")

# Rebuild pages into spreads
spreads_html = []

# Page 1: Cover (Single Spread 0)
spreads_html.append(f"""
<!-- Spread 0: Cover Page -->
<div class="spread-wrapper active single" id="spread0">
  <div class="page cover-page" style="padding:0;background:#0d3d2a">
    <img src="assets/images/playbook_cover.png" style="width:100%;height:100%;object-fit:cover;display:block;min-height:1123px" alt="Mute Notifications, Not Your Pain — Playbook 01">
  </div>
</div>
""")

# Page 3 (Welcome) content image insertion
page_3_body = pages[2]['body']
image_card_welcome = """
        <div class="playbook-img-card">
          <img src="assets/images/shield_mercy_stage.jpg" alt="Mercy Ogunwale - Project SHIELD Stage Presentation">
          <div class="img-caption">REAL IMPACT · Mercy Ogunwale presenting hygiene and health strategies to students during Project SHIELD.</div>
        </div>
"""
right_col_match = re.search(r'<div style="display:flex;flex-direction:column;gap:14px">', page_3_body)
if right_col_match:
    idx = right_col_match.end()
    page_3_body = page_3_body[:idx] + image_card_welcome + page_3_body[idx:]
pages[2]['body'] = page_3_body

# Page 4 (Ch 1 Opener) image insertion
page_4_body = pages[3]['body']
svg_pattern = r'<svg.*?</svg>'
growth_img_html = """
      <div style="width:280px;height:440px;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.12);background:var(--white)">
        <img src="assets/images/playbook_growth.png" style="width:100%;height:100%;object-fit:cover;display:block" alt="Growth and Puberty Illustration">
      </div>
"""
page_4_body = re.sub(svg_pattern, growth_img_html, page_4_body, flags=re.DOTALL)
pages[3]['body'] = page_4_body

# Page 5 image insertion
page_5_body = pages[4]['body']
image_card_growth = """
        <div class="playbook-img-card">
          <img src="assets/images/shield_gracedieu_students_group.jpg" alt="Project SHIELD Adolescent Students Group">
          <div class="img-caption">COMMUNITY · High school students engaged in peer health discussions during the Grace Dieu workshop.</div>
        </div>
"""
right_col_match = re.search(r'<div style="display:flex;flex-direction:column;gap:14px">', page_5_body)
if right_col_match:
    idx = right_col_match.end()
    page_5_body = page_5_body[:idx] + image_card_growth + page_5_body[idx:]
pages[4]['body'] = page_5_body

# Page 6 image insertion
page_6_body = pages[5]['body']
image_card_hygiene = """
        <div class="playbook-img-card" style="margin-bottom: 20px;">
          <img src="assets/images/shield_students_soap.jpg" alt="Students learning handwashing">
          <div class="img-caption">PRACTICAL HYGIENE · Project SHIELD students practicing correct hand sanitation methods using soap.</div>
        </div>
"""
two_col_match = re.search(r'<div class="two-col" style="gap:30px">', page_6_body)
if two_col_match:
    idx = two_col_match.start()
    page_6_body = page_6_body[:idx] + image_card_hygiene + page_6_body[idx:]
pages[5]['body'] = page_6_body

# Page 8 image insertion
page_8_body = pages[7]['body']
image_card_sex_health = """
        <div class="playbook-img-card">
          <img src="assets/images/shield_excellent_teaching.jpg" alt="Health education session on relationships and respect">
          <div class="img-caption">EDUCATION · Practical health seminar addressing adolescent topics and respect in Nigeria.</div>
        </div>
"""
right_col_match = re.search(r'<div>\s*<div class="tag">Romantic Relationships</div>', page_8_body)
if right_col_match:
    idx = right_col_match.start() + len('<div>')
    page_8_body = page_8_body[:idx] + image_card_sex_health + page_8_body[idx:]
pages[7]['body'] = page_8_body

# Page 9 image insertion
page_9_body = pages[8]['body']
mental_img_html = """
      <div style="width:280px;height:440px;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.12);background:var(--white)">
        <img src="assets/images/playbook_mental_health.png" style="width:100%;height:100%;object-fit:cover;display:block" alt="Mental Health and Mind Illustration">
      </div>
"""
page_9_body = re.sub(svg_pattern, mental_img_html, page_9_body, flags=re.DOTALL)
pages[8]['body'] = page_9_body

# Page 10 image insertion
page_10_body = pages[9]['body']
image_card_mental = """
        <div class="playbook-img-card">
          <img src="assets/images/shield_excellent_listening.jpg" alt="Student listening to health mentorship session">
          <div class="img-caption">SUPPORTIVE CARE · Empathy and active listening are key pillars of the mental health support system.</div>
        </div>
"""
left_col_match = re.search(r'<div class="two-col" style="gap:36px">', page_10_body)
if left_col_match:
    idx = left_col_match.end()
    page_10_body = page_10_body[:idx] + image_card_mental + page_10_body[idx:]
pages[9]['body'] = page_10_body

# Page 12 image insertion
page_12_body = pages[11]['body']
digital_img_html = """
      <div style="width:280px;height:440px;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.12);background:var(--white)">
        <img src="assets/images/playbook_digital.png" style="width:100%;height:100%;object-fit:cover;display:block" alt="Digital Wellness Illustration">
      </div>
"""
page_12_body = re.sub(svg_pattern, digital_img_html, page_12_body, flags=re.DOTALL)
pages[11]['body'] = page_12_body

# Page 13 image insertion
page_13_body = pages[12]['body']
image_card_digital = """
        <div class="playbook-img-card">
          <img src="assets/images/cv_workshop_testimonials.png" alt="Digital health safety workshop chat session">
          <div class="img-caption">DIGITAL CONNECTION · Real-life workshop feedback showing impact and screen health awareness.</div>
        </div>
"""
right_col_match = re.search(r'<div>\s*<div class="tag">Digital Hygiene</div>', page_13_body)
if right_col_match:
    idx = right_col_match.start() + len('<div>')
    page_13_body = page_13_body[:idx] + image_card_digital + page_13_body[idx:]
pages[12]['body'] = page_13_body

# Page 14 image insertion
page_14_body = pages[13]['body']
relationships_img_html = """
      <div style="width:280px;height:440px;border-radius:12px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.12);background:var(--white)">
        <img src="assets/images/playbook_relationships.png" style="width:100%;height:100%;object-fit:cover;display:block" alt="Healthy Relationships Illustration">
      </div>
"""
page_14_body = re.sub(svg_pattern, relationships_img_html, page_14_body, flags=re.DOTALL)
pages[13]['body'] = page_14_body

# Page 15 image insertion
page_15_body = pages[14]['body']
image_card_rel = """
        <div class="playbook-img-card">
          <img src="assets/images/shield_gracedieu_students_all.jpg" alt="Students and educators group portrait">
          <div class="img-caption">TRUST & RESPECT · High school student community celebrating graduation at the end of Project SHIELD.</div>
        </div>
"""
left_col_match = re.search(r'<div class="two-col" style="gap:36px">', page_15_body)
if left_col_match:
    idx = left_col_match.end()
    page_15_body = page_15_body[:idx] + image_card_rel + page_15_body[idx:]
pages[14]['body'] = page_15_body

# Compile spreads 1-7
for spread_num in range(1, 8):
    left_idx = (spread_num * 2) - 1
    right_idx = left_idx + 1
    
    left_p = pages[left_idx]
    right_p = pages[right_idx]
    
    spread_html = f"""
<!-- Spread {spread_num}: Pages {left_p['index']} & {right_p['index']} -->
<div class="spread-wrapper" id="spread{spread_num}">
  <div class="page left-page"{left_p['attrs']}>
    {left_p['body']}
  </div>
  <div class="page right-page"{right_p['attrs']}>
    {right_p['body']}
  </div>
</div>
"""
    spreads_html.append(spread_html)

# Page 16 (Closing) and Page 17 (Back Cover)
p16 = pages[15]

page_17_html = """
<div class="page right-page" style="background:var(--green)">
  <div style="min-height:1123px;display:flex;flex-direction:column;justify-content:space-between;padding:68px 58px;text-align:center">
    <div></div>
    <div>
      <div style="width:140px;height:140px;margin:0 auto 24px;border-radius:50%;background:rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:center;box-shadow:0 8px 30px rgba(0,0,0,0.15)">
        <img src="assets/images/epix-logo.png" style="width:100px;height:100px;object-fit:contain;filter:brightness(0) invert(1)" alt="EPIX Logo">
      </div>
      <h2 style="font-family:'Cormorant Garamond',serif;font-size:32px;font-weight:700;color:white;letter-spacing:0.04em;margin-bottom:8px">The EPIX Initiative</h2>
      <p style="font-size:11px;color:#8aaa9a;letter-spacing:0.18em;text-transform:uppercase;font-family:'Space Grotesk',sans-serif;margin-bottom:30px">Evidence-Based Adolescent Education</p>
      <div style="width:40px;height:2px;background:var(--gold);margin:0 auto 30px"></div>
    </div>
    <div>
      <div style="background:white;padding:12px 20px;border-radius:4px;display:inline-block;margin-bottom:20px;box-shadow:0 4px 10px rgba(0,0,0,0.1)">
        <div style="font-family:'Courier New',Courier,monospace;font-size:24px;letter-spacing:1px;color:black;font-weight:bold;margin-bottom:2px">||| | |||| | ||| || |</div>
        <div style="font-size:8px;letter-spacing:0.1em;color:var(--muted)">ISBN 978-01-EPIX-2025</div>
      </div>
      <div style="font-size:10.5px;color:#8aaa9a;line-height:1.7;font-weight:300;margin-bottom:20px">
        Written by Mercy Ogunwale, Founder &amp; Product Lead<br>
        Web: <a href="index.html" style="color:var(--gold);text-decoration:none">www.mercyogunwale.com</a><br>
        Email: contact@mercyogunwale.com
      </div>
      <div style="font-size:8px;color:#3a5a4a;letter-spacing:0.06em">
        © 2025 The EPIX Initiative. All rights reserved.<br>
        Mute Notifications, Not Your Pain · Health Series
      </div>
    </div>
  </div>
</div>
"""

spreads_html.append(f"""
<!-- Spread 8: Pages 16 & 17 -->
<div class="spread-wrapper" id="spread8">
  <div class="page left-page"{p16['attrs']}>
    {p16['body']}
  </div>
  {page_17_html}
</div>
""")

all_spreads_content = "\n".join(spreads_html)

toolbar_html = """
<div class="book-toolbar">
  <div class="tb-left">
    <a href="index.html" class="tb-btn"><i class="fa-solid fa-house"></i> Home</a>
    <a href="epix.html" class="tb-btn"><i class="fa-solid fa-arrow-left"></i> EPIX Initiative</a>
  </div>
  <div class="tb-center">
    <button class="tb-btn active" id="btnSpread" onclick="setViewMode('spread')"><i class="fa-solid fa-book-open"></i> Spread View</button>
    <button class="tb-btn" id="btnSingle" onclick="setViewMode('single')"><i class="fa-solid fa-scroll"></i> Single Page View</button>
  </div>
  <div class="tb-right">
    <span class="tb-page-info" id="pageInfo">Spread 1 of 9</span>
    <button class="tb-btn" onclick="prevSpread()"><i class="fa-solid fa-chevron-left"></i> Prev</button>
    <button class="tb-btn" onclick="nextSpread()">Next <i class="fa-solid fa-chevron-right"></i></button>
    <button class="tb-btn print-btn" onclick="window.print()"><i class="fa-solid fa-print"></i> Print / PDF</button>
  </div>
</div>
"""

font_awesome_link = '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">'
cleaned_head = cleaned_head.replace('</head>', f'{font_awesome_link}\n</head>')

# Slice head part safely up to <body> and combine it with the spreads content
body_idx = cleaned_head.find('<body>')
if body_idx != -1:
    html_head = cleaned_head[:body_idx]
else:
    html_head = cleaned_head

# Re-assemble body as standard strings
final_body = """
<body>

""" + toolbar_html + """

<div class="book-container" id="bookContainer">
  """ + all_spreads_content + """
</div>

<script>
  let activeSpread = 0;
  const spreads = document.querySelectorAll('.spread-wrapper');
  let currentMode = 'spread';

  function showSpread(index) {
    if (index < 0 || index >= spreads.length) return;
    spreads.forEach((s, idx) => {
      if (currentMode === 'spread') {
        s.style.display = idx === index ? 'flex' : 'none';
      }
    });
    activeSpread = index;
    document.getElementById('pageInfo').innerText = `Spread ${activeSpread + 1} of ${spreads.length}`;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function prevSpread() {
    if (activeSpread > 0) {
      showSpread(activeSpread - 1);
    }
  }

  function nextSpread() {
    if (activeSpread < spreads.length - 1) {
      showSpread(activeSpread + 1);
    }
  }

  function setViewMode(mode) {
    currentMode = mode;
    const container = document.getElementById('bookContainer');
    
    if (mode === 'single') {
      document.getElementById('btnSingle').classList.add('active');
      document.getElementById('btnSpread').classList.remove('active');
      container.classList.add('single-mode');
      spreads.forEach(s => {
        s.style.display = 'flex';
      });
      document.getElementById('pageInfo').innerText = 'All Pages';
    } else {
      document.getElementById('btnSpread').classList.add('active');
      document.getElementById('btnSingle').classList.remove('active');
      container.classList.remove('single-mode');
      showSpread(activeSpread);
    }
  }

  // Handle keyboard arrow keys
  document.addEventListener('keydown', (e) => {
    if (currentMode === 'spread') {
      if (e.key === 'ArrowLeft') {
        prevSpread();
      } else if (e.key === 'ArrowRight') {
        nextSpread();
      }
    }
  });

  // Initialize
  showSpread(0);
</script>
</body>
"""

full_html = html_head + final_body + "\n</html>"

with open('epix_playbook_v2.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Playbook compiled successfully!")
print(f"Final file size: {os.path.getsize('epix_playbook_v2.html')} bytes")
