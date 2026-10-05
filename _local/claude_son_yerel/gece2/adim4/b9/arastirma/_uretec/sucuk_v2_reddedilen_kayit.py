"""Preserve the aborted V2B trial as a FAILURE, never as completed validation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'arastirma/_uretec/sucuk_v2_relieved01.log'
rows=[json.loads(line[8:]) for line in p.read_text(encoding='utf-8',errors='replace').splitlines() if line.startswith('MEASURE ')]
r={'tag':'full_relieved_01','status':'ABORTED_REJECTED','completed_cycle':False,
   'reason':'Insufficient flow and slow rotation at tested 3 Nm / 6 rpm; do not select this setting.',
   'causality_warning':'Geometry, torque and speed changed together; not proof geometry alone is worse.',
   'source_log':str(p),'last':rows[-1] if rows else None,'measurements':rows}
(ROOT/'arastirma/3_TOPPING/sucuk_v2/rejected_trial.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in r.items() if k!='measurements'}))
