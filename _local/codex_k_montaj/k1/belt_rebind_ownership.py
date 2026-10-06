"""Reuse the exact full triangle matcher for all four feet and16 new parts."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k78_rebind_ownership.py'
code=source.read_text(encoding='utf-8').replace('if manifest.exists():previous_path=','if False:previous_path=')
code=code.replace('k_parca78_raw.pkl','k_parca_belt_raw.pkl').replace('k_parca78_verified.pkl','k_parca_belt_verified.pkl').replace('step78_ownership_rebind_audit.json','belt_ownership_rebind_audit.json').replace('surface_ownership_registry78.json','surface_ownership_registry_belt.json')
anchor="repairs=pickle.load((H/'topology_repair_proposal.pkl').open('rb'))['repairs']"
replacement="""import gzip
folder=H.parent/'belt_support_candidate'
proposal=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert proposal['source_parts_sha256']==hashlib.sha256(previous_path.read_bytes()).hexdigest()
repairs={a:{'vertices':np.asarray(r['V'],float),'triangles':np.asarray(r['F'],int)} for a,r in proposal['replacement_parts'].items()}
for a,r in proposal['replacement_parts'].items():
 if a not in old:
  meta=dict(old['k72_bant_ayak_kaynagi_4065.0_-421.0_0' if r['tur']=='kaynak' else 'bant_ayagi_65_-3'])
  meta.update(tur=r['tur'],m='kaynak' if r['tur']=='kaynak' else 'sac',dugum='K_BANT__sac')
  old[a]=meta
 old[a]['ac']=str(r['description']);old[a]['tur']=r['tur']
"""
assert anchor in code;code=code.replace(anchor,replacement).replace("H/'topology_repair_proposal.pkl'","H.parent/'belt_support_candidate/geometry.json.gz'").replace("H.parent/'chain73/A/hat3_v10s.json'","H.parent/'belt_support_candidate/A/hat3_v10w.json'").replace('REBIND78','REBIND_BELT')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
