"""Source-bound supersession writer for K prototypes.

Retains v6 inherited labels and exact triangle ownership matching. Explicit
removed parts are never represented by empty/fake solids or hidden geometry.
"""
from pathlib import Path
source=Path(__file__).with_name('78_k_sac_topolojisi.py')
code=source.read_text(encoding='utf-8')
code=code.replace("additional_parts=None):","additional_parts=None,removed_parts=None):")
anchor="wanted={a:Counter(key(t) for t in r['original_triangles']) for a,r in repairs.items()}"
replace="""removals=removed_parts or {}
 assert not set(removals)&set(repairs)
 assert all(r.get('reason') and len(r['original_triangles']) for r in removals.values())
 wanted={a:Counter(key(t) for t in r['original_triangles']) for a,r in dict(repairs,**removals).items()}"""
assert anchor in code;code=code.replace(anchor,replace)
code=code.replace('assert set(templates)==set(repairs)','assert set(templates)==set(repairs)|set(removals)')
anchor="if additional_parts:\n  report['added_parts']"
replace="""if removals:
  report['removed_parts']={a:{'reason':r['reason'],'source_triangles':len(r['original_triangles'])} for a,r in removals.items()}
  report['source_interfaces_intended_unchanged']=False
 if additional_parts:
  report['added_parts']"""
assert anchor in code;code=code.replace(anchor,replace)
namespace=dict(__file__=str(source),__name__='bound_removal_library')
exec(compile(code,str(source),'exec'),namespace)
apply=namespace['apply']
