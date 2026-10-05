"""Adaptive source-vertex motion samples, max 2mm per sampled bend pose.

This validates finite paths/endpoints and sampling, NOT collision/tool access.
"""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'_local/codex_k_montaj'
data=json.loads((O/'source_bending_updated.json').read_text(encoding='utf8'))
def rotation(k,angle):
    k=np.array(k);K=np.array([[0,-k[2],k[1]],[k[2],0,-k[0]],[-k[1],k[0],0]])
    return np.eye(3)+math.sin(angle)*K+2*math.sin(angle/2)**2*(K@K)
def decode(sheet,phase):
    states={number:min(1,max(0,phase*len(sheet['order'])-i)) for i,number in enumerate(sheet['order'])};poses={0:np.eye(4)};bends={b['number']:b for b in sheet['bends']};Z=np.array([0.,0.,1.])
    for b in sheet['bends']:
        f=states[b['number']]
        if f==0:M=np.array(b['flat_child'])
        else:
            theta=b['angle']*f;R=b['BA']/theta-b['K']*sheet['t'];rot=rotation(b['axis'],theta);c=sheet['t']+R if b['direction']>0 else -R
            delta=np.cross(b['axis'],Z)*math.sin(theta)-Z*2*math.sin(theta/2)**2
            M=np.eye(4);M[:3,:3]=np.column_stack([rot@b['out'],b['edge'],rot@Z]);M[:3,3]=np.array(b['p0'])-c*delta
        poses[b['child']]=poses[b['parent']]@M
    points=[]
    for row in sheet['encoded_vertices']:
        if 'panel' in row:M=poses[row['panel']];v=np.array(row['point'])
        else:
            b=bends[row['bend']];f=states[b['number']];s,w,z=row['point'];v=np.array(b['p0'])+np.array(b['edge'])*w+Z*z;M=poses[b['parent']]
            if f==0:v+=np.array(b['out'])*s
            else:
                theta=b['angle']*f;R=b['BA']/theta-b['K']*sheet['t'];r=R+sheet['t']-z if b['direction']>0 else R+z;e=Z*(-1 if b['direction']>0 else 1);a=theta*s/b['BA']
                v+=r*(np.cross(b['axis'],e)*math.sin(a)-e*2*math.sin(a/2)**2)
        points.append(M[:3,:3]@v+M[:3,3])
    return np.array(points)
rows=[]
for sheet in data['sheets']:
    n=len(sheet['order']);times={0.,1.};maximum=0.;cache={}
    def at(t):
        if t not in cache:cache[t]=decode(sheet,t)
        return cache[t]
    def sample(a,b,depth=0):
        mid=(a+b)/2;P,Q,R=at(a),at(mid),at(b)
        distance=max(float(np.linalg.norm(Q-P,axis=1).max()),float(np.linalg.norm(R-Q,axis=1).max()))
        if not np.isfinite(distance):raise ValueError((sheet['name'],'nonfinite'))
        if distance>2.:
            assert depth<20,(sheet['name'],'sampling did not converge');sample(a,mid,depth+1);sample(mid,b,depth+1)
        else:times.update((a,mid,b))
    if n:
        for i in range(n):sample(i/n,(i+1)/n)
    else:at(0);at(1)
    ordered=sorted(times)
    for a,b in zip(ordered,ordered[1:]):maximum=max(maximum,float(np.linalg.norm(at(b)-at(a),axis=1).max()))
    local=at(1);root=np.array(sheet['root']);world=local@root[:3,:3].T+root[:3,3]+sheet['source_offset'];error=float(np.linalg.norm(world-sheet['vertices'],axis=1).max())
    row={'part':sheet['name'],'poses':len(ordered),'phase_samples':ordered,'maximum_adjacent_vertex_motion_mm':maximum,'endpoint_error_mm':error,'passed':maximum<=2.000001 and error<=.01,'collision_checked':False,'press_tool_checked':False};rows.append(row)
    print('BEND_PATH',sheet['name'],len(ordered),'max_step',round(maximum,5),'endpoint',round(error,6),flush=True)
report={'scope':'35 source sheet vertex trajectories only','checks':rows,'passed':all(r['passed'] for r in rows),'collision_checked':False,'full_assembly_release':False}
(O/'bend_path_samples.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('POSES',sum(r['poses'] for r in rows),'PASSED',report['passed'],flush=True);sys.exit(0 if report['passed'] else 2)
