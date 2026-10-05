import sys, os, pickle, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
P=pickle.load(open('a3_parca.pkl','rb'))['P']
K=[a for a in P if P[a].get('kpk')]
S=[a for a in P if not P[a].get('kpk') and not a.startswith('cevre_T')]
print(len(K),len(S))
T={a:P[a]['V'][P[a]['F']]/1000 for a in P}
px,pz=0.736,0.079
for th in [-2,-5,-10,-20,-30,-45,-60,-75,-90,-120,-150,-180]:
    r=np.radians(th); cs,sn=np.cos(r),np.sin(r); bad=[]
    for a in K:
        A=T[a].copy(); dx=A[...,0]-px; dz=A[...,2]-pz; A[...,0]=px+cs*dx+sn*dz; A[...,2]=pz-sn*dx+cs*dz
        lo=A.reshape(-1,3).min(0); hi=A.reshape(-1,3).max(0)
        for b in S:
            B=T[b]; 
            if np.any(B.reshape(-1,3).min(0)>hi) or np.any(B.reshape(-1,3).max(0)<lo): continue
            c=Y.poz_kesisim(np.ascontiguousarray(A),np.ascontiguousarray(B),3e-4).sum()
            if c: bad.append((a,b,int(c)))
    print(th,bad[:6],len(bad))
