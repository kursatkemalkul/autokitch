import glb_oku, numpy as np
J, D = glb_oku.yukle("hat3_v8l.glb")
for nd,(X,T) in D.items():
    if nd.startswith(("B_KASA","B_MODULER","CEK_")) or not len(T): continue
    P = X[T].reshape(-1,3)
    m = (P[:,0]>730)&(P[:,0]<4410)&(P[:,1]<800)&(P[:,2]>-840)&(P[:,2]<90)
    if m.any():
        Q=P[m]; print("%-40s %6d  x %7.1f %7.1f y %6.1f %6.1f z %7.1f %7.1f"%(nd,m.sum()//1,*Q.min(0)[[0]],Q.max(0)[0],Q.min(0)[1],Q.max(0)[1],Q.min(0)[2],Q.max(0)[2]))
