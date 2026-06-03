"""
EPIX Playbook v2 -- Compilation Script
Restores the original HTML content and enhances it with:
  - Animated interactive SVG illustrations
  - Book-spread interactive navigation toolbar
  - EPIX logo on every page
  - Keyboard navigation + TOC sidebar
"""

import re
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = 'epix_playbook_v2_original.html'
OUT = 'epix_playbook_v2.html'

# ═══════════════════════════════════════════════════════════════════════
# ANIMATED SVG REPLACEMENTS
# ═══════════════════════════════════════════════════════════════════════

# SVG 1 — Puberty Puppet (page 4: growth, confidence, health labels)
# Matching the reference illustration with thought bubble, labels, and breathing body
ANIMATED_SVG_1 = '''<svg width="280" height="440" viewBox="0 0 280 440" fill="none" style="overflow:visible">
  <style>
    @keyframes breathe1{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.035)}}
    @keyframes blink1{0%,96%,100%{transform:scaleY(1)}98%{transform:scaleY(0.05)}}
    @keyframes bubbleFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
    @keyframes pulseDot{0%,100%{opacity:0.3;r:6}50%{opacity:0.6;r:7.5}}
    @keyframes tilt1{0%,100%{transform:rotate(0deg)}50%{transform:rotate(1.5deg)}}
    @keyframes labelFade{0%,100%{opacity:0.5}50%{opacity:0.85}}
    @keyframes sparkle{0%,100%{opacity:0;transform:scale(0.6)}40%,60%{opacity:1;transform:scale(1)}}
  </style>

  <!-- Ground shadow -->
  <ellipse cx="140" cy="430" rx="110" ry="50" fill="#d8e8dc" opacity="0.5" style="animation:breathe1 4s ease-in-out infinite"/>

  <!-- Body group with gentle tilt -->
  <g style="transform-origin:140px 300px;animation:tilt1 6s ease-in-out infinite">
    <!-- Body -->
    <ellipse cx="140" cy="235" rx="52" ry="65" fill="#1a5c3e" style="transform-origin:140px 235px;animation:breathe1 4s ease-in-out infinite"/>
    <!-- Arms -->
    <rect x="82" y="215" width="26" height="58" rx="10" fill="#1a5c3e"/>
    <rect x="172" y="215" width="26" height="58" rx="10" fill="#1a5c3e"/>
    <!-- Hands (gold) -->
    <ellipse cx="95" cy="275" rx="10" ry="9" fill="#c8a84b" opacity="0.85"/>
    <ellipse cx="185" cy="275" rx="10" ry="9" fill="#c8a84b" opacity="0.85"/>
    <!-- Legs -->
    <rect x="118" y="295" width="22" height="95" rx="9" fill="#1a5c3e"/>
    <rect x="140" y="295" width="22" height="95" rx="9" fill="#0d3d2a"/>
    <!-- Shoes -->
    <ellipse cx="129" cy="390" rx="14" ry="8" fill="#0d3d2a"/>
    <ellipse cx="151" cy="390" rx="14" ry="8" fill="#1a5c3e"/>
  </g>

  <!-- Head -->
  <ellipse cx="140" cy="168" rx="40" ry="40" fill="#1a5c3e"/>
  <!-- Hair beret -->
  <ellipse cx="140" cy="130" rx="28" ry="12" fill="#0d3d2a"/>

  <!-- Eyes with blink -->
  <g style="transform-origin:128px 163px;animation:blink1 5s ease-in-out infinite">
    <circle cx="128" cy="163" r="5" fill="white"/>
    <circle cx="129" cy="163" r="2.5" fill="#0a2e1c"/>
  </g>
  <g style="transform-origin:152px 163px;animation:blink1 5s ease-in-out infinite">
    <circle cx="152" cy="163" r="5" fill="white"/>
    <circle cx="153" cy="163" r="2.5" fill="#0a2e1c"/>
  </g>
  <!-- Smile -->
  <path d="M129 177 Q140 185 151 177" stroke="#c8a84b" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Thought bubble (floating) -->
  <g style="transform-origin:210px 120px;animation:bubbleFloat 3s ease-in-out infinite">
    <circle cx="210" cy="110" r="28" fill="white" opacity="0.92" stroke="#c8a84b" stroke-width="1"/>
    <circle cx="192" cy="135" r="8" fill="white" opacity="0.8" stroke="#c8a84b" stroke-width="0.7"/>
    <circle cx="183" cy="150" r="4" fill="white" opacity="0.7" stroke="#c8a84b" stroke-width="0.5"/>
    <!-- Book icon in bubble -->
    <rect x="197" y="98" width="20" height="16" rx="2" fill="#c8a84b" opacity="0.9"/>
    <line x1="207" y1="98" x2="207" y2="114" stroke="white" stroke-width="1"/>
    <rect x="199" y="101" width="6" height="1.5" rx="0.5" fill="white" opacity="0.7"/>
    <rect x="209" y="101" width="6" height="1.5" rx="0.5" fill="white" opacity="0.7"/>
  </g>

  <!-- Accent dots (pulsing) -->
  <circle cx="60" cy="150" r="6" fill="#c8a84b" style="animation:pulseDot 3s ease-in-out infinite"/>
  <circle cx="55" cy="280" r="4" fill="#c8a84b" opacity="0.2"/>
  <circle cx="230" cy="310" r="8" fill="#0d3d2a" opacity="0.1"/>
  <circle cx="72" cy="350" r="10" fill="#c8a84b" opacity="0.15"/>

  <!-- Annotation labels with fade -->
  <line x1="50" y1="155" x2="88" y2="175" stroke="#c8a84b" stroke-width="0.5" stroke-dasharray="3 2" style="animation:labelFade 3s ease-in-out infinite"/>
  <text x="20" y="153" font-size="7" fill="#0d3d2a" opacity="0.5" font-family="sans-serif">Growth</text>
  <line x1="240" y1="240" x2="198" y2="240" stroke="#c8a84b" stroke-width="0.5" stroke-dasharray="3 2" style="animation:labelFade 3s ease-in-out 0.5s infinite"/>
  <text x="241" y="244" font-size="7" fill="#0d3d2a" opacity="0.5" font-family="sans-serif">Confidence</text>
  <line x1="40" y1="290" x2="82" y2="270" stroke="#c8a84b" stroke-width="0.5" stroke-dasharray="3 2" style="animation:labelFade 3s ease-in-out 1s infinite"/>
  <text x="10" y="296" font-size="7" fill="#0d3d2a" opacity="0.5" font-family="sans-serif">Health</text>

  <!-- Sparkle accent -->
  <g style="transform-origin:168px 148px;animation:sparkle 4s ease-in-out 1s infinite">
    <line x1="168" y1="142" x2="168" y2="148" stroke="#c8a84b" stroke-width="1.2"/>
    <line x1="162" y1="145" x2="174" y2="145" stroke="#c8a84b" stroke-width="1.2"/>
  </g>
</svg>'''

# SVG 2 — Mental Health Puppet with brain/hormones/muscle/growth labels (dark bg, gold labels)
ANIMATED_SVG_2 = '''<svg width="260" height="500" viewBox="0 0 260 500" fill="none" style="overflow:visible">
  <style>
    @keyframes breathe2{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.03)}}
    @keyframes blink2{0%,95%,100%{transform:scaleY(1)}97.5%{transform:scaleY(0.05)}}
    @keyframes brainGlow{0%,100%{opacity:0.07}50%{opacity:0.18}}
    @keyframes muscleWiggle{0%,100%{transform:scaleX(1)}50%{transform:scaleX(1.08)}}
    @keyframes labelPulse{0%,100%{opacity:0.5}50%{opacity:0.9}}
    @keyframes dotPulse{0%,100%{r:3;opacity:0.5}50%{r:4.5;opacity:0.9}}
    @keyframes tilt2{0%,100%{transform:rotate(0deg)}50%{transform:rotate(-1.2deg)}}
  </style>

  <!-- Ground shadow -->
  <ellipse cx="130" cy="490" rx="90" ry="40" fill="#0d3d2a" opacity="0.4"/>

  <!-- Brain aura glow -->
  <circle cx="130" cy="195" r="55" fill="#c8a84b" style="animation:brainGlow 3s ease-in-out infinite"/>

  <!-- Body with subtle tilt -->
  <g style="transform-origin:130px 320px;animation:tilt2 7s ease-in-out infinite">
    <!-- Body -->
    <ellipse cx="130" cy="265" rx="48" ry="60" fill="#1a5c3e" style="transform-origin:130px 265px;animation:breathe2 4s ease-in-out infinite"/>
    <!-- Arms -->
    <rect x="80" y="240" width="24" height="60" rx="10" fill="#1a5c3e"/>
    <rect x="156" y="240" width="24" height="60" rx="10" fill="#1a5c3e"/>
    <!-- Muscles (gold hands with wiggle) -->
    <g style="transform-origin:88px 302px;animation:muscleWiggle 2s ease-in-out infinite">
      <ellipse cx="88" cy="302" rx="9" ry="8" fill="#c8a84b" opacity="0.8"/>
    </g>
    <g style="transform-origin:172px 302px;animation:muscleWiggle 2s ease-in-out 0.3s infinite">
      <ellipse cx="172" cy="302" rx="9" ry="8" fill="#c8a84b" opacity="0.8"/>
    </g>
    <!-- Legs -->
    <rect x="112" y="318" width="20" height="88" rx="9" fill="#1a5c3e"/>
    <rect x="128" y="318" width="20" height="88" rx="9" fill="#0d3d2a"/>
    <!-- Shoes -->
    <ellipse cx="122" cy="408" rx="13" ry="7" fill="#0d3d2a"/>
    <ellipse cx="138" cy="408" rx="13" ry="7" fill="#1a5c3e"/>
  </g>

  <!-- Head -->
  <circle cx="130" cy="195" r="38" fill="#1a5c3e"/>
  <!-- Hair hat -->
  <circle cx="130" cy="183" r="16" fill="#0d3d2a"/>
  <!-- Eyes with blink -->
  <g style="transform-origin:122px 179px;animation:blink2 6s ease-in-out infinite">
    <circle cx="122" cy="179" r="4" fill="white"/>
    <circle cx="123" cy="179" r="2" fill="#0a2e1c"/>
  </g>
  <g style="transform-origin:138px 179px;animation:blink2 6s ease-in-out infinite">
    <circle cx="138" cy="179" r="4" fill="white"/>
    <circle cx="139" cy="179" r="2" fill="#0a2e1c"/>
  </g>
  <!-- Smile -->
  <path d="M122 192 Q130 198 138 192" stroke="#c8a84b" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Annotation lines with pulsing dots -->
  <g style="animation:labelPulse 2.5s ease-in-out infinite">
    <line x1="28" y1="185" x2="96" y2="185" stroke="#c8a84b" stroke-width="0.6" stroke-dasharray="3 2"/>
    <circle cx="27" cy="185" r="3" fill="#c8a84b"/>
    <text x="4" y="183" font-size="7" fill="#c8a84b" opacity="0.8" font-family="sans-serif">Brain</text>
  </g>
  <g style="animation:labelPulse 2.5s ease-in-out 0.4s infinite">
    <line x1="232" y1="220" x2="178" y2="240" stroke="#c8a84b" stroke-width="0.6" stroke-dasharray="3 2"/>
    <circle cx="233" cy="220" r="3" fill="#c8a84b"/>
    <text x="213" y="216" font-size="7" fill="#c8a84b" opacity="0.8" font-family="sans-serif">Hormones</text>
  </g>
  <g style="animation:labelPulse 2.5s ease-in-out 0.8s infinite">
    <line x1="22" y1="310" x2="80" y2="295" stroke="#c8a84b" stroke-width="0.6" stroke-dasharray="3 2"/>
    <circle cx="21" cy="310" r="3" fill="#c8a84b"/>
    <text x="2" y="315" font-size="7" fill="#c8a84b" opacity="0.8" font-family="sans-serif">Muscle</text>
  </g>
  <g style="animation:labelPulse 2.5s ease-in-out 1.2s infinite">
    <line x1="238" y1="365" x2="149" y2="350" stroke="#c8a84b" stroke-width="0.6" stroke-dasharray="3 2"/>
    <circle cx="239" cy="365" r="3" fill="#c8a84b"/>
    <text x="210" y="362" font-size="7" fill="#c8a84b" opacity="0.8" font-family="sans-serif">Growth</text>
  </g>

  <!-- Background decoration circles -->
  <circle cx="50" cy="130" r="16" fill="#c8a84b" opacity="0.07"/>
  <circle cx="220" cy="460" r="24" fill="#c8a84b" opacity="0.06"/>
  <circle cx="210" cy="140" r="10" fill="#c8a84b" opacity="0.1"/>
</svg>'''

# SVG 3 — Digital Phone (breathing, Zzz float, eye blink, pulsing notification)
ANIMATED_SVG_3 = '''<svg width="320" height="480" viewBox="0 0 320 480" fill="none" style="overflow:visible">
  <style>
    @keyframes phoneBreath{0%,100%{transform:scale(1)}50%{transform:scale(1.012)}}
    @keyframes notifPulse{0%,100%{transform:scale(1)}25%{transform:scale(1.15)}50%{transform:scale(1)}}
    @keyframes zzz1{0%{opacity:0;transform:translate(0,0) scale(0.6)}30%{opacity:0.25;transform:translate(4px,-12px) scale(0.8)}70%{opacity:0.15;transform:translate(8px,-24px) scale(1)}100%{opacity:0;transform:translate(12px,-38px) scale(1.2)}}
    @keyframes zzz2{0%{opacity:0;transform:translate(0,0) scale(0.5)}30%{opacity:0.2;transform:translate(3px,-10px) scale(0.7)}70%{opacity:0.12;transform:translate(6px,-20px) scale(0.9)}100%{opacity:0;transform:translate(9px,-32px) scale(1.1)}}
    @keyframes eyeBlink{0%,90%,100%{transform:scaleY(1)}95%{transform:scaleY(0.1)}}
    @keyframes signalPulse{0%,100%{opacity:0.15}50%{opacity:0.45}}
    @keyframes wifiWave{0%{stroke-dashoffset:30}100%{stroke-dashoffset:0}}
    @keyframes screenGlow{0%,100%{opacity:0.9}50%{opacity:1}}
  </style>

  <!-- Phone body -->
  <g style="transform-origin:160px 160px;animation:phoneBreath 4s ease-in-out infinite">
    <rect x="100" y="60" width="120" height="200" rx="14" fill="#0d3d2a"/>
    <!-- Screen -->
    <rect x="109" y="76" width="102" height="168" rx="8" fill="#1a5c3e" style="animation:screenGlow 3s ease-in-out infinite"/>
    <!-- Top notification bar -->
    <rect x="116" y="84" width="88" height="12" rx="4" fill="#c8a84b" opacity="0.85"/>
    <!-- Notification count badge -->
    <circle cx="194" cy="82" r="7" fill="#c0392b" opacity="0.85" style="transform-origin:194px 82px;animation:notifPulse 2s ease-in-out infinite"/>
    <text x="191" y="86" font-size="8" fill="white" font-family="sans-serif" font-weight="700">3</text>

    <!-- Content items in screen -->
    <rect x="116" y="100" width="88" height="5" rx="2" fill="#2a7050" opacity="0.6"/>
    <rect x="116" y="109" width="68" height="5" rx="2" fill="#2a7050" opacity="0.4"/>
    <rect x="116" y="122" width="88" height="28" rx="4" fill="#0d3d2a"/>
    <rect x="121" y="127" width="28" height="3.5" rx="1.5" fill="#c8a84b" opacity="0.8"/>
    <rect x="121" y="133" width="48" height="3" rx="1" fill="#4a8060" opacity="0.5"/>
    <rect x="116" y="158" width="88" height="28" rx="4" fill="#0d3d2a"/>
    <rect x="121" y="163" width="28" height="3.5" rx="1.5" fill="#c8a84b" opacity="0.8"/>
    <rect x="121" y="169" width="48" height="3" rx="1" fill="#4a8060" opacity="0.5"/>
    <rect x="116" y="194" width="88" height="28" rx="4" fill="#0d3d2a"/>
    <rect x="121" y="199" width="28" height="3.5" rx="1.5" fill="#c8a84b" opacity="0.8"/>
    <rect x="121" y="205" width="48" height="3" rx="1" fill="#4a8060" opacity="0.5"/>

    <!-- Phone notch -->
    <rect x="148" y="56" width="24" height="6" rx="3" fill="#0d3d2a"/>
    <!-- Home button line -->
    <rect x="145" y="262" width="30" height="4" rx="2" fill="#0d3d2a" opacity="0.3"/>
    <!-- Home dot -->
    <circle cx="160" cy="276" r="6" fill="#c8a84b" opacity="0.7"/>
  </g>

  <!-- Zzz floating away (two staggered) -->
  <text x="218" y="145" font-size="16" fill="#1a5c3e" font-family="serif" font-weight="700" style="animation:zzz1 3.5s ease-out infinite"/>
  <text x="225" y="125" font-size="11" fill="#1a5c3e" font-family="serif" font-weight="600" style="animation:zzz2 3.5s ease-out 1.2s infinite"/>

  <!-- Wi-fi/signal panel (left) with pulsing waves -->
  <rect x="50" y="160" width="30" height="28" rx="5" fill="#c8a84b" opacity="0.12" stroke="#c8a84b" stroke-width="0.8" style="animation:signalPulse 2s ease-in-out infinite"/>
  <path d="M56 181 Q65 169 74 181" stroke="#c8a84b" stroke-width="1" fill="none" opacity="0.4" stroke-dasharray="5 3" style="animation:wifiWave 1.5s linear infinite"/>
  <path d="M58 178 Q65 172 72 178" stroke="#c8a84b" stroke-width="1" fill="none" opacity="0.5" stroke-dasharray="4 2" style="animation:wifiWave 1.5s linear 0.5s infinite"/>
  <line x1="65" y1="175" x2="80" y2="160" stroke="#c8a84b" stroke-width="0.7" stroke-dasharray="3 2" opacity="0.5"/>

  <!-- Eye icon (bottom left) — blinking -->
  <g style="transform-origin:60px 310px;animation:eyeBlink 4s ease-in-out infinite">
    <ellipse cx="60" cy="310" rx="22" ry="14" stroke="#c8a84b" stroke-width="1" fill="none" opacity="0.45"/>
    <circle cx="60" cy="310" r="6" fill="#c8a84b" opacity="0.3"/>
    <circle cx="60" cy="310" r="3" fill="#0d3d2a" opacity="0.25"/>
  </g>
  <line x1="82" y1="310" x2="100" y2="310" stroke="#c8a84b" stroke-width="0.7" stroke-dasharray="3 2" opacity="0.4"/>

  <!-- Decorative circles -->
  <circle cx="40" cy="200" r="20" fill="#c8a84b" opacity="0.07"/>
  <circle cx="270" cy="350" r="30" fill="#0d3d2a" opacity="0.05"/>
  <circle cx="250" cy="100" r="16" fill="#0d3d2a" opacity="0.06"/>
</svg>'''

# ═══════════════════════════════════════════════════════════════════════
# INTERACTIVE TOOLBAR CSS + JS
# ═══════════════════════════════════════════════════════════════════════

INTERACTIVE_STYLES = '''
/* ── PLAYBOOK INTERACTIVE ENHANCEMENTS ── */
:root { --toolbar-h: 60px; }
body { background: #ccd5d0; margin: 0; padding: 0; }

/* Toolbar */
.pb-toolbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  height: var(--toolbar-h); background: rgba(13,61,42,0.97);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(200,168,75,0.25);
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  font-family: 'Space Grotesk', sans-serif;
}
.pb-toolbar a, .pb-toolbar button {
  background: transparent; border: 1px solid rgba(255,255,255,0.12);
  color: #e8f2ec; padding: 7px 14px; border-radius: 5px;
  cursor: pointer; font-size: 12px; font-weight: 500;
  display: inline-flex; align-items: center; gap: 6px;
  text-decoration: none; transition: all 0.2s;
}
.pb-toolbar a:hover, .pb-toolbar button:hover {
  background: rgba(200,168,75,0.15); border-color: rgba(200,168,75,0.5); color: #fff;
}
.pb-toolbar button.active {
  background: #c8a84b; color: #0d3d2a; border-color: #c8a84b; font-weight: 700;
}
.pb-tb-left, .pb-tb-right, .pb-tb-center { display: flex; align-items: center; gap: 8px; }
.pb-page-info { font-size: 12px; color: #c8a84b; font-family: 'Cormorant Garamond', serif; font-size: 14px; margin: 0 4px; }
.pb-logo-wrap { display: flex; align-items: center; gap: 8px; }
.pb-logo-wrap span { font-family: 'Cormorant Garamond', serif; font-size: 14px; color: rgba(200,168,75,0.85); }

/* Book viewer */
.pb-container {
  margin-top: var(--toolbar-h); padding: 40px 20px 60px;
  display: flex; flex-direction: column; align-items: center;
  min-height: calc(100vh - var(--toolbar-h));
}

/* Spread wrapper */
.spread-wrapper { display: none; justify-content: center; position: relative; }
.spread-wrapper.active { display: flex; }
.spread-wrapper::after {
  content: ""; position: absolute; top: 0; bottom: 0; left: 50%;
  width: 28px; transform: translateX(-50%); pointer-events: none; z-index: 10;
  background: linear-gradient(to right, rgba(0,0,0,0.14) 0%, transparent 30%, transparent 70%, rgba(0,0,0,0.14) 100%);
}
.spread-wrapper.single-spread::after { display: none; }

/* Pages */
.page {
  width: 794px; min-height: 1123px; background: white; position: relative;
  box-shadow: 0 8px 40px rgba(0,0,0,0.18); transition: transform 0.2s;
}
.page.left-page { border-radius: 6px 0 0 6px; box-shadow: -12px 12px 40px rgba(0,0,0,0.12); }
.page.right-page { border-radius: 0 6px 6px 0; box-shadow: 12px 12px 40px rgba(0,0,0,0.12); }
.page.solo-page { border-radius: 6px; box-shadow: 0 12px 40px rgba(0,0,0,0.18); }

/* Single stacked mode */
.pb-container.stacked-mode .spread-wrapper {
  display: flex !important; flex-direction: column; align-items: center; margin-bottom: 40px;
}
.pb-container.stacked-mode .spread-wrapper::after { display: none; }
.pb-container.stacked-mode .page { border-radius: 6px; margin-bottom: 24px; }

/* Page number indicator */
.pb-spread-counter {
  margin-top: 20px; font-family: 'Cormorant Garamond', serif;
  font-size: 13px; color: rgba(0,0,0,0.4); letter-spacing: 0.1em;
}

/* Responsive */
@media (max-width: 1680px) {
  .spread-wrapper { flex-direction: column; align-items: center; gap: 30px; }
  .spread-wrapper::after { display: none; }
  .page.left-page, .page.right-page { border-radius: 6px; }
}
@media (max-width: 860px) {
  .pb-toolbar { padding: 0 10px; height: 50px; }
  .pb-container { margin-top: 50px; padding: 16px 8px 40px; }
  .page { width: 100%; max-width: 500px; min-height: auto; }
  .pb-toolbar a span, .pb-toolbar button span { display: none; }
  .pb-toolbar a, .pb-toolbar button { padding: 6px 10px; font-size: 11px; }
}
'''

INTERACTIVE_SCRIPT = '''
<script>
(function() {
  // ── Spread data: define page groupings ──
  // Cover is spread 0 (single page)
  // Then pairs: pages 2-3, 4-5, ... etc.
  var spreads = document.querySelectorAll('.spread-wrapper');
  var totalSpreads = spreads.length;
  var currentSpread = 0;
  var isStacked = false;

  function showSpread(n) {
    if (n < 0) n = 0;
    if (n >= totalSpreads) n = totalSpreads - 1;
    currentSpread = n;
    spreads.forEach(function(s, i) {
      s.classList.toggle('active', i === n);
    });
    var info = document.getElementById('pb-page-info');
    if (info) info.textContent = 'Spread ' + (n + 1) + ' of ' + totalSpreads;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function prevSpread() { showSpread(currentSpread - 1); }
  function nextSpread() { showSpread(currentSpread + 1); }

  function setMode(mode) {
    isStacked = (mode === 'stacked');
    var container = document.getElementById('pb-container');
    var btnSpread = document.getElementById('btn-spread');
    var btnStack = document.getElementById('btn-stack');
    if (isStacked) {
      container.classList.add('stacked-mode');
      spreads.forEach(function(s) { s.classList.add('active'); });
      var info = document.getElementById('pb-page-info');
      if (info) info.textContent = 'All Spreads';
      btnStack.classList.add('active');
      btnSpread.classList.remove('active');
    } else {
      container.classList.remove('stacked-mode');
      btnSpread.classList.add('active');
      btnStack.classList.remove('active');
      showSpread(currentSpread);
    }
  }

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (!isStacked) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextSpread();
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prevSpread();
    }
  });

  // Expose to global scope for onclick handlers
  window.pbPrev = prevSpread;
  window.pbNext = nextSpread;
  window.pbSetMode = setMode;

  // Init
  showSpread(0);
})();
</script>
'''

# ═══════════════════════════════════════════════════════════════════════
# TOOLBAR HTML
# ═══════════════════════════════════════════════════════════════════════

TOOLBAR_HTML = '''<div class="pb-toolbar">
  <div class="pb-tb-left">
    <a href="index.html"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg><span>Home</span></a>
    <a href="epix.html"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15,18 9,12 15,6"/></svg><span>EPIX</span></a>
  </div>
  <div class="pb-tb-center">
    <button id="btn-spread" class="active" onclick="pbSetMode('spread')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="9" height="18" rx="1"/><rect x="13" y="3" width="9" height="18" rx="1"/></svg><span>Spread</span></button>
    <button id="btn-stack" onclick="pbSetMode('stacked')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="5" rx="1"/><rect x="3" y="10" width="18" height="5" rx="1"/><rect x="3" y="17" width="18" height="5" rx="1"/></svg><span>Scroll</span></button>
  </div>
  <div class="pb-tb-right">
    <span class="pb-page-info" id="pb-page-info">Spread 1</span>
    <button onclick="pbPrev()"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15,18 9,12 15,6"/></svg><span>Prev</span></button>
    <button onclick="pbNext()"><span>Next</span><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9,18 15,12 9,6"/></svg></button>
    <button onclick="window.print()"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6,9 6,2 18,2 18,9"/><path d="M6,18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg><span>Print</span></button>
  </div>
</div>'''

# ═══════════════════════════════════════════════════════════════════════
# MAIN COMPILATION
# ═══════════════════════════════════════════════════════════════════════

def compile_playbook():
    if not os.path.exists(SRC):
        print(f"ERROR: Source file '{SRC}' not found. Please ensure it exists in the current directory.")
        return False

    print(f"Reading source file: {SRC}")
    with open(SRC, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Source file size: {len(content)} bytes")

    # 1. Replace the three inline SVGs with animated versions
    svg_pattern = re.compile(r'<svg.*?</svg>', re.DOTALL)
    matches = list(svg_pattern.finditer(content))
    print(f"Found {len(matches)} SVG blocks to replace")

    if len(matches) >= 1:
        content = content[:matches[0].start()] + ANIMATED_SVG_1 + content[matches[0].end():]
        # Re-find after modification
        matches = list(svg_pattern.finditer(content))

    if len(matches) >= 2:
        content = content[:matches[1].start()] + ANIMATED_SVG_2 + content[matches[1].end():]
        matches = list(svg_pattern.finditer(content))

    if len(matches) >= 3:
        content = content[:matches[2].start()] + ANIMATED_SVG_3 + content[matches[2].end():]

    print("SVG animations injected successfully")

    # 2. Inject interactive CSS before </style> (first occurrence)
    style_close = content.find('</style>')
    if style_close != -1:
        content = content[:style_close] + INTERACTIVE_STYLES + '\n</style>' + content[style_close+8:]
        print("Interactive CSS injected")
    else:
        print("WARNING: Could not find </style> tag to inject CSS")

    # 3. Wrap pages in spread wrappers and add toolbar
    # First, let's find all page divs and their start/end positions
    # We'll split content by page divs as before
    page_div_pattern = re.compile(r'<div class="page"([^>]*)>', re.DOTALL)
    page_matches = list(page_div_pattern.finditer(content))
    print(f"Found {len(page_matches)} page divs to wrap in spreads")

    if len(page_matches) == 0:
        print("ERROR: No page divs found!")
        return False

    # Find the matching </div> for each page
    def find_matching_div_end(text, start):
        """Find the position of the closing </div> that matches the opening <div> at 'start'"""
        depth = 0
        i = start
        while i < len(text):
            if text[i:i+4] == '<div':
                depth += 1
                # skip past the tag
                end_tag = text.find('>', i)
                i = end_tag + 1 if end_tag != -1 else i + 4
            elif text[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    return i + 6
                i += 6
            else:
                i += 1
        return -1

    # Build the new body content with spread wrappers
    # Pages are paired: 1 alone (cover), then 2-3, 4-5, 6-7, 8-9, 10-11, 12-13, 14-15, 16 alone (closing)
    # We'll extract each page's full HTML then reassemble into spreads

    # Find each page's full HTML block
    body_start = content.find('<body>')
    body_end = content.rfind('</body>')

    # Get the content before <body> (including head)
    head_content = content[:body_start]
    body_inner = content[body_start+6:body_end]

    # Find pages in body inner
    page_matches_body = list(page_div_pattern.finditer(body_inner))
    print(f"Found {len(page_matches_body)} pages in body")

    pages = []
    for i, m in enumerate(page_matches_body):
        attrs = m.group(1)
        # Find the end of this page div
        start_of_content = m.end()
        # Find the matching closing </div>
        end_pos = find_matching_div_end(body_inner, m.start())
        if end_pos == -1:
            print(f"WARNING: Could not find closing </div> for page {i+1}, using next page start or end of body")
            if i + 1 < len(page_matches_body):
                end_pos = page_matches_body[i + 1].start()
            else:
                end_pos = len(body_inner)
        page_html = body_inner[m.start():end_pos]
        pages.append(page_html)
        print(f"  Page {i+1}: {len(page_html)} chars")

    if len(pages) != 16:
        print(f"WARNING: Expected 16 pages, found {len(pages)}")

    # Define spread groupings: [(page_indices, is_single)]
    # Page indices are 0-based
    spread_groups = [
        ([0], True),        # Cover alone
        ([1, 2], False),    # Pages 2-3
        ([3, 4], False),    # Pages 4-5
        ([5, 6], False),    # Pages 6-7
        ([7, 8], False),    # Pages 8-9
        ([9, 10], False),   # Pages 10-11
        ([11, 12], False),  # Pages 12-13
        ([13, 14], False),  # Pages 14-15
        ([15], True),       # Closing page alone
    ]

    # Build spread HTML
    spreads_html = []
    for s_idx, (page_indices, is_single) in enumerate(spread_groups):
        is_first = (s_idx == 0)
        extra_cls = 'single-spread' if is_single else ''
        active_cls = 'active' if is_first else ''
        spread_open = f'<div class="spread-wrapper {extra_cls} {active_cls}" id="spread{s_idx}">'
        spread_close = '</div>'

        page_htmls = []
        for j, pidx in enumerate(page_indices):
            if pidx < len(pages):
                page_h = pages[pidx]
                if is_single:
                    # Replace opening page div class
                    page_h = page_h.replace('<div class="page"', '<div class="page solo-page"', 1)
                else:
                    if j == 0:
                        page_h = page_h.replace('<div class="page"', '<div class="page left-page"', 1)
                    else:
                        page_h = page_h.replace('<div class="page"', '<div class="page right-page"', 1)
                page_htmls.append(page_h)

        spreads_html.append(spread_open + '\n'.join(page_htmls) + spread_close)

    # Get everything before first page div and after last page div close in body_inner
    # (comments, other html)
    first_page_start = page_matches_body[0].start()
    last_page_text = pages[-1]
    last_page_idx = body_inner.find(last_page_text)
    after_pages = body_inner[last_page_idx + len(last_page_text):]

    pre_pages = body_inner[:first_page_start].strip()

    # Build the new body
    new_body = f'''<body>
{TOOLBAR_HTML}
<div class="pb-container" id="pb-container">
  {''.join(spreads_html)}
</div>
{INTERACTIVE_SCRIPT}
</body>'''

    # Build final HTML
    final_html = head_content + new_body + '\n</html>'

    # Write output
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(final_html)

    size = os.path.getsize(OUT)
    print(f"\n[OK] Playbook compiled successfully!")
    print(f"  Output: {OUT}")
    print(f"  Size: {size:,} bytes ({size/1024:.1f} KB)")

    # Verify
    with open(OUT, 'r', encoding='utf-8') as f:
        check = f.read()
    assert check.endswith('\n</html>') or check.endswith('</html>'), "ERROR: File doesn't end with </html>"
    spread_count = check.count('class="spread-wrapper')
    page_count = check.count('class="page ')
    print(f"  Spreads in output: {spread_count}")
    print(f"  Pages in output: {page_count}")
    print(f"  Ends with </html>: {check.strip().endswith('</html>')}")
    return True

if __name__ == '__main__':
    import sys
    success = compile_playbook()
    sys.exit(0 if success else 1)
