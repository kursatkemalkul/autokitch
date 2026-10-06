"""Read changed private clip source once using the existing K extractor."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'head_extract.py'
code=source.read_text(encoding='utf-8')
for old,new in [('cut_head_yoke_candidate','electrical_clip_weld_candidate'),('hat3_v10zd','hat3_v10ze'),
 ('k_bil_head','k_bil_clip'),('k_parca_head_raw','k_parca_clip_raw'),('head_raw_part_audit','clip_raw_part_audit')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
