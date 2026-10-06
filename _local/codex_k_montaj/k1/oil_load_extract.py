"""Read load-mount source once using the existing cache extractor."""
from pathlib import Path
source=Path(__file__).with_name('oil_extract.py')
code=source.read_text(encoding='utf-8')
for old,new in [('oil_shelf_mount_candidate','oil_load_mount_candidate'),
                ('hat3_v10y','hat3_v10z'),('k_bil_oil.pkl','k_bil_oil_load.pkl'),
                ('k_parca_oil_raw.pkl','k_parca_oil_load_raw.pkl'),
                ('oil_raw_part_audit.json','oil_load_raw_part_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
