import sys, re
sys.stdout.reconfigure(encoding='utf-8')

SRC = 'epix_playbook_v2.html'
with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Revert my previous injected LOGO_HTML from all locations
def revert_chapter_injection(m):
    print("Reverted injection at:", m.group(1).split('>')[1][:20])
    return '\n      <div ' + m.group(1)

content, n = re.subn(
    r'<div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">\s*<img src="data:image/png;base64,[^"]+" style="width:48px;height:48px;object-fit:contain;" alt="EPIX Logo"/>\s*<div style="font-family:\'Cormorant Garamond\',serif;font-size:13px;color:rgba\(200,168,75,0\.85\);line-height:1\.2;">\s*<strong>EPIX</strong><br><span style="font-style:italic;font-size:10px;opacity:0\.7;">Initiative</span>\s*</div>\s*</div>\n\s*<div ([^>]+>(?:Chapter One|Chapter Two|Chapter Four|A Final Word))',
    revert_chapter_injection,
    content
)
print(f"Reverted {n} previous logo injections")

# 2. Process all original filtered img tags (the placeholders)
def process_filtered_img(m):
    tag = m.group()
    # Is it the footer (width 18px or 32px)?
    if 'width:18px' in tag or 'width:32px' in tag:
        print("Removed footer square")
        return ''
    
    # Is it the one for 'A Final Word' (width 30px)?
    if 'width:30px' in tag or 'width: 30px' in tag:
        print("Removed 'A Final Word' square")
        return ''
        
    # For TOC (width 28px) and Chapter Three (width 24px) - remove filter to show real logo
    new_tag = re.sub(r'filter:[^;"]*;?', '', tag)
    print("Revealed logo by removing filter (width check:", re.search(r'width:\d+px', tag).group() if re.search(r'width:\d+px', tag) else 'unknown', ")")
    return new_tag

pattern = re.compile(r'<img[^>]*?style="[^"]*?filter:[^"]*?"[^>]*?alt="EPIX[^"]*"[^>]*>')
new_content, count = pattern.subn(process_filtered_img, content)
print(f"Processed {count} filtered image tags")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done. File updated.")
