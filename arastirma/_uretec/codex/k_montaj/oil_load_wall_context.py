"""Reuse removal-only wall-context proof for the new load-mount candidate."""
from pathlib import Path
source=Path(__file__).with_name('oil_wall_context_audit.py')
code=source.read_text(encoding='utf-8').replace("/'oil_shelf_mount_candidate'","/'oil_load_mount_candidate'")
code=code.replace('checks=[]',"assert r['source_walls_unchanged'] and not recipe['wall_repairs']\nassert len(r['original_coarse_wall_bores'])==6\nassert all(j['original_material_mm3']<.001 for j in r['original_coarse_wall_bores'])\nchecks=[]")
code=code.replace('Each wall was constructed as original source solid minus the three declared native Ø5 hole cylinders; no wall material added, so unchanged-source intersections cannot increase. Bracket/fastener new solids were audited separately.', 'Both original source walls are retained by the repair writer; six actual4.9mm clear-core measurements found no wall material. No wall boolean or triangle rewrite is applied.')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
