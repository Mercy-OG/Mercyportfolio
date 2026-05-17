import re

html_content = """<!-- HERO PROJECT -->
<section style="padding-top:2rem; padding-bottom: 2rem;">
<div class="wrap">
<div class="proj-featured reveal" style="background:var(--surface); border-radius:var(--r-m); box-shadow:0 10px 30px var(--shadow-d); overflow:hidden; border:1px solid var(--border); display:flex; flex-direction:column;">
<div style="padding:2.5rem; border-bottom:1px solid var(--border); background:linear-gradient(135deg, rgba(255,107,0,.05), transparent);">
<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem; margin-bottom:1.5rem;">
<div>
<div class="proj-areas" style="margin-bottom:1rem; display:flex; gap:.5rem; flex-wrap:wrap;">
<a href="#" class="tag tag-amber" style="font-size:.75rem;">Data Visualisation</a>
<a href="#" class="tag tag-blue" style="font-size:.75rem;">Digital Health</a>
<a href="#" class="tag tag-muted" style="font-size:.75rem;">Advocacy</a>
<a href="#" class="tag tag-green" style="font-size:.75rem;">NYSC</a>
</div>
<h2 style="font-size:clamp(1.5rem, 3vw, 2.2rem); margin-bottom:.5rem;">Understanding Nigeria's HIV Epidemic</h2>
<p style="color:var(--ink-3); font-size:1.1rem; max-width:800px; line-height:1.6;">An interactive data dashboard to visualise Nigeria's HIV epidemic &mdash; where the burden is heaviest, where the treatment gaps are, and what the most recent data says about new infections.</p>
</div>
<div style="text-align:right;">
<span class="status status-done" style="font-size:.85rem; padding:.4rem .8rem;">Completed &#10003;</span>
</div>
</div>
<div style="display:flex; gap:1rem; align-items:center;">
<a href="dashboard.html" target="_blank" class="btn btn-primary"><i class="fa-solid fa-chart-pie"></i> View Full Dashboard</a>
</div>
</div>
<div style="padding:2.5rem; background:var(--bg);">
<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1.5rem; margin-bottom: 1.5rem;">
<div class="stat-box" style="padding:1.5rem; border:1px solid var(--border); border-radius:var(--r-s); background:var(--surface);">
<h4 style="font-size:1.8rem; color:var(--red); margin-bottom:.5rem;">3.6M</h4>
<p style="font-size:.85rem; color:var(--ink-3); font-weight:500;">People living with HIV</p>
</div>
<div class="stat-box" style="padding:1.5rem; border:1px solid var(--border); border-radius:var(--r-s); background:var(--surface);">
<h4 style="font-size:1.8rem; color:var(--teal); margin-bottom:.5rem;">42%</h4>
<p style="font-size:.85rem; color:var(--ink-3); font-weight:500;">Are virally suppressed</p>
</div>
<div class="stat-box" style="padding:1.5rem; border:1px solid var(--border); border-radius:var(--r-s); background:var(--surface);">
<h4 style="font-size:1.8rem; color:var(--amber); margin-bottom:.5rem;">20,838</h4>
<p style="font-size:.85rem; color:var(--ink-3); font-weight:500;">New infections in Q1 2026</p>
</div>
</div>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> <strong>Role:</strong> Researcher, Data Analyst &amp; Developer</p>
</div>
</div>
</div>
</section>

<!-- PROJECTS GRID -->
<section class="alt" style="padding-top:2rem;">
<div class="wrap">
<p class="sec-kicker reveal">Portfolio</p>
<h2 class="sec-title reveal">Featured Projects</h2>
<div class="bento bento-2" style="margin-top:2.5rem;">

<!-- Project 2 -->
<div class="proj-card reveal">
<div class="proj-head" style="align-items:flex-start;">
<div class="proj-areas" style="flex-wrap:wrap; gap:.5rem;">
<a href="#" class="tag tag-muted" style="font-size:.73rem;">Community Health</a>
<a href="#" class="tag tag-blue" style="font-size:.73rem;">Hygiene</a>
<a href="#" class="tag tag-green" style="font-size:.73rem;">Vocational Training</a>
</div>
<div style="display:flex; flex-direction:column; gap:.4rem; align-items:flex-end;">
<span class="status status-done" style="font-size:.7rem; white-space:nowrap;">Completed &#10003;</span>
<span class="tag tag-blue" style="font-size:.7rem; white-space:nowrap; border-radius:var(--r-pill);"><i class="fa-solid fa-flask"></i> EPIX Initiative</span>
</div>
</div>
<h3 class="proj-title">Project SHIELD</h3>
<p class="proj-desc">A large-scale community health programme that brought hygiene education and vocational skills to 2,000 students across three schools in Etim Ekpo LGA, Akwa Ibom State.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> <strong>Role:</strong> Lead Health Educator &amp; Communications Designer</p>
</div>

<!-- Project 1 -->
<div class="proj-card reveal reveal-s">
<div class="proj-head" style="align-items:flex-start;">
<div class="proj-areas" style="flex-wrap:wrap; gap:.5rem;">
<a href="#" class="tag tag-blue" style="font-size:.73rem;">Digital Health</a>
<a href="#" class="tag tag-amber" style="font-size:.73rem;">Adolescent Health</a>
<a href="#" class="tag tag-muted" style="font-size:.73rem;">Education</a>
</div>
<div style="display:flex; flex-direction:column; gap:.4rem; align-items:flex-end;">
<span class="status status-live" style="font-size:.7rem; white-space:nowrap;">Ongoing</span>
<span class="tag tag-blue" style="font-size:.7rem; white-space:nowrap; border-radius:var(--r-pill);"><i class="fa-solid fa-flask"></i> EPIX Initiative</span>
</div>
</div>
<h3 class="proj-title">The Male Adolescent Project</h3>
<p class="proj-desc">A health education project focused on young men in secondary schools. The goal is simple: get real, useful health information to boys who are largely left out of health conversations.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> <strong>Role:</strong> Project Lead &amp; Health Educator</p>
</div>

<!-- Project 3 -->
<div class="proj-card reveal">
<div class="proj-head" style="align-items:flex-start;">
<div class="proj-areas" style="flex-wrap:wrap; gap:.5rem;">
<a href="#" class="tag tag-muted" style="font-size:.73rem;">Research</a>
<a href="#" class="tag tag-blue" style="font-size:.73rem;">Digital Health</a>
<a href="#" class="tag tag-green" style="font-size:.73rem;">Health Equity</a>
</div>
<div style="display:flex; flex-direction:column; gap:.4rem; align-items:flex-end;">
<span class="status status-live" style="font-size:.7rem; white-space:nowrap;">In Progress</span>
</div>
</div>
<h3 class="proj-title">How Young Nigerians Find and Use Health Information Online</h3>
<p class="proj-desc">A research study exploring how young Nigerians between 15 and 35 search for health information online &mdash; what they trust, what they act on, and what that tells us about how digital health tools should be designed.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> <strong>Role:</strong> Lead Researcher</p>
</div>

<!-- Project 5 -->
<div class="proj-card reveal reveal-s">
<div class="proj-head" style="align-items:flex-start;">
<div class="proj-areas" style="flex-wrap:wrap; gap:.5rem;">
<a href="#" class="tag tag-amber" style="font-size:.73rem;">Mental Health</a>
<a href="#" class="tag tag-blue" style="font-size:.73rem;">Digital Health</a>
<a href="#" class="tag tag-teal" style="font-size:.73rem;">Product</a>
</div>
<div style="display:flex; flex-direction:column; gap:.4rem; align-items:flex-end;">
<span class="status status-live" style="font-size:.7rem; white-space:nowrap;">In Development</span>
<span class="tag tag-blue" style="font-size:.7rem; white-space:nowrap; border-radius:var(--r-pill);"><i class="fa-solid fa-flask"></i> EPIX Initiative</span>
</div>
</div>
<h3 class="proj-title">Echoes by EPIX</h3>
<p class="proj-desc">A stigma-free platform where young people can express what they are going through, privately and safely. Built to be a digital triage and support tool that meets young Nigerians on their phones.</p>
<p class="proj-role"><i class="fa-solid fa-user-pen" style="color:var(--teal);"></i> <strong>Role:</strong> Founder and Product Lead</p>
</div>

</div>
</div>
</section>"""

with open("projects.html", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find("<!-- PERSONAL PROJECTS -->")
end_idx = content.find("<footer>")

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + html_content + "\n" + content[end_idx:]
    with open("projects.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("projects.html updated successfully!")
else:
    print("Could not find delimiters.")
