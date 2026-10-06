"""Measure existing K body fastener axes and thread stack in authoritative mesh."""
from pathlib import Path
import numpy as np,json,pickle,hashlib
H=Path(__file__).resolve().parent;O=H.parent
P=pickle.load((H/'k_parca.pkl').open('rb'))['P'];cad=json.loads((O/'source_cad_inventory.json').read_text(encoding='utf-8'))
rows=[]
def current_roof_slot(host,center,diameter,shaft_diameter):
 """Measure both inward-facing walls of the actual bottom-open slot.

 The original inventory calls this opening circular. Step77 intentionally
 changed it to a bottom-open slot; measure current geometry, not old radii.
 """
 x,y,z=center;q=P[host]['V'][P[host]['F']];half=diameter/2;walls=[]
 for side in (-1,1):
  level=x+side*half
  mask=(np.max(abs(q[:,:,0]-level),axis=1)<.01)&(q[:,:,2].min(1)>=-828.51)&(q[:,:,2].max(1)<=-826.98)&(q[:,:,1].min(1)>=1839.99)&(q[:,:,1].max(1)<=1853.01)
  candidate=q[mask];normal=np.cross(candidate[:,1]-candidate[:,0],candidate[:,2]-candidate[:,0]);length=np.linalg.norm(normal,axis=1)
  candidate=candidate[(length>1e-9)&((normal[:,0]/np.maximum(length,1e-20))*(-side)>.999)]
  if not len(candidate):return {'opening_type':'bottom_open_slot','passed':False,'reason':'Current slot wall missing','side':side}
  lo=candidate.min((0,1));hi=candidate.max((0,1));plane=float(candidate[:,:,0].mean())
  walls.append({'side':side,'plane_x_mm':plane,'y_span_mm':[float(lo[1]),float(hi[1])],'z_span_mm':[float(lo[2]),float(hi[2])],'shaft_vertical_clearance_passed':bool(lo[1]<=y-shaft_diameter/2+.01 and hi[1]>=y+shaft_diameter/2-.01)})
 width=walls[1]['plane_x_mm']-walls[0]['plane_x_mm'];clearance=(width-shaft_diameter)/2
 return {'opening_type':'bottom_open_slot','nominal_width_mm':diameter,'measured_width_mm':width,'shaft_radial_clearance_mm':clearance,'walls':walls,'passed':abs(width-diameter)<.02 and clearance>=.23 and all(w['shaft_vertical_clearance_passed'] for w in walls)}
for j in cad['joins']:
 names=[p['ad'] for p in j['parcalar']];hosts=j['sac']
 if not all(a in P for a in names+hosts):continue
 e=np.asarray(j['eksen'],float);c=np.asarray(j['nokta'],float)+[4000,0,0];d=float(j['dis'][1:]);pitch={5:.8,8:1.25}[d]
 intervals={};deviation={}
 for a in names:
  V=P[a]['V'];t=(V-c)@e;centre=(V.min(0)+V.max(0))/2-c
  # An odd-sided GLB ring has an asymmetric bounding box. Fit the actual circular bore/shaft vertices; bbox centre is not its axis.
  axes=[i for i in range(3) if abs(e[i])<.5];q=V-c;uv=q[:,axes];radius=np.linalg.norm(uv,axis=1);target=d/2+.15 if a.endswith('_pul') else d/2
  uv=np.unique(uv[abs(radius-target)<.1],axis=0)
  if len(uv)<5:raise ValueError('Insufficient circular shaft/bore samples: '+a)
  fit=np.linalg.lstsq(np.column_stack((2*uv,np.ones(len(uv)))),np.sum(uv*uv,axis=1),rcond=None)[0]
  fit_radius=float(np.sqrt(fit[2]+np.sum(fit[:2]**2)));residual=float(np.max(abs(np.linalg.norm(uv-fit[:2],axis=1)-fit_radius)))
  if residual>.02:raise ValueError('Noncircular shaft/bore: '+a)
  deviation[a]=float(np.linalg.norm(fit[:2]));intervals[a]=[float(t.min()),float(t.max())]
 male=next(a for a in names if a.endswith(('_saplama','_vida')));female=next(a for a in names if a.endswith('_somun'));mi=intervals[male];fi=intervals[female]
 engagement=max(0,min(mi[1],fi[1])-max(mi[0],fi[0]));protrusion=mi[1]-fi[1]
 holes=[]
 for hole in j['delikler']:
  a=hole['sac'];centre=np.asarray(hole['merkez'],float)+[4000,0,0];V=P[a]['V'];q=V-centre;z=q@e;r=np.linalg.norm(q-np.outer(z,e),axis=1)
  wanted=hole['cap']/2;select=(r<wanted+1)&(abs(z)<4)
  candidates=r[select];error=float(np.min(abs(candidates-wanted))) if len(candidates) else None
  if a=='ust_sac' and j['ad'] in ('govde_bag_arka_ust_40','govde_bag_arka_ust_360'):
   holes.append(dict(host=a,**current_roof_slot(a,centre,hole['cap'],d)))
  else:holes.append({'host':a,'opening_type':'circular','nominal_diameter_mm':hole['cap'],'nearest_circular_surface_radius_error_mm':error,'passed':error is not None and error<.02})
 row={'id':j['ad'],'hardware':names,'hosts':hosts,'source_axis':e.tolist(),'measured_axis_deviation_mm':deviation,'measured_intervals_mm':intervals,'engagement_mm':engagement,'protrusion_mm':protrusion,'protrusion_threads':protrusion/pitch,'holes':holes,'passed':max(deviation.values())<=.02 and engagement>=d-.02 and pitch-.02<=protrusion<=3*pitch+.02 and all(h['passed'] for h in holes)}
 rows.append(row)
 print('BODY_CONNECTION',row['id'],row['passed'],'engagement',round(engagement,3),'threads',round(protrusion/pitch,3),flush=True)
report={'scope':'existing source-defined K body joins only; not whole K connection release','source_parts_sha256':hashlib.sha256((H/'k_parca.pkl').read_bytes()).hexdigest(),'checks':rows,'passed':all(r['passed'] for r in rows),'count':len(rows),'unresolved':[r['id'] for r in rows if not r['passed']],'full_station_release':False}
(H/'body_connection_measured_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
