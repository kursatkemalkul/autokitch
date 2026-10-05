import json,sys,numpy as np,collections
D=np.load(__import__('os').environ.get('C','zi')+'/m8_onbellek.npz'); PJ=json.load(open(__import__('os').environ.get('C','zi')+'/m8_parca.json',encoding='utf-8')); MEK=[m['kod'] for m in PJ['MEK']]
A,B,C=D['A'],D['B'],D['C']; P=D['P']
lo=np.minimum(np.minimum(A,B),C); hi=np.maximum(np.maximum(A,B),C)
def q(x0,x1,y0,y1,z0,z1,lab=''):
    m=np.all(hi>=[x0,y0,z0],1)&np.all(lo<=[x1,y1,z1],1)
    print('==',lab,[x0,x1,y0,y1,z0,z1],int(m.sum()),'tri')
    c=collections.Counter(P[m])
    for pid,n in c.most_common(40):
        p=PJ['parca'][pid]; print('   %-42s %-22s n%5d kpk%d lo %s hi %s'%(p['ad'],MEK[p['mek']],n,p['kpk'],[round(v) for v in p['lo']],[round(v) for v in p['hi']]))
for a in sys.argv[1:]:
    v=[float(t) for t in a.split(',')[:6]]; q(*v,lab=a.split(',')[6] if len(a.split(','))>6 else '')
