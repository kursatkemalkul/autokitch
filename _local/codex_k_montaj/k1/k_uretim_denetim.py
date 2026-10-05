"""Report full K manufacture coverage; mapping alone is not release evidence."""
from pathlib import Path
import pickle,json,hashlib
H=Path(__file__).resolve().parent
D=pickle.load((H/'plan_k.pkl').open('rb'));P=D['P']
M=json.loads((H/'native_sheet_mapping_audit.json').read_text(encoding='utf-8'));S={r['part']:r for r in M['checks']};A={r['ad']:r for r in D['ACN']}
rows=[]
for a in sorted(S):
 row={'part':a,'mapping_passed':S[a]['passed'],'laser_timeline_present':a in A,'bend_timeline_present':a in D['FRAMES'] if A.get(a,{}).get('bukum') else True,'tool_and_self_collision_verified':False}
 rows.append(row)
missing=[r['part'] for r in rows if not r['laser_timeline_present'] or not r['bend_timeline_present']]
report={'source_plan_sha256':hashlib.sha256((H/'plan_k.pkl').read_bytes()).hexdigest(),'parts':len(P),'mapped_sheet_parts':len(S),'laser_timeline_count':len(A),'mapped_sheet_timeline_missing':missing,'checks':rows,'passed':False,'open_items':['All custom K manufacturing operations need coverage and press/tool/path verification','Bench groups must show each member manufacture and attachment separately']+missing,'production_release':False}
(H/'manufacturing_coverage_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('MANUFACTURE_COVERAGE',len(S),'mapped;',len(A),'laser timelines; missing',missing)
