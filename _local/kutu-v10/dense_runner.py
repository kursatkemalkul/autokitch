"""Independent validation cache; never writes the simultaneous main build cache."""
import os,sys,runpy
from pathlib import Path
U=Path(__file__).resolve().parents[2]/'arastirma'/'_uretec'
sys.path.insert(0,str(U))
import kutu_v10_build as R
args=sys.argv[1:]
R.PRIVATE=Path(__file__).resolve().parent/('validation-interfaces' if 'interfaces' in args else 'validation-beam' if 'beam' in args else 'validation')
ob=R.setup()
sys.argv=['kutu_v10_check.py','dense']+args
try:
    runpy.run_path(str(U/'kutu_v10_check.py'),run_name='__main__')
except BaseException:
    import traceback
    traceback.print_exc()
    code=1
else:code=0
ob.ozet();sys.stdout.flush();sys.stderr.flush();os._exit(code)
