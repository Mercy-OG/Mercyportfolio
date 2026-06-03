"""
Update epix_playbook_v2.html:
  1. Replace the 3 animated SVG illustrations with PNG images
  2. Fill placeholder squares (logo-placeholder divs / empty icon areas) with the EPIX logo
  3. Ensure logo appears on every chapter opener header
"""

import re
import sys
import base64
import os

sys.stdout.reconfigure(encoding='utf-8')

SRC = 'epix_playbook_v2.html'

def load_img_as_base64(path):
    with open(path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('ascii')

def compile():
    with open(SRC, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Loaded {SRC}: {len(content)} bytes")

    # ──────────────────────────────────────────────────
    # 1. Load PNG images as base64
    # ──────────────────────────────────────────────────
    puberty_b64  = load_img_as_base64('images/playbook_puberty.png')
    mental_b64   = load_img_as_base64('images/playbook_mental.png')
    digital_b64  = load_img_as_base64('images/playbook_digital.png')
    print("Loaded 3 PNG illustrations as base64")

    # Build the <img> replacement tags
    IMG_STYLE = 'style="max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block;"'

    img_puberty  = f'<img src="data:image/png;base64,{puberty_b64}" {IMG_STYLE} alt="Puberty illustration"/>'
    img_mental   = f'<img src="data:image/png;base64,{mental_b64}" {IMG_STYLE} alt="Mental health illustration"/>'
    img_digital  = f'<img src="data:image/png;base64,{digital_b64}" {IMG_STYLE} alt="Digital wellness illustration"/>'

    # ──────────────────────────────────────────────────
    # 2. Find and replace the 3 SVG blocks
    # ──────────────────────────────────────────────────
    # We only want the LARGE illustration SVGs (width > 100), not toolbar icons (13x13)
    svg_pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)
    all_svgs = list(svg_pattern.finditer(content))
    print(f"Found {len(all_svgs)} total SVG blocks")

    # Filter to large illustration SVGs (skip toolbar icons which are 13x13 or small)
    illustration_svgs = []
    for m in all_svgs:
        tag_header = m.group()[:200]
        # Check if it has width > 100 (illustration) vs width=13 (toolbar icon)
        width_match = re.search(r'width="(\d+)"', tag_header)
        if width_match:
            w = int(width_match.group(1))
            if w > 100:
                illustration_svgs.append(m)
                print(f"  Illustration SVG: width={w}, pos={m.start()}")
            else:
                print(f"  Toolbar SVG (skipped): width={w}")

    if len(illustration_svgs) < 3:
        print(f"ERROR: Expected at least 3 illustration SVGs, found {len(illustration_svgs)}!")
        return False

    # Replace in reverse order so positions don't shift
    replacements = [
        (illustration_svgs[0].start(), illustration_svgs[0].end(), img_puberty),
        (illustration_svgs[1].start(), illustration_svgs[1].end(), img_mental),
        (illustration_svgs[2].start(), illustration_svgs[2].end(), img_digital),
    ]
    for start, end, replacement in reversed(replacements):
        content = content[:start] + replacement + content[end:]
    print("Replaced 3 illustration SVG blocks with PNG img tags")

    # ──────────────────────────────────────────────────
    # 3. Find placeholder squares and replace with logo
    # ──────────────────────────────────────────────────
    # From inspection, placeholder squares appear as:
    # - Empty divs with a muted background (sage green) on chapter opener top-left
    # - Specifically on pages where logo should sit but is missing
    # We look for specific patterns in chapter opener LEFT panels
    #
    # Pattern A: Divs that serve as a logo placeholder (explicit comment or empty green square)
    # Pattern B: The top-left corner area of chapter openers that has no logo img

    # Extract the EPIX logo from any existing page header (it's embedded as base64 already)
    # Find the logo base64 data from the existing running header <img>
    logo_match = re.search(
        r'<img src="(data:image/png;base64,[^"]+)"[^>]*alt="EPIX"',
        content
    )
    if logo_match:
        logo_src = logo_match.group(1)
        print(f"Found existing EPIX logo in page headers (length={len(logo_src)})")
    else:
        print("WARNING: Could not find EPIX logo in page headers")
        logo_src = None

    # ──────────────────────────────────────────────────
    # 4. Fix chapter opener LEFT panels: add logo at top
    # ──────────────────────────────────────────────────
    # Chapter One (page index 3): left panel starts with:
    #   <div style="display:flex;flex-direction:column;background:#0a2e1c">
    #   Then a flex:1 illustration area, then title area with "Chapter One" label
    #
    # From user screenshots: the SAGE GREEN SQUARE appears to be an image placeholder
    # that shows up in the illustration area. We need to add the logo ABOVE the illustration
    # or fill an existing empty space at the top.
    #
    # The screenshot shows:
    # - A square in the upper area of the page (top-left quadrant)
    # - Text "CHAPTER THREE" / "A FINAL WORD" next to or below it
    # This suggests the square IS the logo position — a colored square with no img inside.
    #
    # Let's look for: <div style="...background..."> that immediately wraps text like "Chapter X"
    # and inject a logo BEFORE that text in each chapter opener's label area.

    LOGO_HTML = ''
    if logo_src:
        LOGO_HTML = f'''<div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
  <img src="{logo_src}" style="width:48px;height:48px;object-fit:contain;" alt="EPIX Logo"/>
  <div style="font-family:'Cormorant Garamond',serif;font-size:13px;color:rgba(200,168,75,0.85);line-height:1.2;">
    <strong>EPIX</strong><br><span style="font-style:italic;font-size:10px;opacity:0.7;">Initiative</span>
  </div>
</div>'''
    else:
        LOGO_HTML = '''<div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
  <div style="width:48px;height:48px;background:#c8a84b;border-radius:4px;display:flex;align-items:center;justify-content:center;">
    <span style="font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:700;color:#0d3d2a;">E</span>
  </div>
  <div style="font-family:'Cormorant Garamond',serif;font-size:13px;color:rgba(200,168,75,0.85);line-height:1.2;">
    <strong>EPIX</strong><br><span style="font-style:italic;font-size:10px;opacity:0.7;">Initiative</span>
  </div>
</div>'''

    # Now inject logo into each chapter opener's title panel
    # Target: the div that contains the chapter label text, e.g. "Chapter One", "Chapter Two" etc.
    # Each has: font-size:8px;letter-spacing:0.18em;...>Chapter X</div>
    
    chapter_label_pattern = re.compile(
        r'(<div style="[^"]*font-size:8px[^"]*letter-spacing[^"]*">(?:Chapter One|Chapter Two|Chapter Three|Chapter Four|A Final Word))',
        re.DOTALL
    )
    
    def inject_logo(m):
        return LOGO_HTML + '\n      ' + m.group(1)
    
    new_content, count = chapter_label_pattern.subn(inject_logo, content)
    print(f"Injected logo before {count} chapter/section labels")
    content = new_content

    # ──────────────────────────────────────────────────
    # 5. Also check for any explicit placeholder square divs
    # ──────────────────────────────────────────────────
    # Look for divs that match: small fixed-size, sage/muted green background
    # These might look like: <div style="width:80px;height:80px;background:#5a7a6a..."></div>
    # or similar sage-colored empty boxes
    placeholder_pattern = re.compile(
        r'<div style="[^"]*background(?:-color)?:\s*(?:#[5-8][0-9a-fA-F]{5}|rgba?\(\s*[5-9]\d[^)]*\))[^"]*(?:width|height):\s*(?:[6-9]\d|1[0-2]\d)px[^"]*">\s*</div>'
    )
    placeholder_matches = list(placeholder_pattern.finditer(content))
    print(f"Found {len(placeholder_matches)} potential placeholder square divs")

    # ──────────────────────────────────────────────────
    # 6. Write output
    # ──────────────────────────────────────────────────
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(content)

    size = os.path.getsize(SRC)
    print(f"\n[OK] Updated successfully: {SRC}")
    print(f"  Size: {size:,} bytes ({size/1024:.1f} KB)")
    
    # Verify
    svg_remaining = len(list(re.finditer(r'<svg\b', content)))
    img_count = content.count('<img ')
    print(f"  Remaining SVG tags: {svg_remaining}")
    print(f"  Total img tags: {img_count}")
    print(f"  Logo injections: {count}")
    
    return True

if __name__ == '__main__':
    success = compile()
    sys.exit(0 if success else 1)
