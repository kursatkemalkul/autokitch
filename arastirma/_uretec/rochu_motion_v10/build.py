"""Local, fixed-mount ROCHU review. OEM CAD is never rescaled to fit a product."""
from model import *
import gzip,hashlib,trimesh
from scipy.optimize import least_squares

WR='/World/RailSystem/Arm/wrist_3_link'
RADIUS=.0343
ANGLES=[45,135,225,315]
TIP=.1097
def mesh(v,f,color):
 t=trimesh.Trimesh(v,f,process=False)
 t.visual=trimesh.visual.ColorVisuals(t,vertex_colors=(np.array(color)*255).astype(np.uint8))
 return t
def save_scene(scene,name):
 raw=scene.export(file_type='glb');(OUT/(name+'.glb.gz')).write_bytes(gzip.compress(raw,compresslevel=6,mtime=0))
def ident(t):
 w=np.eye(4);w[:3,3]=t;return w
def make_head():
 cad=json.loads((H/'cad_meshes.json').read_text());head=trimesh.Scene();parts=[]
 def add(name,v,f,color,parent='world',transform=None):
  t=mesh(v,f,color);head.add_geometry(t,node_name=name,geom_name=name,parent_node_name=parent,transform=np.eye(4) if transform is None else transform);parts.append(dict(name=name,mesh=t,parent=parent,transform=np.eye(4) if transform is None else transform))
 a=cad['adapter'];b=np.array(a['bounds']);centre=b.mean(0);rot=np.array([[1,0,0],[0,0,-1],[0,1,0]])
 for i,p in enumerate(a['pieces']):
  v=(np.array(p['vertices'])-[centre[0],b[0,1],centre[2]])@rot.T*.001
  add('OEM_FCM_R01_'+str(i),v,p['faces'],[.68,.73,.78,1])
 # Catalog SMP-4S outline, adapted to DAC M14 fixing slots.
 add('PROPOSED_DAC_short_star',np.array(cad['dac_plate']['vertices'])*.001+[0,0,.055],cad['dac_plate']['faces'],[1,.48,.14,1])
 add('PROPOSED_spacer_9mm',np.array(cad['spacer']['vertices'])*.001+[0,0,.042],cad['spacer']['faces'],[1,.48,.14,1])
 for name,radius,height,z in [('M8_shank',.004,.030,.045),('M8_head',.0065,.0053,.06265),('M8_washer',.008,.001,.0595)]:
  t=trimesh.creation.cylinder(radius=radius,height=height,sections=24);add(name,t.vertices+[0,0,z],t.faces,[.62,.65,.69,1])
 b=np.array(cad['module']['bounds']);stem=np.array([*b.mean(0)[:2],b[1,2]])
 roots=[]
 for i,angle in enumerate(ANGLES):
  theta=np.deg2rad(angle);root=np.eye(4);root[:3,:3]=Rotation.from_rotvec([0,0,theta+np.pi]).as_matrix();root[:3,3]=[RADIUS*np.cos(theta),RADIUS*np.sin(theta),.073];roots.append(root.tolist())
  parent='Finger_'+str(i);head.graph.update(frame_to=parent,matrix=root)
  p=cad['module']['pieces'][0];v=(np.array(p['vertices'])-stem)*[1,-1,-1]*.001-[0,0,.006]
  add('OEM_DAC_'+str(i),v,p['faces'],[.24,.28,.31,1],parent)
  add('CATALOG_CM_'+str(i),np.array(cad['dac_connector']['vertices'])*.001*[1,1,-1],cad['dac_connector']['faces'],[.66,.72,.77,1],parent)
 save_scene(head,'fixed_head')
 definition=dict(radius_mm=RADIUS*1000,angles_deg=ANGLES,finger_roots=roots,root_z_mm=73,tcp_from_wrist_mm=TIP*1000,tip_inner_face_outward_from_stem_mm=8.5,neutral_diameter_mm=2*RADIUS*1000+17,tip_vacuum_approx_mm=-11,tip_pressure_approx_mm=5,plate_outline_mm=102,plate_thickness_mm=8,slot_centres_mm=[20,42],source_steps={k:cad[k]['sha256'] for k in ['module','adapter']},module_count=4,scale=0.001,plate_is_our_proposal=True,complete_supplier_assembly=False,physical_grasp_verified=False,soft_deformation_is_illustrative=True)
 definition['root_hash']=hashlib.sha256(json.dumps(roots,separators=(',',':')).encode()).hexdigest()
 definition.update(recommended_module='DAC-1G3527',supplied_STEP_filename='BMC-1G3527_SN四级.step',supplier_confirmation_of_STEP_variant_required=True,source_module_bbox_mm=(np.array(cad['module']['bounds'])[1]-np.array(cad['module']['bounds'])[0]).tolist(),gripping_face='Source +X flat face inward, catalog vacuum-clamping diagram',pressure_displacement_not_force_simulation=True,positive_inner_tip_opening_inferred_from_outer_tip_graph=True,air_hoses_not_modelled=True,connector_nut_and_thread_details_are_approximate=True,previous_outward_gripping_face_layout_rejected=True)
 (OUT/'head_definition.json').write_text(json.dumps(definition,indent=2))
 return head,definition
def node_body(m,i):
 while True:
  n=m.j['nodes'][i].get('name','')
  if n.startswith('UR10E_body_') and len(n)==13 and n[-2:].isdigit():return i,n
  if i not in m.parents:return None,None
  i=m.parents[i]
def make_focus(m):
 scene=trimesh.Scene();metadata=[];count=0
 for s in m.shapes:
  n=s['name'];bi,bn=node_body(m,s['id']);keep=(n.startswith(('QR62_','CEK_','A_AGIZ','ROBOT25_IGUS_','ROBOT25_RAY_','ROBOT25_UR_KONTROL_KUTUSU','ROBOT25_KONTROL_KUTUSU_KAIDE')) or 'ACICI' in n or 'DONER__TABLA' in n or n.startswith('ROBOT25_PRODUCT') or n.startswith('ROBOT25_') and 'stock_shape' in n or bn is not None)
  # Include native box-stage components without rebuilding the E station.
  if n.startswith('E_') and np.all(s['bounds'][1]>[4.3,.85,-.5]) and np.all(s['bounds'][0]<[5.0,1.2,.3]):keep=True
  if n=='A_ONYUZ__on_seffaf':keep=True
  if not keep or bn and 8<=int(bn[-2:])<=16:continue
  group='Static';parent=np.eye(4);v=s['world']
  if bn:
   group=bn;parent=m.matrix(bi);v=(v-parent[:3,3])@parent[:3,:3]
  elif 'ACICI' in n:group='Opener'
  elif n.startswith('CEK_') and '__CEKMECE' in n and '__CEKMECE_ARA' not in n:
   group='Drawer_'+('Dough' if n.startswith('CEK_K1') else 'Cola' if n.startswith('CEK_K5') else 'Dessert')
  elif 'stock_shape' in n or n.startswith('ROBOT25_PRODUCT'):
   key=n.split('_')[1] if 'stock_shape' in n else n.split('_')[2];group='Product_'+key;parent=ident(s['bounds'].mean(0));v=s['world']-parent[:3,3]
  if group not in scene.graph.nodes:scene.graph.update(frame_to=group,matrix=parent)
  key='N_'+str(count);scene.add_geometry(mesh(v,s['faces'],s['color']),node_name=key,geom_name=key,parent_node_name=group)
  metadata.append(dict(node=key,source=n,group=group,bounds=s['bounds'].tolist(),vertices=len(v),faces=len(s['faces'])));count+=1
 save_scene(scene,'focus')
 (OUT/'focus_manifest.json').write_text(json.dumps(metadata,indent=2))
 print('FOCUS',count,'triangles',sum(x['faces']for x in metadata),flush=True)
 return metadata
def solve_pose(kin,R,tcp,rail,seeds):
 target=ident(tcp);target[:3,:3]=R;target[:3,3]-=R@np.array([0,0,TIP]);best=None
 def error(q):
  w=kin.worlds(q,rail)[WR];return np.r_[w[:3,3]-target[:3,3],Rotation.from_matrix(target[:3,:3].T@w[:3,:3]).as_rotvec()*.35]
 for seed in seeds:
  seed=np.arctan2(np.sin(seed),np.cos(seed));fit=least_squares(error,seed,bounds=(-2*np.pi,2*np.pi),max_nfev=200,xtol=1e-10,ftol=1e-10,gtol=1e-10);score=np.linalg.norm(fit.fun)
  if best is None or score<best[0]:best=(score,fit.x)
  if score<1e-6:break
 q=best[1];e=error(q);return dict(q=q.tolist(),rail=rail,position_error_mm=np.linalg.norm(e[:3])*1000,angle_error_deg=np.rad2deg(np.linalg.norm(e[3:])/.35),valid=bool(np.linalg.norm(e[:3])<.002 and np.linalg.norm(e[3:])/.35<np.deg2rad(.5)),worlds={kin.data['body_nodes'][k].replace('body','UR10E_body'):v.tolist() for k,v in kin.worlds(q,rail).items() if k in kin.data['body_nodes']})
def make_poses(m,definition):
 order=json.loads((ROOT/'otonom/hat3d/robot-integrated-v28/order_v28.json').read_text());kin=Kin();seeds=[order['trajectory'][0]['state']['q'],[2.4,-1.3,1.5,-1.8,4.7,.9],[0,-1,1.8,-1.4,1.57,0],[3,-1.6,1.5,-1.5,-1.57,0]]
 R=Rotation.from_rotvec([np.pi/2,0,0]).as_matrix();RB=Rotation.from_rotvec([0,np.pi,0]).as_matrix();centres={};shapes={}
 for k in ['Dough','Cola','Dessert','Box']:
  s=next(s for s in m.shapes if s['name']==('ROBOT25_PRODUCT_Box' if k=='Box' else 'ROBOT25_'+k+'_stock_shape'));centres[k]=s['bounds'].mean(0);shapes[k]=s
 poses={};final=order['summary']['final_positions_m']
 for k in centres:
  diameter=max(shapes[k]['bounds'][1][[0,2]]-shapes[k]['bounds'][0][[0,2]])*1000 if k!='Box' else 45
  for mode in ['pick','place']:
   c=centres[k].copy() if mode=='pick' else np.array(final[k]);draw=0.7 if mode=='pick' and k!='Box' else 0
   c[2]+=draw
   # Same dough tool orientation at pickup and table; use the widest belly.
   contact=c.copy();pressure=(diameter-definition['neutral_diameter_mm'])/2
   if k=='Box':
    contact=c.copy();contact[2]+=.1496;pressure=45/np.sqrt(2)-(RADIUS*1000+8.5)
   elif k=='Dough':contact[1]=c[1]-(centres[k][1]-shapes[k]['bounds'][0,1])+.0065
   elif k in ['Cola','Dessert']:contact[1]=c[1]+(shapes[k]['bounds'][1,1]-centres[k][1])-(.0045 if k=='Cola' else .006)
   rail=1.715 if k=='Dough' else 2.95 if k=='Cola' and mode=='pick' else 3.65 if k=='Dessert' and mode=='pick' else 4.86
   if k=='Dough' and mode=='place':rail=kin.data['rail_min']
   orientation=RB if k=='Box' and mode=='pick' else np.eye(3) if k=='Box' else R
   if k=='Box' and mode=='place':contact[2]=c[2]-.1496
   p=solve_pose(kin,orientation,contact,rail,seeds)
   p.update(item=k,mode=mode,product=c.tolist(),contact=contact.tolist(),tip_shift_mm=float(pressure),diameter_mm=diameter,drawer_open_m=draw,root_hash=definition['root_hash'],finger_roots=definition['finger_roots'],tool_orientation=orientation.tolist(),stand_raise_mm=0)
   poses[k+'_'+mode]=p;print(k,mode,'IK',p['valid'],p['position_error_mm'], 'tip mm',pressure,flush=True)
 for mode in ['pick','place']:
  old=poses['Dough_'+mode];orientation=Rotation.from_rotvec([np.deg2rad(135),0,0]).as_matrix();p=solve_pose(kin,orientation,old['contact'],old['rail'],seeds)
  p.update({k:v for k,v in old.items() if k not in ['q','rail','position_error_mm','angle_error_deg','valid','worlds']});p['tool_orientation']=orientation.tolist();p['trial_tilt_deg']=45
  poses['Dough_tilt_'+mode]=p;print('Dough tilt',mode,p['valid'],p['position_error_mm'],flush=True)
 (OUT/'poses.json').write_text(json.dumps(poses,indent=2));return poses
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True);head,definition=make_head();m=Model();manifest=make_focus(m);poses=make_poses(m,definition)
