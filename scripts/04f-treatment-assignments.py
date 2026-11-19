"""Illustrate fixed patient outcomes and alternative treatment assignments."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/661-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Ellipse, FancyBboxPatch
from matplotlib.path import Path as MPath

ROOT = Path(__file__).resolve().parent.parent
GREEN = '#315c43'
fig, axes = plt.subplots(1, 2, figsize=(10, 6.5))
fig.patch.set_facecolor('white')

def acorn(ax, x, y):
    vertices = [(x-.21,y+.06),(x-.23,y-.17),(x,y-.32),(x+.23,y-.17),
                (x+.21,y+.06),(x,y+.13),(x-.21,y+.06)]
    codes = [MPath.MOVETO]+[MPath.CURVE3]*6
    ax.add_patch(PathPatch(MPath(vertices,codes),facecolor='#e6eedf',edgecolor=GREEN,lw=1.5))
    ax.add_patch(Ellipse((x,y+.07),.47,.18,facecolor='#d3b27a',edgecolor=GREEN,lw=1.3))
    ax.plot([x,x+.04],[y+.16,y+.24],color=GREEN,lw=1.7)

def medication(ax,x,y):
    ax.text(x,y-.48,'Medication',ha='center',va='center',fontsize=9,color=GREEN,
            bbox=dict(boxstyle='round,pad=.26',fc='#fff8e8',ec='#b7791f',lw=1.2))

for panel, ax in enumerate(axes):
    ax.set(xlim=(-.8,3.3),ylim=(-.8,5.05));ax.axis('off')
    ax.text(1.25,4.85,['Observed assignment','Another possible assignment'][panel],
            ha='center',fontsize=13,weight='bold',color=GREEN)
    ax.text(.45,4.3,'Hospitalized',ha='center',fontsize=10,color=GREEN)
    ax.text(2.1,4.3,'Not hospitalized',ha='center',fontsize=10,color=GREEN)
    for row in range(4):
        y=3.7-row
        ax.add_patch(FancyBboxPatch((-.68,y-.67),3.8,.99,boxstyle='round,pad=.02',
                                   fc='#fafbf8',ec='#dce3d9',lw=.8,zorder=0))
        ax.text(-.52,y-.1,f'Pair {row+1}',ha='left',va='center',fontsize=8,color='#59655b')
        for x in [.45,2.1]:acorn(ax,x,y)
        medication(ax,.45 if panel==0 or row%2==0 else 2.1,y)
    ax.text(1.25,-.65,['4 hospitalizations among treated patients',
                      '2 hospitalizations among treated patients'][panel],
            ha='center',fontsize=10,color=GREEN)
fig.text(.5,.03,'Each acorn is the same patient in both panels. Only the medication labels move.',
         ha='center',fontsize=10,color=GREEN)
fig.subplots_adjust(left=.02,right=.99,top=.98,bottom=.10,wspace=.14)
fig.savefig(ROOT/'images/04f-treatment-assignments.svg',bbox_inches='tight')
fig.savefig('/tmp/04f-treatment-assignments.png',dpi=150,bbox_inches='tight')
