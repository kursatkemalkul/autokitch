# python proj.py out.png "lo" "hi" regex
import numpy as np, json, sys, re
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
Z=np.load("m8_onbellek.npz"); d=json.load(open("m8_parca.json"))
A,B,C=Z["A"],Z["B"],Z["C"]; P=Z["P"]
lo=np.array(eval(sys.argv[2])); hi=np.array(eval(sys.argv[3])); pat=re.compile(sys.argv[4])
ad=np.array([d["parca"][k]["ad"] for k in range(len(d["parca"]))])
mn=np.minimum(np.minimum(A,B),C); mx=np.maximum(np.maximum(A,B),C)
m=np.all(mx>lo,1)&np.all(mn<hi,1)
ok=np.array([bool(pat.search(a)) for a in ad])
m&=ok[P]
fig,ax=plt.subplots(1,3,figsize=(21,8))
cols={}
for k in np.unique(P[m]):
    mm=m&(P==k); n=ad[k]; c=cols.setdefault(n,"C%d"%(len(cols)%10))
    T=np.stack([A[mm],B[mm],C[mm]],1)
    for a_,(u,w) in zip(ax,((0,1),(0,2),(2,1))):
        for t in T[::1]: a_.fill(t[:,u],t[:,w],color=c,alpha=0.25,lw=0)
for a_,(u,w) in zip(ax,((0,1),(0,2),(2,1))):
    a_.set_xlabel("xyz"[u]);a_.set_ylabel("xyz"[w]);a_.set_aspect("equal");a_.grid(alpha=.3)
for n,c in cols.items(): ax[0].plot([],[],color=c,label=n)
ax[0].legend(fontsize=7)
fig.tight_layout(); fig.savefig(sys.argv[1],dpi=70)
