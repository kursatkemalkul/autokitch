import sys,os,numpy as np,pickle
sys.path.insert(0,'../cekmece'); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
g=G('../../hat3_v9k.glb')
ck=sorted(set(n.get('name','').split('__')[0] for n in g.J['nodes'] if n.get('name','').startswith('CEK_')))
OUT={}
for c in ck:
    L=[]
    for nm in [n.get('name') for n in g.J['nodes'] if n.get('name','').startswith(c+'__')]:
        ni=g.byname[nm]
        for X,T,mek,mat,ex in g.tris(ni):
            cl=bilesen(X,T); Pm=X[T]
            for k in np.unique(cl):
                Q=Pm[cl==k].reshape(-1,3); L.append((nm.split('__',1)[1],Q.min(0),Q.max(0),int((cl==k).sum())))
    OUT[c]=L
pickle.dump(OUT,open('cek_comp.pkl','wb'))
for c in ck:
    L=OUT[c]; 
    ref=[x for x in L if x[0]=='celik' and abs((x[2]-x[1])[0]-8.5)<0.1 and (x[2]-x[1])[2]>500]
    print(c, len(L), 'ray', [np.round(r[1],1).tolist() for r in ref])
