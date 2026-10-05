"""Repair the inherited invalid equal-radius elbow without closing its bore."""
from pathlib import Path
import cadquery as cq
import kasar_cad_v14 as o
def build():
    zc=(o.AG_Z0+o.AG_Z1)/2
    t=o.silz(0,o.CY,25.,o.ZF-1.3,o.TUP_Z1)
    f=o.silz(0,o.CY,31.,o.ZF,o.ZF+5).union(o.kut(-41,41,o.CY-9,o.CY+9,o.ZF,o.ZF+5))
    # 0.05 mm radial difference removes the coincident cylinder seam.
    branch=o.sily(0,zc,25.05,o.BORU_ALT,o.CY)
    t=t.union(f).union(branch).cut(o.silz(0,o.CY,22.,o.ZF-4,o.TUP_Z1+1))
    t=t.cut(o.sily(0,zc,22.05,o.BORU_ALT-1,o.CY+1))
    for sign in [-1,1]:t=t.cut(o.silz(sign*33,o.CY,2.25,o.ZF-1,o.ZF+6))
    t=o.BR.tirnak_ekle(t,25.,o.CY)
    return t.val()
if __name__=='__main__':
    s=build();print('TUBE',s.isValid(),len(s.Solids()),s.Volume(),flush=True)
    assert s.isValid() and len(s.Solids())==1
    out=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING/kasar_v2/cad/cikis_tupu_v15.step'
    cq.exporters.export(s,str(out))
