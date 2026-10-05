"""Measure existing K body fastener axes and thread stack in authoritative mesh."""
from pathlib import Path
import numpy as np,json,pickle,hashlib
H=Path(__file__).resolve().parent;O=H.parent
P=pickle.load((H/'k_parca.pkl').open('rb'))['P'];cad=json.loads((O/'source_cad_inventory.json').read_text(encoding='utf-8'))
rows=[]
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
  holes.append({'host':a,'nominal_diameter_mm':hole['cap'],'nearest_circular_surface_radius_error_mm':error,'passed':error is not None and error<.02})
 row={'id':j['ad'],'hardware':names,'hosts':hosts,'source_axis':e.tolist(),'measured_axis_deviation_mm':deviation,'measured_intervals_mm':intervals,'engagement_mm':engagement,'protrusion_mm':protrusion,'protrusion_threads':protrusion/pitch,'holes':holes,'passed':max(deviation.values())<=.02 and engagement>=d-.02 and pitch-.02<=protrusion<=3*pitch+.02 and all(h['passed'] for h in holes)}
 rows.append(row)
 print('BODY_CONNECTION',row['id'],row['passed'],'engagement',round(engagement,3),'threads',round(protrusion/pitch,3),flush=True)
report={'scope':'existing source-defined K body joins only; not whole K connection release','checks':rows,'passed':all(r['passed'] for r in rows),'count':len(rows),'unresolved':[r['id'] for r in rows if not r['passed']],'full_station_release':False}
(H/'body_connection_measured_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
