# -*- coding: utf-8 -*-
"""E (KUTU KATLAMA) MONTAJ ANİMASYONU v2 (model: hat3_v10h · zincir 00–66) · 5 Eki 2026 · Claude · bulut oturumu
Girdi: e_parca.pkl (e_parca.py), acinim_E (adım 35 E gövde: h3_e_sac_v1) · Çıktı: plan_e.pkl → e_cikti.py
Altyapı: _altyapi.py (TOPPING v6 / F v2 ile aynı: zaman çizelgesi, plan anı yol denetimi, yerleştirici).
Kapsam: kaide + ayaklar, kaynaklı alt montaj (taban + ön kasa + kulaklar), şarjör + asansör, besleyici, kalıp / köprü / kapak / köşe / parmak /
piston mekanizmaları, yan / üst / arka saclar (FHP saplama + içten pul + fiberli somun), E panosu + fiş paneli + kablolar + vakum hattı,
4 ön kapak + menteşe + bas-aç + emniyet, şarjör yan kapısı, robot çöpü. Karton yığını işletmede doldurulur → bu animasyonda yok."""
import sys, os, json, pickle, math, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_t5 as SM
import re as _re
T0 = time.time()
D0 = pickle.load(open('e_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']
for a in [a for a in P if a.startswith('karton_stok')]: del P[a]

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]
    if ad not in P: continue
    s = SM.Sac(ad); SAC[ad] = s
    old = P[ad]
    V, F = (s.dunya(s.yerel({})), s.F) if s.bukum else (old['V'], old['F'])
    P[ad] = dict(old, V=V, F=F, Vm=old['V'], Fm=old['F'], model_lo=old['V'].min(0), model_hi=old['V'].max(0))
print('sac', len(SAC))
AD_TR = {'taban_sac_3': 'Taban 3 mm', 'sol_sac_pizza_penceresi': 'Yan sol 1,5 (pizza penceresi)', 'sag_sac': 'Yan sağ 1,5 (şarjör açıklığı)',
         'arka_sac': 'Arka sac 1,5', 'ust_sac': 'Üst sac 1,5', 'govde_kosebent_sag_arka_alt': 'Köşebent sağ arka alt',
         'kaide_e_ray_on': 'Kaide ön ray 60 × 60', 'kaide_e_ray_arka': 'Kaide arka ray 60 × 60', 'onyuz_dikme_sol': 'Ön dikme sol', 'onyuz_dikme_orta': 'Ön dikme orta',
         'onyuz_dikme_sag': 'Ön dikme sağ', 'sarjor_yan_kapisi': 'Şarjör yan kapısı 1,5', 'sarjor_yan_kapisi_ic_tava': 'Şarjör kapısı iç tava',
         'sarjor_yan_kapisi_mentese_lamasi': 'Kapı menteşe laması 3', 'sarjor_yan_kapisi_basac_lamasi': 'Bas-aç laması 3'}
def bk(x): return x.replace('_', ' ')
def tr(a):
    if a in AD_TR: return AD_TR[a]
    m = _re.match(r'onyuz_kapak_E_(alt|ust)_(sol|sag)$', a)
    if m: return 'Kapak %s %s (dış tava 1,5)' % ({'alt': 'alt', 'ust': 'üst'}[m.group(1)], {'sol': 'sol', 'sag': 'sağ'}[m.group(2)])
    return P[a]['ac'].split('·')[0].split(';')[0].strip() if a in P else a
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2

# ------------------------------------------------------------------ PEM / FHP saplama → sac (üretimde preslenir, sacla gelir) · host.json: baş hangi sacın yüzüyle aynı
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
HOST = json.load(open('host.json'))
for p, h in HOST.items():
    if p not in P or not h: continue
    s, yan = h
    if s not in P: continue
    pem_bagla(p, s, yan, 'PEM FHP-M6' if 'taban_3' in p or p.startswith('arayuz_mek_taban') else 'PEM FHP-M5')
for p in [a for a in P if a.startswith('govde_pem_m8_ust')]: pem_bagla(p, 'ust_sac', (0, -1.0, 0), 'PEM SP-M8')
for p in [a for a in P if a.startswith('e_arka_pem_')]: pem_bagla(p, 'sol_sac_pizza_penceresi', (0, 0, 1.0), 'PEM S-M5 (zincir 69)')
for p in [a for a in P if a.startswith('e_arka_civata_')]: P[p]['eks'] = np.array([0, 0, 1.0])
for p in [a for a in P if _re.match(r'emniyet_E_([A-Z]+_[A-Z]+)_\d_somun$', a)]:
    pem_bagla(p, 'emniyet_E_%s_braket' % _re.match(r'emniyet_E_([A-Z]+_[A-Z]+)_', p).group(1), (0, 0, -1.0), 'PEM S-M4-2 (sensör braketi)')
for p in [a for a in P if _re.match(r'emniyet_E_[A-Z]+_[A-Z]+_\d_vida$', a)]: P[p]['eks'] = np.array([0, 0, -1.0])
pem_bagla('besleyici_motor_yuvasi_braketi_saplama', 'sag_sac', (1.0, 0, 0), 'PEM FHP-M4 (zincir 85 · motor yuvası köşebendi)')
print('PEM / saplama', {k: len(v) for k, v in PEM_SAC.items()})
# pul / somun giriş ekseni: saplamanın ucundan başa doğru (baş = yan)
for a in list(P):
    m = _re.match(r'(.+)_(pul|somun)$', a)
    if m and m.group(1) + '_saplama' in P and 'yan' in P[m.group(1) + '_saplama']:
        P[a]['eks'] = P[m.group(1) + '_saplama']['yan'].copy()
for a in [a for a in P if a.startswith(('kaide_e_vida', 'arayuz_uke_m8'))]: P[a]['eks'] = np.array([0, -1.0, 0])
for a in [a for a in P if _re.match(r'ayak_\d+(_kontra)?$', a)]: P[a]['eks'] = np.array([0, 1.0, 0])
for a in [a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit_vida', a)]: P[a]['eks'] = np.array([-1.0 if '_sol_' in a else 1.0, 0, 0])

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())
# yerel 6 Eki: CCD temas bulunca hareket boyunca 2 mm adımla GERÇEK kesişim (0,3 mm) aranır — sıfır boşluklu delikte eksen boyunca kayma çarpışma sayılmaz
# (e_cikti 1b doğrulamasıyla aynı ölçüt; son denetim yine tam ağla yapılır)
def _gercek_kesisim(a, b, ofs, v_m):
    A0 = tri(a) + np.asarray(ofs, float) / 1000.0; B = tri(b); n_ = max(2, int(np.ceil(np.linalg.norm(v_m) * 1000.0 / 2.0)) + 1)
    lo_b = B.min((0, 1)); hi_b = B.max((0, 1))
    for s_ in np.linspace(0.0, 1.0, n_):
        A = A0 + s_ * v_m; sa = np.all(A.min(1) <= hi_b, 1) & np.all(A.max(1) >= lo_b, 1)
        if sa.any() and int(Y.poz_kesisim(np.ascontiguousarray(A[sa]), np.ascontiguousarray(B), 3e-4).sum()): return True
    return False
_serbest0 = serbest
def serbest(adlar, ofs, yerinde, ofs2=None):
    ofs_ = np.asarray(ofs, float); ofs2_ = np.zeros(3) if ofs2 is None else np.asarray(ofs2, float)
    return [(a, b) for a, b in _serbest0(adlar, ofs, yerinde, ofs2) if _gercek_kesisim(a, b, ofs_, (ofs2_ - ofs_) / 1000.0)]

_kg = kamera_genel
def kamera_genel(adlar, **k):                                                    # E dar ve uzun: adım kamerası 1,6 kat geride (bütün istasyon görünsün)
    k['olcek'] = k.get('olcek', 1.25) * 1.6; return _kg(adlar, **k)
# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
def haric(a, b, neden): HARIC_PLAN.add((a, b)); HARIC_NEDEN[(a, b)] = neden
for a_, b_, n_ in json.load(open(os.path.join(HERE, 'mek_ic_ice.json'), encoding='utf-8')):
    haric(a_, b_, ('MODEL AÇIĞI (E mekanizma üreteci): son konumda iç içe %d üçgen — sıkı geçme / göbek ↔ mil / kasnak ↔ kayış (üreteçte boşluk yok)' % n_) if n_ else
          'MODEL AÇIĞI (E mekanizma üreteci): GÖMÜLÜ — mil / motor mili / blok karşı parçanın içinde deliksiz modellenmiş (gerçekte delik / yuva var; üreteçte açılacak)')
for st_ in [a for a in P if a.startswith(('arayuz_mek', 'arayuz_j3'))]:
    lo_, hi_ = kutu(st_)
    for m_ in [m for m in P if P[m]['tur'] in ('mek',) and np.all(kutu(m)[0] <= hi_ + 1) and np.all(kutu(m)[1] >= lo_ - 1)]:
        haric(st_, m_, 'arayüz saplaması mekanizma kulağındaki deliğe eksen boyunca geçer (model sıfır boşluk)')
KAY = lambda pre: sorted(k for k in P if k.startswith(pre) and P[k]['tur'] == 'kaynak')
def koy(adlar, adaylar, metin, **k):
    global t
    if isinstance(adlar, str): adlar = [adlar]
    return yerlestir(list(adlar), adaylar, t, metin, **k)
def sira_tak(adlar, t0, yol, sure=0.5, ara=0.12, ofs0=None):
    tt = t0
    for i, a in enumerate(adlar): tt = tak(a, t0 + i * ara, sure, yol, ofs0=ofs0)
    return tt
def AD(*yon, lift=(20, 40, 120, 300, 500), yan=(30, -30), son=()):
    """yön(ler)den yaklaş · lift: yukarıdan in · yan: x ofsetle · son: son bacak (saplamaya eksen boyunca oturma)"""
    L_ = []
    for d in yon: L_.append(YOL(d))
    for d in yon:
        for e in son: L_.append(YOL(d, e))
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
ON9, ARKA9, UST6 = (0, 0, 900), (0, 0, -900), (0, 600, 0)
SAG7, SOL7 = (900, 0, 0), (-900, 0, 0)
SON = [(15, 0, 0), (-15, 0, 0), (0, 15, 0), (0, -15, 0), (0, 0, -15), (0, 0, 15), (30, 0, 0), (-30, 0, 0), (0, 30, 0), (0, -30, 0)]
def vidala(adlar, t0, yol=30.0):
    tt = t0
    for i_, a_ in enumerate(adlar):
        for b in [b for b in (a_[:-6] + '_pul',) if a_.endswith('_somun') and b in P]: tt = max(tt, tak(b, t0 + i_ * 0.12, 0.4, yol))
        tt = max(tt, tak(a_, t0 + i_ * 0.12 + 0.3, 0.5, yol))
    return tt
def somunla(rx, t0, yol=25.0):
    return vidala(sorted(a for a in P if _re.match(rx, a) and a.endswith('_somun')), t0, yol)
def var(*adlar): return [a for a in adlar if a in P]
# ------------------------------------------------------------------ E MEKANİZMA TEZGÂHI (zincir 81–85 · yerel oturum 6 Eki): modül parça parça tezgâhta kurulur, her bağlantı elemanı
# kendi ekseninde tek tek; sonra modül bütün olarak yerine. Tezgâh = makinenin önünde TEZ ofsetinde (aynı ofsetteki parçalar arasında yol denetimi).
BAG = {}
for s_ in 'mnopq': BAG.update(json.load(open(os.path.join(HERE, 'ent', 'hat3_v10%s_ent.json' % s_), encoding='utf-8'))['baglanti'])
for f_, b_ in BAG.items():
    if f_ in P and 'eks' in b_: P[f_]['eks'] = np.asarray(b_['eks'], float) * (1.0 if 'hedef' in b_ else -1.0)   # vida / pim / setskur: eksen boyunca · somun / pul / segman: yüze doğru
MEKAD = {a: P[a]['aile'] for a in P if P[a].get('mek_ad')}
TEZ = np.array([0.0, 0.0, 1500.0]); TEZ_YER = []; TEZDE = set()
def _ic(a, b, tol=0.6): return np.all(LO_[a] <= HI_[b] + tol) and np.all(HI_[a] >= LO_[b] - tol)
LO_ = {a: P[a]['V'].min(0) for a in P}; HI_ = {a: P[a]['V'].max(0) for a in P}
YENI81 = [a for a in P if a in BAG and BAG[a].get('yeni')]                     # zincir 81–85 yeni braketler + kaynak dikişleri
def tez_yol(adlar, adaylar):
    global YERINDE
    k_ = YERINDE; YERINDE = TEZ_YER
    try: return yol_sec(list(adlar), adaylar)
    finally: YERINDE = k_
TEZ_AD = [YOL((0, 150, 0)), YOL((0, 0, 150)), YOL((0, 0, -150)), YOL((150, 0, 0)), YOL((-150, 0, 0)), YOL((0, -150, 0)),
          YOL((0, 150, 0), (0, 0, 40)), YOL((0, 150, 0), (0, 0, -40)), YOL((0, 150, 0), (40, 0, 0)), YOL((0, 150, 0), (-40, 0, 0)),
          YOL((0, 0, 150), (0, 30, 0)), YOL((0, 0, -150), (0, 30, 0)), YOL((150, 0, 0), (0, 30, 0)), YOL((-150, 0, 0), (0, 30, 0)), YOL((0, 400, 0)), YOL((0, 0, 400)), YOL((0, 0, -400))]
def tez_koy(adlar, tt, metin=None, sure=0.45, yol=None):
    if isinstance(adlar, str): adlar = [adlar]
    yol = tez_yol(adlar, ([yol] if yol is not None else []) + TEZ_AD)
    for a in adlar: basla(a, TEZ + yol[0], tt)
    for p0, p1 in zip(yol[:-1], yol[1:]):
        su = max(sure * float(np.linalg.norm(p1 - p0)) / 150.0, 0.25)
        for a in adlar: git(a, TEZ + p1, tt, su)
        tt += su
    vurgu(adlar, tt, tt + 0.9); TEZ_YER.extend(adlar); TEZDE.update(adlar)
    if metin: olay(tt - 0.2, metin)
    return tt
def tez_buyu(a, tt, sure=0.5):
    basla(a, TEZ, tt); ISTISNA.add(a); MF[a] = dict(buyu=[round(tt, 3), round(tt + sure, 3)]); VU[a].append([round(tt, 3), round(tt + sure + 0.8, 3)])
    TEZ_YER.append(a); TEZDE.add(a); return tt + sure
TAKMA = {'e_sag_sac': 'sag_sac', 'e_saplama_asansor': 'arayuz_mek_sag_17', 'e_saplama_besleyici_uc': 'arayuz_mek_sag_18', 'e_saplama_katlama': 'arayuz_mek_sol_9'}   # 85: sac / önceki saplama takma adları
def gerek(f):
    b = BAG[f]; return [TAKMA.get(x, x) for x in (b.get('A'), b.get('B')) if x]
def bag_hazir(yerde):
    """tüm parçaları yerinde olan, henüz takılmamış bağlantı elemanları (vida önce, pul / somun cıvatasından sonra)"""
    out = []
    for f in sorted(BAG):
        if f not in P or f in GOR or 'eks' not in BAG[f] or BAG[f].get('saplama'): continue
        if not all(x in yerde for x in gerek(f)): continue
        m_ = _re.match(r'(.+)_(pul|somun)$', f)
        if m_ and m_.group(1) in BAG and m_.group(1) not in GOR and m_.group(1) not in out: continue
        if f.endswith('_somun') and f[:-6] + '_pul' in BAG and f[:-6] + '_pul' not in GOR and f[:-6] + '_pul' not in out: continue
        out.append(f)
    return out
def kaynak_hazir(yerde):
    return [k for k in YENI81 if P[k]['tur'] == 'kaynak' and k not in GOR and all(b in yerde for b in [b for b in MEKAD if _ic(k, b, 0.3)] or ['_yok_'])]
def yol_mm(f, yerde):
    """bağlantı elemanının ekseni boyunca geri çekilme: 25 → 3 mm, yerindeki parçalara çarpmayan ilki (iki bacak arası boşluğa kısa mesafeden)"""
    e_ = np.asarray(P[f]['eks'], float)
    for L_ in (25.0, 15.0, 10.0, 6.0, 3.0):
        if not serbest([f], -e_ * L_, yerde, ofs2=np.zeros(3)): return L_
    return 3.0
def grupla(L_):
    """aynı parça çiftini bağlayanlar (paralel eksenler) bir grup; gruplar SIRAYLA (birinin yolu ötekinin başlangıcından geçmesin)"""
    G_ = collections.OrderedDict()
    for f in L_: G_.setdefault(tuple(sorted(str(x) for x in gerek(f))) + (_re.sub(r'_(pul|somun)$', '', f).rsplit('_', 1)[0],), []).append(f)
    return list(G_.values())
def tez_baglar(tt, ara=0.08):
    while True:
        L_ = bag_hazir(TEZDE)
        if not L_: break
        for G_ in grupla(L_):
            t1 = tt
            for i_, f in enumerate(G_):
                t1 = max(t1, tak(f, tt + i_ * ara, 0.4, yol_mm(f, TEZ_YER), ofs0=TEZ)); TEZDE.add(f); TEZ_YER.append(f)
            tt = t1 + 0.03
    for k in kaynak_hazir(TEZDE): tt = tez_buyu(k, tt, 0.4)
    return tt
ROL_SIRA = {'tasiyici': 0, 'parca': 1, 'burc': 2, 'mil': 3, 'somun': 3, 'motor': 4, 'kayis': 5, 'sensor': 6, 'vantuz': 6, 'hortum': 7}
def adaylar_(a):
    """tezgâh giriş yolları: eksenler + parçanın kendi ana ekseni (PCA) boyunca 150 / 400 / 800, yukarıdan iki bacaklı"""
    V_ = P[a]['V']; c_ = V_ - V_.mean(0); w_, U_ = np.linalg.eigh(c_.T @ c_); ax_ = U_[:, -1]
    out = []
    for d_ in ((0, 1, 0), (0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, -1, 0), tuple(ax_), tuple(-ax_)):   # 150 mm'de çarpan yön, daha uzunda da çarpar (aynı son bacak) → yalnız 150
        out.append(YOL(tuple(np.asarray(d_, float) * 150.0)))
    for d_ in ((0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0)):
        out.append(YOL((0, 300.0, 0), tuple(np.asarray(d_, float) * 120.0)))
    return out
SOK_KAYIT = {}
PROF = '--prof' in sys.argv
def sira_bul(adlar):
    import __main__, sok_paralel as SP
    tercih = lambda a: (-ROL_SIRA.get(P[a].get('rol', 'parca'), 1), -adlar.index(a))
    f_ = __main__.__dict__.pop('__file__', None)                                # Windows spawn: işçiler bu betiği yeniden çalıştırmasın
    try: return SP.sira_bul_paralel(adlar, adaylar_, tercih, os.path.join(HERE, 'e_parca.pkl'), isci=16)
    finally:
        if f_: __main__.__file__ = f_
def sira_bul_tek(adlar):
    """sökerek montaj sırası: tam modülden yolu serbest olan parça çıkarılır (tercih: sonra gelmesi gereken roller önce); ters sıra = montaj sırası + giriş yolu.
    Hız: bir parça denendiğinde onu engelleyenler kaydedilir; o engellerden biri çıkmadıkça yeniden denenmez."""
    kal = list(adlar); cik = []; engel = {}
    tercih = lambda a: (-ROL_SIRA.get(P[a].get('rol', 'parca'), 1), -adlar.index(a))
    aday = {a: adaylar_(a) for a in adlar}
    while kal:
        kset = set(kal); bul_a = None
        for a in sorted(kal, key=tercih):
            if a in engel and not (engel[a] - kset) and engel[a]: continue          # engelleri hâlâ yerinde
            dig = [b for b in kal if b != a]; eng = set(); _t0 = time.time()
            for yol in aday[a]:
                s_ = []
                for p0, p1 in zip(yol[:-1], yol[1:]):
                    s_ += serbest([a], p0, dig, ofs2=p1)
                    if s_: break
                if not s_: bul_a = (a, yol); break
                eng |= set(b for _, b in s_)
            if PROF: print('    dene %-34s %s %.2f s' % (a, 'OK' if bul_a else 'X', time.time() - _t0), flush=True)
            if bul_a: break
            engel[a] = eng
        if bul_a is None:
            a = sorted(kal, key=tercih)[0]; bul_a = (a, None); SOK_KAYIT[a] = 'sökülemedi: %s' % sorted(engel.get(a, ()))[:4]
        cik.append(bul_a); kal.remove(bul_a[0]); engel.pop(bul_a[0], None)
        if len(cik) % 20 == 0: print('  sökme', len(cik), '/', len(adlar), flush=True)
    return list(reversed(cik))
def modul_kur(aileler, ad, haric_=()):
    """aileler sırasıyla: her parça tezgâhta yerine, ardından hazır olan bağlantılar; yeni braketler bağlandıkları parça gelince"""
    global t
    adlar = [a for fa in aileler for a in sorted((a for a in MEKAD if MEKAD[a] == fa and a not in haric_), key=lambda a: (ROL_SIRA.get(P[a].get('rol', 'parca'), 1), a))]
    def es(b): return set(x for f in BAG for x in (BAG[f].get('A'), BAG[f].get('B')) if b in (BAG[f].get('A'), BAG[f].get('B')) and x and x != b)
    yeni_br = [b for b in YENI81 if P[b]['tur'] != 'kaynak' and b not in haric_ and es(b) & set(adlar)]
    yeni_br = [b for b in yeni_br]
    katilar = [a for a in adlar if P[a].get('rol', 'parca') not in ('kayis', 'hortum')] + yeni_br
    SIRA = sira_bul(katilar); YOLU = dict(SIRA)
    print('sökerek sıra', ad, len(SIRA), 'yolsuz', [a for a, y in SIRA if y is None])
    sargi = [a for a in adlar if P[a].get('rol', 'parca') in ('kayis', 'hortum')]
    for a, _ in SIRA:
        if a in yeni_br: t = tez_koy(a, t, '%s (yeni)' % P[a]['ac'].split('·')[0].strip(), yol=YOLU[a]); t = tez_baglar(t); continue
        t = tez_koy(a, t, tr(a), yol=YOLU[a])
        for k_ in [k_ for k_ in sargi if k_ not in TEZDE and all(b in TEZDE for b in adlar if b != k_ and _ic(k_, b, 0.5) and P[b].get('rol', 'parca') != 'kayis')]:
            t = tez_buyu(k_, t, 0.6); olay(t - 0.3, '%s: kasnaklara / rakorlara sarılır' % tr(k_))
        t = tez_baglar(t)
    for k_ in [k_ for k_ in sargi if k_ not in TEZDE]: t = tez_buyu(k_, t, 0.6)
    t = tez_baglar(t)
    return adlar + [b for b in yeni_br if b in TEZDE]
def modul_tasi(adlar_tum, adaylar, metin):
    """tezgâhtaki modül (parçalar + bağlantı elemanları + kaynaklar) bütün olarak yerine · yol makinede yerinde olanlara göre denetlenir"""
    global t
    yol = None
    for yol_ in adaylar:
        s_ = []
        for p0, p1 in zip(yol_[:-1], yol_[1:]): s_ += serbest([a for a in adlar_tum if P[a]['tur'] not in ('kaynak', 'kablo')], p0, YERINDE, ofs2=p1)
        if not s_: yol = yol_; break
    if yol is None:
        yol = adaylar[0]; PLAN_SORUN.append(dict(parca=adlar_tum[:4], sorun=s_[:4], tum=[]))
    tt = t
    for p0, p1 in zip(yol[:-1], yol[1:]):
        su = max(1.0 * float(np.linalg.norm(p1 - p0)) / 900.0, 0.4)
        for a in adlar_tum: git(a, CUR[a] + (p1 - p0), tt, su)
        tt += su
    olay(tt - 0.3, metin); vurgu([a for a in adlar_tum if P[a]['tur'] == 'mek'], tt, tt + 1.0)
    for a in adlar_tum: YER[a] = tt
    YERINDE.extend(adlar_tum); TEZ_YER.clear(); TEZDE.clear()
    t = tt + 0.2
def makine_baglar(t0, ara=0.1):
    yerde = set(YERINDE); L_ = bag_hazir(yerde); tt = t0
    for G_ in grupla(L_):
        t1 = tt
        for i_, f in enumerate(G_): t1 = max(t1, tak(f, tt + i_ * ara, 0.45, yol_mm(f, YERINDE)))
        tt = t1 + 0.03
    return tt + (0.1 if L_ else 0.0)
KAM.append([0.0, [6.4, 2.6, 2.4], [4.8, 1.0, -0.4]])
t = 0.4
# ---- 1 KAİDE
adim('Kaide ve ayaklar', 'Kaide: 304 kare boru 60 × 60 × 3 ön / arka ray + 40 × 60 kayıtlar, tezgâhta TIG; raylara DIN 929 kaynak somunları (ayak M12, taban M8). Ayaklar alttan vidalanır, kontra somun.',
     'kaide (2 ray + 3 kayıt + 4 tapa) · ayak × 6 + kontra')
kamera_genel(['kaide_e_ray_on', 'kaide_e_ray_arka'], yon=(0.45, 0.55, 0.75), olcek=1.0)
KAIDE = var('kaide_e_ray_on', 'kaide_e_ray_arka', 'kaide_e_kayit_sol', 'kaide_e_kayit_orta', 'kaide_e_kayit_sag') + sorted(a for a in P if a.startswith(('kaide_e_ray_on_tapa', 'kaide_e_ray_arka_tapa', 'kaide_e_ayak_somunu', 'kaide_e_somun')))
t = koy(KAIDE, AD(UST6, lift=(), yan=()), 'Kaide (kaynaklı çerçeve, tezgâhta) → yere', tezgah_kaynak=KAY('kaide_e_kayit'))
for i_, a_ in enumerate(sorted(a for a in P if _re.match(r'ayak_\d$', a))):
    tt_ = tak(a_, t + i_ * 0.12, 0.5, 60.0)
    if a_ + '_kontra' in P: tak(a_ + '_kontra', t + i_ * 0.12, 0.5, 60.0)        # kontra somun ayağın milinde, ayakla birlikte gelir
t = tt_ + 0.4; olay(t - 0.4, 'Ayarlı ayak M12 × 6 (kontra somunu milinde) → ray kaynak somunlarına'); t += 0.2
# ---- 2 ALT MONTAJ
adim('Taban ve ön kasa (kaynaklı alt montaj)', 'Taban 3 mm + ön kasa (sol / orta / sağ dikme, 788 kayıtları, tapalar) + panel kulakları tezgâhta TIG; tabana FHP saplamalar preslenir. Kaidenin üstüne iner: 7 × M8 bombe başlı vida yukarıdan ray kaynak somunlarına.',
     'taban · dikme × 3 · kayıt × 2 · kulak × 18 · vida M8 × 7')
kamera_genel(['taban_sac_3', 'onyuz_dikme_sol', 'onyuz_dikme_sag'], yon=(0.45, 0.5, 0.8), olcek=0.9)
ALT = ['taban_sac_3'] + var('onyuz_dikme_sol', 'onyuz_dikme_orta', 'onyuz_dikme_sag', 'onyuz_kayit_788_sol', 'onyuz_kayit_788_sag') + sorted(a for a in P if a.startswith('onyuz_dikme_') and a.endswith('_tapa')) \
    + sorted(a for a in P if _re.match(r'govde_kulak_(sol|sag)_(on|taban)_\d+$', a)) + sorted(a for a in P if _re.match(r'emniyet_E_[A-Z]+_[A-Z]+_braket$', a))
ALT_K = KAY('onyuz_dikme_') + KAY('onyuz_kayit_788') + KAY('govde_kulak_') + sorted(a for a in P if _re.match(r'emniyet_E_.*_braket_kaynak$', a))
t = koy(ALT, AD(UST6, lift=(), yan=()), 'Taban + ön kasa + kulaklar + sensör braketleri (tezgâhta TIG) → kaidenin üstüne',
        pem=sorted(PEM_SAC.get('taban_sac_3', [])) + sorted(p for b in ALT for p in PEM_SAC.get(b, []) if b.startswith('emniyet_')), tezgah_kaynak=ALT_K)
t = sira_tak(sorted(a for a in P if a.startswith('kaide_e_vida')), t, 30.0, 0.45, 0.1); olay(t - 0.5, 'Taban ↔ kaide: M8 bombe başlı vida × 7 (ray içindeki kaynak somununa)'); t += 0.2
# ---- 3 ROBOT ÇÖPÜ + ŞARJÖR + ASANSÖR
adim('Robot çöpü, şarjör ve asansör', 'Robot çöpü (kova + poşet + oluk) yukarıdan sol öne; şarjör + asansör (hazır alt montaj: yığın tablası, vida mili, motor, kılavuzlar) yukarıdan tabanın M6 saplamalarına; yan saplamalar yan saclar gelince bağlanır.',
     'robot çöpü · şarjör + asansör')
kamera_genel(['sarjor_asansor'], yon=(0.4, 0.6, 0.7), olcek=0.9)
t = koy('robot_copu', AD(UST6, ON9, lift=(5, 20), son=SON), 'Robot çöpü (kova + poşet) → yukarıdan sol öne: kılavuzunda oturur, boşaltmak için elle çıkar')
t = koy(['sarjor_asansor'], AD(UST6, ARKA9, lift=(), son=SON), 'Şarjör + asansör → yukarıdan, tabanın M6 saplamalarına')
# ---- 4 ÜST MODÜL (tezgâhta parça parça · zincir 81–85)
adim('Üst modül (tezgâhta)', 'Tezgâhta parça parça: besleyici (plaka, dikmeler + köşebentler, raylar, mil yatağı, kasnaklar, motor yuvası + motor, kayış, sensör), besleyici iticisi (kızak plakaları + arabalar, kollar TIG, kiriş, kılavuz / orta blok, ped, kelepçe), vakum barı (miller + segman, blok, vantuzlar, hortum), köşe kaldırıcı + 4 köşe tutucu + köşe pistonu, arka itici + piston, ön parmak. Her vida kendi deliğine tek tek. Modül bütün olarak yukarıdan şarjörün üstüne iner (montaj dayamasında); üst sac gelince askı saplamaları geçer. Motor yuvası köşebendi GEÇİCİ OLARAK DAYALI — 7. adımda yan sağın preslenmiş saplamasına somunla sabitlenecek.',
     'besleyici · itici · vakum · köşe kaldırıcı × 4 · köşe pistonu · arka itici + piston · ön parmak')
kamera_genel([a for a in MEKAD if MEKAD[a] in ('besleyici', 'kose', 'piston')], yon=(-0.55, 0.5, 0.65), olcek=0.75, ofs=TEZ)
USTM = modul_kur(['besleyici', 'itici_b', 'vakum', 'kose', 'kose_tutucu', 'kose_piston', 'itici', 'piston', 'parmak'], 'üst', haric_=('besleyici_uc_sensor_tutucu', 'besleyici_uc_sensor'))
USTM_TUM = [a for a in list(TEZ_YER)]
for a_ in USTM_TUM: P[a_]['tezgah'] = True                                   # üst sac gelene kadar montaj dayamasında
olay(t + 0.1, '⚠ GEÇİCİ DAYALI: üst modül montaj dayamasında — üst sacın askı saplamaları (5. adım) ve yan sağın motor yuvası saplaması (7. adım) bağlar')
kamera_genel(['sarjor_asansor'], yon=(-0.6, 0.55, 0.6), olcek=1.3)
modul_tasi(USTM_TUM, [[TEZ, TEZ + np.array([0, 900.0, 0]), np.array([0, 900.0, 0]), np.zeros(3)], [TEZ, TEZ + np.array([0, 1200.0, 0]), np.array([0, 1200.0, 0]), np.zeros(3)],
                      [TEZ, TEZ + np.array([0, 700.0, 0]), np.array([0, 700.0, 0]), np.zeros(3)]], 'Üst modül (tezgâhta kuruldu) → yukarıdan, dayamaya')
# ---- 5 ÜST
adim('Üst sac', 'Üst sac (1,5 · yan dönüşler, Harting ağzı, U ↔ E için 3 × PEM M8, mekanizma askı saplamaları) yukarıdan ön kasanın tepesine iner (arkası montaj dayamasında): askı saplamaları üst modülün kulaklarına geçer; yanlar gelince yan saplamalar dönüşlerinden geçer.',
     'üst sac')
kamera_genel(['ust_sac'], yon=(0.5, 0.7, 0.5), olcek=0.8)
t = koy('ust_sac', AD(UST6, lift=(), yan=()), 'Üst sac → yukarıdan ön kasaya, askı saplamaları üst modüle', pem=sorted(PEM_SAC.get('ust_sac', [])))
t = somunla(r'govde_kulak_ust_[a-z]+_bag', t, 20.0); t += 0.2
t = makine_baglar(t)
# ---- 6 YAN SOL
adim('Yan sol', 'Yan sol (1,5 · pizza penceresi, preslenmiş FHP saplamalar) tezgâhta fiş paneli J3 ile birlikte soldan: saplamaları kulaklardan, üst sacın sol dönüşünden ve şarjör kulaklarından geçer; içten pul + fiberli somun.',
     'yan sol + fiş paneli J3 · pul + somun M5')
kamera_genel(['sol_sac_pizza_penceresi'], yon=(-0.8, 0.45, 0.45), olcek=0.8)
t = koy(['sol_sac_pizza_penceresi', 'fis_paneli'], AD(SOL7, lift=(0.5, 1, 2), yan=()), 'Yan sol (fiş paneli J3 tezgâhta) → soldan, saplamalar kulaklara', pem=sorted(PEM_SAC.get('sol_sac_pizza_penceresi', [])))
t = somunla(r'govde_(kulak_sol_(on|taban)_\d+_bag|bag_ust_sol)', t, 12.0); olay(t - 0.6, 'Yan sol ↔ kulaklar + üst: pul + fiberli somun M5'); t += 0.2
# ---- 6b ALT MODÜL (tezgâhta parça parça · zincir 81–85)
adim('Alt modül (tezgâhta)', 'Tezgâhta parça parça: kalıp (taban, kolonlar, yataklar, vida mili + segmanlar, motor, sensör), kalıp yuvası (milleri, plakalar), köprü (taşıyıcı, motor bloğu, motor, sensör), kapak katlama (şasi, motor plakaları, dişli kutulu motor, yataklar, tahrik mili, palet braketleri, kılavuzlar) + katlayıcı kolu. Her vida kendi deliğine tek tek. Modül sağdan girer, sol yanın saplamalarına oturur.',
     'kalıp · kalıp yuvası · köprü · kapak katlama · katlayıcı kol')
kamera_genel([a for a in MEKAD if MEKAD[a] in ('kalip', 'kapak')], yon=(0.6, 0.5, 0.65), olcek=0.8, ofs=TEZ)
ALTM = modul_kur(['kalip', 'kalip_yuva', 'kopru', 'kapak', 'kapak_katlayici'], 'alt')
ALTM_TUM = [a for a in list(TEZ_YER)]
kamera_genel(['sarjor_asansor'], yon=(0.8, 0.45, 0.45), olcek=1.3)
modul_tasi(ALTM_TUM, [[TEZ, np.array([900.0, 0, 1500.0]), np.array([900.0, 0, 0]), np.zeros(3)], [TEZ, np.array([0, 0, 1500.0]) + np.array([0, 0, 0]), np.array([0, 0, 900.0]), np.zeros(3)],
                      [TEZ, np.array([900.0, 120.0, 1500.0]), np.array([900.0, 120.0, 0]), np.array([0, 120.0, 0]), np.zeros(3)]], 'Alt modül (tezgâhta kuruldu) → sağdan, sol saplamalara')
t = makine_baglar(t)
# katlama sensörü tutucusu (sol yan sacın preslenmiş M5 saplamasına) + sensör
t = koy('katlama_sensor_tutucu', AD((60, 0, 0), (60, 0, 300), lift=(), yan=(), son=SON), 'Katlama sensörü tutucusu → sol yanın M5 saplamasına (içeriden)')
t = koy('katlama_sensor', AD((0, -60, 0), (60, 0, 0), (0, 0, 300), lift=(), yan=()), 'Katlama sensörü (Omron E3Z) → tutucusunun altına')
t = makine_baglar(t)
# ---- 7 YAN SAĞ
adim('Yan sağ', 'Yan sağ (şarjör kapısı açıklığı, preslenmiş saplamalar; bas-aç laması tezgâhta) sağdan: saplamaları kulaklardan, üst sacın dönüşünden ve mekanizma kulaklarından geçer; köşebent; içten pul + somunlar. Üst modülün motor yuvası köşebendi saplamasına somunla sabitlenir; asansör ve besleyici uç sensörlerinin tutucuları (E3Z + 4 mm dil) yan sağın saplamalarına.',
     'yan sağ + bas-aç laması · köşebent · pul + somun')
kamera_genel(['sag_sac'], yon=(0.85, 0.45, 0.3), olcek=0.8)
t = koy(['sag_sac'] + var('sarjor_yan_kapisi_basac_lamasi', 'sarjor_yan_kapisi_basac'), AD(SAG7, lift=(0.5, 1, 2), yan=()), 'Yan sağ (bas-aç laması tezgâhta) → sağdan', pem=sorted(PEM_SAC.get('sag_sac', [])))
t = somunla(r'govde_(kulak_sag_(on|taban)_\d+_bag|bag_ust_sag|bag_kapi_basac)', t, 20.0); olay(t - 0.6, 'Yan sağ: pul + fiberli somunlar'); t += 0.2
t = koy(var('govde_kosebent_sag_arka_alt'), AD(ARKA9, lift=(0.5, 1), yan=(), son=SON), 'Köşebent → yan sağ saplamasına')
t = somunla(r'govde_bag_kosebent_yan', t, 20.0)
t = makine_baglar(t); olay(t - 0.4, 'Motor yuvası köşebendi: yan sağın preslenmiş M4 saplamasına pul + fiberli somun (3. adımdaki geçici dayama bitti)')
for ad_, tut_ in (('asansor', 'asansor_sensor_tutucu'), ('besleyici_uc', 'besleyici_uc_sensor_tutucu')):
    t = koy([tut_, ad_ + '_sensor_dili'], AD((-60, 0, 0), (-60, 0, 300), (-60, 300, 0), lift=(), yan=(), son=SON), '%s (dili tezgâhta TIG) → yan sağın M5 saplamasına (içeriden)' % tr(tut_),
            tezgah_kaynak=[ad_ + '_sensor_dili_kaynak'])
    t = koy(ad_ + '_sensor', AD((0, -60, 0), (-60, 0, 0), (0, 0, 300), lift=(), yan=()), 'Omron E3Z → dilin yanına')
    t = makine_baglar(t)
# ---- 8 ARKA + PANO
adim('Arka sac ve E panosu', 'Tezgâhta arka sacın iç yüzüne: E panosu (Beckhoff + Siemens + sürücüler, hazır) ve şarjör kapısı menteşe laması + menteşe gövdeleri. Arka sac (alt + üst dönüş) arkadan sürülür, saplamaları yan dönüşlerden geçer; içten pul + somunlar.',
     'arka sac + pano + menteşe laması · pul + somun')
kamera_genel(['arka_sac'], yon=(0.4, 0.45, -0.85), olcek=0.8)
ARK = ['arka_sac', 'istasyon_kutusu'] + var('sarjor_yan_kapisi_mentese_lamasi', 'sarjor_yan_kapisi_mentese_0', 'sarjor_yan_kapisi_mentese_1')
t = koy(ARK, AD(ARKA9, lift=(0.5, 1, 2), yan=()), 'Arka sac + E panosu + menteşe laması (tezgâhta) → arkadan', pem=sorted(PEM_SAC.get('arka_sac', [])))
t = somunla(r'govde_bag_(arka_sag|taban_arka|ust_arka|kosebent_arka|kapi_lamasi)', t, 10.0)
t = somunla(r'govde_bag_arka_sol', t, 12.0)
t = makine_baglar(t)
t = sira_tak(sorted(a for a in P if a.startswith('e_arka_civata_')), t, 25.0, 0.45, 0.1); olay(t - 0.5, 'Şarjör arkası 4 nokta: dıştan M5 × 6 bombe başlı cıvata → yan sol dönüşündeki preslenmiş somuna (zincir 69)'); t += 0.2; olay(t - 0.6, 'Arka ↔ yanlar / taban / üst: pul + fiberli somunlar'); t += 0.2
# ---- 9 ELEKTRİK
adim('Kablolar ve vakum hattı', 'Güç (kırmızı) ve bilgi (mavi) kabloları, vakum hattı kanallar boyunca: pano ↔ fiş paneli ↔ motorlar / sensörler.', 'kablolar · vakum hattı')
kamera_genel(['istasyon_kutusu', 'fis_paneli'], yon=(0.6, 0.5, -0.6), olcek=1.0)
for a in ('kablo_guc', 'kablo_bilgi', 'hava_hatti'): buyu(a, t, 1.0)
olay(t, 'Güç (kırmızı) / bilgi (mavi) kabloları + vakum hattı'); t += 1.2
# ---- 10 ŞARJÖR YAN KAPISI
adim('Şarjör yan kapısı', 'Kapı (dış sac + iç tava, punta) tezgâhta menteşe kanatlarıyla; sağdan menteşe gövdelerine.', 'kapı + menteşe kanatları')
kamera_genel(['sarjor_yan_kapisi'], yon=(0.9, 0.35, 0.2), olcek=1.1)
KPI = var('sarjor_yan_kapisi', 'sarjor_yan_kapisi_ic_tava', 'sarjor_yan_kapisi_mentese_0_kanat', 'sarjor_yan_kapisi_mentese_1_kanat')
t = koy(KPI, AD(SAG7, lift=(0.5, 1), yan=()), 'Şarjör yan kapısı (tezgâhta: dış sac ↔ iç tava 6 punta) → menteşeleriyle sağdan', tezgah_punta=KAY('sarjor_yan_kapisi_punta'))
# ---- 11 KAPAKLAR
adim('Ön kapaklar', 'Bas-aç mandalları orta dikmeye, menteşe gövdeleri dikmelere (iç yandan 2 × M5), emniyet sensörleri; 4 kapak tezgâhta (dış tava + iç tava punta, köşeler TIG, karşılıklar; sol üstte robot ağzı kasası) menteşeleriyle önden.',
     'bas-aç × 6 · menteşe × 12 · emniyet × 4 · kapak × 4')
kamera_genel(['onyuz_kapak_E_ust_sol', 'onyuz_kapak_E_alt_sag'], yon=(0.35, 0.4, 0.9), olcek=0.9)
for a in sorted(a for a in P if a.startswith('onyuz_kapak_E_basac')):
    haric(a, 'onyuz_dikme_orta', 'bas-aç gövdesi orta dikmenin Ø12,2 deliğine geçme (yaylı tırnak; model sıfır boşluk)')
    koy(a, AD(ON9), 'Bas-aç → orta dikmeye', sure_bekle=0.02)
t = bitti()
for a in sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit$', a)): koy(a, AD(ON9, lift=(5,), son=SON), 'Menteşe gövdesi → dikmeye', sure_bekle=0.02)
t = bitti()
t = sira_tak(sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit_vida', a)), t, 20.0, 0.4, 0.05); olay(t - 0.4, 'Menteşe gövdeleri: iç yandan 2 × M5'); t += 0.2
for a in sorted(a for a in P if _re.match(r'emniyet_E_[A-Z]+_[A-Z]+_sensor$', a)): koy(a, AD(ON9, son=SON), 'Emniyet sensörü RSS36 → braketine', sure_bekle=0.02)
t = bitti()
t = sira_tak(sorted(a for a in P if _re.match(r'emniyet_E_[A-Z]+_[A-Z]+_\d_vida$', a)), t, 25.0, 0.45, 0.06); olay(t - 0.5, 'Sensörler: önden 2 × M4 × 20 → braketteki preslenmiş somuna'); t += 0.2
for k_ in ('alt_sol', 'alt_sag', 'ust_sol', 'ust_sag'):
    y_ = k_.split('_')[1]; u_ = k_.split('_')[0]
    KP = sorted(a for a in P if a.startswith('onyuz_kapak_E_%s' % k_) and P[a]['tur'] != 'kaynak')
    KP = ['onyuz_kapak_E_%s' % k_] + [a for a in KP if a != 'onyuz_kapak_E_%s' % k_]
    KP += sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_%s_\d_kanat$' % y_, a) and ((int(a.split('_')[5]) < 3) == (u_ == 'alt')))
    KP += [a for a in P if a.startswith('emniyet_E_%s_%s_aktuator' % (u_.upper(), y_.upper())) and P[a]['tur'] != 'kaynak']
    t = koy(KP, AD(ON9, lift=(20, 40), yan=()), 'Kapak %s (tezgâhta: menteşe kanatları + karşılıklar punta, aktüatör PEM + M4) → menteşeleriyle önden' % k_.replace('_', ' ').replace('ust', 'üst').replace('sag', 'sağ'),
            grup_kaynak=KAY('onyuz_kapak_E_%s_kose' % k_), tezgah_punta=KAY('onyuz_kapak_E_%s_punta' % k_))
# ---- 13 HAT
adim('Hat bağlantısı', 'Sahada: K (silik) solda — K ↔ E 3 × M8; U (silik) üstte — U tabanından üst sacın 3 × PEM M8 somununa.', 'K · U (silik)')
t = sira_tak(sorted(a for a in P if a.startswith('arayuz_uke_m8')), t, 30.0, 0.45, 0.1)
for a in ('cevre_B', 'cevre_U', 'cevre_K', 'cevre_diger'):
    if a in P: basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'K ve U (silik) yerinde · U ↔ E: M8 × 3'); t += 1.0
kam(t, ([6.6, 2.8, 2.6], [4.8, 1.0, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
SADE = [(r'PEM SP-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'PEM FHS-M(\d)(-\d)?', r'preslenmiş saplama M\1'), (r'PEM FHP-M(\d)(-\d+)?', r'preslenmiş saplama M\1'),
        (r'PEM S-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'\bPEM\b', 'preslenmiş'), (r'ISO 4762 ', 'cıvata '), (r'ISO 7380(-1)? ', 'bombe başlı vida '), (r'TEK ÜRÜN', 'hazır ürün')]
def sade(x):
    for a_, b_ in SADE: x = _re.sub(a_, b_, x)
    return x
for x in ADIM: x['ad'] = sade(x['ad']); x['metin'] = sade(x['metin']); x['liste'] = sade(x['liste'])
OLAY = [[o[0], sade(o[1])] for o in OLAY]
for x in ACN: x['ac'] = sade(x['ac'])
for a in P: P[a]['ac'] = sade(P[a]['ac'])
KAPGRUP = []
exec(open(os.path.join(HERE, '_son.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_e.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
