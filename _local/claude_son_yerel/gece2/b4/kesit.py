import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
R=pickle.load(open('bil_v9n.pkl','rb'))
def seg_plane(P, n, o):
    n=np.asarray(n,float); d=(P-np.asarray(o,float))@n  # (k,3)
    out=[]
    for t,dd in zip(P,d):
        s=np.sign(np.round(dd,9))
        if np.all(s>0) or np.all(s<0): continue
        pts=[]
        for i in range(3):
            j=(i+1)%3
            if dd[i]==0: pts.append(t[i])
            if dd[i]*dd[j]<0: pts.append(t[i]+(t[j]-t[i])*dd[i]/(dd[i]-dd[j]))
        if len(pts)>=2: out.append(pts[:2])
    return np.array(out)
def kes(d,no,n,o,ax):
    b=[x for x in R[d] if x['no']==no][0]; s=seg_plane(b['P'],n,o)
    if not len(s): print(d,no,'-'); return
    Q=s.reshape(-1,3)[:,ax]; u=np.unique(np.round(Q,2),axis=0)
    print('%s[%d] kesit'%(d,no), len(s),'seg', 'nokta', u.tolist() if len(u)<40 else (np.round(Q.min(0),2).tolist(), np.round(Q.max(0),2).tolist(), len(u)))
if __name__=='__main__':
    import ast
    kes(sys.argv[1], int(sys.argv[2]), ast.literal_eval(sys.argv[3]), ast.literal_eval(sys.argv[4]), ast.literal_eval(sys.argv[5]))
