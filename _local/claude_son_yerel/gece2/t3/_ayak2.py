import pickle, numpy as np, sys
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('t_bil.pkl','rb')); L=B['L']; MEK=B['MEK']
def kod(o): return MEK[o['mek']]['kod'] if o['mek']>=0 else ''
def tri_box(lo_, hi_, ex=lambda o: False):
    hits=[]
    for o in L:
        if ex(o): continue
        if not (np.all(o['hi']>lo_) and np.all(o['lo']<hi_)): continue
        P=o['V'][o['F']]; a=P.min(1); b=P.max(1)
        m=np.all(b>lo_,1)&np.all(a<hi_,1)
        if m.any(): hits.append((o['dug'],kod(o),np.round(o['lo']).astype(int).tolist(),np.round(o['hi']).astype(int).tolist(),int(m.sum())))
    return hits
tabs=[(1466,1302),(1620,1302),(1778,1403),(2173,1403)]
eski = lambda o: o['dug']=='TOPPING_MODUL__sac' and abs(o['lo'][2]+828.5)<0.1 and abs(o['hi'][2]+826)<0.1
for x0,yt in tabs:
    # strap
    lo_=np.array([x0+0.05,1109.05,-828.45]); hi_=np.array([x0+30-0.05,yt-0.05,-826.05])
    print('strap',x0, tri_box(lo_,hi_,eski))
    # foot flange on taban: z -826..-796, y 1109..1111.5
    lo_=np.array([x0+0.05,1109.05,-826.0]); hi_=np.array([x0+30-0.05,1111.5,-796]); print('  flange', tri_box(lo_,hi_,eski))
