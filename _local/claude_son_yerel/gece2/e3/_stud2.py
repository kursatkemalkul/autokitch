import sys, os, pickle, numpy as np, re, trimesh
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('e3_parca_ham.pkl','rb')); P=D['P']; M=D['MEKK']
comps=[(md,i,o) for md,L in M.items() for i,o in enumerate(L)]
TM={}
def tm(k,o):
    if k not in TM: TM[k]=trimesh.Trimesh(o['V'],o['F'],process=False)
    return TM[k]
sac=[a for a in P if P[a]['tur'] in('sac','profil')]
OUT={}
for a in sorted(x for x in P if x.startswith(('g_arayuz_mek','g_arayuz_j3'))):
    V=P[a]['V']; lo,hi=V.min(0),V.max(0); ext=hi-lo; ax=int(np.argmax(ext))
    s=V[:,ax]; oth=[k for k in range(3) if k!=ax]
    ml=s<lo[ax]+0.6; mh=s>hi[ax]-0.6
    rl=np.ptp(V[ml][:,oth],0).max(); rh=np.ptp(V[mh][:,oth],0).max()
    e=np.zeros(3); e[ax]=1.0 if rl>rh else -1.0   # baş → uç yönü
    c=(lo+hi)/2; bas=c.copy(); bas[ax]= lo[ax] if e[ax]>0 else hi[ax]; uc=c.copy(); uc[ax]= hi[ax] if e[ax]>0 else lo[ax]
    # ray from head along e, also offset rays at r=3.2 (outside stud Ø5 to see hole wall) 
    res=[]
    for off in [np.zeros(3)]+[np.eye(3)[k]*3.3*sg for k in oth for sg in (1,-1)]:
        p0=bas+off-e*1.0
        hits=[]
        for md,i,o in comps:
            if np.any(o['lo']>np.maximum(p0,p0+e*60)+0.5) or np.any(o['hi']<np.minimum(p0,p0+e*60)-0.5): continue
            loc,_,_=tm((md,i),o).ray.intersects_location([p0],[e])
            for l in loc:
                d=float((l-p0)@e)-1.0
                if -0.5<=d<=60: hits.append((round(d,2),md,o['dug'][:26]))
        res.append(sorted(hits))
    L=float(ext[ax])
    print(a[2:],'L',round(L,1),'e',e.astype(int).tolist())
    print('   eksen:',res[0][:6]); print('   r3.3 :',res[1][:6])
    OUT[a]=dict(e=e,bas=bas,uc=uc,L=L,eksen=res[0],yan=res[1:])
pickle.dump(OUT,open('_stud2.pkl','wb'))
