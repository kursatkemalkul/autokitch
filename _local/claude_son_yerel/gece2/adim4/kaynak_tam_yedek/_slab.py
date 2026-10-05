import sys, numpy as np, glb_oku
from scipy import ndimage
J,D=glb_oku.yukle("hat3_v8l.glb")
x0,x1,y0,y1,z0,z1=map(float,sys.argv[1:7])
def ornekle(P, ADIM=2.0):
    out=[P.reshape(-1,3)]
    L=np.max(np.linalg.norm(P[:,[1,2,0]]-P,axis=2),axis=1); n=np.maximum(1,np.ceil(L/ADIM)).astype(int)
    for k in np.unique(n):
        W=np.array([(1-a/k-b/k,a/k,b/k) for a in range(k+1) for b in range(k+1-a)])
        out.append(np.einsum("wk,tkd->twd",W,P[n==k]).reshape(-1,3))
    return np.concatenate(out)
for nd in sys.argv[7:]:
    X,T=D[nd]; P=X[T]
    m=(P[:,:,0].max(1)>x0)&(P[:,:,0].min(1)<x1)&(P[:,:,1].max(1)>y0)&(P[:,:,1].min(1)<y1)&(P[:,:,2].max(1)>z0)&(P[:,:,2].min(1)<z1)
    if not m.any(): continue
    Q=ornekle(P[m]); Q=Q[(Q[:,0]>x0)&(Q[:,0]<x1)&(Q[:,1]>y0)&(Q[:,1]<y1)&(Q[:,2]>z0)&(Q[:,2]<z1)]
    if not len(Q): continue
    # 2D grid cluster in x-z
    g=np.zeros((int((x1-x0)/2)+1,int((z1-z0)/2)+1),bool); g[((Q[:,0]-x0)/2).astype(int),((Q[:,2]-z0)/2).astype(int)]=True
    g=ndimage.binary_dilation(g,iterations=2); lab,n=ndimage.label(g)
    print("==",nd)
    for sl in ndimage.find_objects(lab):
        print("   x %7.1f-%7.1f z %7.1f-%7.1f"%(x0+sl[0].start*2,x0+sl[0].stop*2,z0+sl[1].start*2,z0+sl[1].stop*2))
