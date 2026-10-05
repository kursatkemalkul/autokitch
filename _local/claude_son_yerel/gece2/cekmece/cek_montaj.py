# -*- coding: utf-8 -*-
"""TEK ÇEKMECE MONTAJ ANİMASYONU (B dolabı · K2 sütunu · orta sıra = CEK_K2_lahm_3) · 4 Eki 2026 · yerel
plan.md'deki atölye sırası → hareketler (ist-montaj arayüzü: c, m, bb, g, h, k) → yol denetimi (2 mm adım, üçgen düzeyinde CCD)
→ cekmece_montaj.glb + cekmece_montaj.json"""
import sys, os, json, pickle, struct, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
A6 = os.path.join(HERE, '..', 'adim6'); sys.path.insert(0, A6); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim as Y
import glbio
Y.ADIM = 0.002                       # 2 mm adım (her hareket; ray boyunca sürme dahil)
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'cekmece_montaj')
P = pickle.load(open('parca.pkl', 'rb'))

# ------------------------------------------------------------------ montaj sehpası (tezgâh) — çekmece burada kurulur
S = 900.0          # tezgâh konumu: çekmece son yerinden +z 900 mm önde
def kutu(x0, x1, y0, y1, z0, z1):
    v = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float) / 1000
    f = [[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6], [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3]]
    return v, np.array(f)
v, f = kutu(1520, 2010, 0, 421.5, 330, 900)
P['tezgah'] = dict(V=v, F=f, m='tezgah', tur='cevre', ac='montaj tezgâhı')

CEVRE = [a for a in P if P[a]['tur'] == 'cevre']
HAR = {a: [] for a in P}; GOR = {a: 0.0 for a in P}; KAY = set(); ROT = {a: [] for a in P}
ADIM, OLAY, KAM = [], [], []
t = 0.0


def mm(v): return [round(x / 1000, 6) for x in v]


def hareket(parcalar, bacaklar, olay=None, bas=None):
    """bacaklar: [(dx,dy,dz mm, süre s)] — parça son yerinden Σd uzakta belirir, bacakları sırayla kat eder"""
    global t
    t0 = t if bas is None else bas
    tt = t0
    for a in parcalar:
        if not HAR[a] and a not in KAY: GOR[a] = round(t0, 3)
    for d, sure in bacaklar:
        for a in parcalar: HAR[a].append([round(tt, 3), round(tt + sure, 3)] + mm(d))
        tt += sure
    if olay: OLAY.append([round(t0, 3), olay])
    t = max(t, tt)
    return t0, tt


def grup_bacak(parcalar, d, sure, olay=None):
    """zaten görünür parçaların ortak hareketi (çekmecenin raya sürülmesi)"""
    global t
    for a in parcalar: HAR[a].append([round(t, 3), round(t + sure, 3)] + mm(d))
    if olay: OLAY.append([round(t, 3), olay])
    t += sure


def cek(parcalar, sure, olay):
    """kablo / kayış: kanal boyunca çekme · kasnaklara sarma (yerinde uzar — tek istisna)"""
    global t
    for a in parcalar:
        HAR[a] = [[round(t, 3), round(t + sure, 3), 0, 0, 0]]; GOR[a] = round(t, 3); KAY.add(a)
    OLAY.append([round(t, 3), olay]); t += sure


def bekle(s):
    global t; t += s


def adim(ad, metin, liste, kam):
    ADIM.append(dict(no=len(ADIM) + 1, ad=ad, t0=round(t, 3), metin=metin, liste=liste))
    KAM.append([round(t, 3), kam[0], kam[1]])


# kamera noktaları (konum, hedef) — metre
K_ARKA = ([2.10, 0.98, 0.42], [1.56, 0.46, -0.66])
K_RAY = ([2.35, 0.95, 1.05], [1.70, 0.44, -0.33])
K_SOL = ([2.05, 0.80, 0.55], [1.47, 0.46, -0.33])
K_TEZ = ([2.75, 1.25, 1.95], [1.77, 0.43, 0.62])
K_SUR = ([3.05, 1.15, 1.85], [1.75, 0.44, 0.15])
K_ON = ([1.98, 0.78, 0.62], [1.50, 0.45, -0.12])
K_SON = ([2.55, 0.92, 1.30], [1.76, 0.44, -0.22])
K_VIDA = ([1.86, 0.63, 0.22], [1.45, 0.445, -0.33])
K_TEZM = ([2.12, 0.82, 1.18], [1.62, 0.44, 0.55])
CEKMECE = ['cekmece_govdesi', 'silikon_tepsi', 'kizak_lamasi_sol', 'kizak_lamasi_sag', 'kizak_sol', 'kizak_sag',
           'kayis_lamasi', 'miknatis', 'on_braket_sol', 'on_braket_sag']
MOTOR_GRUP = ['motor_braketi', 'motor', 'motor_flansi', 'arka_kasnak']
TM = (150, -3, 1300)        # motor alt montajı tezgâhta: son yerinden +x 150, −y 3 (braket tezgâha oturur), +z 1300

# ================================================================== PLAN (plan.md ile birebir)
KAM.append([0.0, K_TEZ[0], K_TEZ[1]])
bekle(1.0)
adim('Tezgâh: motor grubu',
     'Tahrikin arka grubu tezgâhta hazırlanır: motor braketi tezgâha konur; step motor (mili, arka kapağı ve kablo rakoruyla) ve flanşı kendi ekseni boyunca yandan braketin içine sürülüp vidalanır; GT3 motor kasnağı mile karşı taraftan, mil ekseninde takılır. Motor dolabın içinde braketin içine giremez — arkadaki dikey kablo kanalı yolu kapatır; bu yüzden grup tezgâhta kurulur.',
     'motor braketi · step motor (mil + arka kapak + kablo rakoru) · motor flanşı · GT3 motor kasnağı', K_TEZM)
hareket(['motor_braketi'], [((0, 120, 0), 1.2)], 'Motor braketi tezgâha konur')
bekle(0.2)
hareket(['motor', 'motor_flansi'], [((60, 0, 0), 1.3)], 'Step motor kendi ekseninde braketin içine sürülür')
bekle(0.2)
hareket(['arka_kasnak'], [((-30, 0, 0), 1.0)], 'GT3 motor kasnağı mile takılır (mil ekseninde)')
bekle(0.5)

adim('Motor grubu arka duvara',
     'Motor grubu tezgâhtan kaldırılır, önden çerçeve açıklığından bölmeye girer ve braket arka duvara oturup cıvatalanır. Sol sabit ray henüz takılı değildir; kasnak sol taraftan rahat geçer.',
     'motor grubu (4 parça) · braket → arka duvar', K_ARKA)
grup_bacak(MOTOR_GRUP, (0, TM[1], 0), 0.5, 'Motor grubu tezgâhtan kaldırılır')
grup_bacak(MOTOR_GRUP, (TM[0], 0, 0), 1.0, None)
grup_bacak(MOTOR_GRUP, (0, 0, TM[2]), 3.2, 'Motor grubu önden girer, braket arka duvara oturur')
bekle(0.6)

adim('Sensör plakası · sabit raylar',
     'Sensör lamasının arka plakası yukarıdan arka duvara oturur. Sol ve sağ sabit raylar (bilyalı teleskop rayın dış profili) önden, çerçeve açıklığından bölmeye girer; sonra yana kayıp bölme sacına yaslanır. Ray delikleri bölmedeki PEM somunlarının hizasındadır.',
     'sensör plakası · sabit ray sol · sabit ray sağ', K_RAY)
hareket(['sensor_plakasi'], [((0, 40, 0), 0.9)], 'Sensör plakası yukarıdan arka duvara oturur')
bekle(0.2)
t0 = t
hareket(['sabit_ray_sol'], [((0, 0, 800), 2.2), ((10, 0, 0), 0.7)], 'Sabit raylar önden girer, bölme saclarına yaslanır', bas=t0)
t = t0
hareket(['sabit_ray_sag'], [((0, 0, 800), 2.2), ((-10, 0, 0), 0.7)], None, bas=t0)
bekle(0.5)

adim('Ray vidaları',
     'Her ray 3 adet M5 × 10 havşa başlı vidayla bölme sacındaki PEM somununa vidalanır (toplam 6). Vidalar ray gövdesine dik, kendi eksenleri boyunca girer; arkadaki köpük kapağı PU sızıntısını önler.',
     '6 × M5 × 10 havşa başlı (DIN 7991) · PEM SP-M5 bölmede hazır', K_VIDA)
for k in (1, 2, 3):
    t0 = t
    hareket(['vida_sol_%d' % k], [((40, 0, 0), 0.7)], 'Ray vidası %d / 3 (sol ve sağ) — kendi ekseninde' % k, bas=t0)
    t = t0
    hareket(['vida_sag_%d' % k], [((-40, 0, 0), 0.7)], None, bas=t0)
    bekle(0.15)
bekle(0.5)

adim('Avara braketi · reed sensörler',
     'Ön avara braketi ile sensör laması tek kaynaklı parçadır: bölmenin içinden yana kayarak yerine gelir, kulağı ön çerçevenin arkasına cıvatalanır. İki reed sensör (kapalı ve açık konum) lamanın altına aşağıdan takılır.',
     'avara braketi + sensör laması · reed sensör (arka = kapalı) · reed sensör (ön = açık)', K_SOL)
hareket(['avara_braketi'], [((30, 0, 0), 1.2)], 'Avara braketi + sensör laması yana kayarak yerine gelir')
bekle(0.3)
t0 = t
hareket(['reed_arka'], [((0, -20, 0), 0.8)], 'Reed sensörler lamanın altına aşağıdan takılır', bas=t0)
t = t0
hareket(['reed_on'], [((0, -20, 0), 0.8)], None, bas=t0)
bekle(0.5)

adim('Ara raylar',
     'Ara raylar (teleskobun orta profili) önden, ray ekseni boyunca sabit rayın içine sürülür.',
     'ara ray sol · ara ray sağ', K_RAY)
t0 = t
hareket(['ara_ray_sol'], [((0, 0, 760), 2.6)], 'Ara raylar ray ekseni boyunca sabit rayın içine sürülür', bas=t0)
t = t0
hareket(['ara_ray_sag'], [((0, 0, 760), 2.6)], None, bas=t0)
bekle(0.6)

adim('Tezgâh: çekmece gövdesi · silikon tepsi',
     'Çekmece tezgâhta kurulur: sac tava (çekmece gövdesi) tezgâha konur, silikon tepsi üstten içine yerleşir.',
     'çekmece gövdesi (sac tava) · silikon tepsi', K_TEZ)
hareket(['cekmece_govdesi'], [((0, 150, 0), 1.2)], 'Çekmece gövdesi tezgâha konur')
bekle(0.2)
hareket(['silikon_tepsi'], [((0, 120, 0), 1.0)], 'Silikon tepsi gövdenin içine yerleşir')
bekle(0.5)

adim('Tezgâh: kızaklar · kayış laması · ön braketler',
     'Kızak bağlantı lamaları gövdenin iki yanına, kızaklar (teleskobun iç profili) lamalara vidalanır. Sol yana kayış kelepçe laması, üstüne mıknatıs yuvası takılır. Ön kapak braketleri gövdenin önüne oturur.',
     'kızak laması sol / sağ · kızak sol / sağ · kayış laması · mıknatıs · ön braket sol / sağ', K_TEZ)
t0 = t
hareket(['kizak_lamasi_sol'], [((-40, 0, 0), 0.8)], 'Kızak lamaları gövdenin yanlarına', bas=t0)
t = t0
hareket(['kizak_lamasi_sag'], [((40, 0, 0), 0.8)], None, bas=t0)
bekle(0.2)
t0 = t
hareket(['kizak_sol'], [((-40, 0, 0), 0.8)], 'Kızaklar lamalara vidalanır', bas=t0)
t = t0
hareket(['kizak_sag'], [((40, 0, 0), 0.8)], None, bas=t0)
bekle(0.2)
hareket(['kayis_lamasi'], [((0, 40, 0), 0.8)], 'Kayış kelepçe laması sol yana')
bekle(0.1)
hareket(['miknatis'], [((0, 40, 0), 0.7)], 'Mıknatıs yuvası lamanın üstüne')
bekle(0.1)
t0 = t
hareket(['on_braket_sol'], [((0, 0, 40), 0.8)], 'Ön kapak braketleri gövdenin önüne', bas=t0)
t = t0
hareket(['on_braket_sag'], [((0, 0, 40), 0.8)], None, bas=t0)
bekle(0.6)

adim('Çekmece raylara sürülür',
     'Kurulan çekmece tezgâhtan alınır, kızaklar ara rayların ağzına hizalanır ve çekmece ray ekseni boyunca, düz bir çizgide içeri sürülür. Kızak ara rayın içinde, profiller hizalı ilerler; çekmece arka konumda durur.',
     'çekmece grubu (10 parça) · 900 mm sürme · ray ekseni z', K_SUR)
grup_bacak(CEKMECE, (0, 0, S), 5.5, 'Çekmece ray ekseni boyunca içeri sürülür — kızak ara rayın içinde')
bekle(0.6)

adim('Avara kasnağı · kayış',
     'Ön avara kasnağı miliyle birlikte önden braketine takılır. GT3 kayış motor kasnağı ile avara kasnağına sarılır, üst kolu çekmecedeki kelepçe lamasına sıkılır ve avara braketinden gerdirilir.',
     'GT3 avara kasnağı + mili · GT3 kayış (sarma)', K_ON)
hareket(['avara_kasnagi'], [((0, 0, 60), 1.0)], 'Avara kasnağı miliyle önden braketine takılır')
bekle(0.3)
cek(['kayis'], 1.8, 'GT3 kayış kasnaklara sarılır, kelepçeye sıkılır, gerdirilir')
bekle(0.5)

adim('Ön panel · ön kapak',
     'Ön panel çekmecenin ön kapak braketlerine, şeffaf ön kapak da panelin önüne takılır.',
     'ön panel · ön kapak (şeffaf)', K_SON)
hareket(['on_panel'], [((0, 0, 240), 1.2)], 'Ön panel braketlere takılır')
bekle(0.2)
hareket(['on_kapak'], [((0, 0, 240), 1.2)], 'Şeffaf ön kapak takılır')
bekle(0.5)

adim('Kablolar',
     'Reed sensör kabloları ve motor kablosu bölmedeki kablo kanalı boyunca arkaya, oradan dikey kanala çekilir.',
     'reed sensör kabloları · motor kablosu', K_ARKA)
cek(['kablo_sensor', 'kablo_motor'], 2.4, 'Sensör ve motor kabloları kanal boyunca çekilir')
bekle(0.6)
KAM.append([round(t, 3), K_SON[0], K_SON[1]])
bekle(2.4)
TOPLAM = round(t, 2)
for i, a in enumerate(ADIM): a['t1'] = ADIM[i + 1]['t0'] if i + 1 < len(ADIM) else TOPLAM

# ------------------------------------------------------------------ YOL DENETİMİ
haric = {('arka_kasnak', 'kayis')}           # kayış dişi kasnak dişine geçer (son konum, model teması)
VIDA = ['vida_%s_%d' % (s_, k_) for s_ in ('sol', 'sag') for k_ in (1, 2, 3)]
for v_ in VIDA: haric.add(tuple(sorted((v_, 'cevre_kopuk_kapagi'))))   # MODEL GİRİŞİMİ: vida ucu köpük kapağı tabanını deliyor (son konumda var) — aşağıda ölçülür, raporda
t1 = time.time()
DN = Y.Denetci(P, HAR, ROT, GOR, KAY, set(), haric)
CAK = DN.denetle(ilerleme=False)
print('YOL: çift %d · çakışma %d · %.0f s' % (DN.ciftsay, len(CAK), time.time() - t1), flush=True)
for r in CAK: print('  ÇAKIŞMA', r)
# vida ucu ↔ köpük kapağı tabanı: son konumdaki girişim (model hatası, yol değil) — ölçü
Kk = P['cevre_kopuk_kapagi']['V'] * 1000
DIS = {}
for v_ in VIDA:
    vv = P[v_]['V'] * 1000; sol = 'sol' in v_
    m_ = (np.abs(Kk[:, 2] - (vv[:, 2].min() + vv[:, 2].max()) / 2) < 6)
    taban = Kk[m_, 0].min() if sol else Kk[m_, 0].max()
    uc = vv[:, 0].min() if sol else vv[:, 0].max()
    DIS[v_] = round(float(taban - uc) if sol else float(uc - taban), 2)
print('VİDA UCU köpük kapağı tabanını geçiyor (mm):', DIS)
# belirme: her parça (çevre ve çekme hariç) en az bir sıfırdan farklı bacakla gelir
BELIRME = [a for a in P if a not in CEVRE and a not in KAY and not any(abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 for h in HAR[a])]
# havada: oturduğu anda yerinde bir parçaya ≤ 0,6 mm değmeli (son konum); tezgâh aşaması ayrıca
TEM = Y.temas_denetim(P, HAR, GOR, KAY, set(), tol=6e-4, turler=('ray', 'sac', 'mek', 'baglanti', 'kapak'))
HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l)
# tezgâh aşaması: tezgâhta duran parçalar (S kadar önde) — kendi aralarında + tezgâh
def tezgah_temas(parcalar, ofs, n_grup):
    PS = {a: dict(V=P[a]['V'] + np.array(ofs) / 1000, F=P[a]['F'], tur=P[a]['tur']) for a in parcalar}
    PS['tezgah'] = P['tezgah']
    HS = {a: HAR[a][:-n_grup] for a in parcalar}; HS['tezgah'] = []
    GS = {a: GOR[a] for a in PS}
    return Y.temas_denetim(PS, HS, GS, set(), set(), tol=6e-4, turler=('ray', 'sac', 'mek', 'kapak'))
TEM_S = tezgah_temas(CEKMECE, (0, 0, S), 1)
TEM_S.update({'motor:' + k: v for k, v in tezgah_temas(MOTOR_GRUP, TM, 3).items()})
HAVADA_S = sorted(a for a, (tl, l) in TEM_S.items() if not l)
print('BELİRME', BELIRME, '· HAVADA (son)', HAVADA, '· HAVADA (tezgâh)', HAVADA_S)
for a, (tl, l) in TEM.items(): print('  temas %-18s t=%6.2f  ← %s' % (a, tl, l[:4]))
for a, (tl, l) in TEM_S.items(): print('  tezgâh temas %-18s t=%6.2f  ← %s' % (a, tl, l[:4]))

# ------------------------------------------------------------------ GLB + JSON
MATAD = ['sac', 'kapak', 'profil', 'kaynak', 'baglanti', 'arayuz', 'pu', 'yalitim', 'mekanizma', 'motor', 'alu', 'koyu', 'sensor', 'elektrik',
         'kanal', 'fis', 'guc', 'bilgi', 'hava', 'kapak_s', 'urun', 'silik', 'tezgah', 'tepsi']
MATS = [dict(name=m, pbrMetallicRoughness=dict(baseColorFactor=[0.8, 0.8, 0.8, 1], metallicFactor=0.5, roughnessFactor=0.4)) for m in MATAD]
os.makedirs(OUT, exist_ok=True)
dug, PARCA = [], {}
for a in P:
    V = P[a]['V']; c = np.round((V.min(0) + V.max(0)) / 2, 4)
    dug.append(dict(ad=a, V=(V - c).astype(np.float32), F=np.asarray(P[a]['F'], np.uint32), mat=MATAD.index(P[a]['m']), translation=c))
    PARCA[a] = dict(c=c.tolist(), m=P[a]['m'], bb=[np.round(V.min(0), 6).tolist(), np.round(V.max(0), 6).tolist()], g=GOR[a], h=HAR[a], ad=P[a]['ac'])
    if a in KAY: PARCA[a]['k'] = 1
yol = os.path.join(OUT, 'cekmece_montaj.glb')
glbio.yaz(yol, dug, MATS)
f = open(yol, 'rb').read(); L = struct.unpack('<I', f[12:16])[0]; JJ = json.loads(f[20:20 + L]); rest = f[20 + L:]
for nd, d in zip(JJ['nodes'], dug): nd['translation'] = [float(x) for x in d['translation']]
js = json.dumps(JJ, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
while len(js) % 4: js += b' '
f = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack('<II', len(js), 0x4E4F534A) + js + rest
open(yol, 'wb').write(f)
gos = [a for a in P if a not in CEVRE]
DENETIM = dict(adim=len(ADIM), hareket=sum(1 for a in gos if HAR[a] and a not in KAY), cift=DN.ciftsay, cakisma=len(CAK),
               vida_kopuk_kapagi_mm=DIS, belirme=len(BELIRME), havada=len(HAVADA) + len(HAVADA_S), cekme=sorted(KAY), adim_mm=Y.ADIM * 1000,
               siyirma_mm=Y.SINIR * 1000, oturma_mm=Y.OTURMA * 1000, haric=[list(x) for x in haric])
OUTJ = dict(surum='cekmece_montaj_v1', ist='CEKMECE', tarih='4 Eki 2026', kaynak='hat3_v9j.glb · CEK_K2_lahm_3 (B · K2 sütunu · orta sıra) + B gövdesi (silik, kırpılmış)',
            birim='m', toplam=TOPLAM, baslik=dict(kod='B · K2-3'),
            zarf=[[1.40, 0.0, -0.80], [2.12, 0.52, 0.95]], ghost=[], ghost_t=None,
            adimlar=ADIM, olaylar=OLAY, kamera=KAM, parcalar=PARCA, acinim=[], montaj_sirasi=[],
            sayim=dict(gosterilen=len(gos), cevre=len(CEVRE), ucgen=int(sum(len(P[a]['F']) for a in P))), denetim=DENETIM)
json.dump(OUTJ, open(os.path.join(OUT, 'cekmece_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
pickle.dump(dict(HAR=HAR, GOR=GOR, KAY=KAY, CAK=CAK, BELIRME=BELIRME, HAVADA=HAVADA, HAVADA_S=HAVADA_S, TEM=TEM, TEM_S=TEM_S, ADIM=ADIM, OLAY=OLAY,
                 DENETIM=DENETIM, TOPLAM=TOPLAM), open('sonuc.pkl', 'wb'))
print('parça', len(gos), 'çevre', len(CEVRE), 'süre', TOPLAM, 's · adım', len(ADIM), '· GLB %.2f MB' % (len(f) / 1e6))
