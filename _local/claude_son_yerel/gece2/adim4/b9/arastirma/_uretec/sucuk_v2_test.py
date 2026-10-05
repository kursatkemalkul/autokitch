"""Fast invariants. Not a substitute for PhysX runs or food calibration."""
from pathlib import Path
import ast, json, unittest, itertools, types
import numpy as np

HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'3_TOPPING/sucuk_v2'

class V2Invariants(unittest.TestCase):
    def test_asserted_wrapper_transforms_compile(self):
        for name in ['sucuk_v2_deney.py','sucuk_v2_izle.py']:
            path=HERE/name
            tree=ast.parse(path.read_text(encoding='utf-8'))
            last=tree.body.pop()
            self.assertIsInstance(last,ast.Expr)
            self.assertEqual(last.value.func.id,'exec')
            env={'__file__':str(path),'__name__':'validation_only'}
            exec(compile(tree,str(path),'exec'),env)
            compile(env['src'],str(path),'exec')
            self.assertNotIn('len(emitted)*cube_kg*1000',env['src']) if name.startswith('sucuk_v2_deney') else None

    def test_radius_laws_monotonic_and_reachable(self):
        for path in OUT.glob('radius_law_v*.json'):
            law=json.loads(path.read_text())
            t=np.array(law['progress_knots']);r=np.array(law['radius_knots_mm'])
            self.assertEqual(len(t),len(r))
            self.assertTrue(np.isfinite(t).all() and np.isfinite(r).all())
            self.assertTrue((np.diff(t)>0).all())
            self.assertTrue((np.diff(r)<=0).all())
            self.assertEqual(float(t[0]),0.);self.assertEqual(float(t[-1]),1.)
            self.assertTrue(((r>17.5)&(r<=125)).all())

    def test_full_stock_initial_pack_no_intersections(self):
        tree=ast.parse((HERE/'sucuk_v2_sahne.py').read_text())
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='food_pack')
        env={'np':np}
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'food_pack_only','exec'),env)
        a=types.SimpleNamespace(seed=7,stock_g=2800,mixed=True,count=600)
        sizes,masses,positions=env['food_pack'](a)
        self.assertEqual(len(sizes),5315)
        self.assertTrue(2800<=masses.sum()*1000<2801)
        self.assertTrue(((sizes>=.006)&(sizes<=.010)).all())
        lo=positions-sizes[:,None]/2;hi=positions+sizes[:,None]/2
        # Arithmetic roundoff only: tolerance is 0.1 nanometre, not a fit allowance.
        self.assertTrue((lo>=np.array([1.4725-.065,.212,.474])-1e-10).all(),lo.min(0))
        self.assertTrue((hi<=np.array([1.4725+.065,.515,.610])+1e-10).all(),hi.max(0))
        cells={};checked=0
        for i,p in enumerate(positions):
            c=tuple(np.floor(p/.01).astype(int))
            for delta in itertools.product([-1,0,1],repeat=3):
                key=tuple(c[k]+delta[k] for k in range(3))
                for j in cells.get(key,[]):
                    overlap=np.minimum(hi[i],hi[j])-np.maximum(lo[i],lo[j])
                    self.assertFalse((overlap>1e-9).all(),(i,j,overlap))
                    checked+=1
            cells.setdefault(c,[]).append(i)
        self.assertGreater(checked,len(sizes))

if __name__=='__main__':unittest.main(verbosity=2)
