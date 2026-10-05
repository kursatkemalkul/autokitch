"""Same broad-phase coverage as the v1 failure audit, using v2 geometry."""
import os
import kk_kompakt_v2 as V
import kk_v1_carpisma_teshis_v1 as A

if __name__=='__main__':
    V.OUT.mkdir(parents=True,exist_ok=True)
    A.M.OUT=V.OUT
    A.M.build=V.build
    A.run(source_name='kk_kompakt_v2.py')
    os._exit(0)
