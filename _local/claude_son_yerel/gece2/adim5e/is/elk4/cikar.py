# -*- coding: utf-8 -*-
"""elk4 1: v8zk istasyon iç kabloları -> bileşen, doğru parçalar, kanal içi/dışı uzunluk. SALT OKUMA."""
import sys, pickle, re, numpy as np
S=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5e\is"
sys.path.insert(0,S+r"\gece"); sys.path.insert(0,S); sys.path.insert(0,S+r"\gece\m8\kablo_is")
import m8kit, serit
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
G=m8kit.Glb(sys.argv[1] if len(sys.argv)>1 else S+r"\hat3_v8zk.glb")
KABLO=re.compile(r"^(ELK_TOPPING|ELK_K|ELK_DOLAP|ELK_ISTASYON|ELK_K_TARTI|ELK_QR_KABLO|ELK_E|ELK_U)__(kablo|kablo_sinyal|kablo_veri)$|^(K_ELEKTRIK__hava|TOPPING_MODUL__hava_ana)$")
def comps(P):
    Pq=np.round(P.reshape(-1,3),2); u,inv=np.unique(Pq,axis=0,return_inverse=True); Ti=inv.reshape(-1,3)
    r_=np.r_[Ti[:,0],Ti[:,1]]; c_=np.r_[Ti[:,1],Ti[:,2]]
    k,lab=connected_components(coo_matrix((np.ones(len(r_)),(r_,c_)),shape=(len(u),len(u))),directed=False)
    return lab[Ti[:,0]]
# kanal grupları
KAN=[]
for p in G.prims:
    if p.get("gizli") or not re.search(r"__kanal$",p["name"]): continue
    vis=G.gorunur(p); P=p["X"][p["T"][vis]]
    if not len(P): continue
    tl=comps(P)
    B=[(P[tl==c].reshape(-1,3).min(0),P[tl==c].reshape(-1,3).max(0)) for c in np.unique(tl)]
    # birleşik: dokunan kutular
    par=list(range(len(B)))
    def f(i):
        while par[i]!=i: par[i]=par[par[i]]; i=par[i]
        return i
    for i in range(len(B)):
        for j in range(i+1,len(B)):
            if np.all(B[i][0]<=B[j][1]+0.3) and np.all(B[j][0]<=B[i][1]+0.3): par[f(i)]=f(j)
    gg={}
    for i in range(len(B)): gg.setdefault(f(i),[]).append(i)
    for g in gg.values():
        lo=np.min([B[i][0] for i in g],0); hi=np.max([B[i][1] for i in g],0)
        KAN.append((p["name"],lo,hi))
print("kanal grubu",len(KAN))
def ic(pt,e=0.5):
    for _,lo,hi in KAN:
        if np.all(pt>=lo-e) and np.all(pt<=hi+e): return True
    return False
KAY=[]
for pi,p in enumerate(G.prims):
    if p.get("gizli") or not KABLO.match(p["name"]): continue
    vis=G.gorunur(p); idx=np.where(vis)[0]; P=p["X"][p["T"][idx]]
    tl=comps(P)
    for c in np.unique(tl):
        m=tl==c; Q=P[m]
        Sg=serit.segmentler(Q); Sg=[q for q in Sg if np.linalg.norm(q['b']-q['a'])>0.8*q['r']]
        Lt=0; Lo=0
        for q in Sg:
            L=np.linalg.norm(q['b']-q['a']); n=max(2,int(L/5)); Lt+=L
            ts=np.linspace(0,1,n); pts=q['a'][None]+ts[:,None]*(q['b']-q['a'])[None]
            q['ic']=np.array([ic(x) for x in pts]); Lo+=L*(1-q['ic'].mean())
        lo=Q.reshape(-1,3).min(0); hi=Q.reshape(-1,3).max(0)
        KAY.append(dict(prim=p["name"],pi=pi,tri=idx[m],S=Sg,L=Lt,Lacik=Lo,lo=lo,hi=hi,r=np.median([q['r'] for q in Sg]) if Sg else 0))
def ist(d):
    c=(d['lo']+d['hi'])/2; x,y,z=c
    if 'QR' in d['prim']: return 'QR'
    if 'DOLAP' in d['prim'] or y<788: return 'B'
    if y>1862 and 2500<x<4000: return 'U'
    if x<1436: return 'A'
    if x<2500: return 'TOPPING'
    if x<4000: return 'F'
    if x<4400: return 'K'
    return 'E'
for d in KAY: d['ist']=ist(d)
pickle.dump(dict(KAY=KAY,KAN=KAN),open(S+r"\elk4\kay0.pkl","wb"))
import collections
s=collections.defaultdict(lambda:[0,0,0,0])
for d in KAY:
    a=s[d['ist']]; a[0]+=1; a[1]+=d['L']; a[2]+=d['Lacik']; a[3]+=d['Lacik']>150
for k,v in s.items(): print("%-8s bileşen %4d  toplam %7.0f  açık %7.0f  açık>150 bileşen %d"%(k,v[0],v[1],v[2],v[3]))
