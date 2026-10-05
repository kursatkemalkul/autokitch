"""Independent STEP assembly and capacity audit for the local cheese revision."""
from pathlib import Path
import json,math
import cadquery as cq
import kasar_cad_v14 as old
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2'
SRC=ROOT/'arastirma/3_TOPPING/kasar_kabi_v14/step'
shapes={}
for p in SRC.glob('*.step'):
    if p.stem=='helezon_TEK_PARCA':continue
    changed=OUT/'cad'/(p.stem+'_v15.step')
    shapes[p.stem]=cq.importers.importStep(str(changed if changed.exists() else p)).val()
rows=[]
for c in 'BCD':
    name='helezon_'+c;s=shapes[name]
    rows.append(dict(check=name+' single solid',pass_=s.isValid() and len(s.Solids())==1))
    for angle in [0,45,90,135,180,225,270,315]:
        rot=s.rotate((0,40,0),(0,40,1),angle)
        for other in ['govde','plaka_on','plaka_arka','cikis_tupu','yatak_kapagi']:
            vol=rot.intersect(shapes[other]).Volume(tol=1e-7)
            rows.append(dict(check=f'{name} vs {other} @{angle}',pass_=vol<.02,overlap_mm3=vol))
    for other in ['helezon_A','helezon_B','helezon_C','helezon_D']:
        if other==name:continue
        vol=s.intersect(shapes[other]).Volume(tol=1e-7)
        rows.append(dict(check=name+' vs '+other,pass_=vol<.02,overlap_mm3=vol))
    print('CHECKED',name,flush=True)
# Exact wetted internal volume up to approved fill line, less intersecting
# hardware. No bulk/solid density interchange.
inner=old.kesit(0,old.Y_DOLUM).extrude(old.ZFI-old.ZBI).translate((0,0,old.ZBI)).val()
iv=inner.Volume(tol=1e-7);disp={}
for name,s in shapes.items():
    if name=='tasima_tapasi':continue
    v=s.intersect(inner).Volume(tol=1e-7)
    assert -.01<=v<=s.Volume(tol=1e-7)+.1,(name,v)
    if v>.01:disp[name]=v
free=(iv-sum(disp.values()))/1e6
capacity=dict(fill_line_y_mm=old.Y_DOLUM,inner_l=iv/1e6,displacement_mm3=disp,free_l=free,
    full_stock_g=8800,minimum_bulk_density_for_90pct_g_ml=8.8/(free*.9),
    cases=[dict(bulk_g_ml=rho,fill_percent=100*8.8/rho/free,passes_90pct=8.8/rho/free<=.9) for rho in [.4,.48,.5,.55]])
# Source opening remains open along its cylinder; cylinders are test gauges,
# not added geometry. Gauge D43.8 must pass from mouth to the exit.
tube=shapes['cikis_tupu']
gauge=old.sily(0,212.5,21.9,-9,40.5).val()
overlap=tube.intersect(gauge).Volume(tol=1e-7)
rows.append(dict(check='Nozzle bore open (D43.8 gauge)',pass_=overlap<.02,overlap_mm3=overlap))
res=dict(checks=rows,capacity=capacity,passed=sum(r['pass_'] for r in rows),failed=sum(not r['pass_'] for r in rows))
(OUT/'structural_checks.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print(json.dumps(res,indent=2),flush=True)
