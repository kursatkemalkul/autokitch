import json,struct,sys,numpy as np,re
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
G={}
for i,nd in enumerate(J['nodes']):
    nm=nd.get('name','')
    if 'mesh' not in nd: continue
    g=nm.split('__')[0]
    t=np.array(nd.get('translation',[0,0,0]))
    for p in J['meshes'][nd['mesh']]['primitives']:
        a=J['accessors'][p['attributes']['POSITION']]
        lo=(np.array(a['min'])+t)*1000; hi=(np.array(a['max'])+t)*1000
        n=J['accessors'][p['indices']]['count']//3
        if g in G: G[g]=[np.minimum(G[g][0],lo),np.maximum(G[g][1],hi),G[g][2]+n]
        else: G[g]=[lo,hi,n]
for g,(lo,hi,n) in G.items(): print('%-28s %8d lo %s hi %s'%(g,n,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist()))
