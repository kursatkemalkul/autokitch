# -*- coding: utf-8 -*-
"""B (ÇEKMECELİ SOĞUK DOLAP) MONTAJ ANİMASYONU v3 — çekmece v3 yöntemiyle (plan_B.md ile birebir) · 4 Eki 2026 · yerel
Girdi: b3_parca.pkl (hat3_v9l), acinim_B (sac_morf) · Çıktı: plan_b3.pkl → b3_cikti.py (denetim + GLB/JSON)
Her parça kendi YAKLAŞMA ÇİZGİSİNDE (yerinin üstünde / önünde / arkasında) belirir: sac → düz açınım (lazer) → bükümler (abkant, sırayla) → PEM / köpük kapağı preslenir →
tek doğru boyunca yerine iner. Yön, plan anında sürekli çarpışma denetimiyle (aday yönler sırayla) seçilir."""
import sys, os, json, pickle, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cekmece')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'b3')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf as SM
T0 = time.time()
D0 = pickle.load(open('b4_parca.pkl', 'rb')); P = D0['P']; CEKD = D0['CEKD']
URUN_YOK = True

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ (son konum = model ±0,02)
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); SAC['g_' + ad] = s
    old = P['g_' + ad]
    if s.bukum: V, F = s.dunya(s.yerel({})), s.F
    else: V, F = old['V'], old['F']                      # düz sac: modelin kendi ağı (adım 44 delikleri dahil)
    kb = np.array(D0['ENT'][ad]['kutu'])
    P['g_' + ad] = dict(V=V, F=F, m=old['m'], tur='sac', ac=old['ac'], bom=old.get('bom'), model_lo=kb[[0, 2, 4]], model_hi=kb[[1, 3, 5]])
print('sac', len(SAC))
# PEM + köpük kapağı → sac başına grup
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def icinde(a, b, pay=3.0):
    l, h = kutu(a); L, H = kutu(b); return np.all(l >= L - pay) and np.all(h <= H + pay)
def birles(adlar):
    VV, FF, n = [], [], 0
    for a in adlar: VV.append(P[a]['V']); FF.append(P[a]['F'] + n); n += len(P[a]['V'])
    return np.vstack(VV), np.vstack(FF)
PEMS = [a for a in P if a.startswith('g_ray_pem') and 'kopuk' not in a]
KAPS = [a for a in P if a.startswith('g_ray_pem') and 'kopuk' in a]
PEM_SAC = {}
for grp, ad_on, ac, m in ((PEMS, 'pem_', 'PEM SP-M5-1 (preslenir)', 'baglanti'), (KAPS, 'kapak_', 'PE köpük kapağı (PEM arkasına)', 'koyu')):
    by = {}
    for a in grp:
        la, ha = kutu(a); ca = (la + ha) / 2; cand = []
        for s_ in SAC:
            ls, hs = P[s_]['model_lo'], P[s_]['model_hi']; ex = hs - ls; ax = int(np.argmin(ex))
            if ex[ax] > 3 or abs((ls[ax] + hs[ax]) / 2 - ca[ax]) > 4: continue
            o = [k for k in range(3) if k != ax]
            if all(ls[k] - 1 < la[k] and ha[k] < hs[k] + 1 for k in o): cand.append(s_)
        assert len(cand) == 1, (a, cand)
        by.setdefault(cand[0], []).append(a)
    for s, L in by.items():
        V, F = birles(L); n = ad_on + s[2:]
        ls, hs = P[s]['model_lo'], P[s]['model_hi']; ax = int(np.argmin(hs - ls)); sx = (ls[ax] + hs[ax]) / 2; cx = (V[:, ax].min() + V[:, ax].max()) / 2
        yv = np.zeros(3); yv[ax] = float(np.sign(cx - sx))
        P[n] = dict(V=V, F=F, m=m, tur='baglanti', ac='%d × %s' % (len(L), ac), sac=s, yan=yv)
        PEM_SAC.setdefault(s, []).append(n)
        for a in L: P.pop(a)
# kovan köşe kaynakları → kovan başına · silikonlar
KAYNAK_GRUP = {}
for a in [a for a in P if 'kose_kaynagi' in a]:
    kv = a.split('_kose_kaynagi')[0]; KAYNAK_GRUP.setdefault(kv, []).append(a)
for kv, L in KAYNAK_GRUP.items():
    x0 = P[kv]['V'][:, 0].min()
    for yan, LL in (('a', [a for a in L if P[a]['V'][:, 0].min() < x0 + 2.0]), ('b', [a for a in L if P[a]['V'][:, 0].min() >= x0 + 2.0])):
        if not LL: continue
        V, F = birles(LL); P['kaynak_%s_%s' % (kv[2:], yan)] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac='TIG köşe dikişi × %d: kovan ↔ bölme sacı %s' % (len(LL), yan.upper()))
    for a in L: P.pop(a)
def grupla(yeni, adlar, m, tur, ac, **k):
    V, F = birles(adlar); P[yeni] = dict(V=V, F=F, m=m, tur=tur, ac=ac, **k)
    for a in adlar: P.pop(a)
grupla('takozlar', [a for a in P if a.startswith('g_isi_kalkani_takozu')], 'koyu', 'mek', '12 PTFE + cam elyaf takoz')
grupla('percin_sase', [a for a in P if a.startswith('g_percin_somun_sase')], 'baglanti', 'baglanti', '10 × M8 kapalı uçlu perçin somun (şase üst duvarı)', eks=(0, -1.0, 0))
grupla('percin_ust', [a for a in P if a.startswith(('g_percin_somun_ab', 'g_percin_somun_kb', 'g_percin_somun_ek'))], 'baglanti', 'baglanti', '12 × M8 kapalı uçlu perçin somun (A, K ve TOPPING bağlantısı için üst kirişlerde)', eks=(0, -1.0, 0))
grupla('sase_pul', [a for a in P if a.startswith('g_arayuz_sase') and a.endswith('_pul')], 'baglanti', 'baglanti', '10 × DIN 9021 M8 pul', eks=(0, -1.0, 0))
grupla('sase_civata', [a for a in P if a.startswith('g_arayuz_sase')], 'baglanti', 'baglanti', '10 × ISO 4762 M8 × 16 cıvata → kapalı uçlu perçin somun', eks=(0, -1.0, 0))
grupla('silikon_arka_kose', [a for a in P if a.startswith('g_arka_kose_silikonu')], 'yapistirici', 'silikon', 'arka köşe silikonları (gıda sınıfı)')
for k in range(1, 6):
    L = [a for a in P if a.startswith('g_bolme_%d_gider_silikonu' % k)]
    if L: grupla('silikon_gider_%d' % k, L, 'yapistirici', 'silikon', 'gider geçişi silikonu (bölme %d)' % k)
grupla('silikon_ek_yeri', [a for a in P if a.startswith('g_ek_yeri_silikon')], 'yapistirici', 'silikon', 'dış kabuk ek yeri silikonu (taban / arka / tavan)')
grupla('cerceve_dolgu', ['g_on_cerceve_ek_lamasi'] if False else [], 'kapak', 'sac', '') if False else None
for a in list(P):
    if a.startswith('CEK_') and URUN_YOK: pass
# ------------------------------------------------------------------ 2. üretilen kaynak dikişleri (modelde yok — animasyonda; 0,6 mm ≤ yol toleransı)
def kutu_m(lo, hi): return G.kutu(lo, hi)
def kaynak_ekle(ad, kutular, ac):
    V, F = G.mesh(G.birlesim([G.kutu(l, h) for l, h in kutular])); P[ad] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac=ac)
W_ = 0.6
for a in [a for a in P if a.startswith('sase_capraz_')]:
    lo, hi = kutu(a)
    for zf, s in ((lo[2], 1), (hi[2], -1)):
        z0, z1 = (zf, zf + W_) if s > 0 else (zf - W_, zf)
        kaynak_ekle('kaynak_%s_%s' % (a, 'arka' if s > 0 else 'on'),
                    [((lo[0] - W_, lo[1] + 1, z0), (lo[0], hi[1] - 1, z1)), ((hi[0], lo[1] + 1, z0), (hi[0] + W_, hi[1] - 1, z1)),
                     ((lo[0], lo[1] - W_, z0), (hi[0], lo[1], z1))], 'TIG çevre dikişi: çapraz profil ↔ boy profili')
def halka(ad, a, y, ac):
    lo, hi = kutu(a)
    kaynak_ekle(ad, [((lo[0] - W_, y - W_, lo[2]), (lo[0], y, hi[2])), ((hi[0], y - W_, lo[2]), (hi[0] + W_, y, hi[2])),
                     ((lo[0], y - W_, lo[2] - W_), (hi[0], y, lo[2])), ((lo[0], y - W_, hi[2]), (hi[0], y, hi[2] + W_))], ac)
for a in [a for a in P if a.startswith('moduler_dikme_')]:
    halka('kaynak_' + a, a, kutu(a)[1][1], 'TIG çevre dikişi: ara dikme ↔ üst kiriş')
for a in [a for a in P if a.startswith('tasiyici_dikme_') and kutu(a)[1][1] < 750]:
    halka('kaynak_' + a, a, kutu(a)[1][1], 'TIG çevre dikişi: taşıyıcı dikme ↔ üst çerçeve')
for ck, d in CEKD.items():
    R0 = np.asarray(d['R0'])
    m = G.birlesim([G.kaynak_dikisi(R0 + (2.0, 71.7, 699.7), R0 + (10.0, 71.7, 699.7), 0.6), G.kaynak_dikisi(R0 + (0.7, 74.0, 699.7), R0 + (0.7, 82.0, 699.7), 0.6)])
    V, F = G.mesh(m); P[ck + '_kaynak'] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac='TIG köşe (içeriden): avara ön flanşı ↔ ön çerçeve arkası (2 × 8 mm)')
print('öğe', len(P), '%.0f s' % (time.time() - T0))

# ------------------------------------------------------------------ 3. zaman çizelgesi altyapısı (cek_montaj_v3 ile aynı model)
HAR = {a: [] for a in P}; GOR = {}; MF = {}; FRAMES = {}; VU = {a: [] for a in P}; ISTISNA = set()
ADIM, OLAY, KAM, ACN = [], [], [], []
CUR = {}
YER = {}            # yerine oturma zamanı
def mm2(v): return [round(float(x) / 1000.0, 6) for x in v]
def basla(a, ofs, tg): CUR[a] = np.asarray(ofs, float); GOR[a] = round(tg, 3)
def git(a, ofs, t0, sure):
    ofs = np.asarray(ofs, float); d = CUR[a] - ofs
    if np.linalg.norm(d) > 1e-9: HAR[a].append([round(t0, 3), round(t0 + sure, 3)] + mm2(d))
    CUR[a] = ofs
def vurgu(adlar, t0, t1):
    for a in adlar: VU[a].append([round(t0, 3), round(t1, 3)])
def olay(tt, m): OLAY.append([round(tt, 3), m])
def kam(tt, k): KAM.append([round(tt, 3), k[0], k[1]])
t = 0.0
def adim(ad, metin, liste):
    ADIM.append(dict(no=len(ADIM) + 1, ad=ad, t0=round(t, 3), metin=metin, liste=liste))
def buyu(a, t0, sure=0.8):
    basla(a, np.zeros(3), t0); ISTISNA.add(a); MF[a] = dict(buyu=[round(t0, 3), round(t0 + sure, 3)]); VU[a].append([round(t0, 3), round(t0 + sure + 0.8, 3)]); YER[a] = t0 + sure; YERINDE.append(a)
    return t0 + sure

# ------------------------------------------------------------------ 4. plan anı yol denetimi (doğru boyunca yaklaşma, yerinde olanlara karşı)
VEK = {}
def tri(a):
    if a not in VEK: VEK[a] = Y._vekil(P[a]['V'] / 1000.0, np.asarray(P[a]['F']))
    return VEK[a]
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
def serbest(adlar, ofs, yerinde, haric=(), ofs2=None):
    """adlar (birlikte) ofs (mm) konumundan ofs2'ye (yoksa son konuma) doğru hareketinde yerinde olan parçaları deliyor mu → [(a, b)]"""
    ofs = np.asarray(ofs, float); ofs2 = np.zeros(3) if ofs2 is None else np.asarray(ofs2, float)
    v = (ofs2 - ofs) / 1000.0; sorun = []
    if np.linalg.norm(v) < 1e-9: return sorun
    for a in adlar:
        A0 = tri(a) + ofs / 1000.0
        l = (np.minimum(LO[a] + ofs2, LO[a] + ofs)) / 1000.0; h = (np.maximum(HI[a] + ofs2, HI[a] + ofs)) / 1000.0
        for b in yerinde:
            if b in adlar or b in haric or (a, b) in HARIC_PLAN or (b, a) in HARIC_PLAN: continue
            if np.any(LO[b] / 1000.0 > h + 1e-4) or np.any(HI[b] / 1000.0 < l - 1e-4): continue
            B = tri(b)
            amn = np.minimum(A0.min(1), (A0 + v).min(1)); amx = np.maximum(A0.max(1), (A0 + v).max(1))
            sa = np.all(amn <= HI[b] / 1000.0 + 1e-4, 1) & np.all(amx >= LO[b] / 1000.0 - 1e-4, 1)
            if not sa.any(): continue
            smn = amn[sa].min(0); smx = amx[sa].max(0)
            sb = np.all(B.min(1) <= smx + 1e-4, 1) & np.all(B.max(1) >= smn - 1e-4, 1)
            if not sb.any(): continue
            lam = Y.ccd(np.ascontiguousarray(A0[sa]), np.ascontiguousarray(B[sb]), v.astype(np.float64), Y.SINIR)
            m = lam < 1.5
            if not m.any(): continue
            pts = lam[m][:, None] * v[None, :]
            der = np.minimum(np.linalg.norm(pts - v[None, :], axis=1), np.linalg.norm(pts, axis=1))
            if der.max() > Y.OTURMA: sorun.append((a, b))
    return sorun
HARIC_PLAN = set(); HARIC_NEDEN = {}
YERINDE = []        # sırayla yerine oturanlar
PLAN_SORUN = []

YON = {'ust': np.array([0, 1.0, 0]), 'on': np.array([0, 0, 1.0]), 'arka': np.array([0, 0, -1.0]), 'sag': np.array([1.0, 0, 0]), 'sol': np.array([-1.0, 0, 0]),
       'alt': np.array([0, -1.0, 0])}
def mesafe(adlar, yon, ek=0.0, kare_lo=None, kare_hi=None):
    lo = np.min([LO[a] for a in adlar], 0); hi = np.max([HI[a] for a in adlar], 0)
    if kare_lo is not None: lo = np.minimum(lo, kare_lo); hi = np.maximum(hi, kare_hi)
    if yon == 'ust': return max(60.0, 960.0 - lo[1]) + ek
    if yon == 'on': return max(60.0, 260.0 - lo[2]) + ek
    if yon == 'arka': return max(60.0, hi[2] + 1000.0) + ek
    if yon == 'sag': return max(60.0, 4560.0 - lo[0]) + ek
    if yon == 'sol': return max(60.0, hi[0] - 580.0) + ek
    if yon == 'alt': return 150.0 + ek
def yon_sec(adlar, adaylar, kare_lo=None, kare_hi=None, ek=0.0):
    """dönüş: nokta listesi (son konuma göre ötelemeler, ilk = başlangıç) — tek doğru ya da iki bacak (ör. sütundan yana)"""
    ilk = None; TUMS = []
    for y in adaylar:
        if isinstance(y, tuple):
            yy, ara = y; ara = np.asarray(ara, float)
            L = mesafe(adlar, yy, ek, kare_lo, kare_hi) + max(0.0, float(ara @ YON[yy]))
            yol = [ara + YON[yy] * L, ara, np.zeros(3)]
        else:
            L = mesafe(adlar, y, ek, kare_lo, kare_hi); yol = [YON[y] * L, np.zeros(3)]
        s = []
        for p0, p1 in zip(yol[:-1], yol[1:]): s += serbest(adlar, p0, YERINDE, ofs2=p1)
        if ilk is None: ilk = (y, yol, s)
        TUMS.append((str(y), s[:3]))
        if not s: return y, yol
    PLAN_SORUN.append(dict(parca=adlar[:3], yon=str(ilk[0]), sorun=ilk[2][:4], tum=TUMS))
    return ilk[0], ilk[1]

# ------------------------------------------------------------------ 5. zamanlayıcı (aynı adımdaki bağımsız parçalar alan çakışmazsa paralel)
AKTIF = []          # (lo, hi, t0, t1)
def alan_bos(lo, hi, t0, t1):
    tt = t0
    while True:
        eng = [x for x in AKTIF if x[2] < tt + (t1 - t0) - 1e-6 and x[3] > tt + 1e-6 and np.all(x[0] <= hi + 5) and np.all(x[1] >= lo - 5)]
        if not eng: return tt
        tt = max(x[3] for x in eng)
HIZ = 2200.0        # mm/s taşıma
def sac_kareleri(a):
    s = SAC[a]; V = P[a]['V']; nb = len(s.bukum)
    if not nb: return None
    sira = sorted(s.bukum, key=lambda b: b['no'])
    kar = []; f = {b['no']: 0.0 for b in sira}
    kar.append(s.dunya(s.yerel(dict(f))) - V)
    for b in sira:
        for x in np.linspace(0, 1, 7)[1:]:
            f[b['no']] = x; kar.append(s.dunya(s.yerel(dict(f))) - V)
    return kar
def yerlestir(adlar, adaylar, t_min, metin, pem=(), grup_kaynak=(), sure_bekle=0.15, ek=0.0, kamera_yakin=False, eks_yol=None, tezgah_kaynak=()):
    """adlar: birlikte hareket eden parçalar (ilki ana) · adaylar: yön listesi · pem: (PEM / kapak öğeleri — üretimde preslenir, sonra birlikte taşınır)
    dönüş: oturma zamanı"""
    global t
    a0 = adlar[0]
    kar = sac_kareleri(a0) if a0 in SAC else None
    klo = khi = None
    if kar:
        X = np.vstack([P[a0]['V'] + k for k in kar]); klo, khi = X.min(0), X.max(0)
    y_, yol = yon_sec(list(adlar) + list(pem), adaylar, klo, khi, ek); ofs = yol[0]
    L = float(sum(np.linalg.norm(b - a) for a, b in zip(yol[:-1], yol[1:])))
    tum = list(adlar) + list(pem)
    lo = np.min([LO[a] for a in tum], 0); hi = np.max([HI[a] for a in tum], 0)
    if klo is not None: lo = np.minimum(lo, klo); hi = np.maximum(hi, khi)
    rlo = np.min([lo + p for p in yol], 0); rhi = np.max([hi + p for p in yol], 0)
    sure_uret = 0.8 if tezgah_kaynak else 0.0
    if a0 in SAC:
        nb = len(SAC[a0].bukum); sure_uret = 0.45 + nb * 0.5 + (0.55 if pem else 0.0)
    sure_tasi = max(0.45 * (len(yol) - 1), L / HIZ)
    toplam = sure_uret + sure_bekle + sure_tasi
    ts = alan_bos(rlo, rhi, t_min, t_min + toplam)
    for a in tum: basla(a, ofs, ts)
    tt = ts
    if a0 in SAC:
        s = SAC[a0]; nb = len(s.bukum)
        olay(tt, '%s · LAZER: düz açınım %s × %s mm (kontur + delikler)' % (P[a0]['ac'], ('%.0f' % s.levha['boy']), ('%.0f' % s.levha['en'])))
        ACN.append(dict(ad=a0, ac=P[a0]['ac'], t=s.t, t0=round(tt, 3), t1=round(tt + sure_uret, 3), levha=[s.levha['boy'], s.levha['en']],
                        bukum=[dict(no=b['no'], aci=b['aci'], ack=b['ad'].replace('_', ' ')) for b in sorted(s.bukum, key=lambda b: b['no'])]))
        tt += 0.45
        if kar:
            FRAMES[a0] = kar; seg = []
            for i, b in enumerate(sorted(s.bukum, key=lambda b: b['no'])):
                seg.append([round(tt, 3), round(tt + 0.42, 3), 6 * i, 6 * i + 6])
                olay(tt, '%s · ABKANT büküm %d / %d: %s · %d° · iç R %.2f' % (P[a0]['ac'], b['no'], nb, b['ad'].replace('_', ' '), round(b['aci']), b['R']))
                tt += 0.5
            MF[a0] = dict(seg=seg)
        if pem:
            for p in pem:
                e_ = np.asarray(P[p]['yan'], float) * 30.0
                basla(p, ofs + e_, tt); git(p, ofs, tt, 0.45); vurgu([p], tt + 0.3, tt + 1.0)
            olay(tt, '%s · PEM presleme: %s' % (P[a0]['ac'], ' + '.join((('%d × ' % n_) if n_ > 1 else '') + k_ for k_, n_ in __import__('collections').Counter(P[p]['ac'] for p in pem).items())))
            tt += 0.55
    if tezgah_kaynak:
        for k_ in tezgah_kaynak: MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, 'Tezgâhta: %s' % P[tezgah_kaynak[0]]['ac']); tt += 0.8
    tt += sure_bekle
    for p0, p1 in zip(yol[:-1], yol[1:]):
        su = sure_tasi * float(np.linalg.norm(p1 - p0)) / max(L, 1e-6); su = max(su, 0.3)
        for a in tum: git(a, CUR[a] + (p1 - p0), tt, su)
        tt += su
    sure_tasi = 0.0
    if metin: olay(tt - sure_tasi * 0.5, metin)
    vurgu(list(adlar), tt, tt + 1.1)
    for k_ in grup_kaynak:
        buyu(k_, tt, 0.6); vurgu([k_], tt, tt + 1.4)
    for a in tum: YER[a] = tt
    YERINDE.extend(tum); YERINDE.extend(grup_kaynak)
    AKTIF.append((rlo, rhi, ts, tt + 0.05))
    if kamera_yakin:
        c = (np.min([LO[a] for a in adlar], 0) + np.max([HI[a] for a in adlar], 0)) / 2000.0
        d = np.array([0.5, 0.45, 0.75]); d /= np.linalg.norm(d)
        kam(ts, ((c + d * 0.9).round(3).tolist(), c.round(3).tolist()))
    return tt
def tak(a, t0, sure=0.55, yol=30.0, metin=None):
    """bağlantı elemanı kendi ekseninde (P[a]['eks'] = giriş yönü)"""
    e_ = np.asarray(P[a]['eks'], float); basla(a, -e_ * yol, t0); git(a, np.zeros(3), t0, sure); vurgu([a], t0 + sure * 0.5, t0 + sure + 0.8)
    YER[a] = t0 + sure; YERINDE.append(a)
    if metin: olay(t0, metin)
    return t0 + sure
def bitti():
    return max([YER[a] for a in YER] + [t])
def kamera_genel(adlar, yon=(0.45, 0.5, 0.75), olcek=1.25, tt=None):
    lo = np.min([LO[a] for a in adlar], 0) / 1000.0; hi = np.max([HI[a] for a in adlar], 0) / 1000.0
    c = (lo + hi) / 2; r = float(np.linalg.norm(hi - lo)) * olcek + 0.4
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    kam(t if tt is None else tt, ((c + d * r).round(3).tolist(), c.round(3).tolist()))
def yakin(nokta_mm, uz=0.35, yon=(0.55, 0.42, 0.72), tt=None):
    c = np.asarray(nokta_mm, float) / 1000.0; d = np.asarray(yon, float); d /= np.linalg.norm(d)
    kam(t if tt is None else tt, ((c + d * uz).round(3).tolist(), c.round(3).tolist()))
def merkez(a): return (LO[a] + HI[a]) / 2

# ================================================================== PLAN v4 (Kemal geri bildirimi 4 Eki: sade metin, kalıcı kırmızı kaynak / punta, yeşil yapıştırıcı,
# PU levhalar takılabilir parçalar (zincir 46), gerçek bağlantı elemanları (zincir 47 / 49) — her biri kendi deliğine, kendi ekseninde)
import re as _re
TR = {'dis_taban': 'Dış taban sacı', 'dis_tavan': 'Dış tavan sacı', 'dis_arka': 'Dış arka sac', 'dis_sol_yan': 'Dış sol yan sac', 'dis_sag_yan': 'Dış sağ yan sac',
      'ic_taban': 'İç taban sacı', 'ic_tavan': 'İç tavan sacı', 'ic_arka': 'İç arka sac', 'ic_sol_duvar': 'İç sol duvar sacı', 'teknik_sol_duvar': 'Teknik bölme kapama sacı',
      'tk_ara_arka_sac': 'Teknik bölme ara sacı', 'isi_kalkani_u': 'Isı kalkanı (U sac)', 'isi_kalkani_isinim': 'Isı kalkanı ışınım sacı (0,8)',
      'on_cerceve': 'Ön çerçeve (AISI 430)', 'pu_taban': 'Taban yalıtım levhası (PU)', 'pu_tavan_yuksek': 'Tavan yalıtım levhası (PU, yüksek kısım)',
      'pu_tavan_topping': 'Tavan yalıtım levhası (PU, TOPPING altı)', 'pu_tavan_firin': 'Tavan yalıtım levhası (PU, fırın altı)', 'pu_b5_ust': 'Bölme 5 üstü yalıtım levhası (PU)',
      'pu_isi_kalkani_kose_sol': 'Isı kalkanı sol köşe yalıtım şeridi (PU)', 'pu_isi_kalkani_kose_sag': 'Isı kalkanı sağ köşe yalıtım şeridi (PU)',
      'pu_arka_yuksek_arka': 'Arka yalıtım levhası, arka katman (PU, yüksek kısım)', 'pu_arka_yuksek_on': 'Arka yalıtım levhası, ön katman (PU, yüksek kısım)',
      'pu_arka_alcak_arka': 'Arka yalıtım levhası, arka katman (PU, alçak kısım)', 'pu_arka_alcak_on': 'Arka yalıtım levhası, ön katman (PU, alçak kısım)',
      'pu_sol_arka_serit': 'Sol duvar arka yalıtım şeridi (PU)', 'pu_sol_kose_alt': 'Sol alt köşe dolgu şeridi (PU)', 'pu_sol_kose_ust': 'Sol üst köşe dolgu şeridi (PU)',
      'pu_sol': 'Sol duvar yalıtım levhası (PU)', 'tk_ara_pu': 'Teknik bölme ara yalıtım levhası (PU)', 'tk_depo_arka_pu': 'Soğuk depo arka yalıtım levhası (PU)',
      'tk_depo_sag_pu': 'Soğuk depo sağ yalıtım levhası (PU)', 'tk_depo_tavan_pu': 'Soğuk depo tavan yalıtım levhası (PU)', 'tk_depo_kose_dolgu': 'Soğuk depo sağ üst köşe dolgu şeridi (PU)',
      'kosebent_sol_alt': 'Sol alt köşebent', 'kosebent_sol_ust': 'Sol üst köşebent', 'kosebent_sag_alt': 'Sağ alt köşebent', 'kosebent_sag_ust': 'Sağ üst köşebent',
      'dis_taban_ek_lamasi': 'Dış taban ek laması', 'dis_tavan_ek_lamasi': 'Dış tavan ek laması', 'dis_arka_ek_lamasi': 'Dış arka ek laması', 'on_cerceve_ek_lamasi': 'Ön çerçeve ek laması'}


def ad_tr(a):
    s = P[a]['ac'] if a in P else a
    m = _re.match(r'bolme_(\d)_(sac_a|sac_b|pu|kovan_\d)', s)
    if m:
        k, x = m.groups()
        return 'Bölme %s %s' % (k, {'sac_a': 'sol sacı (A)', 'sac_b': 'sağ sacı (B)', 'pu': 'yalıtım levhası (PU)'}.get(x, 'kablo geçiş kovanı'))
    for k in sorted(TR, key=len, reverse=True):
        if s.startswith(k):
            n = s[len(k):].strip('_')
            return TR[k] + ((' ' + n) if n and n.isdigit() else '')
    return s.replace('_', ' ')


for a in P:
    if a.startswith('g_') and P[a]['tur'] in ('sac', 'pu', 'mek'): P[a]['ac'] = ad_tr(a)

# ---------------------------------------------------------------- yapıştırıcı katmanları (PU levha ↔ dayandığı sac; ince yeşil, levhadan sonra belirir, kalır)
def yapistirici(pu, eks, taraf, ad=None):
    lo, hi = P[pu]['V'].min(0).copy(), P[pu]['V'].max(0).copy()
    if taraf < 0: hi[eks] = lo[eks] + 0.3
    else: lo[eks] = hi[eks] - 0.3
    k = 2.0
    for i in range(3):
        if i != eks: lo[i] += k; hi[i] -= k
    V, F = G.mesh(G.kutu(lo, hi)); n = ad or 'yap_' + pu[2:]
    P[n] = dict(V=V, F=F, m='yapistirici', tur='silikon', ac='yapıştırıcı (PU ↔ sac, tek bileşenli PU yapıştırıcı)')
    LO[n] = V.min(0); HI[n] = V.max(0); HAR[n] = []; VU[n] = []
    return n


def yapistir(pu, eks, taraf, tt):
    n = yapistirici(pu, eks, taraf); r = buyu(n, tt, 0.5)
    while n in YERINDE: YERINDE.remove(n)                          # yapıştırıcı filmi yol denetiminde engel değil (levhanın yüzünde)
    return r


# ---------------------------------------------------------------- puntalar (üreteçten: h3_b_sac_v1 punta noktaları) — kırmızı nokta, iki parça yerinde olunca
PUNTA = json.load(open('puntalar_B.json', encoding='utf-8'))
PUNTA_GRUP = []
for k in PUNTA:
    a, b = ['g_' + x for x in k['parcalar']]
    if a not in P or b not in P or not k['noktalar']: continue
    cs = [G.kutu(np.array(p) - 2.0, np.array(p) + 2.0) for p in k['noktalar']]
    V, F = G.mesh(G.birlesim(cs)); n = 'punta_%s__%s' % (a[2:], b[2:])
    while n in P: n += '_'
    P[n] = dict(V=V, F=F, m='punta', tur='kaynak', ac='punta × %d: %s ↔ %s' % (k['adet'], ad_tr(a), ad_tr(b)))
    LO[n] = V.min(0); HI[n] = V.max(0); HAR[n] = []; VU[n] = []
    PUNTA_GRUP.append((n, a, b))


def puntala(tt):
    """iki parçası da yerinde olan puntalar belirir (kırmızı, kalıcı) · dönüş: belirenler"""
    out = []
    for n, a, b in PUNTA_GRUP:
        if n in GOR: continue
        if a in YER and b in YER and YER[a] <= tt + 1e-6 and YER[b] <= tt + 1e-6:
            buyu(n, tt, 0.35); out.append(n)
    if out: olay(tt, 'Punta (direnç nokta kaynağı, kırmızı): ' + ' · '.join(P[n]['ac'] for n in out[:3]) + (' …' if len(out) > 3 else ''))
    return out


# ---------------------------------------------------------------- bağlantı elemanları (b_*): sacta preslenenler sacla gelir, gerisi karşı parça yerine oturunca kendi ekseninde
BAG = [a for a in P if a.startswith('b_') and P[a].get('etur')]
GRUP = {}
SUF = ('_kaynak_somunu', '_percin_somun', '_saplama', '_civata', '_somun', '_pul_alt', '_pul', '_burc', '_percin')
for a in BAG:
    k = a
    for s_ in SUF:
        if a.endswith(s_): k = a[:-len(s_)]; break
    GRUP.setdefault(k, []).append(a)
BAGSET = set(BAG)
import re as _re
for a_ in BAG:                                              # sayfa metni: ham ad yerine standart ad (BOM satırından)
    if '_' in P[a_]['ac'] and P[a_].get('bom'):
        b_ = _re.sub(r'\s*\(.*$', '', P[a_]['bom'][0]); b_ = b_.replace(' kendinden perçinli saplama', ' saplama').replace(' kendinden perçinli', '')
        P[a_]['ac'] = b_.strip()
YAPI = [a for a in P if a not in BAGSET and not a.startswith(('kaynak_', 'punta_', 'yap_')) and P[a]['tur'] not in ('kablo', 'pu', 'silikon', 'kaynak')]
BOX = np.array([np.r_[LO[a], HI[a]] for a in YAPI])
STUD = {}          # ev sahibi parça → [saplama / kaynak somunu / perçin somun / burç] (üretimde preslenir / kaynaklanır, ev sahibiyle gelir)


def ev_sahibi(nokta, sac_once=False):
    q = np.asarray(nokta)
    m = np.all(BOX[:, :3] <= q + 0.3, 1) & np.all(BOX[:, 3:] >= q - 0.3, 1)
    c = [YAPI[i] for i in np.where(m)[0]]
    if sac_once and any(P[a]['tur'] == 'sac' for a in c): c = [a for a in c if P[a]['tur'] == 'sac']
    if not c: return None
    return min(c, key=lambda a: np.prod(HI[a] - LO[a] + 0.5))


for k, L in GRUP.items():
    ev = None
    for a in L:
        et = P[a]['etur']; n = np.asarray(P[a]['n'], float)
        if et == 'saplama':
            V = P[a]['V']; s = V @ n; bas = V[s < s.min() + 0.3].mean(0)
            ev = ev_sahibi(bas, sac_once=True) or ev
            if ev: STUD.setdefault(ev, []).append(a); P[a]['yan'] = -n; P[a]['ev'] = ev
        elif et in ('kaynak_somunu', 'percin_somun'):
            if et == 'kaynak_somunu':
                q = (LO[a] + HI[a]) / 2; c = [x for x in YAPI if x.startswith(('moduler_', 'tasiyici_')) and np.all(LO[x] <= q + 0.3) and np.all(HI[x] >= q - 0.3)]
                e2 = min(c, key=lambda x: np.prod(HI[x] - LO[x] + 0.5)) if c else None
            else: e2 = ev_sahibi((LO[a] + HI[a]) / 2 + n * 4.0)
            if e2: STUD.setdefault(e2, []).append(a); P[a]['yan'] = -n if et == 'percin_somun' else np.array([0, 1.0, 0]); P[a]['ev'] = e2
    for a in L:
        if a.endswith('_burc'):
            st = [x for x in L if x.endswith('_saplama')]
            if st and P[st[0]].get('ev'): STUD.setdefault(P[st[0]]['ev'], []).append(a); P[a]['yan'] = np.asarray(P[a]['n'], float); P[a]['ev'] = P[st[0]]['ev']
TEZGAH_BAG = set()


def grup_kalan(L):
    return [a for a in L if 'ev' not in P[a] and a not in TEZGAH_BAG]


GDOKUN = {}
BSAC = [a for a in BAG if P[a]['etur'] == 'sac']
YAPI2 = YAPI + BSAC; BOX2 = np.array([np.r_[LO[a], HI[a]] for a in YAPI2])
for k, L in GRUP.items():
    R = grup_kalan(L)
    if not R: continue
    lo = np.min([LO[a] for a in R], 0) - 0.4; hi = np.max([HI[a] for a in R], 0) + 0.4
    m = np.all(BOX2[:, :3] <= hi, 1) & np.all(BOX2[:, 3:] >= lo, 1)
    GDOKUN[k] = [YAPI2[i] for i in np.where(m)[0] if YAPI2[i] not in L and not (k.startswith('b_kanal_') and YAPI2[i].startswith(('CEK_', 'evaporator', 'sogutma_grubu', 'b_kanal_988')))]   # iç kanal perçinleri kablolar / çekmeceler gelmeden atılır
    if k.startswith('b_f1_'): GDOKUN[k].append('g_teknik_sol_duvar')        # taban ↔ arka köşe perçinleri bölmeler kurulduktan sonra (bölme levhaları yandan kayarken engel olmasın)
YAZILAN = {'saplama': 'PEM saplama', 'civata': 'cıvata', 'somun': 'somun', 'pul': 'pul', 'percin': 'kör perçin', 'kaynak_somunu': 'kaynak somunu', 'percin_somun': 'perçin somun'}


def bag_sira(L):
    """sac (konsol / kelepçe) önce · baş tarafı (giriş yönü) pul → cıvata / perçin → karşı uç pul → somun"""
    cv = [a for a in L if P[a]['etur'] in ('civata', 'percin')]
    c_cv = (LO[cv[0]] + HI[cv[0]]) / 2 if cv else None
    out = []
    for a in L:
        n = np.asarray(P[a]['n'], float); c = (LO[a] + HI[a]) / 2; et = P[a]['etur']
        if et in ('civata', 'percin'): eks, s = n, 1
        elif et == 'sac': eks, s = None, 0
        elif c_cv is not None and (c - c_cv) @ n < 0: eks, s = n, 0.5
        else: eks, s = -n, 2 + (c @ n) * 1e-3
        out.append((s, a, eks))
    return sorted(out, key=lambda x: x[0])


def baglantilari_tamamla(tt=None, metin=None):
    """yerinde olan parçalara bağlanan bütün bağlantı grupları aynı anda takılır (grup içi sırayla) · dönüş: bitiş zamanı"""
    global t
    t0 = bitti() if tt is None else tt; son = t0; n_g = 0; say = {}
    for k, L in GRUP.items():
        R = grup_kalan(L)
        if not R or any(a in GOR for a in R): continue
        dk = GDOKUN.get(k, [])
        if not dk or any(d not in YER for d in dk): continue
        if any(P[a].get('ev') and P[a]['ev'] not in YER for a in L): continue
        tt_ = t0
        for s, a, eks in bag_sira(R):
            if eks is None:
                n_ = np.asarray(P[a]['n'], float) if P[a].get('n') else np.zeros(3)
                ad_ = ['on', 'ust', ('on', tuple(-12.0 * n_)), ('ust', tuple(-12.0 * n_)), ('on', (12.0, 0, 0)), ('on', (-12.0, 0, 0)), ('ust', (12.0, 0, 0)), 'sag', 'sol', 'alt', 'arka']
                tt_ = yerlestir([a], ad_, tt_, None, sure_bekle=0.0); continue
            P[a]['eks'] = tuple(eks); tt_ = tak(a, tt_, 0.4, 22.0 if P[a]['etur'] == 'civata' else (3.0 if a.startswith('b_kanal_') else 7.0)) + 0.05
            say[P[a]['etur']] = say.get(P[a]['etur'], 0) + 1
        son = max(son, tt_); n_g += 1
    if n_g:
        olay(t0, metin or ('Bağlantı (mavi): ' + ' · '.join('%d %s' % (v, YAZILAN.get(k_, k_)) for k_, v in sorted(say.items())) + ' — her biri kendi deliğine, kendi ekseninde'))
    return son


_yer0 = yerlestir
def yerlestir(adlar, adaylar, t_min, metin, pem=(), **k):
    """v4: ev sahibi parçalardaki saplama / kaynak somunu / perçin somun üretimde preslenir ve parçayla gelir"""
    ek = [s for a in adlar for s in STUD.get(a, []) if s not in GOR]
    return _yer0(adlar, adaylar, t_min, metin, pem=list(pem) + ek, **k)


def adim_sonu(ek_metin=None):
    global t
    t = bitti(); puntala(t); t2 = baglantilari_tamamla(t, ek_metin); t = max(t, t2) + 0.2


for k in range(1, 6):
    for kv in [x for x in P if x.startswith('g_bolme_%d_kovan' % k)]:
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, kv)); HARIC_NEDEN[('g_bolme_%d_pu' % k, kv)] = 'kovan PU levhadaki yuvasından sıfır boşlukla geçer (levha yuvası kovan ölçüsünde kesilir)'
    for yan in ('a', 'b'):
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))); HARIC_NEDEN[('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))] = 'köpük kapağı PU levhadaki cebine oturur (son 1 mm, temas)'
for k_, L_ in (('kapak_ic_arka_1', ('g_pu_arka_yuksek_on',)), ('kapak_ic_arka_2', ('g_pu_arka_yuksek_on', 'g_pu_arka_alcak_on'))):
    for x in L_: HARIC_PLAN.add((k_, x)); HARIC_NEDEN[(k_, x)] = 'köpük kapağı PU levhadaki cebine oturur (son 1 mm, temas)'
for a in ('g_dis_taban_1', 'g_dis_taban_2'): HARIC_PLAN.add(('percin_sase', a)); HARIC_NEDEN[('percin_sase', a)] = 'perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15)'
for a_, L_ in (('percin_sase', ('sase_boy_arka', 'sase_boy_on')), ('percin_ust', ('moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'))):
    for x in L_: HARIC_PLAN.add((a_, x)); HARIC_NEDEN[(a_, x)] = 'perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)'
for a in [x for x in ('g_dis_tavan_1', 'g_dis_tavan_2', 'tasiyici_ust', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574', 'gfrp_ust_arka', 'gfrp_ust_on') if x in P]:
    HARIC_PLAN.add(('percin_ust', a)); HARIC_NEDEN[('percin_ust', a)] = 'perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15)'

KAM.append([0.0, [6.2, 3.2, 5.6], [2.57, 0.45, -0.4]])
t = 0.4
SASE = ['sase_boy_arka', 'sase_boy_on'] + sorted(a for a in P if a.startswith('sase_capraz_'))
YAN = (36.0, 0.0, 0.0)          # bölme kalınlığı 35 + 1: kovan uçlarını aşacak kadar yana, sonra −x
# ---- 1 ŞASE
adim('Şase', 'Alt şase: 2 boy profili + 7 çapraz profil (AISI 304 kutu 60 × 60, kesim boyunda) yukarıdan iner; her çapraz profil iki ucundan boy profillerine TIG çevre dikişiyle kaynaklanır (kırmızı dikiş). Üst duvara 10 × M8 kapalı uçlu perçin somun sıkılır; soğutma grubu rayları için 3 × M4 kapalı uçlu perçin somun şaseyle gelir.',
     'boy profili × 2 · çapraz profil × 7 · TIG çevre dikişi × 14 · M8 kapalı uçlu perçin somun × 10 · M4 kapalı uçlu perçin somun × 3')
kamera_genel(SASE, olcek=0.9)
for a in ['sase_boy_arka', 'sase_boy_on']: P[a]['fikstur'] = True; t = yerlestir([a], ['ust'], t, 'Boy profili 60 × 60 (kesim boyu 3661) kaynak fikstürüne', sure_bekle=0.1)
KAY_SASE = {a: [k for k in P if k.startswith('kaynak_' + a + '_')] for a in SASE if a.startswith('sase_capraz')}
ilk = True
for a in sorted(KAY_SASE):
    tt = yerlestir([a], ['ust'], t, 'Çapraz profil ↔ boy profilleri: iki uçta TIG çevre dikişi (kırmızı)', grup_kaynak=KAY_SASE[a], sure_bekle=0.05)
    if ilk: yakin(merkez(KAY_SASE[a][0]), 0.45, tt=tt - 0.2); ilk = False
t = bitti() + 0.2
yakin(np.array([1100, 115, -110]), 0.3)
t = tak('percin_sase', t, 0.6, 40.0, 'M8 kapalı uçlu perçin somun × 10 → şase üst duvarındaki deliklere sıkılır (çekme aleti, başı oturur)') + 0.5
# ---- 2 AYAKLAR
adim('Ayaklar', '14 ayarlı ayak (M12, katalog) şasenin altındaki kör burçlara aşağıdan vidalanır.', 'ayarlı ayak × 14 (M12)')
kamera_genel(SASE + ['ayaklar'], yon=(0.4, 0.25, 0.8), olcek=0.8)
t = yerlestir(['ayaklar'], ['alt'], t, 'Ayarlı ayaklar M12 → şase altındaki burçlara (aşağıdan vidalanır)') + 0.4
# ---- 3 DIŞ TABAN
adim('Dış taban', 'Dış taban iki parça (AISI 304 1,5 mm, lazer — büküm yok; zincir kanalı konsolları için 2 PEM saplama preslenmiş) şasenin üstüne iner; perçin somun başları tabandaki Ø15,5 boşluk deliklerine girer. Ek yerine üstten ek laması (punta, kırmızı). 10 × M8 × 16 cıvata + pul taban deliklerinden şasedeki kapalı uçlu perçin somunlara.',
     'dış taban 1 / 2 · ek laması (punta) · M8 × 16 cıvata × 10 + pul × 10')
kamera_genel(['g_dis_taban_1', 'g_dis_taban_2'], olcek=0.75)
for a in ['g_dis_taban_1', 'g_dis_taban_2', 'g_dis_taban_ek_lamasi']: t = yerlestir([a], ['ust'], t, '%s → şase üst yüzüne' % P[a]['ac'])
t = bitti(); puntala(t); t += 0.6
yakin(np.array([1100, 125, -110]), 0.3, tt=t + 0.2)
t = tak('sase_pul', t + 0.3, 0.5, 30.0, 'DIN 9021 M8 pul × 10 → dış taban delikleri üstüne')
t = tak('sase_civata', t, 0.6, 40.0, 'ISO 4762 M8 × 16 cıvata × 10 → pul + dış taban → şasedeki kapalı uçlu perçin somun (uç kapalı uca değmez)') + 0.3
# ---- 4 TABAN SANDVİÇİ
adim('Taban yalıtımı + iç taban', 'GFRP ısı köprüsü takozları (dikme altları) dış tabana; taban yalıtım levhası (PU, kesilmiş: dikme ve takoz boşlukları, şase cıvatalarının üstünde Ø25 delik) dış tabana yapıştırılır (yeşil yapıştırıcı), deliklere PU tapa; iç taban sacları (1 / 2, arka kenarı 15 mm yukarı bükülü flanş) üstüne.',
     'GFRP takoz × 6 · taban yalıtım levhası (PU) + yapıştırıcı · iç taban 1 / 2 (arka flanşlı)')
kamera_genel(['g_pu_taban_0'], olcek=0.7)
t = yerlestir(['gfrp_alt'], ['ust'], t, 'GFRP takoz × 6 → dış taban (dikme altları)')
t = yerlestir(['g_pu_taban_0'], ['ust', 'on'], t, 'Taban yalıtım levhası (PU) → dış tabanın üstüne')
t = yapistir('g_pu_taban_0', 1, -1, t); olay(t - 0.5, 'Yapıştırıcı (yeşil): taban yalıtım levhası ↔ dış taban')
TAPA = sorted(a for a in P if a.startswith('g_pu_taban_tapa'))
for a in TAPA: P[a]['ac'] = 'PU tapa Ø25'; yerlestir([a], ['ust'], t, None, sure_bekle=0.0)
t = bitti(); olay(t - 0.4, 'PU tapa Ø25 × 10 → levhadaki deliklerden şase cıvatalarının başı üstüne')
for a in ['g_ic_taban_1', 'g_ic_taban_2']: t = yerlestir([a], ['ust', 'on'], t, '%s (arka kenarı yukarı bükülü) → yalıtım levhasının üstüne' % P[a]['ac'])
adim_sonu()
# ---- 5 DIŞ KABUK: köşebentler + arka panel (tezgâhta yalıtımlı)
adim('Alt köşe dolguları + alt köşebentler', 'Sol alt köşeye köşe dolgu şeritleri (PU, köşebendin büküm dış yayı ile köşe arasındaki boşluk) yatırılır; alt köşebentler (1,5 mm · 1 büküm) tabana oturur, yatay kolu tabana punta.',
     'köşe dolgu şeridi × 3 · alt köşebent × 8 · punta')
kamera_genel(['g_kosebent_sol_alt_1', 'g_kosebent_sol_alt_3'], yon=(0.5, 0.5, 0.7), olcek=0.9)
for i in (1, 2, 3): yerlestir(['g_pu_sol_kose_alt_%d' % i], ['ust', 'on'], t, 'Sol alt köşe dolgu şeridi (PU) → köşeye', sure_bekle=0.0)
t = bitti()
ilk = True
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_alt_' in x):
    yerlestir([a], ['ust', 'on'], t, '%s → taban köşesi' % P[a]['ac'], kamera_yakin=ilk); ilk = False
adim_sonu()
adim('Arka panel (tezgâhta yalıtımlı)', 'Tezgâhta: dış arka 1 + ek laması + dış arka 2 puntalanır; yalıtım levhaları (PU) iki katman olarak sacın içine önden yatırılır — arka katman (23,5 mm) sacın üst ve alt bükümlü kenarlarının (flanş) ARASINA, ön katman (13,8 mm) onun önüne; sol duvarın arka şeridi de. Levhalar sac ve birbirine yapıştırılır (yeşil). Panel bütün olarak arkadan yerine girer; alt kenarı tabana, köşelerde yan saca punta.',
     'dış arka 1 / 2 + ek laması · arka yalıtım levhası: arka katman × 2, ön katman × 2 · sol arka şerit · yapıştırıcı · punta')
kamera_genel(['g_dis_arka_1', 'g_dis_arka_2'], yon=(0.35, 0.55, -0.75), olcek=0.7)
ARKA_PU = ['g_pu_arka_yuksek_arka', 'g_pu_arka_alcak_arka', 'g_pu_sol_arka_serit', 'g_pu_arka_yuksek_on', 'g_pu_arka_alcak_on']
ARKA_GRUP = ['g_dis_arka_1', 'g_dis_arka_ek_lamasi', 'g_dis_arka_2'] + ARKA_PU
YAP_ARKA = [yapistirici(a, 2, -1) for a in ARKA_PU]
t = yerlestir(ARKA_GRUP + YAP_ARKA, ['arka', ('arka', (0.0, 10.0, 0.0))], t, 'Arka panel (dış arka sac + iki katman yalıtım levhası, tezgâhta yapıştırılmış) → arkadan yerine', tezgah_kaynak=YAP_ARKA)
for n_ in YAP_ARKA:
    while n_ in YERINDE: YERINDE.remove(n_)
t = buyu('silikon_arka_kose', t, 0.6); olay(t - 0.6, 'Arka köşe silikonları (yeşil) sıkılır'); adim_sonu()
adim('Sol yan sac', 'Sol yan sac (arka kenarı 25 mm içe bükülü) yukarıdan iner: alt kenarı alt köşebentlerin dik koluna, arka dönüşü arka sacın kenarına dayanır ve PUNTA ile tutturulur (kırmızı noktalar: köşebent dik kolu ↔ yan sac, her 90 mm; arka sac ↔ yan arka dönüşü, her 80 mm). Üst kenarı sonra üst köşebentlere puntalanır.',
     'sol yan · punta: alt köşebentler × 3 (dik kol), arka dönüş × 8')
kamera_genel(['g_dis_sol_yan', 'g_kosebent_sol_alt_2'], yon=(-0.6, 0.45, 0.65), olcek=0.8)
t = yerlestir(['g_dis_sol_yan'], ['ust', 'sol'], t, 'Dış sol yan → alt köşebentlere ve arka sacın kenarına dayanır')
yakin(np.array([750, 140, -400]), 0.35, yon=(0.6, 0.4, 0.7), tt=t - 0.3)
adim_sonu()
# ---- 6 SOL DUVAR + İÇ ARKA
adim('Sol duvar yalıtımı + iç arka ve sol saclar', 'Sol duvar yalıtım levhası (PU, köşeleri köşebent kadar boşaltılmış) üstten iner, dış sol yana yapıştırılır; iç arka saclar (iç yüzünde evaporatör, kanal ve motor braketi saplamaları preslenmiş) arka levhanın önüne; iç sol duvar (15 PEM SP-M5 + köpük kapağı; alt / arka / üst kenarı gıda tarafına bükülü flanş) önüne — flanşları iç taban ve iç arka saca kör perçinle (mavi).',
     'sol yalıtım levhası + yapıştırıcı · iç arka 1 / 2 · iç sol duvar + 15 PEM · kör perçin')
kamera_genel(['g_pu_sol', 'g_ic_arka_1'], olcek=0.7)
t = yerlestir(['g_pu_sol'], ['ust', 'on'], t, 'Sol duvar yalıtım levhası (PU) → dış sol yanın içine')
t = yapistir('g_pu_sol', 0, -1, t)
for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['on', ('on', (0.0, 2.0, 0.0)), 'ust'], t, '%s → arka yalıtım levhasının önüne (taban flanşı arkasında kalır)' % P[a]['ac'], pem=PEM_SAC.get(a, []))
t = yerlestir(['g_ic_sol_duvar'], ['ust', ('on', (60.0, 0.0, 0.0)), 'on'], t, 'İç sol duvar → sol yalıtım levhasının önüne', pem=PEM_SAC.get('g_ic_sol_duvar', []), kamera_yakin=True)
adim_sonu()
# ---- 7 BÖLMELER
adim('Bölmeler 1–5', 'Her bölme bir sandviç: sac A yukarıdan (PEM SP-M5 + köpük kapağı üretimde preslenir; alt / arka / üst kenarı 12 mm dışa bükülü flanş) → kovanlar (kablo geçişi) sütundan yana sürülür, sac A\'ya köşe TIG (kırmızı) → yalıtım levhası (PU) sac A\'ya yapıştırılır → sac B (PEM\'li, flanşlı) sütundan yana kapanır, kovanlara köşe TIG. Flanşlar iç taban ve iç arka saca kör perçinle (mavi). Bölme 5\'in sağını teknik kapama sacı kapatır.',
     'sac A × 5 · kovan × 12 (köşe TIG) · yalıtım levhası × 5 + yapıştırıcı · sac B × 4 + teknik kapama · PEM SP-M5 × 111 · kör perçin · gider silikonu')
ilk = True
for k in range(1, 6):
    kamera_genel(['g_bolme_%d_sac_a' % k, 'g_bolme_%d_pu' % k], yon=(0.6, 0.5, 0.65), olcek=0.75)
    a = 'g_bolme_%d_sac_a' % k
    t = yerlestir([a], ['ust', 'on'], t, 'Bölme %d sol sacı (A) → iç taban + iç arka' % k, pem=PEM_SAC.get(a, []), kamera_yakin=ilk)
    for a in sorted(x for x in SAC if x.startswith('g_bolme_%d_kovan' % k)):
        kk = 'kaynak_%s_a' % a[2:]
        yerlestir([a], [('on', YAN), 'sag', 'ust'], t, '%s → sac A deliğine, köşe TIG' % P[a]['ac'], grup_kaynak=[kk] if kk in P else [], kamera_yakin=ilk); ilk = False
    t = bitti()
    t = yerlestir(['g_bolme_%d_pu' % k], [('on', YAN), 'sag', 'ust'], t, 'Bölme %d yalıtım levhası (PU) → sac A\'ya, kovanlar boşluklarından geçer' % k)
    t = yapistir('g_bolme_%d_pu' % k, 0, -1, t)
    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'
    kb = [x for x in P if x.startswith('kaynak_bolme_%d_kovan' % k) and x.endswith('_b')]
    t = yerlestir([b], [('on', YAN), 'sag', 'ust'] if k < 5 else [('on', (3.0, 0.0, 0.0)), ('on', YAN), 'on', 'ust'], t, '%s → yalıtım levhasının üstüne kapanır, kovanlara köşe TIG' % P[b]['ac'], pem=PEM_SAC.get(b, []), grup_kaynak=kb)
    t = baglantilari_tamamla(t) + 0.1
for k in range(1, 6):
    if 'silikon_gider_%d' % k in P: buyu('silikon_gider_%d' % k, t, 0.6)
olay(t, 'Gider geçişi silikonları (yeşil) sıkılır'); t += 0.9
adim_sonu()
KONS_Z = [a for a in P if a.startswith('b_zincir_') and not a.startswith('b_zincir_taban_')]
TEZGAH_BAG.update(KONS_Z)
for a_ in KONS_Z: P[a_]['tezgah'] = True
adim('Teknik bölme: soğutma grubu, elektrik plakası, zincir kanalı', "Bölmelerden sonra, sağ yan kapanmadan: B elektrik montaj plakası önden dış arka sacın 6 PEM saplamasına (M5 pul + somun); soğutma grubu (kompresör + kondenser + fan, tek ürün) önden iner, taban raylarının uçları 4 × ISO 4762 M4 + pul ile. Enerji zinciri kanalı tezgâhta 2 L konsoluna (2 mm, 1 büküm) 2'şer DIN 7337 Ø3,2 kör perçinle bağlanır, alt ucuna zemin geçiş contası takılır, birlikte üstten iner (conta dış tabandaki geçiş deliğinden aşağı uzanır); konsolların ayağı dış tabandaki PEM saplamalara geçer, M5 pul + somun.",
     'zincir kanalı + 2 L konsol + 4 kör perçin · 2 M5 somun · B elektrik montaj plakası + 6 M5 somun')
kamera_genel(['zincir_kanal', 'elektrik_kutusu'], olcek=1.0)
t = yerlestir(['sogutma_grubu'], ['ust', 'on'], t, 'Soğutma grubu (tek ürün) → teknik bölmenin altı, taban rayları zemine', kamera_yakin=True)
t = baglantilari_tamamla(t, 'Soğutma grubu taban rayı uçları: ISO 4762 M4 + pul → şasedeki kapalı uçlu perçin somun / tabanın altında pul + somun (mavi)') + 0.1
t = yerlestir(['elektrik_kutusu'], ['on', 'ust'], t, 'B elektrik montaj plakası → dış arka sacın saplamalarına', kamera_yakin=True)
t = yerlestir(['zincir_kanal', 'zemin_conta'] + KONS_Z, ['ust', ('ust', (0.0, 0.0, 30.0)), 'on'], t, 'Zincir kanalı + alt ucundaki zemin geçiş contası + 2 L konsol (tezgâhta kör perçinli) → zemin geçişine, konsollar tabandaki saplamalara', kamera_yakin=True)
adim_sonu()
adim('Sağ yan sac', 'Sağ yan sac (arka kenarı içe bükülü; istasyon kutusu konsolları için 2 PEM saplama preslenmiş) yukarıdan iner; alt köşebentlerin dik koluna ve arka sacın kenarına PUNTA (kırmızı).', 'sağ yan · punta')
kamera_genel(['g_dis_sag_yan'], olcek=0.9)
t = yerlestir(['g_dis_sag_yan'], ['ust', 'sag'], t, 'Dış sağ yan → alt köşebentlere ve arka sacın kenarına dayanır')
adim_sonu()
KONS_I = [a for a in P if a.startswith('b_istasyon_') and not a.startswith('b_istasyon_yan_')]
TEZGAH_BAG.update(KONS_I)
for a_ in KONS_I: P[a_]['tezgah'] = True
adim('İstasyon kutusu', 'Tezgâhta: 2 U konsol (2 mm paslanmaz, 2 büküm) kutunun sağ yan duvarına 2\'şer ISO 7380 M4 × 8 + pul + somun ile. Kutu konsollarıyla önden gelir, konsolların uç kolu sağ yan sacın PEM saplamalarına geçer; M5 pul + somun.',
     'U konsol × 2 + M4 × 8 × 4 · M5 pul + somun × 2')
kamera_genel(['istasyon_kutusu'], olcek=1.2)
t = yerlestir(['istasyon_kutusu'] + KONS_I, [('on', (-12.0, 0.0, 0.0)), ('ust', (-12.0, 0.0, 0.0)), ('on', (-12.0, 20.0, 0.0)), 'on', 'ust'], t, 'İstasyon kutusu + konsollar (tezgâhta cıvatalı) → sağ yan sacın saplamalarına', kamera_yakin=True)
adim_sonu()
# ---- 9 EVAPORATÖRLER
adim('Evaporatörler', 'Evaporatör 1 ve 2 (fan + serpantin + tava, tek ürün; üst braketlerine 20 × 22 duvar kulağı) çekmece sütunlarından önden sürülür, 4 braketi iç arka sactaki PEM FHS-M5 saplamalara geçer; M5 pul + somun.',
     'evaporatör × 2 · M5 pul + somun × 8')
kamera_genel(['evaporator_1', 'evaporator_2'], olcek=0.7)
for a in ['evaporator_1', 'evaporator_2']: t = yerlestir([a], ['on', 'ust'], t, '%s → iç arka sactaki saplamalara (önden)' % P[a]['ac'], kamera_yakin=(a == 'evaporator_1'))
adim_sonu()
# ---- 10 İÇ KANALLAR
adim('İç kanallar + kablolar', 'İç kablo kanalı parçaları sütun sütun önden yerine; taban plakasından saca DIN 7337 Ø4 (dar yerde Ø3,2) kör perçin, kanalın içinden (mavi; perçin ucu saç arkasındaki PU levhanın cebine açılır). Güç ve evaporatör kabloları kanal boyunca çekilir.',
     'iç kanal parçası × %d · kör perçin · kablolar' % len([a for a in P if a.startswith('ic_kanal_')]))
kamera_genel([a for a in P if a.startswith('ic_kanal_')], yon=(0.35, 0.4, 0.9), olcek=0.6)
KAD = ['on', ('on', (12.0, 0.0, 0.0)), ('on', (-12.0, 0.0, 0.0)), ('on', (0.0, 12.0, 0.0)), ('on', (0.0, -12.0, 0.0)), 'ust', ('ust', (0.0, 0.0, 12.0))]
KANAL_BUYU = []
for a in sorted(x for x in P if x.startswith('ic_kanal_')):
    n0 = len(PLAN_SORUN); yon_sec([a] + [s for s in STUD.get(a, [])], KAD)
    if len(PLAN_SORUN) > n0: PLAN_SORUN.pop(); KANAL_BUYU.append(a); continue
    yerlestir([a], KAD, t, None, sure_bekle=0.0)
t = bitti()
for a in KANAL_BUYU: buyu(a, t, 0.7)
if KANAL_BUYU: olay(t, '%d kanal parçası kovan / bölme geçişinden geçirilerek birleştirilir (kanal boyunca)' % len(KANAL_BUYU)); t += 0.8
t = baglantilari_tamamla(bitti(), 'İç kanallar: taban plakasından saca DIN 7337 kör perçin, kanalın içinden (mavi) — kablolar çekilmeden önce') + 0.1
t = buyu('guc_kablo', t, 0.8)
if 'evap_kablo' in P: t = buyu('evap_kablo', t - 0.4, 0.8)
olay(t - 0.8, 'Güç (koyu kırmızı) ve evaporatör (koyu mavi) kabloları kanal boyunca çekilir'); t += 0.3
adim_sonu()
KOL = {}
for ck in CEKD: KOL.setdefault(ck.split('_')[1], []).append(ck)
adim('Tahrik üniteleri', 'Her çekmece için: motor braketi önden arka duvara, 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5; step motor (katalog) göbeğiyle braket deliğine, 4 × DIN 7991 M3 × 6; GT3 kasnak mile + DIN 913 M3 × 4 setskur.',
     'motor braketi × 21 + M5 × 6 × 42 · step motor × 21 (siyah silindir) + M3 × 6 × 84 · kasnak × 21 + setskur × 21')
kamera_genel([ck + '_tahrik' for ck in CEKD], yon=(0.35, 0.45, 0.85), olcek=0.6)
ilk = True
for k in sorted(KOL):
    for ck in KOL[k]: yerlestir([ck + '_braket'], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_tahrik_vida', t, 0.5, 25.0)
    olay(t, 'Sütun %s: motor braketi × %d → arka iç sac: 2 × DIN 7991 M5 × 6 → PEM SP-M5' % (k, len(KOL[k])))
    if ilk: yakin(merkez(KOL[k][0] + '_tahrik_vida'), 0.35, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: yerlestir([ck + '_tahrik'], [('on', (4.0, 0.0, 0.0)), ('on', (40.0, 0.0, 0.0)), 'on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_motor_vida', t, 0.5, 12.0)
    olay(t, 'Sütun %s: step motor (siyah silindir, Transmotec PD3665) redüktör göbeğiyle braket deliğine · 4 × DIN 7991 M3 × 6 → motor yüzündeki M3 dişler' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_motor_vida'), 0.3, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: tak(ck + '_kasnak', t, 0.5, 12.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_setskur', t, 0.4, 15.0)
    olay(t - 0.5, 'Sütun %s: GT3 motor kasnağı mile · DIN 913 M3 × 4 setskur radyal deliğe' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_kasnak'), 0.3, tt=t - 0.5); ilk = False
    t = bitti() + 0.15
for a in sorted(x for x in P if x.startswith('b_kanal_') and x != 'b_kanal_988' and not P[x].get('etur')): yerlestir([a], ['on', 'ust'], t, 'Sütun dikey kablo kanalı → iç arka sactaki saplamalara')
t = bitti()
t = buyu('b_kanal_988', t, 1.0); olay(t - 1.0, 'Arka kablo kanalı: parçalar kovanlardan geçirilip birleştirilir (kanal boyunca)')
t = buyu('gider_hortumu', t, 0.8); olay(t - 0.8, 'Gider hortumu kanal boyunca çekilir'); t += 0.2
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
adim_sonu()
# ---- 11 İÇ TAVAN + ISI KALKANI + TEKNİK
adim('İç tavan + ısı kalkanı + teknik kapama', 'İç tavan 1 / 2 tezgâhta tavan yalıtım levhalarıyla (PU, yapıştırılmış) birlikte bölmelerin üstüne iner — bölme ve sol duvar flanşlarına alttan kör perçin; fırın üstünde ısı kalkanı U (2 büküm; tabanında 12 PEM FHS-M4 saplama) + 12 PTFE takoz + ışınım sacı (saplamalara M4 pul + somun); teknik bölmede ara sac ve yalıtım levhaları.',
     'iç tavan × 2 + kör perçin · tavan yalıtım levhaları + yapıştırıcı · ısı kalkanı U + 12 saplama · PTFE takoz × 12 · ışınım sacı + 12 somun · teknik ara sac + levhalar')
kamera_genel(['g_ic_tavan_1', 'g_ic_tavan_2', 'g_isi_kalkani_u'], olcek=0.7)
for sac_, pus in (('g_ic_tavan_1', ['g_pu_tavan_yuksek']), ('g_ic_tavan_2', ['g_pu_tavan_topping', 'g_pu_tavan_firin'])):
    yp = [yapistirici(a, 1, -1) for a in pus]
    t = yerlestir([sac_] + pus + yp, ['ust', 'on'], t, '%s + tavan yalıtım levhası (tezgâhta yapıştırılmış; perçin uçları için levha altı cepli) → bölmelerin üstüne' % P[sac_]['ac'], tezgah_kaynak=yp)
    for n_ in yp:
        while n_ in YERINDE: YERINDE.remove(n_)
t = baglantilari_tamamla(t, 'İç tavan: bölme ve sol duvar üst flanşlarına alttan (gıda tarafından) DIN 7337 Ø4 kör perçin (mavi)') + 0.1
for a in ['g_pu_isi_kalkani_kose_sol_0', 'g_pu_isi_kalkani_kose_sag_0', 'g_isi_kalkani_u']:
    t = yerlestir([a], ['ust', 'on'], t, '%s → yerine' % P[a]['ac'])
t = yerlestir(['takozlar'], ['ust', 'on'], t, '12 PTFE + cam elyaf takoz (siyah küçük kutular, ısı köprüsü kesici) → ısı kalkanının saplamalarına')
t = yerlestir(['g_isi_kalkani_isinim_08'], [('on', (0.0, 12.0, 0.0)), 'ust', 'on'], t, 'Isı kalkanı ışınım sacı → takozların üstüne, saplamalardan geçer')
t = yerlestir(['g_pu_b5_ust'], ['ust', 'on'], t, 'Bölme 5 üstü yalıtım levhası (PU) → yerine')
for a in ['g_tk_ara_arka_sac', 'sogutma_ust_sac', 'g_tk_ara_pu', 'depo_arka_sac', 'g_tk_depo_arka_pu', 'g_tk_depo_sag_pu', 'g_tk_depo_tavan_pu', 'depo_ic_sac']:
    t = yerlestir([a], ['ust', 'on', 'sag'], t, ('%s → teknik bölme' % ad_tr(a)) if a.startswith('g_') else {'depo_arka_sac': 'Soğuk depo arka sacı', 'depo_ic_sac': 'Soğuk depo iç sacı (taban + yanlar)', 'sogutma_ust_sac': 'Soğutma bölmesi üst sacları (2)'}[a] + ' → teknik bölme')
adim_sonu()
adim('Üst köşebentler + köşe dolguları', 'Üst köşebentler (1,5 mm · 1 büküm) yan sacların üst köşesine; dik kolu yan saca PUNTA (kırmızı). Köşebendin büküm dış yayı ile köşe arasındaki boşluğa köşe dolgu şeritleri (PU) üstten yatırılır.', 'üst köşebent × 5 · punta · köşe dolgu şeridi × 4')
kamera_genel(['g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_3'], yon=(0.5, 0.6, 0.6), olcek=0.9)
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti()
for i in (1, 2, 3): yerlestir(['g_pu_sol_kose_ust_%d' % i], ['ust', 'on'], t, 'Sol üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına', sure_bekle=0.0)
yerlestir(['g_tk_depo_kose_dolgu'], ['ust', 'on'], t, 'Soğuk depo sağ üst köşe dolgu şeridi (PU) → köşebendin büküm dış yayı ile köşe arasına', sure_bekle=0.0)
adim_sonu()
# ---- 12 MODÜLER İSKELET
adim('Modüler iskelet', 'Dikmelerin alt ucuna içeriden uç plakası + 2 × DIN 929 M5 kaynak somunu TIG (tezgâhta, kırmızı). 3 ara dikme ve 6 taşıyıcı dikme yukarıdan yalıtım / iç sac boşluklarından GFRP takozlara iner; arka ve ön merdiven çerçeve (kaynaklı alt montaj) iner, ara dikme başları üst kirişe TIG. Her dikme ayağı ALTTAN 2 × ISO 4762 M5 × 16 + pul ile: şase üst duvarı → dış taban → GFRP → uç plakası → kaynak somunu (şase alt duvarındaki erişim deliğinden). Taşıyıcı üst çerçeve TIG; üstte GFRP şeritler ve 12 × M8 kapalı uçlu perçin somun.',
     'ara dikme × 3 · merdiven çerçeve × 2 (TIG) · taşıyıcı dikme × 6 + üst çerçeve (TIG) · ayak cıvatası M5 × 16 × 24 · GFRP şerit × 2 · M8 kapalı uçlu perçin somun × 12')
ISK = ['moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'] + [a for a in P if a.startswith(('moduler_dikme', 'tasiyici_dikme'))]
kamera_genel(ISK, olcek=0.7)
MD = sorted(x for x in P if x.startswith('moduler_dikme'))
for a in MD: yerlestir([a], ['ust'], t, 'Ara dikme (alt ucu plakalı, kaynak somunlu) → GFRP takoz', sure_bekle=0.05)
TD = sorted(a for a in P if a.startswith('tasiyici_dikme') and HI[a][1] < 750)
for a in TD: yerlestir([a], ['ust'], t, 'Taşıyıcı dikme (alt ucu plakalı) → dış taban', sure_bekle=0.05)
t = bitti()
t = yerlestir(['moduler_cerceve_arka'], ['ust'], t, 'Arka merdiven çerçeve → GFRP takozlar · ara dikme başı TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_arka'] if x in P])
t = yerlestir(['moduler_cerceve_on'], ['ust'], t, 'Ön merdiven çerçeve → GFRP takozlar · ara dikme başları TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_on', 'kaynak_moduler_dikme_2076_on'] if x in P])
t = yerlestir([x for x in ['tasiyici_ust', 'tasiyici_dikme_3386_600', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574'] if x in P], ['ust'], t, 'Taşıyıcı üst çerçeve → dikmelere: dikme başları TIG', grup_kaynak=['kaynak_' + a for a in TD])
t = bitti(); yakin(np.array([1436, 110, -706]), 0.35, yon=(0.5, -0.35, 0.8), tt=t)
t = baglantilari_tamamla(t, 'Dikme ayakları alttan: 2 × ISO 4762 M5 × 16 + pul → şase / dış taban / GFRP / uç plakası → kaynak somunu (mavi)') + 0.2
for a in ['gfrp_ust_arka', 'gfrp_ust_on']: t = yerlestir([a], ['ust'], t, 'GFRP üst şerit → üst kiriş')
t = tak('percin_ust', t, 0.6, 40.0, 'M8 kapalı uçlu perçin somun × 12 → üst kirişler (A kaidesi, K iskeleti ve TOPPING M8 × 16 cıvataları için)') + 0.3
adim_sonu()
# ---- 13 TAVAN
adim('Tavan', '3 ek laması; dış tavan 1 / 2 GFRP şeritlerin üstüne, köşebentlere ve arka sacın üst dönüşüne PUNTA (kırmızı); ek yeri silikonu (yeşil).', 'ek laması × 3 · dış tavan × 2 · punta · silikon')
kamera_genel(['g_dis_tavan_1', 'g_dis_tavan_2'], olcek=0.7)
for a in ['g_dis_tavan_ek_lamasi_1', 'g_dis_tavan_ek_lamasi_2', 'g_dis_tavan_ek_lamasi_3']: yerlestir([a], ['ust', 'on'], t, '%s' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_1', 'g_dis_tavan_2']: t = yerlestir([a], ['ust'], t, '%s → GFRP şeritler + köşebentler üstüne' % P[a]['ac'])
t = buyu('silikon_ek_yeri', t, 0.6); olay(t - 0.6, 'Dış kabuk ek yeri silikonu (yeşil: taban / arka / tavan)'); t += 0.3
adim_sonu()
# ---- 14 ÖN ÇERÇEVE
adim('Ön çerçeve + avara üniteleri', '430 ferritik ön çerçeve iki parça (lazer, düz) — iç saclara ve yalıtım levhalarına ALIN yapıştırma (MS polimer, yeşil; ısı köprüsü olmasın diye mekanik bağ yok). Tezgâhta: her çekmecenin avara ünitesi ön flanşından çerçevenin arkasına TIG köşe 2 × 8 mm (kırmızı). Çerçeve 1 (K1–K2) ve 2 (K3–K6) avaralarıyla önden gelir; ek yeri arkadan ek lamasıyla.',
     'ön çerçeve 1 / 2 · ek laması · avara ünitesi × 21 · TIG 2 × 8 mm × 21 · alın yapıştırma')
kamera_genel(['g_on_cerceve_1', 'g_on_cerceve_2'], yon=(0.3, 0.35, 0.9), olcek=0.7)
t = yerlestir(['g_on_cerceve_ek_lamasi'], ['on'], t, 'Ön çerçeve ek laması → bölme 2 önüne')
for cer, kol in (('g_on_cerceve_1', ('K1', 'K2')), ('g_on_cerceve_2', ('K3', 'K5', 'K6'))):
    av = [ck + '_avara' for ck in sorted(CEKD) if ck.split('_')[1] in kol]; ka = [ck + '_kaynak' for ck in sorted(CEKD) if ck.split('_')[1] in kol]
    t = yerlestir([cer] + av + ka, ['on'], t, '%s + %d avara ünitesi (tezgâhta arkasına TIG) → iç sac ve yalıtım levhası önlerine (alın yapıştırma)' % (P[cer]['ac'], len(av)), tezgah_kaynak=ka, kamera_yakin=(cer == 'g_on_cerceve_1'))
t = yerlestir(['g_cerceve_derz_dolgusu'], ['on'], t, 'Ön çerçeve derz dolgu şeridi → çerçeve 1 ↔ 2 arası')
adim_sonu()
# ---- RAYLAR · ÇEKMECELER
adim('Sabit raylar', '42 ray ünitesi (Accuride DZ3832-0700, katalog) sütun sütun önden sürülür; her ray 3 × DIN 7991 M5 × 6 havşa vida ile bölme sacındaki PEM SP-M5\'lere (126 vida, her biri kendi ekseninde).',
     'ray × 42 · DIN 7991 M5 × 6 × 126 → PEM SP-M5')
kamera_genel([ck + '_ray_sol' for ck in CEKD], yon=(0.35, 0.4, 0.9), olcek=0.6)
ilk = True
for k in sorted(KOL):
    rs = [ck + '_ray_' + y for ck in KOL[k] for y in ('sol', 'sag')]
    for r in rs: yerlestir([r], ['on'], t, None, sure_bekle=0.0)
    t = bitti()
    for ck in KOL[k]:
        for y in ('sol', 'sag'): tak(ck + '_vida_' + y, t, 0.55, 25.0)
    olay(t, 'Sütun %s: %d ray × 3 × DIN 7991 M5 × 6 → bölme sacındaki PEM SP-M5 (havşa başı ray deliğine oturur)' % (k, len(rs)))
    if ilk: yakin(merkez(KOL[k][0] + '_vida_sol'), 0.3, tt=t); ilk = False
    vurgu(rs, t, t + 1.2); t = bitti() + 0.15
adim('Çekmeceler', 'İLK çekmecenin tam montajı ayrı sayfada ("Tek çekmece montajı"). Burada 21 çekmece bitmiş alt montaj olarak sütun sütun ray ekseni boyunca sürülür; GT3 kayış kasnaklara sarılır; çekmece açılır, kayış çenesi: alt gövde + üst çene + 2 × ISO 7380 M3 × 12 + 2 × M3 somun; çekmece kapanır; reed ve motor kabloları kanala çekilir.',
     'çekmece × 21 · kayış × 21 · çene: alt gövde + üst çene + 2 × M3 × 12 + 2 × M3 somun · kablolar')
kamera_genel([ck + '_cekmece' for ck in CEKD], yon=(0.35, 0.4, 0.9), olcek=0.6)
ilk = True
for k in sorted(KOL):
    cks = KOL[k]
    grp = [ck + x for ck in cks for x in ('_cekmece', '_ara')]
    t0 = t
    for a in grp: basla(a, np.array([0, 0, 900.0]), t0)
    olay(t0, 'Sütun %s: %d çekmece ray ekseni boyunca sürülür (kızak → ara eleman → dış eleman)' % (k, len(cks)))
    kamera_genel([ck + '_cekmece' for ck in cks], yon=(0.4, 0.4, 0.9), olcek=1.0, tt=t0)
    for a in grp: git(a, np.zeros(3), t0 + 0.2, 1.4)
    t = t0 + 1.7
    for ck in cks: buyu(ck + '_kayis', t, 0.7)
    olay(t, 'Sütun %s: GT3 kayış motor kasnağı ↔ avara kasnağı sarılır' % k); t += 0.85
    for ck in cks: git(ck + '_cekmece', np.array([0, 0, 700.0]), t, 0.9); git(ck + '_ara', np.array([0, 0, 350.0]), t, 0.9)
    olay(t, 'Çekmeceler açılır (çene erişimi)'); t += 1.0
    if ilk: yakin(merkez(cks[0] + '_cene_ust') + np.array([0, 0, 700.0]), 0.28, tt=t - 0.2)
    for ck in cks:
        basla(ck + '_cene_alt', np.array([0, -30.0, 700.0]), t); git(ck + '_cene_alt', np.array([0, 0, 700.0]), t, 0.45)
        basla(ck + '_cene_ust', np.array([30.0, 0, 700.0]), t + 0.5); git(ck + '_cene_ust', np.array([0, 0, 700.0]), t + 0.5, 0.45)
        basla(ck + '_cene_vida', np.array([0, 25.0, 700.0]), t + 1.0); git(ck + '_cene_vida', np.array([0, 0, 700.0]), t + 1.0, 0.45)
        basla(ck + '_cene_somun', np.array([0, -20.0, 700.0]), t + 1.5); git(ck + '_cene_somun', np.array([0, 0, 700.0]), t + 1.5, 0.45)
        vurgu([ck + '_cene_alt', ck + '_cene_ust'], t, t + 1.0); vurgu([ck + '_cene_vida', ck + '_cene_somun'], t + 1.0, t + 2.6)
    olay(t, 'Kayış çenesi: alt gövde (alttan) → üst çene (yandan) → 2 × ISO 7380 M3 × 12 (üstten) → 2 × ISO 4032 M3 somun (alttan)')
    t += 2.1
    for ck in cks:
        for x in ('_cekmece', '_cene_alt', '_cene_ust', '_cene_vida', '_cene_somun'): git(ck + x, np.zeros(3), t, 0.9)
        git(ck + '_ara', np.zeros(3), t, 0.9)
    olay(t, 'Çekmeceler kapanır'); t += 1.0
    for ck in cks:
        if ck + '_kablo' in P: buyu(ck + '_kablo', t, 0.7)
    olay(t, 'Sütun %s: reed sensör + motor kabloları kanal boyunca' % k); t += 0.85
    for ck in cks:
        for x in ('_cekmece', '_ara', '_kayis', '_cene_alt', '_cene_ust', '_cene_vida', '_cene_somun', '_kablo'):
            if ck + x in P: YER[ck + x] = t; YERINDE.append(ck + x)
    ilk = False
# ---- SOĞUK DEPO + ÖN PANELLER
adim('Soğuk depo + ön paneller', 'Izgara tutucuları, depo rayları ve depo çekmecesi (ön panel + PU + conta) önden; soğutma bölmesinin ön ızgarası.',
     'ızgara tutucuları · depo rayları · depo çekmecesi · ön ızgara')
kamera_genel(['depo_cekmece', 'sogutma_on_izgara'], yon=(0.4, 0.35, 0.9), olcek=0.8)
t = yerlestir(['izgara_tutucu'], ['on'], t, 'Izgara tutucuları → ön çerçeve')
t = yerlestir(['depo_ray'], ['on'], t, 'Depo sabit rayları')
t = yerlestir(['depo_cekmece'], ['on'], t, 'Depo çekmecesi ray ekseni boyunca')
t = yerlestir(['sogutma_on_izgara'], ['on'], t, 'Soğutma bölmesi ön ızgarası → tutuculara')
adim_sonu()
t += 0.6
kam(t, ([6.0, 2.6, 5.4], [2.57, 0.45, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
eksik = [a for a in P if a not in GOR]
print('süre %.1f s · adım %d · öğe %d · zamanlanmamış %d %s' % (TOPLAM, len(ADIM), len(P), len(eksik), eksik[:30]))
print('PLAN SORUNU', len(PLAN_SORUN)); [print('  ', s) for s in PLAN_SORUN[:60]]
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM, PLAN_SORUN=PLAN_SORUN,
                 CEKD=CEKD, SAC_AD=list(SAC), HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN), open('plan_b4.pkl', 'wb'))
print('%.0f s' % (time.time() - T0))
