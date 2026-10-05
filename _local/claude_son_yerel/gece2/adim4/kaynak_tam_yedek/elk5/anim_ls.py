import json,struct,numpy as np,re,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl]); BIN=raw[28+jl:]
def acc(i):
    a=J['accessors'][i]; v=J['bufferViews'][a['bufferView']]; n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
    off=v.get('byteOffset',0)+a.get('byteOffset',0); return np.frombuffer(BIN[off:off+a['count']*n*4],np.float32).reshape(-1,n)
pat=sys.argv[2]
for an in J['animations']:
    for c in an['channels']:
        nd=J['nodes'][c['target']['node']]
        if not re.search(pat,nd['name']): continue
        o=acc(an['samplers'][c['sampler']]['output'])
        print(an.get('name'),nd['name'],c['target']['path'],'t',nd.get('translation'),'r',nd.get('rotation'),'min',np.round(o.min(0),4).tolist(),'max',np.round(o.max(0),4).tolist())
