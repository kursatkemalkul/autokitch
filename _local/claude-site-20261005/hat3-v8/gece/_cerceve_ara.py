import sys, numpy as np, glb_oku, bilesen
J,D=glb_oku.yukle(sys.argv[1])
for nd,(X,T) in D.items():
    if len(T)==0 or len(T)>200000: continue
    for a,b,n in bilesen.bilesenler(X,T):
        d=b-a
        if d[0]<15 and d[1]>50 and d[2]>200 and n<400 and 700<a[1]<1400:
            print("%-34s x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %d"%(nd,a[0],b[0],a[1],b[1],a[2],b[2],n))
