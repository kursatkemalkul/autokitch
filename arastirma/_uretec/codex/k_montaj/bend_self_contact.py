"""Native closed panel/strip self-contact at the <=2mm source path samples.

No press tool or inter-station installation checks are implied by this audit.
"""
from lower_support import *
import math
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
import sac_ent as SE
import manifold3d as mf
K.KAPAK_X=(3.,399.);factory=K.kur();_,_,new_shelf=build()
sheets={s.ad:s for s in factory.SAC};sheets[new_shelf.ad]=new_shelf
data=json.loads((OUT/'source_bending_updated.json').read_text(encoding='utf8'));paths=json.loads((OUT/'bend_path_samples.json').read_text(encoding='utf8'));path_by={r['part']:r for r in paths['checks']}
def mesh_block(b,t,block,f):
    a,end,w0,w1=block;V=[];F=[];Z=np.array([0.,0.,1.]);e=Z*(-1 if b['direction']>0 else 1)
    for i in range(33):
        s=a+(end-a)*i/32
        for w,z in ((w0,0),(w1,0),(w1,t),(w0,t)):
            v=np.array(b['p0'])+np.array(b['edge'])*w+Z*z
            if f==0:v+=np.array(b['out'])*s
            else:
                th=b['angle']*f;R=b['BA']/th-b['K']*t;r=R+t-z if b['direction']>0 else R+z;angle=th*s/b['BA']
                v+=r*(np.cross(b['axis'],e)*math.sin(angle)-e*2*math.sin(angle/2)**2)
            V.append(v)
    for i in range(32):
        for k in range(4):
            u=4*i+k;v=4*i+(k+1)%4;x=v+4;y=u+4;F.extend(((u,v,x),(u,x,y)))
    F.extend(((0,2,1),(0,3,2),(128,129,130),(128,130,131)))
    return SE.mf_ucgen(np.array(V)[np.array(F)])
def poses(rec,states):
    out={0:np.eye(4)}
    for b in rec['bends']:
        f=states[b['number']]
        if f==0:M=np.array(b['flat_child'])
        else:
            theta=b['angle']*f;R=b['BA']/theta-b['K']*rec['t'];rot=S._rot(np.array(b['axis']),theta);Z=np.array([0.,0.,1.]);c=rec['t']+R if b['direction']>0 else -R
            delta=np.cross(b['axis'],Z)*math.sin(theta)-Z*2*math.sin(theta/2)**2;M=S._M(np.column_stack([rot@b['out'],b['edge'],rot@Z]),np.array(b['p0'])-c*delta)
        out[b['child']]=out[b['parent']]@M
    return out
rows=[]
for rec in data['sheets']:
    if not rec['bends']:continue
    sheet=sheets[rec['name']];pk,_=sheet._yerel_katilar();_,ser=sheet._bolgeler()
    panel_m={key:SE.mf_ucgen(SE.ucgen(sh)) for key,sh in pk.items() if sh is not None};bad=[];unknown=[];contacts=[];tested=0
    for phase in path_by[rec['name']]['phase_samples']:
        states={number:min(1,max(0,phase*len(rec['order'])-i)) for i,number in enumerate(rec['order'])};M=poses(rec,states);objects=[]
        for key,m in panel_m.items():
            if m is None:unknown.append({'panel':key,'phase':phase});continue
            objects.append((f'panel_{key}',m.transform(M[key][:3,:4])))
        for b in rec['bends']:
            for j,block in enumerate(S._dikd_ayir(ser[b['number']-1],b['BA'])):
                m=mesh_block(b,rec['t'],block,states[b['number']])
                if m is None:unknown.append({'strip':b['number'],'block':j,'phase':phase});continue
                objects.append((f'strip_{b["number"]}_{j}',m.transform(M[b['parent']][:3,:4])))
        bounds={name:np.array(m.bounding_box()).reshape(2,3) for name,m in objects}
        for i,(a,ma) in enumerate(objects):
            for b,mb in objects[i+1:]:
                aa,bb=bounds[a],bounds[b]
                if np.any(np.minimum(aa[1],bb[1])-np.maximum(aa[0],bb[0])<1e-4):continue
                tested+=1;intersection=ma^mb;v=intersection.volume()
                if v>.05:
                    # One sheet is decomposed into tangent panel/strip solids.
                    # Rounded mesh coordinates can overlap at their common
                    # cut plane. Accept ONLY that recorded adjacent boundary,
                    # after measuring every overlap vertex within 0.001mm of it.
                    boundary=False;depth=None
                    if a.startswith('panel_') and b.startswith('strip_'):
                        number=int(b.split('_')[1]);bend=next(r for r in rec['bends'] if r['number']==number)
                        if a==f'panel_{bend["child"]}':
                            V=np.asarray(intersection.to_mesh().vert_properties)[:,:3];inv=np.linalg.inv(M[bend['child']]);Q=V@inv[:3,:3].T+inv[:3,3];depth=float(np.abs(Q[:,0]).max());boundary=depth<=.001
                    row={'a':a,'b':b,'phase':phase,'volume_mm3':v}
                    if boundary:row.update(reason='same-sheet tangent decomposition boundary',maximum_boundary_depth_mm=depth);contacts.append(row)
                    else:bad.append(row)
    row={'part':rec['name'],'poses':len(path_by[rec['name']]['phase_samples']),'solid_pair_tests':tested,'collisions':bad,'measured_same_sheet_boundary_contacts':contacts,'unresolved_solids':unknown,'passed':not bad and not unknown};rows.append(row)
    print('SELF_BEND',rec['name'],'tested',tested,'collisions',len(bad),'unresolved',len(unknown),flush=True)
report={'scope':'native sheet panel/strip self-contact only; source match and press tools separate','checks':rows,'passed':all(r['passed'] for r in rows),'press_tool_checked':False,'full_assembly_release':False}
(OUT/'bend_self_contact.json').write_text(json.dumps(clean(report),indent=2),encoding='utf8');sys.stdout.flush();os._exit(0 if report['passed'] else 2)
