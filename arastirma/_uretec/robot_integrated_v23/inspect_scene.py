"""Read GLB header and node envelopes without tessellating the large machine."""
import gzip,json,struct,sys
from pathlib import Path
import numpy as np
def read(p):
    b=gzip.decompress(Path(p).read_bytes()) if str(p).endswith('.gz') else Path(p).read_bytes()
    n=struct.unpack_from('<I',b,12)[0]
    return json.loads(b[20:20+n]),b[28+n:]
def matrix(n):
    if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
    x,y,z,w=n.get('rotation',[0,0,0,1]);m=np.eye(4)
    m[:3,:3]=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])@np.diag(n.get('scale',[1,1,1]))
    m[:3,3]=n.get('translation',[0,0,0]);return m
def envelopes(g):
    out=[]
    def visit(i,parent):
        n=g['nodes'][i];m=parent@matrix(n);pts=[]
        if 'mesh' in n:
            for p in g['meshes'][n['mesh']]['primitives']:
                a=g['accessors'][p['attributes']['POSITION']]
                if 'min' not in a:continue
                for x in [a['min'][0],a['max'][0]]:
                    for y in [a['min'][1],a['max'][1]]:
                        for z in [a['min'][2],a['max'][2]]:pts.append((m@[x,y,z,1])[:3])
        if pts:out.append({'id':i,'name':n.get('name',''),'box':np.round([np.min(pts,axis=0),np.max(pts,axis=0)],6).tolist(),'extras':n.get('extras',{})})
        for c in n.get('children',[]):visit(c,m)
    for i in g['scenes'][g.get('scene',0)]['nodes']:visit(i,np.eye(4))
    return out
if __name__=='__main__':
    g,_=read(sys.argv[1]);rows=envelopes(g)
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    else:print(json.dumps(rows,ensure_ascii=False))
