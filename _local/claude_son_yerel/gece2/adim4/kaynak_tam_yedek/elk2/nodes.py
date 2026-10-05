import json,struct,sys,numpy as np,re
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
pat=re.compile(sys.argv[2])
for i,nd in enumerate(J['nodes']):
    nm=nd.get('name','')
    if not pat.search(nm): continue
    s=''
    if 'mesh' in nd:
        pr=J['meshes'][nd['mesh']]['primitives']
        n=sum(J['accessors'][p['indices']]['count']//3 for p in pr)
        a=J['accessors'][pr[0]['attributes']['POSITION']]
        t=np.array(nd.get('translation',[0,0,0]))
        lo=(np.array(a['min'])+t)*1000; hi=(np.array(a['max'])+t)*1000
        mat=J['materials'][pr[0]['material']].get('name') if 'material' in pr[0] else None
        s='tri %7d  lo %s hi %s mat %s rot %s'%(n,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist(),mat,'rotation' in nd)
    print(i,nm,s, 'children',len(nd.get('children',[])))
