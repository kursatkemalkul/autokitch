from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'arastirma/_uretec/codex/k_montaj'))
from lower_support import build
from mechanism_mounts import build_mounts
from roof_mounts import build_roof
out={}
for fn in (build,build_mounts,build_roof):
 fn_parts=fn()[0]
 for p in fn_parts:
  b=p['sh'].BoundingBox(); name=p['ad']; mal=p.get('mal','sac')
  node=('K_GOVDE__sac' if mal=='sac' or p.get('tur') in ('sac','profil','kaynak') else 'K_GOVDE__celik')
  if fn==build_mounts: node=('K_BANT' if ('bant' in name or 'M6' in name) else 'K_ITICI')+('__sac' if p.get('tur') in ('sac','profil','kaynak') else '__celik')
  if fn==build_roof: node='K_GOVDE__kabuk' if p is fn_parts[0] else 'K_GOVDE__sac'
  out[name]={'dugum':node,'kutu':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax], 'tur': 'kaynak' if 'kayna' in name else 'profil' if 'dikme' in name else 'arayuz' if any(w in name.lower() for w in ('vida','pem','somun','pul','saplama','civata')) else 'sac', 'bom':p.get('bom',[])}
(Path(__file__).parent/'k_local_ent.json').write_text(json.dumps({'parca':out},ensure_ascii=False,indent=2),encoding='utf-8')
print('Local K records',len(out))
