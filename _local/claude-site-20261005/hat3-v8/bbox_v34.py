import sys, os, glob
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

d = sys.argv[1]
for f in sorted(glob.glob(os.path.join(d, '*.stp'))):
    r = STEPControl_Reader()
    st = r.ReadFile(f)
    if st != IFSelect_RetDone:
        print(os.path.basename(f), 'READ FAIL'); continue
    r.TransferRoots()
    shp = r.OneShape()
    b = Bnd_Box(); b.SetGap(0.0)
    BRepBndLib.Add_s(shp, b, True)
    x0, y0, z0, x1, y1, z1 = b.Get()
    print('%s|%.1f|%.1f|%.1f|%.1f,%.1f,%.1f|%.1f,%.1f,%.1f' % (os.path.basename(f), x1-x0, y1-y0, z1-z0, x0, y0, z0, x1, y1, z1))
