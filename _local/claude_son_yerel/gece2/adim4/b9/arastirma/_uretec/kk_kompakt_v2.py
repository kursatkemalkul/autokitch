"""KK v2: separate, interlocked engineering layout; no writes to main line.

Primary change: linear split lower support, rearward retracting cut plate,
and a parked cutter. No complete-conveyor elevator. All new dimensions [V].
The exporter is shared with v1, but v1 geometry and files remain unchanged.
"""
import csv, json, math, os, struct, sys, time
from pathlib import Path
import numpy as np
import cadquery as cq
import kk_kompakt_v1 as M

E, K = M.E, M.K
P, G = M.P, M.G
OUT = M.ROOT/'arastirma'/'6_KK_kompakt_v2'
W,D,H = 1000.,830.,2030.
XC,ZC = 500.,-265.
BOX,FLAT,CUT = 1104.,1149.6,1164.
STOCK_BOTTOM=136.
STOCK_TOP=STOCK_BOTTOM+566*1.6
TOTAL=20.
part,box,group,catalog=M.part,M.box,M.group,M.catalog
curve,smooth=M.curve,M.smooth

def floor_open(t):
    return curve(t,[(0,220),(1.8,220),(3.0,0),(19.3,0),(20,220)])

def pick_y(t):
    return curve(t,[(0,STOCK_TOP+1.6),(.15,STOCK_TOP+1.6),(1.7,FLAT+1.6),
        (3,FLAT+1.6),(3.5,BOX+1.6),(3.9,BOX+91.6),(6.6,1740),(18.8,1740),(20,1740)])

def plate_z(t):
    return curve(t,[(0,-350),(6.6,-350),(7.6,0),(12.3,0),(13.7,-350),(20,-350)])

def plate_y(t):
    return curve(t,[(0,10),(7.6,10),(7.9,0),(12.,0),(12.3,10),(13.7,10),(14.5,350),(20,350)])

def cut_x(t):
    return curve(t,[(0,-325),(6.6,-325),(7.7,0),(12.0,0),(13.1,-325),(20,-325)])

def root_y(t):
    return curve(t,[(0,STOCK_TOP),(.15,STOCK_TOP),(1.7,FLAT),(3,FLAT),(3.5,BOX),
        (17.9,BOX),(18.35,BOX+55),(20,BOX+55)])

def folds(t):
    side=90*smooth(3.9,4.4,t)
    corner=90*smooth(4.2,4.6,t)
    front=90*smooth(4.6,4.9,t)
    inner=180*smooth(4.9,5.3,t)
    back=90*smooth(3.9,4.6,t)
    lid=180*smooth(14.6,16.6,t)
    flap=90*smooth(14.5,14.8,t)
    return dict(B_SWM=side,B_SWP=-side,B_CTMF=-corner,B_CTMB=corner,
        B_CTPF=-corner,B_CTPB=corner,B_FO=-front,B_FI=-inner,
        B_BW=back,B_LID=lid-back,B_LF=flap,B_LSM=flap,B_LSP=-flap)

def phase(t):
    for end,name in [(1.8,'Karton yukari'),(3.,'Alt destek kapanir'),(3.5,'Karton tabana iner'),
        (4.9,'Kutu duvarlari katlanir'),(6.6,'Vantuzlar park eder'),(7.9,'Kesme plakasi ve kafa gelir'),
        (9.5,'Pide girer'),(10.6,'Sprey'),(12,'Kesim'),(13.7,'Destek geriye cekilir'),
        (16.2,'Kapak kapanir'),(17.9,'Catal girer'),(19.3,'Kutu cikar'),(20.1,'Bitis')]:
        if t<end:return name

def hollow_frame(name,x,z,group='FRAME'):
    depth=10 if z==-10 else 25
    sh=E.kut(x,x+25,123,2028,z,z+depth).cut(E.kut(x+2,x+23,122,2029,z+2,z+depth-2))
    part(name,sh,'sac',group)

def screw_x(name,x0,x1,y,z,nutx,moving,lead=10):
    """Dimensioned screw, nut and bearing assembly, no thread surface rendering."""
    part(name+'_vida',E.silx(y,z,8,x0,x1),'celik',pn='SFU1610 [V uc isleme]',note='Hatve 10 mm; katalog ucu ve omur kontrolu acik')
    nut=E.silx(y,z,14,nutx-23.5,nutx+23.5).union(E.silx(y,z,24,nutx+23.5,nutx+33.5)).cut(E.silx(y,z,8.2,nutx-25,nutx+35))
    part(name+'_somun',nut,'celik',moving,pn='SFU1610-4 [V]')
    for i,x in enumerate((x0-13,x1-12)):
        sh=E.kut(x,x+12,y-25,y+25,z-25,z+25).cut(E.silx(y,z,8.3,x-1,x+13))
        part(name+'_yatak_%d'%i,sh,'anodize',pn='Ozel yatak plakasi / rulman secimi acik')
    catalog(E.nema23,name+'_motor',(x0-35,y,z),(1,0,0),(0,1,0))
    part(name+'_kaplin',E.silx(y,z,12,x0-35,x0).cut(E.silx(y,z,8.1,x0-36,x0+1)),'aluminyum',pn='Kaplin [V delik/esneklik]')

def build():
    P.clear();G.clear()
    for g in ('FRAME','SHELL','STOCK','SPRAY'):group(g)
    group('BED_L',move=lambda t:(-floor_open(t),0,0))
    group('BED_R',move=lambda t:(floor_open(t),0,0))
    group('PICK',move=lambda t:(0,pick_y(t)-(STOCK_TOP+1.6),0))
    group('PLATE_Z',move=lambda t:(0,0,plate_z(t)))
    group('PLATE',parent='PLATE_Z',move=lambda t:(0,plate_y(t),0))
    group('HEAD',move=lambda t:(cut_x(t),0,0))
    group('CUT',parent='HEAD',move=lambda t:(0,-125*smooth(10.7,11.2,t)+125*smooth(11.5,12.,t),0))
    group('CARTON',axis='y',angle=lambda t:90,move=lambda t:(706,0,-5))
    for g,(parent,pivot,axis) in E.DUGUM.items():
        if parent is None:
            group(g,parent='CARTON',move=lambda t:(-500*smooth(18.35,19.3,t),root_y(t)-FLAT,0),scale=lambda t:1. if t<19.35 else .00001)
        else:group(g,pivot,parent=parent,axis=axis,angle=lambda t,g=g:folds(t)[g])
    # The six slices only descend after the solid plate has cleared each slice.
    # This is conservative clearance choreography, not validated food mechanics.
    for i in range(6):
        def food_move(t,i=i):
            dz=plate_z(t)
            # Sector vertices sampled analytically for whole-body support clearance.
            aa=np.linspace(i*math.pi/3,(i+1)*math.pi/3,31)
            rear=min([ZC]+[ZC+149*math.sin(a) for a in aa])
            edge=-85+dz
            drop=0. if edge>=rear-1. else (BOX+1.6-CUT-plate_y(t))*smooth(rear-1,rear-16,edge)
            return (curve(t,[(0,-680),(7.9,-680),(9.5,0),(20,0)]),
                plate_y(t)+drop+55*smooth(17.9,18.35,t),
                95*(1-smooth(7.9,9.5,t))+500*smooth(18.35,19.3,t))
        group('FOOD%d'%i,move=food_move,scale=lambda t:1. if 7.9<=t<19.35 else .00001)
    group('FORK',move=lambda t:(0,55*smooth(17.9,18.35,t),500*(1-smooth(17.0,17.9,t))+500*smooth(18.35,19.3,t)),scale=lambda t:1. if 17<=t<19.35 else .00001)

    for i,(x,z) in enumerate(((0,-10),(975,-10),(0,-770),(975,-770))):hollow_frame('dikme%d'%i,x,z)
    box('taban',(1.5,998.5,123,126,-828.5,-1.5))
    for n,b in [('arka',(0,1000,123,2030,-830,-828.5)),('ust',(0,1000,2028.5,2030,-828.5,0)),
        ('sag',(998.5,1000,123,2028.5,-828.5,0))]:box('kabuk_'+n,b,'kabuk','SHELL')
    left=E.kut(0,1.5,123,2028.5,-828.5,0).cut(E.kut(-1,3,1100,1235,-425,-10))
    part('kabuk_sol_urun_pencereli',left,'kabuk','SHELL')
    box('sarjor_566',(298,702,STOCK_BOTTOM,STOCK_TOP,-817,-13),'karton_yigin','STOCK',kind='SARF',pn='566 + 1 aktif = 567; 1.6 mm [V]')
    box('sarjor_platform',(296,704,128,136,-819,-11),'aluminyum')
    for i in range(0,566,12):box('stok_cizgi%03d'%i,(298,702,STOCK_BOTTOM+i*1.6,STOCK_BOTTOM+i*1.6+.2,-13.2,-13),'karton','STOCK')
    for x in (275,725):
        catalog(E.hgr15,'sarjor_ray%d'%x,940,(x,135,-805),(0,1,0),(0,0,1))
        catalog(E.hgh15,'sarjor_araba%d'%x,(x,180,-805),(0,1,0),(0,0,1))
    # Magazine drive stays OUTSIDE the 804x404 stock footprint.
    part('sarjor_Tr16x4',E.sily(755,-745,8,140,1070),'celik',pn='Tr16x4 [V]')
    catalog(E.nema23,'sarjor_motor',(925,1000,-745),(0,-1,0),(0,0,1))

    # Linear opening leaves: no tall rotating wings in the pickup trajectory.
    for k,side in enumerate(('L','R')):
        g='BED_'+side;left=side=='L'
        spans=((350,376),(414,470)) if left else ((530,586),(624,650))
        for j,(a,b) in enumerate(spans):box('taban_destek_%s%d'%(side,j),(a,b,1094,1104,-425,-122),'sac',g)
        for z in (-470,-85):
            a,b=(250,500) if left else (500,750)
            box('taban_travers_%s%d'%(side,z),(a,b,1080,1094,z-7,z+7),'sac',g)
        x=255 if left else 745
        for z in (-32,-805):
            catalog(E.hgr15,'destek_ray_%s%d'%(side,z),290,(5 if left else 995,1250,z),(1 if left else -1,0,0),(0,1,0))
            catalog(E.hgh15,'destek_araba_%s%d'%(side,z),(x,1250,z),(1 if left else -1,0,0),(0,1,0),group=g)
            if z==-32:
                box('destek_aski_%s%d'%(side,z),(x-6,x+6,1090,1249,-10,-6),'sac',g)
                box('destek_aski_ust_%s'%side,(x-6,x+6,1238,1249,-38,-6),'sac',g)
                box('destek_aski_alt_%s'%side,(x-6,x+6,1080,1094,-92,-6),'sac',g)
            else:box('destek_aski_%s%d'%(side,z),(x-6,x+6,1090,1249,z-10,z+10),'sac',g)
        # Source catalogue geometry. Right stage is mirrored as a complete assembly.
        if left:screw_x('destek_L',110,430,1310,-60,365,g)
        else:
            n=len(P);screw_x('destek_R',110,430,1310,-60,365,g)
            for p in P[n:]:p['shape']=p['shape'].mirror('YZ',(500,0,0))

    # Vacuum: rear frame outside retracted plate, forward cantilevers at x400/600.
    for x in (305,695):box('vakum_arka_uzun%d'%x,(x-7,x+7,STOCK_TOP+64,STOCK_TOP+78,-826,-420 if x==305 else -450),'aluminyum','PICK')
    box('vakum_arka_travers',(305,695,STOCK_TOP+64,STOCK_TOP+76,-826,-817),'aluminyum','PICK')
    box('vakum_on_travers',(305,607,STOCK_TOP+64,STOCK_TOP+76,-426,-414),'aluminyum','PICK')
    for x in (400,600):box('vakum_on_konsol%d'%x,(x-7,x+7,STOCK_TOP+64,STOCK_TOP+76,-420,-200),'aluminyum','PICK')
    cup_specs=[(400,-210,20.7),(600,-210,20.7),(400,-365,20.7),(600,-365,20.7),
        (310,-630,10),(690,-630,10),(310,-745,10),(690,-745,10)]
    for i,(x,z,r) in enumerate(cup_specs):
        sh=E.sily(x,z,r,STOCK_TOP+1.6,STOCK_TOP+5).union(E.sily(x,z,7,STOCK_TOP+5,STOCK_TOP+66))
        part('vantuz%d'%i,sh,'vacuum','PICK',pn='SPB1 40 ED-65' if r>20 else 'Kucuk kenar vantuzu [V]',source=M.SOURCES['cup'],note='Karton porozitesi/vakum tutma testi gerekli')
    for x,hang in ((460,430),(540,570)):
        catalog(E.hgr15,'vakum_Y_ray%d'%x,800,(x,1220,-810),(0,1,0),(0,0,1))
        catalog(E.hgh15,'vakum_Y_araba%d'%x,(x,STOCK_TOP+241.6,-810),(0,1,0),(0,0,1),group='PICK')
        box('vakum_Y_tasiyici%d'%x,(hang-9,hang+9,STOCK_TOP+76,STOCK_TOP+241.6,-781,-775),'sac','PICK')
        box('vakum_ust_baglanti%d'%x,(min(hang,x)-9,max(hang,x)+9,STOCK_TOP+221,STOCK_TOP+252,-781,-775),'sac','PICK')
        box('vakum_alt_baglanti%d'%x,(hang-9,hang+9,STOCK_TOP+64,STOCK_TOP+76,-826,-775),'sac','PICK')
    part('vakum_sfu1620',E.sily(735,-792,8,1140,1910),'celik',pn='SFU1620 [V motor ve fren secimi acik]')

    # Thin cut plate moves to the REAR, not into the inlet conveyor or sideways.
    box('kesme_plakasi',(330,670,1150,1164,-425,-85),'sac','PLATE',note='14 mm; konsol + kilit sehim kontrolu gerekli')
    box('plaka_tasiyici_kol',(670,760,1150,1164,-95,-85),'sac','PLATE')
    for x in (790,835):
        catalog(E.hgr15,'plaka_Z_ray%d'%x,715,(x,1360,-805),(0,0,1),(0,1,0))
        for zz in (-340,-190):catalog(E.hgh15,'plaka_Z_araba%d_%d'%(x,zz),(x,1360,zz),(0,0,1),(0,1,0),group='PLATE_Z')
    box('plaka_Z_ust_baglanti',(770,945,1388,1402,-349,-175),'sac','PLATE_Z')
    # Rear lift lets the lid rotate without crossing the withdrawn plate.
    for x in (875,925):
        catalog(E.hgr15,'plaka_Y_ray%d'%x,490,(x,1140,-350),(0,1,0),(0,0,-1),group='PLATE_Z')
        catalog(E.hgh15,'plaka_Y_araba%d'%x,(x,1164,-350),(0,1,0),(0,0,-1),group='PLATE')
        box('plaka_Y_ray_omurga%d'%x,(x-12,x+12,1138,1634,-349,-338),'sac','PLATE_Z')
    box('plaka_Y_araba_baglanti',(750,945,1154,1176,-390,-379),'sac','PLATE')
    box('plaka_konsol_omurga',(746,760,1150,1164,-390,-85),'sac','PLATE')
    # Inlet stays entirely left of the 404-mm-wide stock.
    for xx in (30,260):
        part('giris_rulo%d'%xx,E.silz(xx,1137,25,-412,-12),'aluminyum',pn='Interroll EC5000 / avara [V tam boy]')
    box('giris_bant_ust',(30,260,1162,1164,-412,-12),'pu_bant')
    box('giris_bant_alt',(30,260,1110,1112,-412,-12),'pu_bant')
    box('giris_kopru',(260,329,1160,1164,-412,-12),'sac')

    # Cutter parks left of the vacuum pickup volume; only the stock plate retreats.
    n=len(K.PARCALAR);K.kesici()
    for p in K.PARCALAR[n:]:
        if p['ad'].startswith('kopru_kirisi') or p['ad']=='silindir_baglanti_plakasi':continue
        g='CUT' if p['grup']=='KESICI' else 'SPRAY' if p['grup']=='SPREY' else 'HEAD'
        part('K_'+p['ad'],p['wp'].translate((200,0,-95)),p['mal'],g,
             source=M.SOURCES['K'],note='Kaynakta [V] govde olculeri var; katalog CAD teyidi acik')
    del K.PARCALAR[n:]
    G['SPRAY']['scale']=lambda t:1 if 9.5<=t<=10.6 else .00001
    for y in (1600,1700):
        catalog(E.hgr15,'kafa_X_ray%d'%y,710,(80,y,-20),(1,0,0),(0,0,-1))
        for x in (455,555):catalog(E.hgh15,'kafa_X_araba%d_%d'%(x,y),(x,y,-20),(1,0,0),(0,0,-1),group='HEAD')
    box('kafa_on_araba_baglanti',(410,590,1578,1730,-62,-48),'sac','HEAD')
    for x in (410,575):
        box('kafa_ust_konsol%d'%x,(x,x+15,1715,1730,-310,-60),'sac','HEAD')
        box('kafa_yan_dikme%d'%x,(x,x+15,1577.5,1715,-310,-220),'sac','HEAD')
    mount=E.kut(410,590,1577.5,1589.5,-310,-220)
    for x in (445,500,555):mount=mount.cut(E.sily(x,-265,11.2,1576,1591))
    part('DGRF_baglanti_delikli',mount,'sac','HEAD')

    # Box and actuated folding paddle surfaces. Each paddle follows its hinge.
    n=len(E.PARCALAR);E.blank()
    for p in E.PARCALAR[n:]:part(p['ad'],p['wp'],'karton',p['grup'],'SARF',source=M.SOURCES['E'])
    del E.PARCALAR[n:]
    # Do not invent independent motion of a locked corner: explicit unresolved tooling.
    # The following reference tool surfaces are distinct from catalogue actuators.
    for side in ('L','R'):
        root='T'+side+'_ROOT'
        group(root,parent='BED_'+side,axis='y',angle=lambda t:90,move=lambda t:(706,BOX-FLAT,-5))
        for gn,(par,piv,axis) in E.DUGUM.items():
            if par is None:continue
            parent=root if par=='B_ROOT' else 'T'+side+'_'+par
            def tool_angle(t,gn=gn):
                a=folds(t)[gn]
                if gn=='B_LID':a-=90*smooth(16.65,17.0,t)
                if gn=='B_FO':a+=180*smooth(16.3,16.9,t)
                return a
            group('T'+side+'_'+gn,piv,parent=parent,axis=axis,angle=tool_angle)
    for n,g,a,b,c,d in [('yan_m','B_SWM',110,410,-402,-370),('yan_p','B_SWP',110,410,-42,-10),
        ('on','B_FO',62,95,-355,-57),('arka','B_BW',425,457,-355,-57),
        ('kapak','B_LID',500,745,-350,-62)]:
        for side,cl,cr in [('L',c,min(d,-207)),('R',max(c,-205),d)]:
            if cr<=cl:continue
            shape=E.kut(a,b,FLAT-3,FLAT-.2,cl,cr)
            if g=='B_FO':
                for gl in (390,500,610):
                    shape=shape.cut(E.kut(a-1,b+1,FLAT-4,FLAT+1,gl-706-15,gl-706+15))
            part('katlama_yuzeyi_'+n+side,shape,'anodize','T'+side+'_'+g,
                 note='Referans temas yuzeyi; tahrik/baglanti henuz TAMAMLANMADI',kind='COZULMEMIS')

    for i in range(6):
        aa=np.linspace(i*math.pi/3+.004,(i+1)*math.pi/3-.004,40)
        poly=[(XC,ZC)]+[(XC+149*math.cos(a),ZC+149*math.sin(a)) for a in aa]
        sh=cq.Workplane('XZ',origin=(0,CUT,0)).polyline(poly).close().extrude(-15)
        part('pide_dilim%d'%i,sh,'hamur','FOOD%d'%i,kind='REFERANS',note='Rijit sektor; gercek sicak gida aktarimi dogrulanmadi')
    for x in (390,500,610):box('robot_catal%d'%x,(x-13,x+13,1095.5,1103.5,-410,30),'robot','FORK',kind='REFERANS')
    return P

def export():
    OUT.mkdir(parents=True,exist_ok=True)
    M.OUT=OUT
    result=M.export_glb()
    old=Path(result['path']);raw=old.read_bytes();jl=struct.unpack_from('<I',raw,12)[0]
    doc=json.loads(raw[20:20+jl]);doc['asset']['generator']='AUTOKITCH KK v2 engineering layout - NOT production release'
    doc['animations'][0]['name']='KK_v2_clearance_choreography_20s'
    blob=raw[28+jl:];js=json.dumps(doc,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
    target=OUT/'kk_kompakt_v2.glb'
    target.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(js)+len(blob))+struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(blob),b'BIN\0')+blob)
    # Retain the intermediate shared-export file; no user file is removed.
    M.reports()
    print('EXPORTED',target,len(P),'parts',flush=True)

def release_status():
    """Fail closed: missing mechanics or collision proof cannot become a release."""
    OUT.mkdir(parents=True,exist_ok=True)
    unfinished=[p['name'] for p in P if p['kind']=='COZULMEMIS']
    interlocks=[]
    for t in np.linspace(0,20,801):
        # A programmed sequence check is separate from collision/physics validation.
        if 1.8<t<3.0 and root_y(t)<FLAT-.05:
            interlocks.append([float(t),'support_closes_before_sheet_is_clear'])
        if 6.6<t<7.6 and (floor_open(t)>.05 or pick_y(t)<1735):
            interlocks.append([float(t),'cut_plate_enters_before_pickup_parks'])
        cutting=125*(smooth(10.7,11.2,t)-smooth(11.5,12.,t))
        if cutting>.1 and (abs(plate_z(t))>.05 or abs(plate_y(t))>.05 or abs(cut_x(t))>.05):
            interlocks.append([float(t),'knife_without_stationary_support'])
        if 14.6<t<16.6 and (plate_y(t)<349.9 or plate_z(t)>-349.9):
            interlocks.append([float(t),'lid_closes_before_plate_parks'])
    status=dict(status='INCOMPLETE_DO_NOT_RELEASE',
        dimensions_mm=[W,D,H],target_stock=567,nominal_cardboard_mm=1.6,
        nominal_stock_height_mm=907.2,width_saving_mm=1430-W,
        source='kk_kompakt_v2.py',parts=len(P),
        sequence_interlock_tests=801,sequence_interlock_failures=interlocks,
        unresolved_tool_surfaces=unfinished,
        unresolved_engineering=[
            'folding actuator, bearing, transmission and locking-tab connections',
            'pickup/plate/cutter-axis drive selection and complete mechanical connections',
            'moving groups: remaining shaft/carriage collision in latest sampled audit',
            'cardboard crease and corner-tab interpenetration; no supplier-approved dieline',
            'complete continuous collision, structural/deflection and pneumatic/cable verification',
            '20 seconds is a timing target, not proven physical cycle time',
            '6 rigid food sectors do not validate hot-food transfer or slice integrity'],
        glb_status='The existing GLB is the FIRST unchecked intermediate export, not the current source. Do not present as final.',
        main_v50_modified=False)
    (OUT/'durum_v2.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'BOM_v2.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Parca','Grup','Tur','Adet','Parca no','Kaynak','Not'])
        for p in P:w.writerow([p['name'],p['group'],p['kind'],1,p['pn'],p['source'],p['note']])
    print('RELEASE BLOCKED:',len(unfinished),'unfinished tooling parts;',len(interlocks),'sequence violations',flush=True)
    return status

if __name__=='__main__':
    build();print('BUILT',len(P),flush=True)
    status=release_status()
    # Review export is explicit; it never means the machine has passed engineering.
    if '--export-unverified-review' in sys.argv:export()
    sys.stdout.flush();os._exit(0)
