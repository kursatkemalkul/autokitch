"""Step97: fixed-rail open-side box turn; animation-only patch."""
from pathlib import Path
import runpy,sys
script=Path(__file__).resolve().parents[2]/'robot_integrated_v28'/'run.py'
sys.argv=[str(script),sys.argv[1],sys.argv[2]]
runpy.run_path(str(script),run_name='__main__')
