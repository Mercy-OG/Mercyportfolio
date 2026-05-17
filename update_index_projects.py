import re

html_content = """<div class="bento bento-3">
<div class="proj-card reveal">
<div class="proj-head">
<div class="proj-areas">
<span class="tag tag-amber" style="font-size:.73rem;">Data Visualisation</span>
<span class="tag tag-blue" style="font-size:.73rem;">Digital Health</span>
</div>
<span class="status status-done">Completed &#10003;</span>
</div>
<h3 class="proj-title">Understanding Nigeria's HIV Epidemic Dashboard</h3>
<p class="proj-desc">An interactive data dashboard to visualise Nigeria's HIV epidemic &mdash; where the burden is heaviest, and where the treatment gaps are.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> Data Analyst &amp; Developer</p>
</div>

<div class="proj-card reveal reveal-s">
<div class="proj-head">
<div class="proj-areas">
<span class="tag tag-muted" style="font-size:.73rem;">Community Health</span>
<span class="tag tag-blue" style="font-size:.73rem;">EPIX</span>
</div>
<span class="status status-done">Completed &#10003;</span>
</div>
<h3 class="proj-title">Project SHIELD</h3>
<p class="proj-desc">A large-scale community health programme that brought hygiene education and vocational skills to 2,000 students across three schools.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> Lead Health Educator</p>
</div>

<div class="proj-card reveal reveal-m">
<div class="proj-head">
<div class="proj-areas">
<span class="tag tag-amber" style="font-size:.73rem;">Mental Health</span>
<span class="tag tag-blue" style="font-size:.73rem;">EPIX</span>
</div>
<span class="status status-live">In Development</span>
</div>
<h3 class="proj-title">Echoes by EPIX</h3>
<p class="proj-desc">A stigma-free platform where young people can express what they are going through. A digital triage and support tool for young Nigerians.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> Founder &amp; Product Lead</p>
</div>
</div>"""

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find('<div class="bento bento-3">')
end_idx = content.find('</div>\n</div>\n</section>\n<!-- COLLABORATE -->')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + html_content + "\n" + content[end_idx:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("index.html updated successfully!")
else:
    print("Could not find delimiters.")
