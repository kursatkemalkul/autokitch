"""Bind byte determinism, K-only scope and complete source surface ownership."""
from pathlib import Path
source=Path(__file__).with_name('oil_source_scope_audit.py')
code=source.read_text(encoding='utf-8')
code=code.replace("source=OUT/'belt_bottom_mount_candidate/A/hat3_v10x.glb'","source=OUT/'oil_shelf_mount_candidate/A/hat3_v10y.glb'")
code=code.replace("folder=OUT/'oil_shelf_mount_candidate'","folder=OUT/'oil_load_mount_candidate'")
code=code.replace("A=folder/'A/hat3_v10y.glb';B=folder/'B/hat3_v10y.glb'","A=folder/'A/hat3_v10z.glb';B=folder/'B/hat3_v10z.glb'")
code=code.replace('k_parca_oil_verified.pkl','k_parca_oil_load_verified.pkl')
code=code.replace('k_parca_bottom_verified.pkl','k_parca_oil_verified.pkl')
code=code.replace('oil_ownership_rebind_audit.json','oil_load_ownership_rebind_audit.json')
code=code.replace('surface_ownership_registry_oil.json','surface_ownership_registry_oil_load.json')
code=code.replace('k_parca_oil_raw.pkl','k_parca_oil_load_raw.pkl')
code=code.replace('885+len','907+len').replace("sha(folder/'A/hat3_v10y.json')","sha(folder/'A/hat3_v10z.json')")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
