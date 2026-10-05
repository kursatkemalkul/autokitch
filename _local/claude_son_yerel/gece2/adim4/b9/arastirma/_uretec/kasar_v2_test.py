"""Fast tests without importing Isaac or launching physics."""
from pathlib import Path
import ast, types, json
import numpy as np
U=Path(__file__).resolve().parent
src=(U/'kasar_v2_deney.py').read_text();ns={'__file__':str(U/'kasar_v2_deney.py')}
exec(src[:src.rfind('exec(compile')],ns);compile(ns['src'],'generated','exec')
assert 'KUP_SUCUK' not in ns['src']
assert 'doz_g=55.' in ns['src']
assert 'cube_kg' not in ns['src']
print('PASS wrapper compile / correct slot / individual masses')
src=(U/'kasar_v2_izle.py').read_text();viewer={'__file__':str(U/'kasar_v2_izle.py')}
exec(src[:src.rfind('exec(compile')],viewer);compile(viewer['src'],'viewer_generated','exec')
assert 'KUP_SUCUK' not in viewer['src'] and '/SUCUK_CUBES/' not in viewer['src']
assert '/KASAR_V2_candidate_tube' in viewer['src']
print('PASS detailed-model replay compile / slot / tube visibility')
law=json.loads((U.parents[1]/'arastirma/3_TOPPING/kasar_v2/radius_law_v1.json').read_text())
knots=np.array(law['progress_knots']);radii=np.array(law['radius_knots_mm'])
assert knots[0]==0 and knots[-1]==1 and np.all(np.diff(knots)>0)
assert np.all(np.diff(radii)<=0) and radii.min()>=20 and radii.max()<=118
x=1257.5-np.sqrt(np.interp(np.linspace(0,1,2001),knots,radii)**2-20**2)
assert np.all(np.isfinite(x)) and np.all(np.diff(x)>=0)
assert np.all((x>=220)&(x<=1520))
print('PASS radius law monotonic / outward-to-inward / machine stroke')
tree=ast.parse((U/'kasar_v2_sahne.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='food_pack')
scope={'np':np}
exec(compile(ast.Module(body=[fn],type_ignores=[]),'pack','exec'),scope)
for stock in [100.,500.]:
    d,m,p=scope['food_pack'](types.SimpleNamespace(stock_g=stock,seed=7))
    assert stock<=m.sum()*1000<stock+.4
    assert np.all(p[:,2]+d[:,2]/2<=.610)
    # Sweep-axis AABB test: no initial shred-shred penetration.
    lo=p-d/2;hi=p+d/2
    for i in range(len(p)):
        near=np.flatnonzero((lo[:,2]<hi[i,2])&(hi[:,2]>lo[i,2])&(lo[:,0]<hi[i,0])&(hi[:,0]>lo[i,0])&(lo[:,1]<hi[i,1])&(hi[:,1]>lo[i,1]))
        assert len(near)==1,(i,near)
    print('PASS packing',stock,len(m),'actual_g',m.sum()*1000)
try:scope['food_pack'](types.SimpleNamespace(stock_g=1000.,seed=7))
except ValueError:print('PASS packing overflow rejected (no overlapping or oversized food)')
else:raise AssertionError('Upper loading volume guard failed')
print('TESTS_COMPLETE')
