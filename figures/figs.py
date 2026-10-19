import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
plt.rcParams.update({'font.family':'Liberation Sans','font.size':8.5,'pdf.fonttype':42,'ps.fonttype':42,
  'mathtext.fontset':'custom','mathtext.rm':'Liberation Sans','mathtext.it':'Liberation Sans:italic','mathtext.bf':'Liberation Sans:bold',
  'axes.linewidth':0.6,'hatch.linewidth':0.5,'savefig.facecolor':'white'})
MM=1/25.4
def save(fig,name):
    for ext,kw in [('png',dict(dpi=1200)),('pdf',{}),('eps',{})]:
        fig.savefig(f'{name}.{ext}',**kw)
    plt.close(fig)
def box(ax,x,y,w,h,text,fs=8.5,lw=0.8,ls='-',bold=False,ha='center',pad=0.0,fc='white',va='center'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=1.2',fc=fc,ec='black',lw=lw,ls=ls))
    tx=x+w/2 if ha=='center' else x+2.2
    ty=y+h/2 if va=='center' else y+h-2.2
    ax.text(tx,ty,text,ha=ha,va=va if va=='center' else 'top',fontsize=fs,fontweight='bold' if bold else 'normal',linespacing=1.25)
def arrow(ax,x1,y1,x2,y2,ls='-',lw=0.8):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=lw,color='black',ls=ls,shrinkA=0,shrinkB=0,mutation_scale=7))
def canvas(wmm,hmm):
    fig=plt.figure(figsize=(wmm*MM,hmm*MM)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,wmm); ax.set_ylim(0,hmm); ax.axis('off'); return fig,ax

# ---------- Fig 1: selection flow ----------
W,H=174,112
fig,ax=canvas(W,H)
box(ax,22,97,130,13,'Search, 9 and 10 October 2026\nSeven themes; Crossref, arXiv, web search, publisher and proceedings pages')
ax.plot([87,87],[97,93],color='black',lw=0.8); ax.plot([46,87],[93,93],color='black',lw=0.8); arrow(ax,46,93,46,88)
box(ax,6,74,80,14,'Records opened and verified on publisher,\nproceedings or repository pages (n = 147)')
arrow(ax,46,74,46,47)
ax.plot([46,94],[60,60],color='black',lw=0.8); arrow(ax,94,60,98,60)
box(ax,98,39,74,42,'',fs=8)
ax.text(101,78,'Not included (n = 62)',ha='left',va='top',fontsize=8.2,fontweight='bold')
ax.text(101,72.5,'Older sources beyond those needed as\n   originals or standards (n = 21)\nPreprints without a peer-reviewed version,\n   not essential (n = 13)\nOutside chest CT, closer source\n   retained (n = 12)\nDetails not verifiable or reporting\n   inconsistent (n = 11)\nRedundant with a retained study (n = 5)',ha='left',va='top',fontsize=8,linespacing=1.28)
box(ax,6,35,80,12,'Sources included in the review (n = 85)',bold=True)
ax.plot([46,46],[35,29],color='black',lw=0.8); ax.plot([40,134],[29,29],color='black',lw=0.8)
arrow(ax,40,29,40,24); arrow(ax,134,29,134,24)
box(ax,6,12,68,12,'Published or first posted online\nin 2025 or 2026 (n = 72)')
box(ax,100,12,68,12,'Older method papers, datasets, standards\nand one earlier reader study (n = 13)')
save(fig,'Fig1')

# ---------- Fig 2: families ----------
W,H=174,96
fig,ax=canvas(W,H)
box(ax,8,82,34,10,'Chest CT volume'); arrow(ax,42,87,58,87)
box(ax,58,82,58,10,'Deep learning model'); arrow(ax,116,87,132,87)
box(ax,132,82,34,10,'Output')
ax.plot([87,87],[82,77],color='black',lw=0.8); ax.plot([24.5,149.5],[77,77],color='black',lw=0.8)
fam=[('Post hoc\nattribution maps','Where in the image\ndid the model look?','Grad-CAM, SHAP, LIME,\nintegrated gradients,\nattention maps'),
     ('Concept-based\nmodels','Which named findings\nled to the output?','Concept bottleneck\nmodels, attribute\nprototypes'),
     ('Anatomically structured,\ncase-based and\ncounterfactual methods','Which lobe? Which similar\ncase? What would change\nthe output?','Lobe-level models, case\nretrieval, prototype\nnetworks, counterfactuals'),
     ('Report-grounded and\nvision-language\nexplanations','What does the model say\nin words, and about\nwhich region?','Image-report pretraining,\nregion-guided report\ngeneration')]
bw=39; gap=3; x0=(W-(4*bw+3*gap))/2
for i,(n,q,m) in enumerate(fam):
    x=x0+i*(bw+gap); arrow(ax,x+bw/2,77,x+bw/2,72)
    ax.add_patch(FancyBboxPatch((x,24),bw,48,boxstyle='round,pad=0,rounding_size=1.2',fc='white',ec='black',lw=0.8))
    ax.text(x+bw/2,70,n,ha='center',va='top',fontsize=8.3,fontweight='bold',linespacing=1.2)
    ax.plot([x+3,x+bw-3],[57,57],color='black',lw=0.4)
    ax.text(x+bw/2,55,q,ha='center',va='top',fontsize=8,fontstyle='italic',linespacing=1.2)
    ax.plot([x+3,x+bw-3],[42,42],color='black',lw=0.4)
    ax.text(x+bw/2,40,m,ha='center',va='top',fontsize=8,linespacing=1.2)
    arrow(ax,x+bw/2,24,x+bw/2,18)
box(ax,x0,2,4*bw+3*gap,16,'')
ax.text(W/2,15,'Evaluation of explanations',ha='center',va='center',fontsize=8.5,fontweight='bold')
ax.text(W/2,10.4,'Is the explanation faithful, plausible, stable and useful to the reader?',ha='center',va='center',fontsize=8,fontstyle='italic')
ax.text(W/2,5.8,'Deletion and insertion tests, randomisation checks, expert rating, reader studies',ha='center',va='center',fontsize=8)
save(fig,'Fig2')

# ---------- Fig 3: evidence map (stacked horizontal bars, black-and-white textures) ----------
fams=['Post hoc attribution\nmaps (n = 12)','Concept-based\nmodels (n = 4)','Anatomically structured,\ncase-based and\ncounterfactual (n = 6)','Report-grounded and\nvision-language (n = 5)']
cats=['Examples only or not stated','Expert rating or agreement','Quantitative measure','Reader study']
data=np.array([[9,2,1,0],[0,0,3,1],[2,1,2,1],[4,0,1,0]])
assert data.sum()==27 and list(data.sum(0))==[15,3,7,2]
styles=[dict(fc='white',hatch=''),dict(fc='white',hatch='////'),dict(fc='white',hatch='xxxx'),dict(fc='black',hatch='')]
fig=plt.figure(figsize=(129*MM,78*MM)); ax=fig.add_axes([0.30,0.33,0.67,0.64])
y=np.arange(len(fams))[::-1]; left=np.zeros(len(fams))
for j,c in enumerate(cats):
    b=ax.barh(y,data[:,j],left=left,height=0.56,edgecolor='black',linewidth=0.7,label=c,**styles[j])
    for i,v in enumerate(data[:,j]):
        if v>0:
            ax.text(left[i]+v/2,y[i],str(v),ha='center',va='center',fontsize=8,fontweight='bold',color='white' if j==3 else 'black',
                    bbox=None if j in (0,3) else dict(fc='white',ec='none',pad=0.8))
    left+=data[:,j]
ax.set_yticks(y); ax.set_yticklabels(fams,fontsize=8); ax.set_xlim(0,12.6); ax.set_xticks(range(0,13,2))
ax.set_xlabel('Number of chest CT studies',fontsize=8.5); ax.tick_params(axis='both',length=2.5,width=0.6,labelsize=8)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.legend(loc='upper center',bbox_to_anchor=(0.30,-0.27),ncol=2,frameon=False,fontsize=8,handlelength=1.8,handleheight=1.1,columnspacing=1.4)
save(fig,'Fig3')

# ---------- Fig 4: CLARITY-CT reference design ----------
W,H=174,104
fig,ax=canvas(W,H)
box(ax,4,62,26,16,'Chest CT\nvolume')
box(ax,40,76,34,14,'Lobe segmentation\nmasks, five lobes')
box(ax,40,52,34,14,'Volumetric encoder\nfeatures')
arrow(ax,30,73,40,81); arrow(ax,30,67,40,60)
box(ax,84,60,30,22,'Lobar pooling\n\nlobar descriptors\nRUL, RML, RLL,\nLUL, LLL',fs=8.2)
arrow(ax,74,81,84,75); arrow(ax,74,60,84,67)
box(ax,124,58,24,26,'Concept layer\n\n23 concepts,\nnon-negative\nweights',fs=8.2)
arrow(ax,114,71,124,71)
box(ax,156,60,15,22,'Findings',fs=8.2)
arrow(ax,148,71,156,71)
# residual pathway routed above the blocks (dashed)
ax.plot([99,99],[82,94],color='black',lw=0.8,ls='--'); ax.plot([99,163.5],[94,94],color='black',lw=0.8,ls='--'); arrow(ax,163.5,94,163.5,82,ls='--')
ax.text(131.25,95.4,'residual pathway with gate; leakage gap reported',ha='center',va='bottom',fontsize=8)
# training-only box
box(ax,4,26,70,18,'Training only: alignment penalty\nAttribution outside the lobes recorded for a\nfinding is penalised (lobe-level labels only)',fs=8,ls='--')
arrow(ax,57,44,57,52,ls='--')
# outputs row, ordered to match the blocks above
outs=['Evidence per lobe\n(exact at lobe level)','Similar past cases\n(prototypes)','Concept\ncontributions','Prediction set\n(conformal calibration)']
ow=39.5; og=3; cx=[4+i*(ow+og)+ow/2 for i in range(4)]
for i,t in enumerate(outs): box(ax,4+i*(ow+og),2,ow,14,t,fs=8.2)
ax.plot([92,92],[60,21],color='black',lw=0.8); ax.plot([cx[0],92],[21,21],color='black',lw=0.8); arrow(ax,cx[0],21,cx[0],16); arrow(ax,cx[1],21,cx[1],16)
ax.plot([136,136],[58,21],color='black',lw=0.8); ax.plot([cx[2],136],[21,21],color='black',lw=0.8); arrow(ax,cx[2],21,cx[2],16)
arrow(ax,163.5,60,163.5,16)
save(fig,'Fig4')

# ---------- Fig 5: geometric vs arithmetic aggregation ----------
F=np.linspace(0,1,401); geo=F**0.25*0.8**0.75; ari=0.25*F+0.75*0.8
fig=plt.figure(figsize=(84*MM,66*MM)); ax=fig.add_axes([0.17,0.17,0.79,0.78])
ax.plot(F,geo,color='black',lw=1.3,ls='-'); ax.plot(F,ari,color='black',lw=1.3,ls=(0,(5,3)))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xlabel('Faithfulness $F$',fontsize=8.5); ax.set_ylabel('Aggregate score',fontsize=8.5)
ax.tick_params(length=2.5,width=0.6,labelsize=8)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.plot([0],[0.6],marker='o',ms=4,mfc='white',mec='black',mew=0.9,clip_on=False,zorder=5); ax.plot([0],[0],marker='o',ms=4,color='black',clip_on=False,zorder=5)
ax.text(0.36,0.90,'Arithmetic mean',fontsize=8,ha='left',va='center'); ax.plot([0.20,0.34],[0.90,0.90],color='black',lw=1.3,ls=(0,(5,3)))
ax.text(0.36,0.33,'Geometric mean (CMXI)',fontsize=8,ha='left',va='center'); ax.plot([0.20,0.34],[0.33,0.33],color='black',lw=1.3)
ax.annotate('0.60 at $F$ = 0',xy=(0,0.6),xytext=(0.05,0.70),fontsize=8,arrowprops=dict(arrowstyle='-',lw=0.5,shrinkA=1,shrinkB=3))
ax.annotate('0 at $F$ = 0',xy=(0,0),xytext=(0.07,0.09),fontsize=8,arrowprops=dict(arrowstyle='-',lw=0.5,shrinkA=1,shrinkB=3))
save(fig,'Fig5')
print('done')
