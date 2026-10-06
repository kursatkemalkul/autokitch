from pathlib import Path
import json,struct,sys
from inspect_scene import envelopes

def header(p):
    with Path(p).open('rb') as f:
        h=f.read(20);return json.loads(f.read(struct.unpack_from('<I',h,12)[0]))

root=Path(__file__).resolve().parents[3]
for label,p in [('robot',root/'otonom/hat3d/robot-integrated-v23/ur10e_short.glb'),('scene',Path(sys.argv[1]))]:
    g=header(p)
    rows=envelopes(g)
    for row in rows:
        n=g['nodes'][row['id']]
        colors=[(g.get('materials') or [{}])[p.get('material',0)].get('pbrMetallicRoughness',{}).get('baseColorFactor') for p in g['meshes'][n['mesh']]['primitives']]
        yellow=any(c and c[0]>.6 and c[1]>.4 and c[2]<.4 for c in colors)
        if label=='robot' or (row['box'][1][2]>.12 and (yellow or 'ZEMIN' in row['name'] or 'ROBOT' in row['name'] or 'zemin' in row['name'])):
            print(json.dumps({'source':label,**row,'colors':colors},ensure_ascii=False))
