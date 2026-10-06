"""Reuse exact one-to-one matcher; include12 newly modelled fasteners."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k78_rebind_ownership.py';code=source.read_text(encoding='utf-8')
code=code.replace('if manifest.exists():previous_path=','if False:previous_path=')
code=code.replace('k_parca78_raw.pkl','k_parca_panel_raw.pkl')
code=code.replace('k_parca78_verified.pkl','k_parca_panel_verified.pkl')
code=code.replace('step78_ownership_rebind_audit.json','panel_ownership_rebind_audit.json')
code=code.replace('surface_ownership_registry78.json','surface_ownership_registry_panel.json')
old="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
new="""import gzip
folder=H.parent/'panel_mount_candidate'
proposal=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert proposal['source_parts_sha256']==hashlib.sha256(previous_path.read_bytes()).hexdigest()
repairs={a:{'vertices':np.asarray(p['V'],float),'triangles':np.asarray(p['F'],int)} for a,p in proposal['replacement_parts'].items()}
for a in proposal['added_parts']:
 meta=dict(old['pano_ara_burcu_0']);meta.update(tur='baglanti',dugum='K_ELEKTRIK__celik')
 meta['V']=repairs[a]['vertices'];meta['F']=repairs[a]['triangles'];old[a]=meta
"""
assert old in code;code=code.replace(old,new)
code=code.replace("H/'topology_repair_proposal.pkl'","H.parent/'panel_mount_candidate/geometry.json.gz'")
code=code.replace("H.parent/'chain73/A/hat3_v10s.json'","H.parent/'panel_mount_candidate/A/hat3_v10u.json'")
code=code.replace('REBIND78','REBIND_PANEL')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
