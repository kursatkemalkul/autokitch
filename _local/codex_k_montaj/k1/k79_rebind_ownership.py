"""Use the stage78 one-to-one matcher with the explicit stage79 recipe.

Keep stage78 active; new results are separate until independently audited.
"""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k78_rebind_ownership.py'
code=source.read_text(encoding='utf-8').replace('78','79').replace('hat3_v10s','hat3_v10t')
code=code.replace('if manifest.exists():previous_path=', 'if False:previous_path=')
old="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
new="""import gzip
repairs=json.loads(gzip.decompress((H/'rounded_post_recipe.json.gz').read_bytes()))['repairs']
for r in repairs.values():
 for k in ('original_triangles','vertices','triangles'):r[k]=np.asarray(r[k],dtype=np.int64 if k=='triangles' else np.float64)"""
assert old in code;code=code.replace(old,new)
code=code.replace("H/'topology_repair_proposal.pkl'", "H/'rounded_post_recipe.json.gz'")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
