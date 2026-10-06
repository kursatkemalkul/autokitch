"""Export the small deterministic repair recipe as JSON; keep pickle local."""
from pathlib import Path
import pickle,json,gzip,hashlib
import numpy as np
H=Path(__file__).resolve().parent
source=H/'topology_repair_proposal.pkl';P=pickle.load(source.open('rb'))
step=json.loads((H.parent/'chain73/A/hat3_v10s.json').read_text(encoding='utf-8'))
D={'source_model_sha256':step['input_sha256'],'source_encoding_sha256':P['source_encoding_sha256'],'repairs':{a:{'original_triangles':r['original_triangles'].tolist(),'vertices':r['vertices'].tolist(),'triangles':r['triangles'].tolist(),'proof':r['proof']} for a,r in P['repairs'].items()}}
data=json.dumps(D,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8');target=H/'topology_repair_recipe.json.gz';target.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
decoded=json.loads(gzip.decompress(target.read_bytes()))
for a,r in P['repairs'].items():
 for k in ('original_triangles','vertices','triangles'):assert np.array_equal(np.asarray(decoded['repairs'][a][k]),r[k]),(a,k)
(H/'topology_recipe_serialization_audit.json').write_text(json.dumps({'recipe_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_model_sha256':D['source_model_sha256'],'array_values_preserved_exactly':True,'deterministic_gzip_mtime':0,'pickle_is_local_cache_only':True,'production_release':False},indent=2),encoding='utf-8')
print('JSON_RECIPE_EXACT',target.stat().st_size,flush=True)
