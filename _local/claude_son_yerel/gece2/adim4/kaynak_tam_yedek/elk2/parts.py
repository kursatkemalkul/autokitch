import json,sys,re,numpy as np
PJ=json.load(open('zi/m8_parca.json',encoding='utf-8')); MEK=[m['kod'] for m in PJ['MEK']]
pat=re.compile(sys.argv[1])
for p in PJ['parca']:
    if pat.search(p['ad']): print('%-40s %-20s kpk%d n%6d lo %s hi %s'%(p['ad'],MEK[p['mek']],p['kpk'],p['n'],[round(v,1) for v in p['lo']],[round(v,1) for v in p['hi']]))
