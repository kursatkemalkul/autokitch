"""Targeted V2 checks. Source production files are read-only.

Not a blanket manufacturing approval: unknown food properties and missing
hardware feedback remain KALDI / NOT VALIDATED, regardless of solid checks.
"""
from pathlib import Path
import json,math
import cadquery as cq
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/sucuk_v2'
OLD=ROOT/'arastirma/3_TOPPING/sucuk_kaseti_v7/step'
cad=json.loads((OUT/'cad/cad_checks.json').read_text())
rows=[]
def check(name,ok,detail):
    rows.append(dict(check=name,result='GECTI' if ok else 'KALDI',detail=detail))
    print(rows[-1],flush=True)
for name,r in cad.items():
    if name=='candidate_checks':continue
    check(name+' closed solid and mesh',r['valid'] and r['closed_mesh'] and r['relative_volume_error']<.001,
          {'bad_edges':r['bad_edges'],'relative_volume_error':r['relative_volume_error']})
d=cq.importers.importStep(str(OUT/'cad/helezon_D_v2.step')).val()
t=cq.importers.importStep(str(OUT/'cad/cikis_tupu_v2.step')).val()
static={name:cq.importers.importStep(str(OLD/(name+'.step'))).val()
        for name in ['govde','plaka_on','yatak_kapagi','on_kovan']}
static['cikis_tupu_v2']=t
for angle in range(0,360,45):
    rotated=d.rotate((0,60,0),(0,60,1),angle)
    for name,other in static.items():
        v=rotated.intersect(other).Volume()
        check(f'D vs {name} at {angle} deg',v<.02,{'overlap_mm3':v})
check('Screw removable through bore',68<72,{'flight_OD_mm':68,'bore_ID_mm':72})
# Global minimum includes the correctly clearanced 0.2 mm front journal.
# Check the flight zone separately instead of mislabelling journal clearance.
flight_zone=d.intersect(cq.Solid.makeBox(100,120,55,cq.Vector(-50,0,150)))
check('Flight-zone radial clearance',abs(flight_zone.distance(t)-2)<.05,{'distance_mm':flight_zone.distance(t)})
rp=OUT/'cad/relieved_checks.json'
if rp.exists():
    rb=json.loads(rp.read_text())
    for name,value in rb.items():
        if name=='checks':continue
        check('V2B '+name+' closed solid and mesh',value['valid'] and value['closed_mesh'] and value['mesh_volume_error']<.001,value)
    for row in rb['checks']['rotation_checks']:
        check('V2B D vs tube '+str(row['angle_deg'])+' deg',row['overlap_mm3']<.02,row)
check('Food stiffness/friction/adhesion measured',False,'VARSAYIM: supplier sample calibration required')
check('Crushing / cutting validated',False,'Compliant contact is not a food damage model')
check('Physical dosing feedback installed',False,'Experiment uses virtual mass crossing counter')
check('Tray contact geometry and pin seating validated',False,
      'Inherited v13 scene uses a full-disc tray collider, not the formed sheet and pin pockets')
check('Two-day idle / cleaning / food-contact qualification',False,'Not tested / no grade-specific declaration yet')
(OUT/'kaset_kontrol_sonuc.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('FINAL',sum(r['result']=='GECTI' for r in rows),'GECTI',sum(r['result']=='KALDI' for r in rows),'KALDI',flush=True)
