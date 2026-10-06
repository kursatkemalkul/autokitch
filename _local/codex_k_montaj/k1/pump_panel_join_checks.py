"""Repeat the established eight panel/DIN measurements on the current source."""
from pathlib import Path
import hashlib,json,pickle
import numpy as np
import trimesh
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
source=ROOT/'arastirma/_uretec/codex/k_montaj/din_geometry_audit.py'
code=source.read_text(encoding='utf-8')
start=code.index('for j in candidate[')
stop=code.index("report={'scope':")
parts=H/'k_parca_pump_verified.pkl'
P=pickle.load(parts.open('rb'))['P']
candidate=json.loads((H.parent/'din_mount_candidate/audit.json').read_text(encoding='utf-8'))
rows=[]
exec(compile(code[start:stop],str(source),'exec'),globals())
assert len(rows)==8
report={'source_parts_sha256':hashlib.sha256(parts.read_bytes()).hexdigest(),
        'scope':'eight panel/DIN fasteners only; device clips are not covered',
        'checks':rows,'passed':all(r['passed'] for r in rows),'production_release':False}
(H/'pump_panel_join_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('BOTTOM_PANEL_JOINS',len(rows),report['passed'],flush=True)
assert report['passed']
