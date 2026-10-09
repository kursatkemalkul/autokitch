from finger_bend import deform
"""Discrete local clearance audit; not a force or continuous-motion certificate."""
from build import *
import manifold3d as md,io
def solid(vertices,faces):
 t=trimesh.Trimesh(vertices,faces,process=True);t.merge_vertices();t.fix_normals();a=md.Manifold(md.Mesh(np.array(t.vertices,dtype=np.float32),np.array(t.faces,dtype=np.uint32)))
 if a.status()==md.Error.NoError:return a,0
 pieces=[];hulls=0
 for p in t.split(only_watertight=False):
  a=md.Manifold(md.Mesh(np.array(p.vertices,dtype=np.float32),np.array(p.faces,dtype=np.uint32)))
  if a.status()!=md.Error.NoError:
   try:p=p.convex_hull
   except Exception:continue
   a=md.Manifold(md.Mesh(np.array(p.vertices,dtype=np.float32),np.array(p.faces,dtype=np.uint32)));hulls+=1
  if a.status()==md.Error.NoError and a.volume()>0:pieces.append(a)
 return md.Manifold.batch_boolean(pieces,md.OpType.Add),hulls
def join(xs):return md.Manifold.batch_boolean(xs,md.OpType.Add)
def head_solid(head,shift):
 parts=[];points=[];proxies=0
 for n in head.graph.nodes_geometry:
  w,g=head.graph[n];t=head.geometry[g];v=t.vertices.copy()
  if n.startswith('OEM_DAC_'):
   v=deform(v,shift)
  v=v@w[:3,:3].T+w[:3,3];a,h=solid(v,t.faces);parts.append(a);points.append(v);proxies+=h
 return join(parts),np.vstack(points),proxies
def shape_at(m,s,pose):
 bi,bn=node_body(m,s['id']);v=s['world']
 if bn and bn in pose['worlds']:
  old=m.matrix(bi);now=np.array(pose['worlds'][bn]);v=(v-old[:3,3])@old[:3,:3]@now[:3,:3].T+now[:3,3]
 return v
if __name__=='__main__':
 m=Model();poses=json.loads((OUT/'poses.json').read_text());definition=json.loads((OUT/'head_definition.json').read_text());head=trimesh.load(io.BytesIO(gzip.decompress((OUT/'fixed_head.glb.gz').read_bytes())),file_type='glb');report={}
 openers=[];opener_proxies=0
 for s in m.shapes:
  if 'ACICI' in s['name']:
   a,h=solid(s['world'],s['faces']);openers.append(a);opener_proxies+=h
 opener=join(openers);tables=[s for s in m.shapes if 'DONER__TABLA' in s['name']];table=join([solid(s['world'],s['faces'])[0]for s in tables])
 for key,p in poses.items():
  hs,hv,hproxies=head_solid(head,p['tip_shift_mm']);w=np.array(p['worlds']['UR10E_body_06']);actual=hs.transform(w[:3,:]);actual_v=hv@w[:3,:3].T+w[:3,3]
  wrist=[];wrist_v=[];wproxies=0
  for s in m.shapes:
   if any(s['name'].startswith('UR10E_body_'+str(i).zfill(2)+'_mesh') for i in [4,5,6]):
    v=shape_at(m,s,p);a,h=solid(v,s['faces']);wrist.append(a);wrist_v.append(v);wproxies+=h
  local=join([actual]+wrist);local_v=np.vstack([actual_v]+wrist_v)
  current=float((local^opener).volume())*1e9 if key.startswith('Dough') and p['mode']=='place' else 0
  table_overlap=float((actual^table).volume())*1e9 if key.startswith('Dough') and p['mode']=='place' else 0
  raise_mm=None
  if key.startswith('Dough') and p['mode']=='place':
   for height in range(0,251,5):
    if (local^opener.translate([0,height/1000,0])).volume()<1e-12:raise_mm=height;break
   # This extra 5mm is a margin over the 5mm scan, not an OEM dimension.
  neighbor_overlap=0;drawer_overlap=0
  if key.startswith('Dough') and p['mode']=='pick':
   for s in m.shapes:
    if s['name'].startswith('CEK_K1') and '__CEKMECE' in s['name'] and '__CEKMECE_ARA' not in s['name']:
     b=s['bounds'].copy();b[:,2]+=.7
     if np.any(b[0]>actual_v.max(0)) or np.any(b[1]<actual_v.min(0)):continue
     a,h=solid(s['world']+[0,0,.7],s['faces']);volume=float((actual^a).volume())*1e9
     if '__hamur__' in s['name']:neighbor_overlap+=volume
     else:drawer_overlap+=volume
  environment_hits=[];environment_proxies=0
  for s in m.shapes:
   n=s['name'];v=s['world'];moving=n.startswith('CEK_') and '__CEKMECE' in n and '__CEKMECE_ARA' not in n
   if p['mode']=='place' and p['item']!='Dough':relevant=n.startswith('QR62_')
   elif p['mode']=='pick' and p['item'] in ['Cola','Dessert']:relevant=n.startswith('CEK_K5' if p['item']=='Cola' else 'CEK_K6')
   elif p['mode']=='pick' and p['item']=='Box':relevant=n.startswith('E_')
   else:relevant=False
   if not relevant:continue
   if moving:v=v+[0,0,p['drawer_open_m']]
   if np.any(v.min(0)>local_v.max(0)) or np.any(v.max(0)<local_v.min(0)):continue
   a,h=solid(v,s['faces']);environment_proxies+=h;volume=float((local^a).volume())*1e9
   if volume>1:environment_hits.append(dict(part=n,conservative_overlap_mm3=volume,proxy_components=h))
  # Intended pose is also measured even when native inverse kinematics failed.
  R=np.array(p['tool_orientation']);target=ident(p['contact']);target[:3,:3]=R;target[:3,3]-=R@np.array([0,0,TIP]);tv=hv@R.T+target[:3,3]
  row=dict(ik_valid=p['valid'],position_error_mm=p['position_error_mm'],angle_error_deg=p['angle_error_deg'],tip_shift_mm=p['tip_shift_mm'],native_opener_local_overlap_mm3=current,native_table_head_overlap_mm3=table_overlap,other_dough_overlap_mm3=neighbor_overlap,drawer_head_overlap_mm3=drawer_overlap,opener_lift_first_clear_5mm_scan=raise_mm,opener_lift_with_scan_and_margin_mm=raise_mm+5 if raise_mm is not None else None,actual_head_bottom_y_mm=float(actual_v[:,1].min()*1000),intended_head_bottom_y_mm=float(tv[:,1].min()*1000),local_head_wrist_top_y_mm=float(local_v[:,1].max()*1000),head_proxy_components=hproxies,wrist_proxy_components=wproxies,root_hash=p['root_hash'])
  row.update(local_environment_hits=environment_hits,environment_proxy_components=environment_proxies,opener_lift_is_diagnostic_only=not p['valid'] or table_overlap>1,usable_opener_height_verified=False)
  report[key]=row;print(key,json.dumps(row),flush=True)
 stock=next(s for s in m.shapes if s['name']=='CEK_K1_lahm_1__hamur__CEKMECE');t=trimesh.Trimesh(stock['world'],stock['faces'],process=True);parts=t.split(only_watertight=False);locations={tuple(np.round(x.bounds.mean(0)[[0,2]],4)) for x in parts}
 # Source dough comprises three coincident footprint pieces for each item.
 stock_count=len(parts)//3+1
 diam=definition['neutral_diameter_mm'];window=dict(short_star_max_open_diameter_mm=2*42+17+2*5,fixed_neutral_mm=diam,fixed_open_limit_mm=diam+10,fixed_closed_limit_mm=diam-22,box_min_height_with_diagonal_contacts_mm=(diam-22)/np.sqrt(2),entry_clearance_on_95mm_product_mm=diam+10-95,remaining_closure_on_45mm_box_mm=45-(diam-22)/np.sqrt(2),r_min_for_95mm_plus_2mm_entry= (95+2-17-10)/2,r_max_for_45mm_box_contact=(45*np.sqrt(2)-17+22)/2)
 result=dict(source='Claude completed Tur5 / web v28; native referenced triangles, no station remodel',stock_count=stock_count,stock_component_count=len(parts),same_mount_all_poses=all(x['finger_roots']==definition['finger_roots']for x in poses.values()),same_dough_orientation_pick_place=poses['Dough_pick']['tool_orientation']==poses['Dough_place']['tool_orientation'],same_tilt_orientation_pick_place=poses['Dough_tilt_pick']['tool_orientation']==poses['Dough_tilt_place']['tool_orientation'],supplier_tip_travel_is_graph_approximation=True,window=window,opener_proxy_component_count=opener_proxies,method='Discrete mesh booleans; non-manifold source components use conservative convex envelopes. Clearance scan every 5mm; 5mm extra shown as proposed margin. Intended soft-tip displacement is illustrative, not FEM or force proof.',physics_verified=False,continuous_path_verified=False,full_robot_environment_certified=False,poses=report)
 (OUT/'audit.json').write_text(json.dumps(result,indent=2));print('DONE stock',stock_count,'mount invariant',result['same_mount_all_poses'],flush=True)
