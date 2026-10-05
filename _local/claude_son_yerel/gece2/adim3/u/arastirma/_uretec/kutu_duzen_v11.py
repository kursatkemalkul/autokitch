# E v11: vacuum pick/place and positively supported forming nest.
# Prototype dimensions; pneumatic sizing/cardboard porosity require trials.
_v10_feed=besleyici
_v10_die=kalip
_v10_blank_angles=blank_acilar
_v10_groups=grup_matrisi
_v10_module=modul
_v10_electric=elektrik
MALZEME.setdefault('vakum_kaucuk',dict(renk=(0.16,0.48,0.78,1),met=0,ruf=.8))
VAC_Y0=YB+T
VAC_STROKE=20.0
VAC_POINTS=((200,-710),(200,-540),(650,-710),(650,-540))

def vacuum_lift(t):
    return VAC_STROKE*(ss(.35,.65,t)-ss(1.4,1.65,t)+ss(1.72,1.9,t)-ss(22.4,22.8,t))

def feed_z(t):
    return BESLE*(ss(.7,1.35,t)-ss(1.92,2.6,t))

def vacuum_trs(t):return (0,vacuum_lift(t),feed_z(t))

def nest_dy(t):
    # Support stays under the base, not attached to the press. It remains down
    # when the press retracts and resets only after the box has left the nest.
    return U_MAX-u_zimba(t)+U_MAX*ss(22.6,22.98,t)

def besleyici():
    _v10_feed()
    remove=('itici_asma_plakasi_','itici_kirisi_','itici_cubugu')
    PARCALAR[:]=[p for p in PARCALAR if not p['ad'].startswith(remove)]
    # Retain the two real guide carriages and belt drive. Remove the pushing bar.
    ytop=Y_BES_PL-34
    for i,x in enumerate((150,650)):
        ekle('vakum_aski_'+str(i),kut(x-10,x+10,1080,ytop,-826,-818),'aluminyum','ITICI')
    ekle('vakum_sabit_travers',kut(130,700,1074,1080,-818,-775),'aluminyum','ITICI')
    for i,x in enumerate((180,670)):
        ekle('vakum_Z_mil_'+str(i),sily(x,-792,6,1000,1125),'celik','VAC_Y')
        ekle('vakum_Z_burc_'+str(i),boru_y(x,-792,10.5,6.1,1044,1074),'celik','ITICI')
        ekle('vakum_Z_burc_yuvasi_'+str(i),kut(x-15,x+15,1040,1074,-807,-777).cut(sily(x,-792,10.5,1039,1075)),'aluminyum','ITICI')
    # Pneumatic Z cylinder, guided externally; body fixed to XY carriage.
    ekle('vakum_Z_silindir',kut(393,427,1080,1155,-809,-775).cut(sily(410,-792,5.1,1079,1150)),'aluminyum','ITICI')
    ekle('vakum_Z_mil_piston',sily(410,-792,5,1018,1080),'celik','VAC_Y')
    head=kut(150,690,1013,1018,-805,-779)
    for x in (150,680):head=head.union(kut(x,x+10,1013,1018,-779,-525))
    for z in (-710,-540):head=head.union(kut(150,690,1013,1018,z-8,z+8))
    ekle('vakum_baslik_cercevesi',head,'aluminyum','VAC_Y')
    for i,(x,z) in enumerate(VAC_POINTS):
        cup=sily(x,z,15,VAC_Y0,VAC_Y0+17).cut(sily(x,z,11,VAC_Y0-1,VAC_Y0+14)).cut(sily(x,z,2,VAC_Y0+13,VAC_Y0+18))
        ekle('vakum_vantuz_'+str(i),cup,'vakum_kaucuk','VAC_Y')
        ekle('vakum_vantuz_sapi_'+str(i),boru_y(x,z,4,2,VAC_Y0+17,1013),'celik','VAC_Y')
    ekle('vakum_manifold',kut(480,520,1018,1030,-797,-755),'aluminyum','VAC_Y')
    # Main feed shown as a flexible service-loop envelope; not a routed cable.
    ekle('vakum_valf_sensor_blogu',kut(455,505,1080,1110,-816,-778),'plastik','ITICI')
    ekle('vakum_tek_karton_sensor',kut(696,718,1090,1116,-799,-777),'sensor','ITICI')
    ekle('vakum_sensor_baglantisi',kut(690,700,1080,1090,-803,-777),'aluminyum','ITICI')
    # Four branches to the suction cups (horizontal and vertical, 4 mm OD).
    tube=silx(1023,-765,2,200,650)
    for i,(x,z) in enumerate(VAC_POINTS):
        tube=tube.union(silz(x,1023,2,-765,z)).union(sily(x,z,2,1003,1023))
    ekle('vakum_dagitim_hatti',tube,'vakum_kaucuk','VAC_Y')
    for p in PARCALAR:
        if p['ad']=='vakum_sabit_travers':
            for x in (180,670):p['wp']=p['wp'].cut(sily(x,-792,6.2,1073,1081))
            p['wp']=p['wp'].cut(sily(410,-792,5.2,1073,1081))
        if p['ad']=='vakum_baslik_cercevesi':
            for x in (180,670):p['wp']=p['wp'].cut(sily(x,-792,6,1012,1019))
            p['wp']=p['wp'].cut(tube)
        if p['ad']=='vakum_manifold':p['wp']=p['wp'].cut(tube)

def kalip():
    _v10_die()
    # Four existing tray rails become one guided nest. Their external product
    # interfaces at the bottom position stay exactly at y=936.
    for p in PARCALAR:
        if p['ad'].startswith('tepsi_cubugu_'):p['grup']='NEST'
    PARCALAR[:]=[p for p in PARCALAR if not p['ad'].startswith('tepsi_ayagi_')]
    nest=kut(118,405,820,826,-222,-190)
    for i,(x0,x1) in enumerate(X_BAR):
        x=(x0+x1)/2
        ekle('destek_kilavuz_mili_'+str(i),sily(x,ZB,8,826,928),'celik','NEST')
        ekle('destek_kilavuz_burcu_'+str(i),boru_y(x,ZB,12,8.1,876,906),'bronz')
        mount=kut(x-17,x+17,874,912,ZB-17,ZB+17).cut(sily(x,ZB,12,873,907)).cut(sily(x,ZB,8.1,905,913))
        ekle('destek_burc_govde_'+str(i),mount,'aluminyum')
    nest=nest.cut(sily(260,ZB,8.1,819,827))
    ekle('destek_hareketli_travers',nest,'aluminyum','NEST')
    ekle('destek_somun',boru_y(260,ZB,14,8.1,826,846),'bronz','NEST')
    ekle('destek_vida',sily(260,ZB,8,735,904),'celik')
    ekle('destek_vida_islenmis_uc',sily(260,ZB,4,729,735),'celik')
    ekle('destek_vida_alt_yatak',boru_y(260,ZB,18,8.1,735,750),'celik')
    frame=kut(225,295,729,735,-245,-185).cut(sily(260,ZB,12.2,728,736))
    for x in (225,289):frame=frame.union(kut(x,x+6,735,912,-251,-245))
    ekle('destek_motor_sasesi',frame,'aluminyum')
    ekle('destek_motor_yatak_yuvasi',kut(240,280,735,754,-226,-186).cut(sily(260,ZB,18,734,751)).cut(sily(260,ZB,8.1,750,755)),'aluminyum')
    nema23('destek_motoru',(260,699,ZB),(0,1,0),(0,0,1))
    ekle('destek_motor_plakasi',kut(229,291,699,705,-237,-175).cut(sily(260,ZB,20,698,706)),'aluminyum')
    for x in (229,285):ekle('destek_motor_dikme_'+str(x),kut(x,x+6,705,729,-237,-231),'aluminyum')
    ekle('destek_motor_kaplin',boru_y(260,ZB,12,3.2,712,734).cut(sily(260,ZB,4.05,723,735)),'aluminyum')
    p=next(p for p in PARCALAR if p['ad']=='kalip_tablasi_6')
    for x0,x1 in X_BAR:p['wp']=p['wp'].cut(sily((x0+x1)/2,ZB,8.2,911,919))

def blank_acilar(t):
    root,A=_v10_blank_angles(t)
    if t<1.7:
        root=(root[0],root[1]+VAC_STROKE*(ss(.35,.65,t)-ss(1.4,1.65,t)),-BESLE+BESLE*ss(.7,1.35,t))
    return root,A

def grup_matrisi(g,t):
    if g=='VAC_Y':return tr4(vacuum_trs(t))
    if g=='ITICI':return tr4((0,0,feed_z(t)))
    if g=='NEST':return tr4((0,nest_dy(t),0))
    return _v10_groups(g,t)

HAREKETLI+=('VAC_Y','NEST')

def elektrik():
    _v10_electric()
    ekle('surucu_STP-DRV-4830_12',TC.din_parca(TC.SURUCU_STEP,690,1687,-787),'kart')
    for i,y in enumerate((1240,1490,1750)):
        ekle('kablo_kanali_ust_mesafe_'+str(i),kut(826,W-SAC,y,y+20,-45,-30),'plastik')
    p=next(p for p in PARCALAR if p['ad']=='plc_S7-1200_1214C')
    p['bom']=("S7-1200 supervisory PLC; motion expansion REQUIRED",1,"13 drivers plus vacuum/Z pneumatic valves; I/O not selected","prototype, not an approved circuit")
