"""Add new step71 shelf and step73 source-preserving roof to bending data."""
from bend_encode import *
from roof_mounts import build_roof
Y=H/'yama_v9'
for path in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
g=Glb(str(OUT/'k73a.glb'));parts,_,shelf=build();roof_parts,_,roof=build_roof()
data=json.loads((OUT/'source_bending.json').read_text(encoding='utf8'));rows=[]
for sheet,shape,name,offset in ((shelf,parts[-1]['sh'],'K_GOVDE__sac',[0,0,0]),(roof,roof_parts[0]['sh'],'K_GOVDE__kabuk',[4000,0,0])):
    bb=shape.BoundingBox();lo=np.array([bb.xmin,bb.ymin,bb.zmin]);hi=np.array([bb.xmax,bb.ymax,bb.zmax]);g.bilesen(name,0)
    candidates=[b for b in g._bc[name] if max(np.max(np.abs(b['lo']-lo)),np.max(np.abs(b['hi']-hi)))<.01]
    assert len(candidates)==1,(sheet.ad,len(candidates))
    b=candidates[0];triangles=np.concatenate([p['X'][p['T'][idx]] for p,idx in b['parca']]);rec=encode_sheet(sheet,triangles,offset);rec['source_component']=f'{name}[{b["no"]}]'
    row={k:rec[k] for k in ('name','endpoint_passed','unclassified_vertices','folded_endpoint_max_error_mm')}
    row['unclassified_examples']=[{'world_mm':rec['vertices'][i],'native_distance_mm':sheet.kati().distance(cq.Vertex.makeVertex(*(np.array(rec['vertices'][i])-offset)))} for i in rec['unclassified_vertices'][:12]]
    rows.append(row);print('NEW_SOURCE_BEND',sheet.ad,'unclassified',len(rec['unclassified_vertices']),'error',rec['folded_endpoint_max_error_mm'],json.dumps(row['unclassified_examples']),flush=True)
    if rec['endpoint_passed']:data['sheets'].append(rec)
report={'checks':rows,'passed':all(r['endpoint_passed'] for r in rows),'full_assembly_release':False}
(OUT/'updated_sheet_bending_audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf8')
# Never overwrite accepted output with a partly unclassified new sheet.
if report['passed']:(OUT/'source_bending_updated.json').write_text(json.dumps(clean(data),separators=(',',':')),encoding='utf8')
sys.stdout.flush();os._exit(0 if report['passed'] else 2)
