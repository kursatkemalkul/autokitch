import numpy as np, json
D=np.load('ze/m8_onbellek.npz'); P=D['P']; A,B,C=D['A'],D['B'],D['C']
J=json.load(open('ze/m8_parca.json',encoding='utf-8'))['parca']
for pid in [390,224,228,391,392,393,394,403,404,405,406,395,396]:
    m=P==pid; V=np.concatenate([A[m],B[m],C[m]])
    print(pid, J[pid]['ad'], V.min(0).round(2), V.max(0).round(2), m.sum())
m=P==390; V=np.unique(np.round(np.concatenate([A[m],B[m],C[m]]),2),axis=0)
cs=[(2440.9,972.3),(2440.9,1003.7),(2490.7,1003.7),(2490.7,972.3),(2450.15,963.1),(2450.15,1012.9),(2481.55,963.1),(2481.55,1012.9)]
for cx,cy in cs:
    r=np.hypot(V[:,0]-cx,V[:,1]-cy); k=r<4
    if k.any(): 
        zz=V[k,2]; print((cx,cy),'motor verts r<4: rmin %.2f rmax %.2f z %.1f..%.1f n %d'%(r[k].min(),r[k].max(),zz.min(),zz.max(),k.sum()))
        for zlev in np.unique(np.round(zz,0))[:12]: 
            kk=k&(np.abs(V[:,2]-zlev)<0.6); print('   z',zlev, 'r', np.round(np.unique(np.round(r[kk],2)),2)[:6])
for pid in [391,393]:
    m=P==pid; V2=np.concatenate([A[m],B[m],C[m]]); c=(V2.min(0)+V2.max(0))/2
    r=np.hypot(V2[:,0]-c[0],V2[:,1]-c[1]); print(pid,'pin r',np.unique(np.round(r,2))[:8], 'z levels',np.unique(np.round(V2[:,2],1))[:10])
