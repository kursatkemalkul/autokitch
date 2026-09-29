from pathlib import Path
import sys,runpy,os,traceback
ROOT=Path(__file__).resolve().parents[2]
U=ROOT/'arastirma'/'_uretec'
sys.path.insert(0,str(U))
import kutu_v10_build as R
R.PRIVATE=ROOT/'_local'/'kutu-v10'/'validation-static'
ob=R.setup()
sys.argv=['kutu_v10_check.py','static']
code=0
try:runpy.run_path(str(U/'kutu_v10_check.py'),run_name='__main__')
except BaseException:
    traceback.print_exc();code=1
ob.ozet();sys.stdout.flush();os._exit(code)
