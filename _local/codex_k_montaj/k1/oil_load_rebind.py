"""Verify every new load-mount triangle against the previous verified source."""
from pathlib import Path
source=Path(__file__).with_name('oil_rebind_ownership.py')
code=source.read_text(encoding='utf-8')
for old,new in [('k_parca_bottom_verified.pkl','k_parca_oil_verified.pkl'),
                ('oil_shelf_mount_candidate','oil_load_mount_candidate'),('hat3_v10y','hat3_v10z'),
                ('k_parca_oil_raw.pkl','k_parca_oil_load_raw.pkl'),
                ('k_parca_oil_verified.pkl','k_parca_oil_load_verified.pkl'),
                ('oil_ownership_rebind_audit.json','oil_load_ownership_rebind_audit.json'),
                ('surface_ownership_registry_oil.json','surface_ownership_registry_oil_load.json')]:
    # Avoid replacing the just-renamed previous input with the output name.
    if old=='k_parca_bottom_verified.pkl':code=code.replace(old,'PREVIOUS_OIL_INPUT.pkl')
    else:code=code.replace(old,new)
code=code.replace('PREVIOUS_OIL_INPUT.pkl','k_parca_oil_verified.pkl')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
