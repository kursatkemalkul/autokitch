"""Archive selected trial sources only when they match recorded run hashes."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
tag='full_candidate_balanced_03'
out=ROOT/'arastirma/3_TOPPING/sucuk_v2'
report=json.loads((out/'runs'/(tag+'.json')).read_text())
folder=out/'selected_sources';folder.mkdir(exist_ok=True)
checks={}
for name,want in report['run_source_hashes'].items():
    raw=(ROOT/'arastirma/_uretec'/name).read_bytes()
    choices=[raw]
    if name=='sucuk_v2_deney.py':
        # Only changes AFTER this selected run: an automated GUI-exit option.
        text=raw.decode('utf-8').replace("ap.add_argument('--exit-gui-after-result', action='store_true', help='GUI smoke-test only')\n",'')
        text=text.replace('while app.is_running() and not args.exit_gui_after_result:app.update()',
                          'while app.is_running():app.update()')
        choices.append(text.encode('utf-8'))
    matched=next((x for x in choices if hashlib.sha256(x).hexdigest()==want),None)
    assert matched is not None,(name,'Cannot recover exact run source: do not mislabel current code')
    (folder/name).write_bytes(matched)
    checks[name]=want
manifest={'tag':tag,'sources':checks,'geometry_and_law_hashes':{},
          'note':'Archived source is for audit; root-relative paths require original _uretec placement.',
          'production_ready':False,'food_data_calibrated':False,
          'full_stock_repeatability_validated':False}
for name in ['cad/closed_meshes.npz','cad/helezon_D_v2.step','cad/cikis_tupu_v2.step','radius_law_v2.json']:
    manifest['geometry_and_law_hashes'][name]=hashlib.sha256((out/name).read_bytes()).hexdigest()
(out/'selected_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('MATCHED_RUN_SOURCES',checks,flush=True)
