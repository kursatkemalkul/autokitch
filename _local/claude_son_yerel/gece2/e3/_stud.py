import sys, os, pickle, numpy as np, re, trimesh
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('e3_parca_ham.pkl','rb')); P=D['P']; M=D['MEKK']
comps=[(md,i,o) for md,L in M.items() for i,o in enumerate(L)]
sac=[a for a in P if P[a]['tur'] in('sac','profil')]
def ax_info(V):
    ext=V.max(0)-V.min(0); ax=int(np.argmax(ext)); return ax,ext
for a in sorted(x for x in P if x.startswith(('g_arayuz_mek','g_arayuz_j3'))):
    V=P[a]['V']; ax,ext=ax_info(V); lo,hi=V.min(0),V.max(0)
    # head end: larger cross-section
    s=V[:,ax]; r=lambda m: np.ptp(V[m][:, [k for k in range(3) if k!=ax]],0).max()
    ml=s<lo[ax]+0.6; mh=s>hi[ax]-0.6
    head_lo = r(ml)>r(mh)
    # host sheet: sheet whose box contains head end
    hp=V[ml].mean(0) if head_lo else V[mh].mean(0)
    host=[b for b in sac if np.all(P[b]['V'].min(0)<=hp+0.3) and np.all(P[b]['V'].max(0)>=hp-0.3)]
    # mechanism comps overlapping stud box
    hits=[(md,o['dug'][:28]) for md,i,o in comps if np.all(o['lo']<=hi+0.5) and np.all(o['hi']>=lo-0.5)]
    print(a[2:], 'eks','xyz'[ax], 'boy %.1f'%ext[ax], 'baş', 'alt' if head_lo else 'üst', host[:2], hits[:4])
