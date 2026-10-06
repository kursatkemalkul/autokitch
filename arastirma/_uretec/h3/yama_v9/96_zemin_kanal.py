"""Step96: remove shop fixtures and rebuild compact floor/trunking."""
from pathlib import Path
import runpy,sys
script=Path(__file__).resolve().parents[2]/'robot_integrated_v27'/'run.py'
sys.argv=[str(script),sys.argv[1],'--output',sys.argv[2]]
runpy.run_path(str(script),run_name='__main__')
