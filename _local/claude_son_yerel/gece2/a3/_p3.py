import sys, os, json, numpy as np, pickle, trimesh
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g=G(os.path.join(HERE,'..','..','hat3_v9l.glb'))
ENT=json.load(open(os.path.join(HERE,'..','adim8','is_tam','hat3_v9a_ent.json'),encoding='utf-8'))['parca']
C=pickle.load(open('cevre_bil.pkl','rb'))
cache={}
def ent(a):
    v=ENT[a]; d=v['dugum']
    if d not in cache: cache[d]=g.tris(g.byname[d])[0][:2]
    X,T=cache[d]; s,n=v['indis']; Tt=T[s//3:(s+n)//3]; u,inv=np.unique(Tt.reshape(-1),return_inverse=True); return X[u],inv.reshape(-1,3)
M={}
for a in ENT: M[a]=ent(a)
for i,o in enumerate(C): M['C%d_%s_%d'%(i,o['dug'],o['mek'])]=(o['V'],o['F'])
TM={k:trimesh.Trimesh(V,F,process=False) for k,(V,F) in M.items()}
def ray(p,d,L=200):
    p=np.array(p,float); d=np.array(d,float); out=[]
    for k,tm in TM.items():
        lo,hi=tm.bounds
        q0=p; q1=p+d*L; blo=np.minimum(q0,q1)-1; bhi=np.maximum(q0,q1)+1
        if np.any(lo>bhi) or np.any(hi<blo): continue
        loc,ir,it=tm.ray.intersects_location([p],[d])
        for l in loc:
            s=float((l-p)@d)
            if 0<=s<=L: out.append((round(s,2),k))
    return sorted(out)
for nm,p,d in [('acici M8',(1041,930,-645),(0,-1,0)),('tabla M6',(880,930,-320),(0,-1,0)),('tabla M6 b',(1300,930,-20),(0,-1,0)),('AB M8',(761,900,-706),(0,-1,0)),('AB M8 c',(1086,900,-110),(0,-1,0)),('T M8',(1400,1300,-300),(1,0,0)),('T M8 b',(1400,2000,-700),(1,0,0))]:
    print(nm,p); [print('   ',x) for x in ray(p,d)]
# offset rays for bolt shank radius (check hole present): r=3.5 offsets
print('==== offset')
for nm,p,d,off in [('acici M8 r5.5',(1041,930,-645),(0,-1,0),(5.5,0,0)),('acici M8 r3.6',(1041,930,-645),(0,-1,0),(3.6,0,0)),('tabla M6 r4.2',(880,930,-320),(0,-1,0),(4.2,0,0)),('tabla M6 r3.0',(880,930,-320),(0,-1,0),(3.0,0,0)),('AB r3.8',(761,900,-706),(0,-1,0),(3.8,0,0)),('AB r5.5',(761,900,-706),(0,-1,0),(5.5,0,0)),('T r3.8',(1400,1300,-300),(1,0,0),(0,3.8,0)),('T r5.5',(1400,1300,-300),(1,0,0),(0,5.5,0))]:
    q=np.array(p)+np.array(off); print(nm,q); [print('   ',x) for x in ray(q,d)]
