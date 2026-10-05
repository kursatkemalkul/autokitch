import sys, json, numpy as np
d=sys.argv[1]; K=[float(v) for v in sys.argv[2:8]]; filt=sys.argv[8] if len(sys.argv)>8 else ''
J=json.load(open(d+'/m8_parca.json',encoding='utf-8')); PJ=J['parca']; MEK=[m['kod'] for m in J['MEK']]; KAT=J['KAT']
for i,p in enumerate(PJ):
    lo,hi=p['lo'],p['hi']
    if hi[0]<K[0] or lo[0]>K[1] or hi[1]<K[2] or lo[1]>K[3] or hi[2]<K[4] or lo[2]>K[5]: continue
    s="%5d %-30s %-20s %-9s %s %6d %s %s"%(i,p['ad'][:30],MEK[p['mek']][:20] if p['mek']>=0 else '-',KAT[p['kat']] if p['kat']>=0 else '-','K' if p['kpk'] else ' ',p['n'],[round(v,1) for v in lo],[round(v,1) for v in hi])
    if filt in s: print(s)
