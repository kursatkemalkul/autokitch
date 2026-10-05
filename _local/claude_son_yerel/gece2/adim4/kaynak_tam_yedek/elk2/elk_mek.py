import json,collections,numpy as np
PJ=json.load(open('zi/m8_parca.json',encoding='utf-8')); MEK=[m['kod'] for m in PJ['MEK']]
E=[i for i,k in enumerate(MEK) if k.endswith('/Elektrik') or k.startswith('Elektrik/') or k=='Çevre/Dükkân hattı']
d=collections.defaultdict(lambda:[0,0,np.full(3,1e9),np.full(3,-1e9)])
for p in PJ['parca']:
    if p['mek'] in E:
        k=(MEK[p['mek']],p['ad']); v=d[k]; v[0]+=1; v[1]+=p['n']; v[2]=np.minimum(v[2],p['lo']); v[3]=np.maximum(v[3],p['hi'])
for k in sorted(d): v=d[k]; print('%-22s %-45s parca %4d tri %7d lo %s hi %s'%(k[0],k[1],v[0],v[1],np.round(v[2]).astype(int).tolist(),np.round(v[3]).astype(int).tolist()))
