import sys, numpy as np, pickle
sys.path.insert(0, r"@@KOK_F@@/tg")
from glbx import yukle
J,D=yukle("hat3_v8p.glb")
R=pickle.load(open("eg/seg_v8p.pkl","rb"))
X0=4400
bands={
 "solsac_arka_donus": (X0+1.5,X0+16.5,126,1860.5,-828.5,-827.0),
 "sagsac_arka_donus": (X0+813.5,X0+828.5,126,1860.5,-828.5,-827.0),
 "tavan_sol_buk": (X0+1.5,X0+3.0,1840.5,1860.5,-828.5,59),
 "tavan_sag_buk": (X0+827,X0+828.5,1840.5,1860.5,-828.5,59),
 "tavan_arka_buk": (X0+1.5,X0+828.5,1840.5,1860.5,-828.5,-827.0),
 "sol_dikme_tam": (X0+1.5,X0+21.5,126,1860.5,29,59),
 "orta_dikme_40": (X0+441.5,X0+481.5,126,1860.5,29,59),
 "sag_dikme": (X0+808.5,X0+828.5,126,1860.5,29,59),
 "kayit788": (X0+21.5,X0+808.5,773,803,29,59),
 "taban_on_uzat": (X0+1.5,X0+828.5,123,126,57.5,59),
 "arka_kose_dikme_sol": (X0+1.5,X0+31.5,126,1860.5,-828.5,-798.5),
 "arka_kose_dikme_sag": (X0+798.5,X0+828.5,126,1860.5,-828.5,-798.5),
}
SKIP=("E_GOVDE__",)
for bn,b in bands.items():
    lo=np.array(b[0::2])+0.05; hi=np.array(b[1::2])-0.05
    hits={}
    for nd,d in D.items():
        if nd.startswith(SKIP): continue
        P=d["X"][d["T"][d["ok"]]]
        if not len(P): continue
        m=((P.max(1)>lo)&(P.min(1)<hi)).all(1)
        if m.any():
            Q=P[m].reshape(-1,3)
            lab = R.get(nd)
            names=set(lab[d["ok"]][m]) if lab is not None else {""}
            hits[nd]=(m.sum(), sorted(names)[:4], Q.min(0).round(1).tolist(), Q.max(0).round(1).tolist())
    print("==",bn)
    for k,v in hits.items(): print("   ",k,v)
