import json,struct,numpy as np
CT={5120:np.int8,5121:np.uint8,5122:np.int16,5123:np.uint16,5125:np.uint32,5126:np.float32}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def oku(yol):
    f=open(yol,'rb').read()
    L=struct.unpack('<I',f[12:16])[0]; J=json.loads(f[20:20+L])
    o=20+L; L2=struct.unpack('<I',f[o:o+4])[0]; B=f[o+8:o+8+L2]
    def acc(i):
        a=J['accessors'][i]; bv=J['bufferViews'][a['bufferView']]
        off=bv.get('byteOffset',0)+a.get('byteOffset',0); dt=CT[a['componentType']]; n=NC[a['type']]
        arr=np.frombuffer(B,dtype=dt,count=a['count']*n,offset=off)
        return arr.reshape(a['count'],n) if n>1 else arr
    parca={}
    for nd in J['nodes']:
        if 'mesh' not in nd: continue
        m=J['meshes'][nd['mesh']]; P=[];I=[];base=0;mats=[]
        for pr in m['primitives']:
            p=acc(pr['attributes']['POSITION']).astype(np.float64); idx=acc(pr['indices']).astype(np.int64)
            P.append(p); I.append(idx+base); base+=len(p); mats.append(J['materials'][pr['material']]['name'] if 'material' in pr else None)
        M=np.eye(4)
        if 'matrix' in nd: M=np.array(nd['matrix']).reshape(4,4).T
        if 'translation' in nd: M[:3,3]=nd['translation']
        assert 'rotation' not in nd and 'scale' not in nd
        V=np.vstack(P); V=(M[:3,:3]@V.T).T+M[:3,3]
        parca[nd['name']]=dict(V=V,F=np.concatenate(I).reshape(-1,3),mat=mats[0],extras=nd.get('extras',{}))
    return J,parca

def yaz(yol, dugumler, malzemeler):
    """dugumler: [dict(ad, V(float32 n×3), F(uint32), mat index, extras, attrs{name:arr})] → GLB, düğüm dönüşümsüz"""
    J={'asset':{'version':'2.0','generator':'k_montaj_v1'},'scene':0,'scenes':[{'nodes':list(range(len(dugumler)))}],
       'nodes':[],'meshes':[],'accessors':[],'bufferViews':[],'buffers':[],'materials':malzemeler}
    buf=bytearray()
    def ekle(arr,typ,ct,target=None,minmax=False):
        arr=np.ascontiguousarray(arr)
        while len(buf)%4: buf.append(0)
        off=len(buf); buf.extend(arr.tobytes())
        bv={'buffer':0,'byteOffset':off,'byteLength':arr.nbytes}
        if target: bv['target']=target
        J['bufferViews'].append(bv)
        a={'bufferView':len(J['bufferViews'])-1,'componentType':ct,'count':int(arr.shape[0]),'type':typ}
        if minmax: a['min']=arr.min(0).tolist(); a['max']=arr.max(0).tolist()
        J['accessors'].append(a); return len(J['accessors'])-1
    for i,d in enumerate(dugumler):
        V=d['V'].astype(np.float32); F=d['F'].astype(np.uint32).reshape(-1)
        at={'POSITION':ekle(V,'VEC3',5126,34962,True)}
        for k,v in d.get('attrs',{}).items():
            v=np.asarray(v,np.float32); at[k]=ekle(v,'VEC3' if v.ndim==2 and v.shape[1]==3 else 'SCALAR',5126,34962)
        ii=ekle(F,'SCALAR',5125,34963)
        J['meshes'].append({'name':d['ad'],'primitives':[{'attributes':at,'indices':ii,'material':d['mat']}]})
        nd={'name':d['ad'],'mesh':i}
        if d.get('extras'): nd['extras']=d['extras']
        J['nodes'].append(nd)
    while len(buf)%4: buf.append(0)
    J['buffers'].append({'byteLength':len(buf)})
    js=json.dumps(J,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    while len(js)%4: js+=b' '
    out=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(buf))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(buf),0x004E4942)+bytes(buf)
    open(yol,'wb').write(out); return len(out)
