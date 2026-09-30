from pathlib import Path
import sys,os,runpy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'arastirma'/'_uretec'))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local'/'kutu-v11'
os.environ['AUTOKITCH_SEED_EXTRA']=str(ROOT.parent/'codex-kutu-main-v84'/'_local'/'kutu-v10'/'cache')
ob=R.setup()
try:runpy.run_path(str(ROOT/'arastirma'/'_uretec'/'kutu_v11_check.py'),run_name='__main__')
finally:ob.ozet();sys.stdout.flush()
os._exit(0)
