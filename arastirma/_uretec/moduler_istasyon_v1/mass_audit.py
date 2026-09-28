"""Raw CAD volume audit: catalog envelopes are NOT reliable weighing data."""
import json,os,sys
import cadquery as cq
from load_source import OUT
info=json.loads((OUT/'.cache/base_parts.json').read_text(encoding='utf-8'))
shapes=list(cq.Shape.importBrep(str(OUT/'.cache/base.brep')))
rows=[]
for p,s in zip(info['parts'],shapes):
    if p['material'] in ('304','celik','sac','paslanmaz','fircali'):
        kg=abs(s.Volume())*7.93e-6
        if kg>5:rows.append(dict(module=p['module'],name=p['name'],kg=round(kg,2),material=p['material']))
print(json.dumps(sorted(rows,key=lambda p:-p['kg']),ensure_ascii=False,indent=2))
sys.stdout.flush();os._exit(0)
