"""K400 prototype, translated from approved k-dar v3 experiment.
No dishwasher. Original cutter/nozzle solids and recorded dimensions retained.
Rodless axes are catalogue ENVELOPES, not supplier CAD. Not production approval.
"""
import math
import cadquery as cq
import kesme_cad_v6 as OLD
from kesme_cad_v6 import *
W=400.0
XC,ZC=200.0,-206.0
X_SON=660.0
X_TASI=420.0
X_OLU=397.0
DONGU=26.0
Z_GELIS=(.3,2.3)
Z_KES=(4.,6.5)
Z_TASI=(6.6,8.4)
Z_ITME=(10.,12.5)
PARCALAR=[]

def add(ad,wp,mal='sac',grup='SABIT'):
    PARCALAR.append(dict(ad=ad,wp=wp,mal=mal,grup=grup,bom=None))

def box(ad,x,y,z,w,h,d,mal='sac',g='SABIT'):
    add(ad,kut(x-w/2,x+w/2,y-h/2,y+h/2,z-d/2,z+d/2),mal,g)

def tube(ad,x,y,z,w,h,d,axis='y'):
    outer=kut(x-w/2,x+w/2,y-h/2,y+h/2,z-d/2,z+d/2)
    inset=[2,2,2]; inset['xyz'.index(axis)]=-1
    inner=kut(x-w/2+inset[0],x+w/2-inset[0],y-h/2+inset[1],y+h/2-inset[1],z-d/2+inset[2],z+d/2-inset[2])
    add(ad,outer.cut(inner))

def ease(a,b,t):
    u=max(0.,min(1.,(t-a)/(b-a)));return u*u*(3-2*u)

def e_time(t):
    """E v11 waits open through the slower K400 push; fold only after return."""
    knots=((0,3),(8.5,11.5),(10,11.5),(12.5,13.1),(13.2,13.35),(14,13.6),(23.4,23))
    if t<0:return max(0,t+3)
    for (a,x),(b,y) in zip(knots,knots[1:]):
        if t<=b:return x+(y-x)*(t-a)/(b-a)
    return 23.

def state(t):
    push=ease(10,12.5,t)
    fx=260+10*ease(9.8,10,t)+240*push
    if t>=12.65:fx=510-250*ease(12.65,14,t)
    pz=-556+350*ease(8.5,9.8,t)-350*ease(14,15.3,t)
    x=-60+260*ease(.3,2.3,t)  # continuous with main oven exit x3940
    if t>=6.6:x=200+220*ease(6.6,8.4,t)+240*push
    return dict(fx=fx,pz=pz,x=x,z=-170-36*ease(.3,2.1,t),follow=14.5*max(0,min(1,(fx-397)/53)),cut=125*ease(4,5.4,t)*(1-ease(5.7,6.5,t)))

def grup_trs(g,t):
    s=state(t);dx=s['fx']-260;dz=s['pz']+556
    return {'KESICI':(0,-s['cut'],0),'ITICI_ARABA':(dx,0,0),'ITICI_CAPRAZ':(dx,0,dz),'ITICI_KOL':(dx,0,dz),'ITICI_YUZ':(dx,-s['follow'],dz)}.get(g,(0,0,0))

def urun_merkez(t):
    s=state(t);settle=ease(12.8,13.2,t)
    y=996-14.5*max(0,min(1,(s['x']-397)/53))
    y=y*(1-settle)+937.6*settle
    return s['x'],y,s['z']

def modul():
    PARCALAR.clear()
    # Closed, flush cabinet, same rear/front and process levels as main line.
    for x in (20,380):
        for z in (-800,42):
            tube(f'kose_dikmesi_{x}_{z}',x,994,z,30,1736,30)
            add(f'ayak_{x}_{z}',sily(x,z,8,8,123).union(sily(x,z,20,0,8)),'celik')
    for y in (140,877,1840):
        for z in (-800,42):tube(f'onyuz_kayit_{y}_{z}',200,y,z,330,30,30,'x')
    for x in (20,380):tube(f'taban_sac_tasiyici_{x}',x,140,-379,30,30,812,'z')
    box('taban_sac_3',200,124.5,-385,397,3,888)
    box('istasyon_tabani_3',200,893.5,-385,397,3,888)
    box('arka_sac',200,994,-829.25,400,1736,1.5,'kabuk')
    box('ust_sac',200,1861.25,-385.5,400,1.5,889,'kabuk')
    for x,ap,name in ((.75,URUN_GIRISI,'sol_sac_urun_girisi'),(399.25,E_PENCERE,'sag_sac_E_penceresi')):
        sh=kut(x-.75,x+.75,126,1860.5,-828.5,59)
        add(name,sh.cut(kut(x-2,x+2,ap[0],ap[1],ap[2],ap[3])),'kabuk')
    for name,y0,y1 in (('alt',126,883),('orta',886,1305),('ust',1308,1859)):
        sh=kut(3,398.5,y0,y1,59,79).cut(kut(4.5,397,y0+1.5,y1-1.5,58,77.5))
        add('onyuz_kapak_'+name,sh,'on_seffaf')
    box('plint_on',200,61.5,18.25,400,123,1.5,'kabuk')
    # Short conveyor; 400 wide belt in z, x direction shortened only.
    for z in (-421,-3):box('bant_yan_'+str(z),200,960,z,390,55,6)
    for x in (65,335):
        for z in (-421,-3):tube(f'bant_ayagi_{x}_{z}',x,915,z,20,40,20)
    box('kayma_tablasi',200,991,-212,254,6,396)
    for x in (46,354):
        add('tahrik_rulosu_'+str(x),silz(x,969,25,-412,-12),'aluminyum')
        wrap=silz(x,969,27,-412,-12).cut(silz(x,969,25,-413,-11))
        wrap=wrap.intersect(kut(x-28 if x==46 else x,x if x==46 else x+28,940,998,-413,-11))
        add('bant_sarim_'+str(x),wrap,'pu_bant')
    box('bant_PU_ust',200,995,-212,308,2,400,'pu_bant')
    box('bant_PU_alt',200,943,-212,308,2,400,'pu_bant')
    box('olu_plaka',391,993,-212,18,6,400)
    for name,x,z,w in (('on',250,-51,300),('arka_a',172,-361,144),('arka_b',332,-361,136)):
        box('cit_'+name,x,998.8,z,w,5,6,'pom')
    for side in (-1,1):
        a=-170+side*195;b=-206+side*155
        sh=cq.Workplane('XY').box(math.hypot(92,b-a),5,6).rotate((0,0,0),(0,1,0),-math.degrees(math.atan2(b-a,92))).translate((54,998.8,(a+b)/2))
        add('cit_giris_'+str(side),sh,'pom')
    for z in (-415,-10):box('sensor_kenar_'+str(z),20,1001,z,12,12,12,'sensor')
    # Original detailed cutter and nozzle translated intact, not scaled.
    OLD.PARCALAR.clear();OLD.kesici()
    for p in OLD.PARCALAR:
        if p['ad'].startswith('kopru_kirisi'):continue
        q=dict(p);q['wp']=q['wp'].translate((-100,0,-36));PARCALAR.append(q)
    for x in (20,380):tube('kopru_kirisi_yan_'+str(x),x,sum(OLD.Y_KIRIS)/2,-379,30,40,812,'z')
    for z in (-126,-286):tube('kopru_kirisi_'+str(z),200,sum(OLD.Y_KIRIS)/2,z,330,40,40,'x')
    # Tank and controls retain experiment envelopes; supplier/internal details pending.
    add('yag_tanki_3L',sily(200,-540,80,1472,1752).cut(sily(200,-540,78.5,1474,1753)))
    add('yag_tanki_kapagi',sily(200,-540,88,1752,1766))
    box('yag_tanki_rafi',200,1469.5,-540,250,5,260)
    for x in (90,310):box('yag_raf_askisi_'+str(x),x,1540,-658,20,144,6)
    box('pano_plakasi',200,1664.5,-820,265,385,4)
    box('pano_elektrik_zarfi',220,1650,-770,220,340,92,'plastik')
    box('sartlandirici_MS4',85,1662,-780,45,60,25,'aluminyum')
    # Drive geometry copied from the tested experiment; hollow output arm.
    box('itici_sabit_plaka',200,961,-700,380,6,170)
    box('itici_MY1B10G_250',200,974.1,-700,360,20.2,28,'aluminyum')
    for z in (-755,-645):box('itici_X_ray_'+str(z),200,969,z,360,10,15,'celik')
    for x in (40,360):
        for z in (-755,-645):
            tube(f'eksen_ayagi_{x}_{z}',x,926.5,z,20,63,20)
            box(f'itici_taban_{x}_{z}',x,899,z,36,8,36)
    box('itici_X_araba',75,987.6,-700,50,6.8,26,'aluminyum','ITICI_ARABA')
    box('itici_X_merkez_yukseltme',75,1018.5,-700,50,55,26,'aluminyum','ITICI_ARABA')
    for z in (-755,-645):
        block=kut(45.6,104.4,968,980,z-16,z+16).cut(kut(44,106,963,974,z-7.5,z+7.5))
        add('itici_X_blok_'+str(z),block,'celik','ITICI_ARABA')
        box('itici_X_ara_'+str(z),75,1013,z,58.8,66,32,'sac','ITICI_ARABA')
    box('itici_Z_plaka',75,1048.5,-590,76,5,460,'sac','ITICI_ARABA')
    box('itici_MY1B10G_350',75,1061.1,-590,28,20.2,460,'aluminyum','ITICI_ARABA')
    for x in (53,97):
        box('itici_Z_yukseltme_'+str(x),x,1063.5,-590,15,25,460,'sac','ITICI_ARABA')
        box('itici_Z_ray_'+str(x),x,1081,-590,15,10,460,'celik','ITICI_ARABA')
        block=kut(x-16,x+16,1080,1092,-794.4,-735.6).cut(kut(x-7.5,x+7.5,1075,1086,-796,-734))
        add('itici_Z_blok_'+str(x),block,'celik','ITICI_CAPRAZ')
    box('itici_Z_araba',75,1074.6,-765,26,6.8,50,'aluminyum','ITICI_CAPRAZ')
    box('itici_yuzer_baglanti',75,1085,-765,8,14,16,'sac','ITICI_CAPRAZ')
    box('itici_Z_kopru',81,1094.5,-765,88,5,65,'sac','ITICI_CAPRAZ')
    box('itici_one_kol',125,1103,-660.5,20,12,221,'sac','ITICI_KOL')
    box('itici_dusey_kol',125,1068.5,-556,20,81,20,'sac','ITICI_KOL')
    arm=kut(115,254,1028,1040,-566,-546).cut(kut(251,255,1027,1041,-567,-545))
    add('itici_yatay_kol',arm,'sac','ITICI_KOL')
    # Sliding tongue and open guide: no overlapping solid rail envelopes.
    guide=kut(247,263,1020.4,1044,-575,-537).cut(kut(251,261,1020,1045,-572,-540))
    add('itici_yuz_kilavuz_kovani',guide,'celik','ITICI_KOL')
    box('itici_yuzer_kilavuz',256,1022,-556,10,36,32,'celik','ITICI_YUZ')
    box('itici_yuz',256,1008.3,-556,8,24,300,'pom','ITICI_YUZ')
    box('itici_alt_dudak',259,996.45,-556,2,.3,300,'pom','ITICI_YUZ')
    return PARCALAR

if __name__=='__main__':
    modul();assert all(p['wp'].val().isValid() for p in PARCALAR)
    print('K400 prototype valid solids',len(PARCALAR),'no dishwasher')
