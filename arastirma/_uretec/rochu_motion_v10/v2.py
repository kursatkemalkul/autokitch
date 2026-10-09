from finger_bend import deform
"""V2 poses on the V1 native scene; one immutable OEM four-finger mounting.

All lengths are metres. Only the copy's E pickup support can receive slots.
Soft-tip travel is an illustration; no force or carton qualification is claimed.
"""
from surface_check import *
from copy import deepcopy
from scipy.spatial.transform import Slerp

class Review:
 def __init__(self):
  self.m=Model();self.kin=Kin();self.old=json.loads((SOURCE/'poses.json').read_text())
  self.definition=json.loads((OUT/'head_definition.json').read_text())
  self.head=trimesh.load(io.BytesIO(gzip.decompress((OUT/'fixed_head.glb.gz').read_bytes())),file_type='glb')
  self.head_cache={};self.fixture_cache={};self.arm_cache={};self.search=[]
  self.arm=[s for s in self.m.shapes if node_body(self.m,s['id'])[1] is not None and int(node_body(self.m,s['id'])[1][-2:])<=6]
  self.products={k:next(s for s in self.m.shapes if s['name']==('ROBOT25_PRODUCT_Box' if k=='Box' else 'ROBOT25_'+k+'_stock_shape')) for k in ['Dough','Cola','Dessert','Box']}
  self.box_cuts=[]
  self.reference_products={}

 def head_parts(self,shift):
  key=round(float(shift),4)
  if key in self.head_cache:return self.head_cache[key]
  if len(self.head_cache)>24:self.head_cache.pop(next(iter(self.head_cache)))
  out=[]
  for n in self.head.graph.nodes_geometry:
   w,g=self.head.graph[n];t=self.head.geometry[g];v=t.vertices.copy()
   if n.startswith('OEM_DAC_'):
    v=deform(v,shift)
   v=v@w[:3,:3].T+w[:3,3];a,h=solid(v,t.faces);out.append((n,v,t.faces,a,h))
  self.head_cache[key]=out;return out

 def product_rotation(self,item,R):return R@np.array(self.old[item+'_pick']['tool_orientation']).T

 def pose(self,item,R,centre,rail=None,seed=None,shift=None):
  old=self.old[item+'_pick'];R=np.array(R);centre=np.array(centre);delta=np.array(old['tool_orientation']).T@(np.array(old['product'])-np.array(old['contact']))
  contact=centre-R@delta
  seeds=[seed] if seed is not None else [old['q'],self.old[item+'_place']['q'],[2.4,-1.3,1.5,-1.8,4.7,.9],[0,-1,1.8,-1.4,1.57,0]]
  p=solve_pose(self.kin,R,contact,rail if rail is not None else (self.kin.data['rail_min'] if item=='Dough' else self.kin.data['rail_max']),seeds)
  p.update(item=item,mode='place',product=centre.tolist(),product_rotation=self.product_rotation(item,R).tolist(),contact=contact.tolist(),tool_orientation=R.tolist(),tip_shift_mm=old['tip_shift_mm'] if shift is None else shift,drawer_open_m=0,root_hash=self.definition['root_hash'],finger_roots=self.definition['finger_roots'])
  return p

 def branches(self,p):
  q=np.array(p['q']);R=np.array(p['tool_orientation']);c=p['product'];out=[]
  for seed in [q,q+[0,0,0,np.pi,-2*q[4],np.pi],q+[np.pi,-.8,-1,0,0,0],q+[0,1,-2,1,0,0]]:
   a=self.pose(p['item'],R,c,p['rail'],seed,shift=p['tip_shift_mm'])
   if not a['valid']:continue
   if any(np.linalg.norm(np.arctan2(np.sin(np.array(a['q'])-x['q']),np.cos(np.array(a['q'])-x['q'])))<.001 for x in out):continue
   out.append(a)
  return out

 def fixture(self,s,cut=False,drawer=0):
  key=(id(s),cut,drawer)
  if key not in self.fixture_cache:
   v=s['world'].copy()
   if drawer and '__CEKMECE' in s['name'] and '__CEKMECE_ARA' not in s['name']:v[:,2]+=drawer
   a,h=solid(v,s['faces'])
   if cut and s['name'] in ['E_KALIP__sac__NEST','E_KALIP__sac']:
    for c in self.box_cuts:a=a-c
    mesh_data=a.to_mesh();v=np.asarray(mesh_data.vert_properties)[:,:3].astype(float);f=np.asarray(mesh_data.tri_verts,dtype=np.int32)
   else:f=s['faces']
   self.fixture_cache[key]=(v,f,a,h)
  return self.fixture_cache[key]

 def tool_parts(self,p,arm=False):
  w=np.array(p['worlds']['UR10E_body_06']);out=[]
  for n,v,f,a,h in self.head_parts(p['tip_shift_mm']):out.append((n,v@w[:3,:3].T+w[:3,3],f,a.transform(w[:3,:]),h))
  for s in self.arm:
   bn=node_body(self.m,s['id'])[1]
   if not arm and int(bn[-2:])<4:continue
   if id(s) not in self.arm_cache:
    old=self.m.matrix(node_body(self.m,s['id'])[0]);v=(s['world']-old[:3,3])@old[:3,:3];a,h=solid(v,s['faces']);self.arm_cache[id(s)]=(a,h)
   a,h=self.arm_cache[id(s)];now=np.array(p['worlds'][bn]);v=shape_at(self.m,s,p);out.append((s['name'],v,s['faces'],a.transform(now[:3,:]),h))
  return out

 def fixtures(self,item,mode='place'):
  if mode=='pick' and item=='Box':return [s for s in self.m.shapes if s['name'].startswith('E_')]
  if item=='Dough':return [s for s in self.m.shapes if 'ACICI' in s['name'] or 'DONER__TABLA' in s['name'] or s['name'].startswith(('A_','B_'))]
  return [s for s in self.m.shapes if s['name'].startswith('QR62_')]+self.reference_products.get(item,[])

 def check(self,p,mode='place',cut=False,arm=False,surface=False,product=True):
  parts=self.tool_parts(p,arm);hits=[];surface_hits=[];volume=0;proxies=0
  allv=np.vstack([x[1] for x in parts]);lo,hi=allv.min(0),allv.max(0)
  for s in self.fixtures(p['item'],mode):
   if np.any(s['bounds'][0]>hi) or np.any(s['bounds'][1]<lo):continue
   bv,bf,b,h=self.fixture(s,cut);proxies+=h
   for n,av,af,a,_ in parts:
    if np.any(bv.min(0)>av.max(0)) or np.any(bv.max(0)<av.min(0)):continue
    vol=max(0,float((a^b).volume())*1e9)
    if vol>.1:hits.append({'part':s['name'],'moving':n,'overlap_mm3':vol});volume+=vol
    if surface and crosses(av[af],bv[bf]):surface_hits.append({'part':s['name'],'moving':n})
  product_hits=[]
  if product:
   ps=self.products[p['item']];v=(ps['world']-ps['bounds'].mean(0))@np.array(p.get('product_rotation',np.eye(3))).T+np.array(p['product']);a,ph=solid(v,ps['faces'])
   for s in self.fixtures(p['item'],mode):
    if np.any(s['bounds'][0]>v.max(0)) or np.any(s['bounds'][1]<v.min(0)):continue
    bv,bf,b,h=self.fixture(s,cut);vol=max(0,float((a^b).volume())*1e9)
    if vol>.1:product_hits.append({'part':s['name'],'overlap_mm3':vol})
  return dict(ik_valid=p['valid'],position_error_mm=p['position_error_mm'],angle_error_deg=p['angle_error_deg'],tool_hits=hits,surface_hits=surface_hits,product_hits=product_hits,total_overlap_mm3=volume,fixture_proxy_components=proxies,arm_included=arm,root_hash=p['root_hash'])

 def bottom(self,item,R):
  s=self.products[item];v=(s['world']-s['bounds'].mean(0))@self.product_rotation(item,R).T
  return float(-v[:,1].min())

 def search_place(self,item):
  candidates=[]
  if item=='Dough':
   for pitch in [0,10,20,30,40,50]:
    for roll in [0,45,90,135,180,225,270,315]:
     R=Rotation.from_euler('x',pitch,degrees=True).as_matrix()@Rotation.from_euler('y',180,degrees=True).as_matrix()@Rotation.from_euler('z',roll,degrees=True).as_matrix()
     for drop in [3,8,15,25]:candidates.append((R,[1.08611652,1.00587+self.bottom(item,R)+drop/1000,-.16993615],{'pitch_up_deg':pitch,'roll_deg':roll,'drop_mm':drop}))
  elif item=='Cola':
   for heading in [0,-15,15,-90]:
    for roll in [0,45,90,135,180,225,270,315]:
     R=Rotation.from_euler('y',heading,degrees=True).as_matrix()@Rotation.from_euler('z',roll,degrees=True).as_matrix()
     for x,z in [(4.87,1.969),(4.91,1.955),(4.84,1.94)]:
      for drop in [4,12,25,40]:candidates.append((R,[x,.85+self.bottom(item,R)+drop/1000,z],{'heading_deg':heading,'roll_deg':roll,'drop_mm':drop}))
  else:
   for yaw in [45,30,60,-45,-30,135,-135,0,90]:
    for lean in [0,10,20,30,40]:
     R=Rotation.from_euler('y',yaw,degrees=True).as_matrix()@Rotation.from_euler('x',90+lean,degrees=True).as_matrix()
     for x,z in [(4.805,1.800),(4.83,1.800),(4.85,1.807)]:candidates.append((R,[x,.85+self.bottom(item,R)+.004,z],{'yaw_deg':yaw,'lean_deg':lean,'drop_mm':4}))
  for i,(R,c,info) in enumerate(candidates):
   p=self.pose(item,R,c);options=[]
   for branch in self.branches(p) if p['valid'] else []:
    check=self.check(branch,product=True);options.append((len(check['product_hits'])+len(check['tool_hits']),check['total_overlap_mm3'],branch,check))
   if options:_,_,p,a=min(options,key=lambda x:x[:2])
   else:a={'total_overlap_mm3':1e12,'tool_hits':[],'product_hits':[]}
   score=(not p['valid'],len(a['product_hits'])+len(a['tool_hits']),a['total_overlap_mm3'],info.get('lean_deg',0),info.get('drop_mm',0))
   row=dict(item=item,**info,ik_valid=p['valid'],position_error_mm=p['position_error_mm'],hits=len(a['tool_hits']),product_hits=len(a['product_hits']),overlap_mm3=a['total_overlap_mm3']);self.search.append(row)
   candidates[i]=(score,p,info,a)
   if i%20==0:print(item,i,'best',min(x[0] for x in candidates[:i+1]),flush=True)
  candidates.sort(key=lambda x:x[0]);best=candidates[0];print('BEST',item,best[0],best[2],flush=True)
  (OUT/(item.lower()+'_search.json')).write_text(json.dumps({'selected':best[2],'pose':best[1],'check':best[3],'trials':[r for r in self.search if r['item']==item]},indent=2))
  return best[1]

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--search',choices=['Dough','Cola','Dessert']);a=parser.parse_args();review=Review()
 if a.search:review.search_place(a.search)
