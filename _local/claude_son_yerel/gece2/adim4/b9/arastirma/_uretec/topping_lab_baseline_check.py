"""Check candidate initial food against the different baseline outlet parts.

B/C cheese repairs retain occupied geometry (prior CAD audit); only D and
the outlet tube differ in the loading envelope. No positions are changed.
"""
import hashlib,json,os,sys
import numpy as np
import cadquery as cq
from topping_lab_config import ROOT,OUT,PRODUCTS,settings,charge

def check():
    # Keep CAD handles local; only plain numerical audit records escape.
    result={}
    for product,folder in [('kasar','kasar_kabi_v14'),('sucuk','sucuk_kaseti_v7')]:
        data=charge(product,settings(kasar=100,sucuk=100))
        pos=data['points']*1000
        pos=np.column_stack([pos[:,0]-PRODUCTS[product]['x']*1000,pos[:,2]-260,362.5-pos[:,1]])
        size=data['dimensions'][:,[0,2,1]]*1000
        checks=[]
        for part in ['helezon_D','cikis_tupu']:
            path=ROOT/'arastirma/3_TOPPING'/folder/'step'/(part+'.step')
            shape=cq.importers.importStep(str(path)).val();b=shape.BoundingBox()
            lo=np.array([b.xmin,b.ymin,b.zmin]);hi=np.array([b.xmax,b.ymax,b.zmax])
            ids=np.flatnonzero(np.all(pos+size/2>=lo,axis=1)&np.all(pos-size/2<=hi,axis=1))
            maximum=0.;bad=[]
            for i in ids:
                box=cq.Solid.makeBox(*size[i],cq.Vector(*(pos[i]-size[i]/2)))
                overlap=box.intersect(shape).Volume(tol=1e-6)
                maximum=max(maximum,overlap)
                if overlap>.001:bad.append(dict(index=int(i),overlap_mm3=overlap))
            row=dict(part=part,candidate_boxes=len(ids),max_overlap_mm3=maximum,intersections=bad,
                     source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            checks.append(row);print(product,part,len(ids),maximum,flush=True)
        result[product]=checks
    assert not any(c['intersections'] for checks in result.values() for c in checks),'Baseline food overlaps original geometry'
    return result

if __name__=='__main__':
    result=check()
    (OUT/'baseline_loading_check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('BASELINE_INITIAL_CLEARANCE_PASS',flush=True)
    # This installed OpenCascade build faults during interpreter teardown,
    # also with local handles. Same batch-CLI workaround as the CAD generators:
    # only after every assertion and file close, flush and bypass teardown.
    # Calculation/assertion errors still propagate normally before this point.
    sys.stdout.flush();sys.stderr.flush();os._exit(0)
