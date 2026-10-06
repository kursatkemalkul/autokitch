"""Encode verified belt caps without replacing current source triangles."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'din_encode.py'
code=source.read_text(encoding='utf-8').replace('k_parca_din_verified.pkl','k_parca_belt_verified.pkl').replace('_din.json','_belt.json')
anchor="code=code.replace(anchor,addition+'\\n'+anchor)"
assert anchor in code
caps='''
# Actual 2mm rounded caps: stock outline locates the original triangles.
# No bending or machining certification is inferred from closure.
cap_audit=json.loads((HERE.parent/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))
for joint in cap_audit['joints']:
 name=joint['cap'];v=P[name]['V'];lo=v.min(0);hi=v.max(0);span=hi-lo
 assert np.allclose(span,[20.,2.,20.],atol=.001),(name,span)
 flat=S.Sac(name,'braket',t=2.,R=3.,birim='K_BANT')
 flat.taban([(0,0),(20,0),(20,20),(0,20)],O=(lo[0],lo[1],hi[2]),ex=(1,0,0),ey=(0,0,-1))
 sheets[name]=flat;old['sheets'].append({'name':name})
 flat_rows.append({'name':name,'thickness_mm':2.,'normal_axis':'Y','native_stock_bounds_mm':[lo.tolist(),hi.tolist()],
                  'source':'verified belt support source mesh','holes_from_current_mesh_preserved':True,
                  'machining_verified':False,'secondary_machining_required':False,'corner_radius_mm':4.})
(HERE/'custom_flat_stock_audit_belt.json').write_text(json.dumps(clean({'parts':flat_rows,'production_release':False}),indent=2),encoding='utf-8')
'''
code=code.replace(anchor,"addition += "+repr(caps)+"\n"+anchor)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__',H=H))

