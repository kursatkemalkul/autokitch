import json
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull
p=Path('_local/codex_robot_v28')
raw=json.loads((p/'body_points.json').read_text())
out={}
for name,groups in raw.items():
    result=[]
    for points in groups:
        v=np.unique(np.asarray(points),axis=0)
        if len(v)>=4 and np.linalg.matrix_rank(v-v[0])==3:
            result.append(v[ConvexHull(v).vertices].tolist())
    out[name]=result
(p/'body_hulls.json').write_text(json.dumps(out))
print({n.split('/')[-1]:[len(v) for v in s] for n,s in out.items()})
