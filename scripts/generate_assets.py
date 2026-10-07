#!/usr/bin/env python3
"""Generate the animated SVG artwork used by README.md.

Run from the repo root:  python3 scripts/generate_assets.py
Every SVG in assets/ is rebuilt from the data below, so edit text/colors here
instead of editing the SVG files by hand.

The SVGs only use inline CSS animations (no scripts, no external fonts or
images) because GitHub renders README images in a sandbox that strips those.
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

BG = "#ffffff"
PANEL = "#ffffff"
LINE = "#d0d7de"
TEXT = "#1f2328"
MUTED = "#59636e"
GREEN = "#059669"
CYAN = "#0891b2"
MAGENTA = "#db2777"
PURPLE = "#7c3aed"
BAR = "#f6f8fa"

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

PATHS = [
    {
        "key": "hobbyist", "num": "01", "title": "Hobbyist Hackers", "color": "#059669",
        "icon": "terminal", "tag": ["Learn the basics and hack", "for the thrill of it."],
        "pill": "SELF-PACED", "level": 1,
        "cmd": "./roadmap --path hobbyist",
        "sub": "From script kiddie to skilled practitioner, one lab at a time.",
        "chips": ["5 STEPS", "BEGINNER", "TRYHACKME · HTB"],
        "flow": ["TryHackMe", "PortSwigger", "Hack The Box", "Keep Learning", "CTF / Bounty"],
    },
    {
        "key": "expressway", "num": "02", "title": "Cyber Expressway", "color": "#0284c7",
        "icon": "bolt", "tag": ["Fast-track into a cyber", "role in under 10 months."],
        "pill": "~10 MONTHS", "level": 3,
        "cmd": "./roadmap --path expressway --fast",
        "sub": "The quickest realistic route to a pentesting job.",
        "chips": ["4 MILESTONES", "INTENSE", "TCM · HTB · OSCP"],
    },
    {
        "key": "bugbounty", "num": "03", "title": "Bug Bounty Hunter", "color": "#d97706",
        "icon": "bug", "tag": ["Build the mindset and land", "your very first bounty."],
        "pill": "ONGOING", "level": 2,
        "cmd": "./roadmap --path bug-bounty",
        "sub": "Mindset, foundations, recon and reporting: get paid for bugs.",
        "chips": ["7 CHAPTERS", "HANDS-ON", "OPENBUGBOUNTY · BURP"],
        "flow": ["Recon", "Scanning", "Exploitation", "Reporting"],
    },
    {
        "key": "certification", "num": "04", "title": "Certification Seekers", "color": "#7c3aed",
        "icon": "medal", "tag": ["Structured, validated skills", "from A+ all the way to OSCP."],
        "pill": "CERT BY CERT", "level": 3,
        "cmd": "./roadmap --path certifications",
        "sub": "Industry-recognized certs, in the order that makes sense.",
        "chips": ["7 CERTS", "STRUCTURED", "COMPTIA · LPI · OFFSEC"],
        "flow": ["A+", "Linux Ess.", "Network+", "Security+", "PenTest+", "CySA+", "OSCP"],
    },
    {
        "key": "degree", "num": "05", "title": "Degree Pursuers", "color": "#db2777",
        "icon": "cap", "tag": ["Earn a B.S. in Cybersecurity", "for a fraction of the cost."],
        "pill": "~1 WGU TERM", "level": 4,
        "cmd": "./roadmap --path degree --cheap",
        "sub": "Stack transfer credits, then finish the BSCSIA in a single term.",
        "chips": ["3 PHASES", "LONG GAME", "SOPHIA · STUDY.COM · WGU"],
        "flow": ["Base Courses", "Certifications", "WGU Enrollment", "B.S. Degree"],
    },
]


# --------------------------------------------------------------------------- icons

def icon(kind, color, size=1.0):
    """A simple line icon centred on (0, 0), roughly 48x48 at size=1."""
    s = f'stroke="{color}" stroke-width="{3.2 / size:.2f}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "terminal":
        body = (f'<rect x="-22" y="-17" width="44" height="34" rx="5" {s}/>'
                f'<path d="M-13 -5 L-5 1 L-13 7" {s}/><path d="M-1 8 H12" {s}/>')
    elif kind == "bolt":
        body = f'<path d="M4 -22 L-12 3 H1 L-4 22 L13 -4 H0 Z" {s}/>'
    elif kind == "bug":
        body = (f'<ellipse cx="0" cy="4" rx="11" ry="15" {s}/>'
                f'<circle cx="0" cy="-14" r="6" {s}/><path d="M0 -8 V19" {s}/>'
                f'<path d="M-11 -2 L-20 -7 M11 -2 L20 -7 M-11 6 H-21 M11 6 H21 M-10 13 L-19 19 M10 13 L19 19" {s}/>'
                f'<path d="M-3 -20 L-7 -24 M3 -20 L7 -24" {s}/>')
    elif kind == "medal":
        body = (f'<path d="M-10 -22 L-4 -6 M10 -22 L4 -6" {s}/>'
                f'<circle cx="0" cy="7" r="14" {s}/>'
                f'<path d="M0 -1 L2.6 4.4 L8.5 5.2 L4.2 9.3 L5.3 15.2 L0 12.4 L-5.3 15.2 L-4.2 9.3 L-8.5 5.2 L-2.6 4.4 Z" {s}/>')
    elif kind == "cap":
        body = (f'<path d="M0 -16 L25 -5 L0 6 L-25 -5 Z" {s}/>'
                f'<path d="M-14 0 V11 C-14 17 14 17 14 11 V0" {s}/><path d="M25 -5 V10" {s}/>'
                f'<circle cx="25" cy="13" r="2.5" fill="{color}"/>')
    else:
        raise ValueError(kind)
    return f'<g transform="scale({size})">{body}</g>'


def write(name, svg):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def rounded_path(x, y, w, h, r):
    """Rounded rect as a <path> d attribute (pathLength works on paths everywhere)."""
    return (f"M{x + r} {y} H{x + w - r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h - r} "
            f"A{r} {r} 0 0 1 {x + w - r} {y + h} H{x + r} A{r} {r} 0 0 1 {x} {y + h - r} "
            f"V{y + r} A{r} {r} 0 0 1 {x + r} {y} Z")


# --------------------------------------------------------------------------- header

def header():
    W, H = 1200, 420
    rnd = random.Random(1337)
    rain = []
    for i in range(34):
        x = 18 + i * 35 + rnd.randint(-6, 6)
        chars = "".join(rnd.choice("01") for _ in range(22))
        dur = rnd.uniform(7, 15)
        delay = -rnd.uniform(0, dur)
        tspans = "".join(f'<tspan x="{x}" dy="19">{c}</tspan>' for c in chars)
        rain.append(f'<text class="rain" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" '
                    f'opacity="{rnd.uniform(0.06, 0.18):.2f}">{tspans}</text>')

    title = "HACKER ROADMAP"
    subtitle = "> choose your path. learn. hack. get hired."
    sub_size = 22
    char_w = sub_size * 0.6
    sub_w = len(subtitle) * char_w
    sub_x = (W - sub_w) / 2
    n = len(subtitle)

    dots = []
    total = len(PATHS)
    gap = 210
    start = W / 2 - gap * (total - 1) / 2
    for i, p in enumerate(PATHS):
        cx = start + i * gap
        dots.append(
            f'<g class="dot" style="animation-delay:{i * 0.35:.2f}s">'
            f'<circle cx="{cx - 62}" cy="352" r="5" fill="{p["color"]}"/>'
            f'<text x="{cx - 50}" y="357" font-family="{MONO}" font-size="13" fill="{MUTED}" '
            f'letter-spacing="1">{escape(p["title"].split()[0].upper())}</text></g>')

    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hacker Roadmap">
<title>Hacker Roadmap</title>
<defs>
  <linearGradient id="title" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{GREEN}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.45" r="0.6">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0.10"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.10"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0 H0 V40" fill="none" stroke="{GREEN}" stroke-opacity="0.10" stroke-width="1"/>
    <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="0 40" dur="4s" repeatCount="indefinite"/>
  </pattern>
  <linearGradient id="fade" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.35" stop-color="#fff" stop-opacity="1"/>
    <stop offset="0.8" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="fademask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="type"><rect class="typer" x="{sub_x:.1f}" y="225" width="{sub_w:.1f}" height="40"/></clipPath>
</defs>
<style>
  .rain{{font-family:{MONO};font-size:15px;fill:{GREEN};animation:fall linear infinite}}
  @keyframes fall{{from{{transform:translateY(-440px)}}to{{transform:translateY(440px)}}}}
  .scan{{animation:scan 6s linear infinite}}
  @keyframes scan{{from{{transform:translateY(-140px)}}to{{transform:translateY({H}px)}}}}
  .typer{{transform-box:fill-box;transform-origin:left;animation:type 9s steps({n},end) infinite}}
  @keyframes type{{0%{{transform:scaleX(0)}}45%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
  .cursor{{animation:cur 9s steps({n},end) infinite,blink 1s step-end infinite}}
  @keyframes cur{{0%{{transform:translateX(0)}}45%,90%{{transform:translateX({sub_w:.1f}px)}}100%{{transform:translateX(0)}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  .g1{{animation:g1 5s infinite}} .g2{{animation:g2 5s infinite}}
  @keyframes g1{{0%,88%,100%{{transform:translate(0,0);opacity:0}}90%{{transform:translate(-5px,2px);opacity:.8}}93%{{transform:translate(4px,-2px);opacity:.8}}96%{{transform:translate(-2px,0);opacity:.6}}}}
  @keyframes g2{{0%,88%,100%{{transform:translate(0,0);opacity:0}}90%{{transform:translate(5px,-2px);opacity:.8}}93%{{transform:translate(-4px,2px);opacity:.8}}96%{{transform:translate(2px,0);opacity:.6}}}}
  .dot{{animation:pulse 2.4s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
  .badge{{animation:pulse 3s ease-in-out infinite}}
  {REDUCED_MOTION}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#fademask)"/>
  <g mask="url(#fademask)">{''.join(rain)}</g>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect class="scan" width="{W}" height="140" fill="url(#scan)"/>

  <g class="badge">
    <rect x="{W/2 - 128}" y="58" width="256" height="30" rx="15" fill="{GREEN}" fill-opacity="0.08" stroke="{GREEN}" stroke-opacity="0.45"/>
    <text x="{W/2}" y="78" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{GREEN}">[ CYBERSECURITY  PATHS ]</text>
  </g>

  <g font-family="{SANS}" font-size="86" font-weight="800" text-anchor="middle" letter-spacing="4">
    <text class="g1" x="{W/2}" y="190" fill="{MAGENTA}">{title}</text>
    <text class="g2" x="{W/2}" y="190" fill="{CYAN}">{title}</text>
    <text x="{W/2}" y="190" fill="url(#title)">{title}</text>
  </g>

  <g clip-path="url(#type)">
    <text x="{sub_x:.1f}" y="254" font-family="{MONO}" font-size="{sub_size}" fill="{TEXT}" xml:space="preserve">{escape(subtitle)}</text>
  </g>
  <rect class="cursor" x="{sub_x + 2:.1f}" y="234" width="12" height="26" fill="{GREEN}"/>

  <path d="M{W/2 - 420} 310 H{W/2 + 420}" stroke="{LINE}" stroke-width="1"/>
  {''.join(dots)}
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{GREEN}" stroke-opacity="0.25"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- cards

def card(p):
    W, H = 400, 230
    c = p["color"]
    border = rounded_path(1.5, 1.5, W - 3, H - 3, 16)
    bars = "".join(
        f'<rect x="{W - 84 + i * 14}" y="{H - 41}" width="9" height="{8 + i * 4}" rx="2" '
        f'transform="translate(0 {-(i * 4)})" fill="{c if i < p["level"] else LINE}"/>'
        for i in range(4))
    tag = "".join(f'<tspan x="28" dy="{0 if i == 0 else 22}">{escape(t)}</tspan>' for i, t in enumerate(p["tag"]))
    pill_w = len(p["pill"]) * 7.8 + 26
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p['title'])}">
<title>{escape(p['title'])}</title>
<defs>
  <radialGradient id="g" cx="0.15" cy="0.2" r="0.9">
    <stop offset="0" stop-color="{c}" stop-opacity="0.18"/><stop offset="1" stop-color="{c}" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  .sweep{{stroke-dasharray:18 82;animation:sweep 5s linear infinite}}
  @keyframes sweep{{to{{stroke-dashoffset:-100}}}}
  .ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}}
  @keyframes ring{{0%{{transform:scale(.8);opacity:.9}}100%{{transform:scale(1.45);opacity:0}}}}
  .float{{animation:float 3.5s ease-in-out infinite}}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
  {REDUCED_MOTION}
</style>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="{PANEL}"/>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="url(#g)"/>
<path d="{border}" fill="none" stroke="{c}" stroke-opacity="0.22" stroke-width="1.5"/>
<path class="sweep" d="{border}" pathLength="100" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round"/>

<circle class="ring" cx="56" cy="58" r="28" fill="none" stroke="{c}" stroke-width="2"/>
<circle cx="56" cy="58" r="28" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.5"/>
<g class="float"><g transform="translate(56 58)">{icon(p['icon'], c, 0.72)}</g></g>

<text x="{W - 28}" y="48" text-anchor="end" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MUTED}">PATH</text>
<text x="{W - 28}" y="80" text-anchor="end" font-family="{MONO}" font-size="30" font-weight="700" fill="{c}">{p['num']}</text>

<text x="28" y="124" font-family="{SANS}" font-size="27" font-weight="800" fill="{TEXT}">{escape(p['title'])}</text>
<text x="28" y="152" font-family="{SANS}" font-size="16" fill="{MUTED}">{tag}</text>

<rect x="28" y="{H - 46}" width="{pill_w:.0f}" height="26" rx="13" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.5"/>
<text x="{28 + pill_w / 2:.0f}" y="{H - 28}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1" fill="{c}">{escape(p['pill'])}</text>
{bars}
</svg>"""


# --------------------------------------------------------------------------- banners

def banner(p):
    W, H = 1200, 260
    c = p["color"]
    cmd = p["cmd"]
    cmd_size = 17
    cmd_w = (len(cmd) + 2) * cmd_size * 0.6
    chips = []
    x = 56
    for chip in p["chips"]:
        w = len(chip) * 7.8 + 28
        chips.append(f'<rect x="{x:.0f}" y="196" width="{w:.0f}" height="28" rx="6" fill="{c}" fill-opacity="0.10" stroke="{c}" stroke-opacity="0.4"/>'
                     f'<text x="{x + w / 2:.0f}" y="215" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1" fill="{c}">{escape(chip)}</text>')
        x += w + 12
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Roadmap for {escape(p['title'])}">
<title>Roadmap for {escape(p['title'])}</title>
<defs>
  <linearGradient id="bg" x1="0" x2="1">
    <stop offset="0" stop-color="{c}" stop-opacity="0.10"/><stop offset="0.6" stop-color="{c}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.2" fill="{c}" fill-opacity="0.18"/>
  </pattern>
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{c}" stop-opacity="0.2"/><stop offset="1" stop-color="{c}"/></linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <clipPath id="type"><rect class="typer" x="78" y="62" width="{cmd_w:.0f}" height="28"/></clipPath>
</defs>
<style>
  .typer{{transform-box:fill-box;transform-origin:left;animation:type 7s steps({len(cmd) + 2},end) infinite}}
  @keyframes type{{0%{{transform:scaleX(0)}}35%,92%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
  .cursor{{animation:cur 7s steps({len(cmd) + 2},end) infinite,blink 1s step-end infinite}}
  @keyframes cur{{0%{{transform:translateX(0)}}35%,92%{{transform:translateX({cmd_w:.0f}px)}}100%{{transform:translateX(0)}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  .orbit{{transform-origin:1040px 140px;animation:spin 14s linear infinite}}
  .orbit2{{transform-origin:1040px 140px;animation:spin 9s linear infinite reverse}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  .float{{animation:float 4s ease-in-out infinite}}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
  .fill{{transform-box:fill-box;transform-origin:left;animation:fill 7s ease-in-out infinite}}
  @keyframes fill{{0%{{transform:scaleX(0)}}60%,100%{{transform:scaleX(1)}}}}
  {REDUCED_MOTION}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{PANEL}"/>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="860" width="340" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="36" fill="{BAR}"/>
  <circle cx="24" cy="18" r="6" fill="#ff5f57"/><circle cx="44" cy="18" r="6" fill="#febc2e"/><circle cx="64" cy="18" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="23" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">hacker-roadmap — path/{p['key']} — PATH {p['num']}</text>

  <text x="56" y="82" font-family="{MONO}" font-size="{cmd_size}" fill="{c}">$</text>
  <g clip-path="url(#type)"><text x="78" y="82" font-family="{MONO}" font-size="{cmd_size}" fill="{TEXT}">{escape(cmd)}</text></g>
  <rect class="cursor" x="80" y="66" width="10" height="21" fill="{c}"/>

  <g>
    <text x="54" y="142" font-family="{SANS}" font-size="46" font-weight="800" fill="{TEXT}">Roadmap for <tspan fill="{c}">{escape(p['title'])}</tspan></text>
    <text x="56" y="176" font-family="{SANS}" font-size="18" fill="{MUTED}">{escape(p['sub'])}</text>
  </g>
  {''.join(chips)}

  <g class="orbit"><circle cx="1040" cy="140" r="78" fill="none" stroke="{c}" stroke-opacity="0.35" stroke-dasharray="4 10"/><circle cx="1118" cy="140" r="5" fill="{c}"/></g>
  <g class="orbit2"><circle cx="1040" cy="140" r="58" fill="none" stroke="{c}" stroke-opacity="0.25"/><circle cx="982" cy="140" r="3.5" fill="{c}"/></g>
  <circle cx="1040" cy="140" r="42" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.6"/>
  <g class="float"><g transform="translate(1040 140)">{icon(p['icon'], c, 1.05)}</g></g>

  <rect x="0" y="{H - 4}" width="{W}" height="4" fill="{LINE}"/>
  <rect class="fill" x="0" y="{H - 4}" width="{W}" height="4" fill="url(#bar)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{c}" stroke-opacity="0.3"/>
</g>
</svg>"""


# --------------------------------------------------------------------------- flows

def flow(p, steps=None, name=None):
    """A row of nodes joined by animated 'data packets', lighting up in sequence."""
    steps = steps or p["flow"]
    c = p["color"]
    W, H = 1200, 160
    n = len(steps)
    margin = 90
    gap = (W - 2 * margin) / (n - 1)
    cycle = 1.1 * n + 2
    xs = [margin + i * gap for i in range(n)]
    parts = [f'<path d="M{xs[0]} 62 H{xs[-1]}" stroke="{LINE}" stroke-width="3"/>',
             f'<path class="flowline" d="M{xs[0]} 62 H{xs[-1]}" stroke="{c}" stroke-width="3" stroke-dasharray="6 14"/>']
    for i, (x, label) in enumerate(zip(xs, steps)):
        delay = i * 1.1
        parts.append(
            f'<g class="node" style="animation-delay:{delay:.1f}s">'
            f'<circle cx="{x:.0f}" cy="62" r="24" fill="{PANEL}" stroke="{c}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="68" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="{c}">{i + 1:02d}</text></g>'
            f'<circle class="halo" style="animation-delay:{delay:.1f}s" cx="{x:.0f}" cy="62" r="24" fill="none" stroke="{c}" stroke-width="2"/>'
            f'<text x="{x:.0f}" y="118" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="600" fill="{TEXT}">{escape(label)}</text>')
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(' → '.join(steps))}">
<title>{escape(' → '.join(steps))}</title>
<style>
  .flowline{{animation:flow 1.2s linear infinite}}
  @keyframes flow{{to{{stroke-dashoffset:-20}}}}
  .node{{animation:node {cycle:.1f}s ease-in-out infinite;opacity:.45}}
  @keyframes node{{0%{{opacity:.45}}{100 * 0.6 / cycle:.1f}%,{100 * (cycle - 1.5) / cycle:.1f}%{{opacity:1}}100%{{opacity:.45}}}}
  .halo{{transform-box:fill-box;transform-origin:center;opacity:0;animation:halo {cycle:.1f}s ease-out infinite}}
  @keyframes halo{{0%{{transform:scale(1);opacity:.9}}{100 * 1.2 / cycle:.1f}%{{transform:scale(1.7);opacity:0}}100%{{opacity:0}}}}
  {REDUCED_MOTION}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{PANEL}" stroke="{c}" stroke-opacity="0.25"/>
<g transform="translate(0 6)">{''.join(parts)}</g>
</svg>"""


def timeline(p):
    """Month-based timeline for the Cyber Expressway."""
    c = p["color"]
    W, H = 1200, 180
    x0, x1 = 80, 1120
    month = (x1 - x0) / 10
    phases = [("TCM PEH", "~2 mo", 0, 2), ("HTB Pentester Path", "~3 mo", 2, 5),
              ("OSCP / PEN-200", "~3 mo", 5, 8), ("Find CVEs", "~2 mo", 8, 10)]
    ticks = "".join(
        f'<path d="M{x0 + i * month:.0f} 92 V102" stroke="{MUTED}" stroke-opacity="0.6"/>'
        f'<text x="{x0 + i * month:.0f}" y="122" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">M{i}</text>'
        for i in range(11))
    blocks = []
    for i, (name, dur, a, b) in enumerate(phases):
        xa, xb = x0 + a * month + 4, x0 + b * month - 4
        blocks.append(
            f'<g class="ph" style="animation-delay:{i * 1.5:.1f}s">'
            f'<rect x="{xa:.0f}" y="40" width="{xb - xa:.0f}" height="40" rx="8" fill="{c}" fill-opacity="{0.10 + i * 0.06:.2f}" stroke="{c}" stroke-opacity="0.6"/>'
            f'<text x="{(xa + xb) / 2:.0f}" y="65" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{TEXT}">{escape(name)}</text>'
            f'<text x="{(xa + xb) / 2:.0f}" y="152" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c}">{escape(dur)}</text></g>')
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Cyber Expressway timeline: 10 months">
<title>Cyber Expressway timeline: 10 months</title>
<style>
  .ph{{opacity:.35;animation:ph 8s ease-in-out infinite}}
  @keyframes ph{{0%{{opacity:.35}}8%,85%{{opacity:1}}100%{{opacity:.35}}}}
  .run{{transform-box:fill-box;transform-origin:left;animation:run 8s linear infinite}}
  @keyframes run{{0%{{transform:scaleX(0)}}80%,100%{{transform:scaleX(1)}}}}
  .head{{animation:head 8s linear infinite}}
  @keyframes head{{0%{{transform:translateX(0)}}80%,100%{{transform:translateX({x1 - x0}px)}}}}
  {REDUCED_MOTION}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{PANEL}" stroke="{c}" stroke-opacity="0.25"/>
<g transform="translate(0 8)">
<text x="{x0}" y="22" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">TIMELINE · 10 MONTHS TO JOB-READY</text>
{''.join(blocks)}
<rect x="{x0}" y="95" width="{x1 - x0}" height="4" rx="2" fill="{LINE}"/>
<rect class="run" x="{x0}" y="95" width="{x1 - x0}" height="4" rx="2" fill="{c}"/>
{ticks}
<g class="head"><circle cx="{x0}" cy="97" r="7" fill="{c}"/><circle cx="{x0}" cy="97" r="13" fill="{c}" fill-opacity="0.25"/></g>
</g>
</svg>"""


# --------------------------------------------------------------------------- misc

def divider():
    W, H = 1200, 24
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
<defs>
  <linearGradient id="p" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .pulse{{animation:move 4s ease-in-out infinite}}
  @keyframes move{{0%{{transform:translateX(-240px)}}100%{{transform:translateX({W}px)}}}}
  {REDUCED_MOTION}
</style>
<path d="M0 12 H{W}" stroke="{LINE}" stroke-width="2"/>
<rect class="pulse" x="0" y="10" width="240" height="4" rx="2" fill="url(#p)"/>
<g fill="{GREEN}"><rect x="{W/2 - 4}" y="8" width="8" height="8" transform="rotate(45 {W/2} 12)"/></g>
</svg>"""


def footer():
    W, H = 1200, 170
    msg = "exit 0  # happy hacking. stay ethical. share the roadmap."
    size = 18
    w = len(msg) * size * 0.6
    x = (W - w - 24) / 2 + 24
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Happy hacking">
<title>Happy hacking</title>
<defs>
  <linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  <clipPath id="type"><rect class="typer" x="{x:.0f}" y="60" width="{w:.0f}" height="30"/></clipPath>
</defs>
<style>
  .typer{{transform-box:fill-box;transform-origin:left;animation:type 8s steps({len(msg)},end) infinite}}
  @keyframes type{{0%{{transform:scaleX(0)}}45%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}
  .cursor{{animation:cur 8s steps({len(msg)},end) infinite,blink 1s step-end infinite}}
  @keyframes cur{{0%{{transform:translateX(0)}}45%,90%{{transform:translateX({w:.0f}px)}}100%{{transform:translateX(0)}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  {REDUCED_MOTION}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{BG}" stroke="{GREEN}" stroke-opacity="0.25"/>
<text x="{x - 24:.0f}" y="82" font-family="{MONO}" font-size="{size}" fill="{GREEN}">$</text>
<g clip-path="url(#type)"><text x="{x:.0f}" y="82" font-family="{MONO}" font-size="{size}" fill="{TEXT}" xml:space="preserve">{escape(msg)}</text></g>
<rect class="cursor" x="{x + 2:.0f}" y="66" width="10" height="22" fill="{GREEN}"/>
<text x="{W/2}" y="128" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{MUTED}">Hacker Roadmap · by <tspan fill="url(#t)" font-weight="700">Hacking-Notes</tspan></text>
</svg>"""


def main():
    write("header.svg", header())
    write("divider.svg", divider())
    write("footer.svg", footer())
    for p in PATHS:
        write(f"cards/{p['key']}.svg", card(p))
        write(f"banners/{p['key']}.svg", banner(p))
        if "flow" in p:
            write(f"flows/{p['key']}.svg", flow(p))
    write("flows/expressway.svg", timeline(PATHS[1]))


if __name__ == "__main__":
    main()
