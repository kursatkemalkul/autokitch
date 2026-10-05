"""Invert actual source vertices into flat/folded native sheet coordinates."""
from lower_support import *

def encode_sheet(sheet,triangles,offset,stock_outline=False):
    V,F=np.unique(triangles.reshape(-1,3),axis=0,return_inverse=True);F=F.reshape(-1,3)
    pk,_=sheet._yerel_katilar();encoded=[];missing=[];worst=0.
    if stock_outline:
        # Current mesh already contains authoritative through holes and machining.
        # Inverse-map its exact vertices against panel stock, not obsolete source
        # hole seats. This never fills holes or changes triangles or bend geometry.
        pk={p.no:cq.Solid.extrudeLinear(S.yuz_poligon(p.poly).outerWire(),[],cq.Vector(0,0,sheet.t)) for p in sheet.paneller}
    for index,world in enumerate(V):
        point=world-np.array(offset);record=None;reconstructed=None
        for panel in sheet.paneller:
            sh=pk.get(panel.no)
            if sh is None:continue
            local=S._p(np.linalg.inv(panel.M),point);bb=sh.BoundingBox()
            if not(bb.xmin-.001<=local[0]<=bb.xmax+.001 and bb.ymin-.001<=local[1]<=bb.ymax+.001 and -.001<=local[2]<=sheet.t+.001):continue
            # Source chamfers/countersinks remove stock after the laser/bend
            # operations. Their surface vertices may be inside the unmachined
            # native panel, not on its boundary. This locates vertices only;
            # the missing machining operation remains a separate release gate.
            # Boolean hole chords can lie ~0.003mm inside the ideal cylinder.
            # Identification uses the declared model acceptance tolerance;
            # reconstruction still keeps the original vertex exactly.
            if sh.distance(cq.Vertex.makeVertex(*local))>.01 and not sh.isInside(cq.Vector(*local),.001):continue
            record={'panel':panel.no,'point':local.tolist()};reconstructed=S._p(panel.M,local);break
        if record is None:
            for B in sheet.bukumler:
                local=S._p(np.linalg.inv(B.ebeveyn.M),point);A=B.p0+np.array([0.,0.,sheet.t+B.R if B.yon>0 else -B.R]);diff=local-A;w=float(diff@B.e3);radial=diff-B.e3*w
                refvec=np.array([0.,0.,-1. if B.yon>0 else 1.]);ang=float(np.arctan2(radial@np.cross(B.k,refvec),radial@refvec));rho=float(np.linalg.norm(radial))
                if not(-.001<=ang/B.th<=1.001 and B.R-.001<=rho<=B.R+sheet.t+.001 and B.a-.001<=w<=B.b+.001):continue
                s=ang/B.th*B.BA;z=sheet.t+B.R-rho if B.yon>0 else rho-B.R;record={'bend':B.no+1,'point':[s,w,z]};r0=np.array([0.,0.,-(B.R+sheet.t-z) if B.yon>0 else B.R+z]);reconstructed=S._p(B.ebeveyn.M,A+S._rot(B.k,ang)@r0+B.e3*w);break
        if record is None:missing.append(index);encoded.append(None)
        else:encoded.append(record);worst=max(worst,float(np.linalg.norm(reconstructed-point)))
    bends=[{'number':B.no+1,'parent':B.ebeveyn.no,'child':B.cocuk.no,'angle':B.th,'direction':B.yon,'BA':B.BA,'K':B.K,'p0':B.p0.tolist(),'axis':B.k.tolist(),'out':B.o3.tolist(),'edge':B.e3.tolist(),'flat_child':B.Ld.tolist()} for B in sheet.bukumler]
    order=next((r.get('sira') for r in sheet.dfm(abkant=True) if r.get('kural')=='abkant'),None) or [B.no+1 for B in sheet.bukumler]
    return {'name':sheet.ad,'root':sheet.paneller[0].M.tolist(),'source_offset':list(offset),'t':sheet.t,'vertices':V.tolist(),'triangles':F.tolist(),'encoded_vertices':encoded,'bends':bends,'order':order,'classification_surface_tolerance_mm':.01,'unclassified_vertices':missing,'folded_endpoint_max_error_mm':worst,'endpoint_passed':not missing and worst<=.01}
