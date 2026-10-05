# -*- coding: utf-8 -*-
"""UNO yerlesim denemesi v1 - basit kutu/silindir GLB (ana modele dokunmaz)."""
import numpy as np, trimesh, json, os, sys
from trimesh.visual.material import PBRMaterial
OUT=sys.argv[1]
C=np.array([1968.0,1500.0,-270.0])  # merkez (mm)
L,R=1495,2441; YF=1152; YS=1572; YS2=1575; YT=2141; ZB=-571; ZF=23; ZH=-170
def mat(rgba,blend=False):
    return PBRMaterial(baseColorFactor=rgba,metallicFactor=0.1,roughnessFactor=0.7,
                       alphaMode='BLEND' if blend else 'OPAQUE',doubleSided=True)
M={'cerceve':mat([60,60,66,255]),'duvar':mat([200,205,212,60],True),'raf':mat([170,175,182,255]),
   'uno':mat([150,155,162,255]),'unoust':mat([185,190,196,255]),'kaset':mat([215,225,232,150],True),
   'hortum':mat([250,250,250,255]),'damla':mat([230,90,30,255]),'tabla':mat([240,200,90,90],True),
   'evap':mat([220,40,40,70],True),'kirmizi':mat([220,30,30,255]),'silindir':mat([110,115,125,255]),
   'yesil':mat([40,170,80,255]),'mandal':mat([60,90,200,255])}
parts=[]
def add(m,name,key):
    m=m.copy(); m.apply_translation(-C); m.apply_scale(0.001)
    m.visual=trimesh.visual.TextureVisuals(material=M[key]); parts.append((name,m))
def box(name,x0,x1,y0,y1,z0,z1,key):
    b=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0]); b.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]); add(b,name,key)
def cylY(name,x,z,y0,y1,d,key):
    c=trimesh.creation.cylinder(radius=d/2,height=y1-y0,sections=32); c.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
    c.apply_translation([x,(y0+y1)/2,z]); add(c,name,key)
def cylZ(name,x,y,z0,z1,d,key):
    c=trimesh.creation.cylinder(radius=d/2,height=z1-z0,sections=32); c.apply_translation([x,y,(z0+z1)/2]); add(c,name,key)
def huni(name,xc,w,y0,y1,yb,zc,dz,boyun,key):
    """kare boyun (y0) -> ust kutu (yb..y1) huni"""
    p=[]
    for (hx,hz,y) in [(boyun/2,boyun/2,y0),(w/2,dz/2,yb)]:
        for sx in (-1,1):
            for sz in (-1,1): p.append([xc+sx*hx,y,zc+sz*hz])
    add(trimesh.convex.convex_hull(np.array(p)),name+'_huni',key)
    box(name+'_kutu',xc-w/2,xc+w/2,yb,y1,zc-dz/2,zc+dz/2,key)
def cerceve():
    t=6
    for (y,z) in [(YF,ZB),(YF,ZF),(YT,ZB),(YT,ZF)]: box('cerceve_x',L,R,y-t/2,y+t/2,z-t/2,z+t/2,'cerceve')
    for x in (L,R):
        for z in (ZB,ZF): box('cerceve_y',x-t/2,x+t/2,YF,YT,z-t/2,z+t/2,'cerceve')
        for y in (YF,YT): box('cerceve_z',x-t/2,x+t/2,y-t/2,y+t/2,ZB,ZF,'cerceve')
    box('arka_duvar',L,R,YF,YT,ZB-2,ZB,'duvar'); box('sol_duvar',L-2,L,YF,YT,ZB,ZF,'duvar'); box('sag_duvar',R,R+2,YF,YT,ZB,ZF,'duvar')
    box('alt_taban_raf',L,R,YF-3,YF,ZB,ZF,'raf')
    box('ust_raf',L,R,YS,YS2,ZB,-50,'raf'); box('ust_raf_on_bukum',L,R,1534,YS,-53,-50,'raf')
    # tabla yolu (tabla hamur Ø276, z merkezi -170) — zemin altinda y 1000
    box('tabla_yolu',1056-138,2375+138,996,1000,ZH-151,ZH+151,'tabla')
    # evaporator kaseti (arka duvarin arkasinda, kuru bolme)
    box('evap_kaseti_zarfi',1676,2216,1383,1765,-826,-640,'evap')
def alt_uno(ad,xc):
    huni(ad,xc,190,1284,1499,1464,-340,440,64,'uno')
    box(ad+'_valf',xc-41,xc+41,1152,1225,-428,-346,'uno')
    cylZ(ad+'_cikis',xc,1190,-346,-170,36,'uno'); cylY(ad+'_dirsek',xc,ZH,1096,1208,36,'uno')
    cylZ(ad+'_pnomatik',xc,1191,-811,-571,38,'silindir')
    damla(ad,xc)
def kaset(ad,x0,w,drop):
    box(ad+'_govde',x0+4,x0+w-4,1152,1504,-525,-200,'kaset')
    box(ad+'_kilavuz_sol',x0,x0+4,1152,1172,-545,-180,'cerceve'); box(ad+'_kilavuz_sag',x0+w-4,x0+w,1152,1172,-545,-180,'cerceve')
    box(ad+'_mandal_ici',x0+w/2-15,x0+w/2+15,1152,1170,-215,-195,'mandal')
    cylY(ad+'_cikis',drop,ZH,1144,1223,60,'kaset')
    cylZ(ad+'_motor',drop,1191,-814,-571,57,'silindir')
    damla(ad,drop)
def ust_uno(ad,xc,w,h,cakisma):
    huni(ad,xc,w,1648,1707+h,1707+h*0.45,-340,440,64,'unoust')
    box(ad+'_valf',xc-41,xc+41,1575,1648,-428,-346,'unoust')
    cylZ(ad+'_cikis',xc,1614,-346,-170,36,'unoust'); cylY(ad+'_dirsek',xc,ZH,1551,1632,36,'unoust')
    cylZ(ad+'_pnomatik',xc,1613,-811,-571,38,'kirmizi' if cakisma else 'silindir')
    cylY(ad+'_HORTUM_D42',xc,ZH,1216,1551,42,'hortum')
    box(ad+'_kesme_valfi',xc-15,xc+15,1152,1216,ZH-21,ZH+21,'unoust')
    damla(ad,xc)
def damla(ad,x):
    cylY(ad+'_dusme_deligi',x,ZH,1048,1149,30,'damla')
    cylY(ad+'_hamura_dusme',x,ZH,1000,1003,40,'damla')

def deneme(ad,alt,ust,tasma=None):
    global parts; parts=[]; cerceve()
    for k,(x0,w,drop) in alt.items():
        if k in('kiyma','kusbasi'): alt_uno(k,x0+w/2)
        else: kaset(k,x0,w,drop)
    for k,(xc,w,h) in ust.items():
        cak = 1657<xc<2235
        ust_uno(k,xc,w,h,cak)
    if tasma:
        for (x0,x1,y0,y1) in tasma: box('TASMA',x0,x1,y0,y1,-575,27,'kirmizi')
    sc=trimesh.Scene()
    for i,(n,m) in enumerate(parts): sc.add_geometry(m,node_name=f'{n}_{i}',geom_name=f'{n}_{i}')
    sc.export(os.path.join(OUT,ad))
# DENEME A: mandallar kaset izine alindi; kiyma|g|kusbasi|kasar|g|sucuk ; 2 mm duvar payi
A_alt={'kiyma':(1497,190,1592),'kusbasi':(1749,190,1844),'kasar':(1939,288,2083),'sucuk':(2289,150,2364)}
A_ust={'harc_BUYUK':(1718,380,392),'sos_KUCUK':(2258,220,285)}
deneme('uno_deneme_A_v1.glb',A_alt,A_ust)
# DENEME B: 3 ust UNO; kiyma|g|kusbasi|g|kasar|g|sucuk -> sag duvari 58 mm asar
B_alt={'kiyma':(1495,190,1590),'kusbasi':(1747,190,1842),'kasar':(1999,288,2143),'sucuk':(2349,150,2424)}
B_ust={'sos_KUCUK':(1716,220,285),'yeni_KUCUK':(1968,220,285),'harc_BUYUK':(2318,380,392)}
deneme('uno_deneme_B_v1.glb',B_alt,B_ust,tasma=[(2441,2499,1152,1504),(2441,2508,1648,2099)])
print('ok')
