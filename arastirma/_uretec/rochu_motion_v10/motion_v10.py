"""User-specified V2 paths. Original fixed head; flexible tips only.

Scene units are metres, world Y is vertical. All approach segments are Cartesian.
Contact is a geometric proposal, never a verified load-bearing grasp.
"""
from cycles import *
from insertion_v9 import GraspProbe
from finger_bend import deform,START

class Corrected(Cycles):
 def append(self,p,*args,**kwargs):
  p=deepcopy(p)
  p['opener_lift_m']=self.opener_lift if self.item=='Dough' else 0
  return super().append(p,*args,**kwargs)

 def path(self,R,c,rail,label,held=True,n=16,shift=None,close_drawer=False,product=None):
  start=self.frames[-1]['pose'];W=np.array(start['worlds']['UR10E_body_06']);a=(W@self.relative)[:3,3]
  turn=Slerp([0,1],Rotation.from_matrix([W[:3,:3],R]));drawer=self.drawer
  for u in np.linspace(0,1,n+1)[1:]:
   u=float(u*u*(3-2*u))
   if close_drawer:self.drawer=drawer*(1-u)
   p=self.solve(turn(u).as_matrix(),a*(1-u)+np.array(c)*u,start['rail']*(1-u)+rail*u)
   if not p['valid']:raise RuntimeError(f'{self.item} {label}: {p["position_error_mm"]:.2f} mm')
   self.append(p,label,held,product=product,shift=shift,grasp_assumption=held)

 def corner_contact(self):
  # User's middle-edge grasp: centre X, outside the carton, tips overlap its lip.
  bounds=self.r.products['Box']['bounds'];c=bounds.mean(0)
  RP=Rotation.from_euler('y',180,degrees=True).as_matrix()
  contact=np.array([c[0],c[1],bounds[1,2]-.0215])
  self.corner_report={'position_m':contact.tolist(),'edge_centre_x_m':float(c[0]),'top_view_yaw_deg':180,'carton_holes':0,'mount_reversed_degrees':0,'physical_grasp_verified':False}
  (OUT/'centre_grip_v9.json').write_text(json.dumps(self.corner_report,indent=2))
  return RP,contact,-5.0

 def fit_grip(self,item,p):
  probe=GraspProbe(self.r,item);R=np.array(p['tool_orientation']);contact=np.array(p['contact']);centre=np.array(p['product'])
  samples=[]
  for shift in np.linspace(0,-11,23):
   parts=probe.measure(R,contact,centre,float(shift),tip_only=True);fingers=[x for x in parts if x['name'].startswith('OEM_DAC_')]
   samples.append((max(abs(x['penetration_mm']) for x in fingers),float(shift),parts))
  _,chosen,tip_parts=min(samples,key=lambda x:x[0]);parts=probe.measure(R,contact,centre,chosen);opened=probe.measure(R,contact,centre,0.)
  self.probe=probe;self.open_shift=0.;self.blocked=False
  self.grip_report={'contact_shift_mm':chosen,'open_shift_mm':0.,'neutral_reset_each_cycle':True,'open_max_penetration_mm':max(x['penetration_mm'] for x in opened),'fingers':[x for x in parts if x['name'].startswith('OEM_DAC_')],'distal_contacts':tip_parts,'physical_grasp_verified':False,'carrying_is_assumed':True,'selection':'Closest distal pad exterior, no scaling or root adjustment; does not establish secure grasp'}
  if item=='Dough':self.grip_report['belly']=self.belly
  (OUT/(item.lower()+'_grip_v10.json')).write_text(json.dumps(self.grip_report,indent=2));print(item,'tip shift',chosen,flush=True)
  return chosen

 def blocked_attempt(self,RP,pc,rail):
  # Preserve the requested target for inspection, but never carry an ungrasped product.
  target=deepcopy(self.pick);contact=np.array(target['contact'])
  lo,hi=0.,.080
  for _ in range(24):
   retreat=(lo+hi)/2;cp=contact-RP[:,2]*retreat
   d=self.probe.measure(RP,cp,pc,self.open_shift)
   if max(x['penetration_mm'] for x in d)>.01:lo=retreat
   else:hi=retreat
  retreat=hi+.001
  safe_c=pc-RP[:,2]*retreat
  self.path(RP,safe_c,rail,'Düz yaklaş · ilk temastan 1 mm önce dur',False,n=28,shift=self.open_shift)
  safe=deepcopy(self.frames[-1]['pose'])
  for _ in range(12):self.append(safe,'Derin giriş engelli · ürün yerinde kalıyor',False,shift=self.open_shift)
  self.path(RP,safe_c-RP[:,2]*.12,rail,'Kavrama yapılmadı · boş geri çekil',False,n=20,shift=self.open_shift)
  self.grip_report.update(stopped_before_requested_target_mm=retreat*1000,actual_lift=False)
  targets=self.probe.measure(RP,contact,pc,self.open_shift)
  hit=[{'part':'Product_'+self.item,'moving':x['name']} for x in targets if x['penetration_mm']>.05]
  inspection={'label':'İstenen derin giriş · mevcut geometride temas var','pose':target,'held':False,'product_matrix':self.product.tolist(),'check':{'native_surface_hits':hit,'not_checked':False,'method':'Product convex exterior samples; not material simulation'}}
  inspection['pose']['tip_shift_mm']=self.open_shift
  return {'key':self.item+'_cycle','frames':self.frames,'grasp_relative':self.relative.flatten().tolist(),'duration_s':14,'description':'Ortadan düz giriş. Gövde düz, yalnız kısa uç esner. Mevcut sabit montaj bu derinliğe çarpmadan giremiyor.','warning':'Derin girişte temas: kutu/tatlı kaldırılmıyor. İstenen derinlik düğmesi sorunlu hedefi gösterir. Uç eğrisi bir hareket yaklaşımıdır; üreticinin basınç altında ölçülmüş şekli değildir.','physical_grasp_verified':False,'grasp_verified':False,'grasp_blocked':True,'inspection_frame':inspection,'grip_report':self.grip_report,'measure':f"{self.grip_report['open_max_penetration_mm']:.1f} mm",'measure_label':'İstenen girişte geometrik iç içe geçme','contact_summary':f"{self.grip_report['open_max_penetration_mm']:.1f} mm temas"}

 def blocked_dough_attempt(self,RP,pc,rail):
  # The true belly target is below the silicone nest lip; keep this failed target visible.
  evidence=json.loads((OUT/'dough_requested_v9_scene_check.json').read_text())
  hits=[h for row in evidence['rows'] for h in row['hits'] if h['native_surface_crossing']]
  assert hits and all(h['fixture']=='CEK_K1_lahm_1__silikon__CEKMECE' for h in hits)
  safe_c=pc+np.array([0,.050,0])
  self.path(RP,safe_c,rail,'Dik yaklaş · silikon yuva önünde dur',False,n=20,shift=self.open_shift)
  safe=deepcopy(self.frames[-1]['pose'])
  for _ in range(12):self.append(safe,'En şişkin kesite erişim engelli · hamur yerinde',False,shift=self.open_shift)
  self.path(RP,pc+[0,.30,0],rail,'Kavrama yok · dik ve boş geri çekil',False,n=20,shift=self.open_shift)
  target=deepcopy(self.pick);target.update(tip_shift_mm=self.open_shift,drawer_open_m=.7,opener_lift_m=self.opener_lift)
  unique=sorted(set((h['fixture'],h['moving']) for h in hits))
  inspection={'label':'Gerçek en şişkin kesit · silikon yuvayla çarpışıyor','pose':target,'held':False,'product_matrix':self.product.tolist(),'check':{'native_surface_hits':[{'part':p,'moving':m} for p,m in unique],'not_checked':False,'method':evidence['scope']}}
  self.grip_report.update(requested_entry_blocked=True,fixture_blocked=True,blocking_fixture='CEK_K1_lahm_1__silikon__CEKMECE',actual_lift=False,stop_above_requested_target_mm=50)
  (OUT/'dough_grip_v9.json').write_text(json.dumps(self.grip_report,indent=2))
  return {'key':'Dough_cycle','frames':self.frames,'grasp_relative':self.relative.flatten().tolist(),'duration_s':14,'description':'Hamurun ölçülen en geniş kesiti hedeflendi. Uçlar bu kotta silikon yuvaya değiyor; hamur alınmadan dik geri çekiliniyor.','warning':'En şişkin noktadaki kavrama mevcut silikon yuva ile çakışıyor. İstenen derinlik düğmesi gerçek temas pozunu gösterir. Bırakma hareketi bu nedenle yürütülmez.','physical_grasp_verified':False,'grasp_verified':False,'grasp_blocked':True,'inspection_frame':inspection,'grip_report':self.grip_report,'measure':str(len(unique))+' uç','measure_label':'Silikon yuvaya temas eden uç','contact_summary':'Silikon yuva engeli'}

 def build(self,item):
  self.item=item;self.frames=[];self.last=None;self.drawer=0
  self.opener_lift=json.loads((OUT/'dough_v7_release_choice.json').read_text()).get('opener_lift_m',0) if item=='Dough' and (OUT/'dough_v7_release_choice.json').exists() else 0
  self.pick=deepcopy(self.review['box_support']['variants']['edge']['pose'] if item=='Box' else self.review['sequences'][item+'_pick']['frames'][0]['pose'])
  pc=np.array(self.pick['product']);RP=np.array(self.pick['tool_orientation']);rail=self.pick['rail']
  if item=='Dough':
   ps=self.r.products['Dough'];t=trimesh.Trimesh(ps['world']-ps['bounds'].mean(0),ps['faces'],process=False);sections=[]
   for y in np.linspace(t.bounds[0,1]+.00001,t.bounds[1,1]-.00001,201):
    lines=trimesh.intersections.mesh_plane(t,[0,1,0],[0,y,0])
    if len(lines):
     v=lines.reshape(-1,3);sections.append((float(np.ptp(v[:,0])),float(y),float((v[:,0].min()+v[:,0].max())/2)))
   width,y,cx=max(sections);contact=np.array(self.pick['contact']);contact[0]=pc[0]+cx;contact[1]=pc[1]+y
   self.belly={'section_count':201,'width_mm':width*1000,'relative_height_mm':y*1000,'contact_world_m':contact.tolist(),'method':'Maximum X span of201 horizontal native product sections'}
   (OUT/'dough_belly_v9.json').write_text(json.dumps(self.belly,indent=2))
   pp=solve_pose(self.r.kin,RP,contact,rail,[self.pick['q']]);pp.update({k:v for k,v in self.pick.items() if k not in pp});pp['contact']=contact.tolist();self.pick=pp
  if item=='Box':
   RP,contact,shift=self.corner_contact();p=solve_pose(self.r.kin,RP,contact,rail,[self.pick['q'],self.r.old['Box_pick']['q']]);p.update({k:v for k,v in self.pick.items() if k not in p});self.pick=p
   self.pick.update(tool_orientation=RP.tolist(),contact=contact.tolist(),tip_shift_mm=shift)
  if item in ['Cola','Dessert']:
   extra=.012 if item=='Cola' else .010
   contact=np.array(self.pick['contact'])+RP[:,2]*extra
   pp=solve_pose(self.r.kin,RP,contact,rail,[self.pick['q']]);pp.update({k:v for k,v in self.pick.items() if k not in pp});pp['contact']=contact.tolist();self.pick=pp
  self.pick['tip_shift_mm']=self.fit_grip(item,self.pick)
  self.pick.update(root_hash=self.r.definition['root_hash'],finger_roots=self.r.definition['finger_roots'])
  self.relative=np.linalg.inv(np.array(self.pick['worlds']['UR10E_body_06']))@at(pc)
  self.product=at(pc if item=='Box' else pc-[0,0,.7])
  top=pc-RP[:,2]*.20 if item=='Box' else pc+[0,.42 if item=='Cola' else .30,0]
  approach=self.solve(RP,top,rail)
  if not approach['valid']:raise RuntimeError(item+' initial approach unreachable')
  self.append(approach,'Alma noktasının önünde bekle' if item=='Box' else 'Ürünün tam üstünde bekle',False,shift=0 if item=='Box' else self.open_shift)
  if item=='Box':
   for shift in np.linspace(0,self.open_shift,9)[1:]:self.append(approach,'Ters takılmış parmakların esnek uçlarını aç',False,shift=float(shift))
  else:
   for d in np.linspace(0,.7,9)[1:]:
    self.drawer=float(d);self.product=at(pc+[0,0,d-.7]);self.append(approach,'Çekmeceyi aç · uç yukarıda sabit',False,shift=self.open_shift)
  self.path(RP,pc,rail,'Kutu kenarının ortasına düz yaklaş' if item=='Box' else 'Dik in · yana kayma yok',False,n=20,shift=self.open_shift)
  for u in np.linspace(0,1,9):self.append(self.pick,'Yalnız uçları kapat · kavrama denemesi',bool(u==1),shift=self.open_shift+(self.pick['tip_shift_mm']-self.open_shift)*u,grasp_assumption=item=='Box')
  lifted=pc+[0,{'Box':.08,'Cola':.36,'Dessert':.20,'Dough':.18}[item],0]
  self.path(RP,lifted,rail,'Dik yüksel · önce ürün çevresini temizle',n=20)
  if item!='Box':
   pp=self.frames[-1]['pose']
   for d in np.linspace(.7,0,17)[1:]:
    self.drawer=float(d);self.append(pp,'Ürün yukarıda sabit · çekmeceyi tamamen kapat',True)
  exitRail=rail-(.60 if item=='Box' else .30) if item in ['Cola','Dessert','Box'] else rail
  if exitRail!=rail:self.path(RP,lifted,exitRail,'Ürün sabit · rayı taşıma için hizala',n=14)
  rail=exitRail
  front=lifted.copy();front[2]=.82
  self.path(RP,front,rail,'Çekmece kapalı · düz dışarı taşı',n=22,close_drawer=False)
  travel=front.copy();travel[1]=max(front[1],.84)
  carryR=Rotation.from_euler('z',90,degrees=True).as_matrix() if item=='Cola' else RP
  self.path(carryR,travel,rail,'İstasyonların önünde taşıma kotuna çık',n=20)
  if item=='Dough':
   R=Rotation.from_euler('x',-20,degrees=True).as_matrix()@Rotation.from_euler('y',180,degrees=True).as_matrix()@Rotation.from_euler('z',90,degrees=True).as_matrix()
   prodR=R@RP.T;ps=self.r.products[item];v=(ps['world']-ps['bounds'].mean(0))@prodR.T
   goal=np.array([1.08611652,1.00587-v[:,1].min()+.008,-.16993615]);rr=self.r.kin.data['rail_min'];floor=1.00587
   if (OUT/'dough_v7_release_choice.json').exists():
    choice=json.loads((OUT/'dough_v7_release_choice.json').read_text());R=np.array(choice['R']);goal=np.array(choice['centre']);rr=choice['rail']
   entry=goal-R[:,2]*.34
   intermediate=entry.copy();intermediate[2]=.70
   self.path(RP,intermediate,rr,'Tablanın önüne düz hizalan',n=24)
   self.path(R,entry,rr,'Dikey eğimi ayarla · üstten bakış düz',n=18)
   self.path(R,goal,rr,'Tablaya düz hizada üst eğimle gir',n=22)
  elif item=='Cola':
   R=Rotation.from_euler('z',90,degrees=True).as_matrix();rr=4.86;floor=.85
   goal=np.array(json.loads((OUT/'cola_release_v8.json').read_text())['centre']);entry=goal+[0,.02,-.32]
   transfer=entry.copy();transfer[2]=.82
   self.path(R,transfer,rr,'Rafın önüne taşı · ürün yatay',n=30)
   self.path(R,entry,rr,'Rafın dışında kolayı yatay yatır',n=20)
   self.path(R,goal,rr,'Sağ duvara yakın düz raf girişi',n=22)
  elif item=='Dessert':
   choice=json.loads((OUT/'dessert_release_v8.json').read_text());R=np.array(choice['R']);rr=choice['rail'];floor=.85;goal=np.array(choice['centre']);entry=goal+[0,.005,-.24]
   self.path(R,entry,rr,'Tatlıyı raf dışında öne 30° eğ · üstten bakış düz',n=32)
   self.path(R,goal,rr,'Üst rafa değmeden düz bırakma yaklaşımı',n=22)
  else:
   # Half-turn puts the gripped edge on the robot side at the destination.
   prodR=Rotation.from_euler('y',180,degrees=True).as_matrix();R=prodR@RP;rr=4.86;floor=.85
   ps=self.r.products[item];v=(ps['world']-ps['bounds'].mean(0))@prodR.T
   goal=np.array([4.909,floor-v[:,1].min()+.045,1.912]);entry=goal+[0,.025,-.36]
   self.path(R,entry,rr,'Kutu elde · rafın önünde yönlen',n=30)
   self.path(R,goal,rr,'Kutuyu düz hizada eğimli bırakma yerine getir',n=22)
  end=np.array(self.frames[-1]['product_matrix']);p=self.frames[-1]['pose']
  for u in np.linspace(0,1,9):self.append(p,'Yalnız uçları aç · ürünü bırak',bool(u<1),product=end,shift=self.pick['tip_shift_mm']+(self.open_shift-self.pick['tip_shift_mm'])*u,grasp_assumption=item=='Box')
  ps=self.r.products[item];v=(ps['world']-ps['bounds'].mean(0))@end[:3,:3].T;fall=max(0,end[1,3]+v[:,1].min()-floor)
  for u in np.linspace(0,1,7)[1:]:
   final=end.copy();final[1,3]-=fall*u
   if item=='Dessert':
    final[:3,:3]=Slerp([0,1],Rotation.from_matrix([end[:3,:3],np.eye(3)]))(u).as_matrix()
    vv=(ps['world']-ps['bounds'].mean(0))@final[:3,:3].T;final[1,3]=floor-vv[:,1].min()+fall*(1-u)
   self.append(p,'Kısa bırakma · fiziksel deney gerekli',False,product=final,shift=self.open_shift)
  retract=goal-R[:,2]*.34 if item=='Dough' else goal+[0,.035,-.28]
  self.path(R,retract,rr,'Ucu geri çek · ürün bırakıldı',False,n=22,shift=self.open_shift,product=final)
  qs=np.array([f['pose']['q'] for f in self.frames]);limits=[]
  for k in range(6):
   low,high=qs[:,k].min(),qs[:,k].max();off=next((n*2*np.pi for n in [0,1,-1,2,-2] if low+n*2*np.pi>=-2*np.pi-1e-6 and high+n*2*np.pi<=2*np.pi+1e-6),None)
   if off is None:raise RuntimeError(item+' joint limits')
   qs[:,k]+=off;limits.append([float(qs[:,k].min()),float(qs[:,k].max())])
  for f,q in zip(self.frames,qs):f['pose']['q']=q.tolist()
  notes={'Dough':'Dik in, dik çık; çekmece kapandıktan sonra düz hizadan, kabul edilen 20° üst eğimle bırak.','Cola':'Dik in, dik çık; raf dışında yatay dön, sağ duvara yakın bırak.','Dessert':'Dik in, dik çık; raf girişinde öne 30° eğ, kolanın robot tarafına bırak. Serbest bırakıldıktan sonra dik oturma hareketi kinematik gösterimdir.','Box':'Deliksiz kutu. Ön kenarın tam ortasına düz yaklaşım. Dört modül V9 yönüne göre tekrar 180° çevrildi; taşıma sırasında bağlantılar sabit.'}
  if item=='Dough' and self.opener_lift:notes[item]+=f' Açıcı için +{self.opener_lift*1000:.0f} mm açıklık denemesi; mevcut mekanizmanın bu stroku doğrulanmış değil.'
  return {'key':item+'_cycle','frames':self.frames,'grasp_relative':self.relative.flatten().tolist(),'joint_ranges_rad':limits,'duration_s':28,'description':notes[item],'warning':'Tam hareket gösterimi: temaslarda devam eder. Ürünün tutulup taşınması varsayımdır; fiziksel kavrama ve çarpışmasızlık onayı değildir.','physical_grasp_verified':False,'grasp_verified':False,'conceptual_motion':True,'contacts_do_not_stop':True,'grip_report':self.grip_report,'measure':str(len(self.frames)),'measure_label':'Animasyon adımı','contact_summary':'Kenar ortası · tutuş denemesi' if item=='Box' else None}

if __name__=='__main__':
 maker=Corrected();data={'version':10,'root_hash':maker.r.definition['root_hash'],'source':'V10 original orientation restored; neutral reset; full conceptual paths continue through contacts by user request','physical_grasp_verified':False,'continuous_path_verified':False,'sequences':{}}
 import sys
 for item in (sys.argv[1:] or ['Dough','Cola','Dessert','Box']):
  seq=maker.build(item);data['sequences'][seq['key']]=seq
  (OUT/(item.lower()+'_v10_candidate.json')).write_text(json.dumps(seq,separators=(',',':')))
  print(item,len(seq['frames']),'frames exported',flush=True)
 if len(data['sequences'])==4:(OUT/'cycles.json').write_text(json.dumps(data,separators=(',',':')))
