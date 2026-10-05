import json,struct,sys,re
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
pat=re.compile(sys.argv[2])
par={}
for i,n in enumerate(J['nodes']):
    for c in n.get('children',[]): par[c]=i
print('scene roots',J['scenes'][0]['nodes'][:10], 'scene extras keys', list(J['scenes'][0].get('extras',{}).keys()))
for i,n in enumerate(J['nodes']):
    nm=n.get('name','')
    if not pat.search(nm): continue
    s=''
    if 'mesh' in n:
        prs=J['meshes'][n['mesh']]['primitives']
        for pr in prs:
            ex=pr.get('extras',{}); m=J['materials'][pr['material']]
            cnt=J['accessors'][pr['indices']]['count']//3
            s+=' | mat=%s tri=%d kat=%s mek=%s kpk=%s'%(m.get('name'),cnt,ex.get('kat',[])[:6],ex.get('mek',[])[:6],ex.get('kpk',[])[:4])
    print(i,nm,'parent',par.get(i),{k:v for k,v in n.items() if k in('translation','rotation','scale','extras')},s)
