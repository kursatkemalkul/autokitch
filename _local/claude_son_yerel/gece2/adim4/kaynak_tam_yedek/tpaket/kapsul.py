import json, numpy as np, sys
def segseg(p1,q1,p2,q2):
    d1=q1-p1; d2=q2-p2; r=p1-p2; a=d1@d1; e=d2@d2; f=d2@r
    if a<1e-12 and e<1e-12: return np.linalg.norm(r)
    if a<1e-12: s=0; t=np.clip(f/e,0,1)
    else:
        c=d1@r
        if e<1e-12: t=0; s=np.clip(-c/a,0,1)
        else:
            b=d1@d2; den=a*e-b*b
            s=np.clip((b*f-c*e)/den,0,1) if den>1e-12 else 0
            t=(b*s+f)/e
            if t<0: t=0; s=np.clip(-c/a,0,1)
            elif t>1: t=1; s=np.clip((b-c)/a,0,1)
    return np.linalg.norm(p1+d1*s-(p2+d2*t))
def kesis(Y, K=(2400,2480,700,1330,-900,0), pay=0.0):
    out=[]; ks=list(Y)
    def seg(k):
        P=np.array(Y[k]['P'],float); S=[]
        for a,b in zip(P[:-1],P[1:]):
            lo=np.minimum(a,b); hi=np.maximum(a,b)
            if hi[0]<K[0] or lo[0]>K[1] or hi[1]<K[2] or lo[1]>K[3]: continue
            S.append((a,b))
        return S
    SS={k:seg(k) for k in ks}
    for i,k1 in enumerate(ks):
        for k2 in ks[i+1:]:
            r=Y[k1]['r']+Y[k2]['r']+pay; dm=1e9; w=None
            for a,b in SS[k1]:
                for c,d in SS[k2]:
                    dd=segseg(a,b,c,d)
                    if dd<dm: dm=dd; w=(a,b,c,d)
            if dm<r: out.append((k1,k2,round(dm-r,2),np.round((w[0]+w[1])/2,1).tolist()))
    return out
if __name__=='__main__':
    Y=json.load(open(sys.argv[1],encoding='utf-8'))
    Y={k:v for k,v in Y.items() if 'ROBOT' not in k}
    for o in kesis(Y): print(o)
