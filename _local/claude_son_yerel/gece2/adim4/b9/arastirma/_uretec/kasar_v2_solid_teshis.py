from pathlib import Path
import cadquery as cq
root=Path(__file__).resolve().parents[2]/'arastirma/3_TOPPING/kasar_kabi_v14/step'
for c in 'ABCD':
    s=cq.importers.importStep(str(root/f'helezon_{c}.step')).val();sol=s.Solids()
    print(c,'solids',len(sol),flush=True)
    for i,t in enumerate(sol):
        b=t.BoundingBox()
        print(i,t.Volume(tol=1e-7),[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],flush=True)
    if len(sol)>1:
        print('distance',sol[0].distance(sol[1]),'overlap',sol[0].intersect(sol[1]).Volume(),flush=True)
        fused=sol[0].fuse(*sol[1:],tol=.0001).clean()
        print('FUSED',len(fused.Solids()),fused.isValid(),fused.Volume(tol=1e-7),flush=True)
