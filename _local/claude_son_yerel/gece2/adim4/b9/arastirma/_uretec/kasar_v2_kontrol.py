"""Kasar V2 checklist. Unknowns remain explicit KALDI; no production release."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2'
rows=[]
def check(name,ok,detail=''):
    r=dict(check=name,result='GECTI' if ok else 'KALDI',detail=detail);rows.append(r);print(r,flush=True)
p=OUT/'cad/cad_checks.json'
check('CAD export completed',p.exists())
if p.exists():
    c=json.loads(p.read_text())
    for name,r in c['meshes'].items():check(name+' closed verified mesh',r['valid'] and r['closed'] and r['mesh_volume_error']<.001,r['mesh_volume_error'])
    for name,r in c['parts'].items():check(name+' solid and differential check',r['valid'] and (r['changed'] or abs(r['new_volume_mm3']-r['old_volume_mm3'])<.01))
    for r in c['checks']:check('D rotation %s vs %s'%(r['angle'],r['part']),r['pass_'],r['overlap_mm3'])
    expected={p.stem for p in (ROOT/'arastirma/3_TOPPING/kasar_kabi_v14/step').glob('*.step') if p.stem!='helezon_TEK_PARCA'}
    check('Every previous part accounted for',set(c['parts'])==expected,len(c['parts']))
    check('Body envelope unchanged; tube delta explicitly recorded',c['design']['body_mm']==[280,325,360] and c['design']['changed_parts']==['helezon_B','helezon_C','helezon_D','cikis_tupu'],c['design'].get('vertical_pipe_new_inner_outer_mm'))
    check('Screw passes existing bore',c['design']['screw_od_mm']<c['design']['trough_id_mm'])
    for name in ['helezon_D_v15.step','helezon_D_v15.stl','KASAR_V2_CAD_v15_MONTAJ.step','BOM_diff.csv']:
        check('File '+name,(OUT/'cad'/name).exists())
rp=OUT/'run_comparison.json'
np=OUT/'nominal_volume_diff.json'
if np.exists():
    for r in json.loads(np.read_text()):
        check('B/C nominal volume preserved: '+r['part'],r['pass_'],r)
sp=OUT/'structural_checks.json'
if sp.exists():
    structural=json.loads(sp.read_text())
    for r in structural['checks']:check('STEP '+r['check'],r['pass_'],r.get('overlap_mm3',''))
runs=json.loads(rp.read_text()) if rp.exists() else []
for r in runs:
    check(r['tag']+' finite physical recording',r['finite'] and r['max_quaternion_norm_error']<.001)
    check(r['tag']+' individual stock masses consistent',r.get('stock_mass_consistent',False))
    report=json.loads((OUT/'runs'/(r['tag']+'.json')).read_text())
    mesh=OUT/'cad'/('closed_meshes.npz' if r['variant']=='candidate' else 'baseline_meshes.npz')
    if 'cad_mesh_sha256' in report['geometry_audit']:
        check(r['tag']+' recording matches CAD mesh',report['geometry_audit']['cad_mesh_sha256']==hashlib.sha256(mesh.read_bytes()).hexdigest())
    if report.get('radius_law_sha256'):
        law=ROOT/report['material_assumptions']['law_file']
        check(r['tag']+' control law reproducible',report['radius_law_sha256']==hashlib.sha256(law.read_bytes()).hexdigest())
check('Baseline and candidate both physically tested',all(any(r['variant']==v for r in runs) for v in ['baseline','candidate']))
check('Real cheese properties calibrated',False,'Dimensions, friction, stiffness, adhesion and bulk density not measured')
check('Crushing and matting validated',False,'Rigid shreds and compliant contact cannot prove food damage or adhesive clumps')
check('SDF and timestep convergence verified',False,'Shared resolution 256 / 480 Hz; not an independent convergence study')
check('Full 8.8 kg and two-day idle tested',False,'Only declared partial-stock physical runs; geometric capacity is separate')
check('Physical dosage sensing or open-loop calibration',False,'Virtual crossing counter is not installed machine hardware')
check('Actual tray sheet and pin seating validated',False,'Inherited v13 solid-disc collider')
check('Motor torque-speed and full-stock thermal duty verified',False,'5 Nm simulated drive ceiling is not a measured torque-speed curve')
check('Flight strength and loaded running clearance verified',False,'Rigid CAD clearance is not a stress/deflection or tolerance analysis')
check('Food-contact materials / cleanability approved',False,'Grade-specific documents, surface finish and joint hygiene not signed off')
(OUT/'kaset_kontrol_sonuc.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
passed=sum(r['result']=='GECTI' for r in rows);failed=len(rows)-passed
print('FINAL',passed,'GECTI',failed,'KALDI; NOT PUBLISHED',flush=True)
sys.exit(1 if failed else 0)
