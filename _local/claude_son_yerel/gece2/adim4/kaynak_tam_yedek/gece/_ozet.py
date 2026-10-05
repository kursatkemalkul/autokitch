import sys, numpy as np, glb_oku, json
J,D=glb_oku.yukle(sys.argv[1])
print(json.dumps({k:(v if not isinstance(v,(list,dict)) or len(json.dumps(v))<300 else str(v)[:300]) for k,v in J.get('scenes',[{}])[0].get('extras',{}).items()},ensure_ascii=False)[:3000])
for k,(X,T) in D.items():
    U=np.unique(T.reshape(-1)) if len(T) else []
    if len(U)==0: print("%-34s BOS"%k); continue
    a=X[U].min(0);b=X[U].max(0)
    print("%-34s %7d  x %7.0f %7.0f y %6.0f %6.0f z %6.0f %6.0f"%(k,len(T),a[0],b[0],a[1],b[1],a[2],b[2]))
