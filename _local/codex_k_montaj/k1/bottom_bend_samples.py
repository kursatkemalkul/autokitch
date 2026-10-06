"""Sample every current source sheet; preserves canonical encoding and reports."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_bukum_ornekle.py'
code=source.read_text(encoding='utf-8')
code=code.replace('current_sheet_bending.json','current_sheet_bending_bottom.json')
code=code.replace('current_bend_samples.json','bottom_bend_samples.json')
namespace=dict(__file__=str(source),__name__=__name__)
exec(compile(code,str(source),'exec'),namespace)
Decoder=namespace['Decoder']
