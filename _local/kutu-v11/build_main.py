from pathlib import Path
import sys,os,runpy,json
ROOT=Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'arastirma'/'_uretec'))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local'/'kutu-v11'
os.environ['AUTOKITCH_SEED_EXTRA']=os.pathsep.join(str(ROOT.parent/n/'_local'/k/'cache') for n,k in [('codex-kutu-v11','kutu-v11'),('codex-kutu-main-v84','kutu-v10')])
check=json.loads((R.PRIVATE/'check.json').read_text())
assert not check['collisions'] and not check['invalid'] and not check['envelope']
assert len(check['support'])==29 and all(r[1]<.05 for r in check['support'])
ob=R.setup()
try:runpy.run_path(str(ROOT/'arastirma'/'_uretec'/'hat_montaj_v85.py'),run_name='__main__')
except BaseException:
    import traceback
    traceback.print_exc();sys.stdout.flush();os._exit(1)
ob.ozet();sys.stdout.flush();os._exit(0)
