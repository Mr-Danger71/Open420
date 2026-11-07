# SPDX-FileCopyrightText: 2026 Mr-Danger71 and Open420 contributors
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Generates the single-colour 3D Open420 logo as an SVG.
#
#   pip install fonttools numpy        (plus the Inter font installed)
#   python3 make_logo.py open420-logo-3d-topdown-black.svg "#000"
#   python3 make_logo.py open420-logo-3d-topdown-white.svg "#fff"
#
# Environment overrides: YAW, PITCH (camera angle), K (radio scale),
# DY (vertical offset), FONT (path to Inter-ExtraBold.otf).
import math, sys, os
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

YAW, PITCH = float(os.environ.get("YAW", -30)), float(os.environ.get("PITCH", 34))
K, DY = float(os.environ.get("K", 1.1)), float(os.environ.get("DY", 36))
OUT = sys.argv[1]; INK = sys.argv[2] if len(sys.argv) > 2 else "#000"
GAP = 3.2                      # width of the transparent separation lines

def Ry(t): c, s = math.cos(t), math.sin(t); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rx(t): c, s = math.cos(t), math.sin(t); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
R = Rx(math.radians(PITCH)) @ Ry(math.radians(YAW))
def proj(p): q = R @ np.asarray(p, float); return (float(q[0]), float(-q[1]))

def hull(pts):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def poly(pts): return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"

def rrect(w, h, r, seg=12):
    pts = []
    for cx, cy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90*i/seg); pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return pts
def circle(r, seg=48): return [(r*math.cos(2*math.pi*i/seg), r*math.sin(2*math.pi*i/seg)) for i in range(seg)]

BW, BH, BD = 100, 150, 38
prof = rrect(BW, BH, 17)
front = [proj((x, y, BD/2)) for x, y in prof]
back = [proj((x, y, -BD/2)) for x, y in prof]
body = hull(front + back)

def cylinder(x, z, r, y0, h):
    bot = [proj((x + u, y0, z + v)) for u, v in circle(r)]
    top = [proj((x + u, y0 + h, z + v)) for u, v in circle(r)]
    return hull(bot + top), top
knob, knob_cap = cylinder(-26, 0, 10, BH/2, 12)
AX = 26
stub, stub_cap = cylinder(AX, 0, 9, BH/2, 14)

def plane_matrix(zf, ox, oy):
    r0, r1 = R[0], R[1]
    a, c, b, d = r0[0], -r0[1], -r1[0], r1[1]
    e = r0[0]*ox + r0[1]*oy + r0[2]*zf
    f = -(r1[0]*ox + r1[1]*oy + r1[2]*zf)
    return f"matrix({a:.5f},{b:.5f},{c:.5f},{d:.5f},{e:.3f},{f:.3f})"
front_m = plane_matrix(BD/2, 0, BH/2)

def find_font():
    if os.environ.get("FONT"):
        return os.environ["FONT"]
    import subprocess
    try:
        return subprocess.run(["fc-match", "-f", "%{file}", "Inter:style=ExtraBold"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        sys.exit("Inter ExtraBold not found: install the Inter font or set FONT=/path/to/Inter-ExtraBold.otf")
font = TTFont(find_font())
gs = font.getGlyphSet(); cmap = font.getBestCmap(); s = 64/font["head"].unitsPerEm
def glyph(ch, baseline):
    g = gs[cmap[ord(ch)]]; bp = BoundsPen(gs); g.draw(bp); xmin, ymin, xmax, ymax = bp.bounds
    pen = SVGPathPen(gs); g.draw(TransformPen(pen, (s,0,0,-s, -(xmax-xmin)*s/2 - xmin*s, baseline)))
    return pen.getCommands(), ymax*s
STEP = 55; ystub = BH/2 + 14
d0, gh = glyph("0", 0); d2, _ = glyph("2", -STEP); d4, _ = glyph("4", -2*STEP)
digits = f'<path d="{d0}"/><path d="{d2}"/><path d="{d4}"/>'
TD = 9; oy = ystub + 3
dig_front_m = plane_matrix(TD/2, AX, oy)
N = 40
ext = "".join(f'<g transform="{plane_matrix(-TD/2 + TD*i/N, AX, oy)}">{digits}</g>' for i in range(N))
digits_all = ext + f'<g transform="{dig_front_m}">{digits}</g>'     # full solid of the antenna

tip = proj((AX, oy + 2*STEP + gh + 6, 0))
CX, CY, Rr, RW = 200, 268, 146, 15
bx, by = zip(*body)
TX, TY = CX - (min(bx)+max(bx))/2*K, CY + DY - (min(by)+max(by))/2*K
tipx, tipy = tip[0]*K + TX, tip[1]*K + TY
G = f"translate({TX:.3f},{TY:.3f}) scale({K})"

def arc(r, a0=-140, a1=-40):
    p0 = (tipx + r*math.cos(math.radians(a0)), tipy + r*math.sin(math.radians(a0)))
    p1 = (tipx + r*math.cos(math.radians(a1)), tipy + r*math.sin(math.radians(a1)))
    return f"M{p0[0]:.2f},{p0[1]:.2f} A{r},{r} 0 0 1 {p1[0]:.2f},{p1[1]:.2f}"
arcs = "".join(f'<path d="{arc(r)}"/>' for r in (18, 33, 48))

ant = [proj((AX + sx*21, y, sz*TD/2)) for sx in (-1,1) for sz in (-1,1) for y in (BH/2, oy + 2*STEP + gh)]
kx0 = min(p[0] for p in ant)*K + TX - 7; kx1 = max(p[0] for p in ant)*K + TX + 7

g2 = GAP*2; W = 'fill="#fff"'; B = 'fill="#000"'
def cut(inner): return f'<g fill="#000" stroke="#000" stroke-width="{g2}" stroke-linejoin="round">{inner}</g>'
def cutline(inner): return f'<g fill="none" stroke="#000" stroke-width="{GAP}" stroke-linejoin="round">{inner}</g>'
FULL = '<rect x="-2000" y="-2000" width="4000" height="4000" fill="#fff"/>'

front_holes = f'''<rect x="-36" y="16" width="72" height="42" rx="7" fill="#000"/>
  <rect x="-30" y="22" width="60" height="30" rx="3" fill="#fff"/>
  {''.join(f'<rect x="-30" y="{74+i*14}" width="60" height="7" rx="3.5" fill="#000"/>' for i in range(4))}'''
# bezel is a transparent ring; screen + slots read as cut-outs

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 430" width="400" height="430">
  <title>Open420 logo</title>
  <defs>
    <mask id="mRing" maskUnits="userSpaceOnUse" x="0" y="0" width="400" height="430">
      {FULL}
      <rect x="{kx0:.2f}" y="0" width="{kx1-kx0:.2f}" height="215" fill="#000"/>
      <g transform="{G}">{cut(f'<path d="{poly(body)}"/>')}</g>
    </mask>
    <mask id="mBody" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">
      {FULL}
      {cut(f'<path d="{poly(front)}"/><path d="{poly(knob)}"/><path d="{poly(stub)}"/>{digits_all}')}
    </mask>
    <mask id="mFront" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">
      {FULL}
      <g transform="{front_m}">{front_holes}</g>
      {cut(digits_all)}
    </mask>
    <mask id="mKnob" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">
      {FULL}{cutline(f'<path d="{poly(knob_cap)}"/>')}
    </mask>
    <mask id="mStub" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">
      {FULL}{cut(digits_all)}{cutline(f'<path d="{poly(stub_cap)}"/>')}
    </mask>
    <mask id="mExt" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="4000" height="4000">
      {FULL}<g transform="{dig_front_m}" fill="#000" stroke="#000" stroke-width="{g2}" stroke-linejoin="round">{digits}</g>
    </mask>
  </defs>
  <g fill="{INK}">
    <circle cx="{CX}" cy="{CY}" r="{Rr}" fill="none" stroke="{INK}" stroke-width="{RW}" mask="url(#mRing)"/>
    <g fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round">{arcs}</g>
    <g transform="{G}">
      <path d="{poly(body)}" mask="url(#mBody)"/>
      <path d="{poly(front)}" mask="url(#mFront)"/>
      <path d="{poly(knob)}" mask="url(#mKnob)"/>
      <path d="{poly(stub)}" mask="url(#mStub)"/>
      <g mask="url(#mExt)">{ext}</g>
      <g transform="{dig_front_m}">{digits}</g>
    </g>
  </g>
</svg>
'''
open(OUT, "w").write(svg)
