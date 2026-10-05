import json,struct,sys
sys.stdout.reconfigure(encoding='utf-8')
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
MEK=J['scenes'][0]['extras']['mekanizmalar']
print('MEK', len(MEK))
for i,m in enumerate(MEK): print(i, json.dumps(m,ensure_ascii=False)[:160])
print('KAT', J['scenes'][0]['extras']['kategoriler'])
for ni,nd in enumerate(J['nodes']):
    if 'mesh' not in nd: continue
    prs=J['meshes'][nd['mesh']]['primitives']
    n=sum(J['accessors'][p['indices']]['count']//3 for p in prs)
    meks=set()
    for p in prs:
        L=p.get('extras',{}).get('mek') or []
        for k in range(0,len(L)-2,3): meks.add(L[k])
    print(ni, nd['name'], n, sorted(meks)[:12])
