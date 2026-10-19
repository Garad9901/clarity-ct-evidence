"""Graphical abstract for MBEC: 32.93 mm x 37.63 mm at 100 %, drawn from the counts in the article."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

plt.rcParams.update({'font.family': 'Liberation Sans', 'savefig.facecolor': 'white'})
MM = 1 / 25.4
W, H = 32.93, 37.63
INK, INK2 = '#0b0b0b', '#52514e'
cats = [('Examples only or none', 15, '#eb6834'), ('Quantitative measure', 7, '#2a78d6'),
        ('Expert rating or agreement', 3, '#1baf7a'), ('Reader study', 2, '#6250d6')]
assert sum(c[1] for c in cats) == 27

fig = plt.figure(figsize=(W * MM, H * MM)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

ax.text(W / 2, H - 1.9, 'Explainable AI for chest CT', ha='center', va='center', fontsize=6, fontweight='bold', color=INK)
ax.text(W / 2, H - 5.5, 'How 27 studies (2025–2026)\nassessed their explanations', ha='center', va='center',
        fontsize=5, color=INK2, linespacing=1.15)

# stacked bar with a 0.25 mm surface gap between segments and numbers on the segments
x0, y0, bw, bh, gap = 2.0, H - 12.9, W - 4.0, 3.6, 0.25
x = x0; unit = (bw - gap * (len(cats) - 1)) / 27
for name, n, col in cats:
    w = n * unit
    ax.add_patch(Rectangle((x, y0), w, bh, fc=col, ec='none'))
    ax.text(x + w / 2, y0 + bh / 2, str(n), ha='center', va='center', fontsize=5, fontweight='bold', color='white')
    x += w + gap

# legend, one row per category, label in text ink beside a colour key
ly = y0 - 2.0
for name, n, col in cats:
    ax.add_patch(Rectangle((x0, ly - 0.8), 1.6, 1.6, fc=col, ec='none'))
    ax.text(x0 + 2.4, ly, name, ha='left', va='center', fontsize=5, color=INK)
    ly -= 2.35

# proposal box
by = 1.2; bhh = ly - by + 0.3
ax.add_patch(FancyBboxPatch((1.2, by), W - 2.4, bhh, boxstyle='round,pad=0,rounding_size=0.8', fc='#eef3fb', ec='#2a78d6', lw=0.5))
ax.text(W / 2, by + bhh / 2, 'Proposed (untested):\nlobe-level concepts and a\nnon-compensatory quality index',
        ha='center', va='center', fontsize=5, color=INK, linespacing=1.2)

base = '/home/claude/figs/Graphical_Abstract_Bhowate'
fig.savefig('/home/claude/figs/_ga_tmp.png', dpi=600)
from PIL import Image
Image.open('/home/claude/figs/_ga_tmp.png').convert('RGB').save(base + '.tif', dpi=(600, 600), compression='tiff_lzw')
fig.savefig(base + '.pdf'); fig.savefig(base + '.eps')
fig.savefig('/home/claude/figs/ga_preview.png', dpi=1200)
print('ok')
