import json,struct,numpy as np,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl]); BIN=raw[20+jl+8:]
def acc(i):
    a=J['accessors'][i]; v=J['bufferViews'][a['bufferView']]; n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
    off=v.get('byteOffset',0)+a.get('byteOffset',0); r=np.frombuffer(BIN[off:off+a['count']*n*4],np.float32)
    return r.reshape(-1,n) if n>1 else r
names=set()
for ai,an in enumerate(J.get('animations',[])):
    out=[]
    for c in an['channels']:
        nd=J['nodes'][c['target']['node']]; names.add(nd['name'])
        if nd['name']=='TOPPING_DONER__TABLA' and c['target']['path']=='translation':
            s=an['samplers'][c['sampler']]; t=acc(s['input']); x=acc(s['output'])[:,0]*1000
            # plateaus
            i=0; pl=[]
            while i<len(t)-1:
                j=i
                while j+1<len(t) and abs(x[j+1]-x[i])<0.05: j+=1
                if t[j]-t[i]>0.3: pl.append((round(float(x[i]),1),round(float(t[i]),2),round(float(t[j]),2)))
                i=j+1
            print(ai,an.get('name'),'acc',s['output'],'plato:',pl)
print(sorted(n for n in names if 'TOPPING' in n)[:80])
