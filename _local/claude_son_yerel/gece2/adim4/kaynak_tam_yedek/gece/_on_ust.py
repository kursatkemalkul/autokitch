import sys, numpy as np, glb_oku, bilesen
J,D=glb_oku.yukle(sys.argv[1])
for nd,(X,T) in D.items():
    if len(T)==0 or len(T)>300000: continue
    U=np.unique(T.reshape(-1))
    if X[U,1].max()<1700 or X[U,2].max()<40: continue
    for a,b,n in bilesen.bilesenler(X,T):
        if b[1]>1800 and b[2]>40 and b[0]-a[0]>100 and a[2]>-100:
            print("%-40s x %7.1f %7.1f  y %7.1f %7.1f  z %6.1f %6.1f  %d"%(nd,a[0],b[0],a[1],b[1],a[2],b[2],n))
