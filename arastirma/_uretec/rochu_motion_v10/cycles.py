from finger_bend import deform
"""Join existing native-FK pickup and release poses into four visible cycles.

New transfer samples use conservative bounds warnings, not a collision/force
certificate. Existing V2 release failures stay visible. No station CAD is rebuilt.
"""
from v2 import *
import itertools
from carton import create_carton

def at(centre,rotation=None):
 w=ident(centre)
 if rotation is not None:w[:3,:3]=rotation
 return w

def corners(bounds):return np.array(list(itertools.product(*zip(*bounds))))

class Cycles:
 def __init__(self):
  self.r=Review();self.review=json.loads((OUT/'review.json').read_text());self.frames=[];self.last=None
  manifest=json.loads((OUT/'focus_manifest.json').read_text());names={x['source'] for x in manifest if not x['group'].startswith(('UR10E','Product_'))}
  self.fixtures=[s for s in self.r.m.shapes if s['name'] in names and not s['name'].startswith(('ROBOT25_','UR10E'))]
  self.arm_bounds=[]
  for s in self.r.arm:
   bi,bn=node_body(self.r.m,s['id']);old=self.r.m.matrix(bi);v=(s['world']-old[:3,3])@old[:3,:3];self.arm_bounds.append((bn,s['name'],corners([v.min(0),v.max(0)])))
  self.head_bounds={}
  self.carton,self.box_original,self.box_contact,self.carton_solid=create_carton(self.r)
  self.fixtures=[s for s in self.fixtures if not s['name'].startswith(('A_AGIZ','A_ONYUZ'))]

 def solve(self,R,c,rail):
  contact=np.array(c)-R@self.relative[:3,3]+R@np.array([0,0,TIP])
  p=solve_pose(self.r.kin,R,contact,rail,[self.last if self.last is not None else self.pick['q'],self.pick['q'],self.r.old[self.item+'_place']['q'],[0,-1,1.8,-1.4,1.57,0],[3,-1.6,1.5,-1.5,-1.57,0]])
  if self.last is not None:p['q']=(np.array(self.last)+np.arctan2(np.sin(np.array(p['q'])-self.last),np.cos(np.array(p['q'])-self.last))).tolist()
  p.update(item=self.item,mode='cycle',contact=contact.tolist(),product=np.array(c).tolist(),tool_orientation=R.tolist(),tip_shift_mm=self.pick['tip_shift_mm'],drawer_open_m=self.drawer,root_hash=self.r.definition['root_hash'],finger_roots=self.r.definition['finger_roots'])
  return p

 def broad_check(self,p,product):
  pressure=round(p['tip_shift_mm'],6)
  if pressure not in self.head_bounds:
   parts=[]
   for name in self.r.head.graph.nodes_geometry:
    w,g=self.r.head.graph[name];t=self.r.head.geometry[g];v=t.vertices.copy()
    if name.startswith('OEM_DAC_'):
     v=deform(v,pressure)
    v=v@w[:3,:3].T+w[:3,3];parts.append((name,corners([v.min(0),v.max(0)])))
   self.head_bounds[pressure]=parts
  W=np.array(p['worlds']['UR10E_body_06']);moving=[]
  for name,v in self.head_bounds[pressure]:
   v=v@W[:3,:3].T+W[:3,3];moving.append((name,np.array([v.min(0),v.max(0)])))
  for bn,name,v in self.arm_bounds:
   w=np.array(p['worlds'][bn]);v=v@w[:3,:3].T+w[:3,3];moving.append((name,np.array([v.min(0),v.max(0)])))
  ps=self.r.products[self.item];v=(ps['world']-ps['bounds'].mean(0))@product[:3,:3].T+product[:3,3];pb=np.array([v.min(0),v.max(0)])
  hits=[];ph=[];seen=set()
  for s in self.fixtures:
   b=s['bounds'].copy();name=s['name']
   prefix={'Dough':'CEK_K1','Cola':'CEK_K5','Dessert':'CEK_K6'}.get(self.item)
   if prefix and name.startswith(prefix) and '__CEKMECE' in name and '__CEKMECE_ARA' not in name:b[:,2]+=p['drawer_open_m']
   for moving_name,mb in moving:
    if np.all(np.minimum(b[1],mb[1])-np.maximum(b[0],mb[0])>0.0002):
     key=(name,moving_name)
     if key not in seen:hits.append({'part':name,'moving':moving_name,'bounds_only':True});seen.add(key)
   if np.all(np.minimum(b[1],pb[1])-np.maximum(b[0],pb[0])>0.0002) and name not in ph:ph.append(name)
  return {'ik_valid':p['valid'],'tool_hits':hits,'product_hits':[{'part':x,'bounds_only':True} for x in ph],'not_checked':True,'method':'Conservative native mesh bounds candidates only. Holes/slots and curved spaces are not resolved by bounds. No continuous collision or secure grasp qualification.'}

 def append(self,p,label,held,product=None,check=None,shift=None,grasp_assumption=False):
  p=deepcopy(p);p['drawer_open_m']=self.drawer
  if shift is not None:p['tip_shift_mm']=shift
  if self.last is not None:
   p['q']=(np.array(self.last)+np.arctan2(np.sin(np.array(p['q'])-self.last),np.cos(np.array(p['q'])-self.last))).tolist()
  self.last=np.array(p['q']);W=np.array(p['worlds']['UR10E_body_06']);product=W@self.relative if held else self.product if product is None else product
  p['product']=product[:3,3].tolist();p['product_rotation']=product[:3,:3].tolist()
  self.frames.append({'label':label,'pose':p,'held':held,'product_matrix':product.tolist(),'check':check if check is not None else self.broad_check(p,product),'grasp_assumption':grasp_assumption})

 def native(self,q,rail,shift=None):
  worlds=self.r.kin.worlds(q,rail);W=worlds[WR];R=W[:3,:3]
  return dict(q=np.array(q).tolist(),rail=float(rail),worlds={self.r.kin.data['body_nodes'][k].replace('body','UR10E_body'):v.tolist() for k,v in worlds.items() if k in self.r.kin.data['body_nodes']},position_error_mm=0,angle_error_deg=0,valid=True,ik_target=False,route='Native joint interpolation; not a collision-checked trajectory',item=self.item,tool_orientation=R.tolist(),product=(W@self.relative)[:3,3].tolist(),contact=(W@np.array([0,0,TIP,1]))[:3].tolist(),tip_shift_mm=self.pick['tip_shift_mm'] if shift is None else shift,drawer_open_m=self.drawer,root_hash=self.r.definition['root_hash'],finger_roots=self.r.definition['finger_roots'])

 def move(self,to,label,held=True,n=10,product=None,shift=None):
  if not to['valid']:raise RuntimeError(self.item+' unreachable endpoint '+label+' '+str(to['position_error_mm']))
  start=self.frames[-1]['pose'];qa=np.array(start['q']);qb=qa+np.arctan2(np.sin(np.array(to['q'])-qa),np.cos(np.array(to['q'])-qa))
  for u in np.linspace(0,1,n+1)[1:]:
   u=float(u*u*(3-2*u));q=qa+(qb-qa)*u;p=self.native(q,start['rail']+(to['rail']-start['rail'])*u,shift)
   self.append(p,label,held,product=product,shift=shift,grasp_assumption=self.item=='Box')

 def nearby(self,R,c,rail,offsets):
  for delta in offsets:
   p=self.solve(R,np.array(c)+delta,rail)
   if p['valid']:return p
  raise RuntimeError(self.item+' no reachable nearby point')

 def straight(self,R,start,end,rail,label,held,n=12,shift=None):
  for u in np.linspace(0,1,n+1)[1:]:
   p=self.solve(R,np.array(start)*(1-u)+np.array(end)*u,rail)
   if not p['valid']:raise RuntimeError(self.item+' straight segment unreachable '+label)
   self.append(p,label,held,shift=shift,grasp_assumption=self.item=='Box')

 def release_new(self,R,centre,rail,floor):
  if self.item=='Dough':
   entry_c=centre-R[:,2]*.28
   horizontal=Rotation.from_euler('y',150,degrees=True).as_matrix()@Rotation.from_euler('z',90,degrees=True).as_matrix()
   level_entry=self.solve(horizontal,entry_c,rail)
   self.move(level_entry,'Rayda taşı · A girişinin önünde yatay bekle',n=18)
   turn=Slerp([0,1],Rotation.from_matrix([horizontal,R]))
   for u in np.linspace(0,1,11)[1:]:
    p=self.solve(turn(u).as_matrix(),entry_c,rail)
    if not p['valid']:raise RuntimeError('Dough upper entry turn unreachable')
    self.append(p,'Üstten çapraz dön · ürün elde',True)
   for distance in np.linspace(.28,0,15)[1:]:
    p=self.solve(R,centre-R[:,2]*distance,rail)
    if not p['valid']:raise RuntimeError('Dough axis approach unreachable')
    self.append(p,'Bırakma yerine üst çapraz eksende gir · ürün elde',True)
  else:
   entry=self.nearby(R,centre,rail,[[0,.04,-.10],[0,.02,-.06],[0,0,0]])
   self.move(entry,'Üstten çapraz yaklaş · ürün elde',n=16)
   goal=self.solve(R,centre,rail);self.move(goal,'Bırakma yerine gir · ürün elde',n=12)
  end=np.array(self.frames[-1]['product_matrix']);p=self.frames[-1]['pose']
  for u in [0,.25,.5,.75,1]:self.append(p,'Dört parmağı aç · ürünü bırak',u<1,product=end,shift=self.pick['tip_shift_mm']+(5-self.pick['tip_shift_mm'])*u,grasp_assumption=self.item=='Box')
  ps=self.r.products[self.item];v=(ps['world']-ps['bounds'].mean(0))@end[:3,:3].T;fall=max(0,end[1,3]+v[:,1].min()-floor)
  for u in [.25,.5,.75,1]:
   pm=end.copy();pm[1,3]-=fall*u;self.append(p,'Kısa bırakma · fizik deneyi gerekli',False,product=pm,shift=5,grasp_assumption=self.item=='Box')

 def build(self,item):
  self.item=item;self.frames=[];self.last=None;self.drawer=0
  self.pick=deepcopy(self.review['box_support']['variants']['edge']['pose'] if item=='Box' else self.review['sequences'][item+'_pick']['frames'][0]['pose'])
  pc=np.array(self.pick['product']);RP=np.array(self.pick['tool_orientation']);self.product=at(pc)
  if item=='Box':
   # Same exterior corner as the inspected scene. Original module roots stay fixed.
   sample=json.loads((OUT/'box_reverse_check.json').read_text())['best_clear_sample']['original']
   W=np.array(sample['wrist_matrix']);RP=W[:3,:3];contact=(W@np.array([0,0,TIP,1]))[:3]
   raw=solve_pose(self.r.kin,RP,contact,self.pick['rail'],[self.pick['q'],self.r.old['Box_pick']['q']])
   raw.update({k:v for k,v in self.pick.items() if k not in raw});self.pick=raw
   self.pick.update(contact=contact.tolist(),tool_orientation=RP.tolist(),root_hash=self.r.definition['root_hash'],finger_roots=self.r.definition['finger_roots'],tip_shift_mm=json.loads((OUT/'tip_bend_corner_contact.json').read_text())['selected_shift_mm'])
  self.relative=np.linalg.inv(np.array(self.pick['worlds']['UR10E_body_06']))@self.product
  if not self.pick['valid']:raise RuntimeError(item+' pickup IK invalid')
  approach=self.solve(RP,pc-RP[:,2]*.10,self.pick['rail']) if item=='Box' else self.nearby(RP,pc,self.pick['rail'],[[0,.06,.06],[0,.03,.03],[0,0,0]])
  if item!='Box':self.product=at(pc-[0,0,.7])
  if item=='Box':
   for shift in np.linspace(0,5,9):self.append(approach,'Gövde sabit · yalnız esnek uçları ters yönde aç',False,shift=float(shift))
  else:self.append(approach,'Alma noktasına yaklaş · uç açık',False,shift=5)
  if item!='Box':
   for d in np.linspace(0,.7,6):
    self.drawer=float(d);self.product=at(pc+[0,0,d-.7]);self.append(approach,'Çekmeceyi aç',False,shift=5)
  if item=='Box':self.straight(RP,pc-RP[:,2]*.10,pc,self.pick['rail'],'Deliksiz kutunun aynı dış köşesine yaklaş',False,n=16,shift=5)
  else:self.move(self.pick,'Açık uçla ürüne yaklaş',False,n=7,shift=5)
  for u in [0,.25,.5,.75,1]:self.append(self.pick,'Dört parmağı kapat · kavra',u==1,shift=5+(self.pick['tip_shift_mm']-5)*u,grasp_assumption=item=='Box')
  if item=='Box':
   lifted=pc+np.array([0,.13,0]);self.straight(RP,pc,lifted,self.pick['rail'],'Kutuyu önce dik kaldır · tutuş varsayımı',True,n=12)
   self.straight(RP,lifted,lifted-RP[:,2]*.10,self.pick['rail'],'Köşeden dışarı çık · kutu elde',True,n=12)
  else:
   back=self.nearby(RP,pc,self.pick['rail'],[[0,0,.12],[0,0,.08],[0,0,.04],[0,0,0]])
   self.move(back,'Ürünü geriye çek',n=8)
   carry=self.nearby(RP,np.array(back['product']),self.pick['rail'],[[0,.10,0],[0,.06,0],[0,.03,0],[0,0,0]])
   self.move(carry,'Ürünü kaldır · ürün elde',n=8)
  if item!='Box':
   for d in np.linspace(.7,0,5)[1:]:self.drawer=float(d);self.append(self.frames[-1]['pose'],'Çekmeceyi kapat · ürün elde',True)
  if item=='Dough':
   # Tool points diagonally DOWN, so wrist is ABOVE the held dough.
   R=Rotation.from_euler('x',-20,degrees=True).as_matrix()@Rotation.from_euler('y',150,degrees=True).as_matrix()@Rotation.from_euler('z',90,degrees=True).as_matrix()
   prodR=R@RP.T;ps=self.r.products[item];v=(ps['world']-ps['bounds'].mean(0))@prodR.T
   centre=np.array([1.08611652,1.00587-v[:,1].min()+.008,-.16993615]);rail=self.r.kin.data['rail_min']
   self.release_new(R,centre,rail,1.00587)
  elif item=='Box':
   R=Rotation.from_euler('y',170,degrees=True).as_matrix()@Rotation.from_euler('x',10,degrees=True).as_matrix()@RP;rail=4.86
   prodR=R@RP.T;ps=self.r.products[item];v=(ps['world']-ps['bounds'].mean(0))@prodR.T
   centre=np.array([4.913,.85-v[:,1].min()+.006,1.912])
   self.release_new(R,centre,rail,.85)
  else:
   release=self.review['sequences'][item+'_place'];rail=release['frames'][0]['pose']['rail']
   self.move(release['frames'][0]['pose'],'Rayda taşı ve bırakma yönüne dön · ürün elde',n=22)
   for f in release['frames']:
    self.append(f['pose'],f['label'],f['held'],product=np.array(f['product_matrix']),check=f['check'])
  final=np.array(self.frames[-1]['product_matrix']);endp=deepcopy(self.frames[-1]['pose']);endR=np.array(endp['tool_orientation']);endc=(np.array(endp['worlds']['UR10E_body_06'])@self.relative)[:3,3]
  if item=='Dough':
   for distance in np.linspace(0,.28,15)[1:]:
    p=self.solve(endR,endc-endR[:,2]*distance,rail)
    if not p['valid']:raise RuntimeError('Dough axis retreat unreachable')
    self.append(p,'Ucu üst çapraz eksende geri çek · ürün bırakıldı',False,product=final,shift=5)
  else:
   direction=[0,.035,-.10]
   out=self.nearby(endR,endc,rail,[direction,np.array(direction)*.5,[0,0,0]])
   self.move(out,'Ucu geri çek · ürün bırakıldı',False,n=8,product=final,shift=5)
  # Equivalent global whole-turn rebase, preserving every FK pose and continuity.
  qs=np.array([f['pose']['q'] for f in self.frames]);limits=[]
  for k in range(6):
   low,high=qs[:,k].min(),qs[:,k].max();offset=next((n*2*np.pi for n in [0,1,-1,2,-2] if low+n*2*np.pi>=-2*np.pi-1e-6 and high+n*2*np.pi<=2*np.pi+1e-6),None)
   if offset is None:raise RuntimeError(item+' joint path exceeds range '+str(k))
   qs[:,k]+=offset;limits.append([float(qs[:,k].min()),float(qs[:,k].max())])
  for f,q in zip(self.frames,qs):f['pose']['q']=q.tolist();f['pose'].pop('joint_limit_exceeded',None)
  warnings={'Dough':'Mevcut rayın yakın konumunda üstten 20° çapraz bırakma. A giriş kapağı kaldırıldı; açıcı korundu. Üst çapraz dönüş, giriş, açılma ve geri çekilme denetimi ayrı ölçüm kaydındadır; bütün yol ve fiziksel kavrama onaylanmış değil.','Cola':'Yatay bırakma. Gerçek tutma ve darbe hesabı değildir.','Dessert':'Tatlı kolanın robot tarafına çapraz bırakılır; kabın eğimli durması ve düz oturma sorunu sürüyor.','Box':'Kapalı kartonda dört gerçek giriş kesiği. Kutu taşıması varsayımsaldır; dört ucun güvenli sıkması, karton dayanımı ve 1 kg taşıması doğrulanmadı.'}
  if item=='Box':warnings[item]='Deliksiz kutu, aynı dış köşe. Bağlantılar ve gövdeler sabit; yalnız esnek uçlar açılıp kapanır. 20 mm köşe yaklaşımı. Tutuş ve karton dayanımı fiziksel olarak doğrulanmadı.'
  return {'key':item+'_cycle','frames':self.frames,'grasp_relative':self.relative.flatten().tolist(),'joint_ranges_rad':limits,'duration_s':24,'description':'Ucu aç → aynı köşeye yaklaş → kavra → dik kaldır → taşı → bırak.','warning':warnings[item]+' Yeni yol yalnız görsel hareket denemesidir; sınır kutusu adayları kesin çarpışma sonucu değildir.','grasp_verified':False,'measure':str(len(self.frames)),'measure_label':'Animasyon adımı','contact_summary':'Dış köşe · deliksiz' if item=='Box' else None,'physical_grasp_verified':False}

if __name__=='__main__':
 maker=Cycles();out={'version':4,'source':'Published V2 with unchanged OEM head and existing native FK; native rail min used for upper dough release','root_hash':maker.r.definition['root_hash'],'continuous_path_verified':False,'physical_grasp_verified':False,'sequences':{}}
 for item in ['Dough','Cola','Dessert','Box']:
  s=maker.build(item);out['sequences'][s['key']]=s;print(item,len(s['frames']),'frames','invalid IK',sum(not f['pose']['valid'] for f in s['frames']),flush=True)
 (OUT/'cycles.json').write_text(json.dumps(out,separators=(',',':')));print('CYCLES EXPORTED',flush=True)
