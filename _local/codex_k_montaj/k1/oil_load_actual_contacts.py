"""Measure all fourteen oil wall/load mounting joints in the actual source."""
from pathlib import Path
source=Path(__file__).with_name('oil_actual_contacts.py')
code=source.read_text(encoding='utf-8').replace('k_parca_oil_verified.pkl','k_parca_oil_load_verified.pkl')
code=code.replace('oil_shelf_mount_candidate','oil_load_mount_candidate').replace('oil_actual_contacts.json','oil_load_actual_contacts.json')
anchor="r={'source_model_sha256':scope['output_sha256'],"
assert anchor in code
code=code.replace(anchor,"""for j in definition['load_joins']:
    for a,b in ((j['screw'],j['carrier']),(j['shim'],j['host']),
                (j['washer'],j['shim']),(j['nut'],j['washer']),
                (j['screw'],j['nut']),(j['carrier'],j['host'])):
        r=contact(a,b);r['joint']=j['id'];rows.append(r)
rows.extend([contact('k79_yag_raf_on_dayama_kaynagi',a)
             for a in ('yag_pompa_rafi','k79_yag_raf_on_dayama')])
"""+anchor)
code=code.replace('Shelf-to-brackets and pump plate-to-shelf fastening, assembly paths and manufacturing processes.',
                  'Pump-to-plate mounting, complete assembly paths and manufacturing processes remain open.')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
