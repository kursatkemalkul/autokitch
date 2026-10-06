"""Exact whole K triangle binding of the appended clip weld prototype."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'head_rebind.py'
code=source.read_text(encoding='utf-8')
for old,new in [('k_parca_catalog_verified','k_parca_head_verified'),('k_parca_head_raw','k_parca_clip_raw'),
 ('head_ownership_rebind_audit','clip_ownership_rebind_audit'),('surface_ownership_registry_head','surface_ownership_registry_clip'),
 ('cut_head_yoke_candidate','electrical_clip_weld_candidate'),('hat3_v10zd','hat3_v10ze')]:code=code.replace(old,new)
# Previous cache path is head; destination must be clip. Replace the wrapper
# output mapping explicitly rather than changing its previous input cache.
code=code.replace("('k_parca78_verified.pkl','k_parca_head_verified.pkl')","('k_parca78_verified.pkl','k_parca_clip_verified.pkl')")
anchor="rows=dict(proposal['parts'],**proposal.get('wall_repairs',{}))"
assert anchor in code
code=code.replace(anchor,anchor+"\nfor j in proposal['joins']:\n a=j['clip'];rows[a]=dict(V=old[a]['V'],F=old[a]['F'],tur=old[a]['tur'],purpose='Exact unchanged clip template')\n")
anchor="meta=dict(old[a]) if a in old else dict(templates[r['tur']])"
assert anchor in code
code=code.replace(anchor,"meta=dict(old[a]) if a in old else dict(old[r['carriers'][0]])")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
