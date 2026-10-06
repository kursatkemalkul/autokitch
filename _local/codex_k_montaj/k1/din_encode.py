"""Re-encode source sheets plus the newly bored4mm panel from current mesh.

Separate caches until all source/closure checks pass. Countersink machining
is explicitly still an open manufacturing operation, not called laser cutting.
"""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_sac_guncelle.py'
code=source.read_text(encoding='utf-8')
code=code.replace("'k_parca.pkl'","'k_parca_din_verified.pkl'")
for name in ('custom_flat_stock_audit','current_sheet_encoding_audit','current_sheet_bending'):
 code=code.replace(f"'{name}.json'",f"'{name}_din.json'")
# Rear sheet has current panel mounting holes at1477; the native factory
# still has the earlier hole pattern. Locate vertices against unchanged stock
# outline while keeping every current hole triangle and every native bend.
code=code.replace("stock_outline=(name=='ust_sac' or", "stock_outline=(name in ('ust_sac','arka_sac') or")
anchor='records=[];audit=[]'
assert anchor in code
addition="""
# Pano is an actual4mm stock plate. Preserve all current bore/countersink
# triangles and annotate secondary machining; no fake abkant is added.
name='pano_plakasi';v=P[name]['V'];lo=v.min(0);hi=v.max(0);span=hi-lo
assert abs(span[2]-4.)<.001 and abs(span[0]-305.)<.001 and abs(span[1]-390.)<.001
flat=S.Sac(name,'braket',t=4.,R=6.,birim='K_ELEKTRIK')
flat.taban([(0,0),(span[0],0),(span[0],span[1]),(0,span[1])],O=lo,ex=(1,0,0),ey=(0,1,0))
sheets[name]=flat;old['sheets'].append({'name':name})
flat_rows.append({'name':name,'thickness_mm':4.,'normal_axis':'Z','native_stock_bounds_mm':[lo.tolist(),hi.tolist()],
                 'source':'verified DIN panel candidate','holes_from_current_mesh_preserved':True,
                 'machining_verified':False,'secondary_operation':'Countersink4 panel M5x20 holes on front and4 DIN M5x12 holes on rear; laser alone does not make countersinks'})
(HERE/'custom_flat_stock_audit_din.json').write_text(json.dumps(clean({'parts':flat_rows,'production_release':False}),indent=2),encoding='utf-8')
"""
code=code.replace(anchor,addition+'\n'+anchor)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
