import sys, os, json, pickle, numpy as np, collections
sys.stdout.reconfigure(encoding='utf-8')
B = pickle.load(open('e_bil.pkl','rb'))['E']
ENT = json.load(open('../adim8/is_tam/hat3_v9c_ent.json', encoding='utf-8'))['parca']
GD = sorted(set(v['dugum'] for v in ENT.values()))
def kut(k): return np.array(k[0::2], float), np.array(k[1::2], float)
for dug in GD:
    C = [o for o in B if o['dug'] == dug]; E = {a: kut(v['kutu']) for a, v in ENT.items() if v['dugum'] == dug}
    kul=set(); A={}
    for a,(lo,hi) in E.items():
        c=[i for i,b in enumerate(C) if i not in kul and np.all(np.abs(b['lo']-lo)<0.35) and np.all(np.abs(b['hi']-hi)<0.35)]
        if len(c)==1: kul.add(c[0]); A[a]=c[0]
    n1=len(A)
    for a,(lo,hi) in E.items():
        if a in A: continue
        c=[i for i,b in enumerate(C) if i not in kul and np.all(b['lo']<=lo+0.35) and np.all(b['hi']>=hi-0.35)]
        if c: i=min(c,key=lambda i: np.prod(C[i]['hi']-C[i]['lo']+0.1)); kul.add(i); A[a]=i
    n2=len(A)
    print(dug, 'ent',len(E),'bil',len(C),'birebir',n1,'kapsayan',n2-n1,'eşleşmeyen ent',[a for a in E if a not in A][:12],'kalan bil',[(np.round(C[i]['lo']),np.round(C[i]['hi'])) for i in range(len(C)) if i not in kul][:6])
    # kapsayan: hangi ent'ler aynı bileşene düştü?
