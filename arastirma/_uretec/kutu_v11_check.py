import json,sys,hashlib
from pathlib import Path
import kutu_cad_v11 as K
K.modul()
P={p['ad']:p for p in K.PARCALAR}
S={n:p['wp'].val() for n,p in P.items()}
new=[n for n in P if n.startswith(('vakum_','destek_','tepsi_cubugu_'))]
new += [n for n in P if n.startswith('kablo_kanali_ust_mesafe_') or n=='surucu_STP-DRV-4830_12']
times=[0,.35,.65,1,1.4,1.65,1.8,2.3,2.7,3,3.5,3.7,4,4.5,5.3,6.3,7.6,8.5,10,15,19,22.8]
if 'dense' in sys.argv:times=sorted(set(times+[i/4 for i in range(92)]))
R={'parts':len(P),'source_sha256':hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(),'complete':False,'sample_count':len(times),'invalid':[n for n,s in S.items() if not s.isValid()],'collisions':[],'support':[],'envelope':[]}
volume_cache={};shape_cache={};bb_cache={}
def transform_key(M):return tuple(round(v,7) for row in M[:3] for v in row)
def relative_key(A,B):
    # Rigid relative transform: invariant when both shapes share a carriage.
    vals=[sum(A[k][i]*B[k][j] for k in range(3)) for i in range(3) for j in range(3)]
    vals += [sum(A[k][i]*(B[k][3]-A[k][3]) for k in range(3)) for i in range(3)]
    return tuple(round(v,6) for v in vals)
for t in times:
    W=K.blank_dunya(t)
    matrices={n:W[P[n]['grup']] if P[n]['grup'].startswith('B_') else K.grup_matrisi(P[n]['grup'],t) for n in S if P[n]['grup'] not in ('PIZZA','CATAL','K_ITICI','SABIT_REF')}
    world={};bb={}
    for n,M in matrices.items():
        key=(n,transform_key(M))
        if key not in shape_cache:
            shape_cache[key]=K.uygula(S[n],M);bb_cache[key]=shape_cache[key].BoundingBox()
        world[n]=shape_cache[key];bb[n]=bb_cache[key]
    seen=set()
    for n in new:
        a=world[n]
        q=bb[n]
        if q.ymin<123 or q.ymax>K.H+.1 or q.xmin<-.1 or q.xmax>K.W+.1 or q.zmin<-K.D-.1 or q.zmax>K.Z_ON+.1:R['envelope'].append([t,n])
        for m,b in world.items():
            if n==m or tuple(sorted((n,m))) in seen:continue
            seen.add(tuple(sorted((n,m))))
            if not K._bb_kesisir(bb[n],bb[m]):continue
            key=(n,m,relative_key(matrices[n],matrices[m]))
            if key not in volume_cache:volume_cache[key]=a.intersect(b).Volume()
            v=volume_cache[key]
            if v>.5:R['collisions'].append([t,n,m,round(v,2)])
    if 2.7<=t<=8.5:
        base=next(n for n in P if n=='B_TABAN')
        R['support'].append([t,min(world[base].distance(world[n]) for n in new if n.startswith('tepsi_cubugu_'))])
    print('TIME',t,'hits',len(R['collisions']),flush=True)
    (Path(__file__).resolve().parents[2]/'_local'/'kutu-v11'/'check.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
out=Path(__file__).resolve().parents[2]/'_local'/'kutu-v11'/'check.json'
R['complete']=True
out.write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R,indent=2),flush=True)
if 'connections' in sys.argv:
    # 0.25 mm accounts for running fits; contact is not proof of a load-rated joint.
    names=[n for n in P if not P[n]['grup'].startswith('B_') and P[n]['grup'] not in ('PIZZA','CATAL','K_ITICI','SABIT_REF') and P[n]['mal']!='karton_yigin' and not n.startswith('icecek_')]
    solids={n:K.uygula(S[n],K.grup_matrisi(P[n]['grup'],0)) for n in names}
    boxes={n:s.BoundingBox() for n,s in solids.items()}
    graph={n:set() for n in names}
    for i,n in enumerate(names):
        for m in names[i+1:]:
            a,b=boxes[n],boxes[m]
            if any(getattr(a,k+'min')>getattr(b,k+'max')+.25 or getattr(b,k+'min')>getattr(a,k+'max')+.25 for k in 'xyz'):continue
            if solids[n].distance(solids[m])<=.25:graph[n].add(m);graph[m].add(n)
    todo=set(names);components=[]
    while todo:
        found=set();stack=[next(iter(todo))]
        while stack:
            n=stack.pop()
            if n in found:continue
            found.add(n);stack.extend(graph[n]-found)
        todo-=found;components.append(sorted(found))
    components.sort(key=len,reverse=True)
    (out.parent/'connections.json').write_text(json.dumps(components,indent=2),encoding='utf-8')
    print('CONNECTION_COMPONENTS',list(map(len,components)),flush=True)
