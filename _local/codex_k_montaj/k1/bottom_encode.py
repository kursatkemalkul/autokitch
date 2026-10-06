"""Encode current80 physical source sheets; retain all bores and native bends."""
from pathlib import Path
H=Path(__file__).resolve().parent;template=H/'din_encode.py';source=H/'k_sac_guncelle.py'
namespace=dict(__file__=str(template),__name__='encoding_template')
exec(template.read_text(encoding='utf-8').split("code=code.replace(anchor,addition+'\\n'+anchor)")[0],namespace)
code=namespace['code'].replace('k_parca_din_verified.pkl','k_parca_bottom_verified.pkl').replace('_din.json','_bottom.json')
code=code.replace("'k72_itici_ust_plaka_'","'k72_itici_ust_plaka_','k72_bant_ayak_flansi_'")
addition=namespace['addition'].replace('_din.json','_bottom.json')
addition+='''
for name in sorted(n for n in P if n.startswith('k79_bant_ust_tapa_') or (n.startswith('k79_bant_disli_plaka_') and 'kaynagi' not in n)):
 v=P[name]['V'];lo=v.min(0);hi=v.max(0);span=hi-lo
 cap=name.startswith('k79_bant_ust_tapa_');t=2. if cap else 6.;width=20. if cap else 16.
 assert np.allclose(span,[width,t,width],atol=.002),(name,span)
 flat=S.Sac(name,'braket',t=t,R=1.5*t,birim='K_BANT')
 flat.taban([(0,0),(width,0),(width,width),(0,width)],O=(lo[0],lo[1],hi[2]),ex=(1,0,0),ey=(0,0,-1))
 sheets[name]=flat;old['sheets'].append({'name':name})
 flat_rows.append({'name':name,'thickness_mm':t,'normal_axis':'Y','native_stock_bounds_mm':[lo.tolist(),hi.tolist()],
                  'source':'verified bottom-access source mesh','holes_from_current_mesh_preserved':True,
                  'machining_verified':False,'secondary_machining_required':not cap,
                  'secondary_operation':None if cap else 'Drill5.0 and tap M6 through6mm stock before welding; actual threaded surface remains nominal proxy'})
(HERE/'custom_flat_stock_audit_bottom.json').write_text(json.dumps(clean({'parts':flat_rows,'production_release':False}),indent=2),encoding='utf-8')
'''
anchor='records=[];audit=[]';assert anchor in code
code=code.replace(anchor,addition+'\n'+anchor)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
