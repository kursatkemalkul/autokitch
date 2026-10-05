"""AUTOKITCH hamur deposu - robotla cekilen pasif tepsiler, v1.

AYRI KAVRAM DENEMESI. Ana montaji/STORE'u degistirmez. mm, Y yukari.
Kaynak: store_cad_v5.py; stok hafizasi 27 Eyl: 160 pide + 400 lahmacun.
Yeni boyutlar [V]; robot IK/kuvvet, sogutma ve hijyen validasyonu YOK.
"""
from pathlib import Path
import csv, json, math, struct
import numpy as np
import cadquery as cq
import store_cad_v5 as OLD

OUT = Path(__file__).resolve().parents[1] / '1_STORE_hamur_deneme_v1'
W,D,H,STROKE = 1380.,830.,1060.,700.
PARTS=[]; GROUPS={'FRAME':None,'SHELL':None,'HOOK':None}; TRAYS=[]
MAT={
 'steel':([.63,.70,.76,1],.7,.32),
 'front':([.19,.41,.49,.25],.25,.5),
 'shell':([.66,.75,.81,.10],.25,.5),
 'liner':([.72,.79,.81,1],.65,.4),
 'blue':([.10,.34,.59,1],.2,.5),
 'tray_p':([.26,.57,.63,1],.0,.8),
 'tray_l':([.54,.44,.72,1],.0,.8),
 'dough_p':([.93,.80,.56,1],0,.92),
 'dough_l':([.97,.88,.69,1],0,.92),
 'black':([.10,.12,.15,1],.1,.65),
 'hook':([1,.47,.12,1],.45,.3),
}
def boxsh(x0,x1,y0,y1,z0,z1):
 return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def cyl(r,l,p,axis=(0,1,0)):
 return cq.Solid.makeCylinder(r,l,cq.Vector(*p),cq.Vector(*axis))
def add(name,shape,mat='steel',group='FRAME',pos=(0,0,0),kind='V_YENI_GEOMETRI'):
 GROUPS.setdefault(group,None)
 sh=shape.val() if isinstance(shape,cq.Workplane) else shape
 b=sh.BoundingBox(); pos=np.array(pos,dtype=float)
 PARTS.append(dict(name=name,shape=sh,mat=mat,group=group,pos=pos,kind=kind,
   lo=np.array([b.xmin,b.ymin,b.zmin])+pos,hi=np.array([b.xmax,b.ymax,b.zmax])+pos))
def box(name,b,mat='steel',group='FRAME',**kw):add(name,boxsh(*b),mat,group,**kw)
def motion(t):
 def s(a,b):
  q=max(0,min(1,(t-a)/(b-a)));return q*q*(3-2*q)
 d=STROKE*(s(1.8,5.8)-s(11.6,15.6))
 hy=-25+25*s(1,1.8)-25*s(5.8,6.5)+25*s(10.9,11.6)-25*s(15.6,16.3)
 # Disengage downwards while the drawer is open. No extra projection into aisle.
 hz=d+30*(1-s(0,1)+s(16.3,17))
 return d,hy,hz

def build():
 # No compressor/panel invented here: this is the DOUGH storage portion only.
 for nm,b in [('left',(0,50,123,1060,-830,-40)),('right',(1330,1380,123,1060,-830,-40)),
              ('back',(50,1330,123,1060,-830,-790)),('top',(50,1330,1000,1060,-790,-40))]:
  box('insulated_'+nm,b,'shell','SHELL',kind='V_INSULATION_ENVELOPE')
 box('bottom',(0,W,123,164.5,-830,-40),'liner')
 box('divider',(670,710,164.5,1000,-790,-40),'shell','SHELL')
 for x,side in ((50,-1),(670,1),(710,-1),(1330,1)):
  xa,xb=sorted((x,x+6*side))
  for z in (-778,-55):box('post_%s_%s'%(x,z),(xa,xb,164.5,1000,z-6,z+6),'steel')
 for x in (35,1345):
  for z in (-775,-55):add('foot',cyl(23,12,(x,0,z)).fuse(cyl(8,111,(x,12,z))))
 remaining={'p':160,'l':400}
 arrangement=[(['p']*7+['l'],50),(['l']*9,710)]
 for col,(types,x0) in enumerate(arrangement):
  y=255.
  for i,typ in enumerate(types):
   pitch=95. if typ=='p' else 80.; nx,nz=(5,5) if typ=='p' else (6,7)
   sx,sz=(105.,130.) if typ=='p' else (88.,90.)
   key=f'{"PIDE" if typ=="p" else "LAHMACUN"}_{col+1}_{i+1}'
   n=min(remaining[typ],nx*nz);remaining[typ]-=n
   xc=x0+310.; group='D_'+key; middle='M_'+key
   tr=dict(key=key,typ=typ,x0=x0,xc=xc,y=y,pitch=pitch,load=n,capacity=nx*nz,group=group,middle=middle)
   TRAYS.append(tr)
   # 560 x 650 tray: centre spacings from OLD are preserved, not made denser.
   tray=boxsh(x0+30,x0+590,y,y+1.5,-710,-60)
   for b in [(x0+30,x0+31.5,y+1.5,y+12,-710,-60),(x0+588.5,x0+590,y+1.5,y+12,-710,-60),
             (x0+31.5,x0+588.5,y+1.5,y+12,-710,-708.5),(x0+31.5,x0+588.5,y+1.5,y+12,-61.5,-60)]:tray=tray.fuse(boxsh(*b))
   add(key+'_tray',tray,'steel',group)
   box(key+'_washable_insert',(x0+32,x0+588,y+1.5,y+4,-708,-62),'tray_'+typ,group)
   # Insulated individual front; adjacent fronts have 3 mm gap.
   fa,fb=(2,688) if col==0 else (692,1378)
   box(key+'_front',(fa,fb,y-5,y+pitch-8,-40,0),'front',group,kind='V_INSULATED_FRONT_40')
   for xs in (x0+31.5,x0+576):box(key+'_front_bracket',(xs,xs+12,y+14,y+34,-60,-40),'steel',group)
   # Gasket outline; cross section simplified, not a selected gasket catalogue part.
   gasket=boxsh(x0+13,x0+607,y-1,y+pitch-13,-53,-40).cut(boxsh(x0+21,x0+599,y+7,y+pitch-21,-54,-39))
   add(key+'_gasket',gasket,'black',group,kind='V_GASKET_PROFILE_UNSELECTED')
   # Robot catches a horizontal handle; drawer weight remains on slides.
   for xx in (xc-22,xc+18):box(key+'_handle_ear',(xx,xx+4,y+32,y+48,0,22),'steel',group)
   add(key+'_handle_pin',cyl(4,40,(xc-20,y+42,20),(1,0,0)),'steel',group)
   box(key+'_label',(x0+15,x0+75,y+15,y+36,0,1),'blue',group)
   # Three nested rails, same cross section convention as original model.
   for side,rx,sign in [('L',x0,1),('R',x0+620,-1)]:
    def rbox(w0,w1,v0,v1,za,zb):
     a,b=sorted((rx+sign*w0,rx+sign*w1));return boxsh(a,b,y+4+v0,y+4+v1,za,zb)
    sections=[('outer','FRAME',[(0,1.2,0,45.7),(0,8.5,0,1.2),(0,8.5,44.5,45.7)],-760,-60),
              ('middle',middle,[(1.7,2.7,1.7,44),(1.7,10.5,1.7,2.7),(1.7,10.5,43,44)],-758,-62),
              ('inner',group,[(11.5,12.7,5,40.7),(3.2,12.7,5,6.2),(3.2,12.7,39.5,40.7)],-756,-64)]
    for label,g,ss,za,zb in sections:
     sh=rbox(*ss[0],za,zb)
     for q in ss[1:]:sh=sh.fuse(rbox(*q,za,zb))
     add(key+'_'+side+'_'+label,sh,'steel',g,kind='CATALOG_ENVELOPE_3832_700_NOT_MANUFACTURER_STEP')
    if sign==1:b=(x0+12.7,x0+30,y+11,y+16,-700,-70)
    else:b=(x0+590,x0+607.3,y+11,y+16,-700,-70)
    box(key+'_'+side+'_mount',b,'steel',group)
   # Fixed support strips attach outer rails to cabinet structure.
   for xs in (x0-2,x0+620):box(key+'_rail_mount',(xs,xs+2,y+4,y+49.7,-778,-49),'steel')
   # Show closed/open flag locations; electrical safety system is not designed here.
   box(key+'_closed_flag',(x0+18,x0+25,y+23,y+32,-76,-70),'blue',group)
   rad=47.5 if typ=='p' else 37.5; hc=12. if typ=='p' else 10.
   dough=OLD.top_kati('hamur' if typ=='p' else 'lahm').val()
   ring=cyl(rad+2.5,3,(0,0,0)).cut(cyl(rad+1.0,5,(0,-1,0)))
   for ix in range(nx):
    for iz in range(nz):
     px=xc+(ix-(nx-1)/2)*sx;pz=-385+(iz-(nz-1)/2)*sz
     add(key+f'_well_{ix}_{iz}',ring,'tray_'+typ,group,(px,y+4,pz))
     if ix*nz+iz<n:add(key+f'_dough_{ix}_{iz}',dough,'dough_'+typ,group,(px,y+4,pz),kind='SOURCE_STORE_V5_DOUGH_GEOMETRY')
   y+=pitch
 assert remaining=={'p':0,'l':0}
 # U-shaped pull hook, open upward. The robot arm is NOT invented/animated.
 hook=boxsh(-10,10,32,55,8,34).cut(cyl(5,22,(-11,42,20),(1,0,0))).cut(boxsh(-11,11,42,56,15,25))
 hook=hook.fuse(boxsh(-10,10,32,37,34,85)).fuse(boxsh(-25,25,27,62,85,90))
 for x in (-17,17):hook=hook.cut(cyl(2.75,7,(x,44,84),(0,0,1)))
 add('ROBOT_TOOL_HOOK_ONLY_NO_ARM',hook,'hook','HOOK',kind='V_TOOL_HOOK_NOT_FINAL_ROBOT_GRIPPER')

def overlap(a,b):return np.all(a['hi']>b['lo']+.05) and np.all(b['hi']>a['lo']+.05)
def shifted(p,v):return dict(p,lo=p['lo']+v,hi=p['hi']+v)
def audit():
 invalid=[p['name'] for p in PARTS if not p['shape'].isValid() or p['shape'].Volume()<=0]
 # Selected drawer against cabinet AND every other drawer, swept at 21 poses.
 # Same-group designed joints, food/support contact are not collision claims.
 hits=[];exact=0; minover=1e9
 for tr in TRAYS:
  moving=[p for p in PARTS if p['group'] in (tr['group'],tr['middle'])]
  obstacles=[p for p in PARTS if p['group'] not in (tr['group'],tr['middle'],'HOOK')]
  obslo=np.array([p['lo'] for p in obstacles]);obshi=np.array([p['hi'] for p in obstacles])
  for d in np.linspace(0,STROKE,21):
   for p in moving:
    v=np.array([0,0,d*(.5 if p['group']==tr['middle'] else 1)])
    q=shifted(p,v)
    candidates=np.where(np.all(q['hi']>obslo+.05,axis=1)&np.all(obshi>q['lo']+.05,axis=1))[0]
    for oi in candidates:
     ob=obstacles[oi]
     exact+=1
     vol=p['shape'].translate(tuple(p['pos']+v)).intersect(ob['shape'].translate(tuple(ob['pos']))).Volume()
     if vol>.5:hits.append(dict(tray=tr['key'],stroke=float(d),a=p['name'],b=ob['name'],mm3=round(vol,2)))
   minover=min(minover,698-d*.5,694-d*.5)
  print('checked',tr['key'],flush=True)
 # Check the modeled hook path separately; NOT a robot-arm clearance test.
 hook=next(p for p in PARTS if p['group']=='HOOK');hook_hits=[]
 for tr in (TRAYS[3],TRAYS[11]):
  obs=[p for p in PARTS if p['group']!='HOOK']
  baselo=np.array([p['lo'] for p in obs]);basehi=np.array([p['hi'] for p in obs])
  factors=np.array([1. if p['group']==tr['group'] else .5 if p['group']==tr['middle'] else 0. for p in obs])
  for t in np.linspace(0,17,171):
   d,hy,hz=motion(t);hv=np.array([tr['xc'],tr['y']+hy,hz]);hq=shifted(hook,hv)
   delta=np.zeros_like(baselo);delta[:,2]=factors*d
   ids=np.where(np.all(hq['hi']>baselo+delta+.05,axis=1)&np.all(basehi+delta>hq['lo']+.05,axis=1))[0]
   for j in ids:
    p=obs[j];exact+=1
    vol=hook['shape'].translate(tuple(hv)).intersect(p['shape'].translate(tuple(p['pos']+delta[j]))).Volume()
    if vol>.5:hook_hits.append(dict(tray=tr['key'],time=float(t),part=p['name'],mm3=round(vol,2)))
 # Reach is a necessary sphere test only, NOT IK or robot collision validation.
 reach=[]
 for tr in TRAYS:
  nx,nz=(5,5) if tr['typ']=='p' else (6,7);sx,sz=(105,130) if tr['typ']=='p' else(88,90)
  for x in (-(nx-1)*sx/2,(nx-1)*sx/2):
   for z in (-385-(nz-1)*sz/2+700,-385+(nz-1)*sz/2+700):
    reach.append(math.sqrt(x*x+(tr['y']+42-970)**2+(z-360)**2))
 report=dict(status='CONCEPT_ONLY_NOT_PRODUCTION_RELEASE',parts=len(PARTS),invalid=invalid,
   sampled_drawer_interferences=hits,hook_interferences=hook_hits,hook_samples_per_demo=171,exact_boolean_tests=exact,stroke_samples_per_drawer=21,
   slide_overlap_min_mm=minover,ray_middle_ratio='[V] 0.5; real cage path needs confirmation',
   stock=dict(pide=160,lahmacun=400,total=560),trays=17,
   old=dict(dough_trays=20,columns_occupied=3,width_span_mm=2010,station_width_mm=2500,strok_mm=628),
   proposal=dict(width_mm=W,depth_mm=D,height_mm=H,stroke_mm=STROKE,pide_trays=7,lahmacun_trays=10,
      plan_reduction_percent=round((2010-W)/2010*100,1),extra_open_projection_mm=72),
   maximum_pick_tcp_distance_mm=round(max(reach),1),reference_reach_mm=779,
   reach_caveat='Necessary spherical check only. Tool offset, joint IK, rail/base collision not verified.',
   unresolved=['Robot hook attachment and pull force; no complete gripper/arm model',
    'Rail detent/hold-open and fail-safe robot handshaking',
    'Cold humid service approval of the rail, manufacturer STEP and width derating',
    'Gasket breakaway force, front profile, tolerance and screw joints',
    'Cooling capacity and air distribution; this is not the full cold station',
    'Dough proofing growth and gripper release verified only against old envelope, not real dough',
    '17-second kinematic illustration is not a measured or simulated production cycle'])
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'kontrol_v1.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
 if invalid or hits or hook_hits:raise RuntimeError(f'CAD CHECK FAILED: invalid={len(invalid)}, drawer hits={len(hits)}, hook hits={len(hook_hits)}')
 return report

def export():
 nodes=[dict(name=g,children=[]) for g in GROUPS];gi={g:i for i,g in enumerate(GROUPS)}
 blob=bytearray();views=[];acc=[];meshes=[];cache={}
 def buf(arr,typ,target=None):
  a=np.asarray(arr);a=a.astype('<u4' if a.dtype.kind in 'iu' else '<f4')
  while len(blob)%4:blob.append(0)
  v=dict(buffer=0,byteOffset=len(blob),byteLength=a.nbytes)
  if target:v['target']=target
  views.append(v);blob.extend(a.tobytes())
  at=dict(bufferView=len(views)-1,componentType=5125 if a.dtype.kind=='u' else 5126,count=len(a),type=typ)
  if a.dtype.kind!='u':at.update(min=np.atleast_1d(a.min(axis=0)).tolist(),max=np.atleast_1d(a.max(axis=0)).tolist())
  acc.append(at);return len(acc)-1
 mats=[];mi={}
 for name,(rgba,met,rough) in MAT.items():
  mi[name]=len(mats);mats.append(dict(name=name,doubleSided=True,alphaMode='BLEND' if rgba[3]<1 else 'OPAQUE',pbrMetallicRoughness=dict(baseColorFactor=rgba,metallicFactor=met,roughnessFactor=rough)))
 for p in PARTS:
  # Shared dough/ring BReps mesh once; others keep their true coordinates.
  key=(id(p['shape']),p['mat'])
  if key not in cache:
   vv,ff=p['shape'].copy().tessellate(.45,.3);v=np.array([[q.x,q.y,q.z] for q in vv])*.001;f=np.array(ff,dtype=np.uint32)
   normals=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
   for j in range(3):np.add.at(normals,f[:,j],fn)
   normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-20)
   meshes.append(dict(primitives=[dict(attributes=dict(POSITION=buf(v,'VEC3',34962),NORMAL=buf(normals,'VEC3',34962)),indices=buf(f.flatten(),'SCALAR',34963),material=mi[p['mat']])]))
   cache[key]=len(meshes)-1
  nodes[gi[p['group']]]['children'].append(len(nodes))
  nodes.append(dict(name=p['name'],mesh=cache[key],translation=(p['pos']*.001).tolist(),extras=dict(status=p['kind'])))
 animations=[];tt=np.linspace(0,17,341);ti=buf(tt,'SCALAR')
 for target in (TRAYS[3],TRAYS[11]):
  sam=[];channels=[]
  for g in GROUPS:
   if g in ('FRAME','SHELL'):continue
   values=[]
   for t in tt:
    d,hy,hz=motion(t)
    if g==target['group']:v=(0,0,d)
    elif g==target['middle']:v=(0,0,d*.5)
    elif g=='HOOK':v=(target['xc'],target['y']+hy,hz)
    else:v=(0,0,0)
    values.append(np.array(v)*.001)
   sam.append(dict(input=ti,output=buf(values,'VEC3'),interpolation='LINEAR'))
   channels.append(dict(sampler=len(sam)-1,target=dict(node=gi[g],path='translation')))
  animations.append(dict(name='Pide tepsisi' if target['typ']=='p' else 'Lahmacun tepsisi',samplers=sam,channels=channels))
 nodes[gi['HOOK']]['translation']=[TRAYS[3]['xc']*.001,(TRAYS[3]['y']-25)*.001,.1]
 data=dict(asset=dict(version='2.0',generator='AUTOKITCH hamur compact v1 CONCEPT, not production'),scene=0,scenes=[dict(nodes=list(gi.values()))],
   nodes=nodes,meshes=meshes,materials=mats,buffers=[dict(byteLength=len(blob))],bufferViews=views,accessors=acc,animations=animations)
 raw=json.dumps(data,separators=(',',':')).encode();raw+=b' '*((-len(raw))%4)
 while len(blob)%4:blob.append(0)
 path=OUT/'hamur_kompakt_deneme_v1.glb'
 path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(raw)+len(blob))+struct.pack('<I4s',len(raw),b'JSON')+raw+struct.pack('<I4s',len(blob),b'BIN\0')+blob)
 with (OUT/'parcalar_v1.csv').open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.writer(f,delimiter=';');wr.writerow(['name','group','material','status'])
  wr.writerows((p['name'],p['group'],p['mat'],p['kind']) for p in PARTS)
 print('EXPORTED',path,'bytes',path.stat().st_size,flush=True)

if __name__=='__main__':
 build();print('BUILT',len(PARTS),'parts',flush=True);audit();export()
 # Avoid OCC destructor shutdown faults after the validated files are closed.
 import sys,os
 sys.stdout.flush();os._exit(0)
