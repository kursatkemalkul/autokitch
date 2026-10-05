# her E_ bileşeni (E_GOVDE hariç isteğe bağlı) için en yakın başka bileşen (aynı hareket grubu ya da sabit) mesafesi
import sys, numpy as np, re
sys.path.insert(0,"."); import govde_denetim_dogru as GD
D=GD.glb_oku(sys.argv[1]); pat=re.compile(sys.argv[2] if len(sys.argv)>2 else "^E_")
HAR=("ITICI","VAC_Y","NEST","PISTON","KOPRU","KATLAYICI","CNR_LIFT","FRONT_Y","KOL","PARMAK","CNR_MF","CNR_MB","CNR_PF","CNR_PB","ASANSOR","PIZZA")
def grup(nd):
    s=nd.split("__")[-1]
    return s if s in HAR else "SABIT"
TUM=[]
lo0=np.array([4300,-20,-900.]); hi0=np.array([5400,2300,200.])
for nd,P in D.items():
    if not len(P): continue
    Q=P.reshape(-1,3)
    if (Q.min(0)>hi0).any() or (Q.max(0)<lo0).any(): continue
    TUM+=GD.bilesenler(nd,P)
LO=np.array([b.lo for b in TUM]); HI=np.array([b.hi for b in TUM])
for A in TUM:
    if not pat.search(A.dugum) or A.dugum.startswith("E_KUTU") or "karton" in A.dugum or "PIZZA" in A.dugum: continue
    gA=grup(A.dugum)
    m=((LO<=A.hi+5)&(HI>=A.lo-5)).all(1)
    en=99.0; ead=None
    for j in np.where(m)[0]:
        B=TUM[j]
        if B is A: continue
        gB=grup(B.dugum)
        if gA!="SABIT" and gB!=gA: continue
        if gA=="SABIT" and gB!="SABIT": continue
        ma,mb=A.mf(),B.mf()
        if ma and mb: g=float(ma.min_gap(mb,5.0))
        else:
            # bbox gap
            d=np.maximum(0,np.maximum(A.lo-B.hi,B.lo-A.hi)); g=float(np.linalg.norm(d))
        if g<en: en,ead=g,B
    if en>0.05:
        print("HAVADA %-32s[%3d] %-5s lo %s hi %s · en yakın %.2f %s" % (A.dugum,A.no,gA,A.lo.round(1).tolist(),A.hi.round(1).tolist(),en,(ead.dugum+"[%d]"%ead.no) if ead else "-"))
import os; sys.stdout.flush(); os._exit(0)
