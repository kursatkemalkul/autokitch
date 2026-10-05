import sys,os,pickle,numpy as np
S=r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
sys.path.insert(0,S); import govde_denetim_dogru as G
D=pickle.load(open(S+r"\gece2\adim8\_v9f_ucgen.pkl","rb"))
P=np.concatenate([d[3] for d in D if d[0]==sys.argv[1]])
B=G.bilesenler(sys.argv[1],P)
q=[float(v) for v in sys.argv[2].split(",")]
for b in B:
    if b.lo[0]<q[1] and b.hi[0]>q[0] and b.lo[1]<q[3] and b.hi[1]>q[2] and b.lo[2]<q[5] and b.hi[2]>q[4]:
        X=b.P.reshape(-1,3)
        print(b.no, b.lo.round(2), b.hi.round(2), len(b.P), 'kapali',b.kapali)
        if len(sys.argv)>3:
            print('  y:',np.unique(X[:,1].round(2))[:30]); print('  z:',np.unique(X[:,2].round(2))[:30]); print('  x:',np.unique(X[:,0].round(1))[:40])
