import os
import re

css_path = r"c:\Users\lenovo\.gemini\antigravity\scratch\mercy-portfolio\css\style.css"

with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace variables
new_root = """:root {
  --bg: #111111;
  --surface: #1c1c1f;
  --surface-2: #252529;
  --shadow-d: #080809;
  --shadow-l: #2a2a2f;

  --teal: #ff6b00;
  --teal-d: #e65c00;
  --teal-l: #ff8c33;
  --teal-xl: rgba(255,107,0,0.15);
  
  --blue: #ff8c33;
  --blue-l: rgba(255,140,51,0.15);
  
  --amber: #f59e0b;
  --amber-l: #fde68a;
  --green: #10b981;
  --red: #ef4444;

  --ink: #ffffff;
  --ink-2: #cbd5e1;
  --ink-3: #94a3b8;
  --ink-4: #64748b;

  --clay: 8px 8px 18px var(--shadow-d), -8px -8px 18px var(--shadow-l);
  --clay-lg: 14px 14px 30px var(--shadow-d), -14px -14px 30px var(--shadow-l);
  --clay-hover: 20px 20px 40px var(--shadow-d), -20px -20px 40px var(--shadow-l);
  --clay-inset: inset 6px 6px 14px var(--shadow-d), inset -6px -6px 14px var(--shadow-l);
  --clay-card: 10px 10px 22px var(--shadow-d), -10px -10px 22px var(--shadow-l), inset 1px 1px 0 rgba(255,255,255,0.03);
}"""

css = re.sub(r':root\s*\{.*?\n\}', new_root, css, flags=re.DOTALL)

# Replace light mode specific RGBA colors
css = css.replace('rgba(255,255,255,.75)', 'rgba(255,255,255,.04)')
css = css.replace('rgba(255,255,255,.85)', 'rgba(255,255,255,.06)')
css = css.replace('rgba(255,255,255,.8)', 'rgba(255,255,255,.05)')
css = css.replace('rgba(255,255,255,.9)', 'rgba(255,255,255,.1)')
css = css.replace('rgba(255,255,255,.95)', 'rgba(255,255,255,.15)')
css = css.replace('rgba(255,255,255,.6)', 'rgba(255,255,255,.1)')

# Header & specific cards
css = css.replace('rgba(228,239,246,.88)', 'rgba(28,28,31,.88)')
css = css.replace('rgba(228,239,246,.96)', 'rgba(28,28,31,.96)')
css = css.replace('rgba(228,239,246,.92)', 'rgba(28,28,31,.92)')

# Alt section
css = css.replace('rgba(255,255,255,.28)', 'var(--surface-2)')
css = css.replace('rgba(176,196,212,.35)', 'rgba(0,0,0,.5)')
css = css.replace('rgba(176,196,212,.5)', 'rgba(0,0,0,.5)')
css = css.replace('rgba(176,196,212,.3)', 'rgba(255,255,255,.1)')

# Accent specific RGBA (old teal was 13,148,136) (new orange is 255,107,0)
css = css.replace('rgba(13,148,136,', 'rgba(255,107,0,')
# (old blue was 2,132,199) (new orange-ish is 255,140,51)
css = css.replace('rgba(2,132,199,', 'rgba(255,140,51,')

# Blobs colors
css = css.replace('rgba(245,158,11,.12)', 'rgba(255,107,0,.12)')

# Tags gradients and background
css = css.replace('linear-gradient(135deg,#ccfbf1,#a7f3d0)', 'linear-gradient(135deg,#ff8c33,#ff6b00)')
css = css.replace('linear-gradient(135deg,#ccfbf1,#5eead4)', 'linear-gradient(135deg,#ff8c33,#ff6b00)')
css = css.replace('color:var(--teal-d)', 'color:#ffffff')

css = css.replace('linear-gradient(135deg,#dbeafe,#bfdbfe)', 'var(--surface-2)')
css = css.replace('linear-gradient(135deg,#dbeafe,#93c5fd)', 'var(--surface-2)')
css = css.replace('color:#1d4ed8', 'color:#ffffff')

css = css.replace('linear-gradient(135deg,#fef3c7,#fde68a)', 'var(--surface-2)')
css = css.replace('linear-gradient(135deg,#fef3c7,#fcd34d)', 'var(--surface-2)')
css = css.replace('color:#92400e', 'color:#ffffff')

css = css.replace('linear-gradient(135deg,#d1fae5,#a7f3d0)', 'var(--surface-2)')
css = css.replace('linear-gradient(135deg,#d1fae5,#6ee7b7)', 'var(--surface-2)')
css = css.replace('color:#065f46', 'color:#ffffff')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS updated!")
