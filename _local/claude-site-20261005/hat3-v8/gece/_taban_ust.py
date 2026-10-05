import sys, numpy as np, glb_oku, bilesen
J,D=glb_oku.yukle(sys.argv[1])
for nd,(X,T) in D.items():
    if len(T)==0: continue
    U=np.unique(T.reshape(-1)); 
    if X[U,0].max()<4000 or X[U,0].min()>4400: continue
    B=bilesen.bilesenler(X,T)
    for a,b,n in B:
        if 4000<=a[0] and b[0]<=4400.5 and 889<=a[1]<=900 and a[2]>-831:
            print("%-30s x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %d"%(nd,a[0],b[0],a[1],b[1],a[2],b[2],n))
