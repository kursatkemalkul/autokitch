"""Modular station revision. Millimetres; v69 process geometry is retained.

Not a lifting certification. Rated loads below are design envelopes that require
verification against the finished machine's mass, welds, feet and installation.
"""
import json, math, os, csv, sys, time
from pathlib import Path
from load_source import load, OUT, ROOT, HERE
import cadquery as cq

PARTS=[]; CHANGES=[]; CHECKS=[]
V=cq.Vector
def box(x0,x1,y0,y1,z0,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,V(x0,y0,z0))
def bb(s):
    b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
def overlap(a,b,t=.05):return all(min(a[2*i+1],b[2*i+1])-max(a[2*i],b[2*i])>t for i in range(3))
def add(name,mod,shape,mat='304',kind='frame',note='',new=True):
    if isinstance(shape,cq.Workplane):shape=shape.val()
    p=dict(name=name,module=mod,shape=shape,material=mat,kind=kind,note=note,new=new);PARTS.append(p);return p
def rhs(name,mod,b,axis,t=3,note=''):
    inner=list(b)
    for i in range(3):
        inner[2*i]+= -1 if i==axis else t;inner[2*i+1]+=1 if i==axis else -t
    return add(name,mod,box(*b).cut(box(*inner)),note=note)
def cyl_y(x,z,r,y0,y1):return cq.Solid.makeCylinder(r,y1-y0,V(x,y0,z),V(0,1,0))

def source(M):
    def append(name,mod,s,mat,unit,group='SABIT'):
        # Only the six machine stations. No robot / QR / counter changes.
        if group in ('URUN','URUN_IZ','REF','SPREY'):return
        b=bb(s);kind='inside'
        if mod=='C' and b[0]<699:
            mod='A' if b[1]<=700.1 else 'T'
        if mod=='C' and name.startswith(('tabla_','tekne','kiris_','ray_','x_','kayis_','avara_','enerji_zinciri','apron','enkoder_')):mod='T'
        if any(k in name for k in ('sac','duvar','yalitim','pu_','kapak','govde','profil','kaide','dikme','kusak','ayak','onyuz')):kind='shell'
        if 'pu'==mat or 'yalitim_gorunur'==mat:mat='PU';kind='insulation'
        if mat=='on_seffaf':mat='304';kind='front'
        add(name,mod,s,mat,kind,note=unit,new=False)
    for p in M.TC.PARCALAR:
        if not M.v1_kalir(p['ad']) or p['ad'] in ('on_kapak','on_kapak_contasi','on_kapak_pu') or p['ad'] in M.AKTARMA_TP10:continue
        d=M.V1_TASI.get(p['ad'],(0,0,0));s=p['wp'].val().translate(V(M.X_BC+d[0],M.Y_MEK+d[1],d[2]))
        if p['ad']=='cikis_yarigi_contasi':s=M.YARIK_V2
        append(p['ad'],'C',s,p['mal'],'TOPPING')
    for p in M.TU.P:
        if p['ad'].startswith(M.V3_CIKAN):continue
        append(p['ad'],'C',p['sh'].translate(V(M.X_BC,0,0)),p['mal'],'TOPPING')
    for p in M.TU.P:
        if p['ad'].startswith('kompresor_'):
            append(p['ad'],'F',p['sh'].translate(V(M.X_BC+M.KOMP_KAY[0],M.KOMP_KAY[1],M.KOMP_KAY[2])),p['mal'],'HAVA')
    for m,mod in [(M.SC,'B'),(M.KS,'K'),(M.KC,'E')]:
        for p in m.PARCALAR:
            if mod=='E' and p['ad'].startswith(('robot_catal_','robot_flansi','REF_')):continue
            s=p['wp'].val();s=s.translate(V(M.X_K if mod=='K' else M.X_E if mod=='E' else 0,0,0))
            append(p['ad'],mod,s,p['mal'],p.get('birim',mod),p.get('grup','SABIT'))
    for m,mod in [(M.AK,'A'),(M.KD,None),(M.FT,'F'),(M.FU,'F'),(M.BM,'K'),(M.IT,'C')]:
        for p in m.PARCALAR:append(p['ad'],mod or ('A' if p['birim']=='KAIDE_A' else 'C'),m.dunya(p),p['mal'],p['birim'],p.get('grup','SABIT'))
    return PARTS

def independent_A(M):
    # Independent right wall, keeping process throat and pneumatic penetrations.
    wall=box(698,699.5,893.5,1860.5,-828.5,59)
    throat=box(697,701,892.5,1042.5,-510.5,5.5)
    wall=wall.cut(throat)
    for y,z in M.TC.RAKOR_ACICI:
        wall=wall.cut(cq.Solid.makeCylinder(7,4,V(697,y+M.Y_MEK,z),V(1,0,0)))
    # Shift only A's right frame members, not machinery, to make room for sheet.
    for p in PARTS:
        if p['module']!='A' or p['note'] not in ('A_GOVDE','A_ONYUZ'):continue
        b=bb(p['shape'])
        if b[0]>=650 and ('sag' in p['name'] or 'lama' in p['name']):
            p['shape']=p['shape'].translate(V(-2,0,0));CHANGES.append(p['name']+': right frame -2 mm, section unchanged')
        elif 'kusak_arka' in p['name'] or 'kayit_ust' in p['name']:
            p['shape']=p['shape'].intersect(box(-10,668,780,1900,-850,100))
    add('A_bagimsiz_sag_duvar_1p5','A',wall,kind='shell',note='304 1.5; own right wall; removable shared rail throat preserved')
    # Gasket only in outer seam; never obstruct the transfer opening.
    seal=box(699.5,700,893.5,1860.5,-828.5,59).cut(box(699,701,903.5,1850.5,-818.5,49)).cut(throat)
    add('A_C_sokulur_cevre_contasi','A',seal,'EPDM','gasket','0.5 installed seam, final gasket compression to supplier specification')
    # Clip remaining sheet/corner overlaps to the new plate, not mechanisms.
    for p in PARTS:
        if p['new'] or p['module']!='A' or p['note'] not in ('A_GOVDE','A_ONYUZ','KAIDE_A'):continue
        if overlap(bb(p['shape']),bb(wall)):
            v=abs(p['shape'].intersect(wall).Volume())
            if v>.1:p['shape']=p['shape'].cut(wall);CHANGES.append(p['name']+': sheet interface relief')

def lower_frame(mod,x0,x1,feet):
    # RHS 40 wide x 60 high x 3, entirely in the existing plinth envelope.
    zs=sorted(set(round(z,2) for x,z in feet));half=30 if mod=='B' else 20;y0=43 if mod=='B' else 63
    members=[]
    for i,z in enumerate(zs):
        xs=[x for x,zz in feet if abs(z-zz)<.1]
        if len(xs)<2:continue
        lo,hi=(1.5,3998.5) if mod=='B' and z in (-110,-760) else (min(xs)-20,max(xs)+20)
        members.append(rhs(mod+'_alt_sasi_boyuna_'+str(i),mod,(lo,hi,y0,123,z-half,z+half),0,note=('60x80x3' if mod=='B' else '40x60x3')+' RHS; continuous bearing under floor; no shell lifting'))
    # Cross members over corner feet; intersections mitred by exact subtraction.
    for i,x in enumerate(sorted(set(round(x,2) for x,z in feet))):
        local=[z for xx,z in feet if abs(x-xx)<.1]
        if len(local)<2:continue
        extra=mod=='E' and len([xx for xx,zz in feet if zz==min(local)])==1
        r=rhs(mod+'_alt_sasi_enine_'+str(i),mod,(x-half,x+half,y0,123,min(local)+(-half if extra else half),max(local)+(half if extra else -half)),2,note='RHS; welded to longitudinal rail')
        for other in members:
            if overlap(bb(r['shape']),bb(other['shape'])):r['shape']=r['shape'].cut(box(*bb(other['shape'])))
        solids=r['shape'].Solids();r['shape']=solids[0];segments=[r]
        for k,s in enumerate(solids[1:]):segments.append(add(r['name']+'_segment_'+str(k+1),mod,s,note='separate RHS segment, end welded to longitudinal member'))
        members.extend(segments)
    for x,z in feet:
        bore=cyl_y(x,z,6.5,y0-1,124)
        for p in members:
            if overlap(bb(p['shape']),bb(bore)):p['shape']=p['shape'].cut(bore)
        nut=box(x-12,x+12,108,120,z-12,z+12).cut(cyl_y(x,z,6.5,107,121))
        add(mod+'_M12_ayak_yuvasi_%g_%g'%(x,z),mod,nut,note='M12 weld-in threaded insert; thread simplified; foot unchanged')
    return members

def B_loadpath():
    # Additional posts in insulation partitions; no drawer capacity/stroke change.
    xs=[17,700,1355,2010]
    beams=[]
    for i,z in enumerate((-110,-747)):
        beams.append(rhs('B_AC_ust_kiris_'+str(i),'B',(2,2502.5,743.5,783.5,z-15,z+15),0,2,note='30x40x2; upper A/C loads to partition posts'))
        add('B_AC_ust_isikesici_'+str(i),'B',box(2,2502.5,783.5,786.5,z-15,z+15),'GFRP','thermal','3 mm structural thermal-break strip; grade/creep to verify')
        for j,x in enumerate(xs):
            post=rhs('B_AC_dikme_%d_%d'%(i,j),'B',(x-15,x+15,127.5,743.5,z-15,z+15),1,2,note='30x30x2; inside wall/partition; full-height load path')
            add('B_AC_alt_isikesici_%d_%d'%(i,j),'B',box(x-15,x+15,124.5,127.5,z-15,z+15),'GFRP','thermal','3 mm structural thermal break below post; final grade/creep to verify')
            # Bearing foot spreader into existing floor then new plinth frame.
            add('B_AC_alt_pabucluk_%d_%d'%(i,j),'B',box(max(1.5,x-15),x+15,123,124.5,z-15,z+15),kind='frame',note='bearing shoe on chassis/floor')
    inserts=[p for p in PARTS if p['new'] and p['module']=='B' and p['name'].startswith('B_AC_')]
    # Foam has exact pockets; don't move rails, drawers, fans, or stored product.
    for p in PARTS:
        if p['new'] or p['module']!='B':continue
        if p['material']!='PU' and not any(k in p['name'] for k in ('bolme_','taban_','tavan_','yan_ic_sac')):continue
        bounds=bb(p['shape'])
        for q in inserts:
            if overlap(bounds,bb(q['shape'])):p['shape']=p['shape'].cut(q['shape'])

def transport_bases():
    # Shipping-only saddles: removed before placing modules on B. Shown only
    # in transport view, never counted as installed structure or insulation.
    for mod,x0,x1,y in [('A',0,700,788),('C',700,2500,788),('F',2500,4000,788)]:
        for i,z in enumerate((-710,-60)):
            add(mod+'_tasima_kizagi_'+str(i),mod,box(x0+20,x1-20,y-80,y,z-35,z+35),'wood','shipping','removable transport saddle; forklift from below; not an overhead lifting point')

def connections():
    # Lower modules tie together under the front RHS; plates carry alignment
    # forces only. Every station has its own feet and independent gravity path.
    for label,mod,xs in [('B_K','K',(3970,4050)),('K_E','E',(4550,4660))]:
        plate=box(xs[0]-15,xs[1]+15,59,63,-125,-95)
        if label=='B_K':plate=box(xs[0]-15,4000,39,43,-125,-95).fuse(box(3996,4000,43,63,-125,-95)).fuse(box(4000,xs[1]+15,59,63,-125,-95))
        for x in xs:
            y=39 if label=='B_K' and x==xs[0] else 59
            bore=cyl_y(x,-110,4.5,y-1,y+17);plate=plate.cut(bore)
            for p in PARTS:
                if p['new'] and 'alt_sasi' in p['name'] and overlap(bb(p['shape']),bb(bore)):p['shape']=p['shape'].cut(bore)
            add('M8_baglanti_civata_'+label+'_'+str(x),mod,cyl_y(x,-110,4,y,y+16).fuse(cyl_y(x,-110,6.5,y-5,y)),kind='connection',note='M8 removable splice fixing; simplified thread; no overhead lifting')
            add('M8_baglanti_somun_'+label+'_'+str(x),mod,box(x-6.5,x+6.5,y+7,y+14,-116.5,-103.5).cut(cyl_y(x,-110,4.2,y+6,y+15)),kind='connection',note='M8 weld nut inside lower RHS')
        add('montaj_baglanti_'+label,mod,plate,kind='connection',note='304 4 mm splice; Ø9 M8; accessible after plinth removal')
    # A/C hold-downs engage the added B beam, not a screw in the foam.
    for mod,xs in [('A',(28,672)),('C',(728,2472))]:
        for x in xs:
            z=-110;bore=cyl_y(x,z,4.5,770,793)
            for p in PARTS:
                if p['module'] in (mod,'B') and p['kind']!='inside' and overlap(bb(p['shape']),bb(bore)):
                    p['shape']=p['shape'].cut(bore)
            add(mod+'_B_M8_civata_'+str(x),mod,cyl_y(x,z,4,771,792).fuse(cyl_y(x,z,6.5,792,797)),kind='connection',note='removable M8 hold-down into B support; service access before top plate closure')
            add(mod+'_B_M8_rondela_'+str(x),mod,cyl_y(x,z,9,790,792).cut(cyl_y(x,z,4.5,789,793)),kind='connection')
            add(mod+'_B_M8_disli_yuva_'+str(x),'B',box(x-6.5,x+6.5,774.5,781.5,z-6.5,z+6.5).cut(cyl_y(x,z,4.2,774,782)),kind='connection',note='weld nut under RHS top wall; modeled nominal clearance')

def cladding_relief():
    structural=[p for p in PARTS if p['new'] and p['kind']=='frame']
    for p in PARTS:
        if p['new'] or p['module'] not in ('B','K','E'):continue
        if not p['name'].startswith(('onyuz_plint','taban_','tavan_','bolme_','yan_pu')):continue
        bounds=bb(p['shape'])
        for q in structural:
            if q['module']==p['module'] and overlap(bounds,bb(q['shape'])):
                v=abs(p['shape'].intersect(q['shape']).Volume())
                if v>.1:p['shape']=p['shape'].cut(q['shape']);CHANGES.append(p['name']+' fitted around '+q['name'])

def engineering():
    # Conservative hand checks; not FEA or a certification of welds / lifting.
    E=193000.;allow=140.
    def beam(name,b,h,t,L,mass,n=2,factor=2):
        I=(b*h**3-(b-2*t)*(h-2*t)**3)/12;F=mass*9.81*factor/n
        stress=(F*L/4)/(I/(h/2));defl=F*L**3/(48*E*I)
        CHECKS.append(dict(name=name,assumption_kg=mass,dynamic_factor=factor,span_mm=L,stress_MPa=round(stress,2),deflection_mm=round(defl,3),limit_MPa=allow,pass_=stress<allow and defl<L/300))
    beam('B boş taşıma: destekler arası EN ÇOK 1000 mm',60,80,3,1000,1000)
    beam('B kullanım: tek ayak açıklığında yerel yük sınırı',60,80,3,960,1300,factor=1.5)
    beam('A mevcut kaide korundu',40,100,2,684,220)
    beam('C mevcut kaide korundu',40,100,2,446,600)
    beam('K alt şase',40,60,3,500,350)
    beam('E alt şase',40,60,3,710,400)
    beam('B A/C üst kirişi, sekiz destekli yük paylaşımı',30,40,2,683,820,n=8,factor=1.5)

def preserve_ancillaries():
    import ast,re
    src=(HERE.parent/'hat_montaj_v69.py').read_text(encoding='utf-8')
    for route in ('ANA_V44','ANA_K48'):
        line=re.search('^'+route+r' = (\[.*?\])\s*(?:#|$)',src,re.M).group(1)
        pts=[(x+700,y-168,z) for x,y,z in ast.literal_eval(line)]
        for i,(a,b) in enumerate(zip(pts,pts[1:])):
            cuts=[0.,1.]
            if a[0]!=b[0]:
                cuts+= [(x-a[0])/(b[0]-a[0]) for x in (2500,4000) if min(a[0],b[0])<x<max(a[0],b[0])]
            cuts.sort()
            for j,(u,v) in enumerate(zip(cuts,cuts[1:])):
                p=V(*[aa+u*(bb-aa) for aa,bb in zip(a,b)]);q=V(*[aa+v*(bb-aa) for aa,bb in zip(a,b)]);d=q-p
                mod='C' if (p.x+q.x)/2<2500 else 'F' if (p.x+q.x)/2<4000 else 'K'
                sh=cq.Solid.makeCylinder(5,d.Length,p,d.normalized()).cut(cq.Solid.makeCylinder(3,d.Length+.2,p-d.normalized()*.1,d.normalized()))
                add(route+'_%d_%d'%(i,j),mod,sh,'hava_ana','inside','existing v69 route retained; disconnect at module seam for transport',False)
    add('D_PIZZA_YEDEK_UST','F',box(2520,3324,1348,1860,-424,-20),'karton','stock','Existing reserve envelope: 320 flat boxes; unloaded for transport',False)

def build():
    from types import SimpleNamespace
    from load_source import cache
    meta=OUT/'.cache/base_parts.json';brep=OUT/'.cache/base.brep'
    if meta.exists() and brep.exists():
        ob=cache();info=json.loads(meta.read_text(encoding='utf-8'));shapes=list(cq.Shape.importBrep(str(brep)))
        assert len(shapes)==len(info['parts']),(len(shapes),len(info['parts']))
        PARTS.extend(dict(p,shape=s) for p,s in zip(info['parts'],shapes))
        M=SimpleNamespace(TC=SimpleNamespace(RAKOR_ACICI=info['rakor']),Y_MEK=892,MALZEME=info['materials'])
    else:
        M,ob=load();source(M)
        cq.Compound.makeCompound([p['shape'] for p in PARTS]).exportBrep(str(brep))
        meta.write_text(json.dumps(dict(parts=[{k:v for k,v in p.items() if k!='shape'} for p in PARTS],rakor=M.TC.RAKOR_ACICI,materials=M.MALZEME),ensure_ascii=False),encoding='utf-8')
    print('SOURCE PARTS',len(PARTS),flush=True)
    for p in PARTS:
        # v69 made every front layer transparent. Recover physical materials,
        # especially foam cores; display alpha is not a material specification.
        if p['material']=='304' and ('_pu' in p['name'] or p['name'].endswith('_pu')):
            p['material']='PU';p['kind']='insulation'
        elif p['material']=='304' and 'conta' in p['name']:
            p['material']='EPDM';p['kind']='gasket'
        if any(k in p['name'] for k in ('dikme','kusak','kaide_','kose_','cerceve_','kiris_','ayak_')) and p['kind'] in ('shell','front'):p['kind']='frame'
    preserve_ancillaries()
    independent_A(M)
    for mod in ('B','K','E'):
        feet=[]
        for p in PARTS:
            if p['module']==mod and p['name'].startswith('ayak_'):
                b=bb(p['shape']);feet.append(((b[0]+b[1])/2,(b[4]+b[5])/2))
        lower_frame(mod,0,0,feet)
    B_loadpath();transport_bases();connections();cladding_relief();engineering()
    return M,ob

if __name__=='__main__':
    M,ob=build()
    from export import write
    write(M,PARTS,CHECKS,CHANGES)
    ob.ozet();sys.stdout.flush();os._exit(0)
