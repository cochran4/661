"""Reproduce the RD teaching figures and numerical examples. Run python3 rd-examples.py."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/661-rd-matplotlib')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'images'
plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'svg.fonttype': 'none'})
GREEN, ROSE = '#315C43', '#9B6A75'

# New gridded curves for the chapter exercises; these are idealized mean curves.
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
for ax,c,left_mean,right_mean,slope,ylim,yticks,title,xlabel,ylabel in [
    (axes[0],0,100,90,.5,(80,110),np.arange(80,111,5),
     'A. Split flow','Minutes relative to start','Mean time to disposition (minutes)'),
    (axes[1],20,6,10,.25,(0,14),np.arange(0,15,2),
     'B. Clinical treatment','Risk score','Mean symptom score')]:
    xl,xr=np.linspace(c-4,c,100),np.linspace(c,c+4,100)
    ax.plot(xl,left_mean+slope*(xl-c),color=GREEN,lw=3)
    ax.plot(xr,right_mean+slope*(xr-c),color=ROSE,lw=3)
    ax.plot(c,left_mean,'o',mfc='white',mec=GREEN,mew=2,ms=7)
    ax.plot(c,right_mean,'o',color=ROSE,ms=7)
    ax.axvline(c,color='#777777',ls='--',lw=1)
    ax.set(xlim=(c-4,c+4),ylim=ylim,xticks=np.arange(c-4,c+5,2),
           yticks=yticks,title=title,xlabel=xlabel,ylabel=ylabel)
    ax.set_axisbelow(True);ax.grid(alpha=.3)
fig.tight_layout(pad=1.5,w_pad=2)
fig.savefig(OUT/'04c-rd-exercise-curves.svg')
fig.savefig('/private/tmp/04c-rd-exercise-curves.png');plt.close(fig)

# Hypothetical score frequencies: appeals shift observations toward eligibility.
score_bins=np.arange(70,90)
score_counts=np.array([24,26,25,27,24,26,25,24,12,8,58,25,27,24,26,25,24,27,26,25])
fig,ax=plt.subplots(figsize=(8,4.8))
ax.bar(score_bins,score_counts,width=.85,
       color=[GREEN if s<80 else ROSE for s in score_bins])
ax.axvline(79.5,ls='--',color='#444444',lw=1.5)
ax.set(xlim=(69,90),ylim=(0,65),xticks=[70,75,79,80,85,89],
       xlabel='Placement-test score',ylabel='Number of students')
ax.set_axisbelow(True);ax.grid(axis='y',alpha=.25)
fig.tight_layout(pad=1.5);fig.savefig(OUT/'04c-rd-score-bunching.svg')
fig.savefig('/private/tmp/04c-rd-score-bunching.png');plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot([0,1],[100,80],'-o',color=GREEN,lw=2.5,label='Department introducing split flow')
ax.plot([0,1],[80,75],'-o',color=ROSE,lw=2.5,label='Comparison department')
ax.plot([0,1],[100,95],'--',color=GREEN,lw=2,label='Without split flow: parallel trend')
ax.scatter([1],[95],facecolors='white',edgecolors=GREEN,s=65,zorder=5)
ax.annotate('',xy=(1.08,95),xytext=(1.08,80),
            arrowprops={'arrowstyle':'<->','color':'#444444'})
ax.text(1.12,87.5,'Effect:\n−15 minutes',va='center',fontsize=11)
for x,y,dx,dy in [(0,100,-.04,2),(0,80,-.04,2),(1,80,-.08,2),(1,75,-.08,-4),(1,95,-.08,2)]:
    ax.text(x+dx,y+dy,str(y),fontsize=11)
ax.set(xlim=(-.15,1.55),ylim=(68,108),xticks=[0,1],xticklabels=['Before','After'],
       yticks=[70,80,90,100],ylabel='Mean time to disposition (minutes)')
ax.grid(axis='y',alpha=.25)
ax.legend(loc='upper center',bbox_to_anchor=(.5,1.28),frameon=False,fontsize=10)
fig.tight_layout(pad=1.5)
fig.savefig(OUT/'04c-did-parallel-trends.svg')
fig.savefig('/private/tmp/04c-did-parallel-trends.png');plt.close(fig)

# Illustrative covariate checks: identical scales make a jump easy to compare.
scores = np.array([71,73,75,77,79,81,83,85,87,89])
smooth = np.array([44,47,45,48,49,50,51,50,53,54])
jump = smooth + (scores >= 80)*20
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharex=True, sharey=True)
for ax, values, title, offset in zip(axes,[smooth,jump],
        ['Gradual change through the cutoff','A jump at the cutoff'],[0,20]):
    for side, color in [(scores<80,GREEN),(scores>=80,ROSE)]:
        ax.scatter(scores[side],values[side],s=35,color=color,zorder=4)
    xl,xr=np.linspace(70,80,100),np.linspace(80,90,100)
    ax.plot(xl,50+.5*(xl-80),color=GREEN,lw=2)
    ax.plot(xr,50+.5*(xr-80)+offset,color=ROSE,lw=2)
    ax.axvline(80,ls='--',color='#777777',lw=1)
    ax.set(xlim=(70,90),ylim=(0,100),xticks=[70,75,80,85,90],
           yticks=[0,20,40,60,80,100],xlabel='Placement-test score',title=title)
    ax.grid(axis='y',alpha=.25)
axes[0].set_ylabel('Women (%)')
fig.tight_layout(pad=1.5,w_pad=2)
fig.savefig(OUT/'04c-rd-gender-balance.svg')
fig.savefig('/private/tmp/04c-rd-gender-balance.png');plt.close(fig)

def identification_picture(name, stage):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    left, right = np.linspace(-4,0,150), np.linspace(0,4,150)
    label0 = r'$m(r)$' if stage == 'jump' else r'$m(r)=m_0(r)$'
    label1 = r'$m(r)=m_1(r)$' if stage in ('right','continuity') else r'$m(r)$'
    ax.plot(left,8+left,color=GREEN,lw=3,label=label0)
    ax.plot(right,14+.5*right,color=ROSE,lw=3,label=label1)
    if stage == 'continuity':
        ax.plot(right,8+right,color=GREEN,lw=2,ls='--')
        ax.plot(left,14+.5*left,color=ROSE,lw=2,ls='--')
    ax.plot(0,8,'o',mfc='white',mec=GREEN,mew=2,ms=7,zorder=5)
    ax.plot(0,14,'o',color=ROSE,ms=7,zorder=5)
    ax.axvline(0,color='#777777',ls=':',lw=1)
    if stage in ('jump','continuity'):
        ax.annotate('',xy=(.2,14),xytext=(.2,8),
                    arrowprops={'arrowstyle':'<->','color':'#444444'})
        ax.text(.45,11,'Jump' if stage=='jump' else 'Effect at c',va='center')
    ax.set(xlim=(-4.3,4.3),ylim=(0,20),xticks=[0],xticklabels=['c'],yticks=[],
           xlabel='Arrival time r',ylabel='Mean time to disposition')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.12),ncol=2,frameon=False)
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT/name)
    fig.savefig(Path('/private/tmp')/name.replace('.svg','.png'))
    plt.close(fig)

for filename, stage in [('04c-regression-discontinuity-jump.svg','jump'),
                         ('04c-rd-left.svg','left'),('04c-rd-right.svg','right'),
                         ('04c-rd-continuity.svg','continuity')]:
    identification_picture(filename,stage)

def picture(name, left, right):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x0, x1 = np.linspace(-4, 0, 100), np.linspace(0, 4, 100)
    ax.plot(x0, left(x0), color=GREEN, lw=3)
    ax.plot(x1, right(x1), color=ROSE, lw=3)
    ax.plot(0, left(0), 'o', ms=8, mfc='white', mec=GREEN, mew=2)
    ax.plot(0, right(0), 'o', ms=8, color=ROSE)
    ax.set(xlim=(-4, 4), ylim=(0, 20), xticks=np.arange(-4, 5),
           yticks=np.arange(0, 21, 2), xlabel='Running variable r (cutoff c = 0)',
           ylabel='Mean outcome')
    ax.grid(True, color='#dddddd', linewidth=.7)
    ax.axvline(0, ls='--', color='#555555', lw=1)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(OUT / name)
    fig.savefig(Path('/private/tmp') / name.replace('.svg', '.png'))
    plt.close(fig)

picture('04c-rd-grid-worked.svg', lambda r: 8+r, lambda r: 14+.5*r)
picture('04c-rd-grid-exercise.svg', lambda r: 12+.5*r, lambda r: 6+.5*r)

# A curve that fits every observed point can extrapolate very poorly.
x_fit = np.linspace(-4, -.5, 8)
y_fit = 8 + x_fit + np.random.default_rng(19).normal(0, .3, 8)
straight = np.polynomial.Polynomial.fit(x_fit, y_fit, 1)
wiggly = np.polynomial.Polynomial.fit(x_fit, y_fit, 7)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
for ax, limits in zip(axes, [(-4.1, -.45), (-.7, .025)]):
    xx = np.linspace(*limits, 800)
    for model, color, label in [(straight, GREEN, 'Straight line'),
                                 (wiggly, ROSE, 'Degree-7 curve')]:
        observed = xx <= -.5
        ax.plot(xx[observed], model(xx[observed]), color=color, lw=2, label=label)
        ax.plot(xx[~observed], model(xx[~observed]), color=color, lw=2, ls='--')
    ax.scatter(x_fit, y_fit, color='#244635', zorder=5)
    ax.set(xlim=limits, xlabel='Running variable r')
    ax.grid(alpha=.2)
axes[0].set(ylim=(3,9), ylabel='Outcome', title='Fit where observations are available')
axes[0].legend(loc='upper left')
axes[1].axvline(0, color='#777777', ls=':')
axes[1].scatter([0,0], [straight(0),wiggly(0)], color=[GREEN,ROSE], zorder=6)
axes[1].scatter([0],[8],marker='*',s=140,color='#333333',zorder=7)
axes[1].set(ylim=(-55,12), title='Extrapolate to the cutoff c = 0')
axes[1].annotate('True mean: 8', (0,8), xytext=(-.5,1),
                  arrowprops={'arrowstyle':'->','color':'#444444'}, fontsize=10)
axes[1].annotate('Wiggly prediction: -48.2', (0,wiggly(0)), xytext=(-.65,-40),
                  arrowprops={'arrowstyle':'->','color':ROSE}, fontsize=10,color=ROSE)
fig.tight_layout();fig.savefig(OUT/'04c-rd-overfit.svg')
fig.savefig('/private/tmp/04c-rd-overfit.png');plt.close(fig)
print('OVERFIT: training MSE, prediction at 0')
for model in [straight,wiggly]:
    print(float(np.mean((y_fit-model(x_fit))**2)),float(model(0)))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, limits, ylabel in [(axes[0], (.3,.7), 'Treatment probability'),
                           (axes[1], (10,12), 'Mean outcome')]:
    ax.plot([16,20], [limits[0]]*2, color=GREEN, lw=3)
    ax.plot([20,24], [limits[1]]*2, color=ROSE, lw=3)
    ax.plot(20,limits[0], 'o', mfc='white', mec=GREEN, ms=7)
    ax.plot(20,limits[1], 'o', color=ROSE, ms=7)
    ax.axvline(20,ls='--',color='#777777',lw=1)
    ax.set(xlim=(16,24),xlabel='Risk score (cutoff = 20)',ylabel=ylabel)
    ax.set_yticks(limits);ax.grid(alpha=.3)
axes[0].set_ylim(0,1);axes[1].set_ylim(9,13)
fig.tight_layout();fig.savefig(OUT/'04c-rd-fuzzy.svg')
fig.savefig('/private/tmp/04c-rd-fuzzy.png');plt.close(fig)

d = np.genfromtxt(ROOT / 'data/rd-senate.csv', delimiter=',', names=True)
d = d[np.isfinite(d['margin']) & np.isfinite(d['vote'])]
r, y = d['margin'], d['vote']

def fit(x, z):
    return np.linalg.lstsq(np.column_stack([np.ones(len(x)), x]), z, rcond=None)[0]

print('Complete cases:', len(d))
near = d[np.argsort(np.abs(d['margin']))[:8]]
near = near[np.argsort(near['margin'])]
print('NEAREST 8 (state identifier, year, margin, vote)')
for row in near:
    print(int(row['state']), int(row['year']), f"{row['margin']:.6f}", f"{row['vote']:.6f}")
print('Eight-row means:', near['vote'][near['margin']<0].mean(),
      near['vote'][near['margin']>=0].mean())
print('BANDWIDTH: h, nleft, nright, meanleft, meanright, s2left, s2right, meanjump, variance(meanjump), interceptleft, interceptright, linearjump')
for h in [5, 10, 15, 20, 30]:
    l, u = (r<0)&(r>=-h), (r>=0)&(r<=h)
    v = y[l].var(ddof=1)/l.sum()+y[u].var(ddof=1)/u.sum()
    bl, bu = fit(r[l],y[l]), fit(r[u],y[u])
    print(h, l.sum(),u.sum(), *[round(t,4) for t in [y[l].mean(),y[u].mean(),
        y[l].var(ddof=1),y[u].var(ddof=1),y[u].mean()-y[l].mean(),v,bl[0],bu[0],bu[0]-bl[0]]])

h=10
fig,ax=plt.subplots(figsize=(8,4.8))
for mask,color in [((r<0)&(r>=-h),GREEN),((r>=0)&(r<=h),ROSE)]:
    ax.scatter(r[mask],y[mask],s=15,alpha=.4,color=color)
    xx=np.linspace(r[mask].min(),r[mask].max(),100)
    xx=np.append(xx,0); xx.sort()
    b=fit(r[mask],y[mask]); ax.plot(xx,b[0]+b[1]*xx,color=color,lw=3)
ax.axvline(0,ls='--',color='#555555')
ax.set(xlabel='Democratic victory margin (percentage points)',ylabel='Later Democratic vote share (%)',
       title='Senate elections: separate linear fits, h = 10')
fig.tight_layout();fig.savefig(OUT/'04c-rd-senate-h10.svg')
fig.savefig('/private/tmp/04c-rd-senate-h10.png');plt.close(fig)

# Same held-out observations for every h. Training is strictly outward from each point.
validation = np.flatnonzero(np.abs(r)<=5)
print('BOUNDARY CROSS-VALIDATION (same validation observations, |r| <= 5)')
for h in [5,10,15,20,30]:
    losses=[]
    for i in validation:
        mask = ((r>=r[i]-h)&(r<r[i])) if r[i]<0 else ((r>r[i])&(r<=r[i]+h))
        if mask.sum()<3: raise ValueError('Too few training observations')
        b=fit(r[mask]-r[i],y[mask])
        losses.append((y[i]-b[0])**2)
    print(h,len(losses),round(np.mean(losses),4))

# Repeated samples reveal bias, unlike a single real dataset.
rng=np.random.default_rng(661)
hs=[.5,1,2,4]
estimates=np.empty((4000,len(hs)))
for k in range(len(estimates)):
    x=rng.uniform(-4,4,400)
    z=10+x+.4*x*x+(x>=0)*(4+.8*x*x)+rng.normal(0,2,400)
    for j,h in enumerate(hs):
        l=(x<0)&(x>=-h);u=(x>=0)&(x<=h)
        estimates[k,j]=fit(x[u],z[u])[0]-fit(x[l],z[l])[0]
print('SIMULATION: h, mean estimate, bias, sample variance, mean squared error')
for j,h in enumerate(hs):
    e=estimates[:,j]
    print(h,*[round(t,4) for t in [e.mean(),e.mean()-4,e.var(ddof=1),np.mean((e-4)**2)]])
fig,ax=plt.subplots(figsize=(8,4.8))
ax.boxplot(estimates,tick_labels=hs,showfliers=False)
ax.axhline(4,color=ROSE,ls='--',label='True effect = 4')
ax.set(xlabel='Bandwidth h',ylabel='Estimated effect',title='4,000 repeated samples; 400 observations per sample')
ax.legend();fig.tight_layout();fig.savefig(OUT/'04c-rd-bandwidth-boxplots.svg')
fig.savefig('/private/tmp/04c-rd-bandwidth-boxplots.png');plt.close(fig)
