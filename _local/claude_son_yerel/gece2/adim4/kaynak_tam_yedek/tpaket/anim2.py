import json,struct,numpy as np,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl]); BIN=raw[20+jl+8:]
def acc(i):
    a=J['accessors'][i]; v=J['bufferViews'][a['bufferView']]; n={'SCALAR':1,'VEC3':3,'VEC4':4}[a['type']]
    off=v.get('byteOffset',0)+a.get('byteOffset',0); r=np.frombuffer(BIN[off:off+a['count']*n*4],np.float32)
    return r.reshape(-1,n) if n>1 else r
an=J['animations'][int(sys.argv[2])]
for c in an['channels']:
    nd=J['nodes'][c['target']['node']]; s=an['samplers'][c['sampler']]
    t=acc(s['input'])
    if nd['name']=='TOPPING_DONER__TABLA' and c['target']['path']=='translation':
        x=acc(s['output'])[:,0]*1000
        print('TABLA x:', ' '.join('%.2f:%.1f'%(a,b) for a,b in zip(t,x)))
    elif nd['name']=='TOPPING_DONER__TABLA':
        q=acc(s['output']); ang=np.degrees(2*np.arctan2(q[:,1],q[:,3]))
        print('TABLA rot active t:', '%.2f-%.2f'%(t[0],t[-1]), 'n',len(t))
        d=np.abs(np.diff(ang))>1e-3; 
        # find rotating intervals
        iv=[];i=0
        while i<len(d):
            if d[i]:
                j=i
                while j<len(d) and d[j]: j+=1
                iv.append((round(float(t[i]),2),round(float(t[j]),2))); i=j
            else: i+=1
        print('  rot intervals',iv)
    else:
        if c['target']['path'] in ('rotation','translation'):
            o=acc(s['output']); 
            print(nd['name'],c['target']['path'],'t %.2f-%.2f'%(t[0],t[-1]),'n',len(t))
