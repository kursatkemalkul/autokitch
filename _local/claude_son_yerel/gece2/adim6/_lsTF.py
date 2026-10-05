import sys,glbio,re,collections
sys.stdout.reconfigure(encoding='utf-8')
for ist in ('TOPPING','F'):
    J,P=glbio.oku(r'../adim5/%s_sac_v1.glb'%ist)
    print('=====',ist,len(P))
    c=collections.Counter()
    for a,p in P.items():
        tur=p['extras'].get('tur') or p['mat']
        k=re.sub(r'_?\d+(_-?\d+)*$','#',a); c[(tur,k)]+=1
    for (tur,k),n in sorted(c.items()): print(tur,k,n)
