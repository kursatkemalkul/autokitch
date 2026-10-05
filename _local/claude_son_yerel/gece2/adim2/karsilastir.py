import json,re,sys,numpy as np
def yukle(f):
    d=json.load(open(f))['D']; return d['cakisma']
B=yukle(sys.argv[1]); N=yukle(sys.argv[2])
def ad(s): return re.sub(r"\[\d+\]$","",s)
def geri(c):
    p=np.array(c['bilgi']['nokta'],float); a=ad(c['parca']);b=ad(c['komsu'])
    if any(x.startswith(("TEZGAH_","DUZ_TEZGAH")) for x in (a,b)): p[0]=7727-p[0]; p[2]=2918-p[2]
    elif any(x.startswith(("QR_","ELK_QR_")) for x in (a,b)) or (4360<=p[0]<=5240 and 660<=p[2]<=1200): p[0]+=200
    return p
Bk=[(frozenset((ad(c['parca']),ad(c['komsu']))),np.array(c['bilgi']['nokta'])) for c in B]
yeni=[];sahte=0
for c in N:
    k=frozenset((ad(c['parca']),ad(c['komsu']))); p=geri(c)
    if any(k==kb and np.linalg.norm(p-pb)<4 for kb,pb in Bk): continue
    if c.get('occ_derinlik') and max(c['occ_derinlik'])<0.05: sahte+=1; continue
    yeni.append(c)
print("son",len(N),"taban",len(B),"| tabanda olmayan gercek:",len(yeni),"| OCC 0 sahte:",sahte)
for c in yeni: print("  YENI",c['parca'],"<->",c['komsu'],c['derinlik'],c['bilgi']['nokta'],c.get('occ_derinlik'))
