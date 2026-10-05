import sys, numpy as np, glb_oku, bilesen
J,D=glb_oku.yukle("hat3_v8u.glb")
x0,x1,y0,y1,z0,z1=map(float,sys.argv[1:7])
for nd in sys.argv[7:]:
    X,T=D[nd]; P=X[T]; c=P.mean(1)
    m=(c[:,0]>x0)&(c[:,0]<x1)&(c[:,1]>y0)&(c[:,1]<y1)&(c[:,2]>z0)&(c[:,2]<z1)
    if not m.any(): continue
    B=bilesen.bilesenler(X,T[m])
    print("==",nd,len(B))
    for a,b,n in sorted(B,key=lambda t:tuple(t[0])):
        print("  x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %d"%(a[0],b[0],a[1],b[1],a[2],b[2],n))
