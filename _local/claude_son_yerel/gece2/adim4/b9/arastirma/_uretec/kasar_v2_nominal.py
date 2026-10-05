"""Check that B/C repairs changed topology, not their occupied nominal volume."""
from pathlib import Path
import json
import cadquery as cq
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'arastirma/3_TOPPING/kasar_v2'
SRC=ROOT/'arastirma/3_TOPPING/kasar_kabi_v14/step'
rows=[]
for letter in 'BC':
    old=cq.importers.importStep(str(SRC/('helezon_'+letter+'.step'))).val()
    new=cq.importers.importStep(str(OUT/'cad'/('helezon_'+letter+'_v15.step'))).val()
    left=new
    removed=[]
    for solid in old.Solids():
        removed.append(solid.cut(new).Volume(tol=1e-7))
        left=left.cut(solid)
    added=left.Volume(tol=1e-7)
    row=dict(part=letter,old_minus_new_mm3=sum(removed),new_minus_old_mm3=added,
             old_solid_count=len(old.Solids()),new_solid_count=len(new.Solids()),
             pass_=sum(removed)<.05 and added<.05)
    rows.append(row);print(json.dumps(row),flush=True)
(OUT/'nominal_volume_diff.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
assert all(r['pass_'] for r in rows),rows
