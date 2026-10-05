# -*- coding: utf-8 -*-
"""AUTOKITCH KK v1 -- 600 mm combined cutting/spray/carton CONCEPT.

Separate experiment. Never imports main() or writes the existing line models.
Dimensions in mm, x along line, y up, z=0 front. Animation is prescribed
kinematics, not a food/cardboard contact simulation or production approval.
Source dimensions: kesme_cad_v1.py, kutu_cad_v3.py. New dimensions marked [V].
"""
from pathlib import Path
import csv, json, math, os, struct, sys, time
import numpy as np
import cadquery as cq
import kutu_cad_v3 as E
import kesme_cad_v1 as K

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'arastirma' / '6_KK_kompakt_v1'
W, D, H = 600., 830., 2030.
N, T = 567, E.T
STOCK_BOTTOM = 145.                       # [V] platform upper face
STOCK_TOP = STOCK_BOTTOM + (N-1)*T       # 566 in stack + 1 active blank = 567
PICK_HIGH = 1348.                         # [V] above opened die wings
BOX_Y, BLANK_Y, CUT_Y = E.TEPSI, E.YB, K.BANT
XC, ZC = 300., -265.                     # R_y(90) of original carton centre
WING_X = (82., 518.)                     # [V] outside the 404 mm blank
WING_Y = 1088.                           # [V]
BELT_STROKE, BELT_PARK_Y = 360., 1680.    # [V] return above lid and platen drive
DURATION = 20.
P, G = [], {}
SOURCES = {
 'E': 'arastirma/_uretec/kutu_cad_v3.py',
 'K': 'arastirma/_uretec/kesme_cad_v1.py',
 'retract': 'https://www.dornerconveyors.com/solutions/retracting-conveyors',
 'festo': 'https://www.festo.com/media/catalog/202791_documentation.pdf',
 'cup': 'https://www.schmalz.com/10.01.06.03499',
 'motor': 'https://www.automationdirect.com/adc/shopping/catalog/motion_control/stepper_systems/stepper_motors/stp-mtr-23079',
 'rail': 'https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E.pdf',
}
MATERIALS = dict(E.MALZEME)
MATERIALS.update(K.MALZEME)
MATERIALS['anodize'] = dict(renk=(.12,.28,.35,1),met=.65,ruf=.34)
MATERIALS['rubber'] = dict(renk=(.16,.19,.2,1),met=0,ruf=.8)
MATERIALS['vacuum'] = dict(renk=(.15,.50,.75,1),met=.05,ruf=.5)

def smooth(a,b,t):
    q=max(0.,min(1.,(t-a)/(b-a))) if a!=b else float(t>=b)
    return q*q*(3-2*q)

def curve(t, knots):
    if t<=knots[0][0]: return knots[0][1]
    for (a,u),(b,v) in zip(knots,knots[1:]):
        if t<=b: return u+(v-u)*smooth(a,b,t)
    return knots[-1][1]

def group(name, pivot=(0,0,0), parent=None, axis=None, angle=None, move=None, scale=None):
    G[name]=dict(pivot=np.array(pivot,dtype=float),parent=parent,axis=axis,
                 angle=angle or (lambda t:0.),move=move or (lambda t:(0,0,0)),
                 scale=scale or (lambda t:1.))

def part(name, shape, mat='sac', group='FRAME', kind='URETIM', pn='', source='[V] yeni tasarim', note=''):
    assert not any(p['name']==name for p in P), name
    if isinstance(shape,cq.Workplane): shape=shape.val()
    P.append(dict(name=name,shape=shape,mat=mat,group=group,kind=kind,pn=pn,source=source,note=note))

def box(name, bounds, mat='sac', group='FRAME', **kw):
    part(name,E.kut(*bounds),mat,group,**kw)

def tube(name,x0,x1,y0,y1,z0,z1,t=2,group='FRAME'):
    sh=E.kut(x0,x1,y0,y1,z0,z1).cut(E.kut(x0+t,x1-t,y0-1,y1+1,z0+t,z1-t))
    part(name,sh,'sac',group)

def catalog(fn,*args,group='FRAME',**kw):
    start=len(E.PARCALAR)
    fn(*args,grup=group,**kw)
    for p in E.PARCALAR[start:]:
        bom=p.get('bom') or ('',1,'','')
        part(p['ad'],p['wp'],p['mal'],group,'SATIN ALMA',bom[0],bom[3],bom[2])
    del E.PARCALAR[start:]

def bolt(name,x,y,z,axis='y',group='FRAME',length=18):
    # M6 shank + socket head. Thread not represented; ISO dimension envelope.
    if axis=='y': sh=E.sily(x,z,3,y-length,y).union(E.sily(x,z,5,y,y+6))
    else: sh=E.silz(x,y,3,z-length,z).union(E.silz(x,y,5,z,z+6))
    part(name,sh,'celik',group,'SATIN ALMA','ISO 4762 M6x%d'%length,'ISO 4762; dis geometrisi sade')

def wing_angle(t):
    return curve(t,[(0,0),(.55,90),(1.85,90),(2.45,0),(20,0)])

def blank_y(t):
    return curve(t,[(0,STOCK_TOP),(.55,STOCK_TOP),(1.8,PICK_HIGH),(2.45,PICK_HIGH),
                    (3.2,BLANK_Y),(3.35,BLANK_Y),(4.25,BOX_Y),(17.6,BOX_Y),(18.2,BOX_Y+55),(20,BOX_Y+55)])

def blank_fold(t):
    # Reuse original hinge tree and forming law; lid remains flat for belt entry.
    old=curve(t,[(0,1.7),(3.35,1.7),(4.25,3.3),(4.8,4.5),(5.5,5.7),(6.2,8.1),(20,8.1)])
    _,a=E.blank_acilar(old)
    lid=curve(t,[(0,0),(13.8,0),(14.3,85),(14.6,100),(15.5,180),(20,180)])
    a['B_LID']=lid-a['B_BW']
    flap=90*smooth(13.8,14.6,t)
    a.update(B_LF=flap,B_LSM=flap,B_LSP=-flap)
    return a

def belt_move(t):
    dz=curve(t,[(0,-BELT_STROKE),(6.8,-BELT_STROKE),(7.5,0),(12.2,0),(13.,-BELT_STROKE),(20,-BELT_STROKE)])
    y=curve(t,[(0,BELT_PARK_Y),(6.1,BELT_PARK_Y),(6.8,CUT_Y),(13.,CUT_Y),(13.8,BELT_PARK_Y),(20,BELT_PARK_Y)])
    return (0,y-CUT_Y,dz)

def press_move(t):
    y=curve(t,[(0,1450),(3.2,1450),(3.35,BLANK_Y+T),(4.25,BOX_Y+T),
       (4.45,BOX_Y+T+65),(5.,BOX_Y+T+65),(5.5,BOX_Y+T),(5.65,BOX_Y+T),
       (6.15,1450),(6.75,1450),(7.2,1550),(15.9,1550),(16.3,1149.6),(16.45,1149.6),(17.,1450),(20,1450)])
    return (0,y-1450,0)

def press_angle(t):
    return curve(t,[(0,0),(6.15,0),(6.75,-90),(15.5,-90),(15.9,0),(20,0)])

def pickup_move(t):
    y=curve(t,[(0,STOCK_TOP+T),(.55,STOCK_TOP+T),(1.8,PICK_HIGH+T),(2.45,PICK_HIGH+T),
              (3.2,BLANK_Y+T),(3.6,1385),(19.3,1385),(20,STOCK_TOP+T)])
    # Park above all tooling before the press descends.
    x=curve(t,[(0,0),(3.2,0),(3.6,0),(20,0)])
    return (x,y-(STOCK_TOP+T),0)

def phase(t):
    for end,name in [(0.55,'Destekler aciliyor'),(1.8,'Karton depodan yukari aliniyor'),
       (2.45,'Destekler kapaniyor'),(3.2,'Karton kaliba birakiliyor'),(6.2,'Kutu tabani katlaniyor'),
       (7.5,'Kesme bandi yerine geliyor'),(9.5,'Pide firindan geliyor'),(10.7,'Tereyagi spreyi'),
       (12.2,'Alti dilim kesme'),(13.8,'Pide kutuya aktariliyor'),(17.,'Kutu kapagi kapaniyor'),
       (19.3,'Robot kutuyu aliyor'),(20.1,'Cevrim bitiyor')]:
        if t<end:return name

def build():
    P.clear();G.clear()
    for g in ('FRAME','SHELL','STOCK','SPRAY'):group(g)
    for i,x in enumerate(WING_X):
        group('WING%d'%i,(x,WING_Y,0),axis='z',angle=lambda t,i=i:(1 if i==0 else -1)*wing_angle(t))
    group('BELT_LIFT',move=lambda t:(0,belt_move(t)[1],0))
    group('BELT',parent='BELT_LIFT',move=lambda t:(0,0,belt_move(t)[2]))
    group('PRESS_LIFT',move=press_move)
    group('PRESS',(XC,1450,-425),parent='PRESS_LIFT',axis='x',angle=press_angle)
    group('PICK',move=pickup_move)
    group('HEAD',move=lambda t:(0,curve(t,[(0,300),(7.5,300),(8.5,0),(12.3,0),(13.5,300),(20,300)]),0))
    group('CUT',parent='HEAD',move=lambda t:(0,-125*curve(t,[(0,0),(10.8,0),(11.4,1),(11.6,1),(12.1,0),(20,0)]),0))
    group('CARTON',axis='y',angle=lambda t:90,move=lambda t:(506,0,-5))
    for g,(parent,pivot,axis) in E.DUGUM.items():
        if parent is None:
            # old -z moves to new -x; extraction towards new front = old -x.
            group(g,parent='CARTON',move=lambda t:(-500*smooth(18.2,19.3,t),blank_y(t)-BLANK_Y,0),
                  scale=lambda t:1. if t<19.35 else .00001)
        else: group(g,pivot,parent=parent,axis=axis,angle=lambda t,g=g:blank_fold(t)[g])
    group('FOOD',move=lambda t:(curve(t,[(0,-460),(7.5,-460),(9.5,0),(20,0)]),
          curve(t,[(0,0),(12.45,0),(13.,BOX_Y+T-CUT_Y),(17.6,BOX_Y+T-CUT_Y),(18.2,BOX_Y+T+55-CUT_Y),(20,BOX_Y+T+55-CUT_Y)]),
          curve(t,[(0,95),(7.5,95),(9.5,0),(18.2,0),(19.3,500),(20,500)])),scale=lambda t:1. if 7.5<=t<19.35 else .00001)
    group('FORK',move=lambda t:(0,55*smooth(17.6,18.2,t),curve(t,[(0,500),(17.,500),(17.6,0),(18.2,0),(19.3,500),(20,500)])),scale=lambda t:1. if 17<=t<19.35 else .00001)

    # Frame: lower magazine, removable front access, top technical shelf.
    for i,(x,z) in enumerate(((20,-42),(550,-42),(20,-822),(550,-822))):
        tube('dikme_%d'%i,x,x+30,123,2028,z,z+30)
        part('ayak_%d'%i,E.sily(x+15,z+15,18,0,8).union(E.sily(x+15,z+15,6,8,123)),kind='SATIN ALMA',pn='Elesa LV.A-SST M12 [V]')
    box('taban',(2,598,123,126,-828,-2))
    box('ust_raf',(2,598,1815,1819,-828,-470))
    for name,b in [('arka',(0,600,123,2030,-830,-828.5)),('ust',(0,600,2028.5,2030,-828.5,0)),
                   ('sol',(0,1.5,123,2030,-828.5,0)),('sag',(598.5,600,123,2030,-828.5,0))]:
        part('kabuk_'+name,E.kut(*b),'kabuk','SHELL')
    # Full-size stock. Each tenth layer is a shallow line, not an expanded stack.
    box('566_karton_arti_1_aktif',(98,502,STOCK_BOTTOM,STOCK_TOP,-817,-13),'karton_yigin','STOCK',kind='SARF',pn='320x320x42 E-dalga; 804x404 acilim [V]',note='566 yigin + 1 hareketli karton = 567; kalinlik toleransi teyitsiz')
    for i in range(0,N-1,10):
        box('katman_%03d'%i,(98,502,STOCK_BOTTOM+i*T,STOCK_BOTTOM+i*T+.22,-13.2,-13),'karton','STOCK')
    box('sarjor_asansor_platformu',(96,504,137,145,-819,-11),'aluminyum')
    for x in (20.,580.):
        catalog(E.hgr15,'sarjor_HGR15_%d'%x,925,(x,150,-440),(0,1,0),(0,0,1))
        catalog(E.hgh15,'sarjor_HGH15_%d'%x,(x,200,-440),(0,1,0),(0,0,1))
        box('platform_kulak_%d'%x,(min(x,96),max(x+15,504) if x>500 else 98,137,145,-420,-380))
    part('sarjor_Tr16x4',E.sily(565,-600,8,150,1090),'celik',kind='SATIN ALMA',pn='Tr16x4 DIN103 [V]')
    catalog(E.nema23,'sarjor_motor_STP_MTR_23079',(565,255,-670),(0,1,0),(0,0,1))

    # Split folding/support die. Wings rotate UP outside blank x=98..502.
    for i,x in enumerate(WING_X):
        g='WING%d'%i
        lo,hi=(82,300) if i==0 else (300,518)
        part('destek_mentese_mili_%d'%i,E.silz(x,WING_Y,8,-454,-80),'celik',g)
        for zz in (-425,-105):
            box('destek_kolu_%d_%d'%(i,zz),(lo,hi,1082,1094,zz-6,zz+6),'sac',g)
        for j,(a,b) in enumerate(((138,174),(224,268)) if i==0 else ((332,376),(426,462))):
            box('catal_aralikli_destek_%d_%d'%(i,j),(a,b,1096,1104,-425,-105),'sac',g)
        a,b=(133,138) if i==0 else (462,467)
        box('yan_katlama_kalibi_%d'%i,(a,b,1094,1149.5,-425,-105),'anodize',g)
        for j,zz in enumerate((-99,-430)):
            box('uc_katlama_kalibi_%d_%d'%(i,j),(max(lo,140),min(hi,460),1094,1129.5,zz-3,zz+3),'anodize',g)
        for zz in (-445,-85):
            sh=E.kut(x-15,x+15,1070,1100,zz-8,zz+8).cut(E.silz(x,WING_Y,8.2,zz-9,zz+9))
            part('mentese_yatagi_%d_%d'%(i,zz),sh,'aluminyum')
        # Hard stops carry pressing load, not the gear reducer.
        for zz in (-415,-115):
            sx=60 if i==0 else 520
            box('mekanik_dayama_%d_%d'%(i,zz),(sx,sx+20,1075,1082,zz-10,zz+10))
        mx=52 if i==0 else 548
        catalog(E.pgcn23,'kanat_reduktor_%d'%i,(mx,970,-55),(0,0,1),(0,1,0))
        catalog(E.nema23,'kanat_motor_%d'%i,(mx,970,-134),(0,0,1),(0,1,0))
        catalog(E.kasnak,'kanat_kasnak_40_%d'%i,x,WING_Y,-52,40,eksen='z',group=g)
        catalog(E.kasnak,'motor_kasnak_20_%d'%i,mx,970,-52,20,eksen='z')
        # Non-closed transmission routing placeholder explicitly in open items.
        part('kanat_kayis_hatti_%d'%i,K.boru([(mx,970,-45),(x,WING_Y,-45)],3),'kayis',pn='GT3 9 mm [V]',note='Yol temsili; kapali kayis ve gergi henuz cozulmedi')
        for zz in (-405,-125):bolt('kanat_baglanti_%d_%d'%(i,zz),lo+40,1094,zz,group=g)

    # Vacuum handling frame: 8 cups support base and lid. Catalogue cup dimensions.
    for x in (112,488):
        box('vakum_boyuna_%d'%x,(x-8,x+8,STOCK_TOP+55,STOCK_TOP+71,-790,-40),'aluminyum','PICK')
    for j,z in enumerate((-210,-345,-640,-745)):
        box('vakum_travers_%d'%j,(112,488,STOCK_TOP+55,STOCK_TOP+65,z-6,z+6),'aluminyum','PICK')
        for i,x in enumerate((176,424)):
            sh=E.sily(x,z,20.7,STOCK_TOP+T,STOCK_TOP+T+3)
            sh=sh.union(E.sily(x,z,15,STOCK_TOP+T+3,STOCK_TOP+T+33))
            sh=sh.union(E.sily(x,z,8,STOCK_TOP+T+33,STOCK_TOP+66))
            part('vantuz_SPB1_40_%d_%d'%(j,i),sh,'vacuum','PICK','SATIN ALMA','Schmalz SPB1 40 ED-65 G1/4-IG 10.01.06.03499',SOURCES['cup'],'Olcu katalog; koruk yuzeyi sade')
    for x in (60,540):
        catalog(E.hgr15,'vakum_HGR15_%d'%x,610,(x,1055,-790),(0,1,0),(0,0,1))
        catalog(E.hgh15,'vakum_HGH15_%d'%x,(x,STOCK_TOP+64,-790),(0,1,0),(0,0,1),group='PICK')
    catalog(E.nema23,'vakum_motor',(540,1750,-790),(0,-1,0),(0,0,1))

    # Translating conveyor. Thin sliding bed clears the flat carton lid below.
    box('bant_kesme_destegi_10',(93,507,1152,1162,-420,-80),'sac','BELT',note='[V] 10 mm plaka; sehim kuvvet testiyle dogrulanacak')
    box('bant_PU_ust',(78,522,1162,1164,-420,-80),'pu_bant','BELT',kind='SATIN ALMA',pn='Habasit / Ammeraal PU 2 mm [V]')
    box('bant_PU_alt',(65,535,1070,1072,-420,-80),'pu_bant','BELT',note='Alt donus kolu kutu tabaninin altinda, stokun ustunde')
    for x in (65,535):
        part('bant_rulo_%d'%x,E.silz(x,1137,25,-420,-80),'aluminyum','BELT','SATIN ALMA','Interroll EC5000 D50 [V]',SOURCES['K'])
        part('bant_alt_avara_%d'%x,E.silz(x,1097,25,-420,-80),'aluminyum','BELT',pn='D50 avara [V]')
        a,b=(38,40) if x==65 else (560,562)
        box('bant_yan_donus_%d'%x,(a,b,1097,1137,-420,-80),'pu_bant','BELT')
        box('bant_yan_tasiyici_%d'%x,(x-8,x+8,1128,1156,-425,-75),'sac','BELT')
    # Centre and approach guide; incoming product centre remains z=-170 at x=0.
    sh=cq.Workplane('XZ',origin=(0,1166,0)).polyline([(10,-18),(280,-106),(300,-106),(300,-102),(280,-102),(10,-14)]).close().extrude(-20)
    part('pide_yonlendirme_citi',sh,'uhmw','BELT',note='[V] 95 mm merkez kaydirmasi; gida surtunmesi denemesi gerekli')
    for x in (45,555):
        catalog(E.hgr15,'bant_Z_HGR15_%d'%x,735,(x,1160,-70),(0,0,-1),(0,1,0),group='BELT_LIFT')
        catalog(E.hgh15,'bant_Z_HGH15_%d'%x,(x,1160,-265),(0,0,-1),(0,1,0),group='BELT')
    for x in (20,580):
        catalog(E.hgr15,'bant_Y_HGR15_%d'%x,660,(x,1080,-795),(0,1,0),(1 if x<300 else -1,0,0))
        catalog(E.hgh15,'bant_Y_HGH15_%d'%x,(x,1160,-795),(0,1,0),(1 if x<300 else -1,0,0),group='BELT_LIFT')
    catalog(E.nema23,'bant_Z_motor',(550,1700,-745),(0,0,-1),(0,1,0))
    catalog(E.nema23,'bant_Y_motor',(550,1750,-605),(0,-1,0),(0,0,1))

    # Original cutter & spray head, lifted clear for carton pickup/closing.
    start=len(K.PARCALAR);K.kesici()
    for p in K.PARCALAR[start:]:
        if p['ad'].startswith('kopru_kirisi') or p['ad']=='silindir_baglanti_plakasi':continue
        g='CUT' if p['grup']=='KESICI' else ('SPRAY' if p['grup']=='SPREY' else 'HEAD')
        b=p.get('bom') or ('',1,'','')
        part('K_'+p['ad'],p['wp'].translate((0,0,-95)),p['mal'],g,
             'SATIN ALMA' if 'DGRF' in p['ad'] or 'PulsaJet' in p['ad'] or 'UniJet' in p['ad'] else 'URETIM',b[0],b[3] or SOURCES['K'],b[2])
    del K.PARCALAR[start:]
    G['SPRAY']['scale']=lambda t:1. if 9.5<=t<=10.7 else .00001
    for x in (95,505):
        catalog(E.hgr15,'kesici_HGR15_%d'%x,430,(x,1370,-58),(0,1,0),(0,0,-1))
        catalog(E.hgh15,'kesici_HGH15_%d'%x,(x,1460,-58),(0,1,0),(0,0,-1),group='HEAD')
        box('kafa_yan_kolu_%d'%x,(x-8,x+8,1460,1480,-300,-60),'sac','HEAD')
    box('kafa_koprusu',(95,505,1460,1478,-310,-295),'sac','HEAD')
    catalog(E.nema23,'kafa_Y_motor',(505,1910,-65),(0,-1,0),(0,0,1))

    # Independent folding platen folds upright behind cutter when not in use.
    box('katlama_baski_plakasi',(144,456,1450,1458,-425,-113),'anodize','PRESS')
    part('baski_mentese_mili',E.silx(1450,-425,8,120,480),'celik','PRESS')
    for x in (78,522):
        catalog(E.hgr15,'baski_Y_HGR15_%d'%x,690,(x,1050,-460),(0,1,0),(0,0,1))
        catalog(E.hgh15,'baski_Y_HGH15_%d'%x,(x,1450,-460),(0,1,0),(0,0,1),group='PRESS_LIFT')
        a,b=(78,130) if x<300 else (470,522)
        box('baski_mentese_tasiyici_%d'%x,(a,b,1440,1447,-460,-413),'aluminyum','PRESS_LIFT')
    catalog(E.pgcn23,'baski_cevirme_reduktor',(480,1520,-480),(1,0,0),(0,1,0),group='PRESS_LIFT')
    catalog(E.nema23,'baski_cevirme_motor',(401,1520,-480),(1,0,0),(0,1,0),group='PRESS_LIFT')
    catalog(E.nema23,'katlama_Y_motor',(50,1760,-60),(0,-1,0),(0,0,1))
    # Four corner fingers are represented as actuated tools, not hidden rotations.
    for i,(x,z) in enumerate(((144,-111),(456,-111),(144,-419),(456,-419))):
        g='FINGER%d'%i;group(g,(x,1110,z),parent='WING%d'%(0 if x<300 else 1),axis='y',angle=lambda t,i=i:(-1 if i%2 else 1)*90*smooth(3.8,4.3,t))
        box('kose_tirnagi_parmagi_%d'%i,(x-2,x+2,1110,1125,z-20,z+20),'uhmw',g,note='[V] baglanti ve strok cozum bekliyor')

    # Folded paper tree reuses unchanged panel geometry and thickness.
    start=len(E.PARCALAR);E.blank()
    for p in E.PARCALAR[start:]:part(p['ad'],p['wp'],'karton',p['grup'],'SARF',source=SOURCES['E'])
    del E.PARCALAR[start:]
    part('pide_D300_h15',E.sily(XC,ZC,150,CUT_Y,CUT_Y+15),'hamur','FOOD','REFERANS',source=SOURCES['K'])
    part('pide_ust',E.sily(XC,ZC,140,CUT_Y+15,CUT_Y+15.8),'kasar_ust','FOOD','REFERANS')
    for x in (198,300,402):box('robot_catal_%d'%x,(x-13,x+13,1095.5,1103.5,-405,30),'robot','FORK',kind='REFERANS',note='3 dis 26x8; robot gerisi gosterilmiyor')

    # Independent top technical cabinet keeps equipment out of 567-blank volume.
    part('yag_tanki_3L_yatay',E.silx(1910,-645,70,35,285).cut(E.silx(1910,-645,68.5,37,283)),'sac',pn='Isitmali gida tanki 3 L [V]',note='Yatay yeni tasarim; basincli kap imalat onayi yok')
    part('tank_kapak',E.silx(1910,-645,74,27,35),'celik')
    box('PLC_S7_1200',(350,460,1840,1940,-820,-745),'siemens',kind='SATIN ALMA',pn='6ES7214-1AG40-0XB0',note='Katalog zarf; konektorler bu revizyonda sade')
    box('valf_adasi',(340,530,1960,2010,-820,-755),'aluminyum',kind='SATIN ALMA',pn='Festo VUVG-L10 [V]')
    # Existing real catalogue supply and drivers.
    for i in range(4):
        part('surucu_STP_DRV_4830_%d'%i,K.TC.din_parca(K.TC.SURUCU_STEP,330+i*52,1840,-470),'kart',kind='SATIN ALMA',pn='STP-DRV-4830',source='Mevcut TraceParts STEP')
    part('guc_NDR240',K.TC.din_parca(K.TC.GUC_STEP,430,1840,-650),'aluminyum',kind='SATIN ALMA',pn='NDR-240-24 [V akim butcesi]',source='Mevcut TraceParts STEP')
    return P

def rot(axis,deg):
    if not axis:return np.eye(4)
    return np.array(E.rot4(axis,deg))

def transform(g,t,cache=None):
    cache={} if cache is None else cache
    if g in cache:return cache[g]
    d=G[g];parent=d['parent'];pp=G[parent]['pivot'] if parent else np.zeros(3)
    m=np.eye(4);m[:3,3]=d['pivot']-pp+np.asarray(d['move'](t))
    m=m@rot(d['axis'],d['angle'](t));m[:3,:3]*=d['scale'](t)
    cache[g]=(transform(parent,t,cache)@m if parent else m)
    return cache[g]

def world_shape(p,t,cache=None):
    m=transform(p['group'],t,cache).copy()
    m[:3,3]-=m[:3,:3]@G[p['group']]['pivot']
    return E.tasi(p['shape'],m.tolist())

def export_glb():
    nodes=[];idx={}
    for name,d in G.items():
        parent=d['parent'];pp=G[parent]['pivot'] if parent else np.zeros(3)
        n=dict(name=name,translation=((d['pivot']-pp+np.array(d['move'](0)))*.001).tolist())
        if d['axis']:n['rotation']=list(E.quat(d['axis'],d['angle'](0)))
        n['scale']=[d['scale'](0)]*3
        idx[name]=len(nodes);nodes.append(n)
    for name,d in G.items():
        if d['parent']:nodes[idx[d['parent']]].setdefault('children',[]).append(idx[name])
    blob=bytearray();views=[];acc=[];meshes=[];mats=[];mi={}
    def add(a,typ,target=None):
        a=np.asarray(a);a=a.astype('<u4' if a.dtype.kind in 'iu' else '<f4')
        while len(blob)%4:blob.append(0)
        view=dict(buffer=0,byteOffset=len(blob),byteLength=a.nbytes)
        if target:view['target']=target
        views.append(view);blob.extend(a.tobytes())
        at=dict(bufferView=len(views)-1,componentType=5125 if a.dtype.kind=='u' else 5126,count=len(a),type=typ)
        if typ!='SCALAR':at.update(min=a.min(axis=0).tolist(),max=a.max(axis=0).tolist())
        elif a.dtype.kind!='u':at.update(min=[float(a.min())],max=[float(a.max())])
        acc.append(at);return len(acc)-1
    def material(k):
        if k not in mi:
            d=MATERIALS[k];m=dict(name=k,pbrMetallicRoughness=dict(baseColorFactor=list(d['renk']),metallicFactor=d['met'],roughnessFactor=d['ruf']),doubleSided=True)
            if d.get('saydam'):m['alphaMode']='BLEND'
            mi[k]=len(mats);mats.append(m)
        return mi[k]
    tri=0
    for no,p in enumerate(P):
        # Copy before tessellation: OCC caches meshes on original shapes.
        sh=p['shape'].copy();verts,faces=sh.tessellate(.32,.4)
        v=np.array([[q.x,q.y,q.z] for q in verts]);f=np.array(faces,dtype=np.uint32)
        if not len(v):continue
        v=(v-G[p['group']]['pivot'])*.001
        n=np.zeros_like(v);fn=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
        for j in range(3):np.add.at(n,f[:,j],fn)
        n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-20)
        prim=dict(attributes=dict(POSITION=add(v,'VEC3',34962),NORMAL=add(n,'VEC3',34962)),indices=add(f.reshape(-1),'SCALAR',34963),material=material(p['mat']))
        meshes.append(dict(name=p['name'],primitives=[prim]));ni=len(nodes)
        nodes.append(dict(name=p['name'],mesh=len(meshes)-1,extras=dict(kind=p['kind'],part_number=p['pn'],source=p['source'],note=p['note'])))
        nodes[idx[p['group']]].setdefault('children',[]).append(ni);tri+=len(f)
        if no%60==0:print('mesh',no,'/',len(P),flush=True)
    tt=np.linspace(0,DURATION,401);ti=add(tt,'SCALAR');sam=[];ch=[]
    def channel(name,path,a,typ):
        sam.append(dict(input=ti,output=add(a,typ),interpolation='LINEAR'))
        ch.append(dict(sampler=len(sam)-1,target=dict(node=idx[name],path=path)))
    for name,d in G.items():
        pp=G[d['parent']]['pivot'] if d['parent'] else np.zeros(3)
        trs=np.array([(d['pivot']-pp+np.array(d['move'](t)))*.001 for t in tt])
        if np.ptp(trs,axis=0).max()>1e-8:channel(name,'translation',trs,'VEC3')
        if d['axis']:
            q=np.array([E.quat(d['axis'],d['angle'](t)) for t in tt])
            if np.ptp(q,axis=0).max()>1e-8:channel(name,'rotation',q,'VEC4')
        ss=np.array([[d['scale'](t)]*3 for t in tt])
        if np.ptp(ss)>1e-8:channel(name,'scale',ss,'VEC3')
    while len(blob)%4:blob.append(0)
    data=dict(asset=dict(version='2.0',generator='AUTOKITCH KK kompakt v1 - concept kinematics'),scene=0,scenes=[dict(nodes=[idx[g] for g,d in G.items() if not d['parent']])],nodes=nodes,meshes=meshes,materials=mats,buffers=[dict(byteLength=len(blob))],bufferViews=views,accessors=acc,animations=[dict(name='KK_20s_kinematic_concept',samplers=sam,channels=ch)])
    js=json.dumps(data,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
    path=OUT/'kk_kompakt_v1.glb'
    path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(js)+len(blob))+struct.pack('<I4s',len(js),b'JSON')+js+struct.pack('<I4s',len(blob),b'BIN\0')+blob)
    return dict(path=str(path),triangles=tri,nodes=len(nodes),channels=len(ch),mb=path.stat().st_size/1e6)

def bounds(p,t):
    if '_bb_points' not in p:
        b=p['shape'].BoundingBox()
        p['_bb_points']=np.array([[x,y,z,1] for x in (b.xmin,b.xmax) for y in (b.ymin,b.ymax) for z in (b.zmin,b.zmax)])
    pts=p['_bb_points']
    m=transform(p['group'],t).copy();m[:3,3]-=m[:3,:3]@G[p['group']]['pivot']
    v=(m@pts.T).T[:,:3];return v.min(0),v.max(0)

def verify():
    invalid=[p['name'] for p in P if not p['shape'].isValid() or p['shape'].Volume()<=0]
    envelope={};ts=np.linspace(0,20,201)
    for p in P:
        if p['kind']=='REFERANS' or p['group'].startswith('B_') or p['group']=='SPRAY':continue
        for t in ts:
            a,b=bounds(p,t)
            if any(a<np.array([0,0,-830])-.2) or any(b>np.array([600,2030,0])+.2):
                envelope[p['name']]=dict(time=round(float(t),2),min=a.tolist(),max=b.tolist());break
    # Critical path intersections. These are actual CAD solids, not visual assertions.
    selected=[('B_TABAN','bant_PU_alt'),('B_KAPAK','bant_PU_alt'),('B_KAPAK','bant_kesme_destegi_10'),
              ('B_TABAN','katlama_baski_plakasi'),('B_KAPAK','katlama_baski_plakasi'),
              ('B_TABAN','catal_aralikli_destek_0_0'),('B_TABAN','yan_katlama_kalibi_0'),
              ('B_TABAN','kose_tirnagi_parmagi_0'),('B_KAPAK','vakum_travers_2')]
    by={p['name']:p for p in P};hits=[]
    for an,bn in selected:
        for t in (0,.55,1.,1.8,2.15,2.45,2.8,3.2,4.25,5.5,6.8,7.5,10.,12.6,13.,13.8,14.4,15.2,16.2,17.6):
            pa,pb=by[an],by[bn];a,b=bounds(pa,t);c,d=bounds(pb,t)
            if np.all(np.minimum(b,d)-np.maximum(a,c)>.05):
                v=world_shape(pa,t).intersect(world_shape(pb,t)).Volume()
                if v>1.:hits.append(dict(a=an,b=bn,time=t,volume_mm3=round(v,2)))
    result=dict(status='KAVRAM - URETIM ONAYI YOK',envelope_mm=[W,D,H],old_width_mm=1430,width_saved_mm=1430-W,
       stock_count=N,stock_thickness_mm=T,stock_height_mm=N*T,stock_1p8_count=int(math.floor(N*T/1.8+1e-9)),
       fixed_heights_mm=dict(oven=1166,cut=CUT_Y,blank=BLANK_Y,box=BOX_Y),
       invalid_solids=invalid,envelope_violations=envelope,critical_intersections=hits,
       coverage='201 zarf pozu; 9 kritik cift x 20 poz. Tam parca-parca surekli temas taramasi DEGIL.',
       timing=[dict(t=round(t,2),phase=phase(t)) for t in np.arange(0,20,.1)],sources=SOURCES)
    (OUT/'kontrol_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('CHECK',len(invalid),'invalid;',len(envelope),'outside;',len(hits),'critical intersections',flush=True)
    for name,v in envelope.items():print('OUTSIDE',name,v,flush=True)
    for v in hits:print('HIT',v,flush=True)
    return result

def reports():
    with (OUT/'BOM_v1.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Parca','Grup','Tur','Adet','Parca no','Kaynak','Not'])
        for p in P:w.writerow([p['name'],p['group'],p['kind'],1,p['pn'],p['source'],p['note']])
    calc=dict(stock_mass_kg=N*.16,stock_mass_source='[V] eski model: 100 kutu /16 kg; yeni karton tartilmadi',
       elevator_torque_Nm=(N*.16+10)*9.81*.004/(2*math.pi*.35)/2,
       elevator_assumptions='[V] Tr16x4 eta=.35; 2:1 dis oran; 10 kg platform. Motorun hiz-tork egrisiyle teyit gerekli.',
       cut_force_range_N=[798,2394],cut_force_source='[V] kesme_v1: 798 mm agiz x 1..3 N/mm. Kesim testi yok.',
       DGRF_63_force_N=1870,DGRF_source=SOURCES['festo'],
       drop_mm=CUT_Y-BOX_Y-T,drop_time_s=math.sqrt(2*(CUT_Y-BOX_Y-T)/9810),
       cycle_s=20,cycle_source='[V] onceden atanmis kinematik; prototip veya dinamik simulasyon sonucu degil')
    (OUT/'hesap_v1.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    t0=time.time();build();print('PARTS',len(P),'build seconds',round(time.time()-t0,1),flush=True)
    reports();result=verify()
    if '--check-only' not in sys.argv:print(export_glb(),flush=True)
    print('DONE',round(time.time()-t0,1),'seconds',flush=True)
    sys.stdout.flush();os._exit(0)
