import json,struct,sys,numpy as np,re
from vox import S
raw=open(S+r"\hat3_v8zk.glb",'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
bo=20+jl; BIN=raw[bo+8:]
def acc(i):
    a=J['accessors'][i]; v=J['bufferViews'][a['bufferView']]; n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
    off=v.get('byteOffset',0)+a.get('byteOffset',0); return np.frombuffer(BIN[off:off+a['count']*n*4],np.float32).reshape(-1,n)
pat=re.compile(sys.argv[1]); seen={}
for a in J['animations']:
    for c in a['channels']:
        nd=J['nodes'][c['target']['node']]; nm=nd['name']
        if not pat.search(nm) or c['target']['path']!='translation': continue
        o=acc(a['samplers'][c['sampler']]['output'])*1000; t0=np.array(nd.get('translation',[0,0,0]))*1000
        d=o-t0; k=nm
        lo,hi=d.min(0),d.max(0)
        if k in seen: lo=np.minimum(lo,seen[k][0]); hi=np.maximum(hi,seen[k][1])
        seen[k]=(lo,hi)
for k,(lo,hi) in seen.items(): print(k,np.round(lo).tolist(),np.round(hi).tolist())
