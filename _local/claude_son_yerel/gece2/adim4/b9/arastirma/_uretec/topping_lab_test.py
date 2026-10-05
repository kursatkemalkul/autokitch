"""Fast regression tests for the actual lab source, packs and assembly."""
import unittest, json
import numpy as np
from pxr import Usd,UsdPhysics,UsdGeom
from topping_lab_config import *

class LabTests(unittest.TestCase):
    def test_recipe_order(self):
        self.assertEqual(RECIPES['karisik'],['kasar','sucuk'])
        self.assertEqual(RECIPES['sucuk'],['sucuk'])

    def test_validation(self):
        for v in [-1,101,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):settings(kasar=v)
        with self.assertRaises(ValueError):settings(kasar_g=0)
        self.assertEqual(settings(kasar=100,sucuk=100,dry_run=True)['fill_percent'],{'kasar':0.,'sucuk':0.})

    def test_laws(self):
        for p in PRODUCTS:
            xs=np.array([radius_x(p,t) for t in np.linspace(0,1,101)])
            self.assertTrue(np.all(np.diff(xs)>=-1e-9))
            self.assertTrue(np.all((xs>.22)&(xs<1.52)))

    def test_assembly(self):
        for variant in ['candidate','baseline']:
            s=Usd.Stage.Open(str(OUT/f'TOPPING_LAB_v1_{variant}.usd'))
            self.assertEqual(UsdGeom.GetStageUpAxis(s),'Z')
            bodies=[p for p in s.Traverse() if p.HasAPI(UsdPhysics.RigidBodyAPI)]
            self.assertEqual(len(bodies),8)
            for p in s.Traverse():
                if p.IsA(UsdPhysics.Joint):
                    for rel in [UsdPhysics.Joint(p).GetBody0Rel(),UsdPhysics.Joint(p).GetBody1Rel()]:
                        for target in rel.GetTargets():self.assertTrue(s.GetPrimAtPath(target).IsActive())
            self.assertFalse(s.GetPrimAtPath(MY+'/HELEZON_KIYMA').IsActive())
            self.assertFalse(s.GetPrimAtPath(MY+'/SABIT/ups').IsActive())
            x=UsdGeom.Xformable(s.GetPrimAtPath(MY+'/ARABA')).ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()[0]
            self.assertAlmostEqual(x+.9,.22,places=5)

    def test_charge(self):
        for product in PRODUCTS:
            if not (OUT/f'{product}_packing.json').exists():self.skipTest('Full packing still computing')
            meta=json.loads((OUT/f'{product}_packing.json').read_text())
            self.assertGreaterEqual(meta['packed_max_g'],meta['two_day_stock_g'])
            self.assertEqual(meta['max_sample_overlap_mm3'],0)
            for mode in ['hazne','stok']:
                for fill in [0,10,50,100]:
                    c=settings(mode=mode,kasar=fill,sucuk=fill);d=charge(product,c)
                    self.assertGreaterEqual(d['report']['actual_g']+1e-8,d['report']['requested_g'])
                    self.assertLess(d['report']['actual_g']-d['report']['requested_g'],1.1)
                    if fill:self.assertLessEqual(d['report']['max_initial_z_m'],meta['fill_line_world_z_m'])
            # Independent broadphase for pair overlap: all potential neighbours
            # then exact axis-aligned separation, not just nearest centres.
            from scipy.spatial import cKDTree
            d=charge(product,settings(kasar=100,sucuk=100));v=d['points'];sz=d['dimensions']
            pairs=cKDTree(v).query_pairs(float(np.linalg.norm(sz.max(0)))+.0001,output_type='ndarray')
            overlap=(sz[pairs[:,0]]+sz[pairs[:,1]])/2-np.abs(v[pairs[:,0]]-v[pairs[:,1]])
            self.assertFalse(np.any(np.all(overlap>1e-8,axis=1)))

    def test_baseline_initial_clearance(self):
        audit=json.loads((OUT/'baseline_loading_check.json').read_text())
        self.assertEqual(set(audit),set(PRODUCTS))
        for checks in audit.values():
            for item in checks:
                self.assertEqual(item['intersections'],[])
                self.assertLessEqual(item['max_overlap_mm3'],.001)

if __name__=='__main__':unittest.main(verbosity=2)
