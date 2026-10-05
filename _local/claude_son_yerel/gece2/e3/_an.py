import sys, pickle, numpy as np, re, collections
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('e3_parca_ham.pkl','rb')); P=D['P']
LO={a:P[a]['V'].min(0) for a in P}; HI={a:P[a]['V'].max(0) for a in P}
YAPI=[a for a in P if P[a]['tur'] in ('sac','profil')]
def host(q):
    c=[a for a in YAPI if np.all(LO[a]<=q+0.3) and np.all(HI[a]>=q-0.3)]
    return sorted(c,key=lambda a: np.prod(HI[a]-LO[a]+0.5))
def eks(a):
    V=P[a]['V']; ext=HI[a]-LO[a]; ax=int(np.argmax(ext)); oth=[k for k in range(3) if k!=ax]; s=V[:,ax]
    ml=s<s.min()+0.6; mh=s>s.max()-0.6
    e=np.zeros(3); e[ax]=1.0 if np.ptp(V[ml][:,oth],0).max()>np.ptp(V[mh][:,oth],0).max() else -1.0
    b=(LO[a]+HI[a])/2; b[ax]=s.min() if e[ax]>0 else s.max(); return e,b,ext[ax]
for a in sorted(P):
    et=P[a].get('etur')
    if et in('saplama','civata','pem','kaynak_somunu') and not a.startswith('g_arayuz_mek'):
        e,b,L=eks(a); print('%-44s %-8s e %-12s L %5.1f bas %s host %s'%(a[2:],et,e.astype(int).tolist(),L,np.round(b,1).tolist(),host(b)[:2]))
