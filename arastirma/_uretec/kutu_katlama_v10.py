# v10 — positive-drive tooling. All tool transforms and cardboard transforms
# share the same cycle. This is a dimensional prototype, NOT a tested die line.
MALZEME.setdefault('bronz',dict(renk=(0.64,0.43,0.18,1.0),met=0.8,ruf=0.35))
V10_U_PAUSE = 12.0
V10_PAUSE = Z_ZIMBA[0] + (Z_ZIMBA[1]-Z_ZIMBA[0])*V10_U_PAUSE/U_MAX
V10_DELAY = 3.0
V10_SIDE = _ray_uzeri(V10_U_PAUSE, KALIP, 2.1)
V10_FOLD = (3.0, 3.7)
V10_LIFT = (4.0, 4.5)
V10_RETURN = (4.7, 5.3)
V10_TOOL_STROKE = 38.0
_v9_u = u_zimba
_v9_blank = blank_acilar
_v9_parmak = parmak
_v9_piston = piston
_v9_kapak = kapak_mekanizmasi
_v9_grup = grup_matrisi
_v9_blank_make = blank
_v9_govde = govde
_v9_besleyici = besleyici
_v9_elektrik = elektrik
_v9_modul = modul
for _v10_name in ('Z_ZIMBA','Z_KALK1','Z_PARMAK','Z_VURUS2','Z_KOPRU','Z_FLAP','Z_KOL','Z_PIZZA',
                  'Z_KITICI_DON','Z_KAFA_HAZIR','Z_YATIR','Z_KAPAT','Z_KOL_DON','Z_CATAL','Z_GIZLE'):
    globals()[_v10_name] = tuple(v + V10_DELAY if v >= 3.3 else v for v in globals()[_v10_name])
DONGU += V10_DELAY
KONTROL_ANLARI = tuple(i/10 for i in range(int(DONGU*10)+1))
GECIS_ANLARI = tuple(t+3 if t>=3.3 else t for t in GECIS_ANLARI) + tuple(2.85+i*.15 for i in range(24))
PIZZA_ANLARI = tuple(t+3 for t in PIZZA_ANLARI)

def u_zimba(t):
    if t < V10_PAUSE: return U_MAX*lin(2.7,3.3,t)
    if t < V10_PAUSE+V10_DELAY: return V10_U_PAUSE
    return U_MAX*lin(2.7,3.3,t-V10_DELAY)

_v9_kafa = kafa
def kafa(t):
    if Z_ZIMBA[0] <= t < Z_ZIMBA[1]: return YB+T-u_zimba(t)
    if 6.3 <= t < 7.1: return (YB+T-U_MAX)+45*(ss(6.3,6.55,t)-ss(6.85,7.1,t))
    if 7.1 <= t < 8.2: return YB+T-U_MAX
    if 8.2 <= t < 8.7: return (YB+T-U_MAX)+(H_UST-(YB+T-U_MAX))*ss(8.2,8.7,t)
    if Z_VURUS2[0] <= t < Z_VURUS2[3]: return H_UST  # 180-degree positive tuck replaces blind second punch
    return _v9_kafa(t)

def corner_angle(t):
    return -15+15*ss(V10_PAUSE,3.0,t)+90*ss(*V10_FOLD,t)-105*ss(*V10_RETURN,t)

def corner_lift(t):
    # 38 mm clears the upright carton while forming. At the top of the press
    # stroke, use 60 mm for the tucker's 180-degree reset quadrant. Lower back
    # to 38 mm at tucker=0 before it parks at -90; then return home.
    return (V10_TOOL_STROKE*ss(*V10_LIFT,t)
            +22*(ss(8.75,9.05,t)-ss(9.5,9.75,t))
            -V10_TOOL_STROKE*ss(10.25,10.55,t))

def _v10_add(a,b): return tuple(a[i]+b[i] for i in range(3))
def _v10_mul(v,s): return tuple(x*s for x in v)
def _v10_point(M,p): return tuple(sum(M[i][j]*p[j] for j in range(3))+M[i][3] for i in range(3))
def _v10_place(wp,ex,ey,P): return cq.Workplane(obj=yerles(wp.val(),ex,ey,P))
def _v10_faceplace(wp,ex,ey,out,P):
    ez=capraz(ex,ey)
    if sum(ez[i]*out[i] for i in range(3))<0: wp=wp.mirror('XY')
    return _v10_place(wp,ex,ey,P)

def govde():
    _v9_govde()
    p=next(p for p in PARCALAR if p['ad']=='agiz_ust_kirisi')
    p['wp']=p['wp'].translate((0,0,69))  # z29..49, ahead of tool bearings ending at z28
    p['wp']=p['wp'].intersect(kut(SAC+20,W-SAC-20,1161,1178,28,50))  # butt joints to front posts, no overlapping solids

def besleyici():
    _v9_besleyici()
    p=next(p for p in PARCALAR if p['ad']=='besleyici_plakasi')
    for x0,x1 in ((67,134),(385,454)):
        p['wp']=p['wp'].cut(kut(x0,x1,1331,1338,-412,-317))

# Corner tool axes are aligned with the actual corner crease at the dwell,
# not with an arbitrary vertical axis. Shaft ends ABOVE the cardboard.
CORNER = {}
for _code,_sx,_sz in (('MF',-1,-1),('MB',1,-1),('PF',-1,1),('PB',1,1)):
    _theta = -_sz*V10_SIDE
    _R = rot4('x',_theta)
    _axis = _v10_point(_R,(0,0,_sz))
    _pivot = (BX0+T if _sx<0 else BX1-T, H_UST, BZ0 if _sz<0 else BZ1)
    CORNER['CNR_'+_code] = dict(P=_pivot,axis=_axis,sign=_sx*_sz,side=_sz,end=_sx,theta=_theta)

def corner_quat(g,t):
    a=math.radians(CORNER[g]['sign']*corner_angle(t))/2
    return tuple(x*math.sin(a) for x in CORNER[g]['axis'])+(math.cos(a),)

def corner_translation(t): return (0,kafa(t)-H_UST+corner_lift(t),0)

def _axis_rotation(axis,angle):
    x,y,z=axis; a=math.radians(angle); c=math.cos(a); s=math.sin(a); q=1-c
    return [[c+x*x*q,x*y*q-z*s,x*z*q+y*s,0],
            [y*x*q+z*s,c+y*y*q,y*z*q-x*s,0],
            [z*x*q-y*s,z*y*q+x*s,c+z*z*q,0],[0,0,0,1]]

def corner_tools():
    y=H_UST
    # Motorised common lift: keep fingers at 90, withdraw 38 mm, THEN reset.
    # At the bottom stroke the hub starts at 46+38=84 mm above the head:
    # clears the still-upright double front wall (42+40=82) by nominal 2 mm.
    bridge=kut(16,444,y+180,y+186,-222,-190)
    for x in (196,316):bridge=bridge.union(kut(x,x+8,y+76,y+180,-222,-190))
    ekle('kose_takim_sabit_kopru',bridge,'aluminyum','PISTON')
    frame=kut(16,444,y+84,y+90,-371,-15).cut(kut(76,413,y+83,y+91,-344,-68))
    frame=frame.cut(kut(132,387,y+83,y+91,-398,-348))
    # Front spindle and return strap pass through this relieved tooling window.
    # The corner bearing seat remains on x90..118, z-68..-35.
    frame=frame.cut(kut(75,135,y+83,y+91,-35,-14))
    frame=frame.cut(kut(77,87,y+83,y+91,-69,-14))
    # Rib behind the punch: stiffens the remaining rear cross-tie in bending.
    frame=frame.union(kut(76,413,y+90,y+112,-348,-344))
    for x in (30,436): frame=frame.cut(sily(x,-206,10.6,y+80,y+95))
    for x in (230,286): frame=frame.cut(kut(x-1,x+5,y+83,y+91,-17,-4))
    for c in CORNER.values():
        frame=frame.cut(_v10_place(sily(0,0,8.2,45,125),(1,0,0),c['axis'],c['P']))
    frame=frame.cut(sily(260,-35,7.1,y+80,y+95))
    ekle('kose_takim_hareketli_cerceve',frame,'aluminyum','CNR_LIFT')
    for i,x in enumerate((30,436)):
        ekle('kose_takim_kilavuz_%d'%i,sily(x,-206,6,y+66,y+210),'celik','PISTON')
        ekle('kose_takim_burc_%d'%i,boru_y(x,-206,10.5,6.1,y+66,y+96),'celik','CNR_LIFT')
        ekle('kose_takim_burc_govde_%d'%i,kut(x-14,x+14,y+64,y+97,-220,-192).cut(sily(x,-206,10.5,y+63,y+98)),'aluminyum','CNR_LIFT')
    ekle('kose_takim_vida',sily(260,-35,4,y+42,y+200),'celik','PISTON')
    ekle('kose_takim_somun',boru_y(260,-35,10,4.1,y+90,y+115),'bronz','CNR_LIFT')
    ekle('kose_takim_vida_yatagi',boru_y(260,-35,11,4.1,y+178,y+188),'celik','PISTON')
    ekle('kose_takim_vida_yatak_govdesi',kut(230,290,y+178,y+188,-55,-5).cut(sily(260,-35,11,y+177,y+189)),'aluminyum','PISTON')
    ekle('kose_takim_vida_kaplini',boru_y(260,-35,8,3.2,y+196,y+222).cut(sily(260,-35,4.05,y+195,y+202)),'aluminyum','PISTON')
    nema23('kose_takim_kaldirma_motoru',(260,y+230,-35),(0,-1,0),(0,0,1),'PISTON')
    ekle('kose_takim_motor_plakasi',kut(230,290,y+224,y+230,-65,-5).cut(sily(260,-35,20,y+223,y+231)),'aluminyum','PISTON')
    feet=kut(196,324,y+70,y+76,-206,-190)
    for x in (230,286):
        feet=feet.union(kut(x,x+4,y+76,y+224,-16,-7)).union(kut(x,x+4,y+70,y+76,-206,-7))
    ekle('kose_takim_motor_ayaklari',feet,'aluminyum','PISTON')
    for g,c in CORNER.items():
        P=c['P']; axis=c['axis']; ex=(c['end'],0,0); normal=(0,-math.cos(math.radians(c['theta'])),-math.sin(math.radians(c['theta'])))
        # Local coordinates: X = distance from crease; Y = along crease;
        # Z = outward from paper. Flat contact shoe touches the panel's outer face.
        M=eksen_matrisi(ex,axis,normal,P)
        shoe=kut(25,35,10,33,1.6,3.6)
        stem=kut(29,35,33,50,1.6,5.6).union(kut(-4,35,46,50,1.6,5.6))
        ekle('kose_'+g+'_temas_pabucu',_v10_faceplace(shoe,ex,axis,normal,P),'uhmw',g)
        ekle('kose_'+g+'_katlama_kolu',_v10_faceplace(stem,ex,axis,normal,P),'sac',g)
        # shaft and keyed radial hub; no full shaft passes through the carton.
        ekle('kose_'+g+'_mil',_v10_place(sily(0,0,4,44,92),ex,axis,P),'celik',g)
        hub=boru_y(0,0,8,4.0,46,53)
        ekle('kose_'+g+'_gobek',_v10_place(hub,ex,axis,P),'celik',g)
        for j,h in enumerate((61,77)):
            ekle('kose_'+g+'_rulman_'+str(j),_v10_place(boru_y(0,0,11,4.05,h,h+7),ex,axis,P),'celik','CNR_LIFT')
        housing=kut(-16,16,58,87,-16,16).cut(sily(0,0,4.1,57,88))
        for h in (61,77): housing=housing.cut(sily(0,0,11, h,h+7))
        ekle('kose_'+g+'_yatak_govdesi',_v10_place(housing,ex,axis,P),'aluminyum','CNR_LIFT')
        nema23('kose_'+g+'_motor',_v10_add(P,_v10_mul(axis,116)),_v10_mul(axis,-1),(1,0,0),'CNR_LIFT')
        cp=sily(0,0,8,88,114.4).cut(sily(0,0,4.05,87,94)).cut(sily(0,0,3.2,94,115))
        ekle('kose_'+g+'_kaplin',_v10_place(cp,ex,axis,P),'aluminyum',g)
        mount=kut(-30,30,110,116,-30,30).cut(sily(0,0,20,109,117))
        mount=mount.union(kut(-30,-24,84,110,-30,30)).union(kut(24,30,84,110,-30,30))
        ekle('kose_'+g+'_motor_kelepcesi',_v10_place(mount,ex,axis,P),'aluminyum','CNR_LIFT')

# The front panel folds about its SCORE. A one-sided double-bearing shaft
# leaves the rear feeding path unobstructed. Belt motor stays below the tray.
PARMAK_P=(BX0+T/2,TEPSI+T+H_ON)
PARMAK_R=38.0
def parmak_psi(t):
    return -90*(1-ss(6.55,6.85,t)+ss(9.8,10.2,t))-180*(ss(7.2,8.0,t)-ss(9.15,9.5,t))

def front_dy(t): return 100*(1-ss(6.4,6.8,t)+ss(9.5,9.8,t))
Z_KOPRU=(9.9,10.3,Z_KOPRU[2],Z_KOPRU[3])


def piston():
    _v9_piston()
    p=next(p for p in PARCALAR if p['ad']=='piston_kafasi')
    # Relieve the FULL width of the inner front flap, not only the central
    # tucker paddle. Its two end regions also sweep over the press head.
    p['wp']=p['wp'].cut(kut(111,147,H_UST-1,H_UST+21,PK_Z[0]-1,PK_Z[1]+1))
    p['bom']=("Piston kafası 6082 · ön kenar x147; 261 × 296 × 20",1,
              "ön iç duvar tam genişlik süpürmesine açık; fiziksel karton testi bekleniyor","üretim prototipi")
    corner_tools()

def kapak_mekanizmasi():
    _v9_kapak()
    for p in PARCALAR:
        if p['ad']=='flap_katlayici_somun_kolu': p['wp']=p['wp'].cut(sily(775,-330,6.2,889,901))
    # U frame is a LINEAR folder, not three hingeless rotating metal leaves.
    # Existing SFU16 motor drives a nut + carriage, now on two explicit guides.
    for i,z in enumerate((-330,-75)):
        ekle('flap_kilavuz_mili_'+str(i),sily(775,z,6,838,974),'celik')
        for j,y in enumerate((832,974)):
            ekle('flap_kilavuz_kelepce_%d%d'%(i,j),kut(763,787,y,y+6,z-12,z+12).cut(sily(775,z,6.1,y-1,y+7)),'aluminyum')
        ekle('flap_kilavuz_diregi_'+str(i),kut(792,798,832,980,z-12,z+12).union(kut(775,798,974,980,z-12,z+12)),'aluminyum')
        ekle('flap_lineer_burc_'+str(i),boru_y(775,z,10.5,6.1,900,930),'celik','KATLAYICI')
        ekle('flap_lineer_burc_govdesi_'+str(i),kut(760,790,897,933,z-15,z+15).cut(sily(775,z,10.5,896,934)),'aluminyum','KATLAYICI')
        ekle('flap_burc_baglantisi_'+str(i),kut(739,760,890,900,z-15,z+15),'aluminyum','KATLAYICI')
    ekle('flap_vida_alt_islenmis_uc',sily(750,-300,5,710,732),'celik')
    ekle('flap_vida_alt_rulmani',boru_y(750,-300,13,5.05,724,732),'celik')

def blank_acilar(t):
    root,A=_v9_blank(t)
    # Explicit 90 degree corner tools at the 12 mm dwell, not magic angles.
    a=90*ss(*V10_FOLD,t)
    A.update(B_CTMF=-a,B_CTPF=-a,B_CTMB=a,B_CTPB=a)
    # Front die captures the external wall before the double-wall tool starts.
    f=max(-A['B_FO'],90*ss(32,U_MAX,u_zimba(t)))
    A['B_FO']=-f
    A['B_FI']=-180*ss(7.2,8.0,t)
    return root,A

def grup_matrisi(g,t):
    if g=='FRONT_Y': return tr4((0,front_dy(t),0))
    if g=='PARMAK': return mm4(tr4((0,front_dy(t),0)),_v9_grup(g,t))
    if g=='CNR_LIFT': return tr4(corner_translation(t))
    if g in CORNER:
        c=CORNER[g]; P=c['P']
        return mm4(tr4(_v10_add(P,corner_translation(t))),mm4(_axis_rotation(c['axis'],c['sign']*corner_angle(t)),tr4(_v10_mul(P,-1))))
    return _v9_grup(g,t)

HAREKETLI=HAREKETLI+('CNR_LIFT','FRONT_Y')+tuple(CORNER)

# Final front-fold architecture: no separate vertical stage. The existing
# press carries the tucker, stays down during folding, then withdraws upward.
PARMAK_P=(BX0+T/2,H_UST+42)
def front_dy(t):return kafa(t)-H_UST
def parmak():
    x,y=PARMAK_P
    paddle=kut(x-7.4,x-4.4,y+6,y+37,-305,-107).union(kut(x-56,x-52,y-22,y-18,-305,-20))
    for zz in (-290,-130):
        paddle=paddle.union(kut(x-56,x-52,y-22,y+8,zz,zz+10)).union(kut(x-56,x-4.4,y+5,y+8,zz,zz+10))
    ekle('devirme_parmagi',paddle,'sac','PARMAK')
    ekle('parmak_temasi_UHMW',kut(x-4.4,x-2.4,y+6,y+33,-305,-107),'uhmw','PARMAK')
    ekle('parmak_tahrik_yan_kolu',kut(x-56,x+6,y-22,y+6,-24,-20).union(silz(x,y,10,-24,-18)),'celik','PARMAK')
    ekle('parmak_mili',silz(x,y,6,-24,28),'celik','PARMAK')
    for i,z in enumerate((-3,20)):
        ekle('parmak_yatagi_'+str(i),silz(x,y,14,z,z+8).cut(silz(x,y,6.05,z-1,z+9)),'celik','FRONT_Y')
        ekle('parmak_yatak_ayagi_'+str(i),kut(x-20,x+20,y-18,y+18,z-4,z+8).cut(silz(x,y,14,z-5,z+9)),'aluminyum','FRONT_Y')
    mx,my=340,H_UST+200
    for ad,xx,yy in (('ust',x,y),('alt',mx,my)):
        ekle('parmak_kasnak_'+ad,silz(xx,yy,10,7,18).cut(silz(xx,yy,3.2 if ad=='alt' else 6,6,19)),'aluminyum','PARMAK' if ad=='ust' else 'FRONT_Y')
    dx=x-mx;dy=y-my;ll=math.hypot(dx,dy);nx=-dy/ll;ny=dx/ll
    def capsule(r,z0,z1):
        xy=[(mx+nx*r,my+ny*r),(x+nx*r,y+ny*r),(x-nx*r,y-ny*r),(mx-nx*r,my-ny*r)]
        return cq.Workplane('XY').polyline(xy).close().extrude(z1-z0).translate((0,0,z0)).union(silz(mx,my,r,z0,z1)).union(silz(x,y,r,z0,z1))
    ekle('parmak_kayisi',capsule(12,8,17).cut(capsule(10,7,18)),'kayis','FRONT_Y')
    nema23('parmak_motoru',(mx,my,-5),(0,0,1),(0,1,0),'FRONT_Y')
    mount=kut(mx-31,mx+31,my-31,my+31,-5,1).cut(silz(mx,my,20,-6,2))
    mount=mount.union(kut(mx+31,mx+37,H_UST+70,my+31,-5,1))
    mount=mount.union(kut(316,mx+37,H_UST+70,H_UST+76,-160,1))
    ekle('parmak_motor_braketi',mount,'aluminyum','FRONT_Y')
    holder=kut(x-20,x+20,y+18,H_UST+96,0,27)
    holder=holder.union(kut(x-20,204,H_UST+90,H_UST+96,0,27))
    holder=holder.union(kut(196,204,H_UST+70,H_UST+90,0,27)).union(kut(196,204,H_UST+70,H_UST+76,-160,27))
    channel=capsule(13,6,19)
    ekle('parmak_piston_baglantisi',holder.cut(channel),'aluminyum','FRONT_Y')
    for p in PARCALAR:
        if p['ad'].startswith('parmak_yatak_ayagi_'):p['wp']=p['wp'].cut(channel)
    # Last bearing/shaft face is z=28, holder z=27: remain behind the z=29
    # cabinet cross-member throughout the complete vertical head stroke.

def elektrik():
    _v9_elektrik()
    p=next(p for p in PARCALAR if p['ad']=='klemens_sirasi')
    p['wp']=p['wp'].translate((0,-65,0))
    ekle('din_rayi_ek_klemens',kut(450,770,1632,1667,-822,-815),'celik')
    for i in range(7,12):
        ekle('surucu_STP-DRV-4830_%d'%i,TC.din_parca(TC.SURUCU_STEP,90+50*i,1687,-787),'kart')
    # Never imply that enable multiplexing turns four PTO channels into thirteen
    # independently controlled holding axes. Controller/I-O selection is OPEN.
    p=next(p for p in PARCALAR if p['ad']=='plc_S7-1200_1214C')
    p['bom']=("S7-1200 supervisory PLC; motion expansion REQUIRED",1,"12 independent motor drivers; PTO/fieldbus hardware not selected", "not an approved wiring design")

def modul():
    result=_v9_modul()
    p={p['ad']:p for p in PARCALAR}
    def pocket(a,b):p[a]['wp']=p[a]['wp'].cut(p[b]['wp'])
    # Actual fitted pockets, not collision exclusions. These leave mating faces.
    for i in range(2):
        pocket('kose_takim_sabit_kopru','kose_takim_kilavuz_'+str(i))
        pocket('kose_takim_hareketli_cerceve','kose_takim_burc_govde_'+str(i))
        pocket('flap_kilavuz_diregi_'+str(i),'flap_kilavuz_kelepce_'+str(i)+'1')
        for mate in ('flap_katlayici_alt_bagi','flap_katlayici_somun_kolu'):
            pocket('flap_burc_baglantisi_'+str(i),mate)
    pocket('kose_takim_vida_yatak_govdesi','kose_takim_motor_ayaklari')
    for g in CORNER:
        for suffix in ('rulman_1','yatak_govdesi','motor_kelepcesi'):
            pocket('kose_takim_hareketli_cerceve','kose_'+g+'_'+suffix)
        pocket('kose_'+g+'_katlama_kolu','kose_'+g+'_gobek')
        pocket('kose_'+g+'_katlama_kolu','kose_'+g+'_mil')
    pocket('devirme_parmagi','parmak_tahrik_yan_kolu')
    pocket('parmak_tahrik_yan_kolu','parmak_mili')
    pocket('parmak_motor_braketi','piston_kaburgasi_0')
    pocket('parmak_motor_braketi','parmak_piston_baglantisi')
    for i in range(2):
        pocket('parmak_piston_baglantisi','parmak_yatak_ayagi_'+str(i))
        pocket('parmak_piston_baglantisi','parmak_yatagi_'+str(i))
    pocket('flap_lineer_burc_govdesi_0','flap_katlayici_somun_kolu')
    p['flap_katlayici_kaplini']['wp']=p['flap_katlayici_kaplini']['wp'].cut(sily(750,-300,5.05,709,723))
    p['flap_katlayici_yatak_braketi']['wp']=p['flap_katlayici_yatak_braketi']['wp'].cut(sily(750,-300,13,723,733))
    return result
