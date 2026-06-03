import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('epix_playbook_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract the logo img tag from Chapter Three
ch3_idx = content.find('Chapter Three')
# Find the img tag right before it
img_match = re.search(r'(<img src="data:image/png;base64,[^"]+" style="width:24px;height:24px;object-fit:contain;opacity:0\.6" alt="EPIX">)', content[:ch3_idx])
if not img_match:
    print("Could not find Chapter 3 logo image!")
    sys.exit(1)

logo_img = img_match.group(1)
print(f"Extracted logo img tag, length: {len(logo_img)}")

# 2. Add it to Chapter One, Two, Four, Five
chapters = [
    ('Chapter One', 'var(--gold)', '10px'),
    ('Chapter Two', 'var(--green)', '16px'),
    ('Chapter Four', 'var(--gold)', '14px'),
    ('Chapter Five', 'var(--green)', '16px'),
]

for ch, color, mb in chapters:
    # Look for: <div style="font-size:8px;letter-spacing:0.18em;color:var(--gold);text-transform:uppercase;margin-bottom:10px;font-family:'Space Grotesk',sans-serif">Chapter One</div>
    # Note: color and margin-bottom vary
    pattern = re.compile(
        r'<div style="font-size:8px;letter-spacing:0\.18em;color:' + re.escape(color) + 
        r';text-transform:uppercase;margin-bottom:' + mb + 
        r';font-family:\'Space Grotesk\',sans-serif">' + ch + r'</div>'
    )
    
    def replace_ch(m):
        return f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:{mb}">{logo_img}<span style="font-size:8px;letter-spacing:0.18em;color:{color};text-transform:uppercase;font-family:\'Space Grotesk\',sans-serif">{ch}</span></div>'
    
    new_content, count = pattern.subn(replace_ch, content)
    if count == 0:
        print(f"Warning: Could not replace {ch}!")
    else:
        print(f"Replaced {ch}")
    content = new_content

# 3. Add to A Final Word
# Look for:
# <div style="display:flex;align-items:center;gap:10px;margin-bottom:28px">\s*<div style="font-size:8px;letter-spacing:0.2em;color:var(--gold);text-transform:uppercase;font-family:'Space Grotesk',sans-serif">A Final Word</div></div>
pattern_fw = re.compile(
    r'(<div style="display:flex;align-items:center;gap:10px;margin-bottom:28px">\s*)<div style="font-size:8px;letter-spacing:0\.2em;color:var\(--gold\);text-transform:uppercase;font-family:\'Space Grotesk\',sans-serif">A Final Word</div></div>'
)
def replace_fw(m):
    return m.group(1) + logo_img + '<span style="font-size:8px;letter-spacing:0.2em;color:var(--gold);text-transform:uppercase;font-family:\'Space Grotesk\',sans-serif">A Final Word</span></div>'

new_content, count = pattern_fw.subn(replace_fw, content)
if count == 0:
    print(f"Warning: Could not replace A Final Word!")
else:
    print(f"Replaced A Final Word")
content = new_content

with open('epix_playbook_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. File updated.")
