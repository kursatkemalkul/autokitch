import sys, numpy as np, glb_oku, bilesen
J,D=glb_oku.yukle(sys.argv[1])
y0,y1,zmin=float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
for nd,(X,T) in D.items():
    if len(T)==0 or len(T)>300000: continue
    U=np.unique(T.reshape(-1))
    if X[U,1].min()>y1 or X[U,2].max()<zmin: continue
    for a,b,n in bilesen.bilesenler(X,T):
        if a[1]<y1 and b[1]>y0 and b[2]>zmin and b[0]-a[0]>150:
            print("%-34s x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %d"%(nd,a[0],b[0],a[1],b[1],a[2],b[2],n))
