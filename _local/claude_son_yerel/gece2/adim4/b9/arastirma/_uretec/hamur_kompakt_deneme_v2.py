"""AUTOKITCH hamur tepsisi denemesi v2 -- MOTORIZED DRAWERS RETAINED.
Separate 3D comparison specimens, NOT a whole cold-store redesign.
Only removable insert and food positions change versus store_cad_v5.
All dimensions mm. Food envelopes are existing CAD, not measured proofed dough.
"""
from pathlib import Path
import csv,json,math,struct,sys,os
import numpy as np
import cadquery as cq
import store_cad_v5 as S

OUT=Path(__file__).resolve().parents[1]/'1_STORE_hamur_deneme_v2'
X0,YO=S.XI,400.
STROKE=S.STROK
V,A=160.,400. # [V] illustrative speed/acceleration, not validated hardware motion
RAMP=V/A;MOVE=STROKE/V+RAMP;HOLD=3.;TEND=.8+2*MOVE+HOLD+.8
MODELS={};REPORTS={}
def pos_at(t):
 def travel(t):
  if t<=0:return 0.
  if t<RAMP:return .5*A*t*t
  if t<MOVE-RAMP:return .5*A*RAMP**2+V*(t-RAMP)
  if t<MOVE:return STROKE-.5*A*(MOVE-t)**2
  return STROKE
 return travel(t-.8)-travel(t-(.8+MOVE+HOLD))
def bb(sh):
 b=sh.BoundingBox();return np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])
def part(ad,sh,mal,group,bom=None):
 shape=sh.val() if isinstance(sh,cq.Workplane) else sh
 lo,hi=bb(shape)
 return dict(ad=ad,shape=shape,mal=mal,grup=group,bom=bom,lo=lo,hi=hi)

def layout(tip,new):
 t=S.TOP[tip];xc=X0+S.WO/2
 tub0=S.Z_CON0-2-S.TUB[tip]
 zc=tub0+5+t['td']/2
 if not new:
  pts=[(xc+(i-(t['nx']-1)/2)*t['ax'],zc+(j-(t['nz']-1)/2)*t['az']) for i in range(t['nx']) for j in range(t['nz'])]
  return pts,(xc-265,xc+265,tub0+5,tub0+5+t['td'])
 if tip=='hamur':
  pts=[(xc+(i-2)*105,zc+(j-2)*105) for i in range(5) for j in range(5)]
  return pts,(xc-265,xc+265,zc-263,zc+263)
 pts=[]
 for row in range(7):
  n=6 if row%2==0 else 5
  pts += [(xc+(i-(n-1)/2)*88,zc+(row-3)*76.5) for i in range(n)]
 return pts,(xc-265,xc+265,zc-272,zc+272)

def build(tip):
 kod='ORNEK_'+tip.upper();S.PARCALAR[:]=[]
 S.cekmece('K1',kod,tip,X0,YO)
 old=[part(p['ad'],p['wp'],p['mal'],p['grup'],p['bom']) for p in S.PARCALAR]
 mechanical=[p for p in old if not p['ad'].endswith('_tepsi') and '_top_' not in p['ad']]
 pts,bounds=layout(tip,True);a,b,c,d=bounds
 ty=YO+S.KC+1.;t=S.TOP[tip]
 holes=cq.Workplane('XZ').pushPoints(pts).circle(t['cr']).extrude(-(S.CUKUR_H+1)).translate((0,ty+S.TEPSI_T-S.CUKUR_H,0))
 insert=S.kut(a,b,ty,ty+S.TEPSI_T,c,d).cut(holes)
 new=mechanical+[part(kod+'_tepsi',insert,'silikon','CEKMECE',('New pocket pattern [V]',1,'Food-contact material approval pending',''))]
 dough=S.top_kati(tip)
 for i,(x,z) in enumerate(pts):new.append(part(kod+'_top_'+str(i),dough.translate((x,YO+S.Y_OTUR,z)),'hamur','CEKMECE'))
 for name,parts in [('old',old),('new',new)]:MODELS[tip+'_'+name]=parts
 oldpts,_=layout(tip,False)
 nearest=min(math.hypot(x-u,z-v) for i,(x,z) in enumerate(pts) for u,v in pts[i+1:])
 oldnearest=min(math.hypot(x-u,z-v) for i,(x,z) in enumerate(oldpts) for u,v in oldpts[i+1:])
 REPORTS[tip]=dict(old=len(oldpts),new=len(pts),increase_pct=round((len(pts)/len(oldpts)-1)*100,2),
  insert_mm=[b-a,d-c,S.TEPSI_T],nominal_dough_diameter_mm=2*t['R'],
  min_surface_gap_mm=round(nearest-2*t['R'],3),old_min_surface_gap_mm=round(oldnearest-2*t['R'],3),
  min_hole_web_mm=round(nearest-2*t['cr'],3),
  min_insert_edge_mm=round(min(min(x-a,b-x,z-c,d-z)-t['cr'] for x,z in pts),3),
  rear_dough_edge_when_open_mm=round(min(z-t['R']+STROKE for x,z in pts),3),
  clear_above_dough_mm=round(S.HH[tip]-S.Y_OTUR-t['hc']-t['R'],3),
  identical_mechanical_parts=len(mechanical),mechanical_geometry_reused_by_reference=True,
  two_day_trays_old=math.ceil((160 if tip=='hamur' else 400)/len(oldpts)),
  two_day_trays_new=math.ceil((160 if tip=='hamur' else 400)/len(pts)))
 assert all(p in new for p in mechanical)

def check(tip):
 parts=MODELS[tip+'_new'];invalid=[p['ad'] for p in parts if not p['shape'].isValid() or p['shape'].Volume()<=0]
 # Check NEW insert/food against unchanged mechanisms. Drawer original mounting
 # contacts are not relabeled as newly certified manufacturing joints.
 added=[p for p in parts if p['ad'].endswith('_tepsi') or '_top_' in p['ad']]
 mech=[p for p in parts if p not in added]
 hits=[];tests=0
 for stroke in np.linspace(0,STROKE,33):
  for p in added:
   v=np.array([0,0,stroke]);lo=p['lo']+v;hi=p['hi']+v
   for q in mech:
    factor={'SABIT':0,'CEKMECE_ARA':S.RAY_ARA_ORAN,'CEKMECE':1}.get(q['grup'],0)
    w=np.array([0,0,stroke*factor])
    if not(np.all(hi>q['lo']+w+.05) and np.all(q['hi']+w>lo+.05)):continue
    tests+=1;vol=p['shape'].translate(tuple(v)).intersect(q['shape'].translate(tuple(w))).Volume()
    if vol>.5:hits.append(dict(stroke=float(stroke),a=p['ad'],b=q['ad'],volume=round(vol,3)))
 # All-food and food/insert intersections checked at initial pose (same group).
 for i,p in enumerate(added):
  for q in added[i+1:]:
   if not(np.all(p['hi']>q['lo']+.05) and np.all(q['hi']>p['lo']+.05)):continue
   tests+=1;vol=p['shape'].intersect(q['shape']).Volume()
   if vol>.5:hits.append(dict(a=p['ad'],b=q['ad'],volume=round(vol,3)))
 r=REPORTS[tip];r.update(invalid=invalid,new_content_interferences=hits,exact_tests=tests,sampled_positions=33)
 assert r['rear_dough_edge_when_open_mm']>5
 assert r['min_surface_gap_mm']>=r['old_min_surface_gap_mm']-.001
 assert r['min_insert_edge_mm']>=2
 assert r['clear_above_dough_mm']>=2
 return not invalid and not hits

def glb(key,parts):
 groups=['SABIT','CEKMECE','CEKMECE_ARA'];nodes=[dict(name=g,children=[]) for g in groups];idx={g:i for i,g in enumerate(groups)}
 blob=bytearray();views=[];acc=[];meshes=[];mats=[];mi={}
 def buf(values,typ,target=None):
  a=np.asarray(values);a=a.astype('<u4' if a.dtype.kind in 'iu' else '<f4')
  while len(blob)%4:blob.append(0)
  view=dict(buffer=0,byteOffset=len(blob),byteLength=a.nbytes)
  if target:view['target']=target
  views.append(view);blob.extend(a.tobytes())
  at=dict(bufferView=len(views)-1,componentType=5125 if a.dtype.kind=='u' else 5126,count=len(a),type=typ)
  if a.dtype.kind!='u':at.update(min=np.atleast_1d(a.min(axis=0)).tolist(),max=np.atleast_1d(a.max(axis=0)).tolist())
  acc.append(at);return len(acc)-1
 def mat(name):
  if name not in mi:
   m=S.MALZEME.get(name,S.MALZEME['sac']);rgba=list(m['renk'])
   if name=='silikon':rgba=[.10,.55,.59,1] if key.endswith('new') else [.46,.51,.55,1]
   spec=dict(name=name,pbrMetallicRoughness=dict(baseColorFactor=rgba,metallicFactor=m['met'],roughnessFactor=m['ruf']),doubleSided=True)
   if rgba[3]<1:spec['alphaMode']='BLEND'
   mi[name]=len(mats);mats.append(spec)
  return mi[name]
 rotating=[]
 for p in parts:
  vv,ff=p['shape'].copy().tessellate(.35,.3);v=np.array([[q.x,q.y,q.z] for q in vv])*.001;f=np.array(ff,dtype=np.uint32)
  spin=p['ad'].endswith(('_motor_kasnagi','_motor_mili','_avara'))
  pivot=np.array([X0+S.KX,YO+S.KY,S.Z_AVARA if p['ad'].endswith('_avara') else S.Z_MOTOR])*.001
  if spin:v-=pivot
  n=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
  for j in range(3):np.add.at(n,f[:,j],fn)
  n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-20)
  meshes.append(dict(primitives=[dict(attributes=dict(POSITION=buf(v,'VEC3',34962),NORMAL=buf(n,'VEC3',34962)),indices=buf(f.flatten(),'SCALAR',34963),material=mat(p['mal']))]))
  ni=len(nodes);nodes[idx[p['grup']]]['children'].append(ni)
  node=dict(name=p['ad'],mesh=len(meshes)-1)
  if spin:node['translation']=pivot.tolist();rotating.append(ni)
  nodes.append(node)
 tt=np.linspace(0,TEND,401);ti=buf(tt,'SCALAR');sam=[];channels=[]
 for group,factor in [('CEKMECE',1),('CEKMECE_ARA',S.RAY_ARA_ORAN)]:
  sam.append(dict(input=ti,output=buf([[0,0,pos_at(t)*factor*.001] for t in tt],'VEC3'),interpolation='LINEAR'))
  channels.append(dict(sampler=len(sam)-1,target=dict(node=idx[group],path='translation')))
 for ni in rotating:
  angles=np.array([pos_at(t)/(S.KAS_PD/2) for t in tt])
  sam.append(dict(input=ti,output=buf([[math.sin(a/2),0,0,math.cos(a/2)] for a in angles],'VEC4'),interpolation='LINEAR'))
  channels.append(dict(sampler=len(sam)-1,target=dict(node=ni,path='rotation')))
 obj=dict(asset=dict(version='2.0',generator='AUTOKITCH motorized tray density trial v2; kinematics only'),scene=0,scenes=[dict(nodes=[0,1,2])],nodes=nodes,meshes=meshes,materials=mats,buffers=[dict(byteLength=len(blob))],bufferViews=views,accessors=acc,animations=[dict(name='Motorlu ac-kapa',samplers=sam,channels=channels)])
 js=json.dumps(obj,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
 while len(blob)%4:blob.append(0)
 (OUT/(key+'.glb')).write_bytes(struct.pack('<4sII',b'glTF',2,28+len(js)+len(blob))+struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(blob),b'BIN\0')+blob)
 with (OUT/(key+'_parcalar.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.writer(f,delimiter=';');wr.writerow(['ad','malzeme','grup','kaynak'])
  for p in parts:wr.writerow([p['ad'],p['mal'],p['grup'],'new insert/position [V]' if key.endswith('new') and (p['ad'].endswith('_tepsi') or '_top_' in p['ad']) else 'store_cad_v5 unchanged'])

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 ok=True
 for tip in ('hamur','lahm'):
  build(tip);ok=check(tip) and ok;print(tip,REPORTS[tip],flush=True)
 report=dict(version=2,status='DESIGN_TRIAL_NOT_PRODUCTION_RELEASE',motorized=True,robot_drawer_pulling=False,stroke_mm=STROKE,
  unchanged=['external drawer dimensions','Transmotec motor geometry','GT3 belt and pulleys','Accuride three-part rails','sensors','front and gasket','stroke'],
  altered=['removable insert pocket pattern','insert depth within existing tray','dough positions'],
  nominal_envelope_capacity_old=8*20+12*36,nominal_envelope_capacity_new=8*25+12*39,
  loading_rule='160 pide +400 lahmacun unchanged; full trays are capacity illustration only',results=REPORTS,
  duration=TEND,open_time=.8+MOVE+.8,speed_mm_s=V,acceleration_mm_s2=A,
  limitations=['No proofing expansion data; CAD dough size only','Gripper finger envelope not validated; minimum dough spacing is not an access proof',
   'Motor torque/load test not performed with increased dough mass','This is a removable-insert proposal, not a full redesigned STORE cabinet',
   'Original motor/rail geometries are source models, not newly downloaded supplier STEP','Animation is illustrative, not real machine control or physics'])
 (OUT/'kontrol_v2.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
 if not ok:raise RuntimeError('New insert/food collision audit failed; GLB export blocked')
 for key,parts in MODELS.items():glb(key,parts)
 print('EXPORTED FOUR COMPARISON GLBs',OUT,flush=True)
 sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
