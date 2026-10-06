"""Independent column envelope, USB route and purchase-CAD provenance checks."""
from pathlib import Path
import json,hashlib
import numpy as np
from segment_distance import dist
R=Path(__file__).resolve().parents[3];A=R/'otonom/hat3d/robot-integrated-v25'
m=json.loads((A/'manifest.json').read_text());q=m['services']['qr_customer'];routes=q['internal_usb_routes'];errors=[]
lo,hi=np.array(q['column_bounds']);lengths={}
for c in routes:
    p=np.array(c['points']);r=c['r']
    if np.any(p.min(axis=0)-r<lo-1e-5) or np.any(p.max(axis=0)+r>hi+1e-5):errors.append(c['name']+' leaves column envelope')
    if c['minimum_radius_m']<.025:errors.append(c['name']+' tighter than R25')
    length=float(np.linalg.norm(np.diff(p,axis=0),axis=1).sum());lengths[c['name']]=length
    if length>2:errors.append(c['name']+' exceeds selected 2 m USB run')
p=np.array(routes[0]['points']);s=np.array(routes[1]['points']);ii,jj=np.meshgrid(np.arange(len(p)-1),np.arange(len(s)-1),indexing='ij');i=ii.ravel();j=jj.ravel();d=dist(p[i],p[i+1],s[j],s[j+1]);clear=float(d.min()-routes[0]['r']-routes[1]['r'])
if clear<.002:errors.append('Internal USB cables intersect / insufficient separation')
step=R/'arastirma/_uretec/robot_integrated_v25/vendor/K_Range 12 way.STEP'
if hashlib.sha256(step.read_bytes()).hexdigest()!=q['keypad']['sha256']:errors.append('Keypad supplier CAD source differs')
if not np.allclose(q['keypad']['dimensions_mm'],[99.5,118.5,14],atol=1e-5):errors.append('Keypad supplier outer dimensions changed')
if not np.allclose(q['reader']['dimensions_mm'],[41.5,49.5,24.3]):errors.append('Reader catalogue dimensions changed')
layout=m['services']['layout_scan']
if layout['panel_clearance_m']<.05 or layout['qr_column_clearance_m']<0:errors.append('New wall/panel/column blocks a recorded frame')
report={'version':25,'usb_length_m':lengths,'usb_surface_clearance_m':clear,'minimum_usb_radius_m':.025,'unchanged_keypad_supplier_step_sha256':q['keypad']['sha256'],'reader_geometry':'catalogue envelope reconstruction, not OEM CAD','recorded_frame_panel_clearance_m':layout['panel_clearance_m'],'recorded_frame_column_clearance_m':layout['qr_column_clearance_m'],'errors':errors,'passed':not errors,'scope':'new layout/column only; physical unlock circuit and complete robot collision remain open'}
(A/'qr_column_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report));raise SystemExit(bool(errors))
