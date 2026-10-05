import sys;sys.path.insert(0,'..');sys.path.insert(0,'.')
import glbkit,numpy as np,time
t=time.time();G=glbkit.Glb('../hat3_v8x.glb');print('yuk',time.time()-t)
LIN=('kablo','kablo_veri','hava_ana','hava','bakir','hortum_gida','hortum_yag','hortum_orgu','zincir')
tot=0
for p in G.prims:
    v=G.gorunur(p).sum();tot+=v
    mat=p['name'].split('__')[1] if '__' in p['name'] else ''
    if mat in LIN:
        tl,k=G.komp(p);print(p['name'],v,len(k))
print('toplam',tot)
