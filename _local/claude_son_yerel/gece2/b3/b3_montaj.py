# -*- coding: utf-8 -*-
"""B (ÇEKMECELİ SOĞUK DOLAP) MONTAJ ANİMASYONU v3 — çekmece v3 yöntemiyle (plan_B.md ile birebir) · 4 Eki 2026 · yerel
Girdi: b3_parca.pkl (hat3_v9l), acinim_B (sac_morf) · Çıktı: plan_b3.pkl → b3_cikti.py (denetim + GLB/JSON)
Her parça kendi YAKLAŞMA ÇİZGİSİNDE (yerinin üstünde / önünde / arkasında) belirir: sac → düz açınım (lazer) → bükümler (abkant, sırayla) → PEM / köpük kapağı preslenir →
tek doğru boyunca yerine iner. Yön, plan anında sürekli çarpışma denetimiyle (aday yönler sırayla) seçilir."""
import sys, os, json, pickle, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf as SM
T0 = time.time()
D0 = pickle.load(open('b3_parca.pkl', 'rb')); P = D0['P']; CEKD = D0['CEKD']
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
            ls, hs = kutu(s_); ex = hs - ls; ax = int(np.argmin(ex))
            if ex[ax] > 3 or abs((ls[ax] + hs[ax]) / 2 - ca[ax]) > 4: continue
            o = [k for k in range(3) if k != ax]
            if all(ls[k] - 1 < la[k] and ha[k] < hs[k] + 1 for k in o): cand.append(s_)
        assert len(cand) == 1, (a, cand)
        by.setdefault(cand[0], []).append(a)
    for s, L in by.items():
        V, F = birles(L); n = ad_on + s[2:]
        ls, hs = kutu(s); ax = int(np.argmin(hs - ls)); sx = (ls[ax] + hs[ax]) / 2; cx = (V[:, ax].min() + V[:, ax].max()) / 2
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
grupla('sase_civata', [a for a in P if a.startswith('g_arayuz_sase')], 'baglanti', 'baglanti', '10 × ISO 4762 M8 cıvata → perçin somun', eks=(0, -1.0, 0))
grupla('silikon_arka_kose', [a for a in P if a.startswith('g_arka_kose_silikonu')], 'koyu', 'silikon', 'arka köşe silikonları')
for k in range(1, 6):
    L = [a for a in P if a.startswith('g_bolme_%d_gider_silikonu' % k)]
    if L: grupla('silikon_gider_%d' % k, L, 'koyu', 'silikon', 'gider geçişi silikonu (bölme %d)' % k)
grupla('silikon_ek_yeri', [a for a in P if a.startswith('g_ek_yeri_silikon')], 'koyu', 'silikon', 'dış kabuk ek yeri silikonu (taban / arka / tavan)')
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
    ilk = None
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
        if not s: return y, yol
    PLAN_SORUN.append(dict(parca=adlar, yon=str(ilk[0]), sorun=ilk[2][:4]))
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
            olay(tt, '%s · PEM presleme: %s' % (P[a0]['ac'], ' + '.join(P[p]['ac'] for p in pem)))
            tt += 0.55
    if tezgah_kaynak:
        for k_ in tezgah_kaynak: MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, 'Tezgâhta TIG: %s' % P[tezgah_kaynak[0]]['ac']); tt += 0.8
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

# ================================================================== PLAN (plan_B.md v2 sırası)
for a in ('g_dis_taban_1', 'g_dis_taban_2'): HARIC_PLAN.add(('percin_sase', a))
for k in range(1, 6):
    for kv in [x for x in P if x.startswith('g_bolme_%d_kovan' % k)]:
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, kv)); HARIC_NEDEN[('g_bolme_%d_pu' % k, kv)] = 'kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)'
for kb_ in ('g_kosebent_sag_ust_2',):
    for pu in ('g_tk_depo_arka_pu', 'g_tk_depo_sag_pu'):
        HARIC_PLAN.add((kb_, pu)); HARIC_NEDEN[(kb_, pu)] = 'MODEL AÇIĞI: PU levha köşebendin büküm dış köşesini ve ön ucunu sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'
N_PU = 'MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli'
for pu, L in (('g_pu_arka_yuksek', ('g_dis_arka_1', 'g_dis_arka_ek_lamasi', 'g_dis_arka_2')), ('g_pu_arka_alcak', ('g_dis_arka_2',)),
              ('g_pu_sol', ('g_kosebent_sol_alt_1', 'g_kosebent_sol_alt_2', 'g_kosebent_sol_alt_3', 'g_dis_arka_1', 'g_dis_sol_yan'))):
    for x in L: HARIC_PLAN.add((pu, x)); HARIC_NEDEN[(pu, x)] = N_PU
for k in range(1, 6):
    for yan in ('a', 'b'):
        HARIC_PLAN.add(('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))); HARIC_NEDEN[('g_bolme_%d_pu' % k, 'kapak_bolme_%d_sac_%s' % (k, yan))] = 'köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)'
for a_, L_ in (('percin_sase', ('sase_boy_arka', 'sase_boy_on')), ('percin_ust', ('moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'))):
    for x in L_: HARIC_PLAN.add((a_, x)); HARIC_NEDEN[(a_, x)] = 'perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)'
for kb_ in ('g_kosebent_sol_ust_1', 'g_kosebent_sol_ust_2', 'g_kosebent_sol_ust_3'):
    HARIC_PLAN.add((kb_, 'g_pu_sol')); HARIC_NEDEN[(kb_, 'g_pu_sol')] = 'MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz'
for a in ('g_dis_tavan_1', 'g_dis_tavan_2', 'tasiyici_ust', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574', 'gfrp_ust_arka', 'gfrp_ust_on'): HARIC_PLAN.add(('percin_ust', a))
KAM.append([0.0, [6.2, 3.2, 5.6], [2.57, 0.45, -0.4]])
t = 0.4
SASE = ['sase_boy_arka', 'sase_boy_on'] + sorted(a for a in P if a.startswith('sase_capraz_'))
YAN = (60.0, 0.0, 0.0)          # sütundan yana sürme (bölme sandviçi): önce sütunda +x 60, sonra −x
# ---- 1 ŞASE
adim('Şase', 'Alt şase: 2 boy profili + 7 çapraz profil (AISI 304 kutu 60 × 60, kesim boyunda) yukarıdan iner; her çapraz profil iki ucundan boy profillerine TIG çevre dikişiyle kaynaklanır. Üst duvara 10 × M8 kapalı uçlu perçin somun sıkılır.',
     'boy profili × 2 · çapraz profil × 7 · TIG çevre dikişi × 14 · M8 perçin somun × 10')
kamera_genel(SASE, olcek=0.9)
for a in ['sase_boy_arka', 'sase_boy_on']: t = yerlestir([a], ['ust'], t, 'Boy profili 60 × 60 (kesim boyu 3661) yerine', sure_bekle=0.1)
KAY_SASE = {a: [k for k in P if k.startswith('kaynak_' + a + '_')] for a in SASE if a.startswith('sase_capraz')}
ilk = True
for a in sorted(KAY_SASE):
    tt = yerlestir([a], ['ust'], t, 'Çapraz profil ↔ boy profilleri: iki uçta TIG çevre dikişi', grup_kaynak=KAY_SASE[a], sure_bekle=0.05)
    if ilk: yakin(merkez(KAY_SASE[a][0]), 0.45, tt=tt - 0.2); ilk = False
t = bitti() + 0.2
yakin(np.array([1100, 115, -110]), 0.3)
t = tak('percin_sase', t, 0.6, 40.0, 'Perçin somun M8 × 10 → şase üst duvarındaki deliklere sıkılır (çekme aleti, başı oturur)') + 0.5
# ---- 2 AYAKLAR
adim('Ayaklar', '14 ayarlı ayak (M12, katalog) şasenin altındaki kör burçlara aşağıdan vidalanır.', 'ayarlı ayak × 14 (M12)')
kamera_genel(SASE + ['ayaklar'], yon=(0.4, 0.25, 0.8), olcek=0.8)
t = yerlestir(['ayaklar'], ['alt'], t, 'Ayarlı ayaklar M12 → şase altındaki burçlara (aşağıdan vidalanır)') + 0.4
# ---- 3 DIŞ TABAN + ŞASE CIVATALARI
adim('Dış taban', 'Dış taban iki parça (AISI 304 1,5 mm, lazer — büküm yok) şasenin üstüne iner; perçin somun başları tabandaki Ø15,5 boşluk deliklerine girer. Ek yerine üstten ek laması (punta 18). 10 × M8 cıvata + pul taban deliklerinden şasedeki perçin somunlara.',
     'dış taban 1 / 2 · ek laması (punta 18) · M8 cıvata × 10 + pul × 10')
kamera_genel(['g_dis_taban_1', 'g_dis_taban_2'], olcek=0.75)
for a in ['g_dis_taban_1', 'g_dis_taban_2', 'g_dis_taban_ek_lamasi']: t = yerlestir([a], ['ust'], t, '%s → şase üst yüzüne' % P[a]['ac'])
olay(t - 0.3, 'Punta 18 nokta: dış taban ek laması ↔ taban 1 / 2'); vurgu(['g_dis_taban_ek_lamasi'], t - 0.3, t + 1.0)
yakin(np.array([1100, 125, -110]), 0.3, tt=t + 0.2)
t = tak('sase_pul', t + 0.3, 0.5, 30.0, 'DIN 9021 M8 pul × 10 → dış taban delikleri üstüne')
t = tak('sase_civata', t, 0.6, 40.0, 'ISO 4762 M8 cıvata × 10 → pul + dış taban → şase perçin somunu') + 0.3
# ---- 4 TABAN SANDVİÇİ
adim('Taban yalıtımı + iç taban', 'GFRP ısı köprüsü takozları (dikme altları) dış tabana; PU yalıtım levhası (kesilmiş: dikme, takoz ve cıvata boşlukları açık) serilir; iç taban sacları (1 / 2) üstüne.',
     'GFRP takoz × 6 · PU taban levhası · iç taban 1 / 2')
kamera_genel(['g_pu_taban_0'], olcek=0.7)
t = yerlestir(['gfrp_alt'], ['ust'], t, 'GFRP takoz × 6 → dış taban (dikme altları)')
t = yerlestir(['g_pu_taban_0'], ['ust', 'on'], t, 'PU taban levhası → dış tabanın üstüne (kesilmiş levha)')
for a in ['g_ic_taban_1', 'g_ic_taban_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın üstüne' % P[a]['ac'])
t += 0.3
# ---- 5 DIŞ KABUK
adim('Dış kabuk (taban köşebentleri + arka)', 'Alt köşebentler (1,5 mm · 1 büküm) tabana; arka sac 1 / 2 (2 büküm) arkadan, ek laması içeriden (punta); arka köşe silikonu.',
     'köşebent alt × 8 · arka 1 / 2 + ek laması · punta · silikon')
kamera_genel(['g_dis_sol_yan', 'g_dis_sag_yan', 'g_dis_arka_1', 'g_dis_arka_2'], yon=(0.35, 0.55, -0.75), olcek=0.7)
ilk = True
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_alt_' in x):
    yerlestir([a], ['ust', 'on'], t, '%s → taban köşesi (punta)' % P[a]['ac'], kamera_yakin=ilk); ilk = False
t = bitti()
t = yerlestir(['g_dis_arka_1', 'g_dis_arka_ek_lamasi'], ['arka', 'ust'], t, 'Dış arka 1 (+ ek laması tezgâhta puntalı) → arkadan')
t = yerlestir(['g_dis_arka_2'], ['arka', 'ust'], t, 'Dış arka 2 → arkadan, ek lamasına punta')
t = buyu('silikon_arka_kose', t, 0.6); olay(t - 0.6, 'Arka köşe silikonları sıkılır'); t += 0.3
adim('Sol yan sac', 'Sol yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sol yan · punta')
kamera_genel(['g_dis_sol_yan'], olcek=0.9)
t = yerlestir(['g_dis_sol_yan'], ['ust', 'sol'], t, 'Dış sol yan → taban + köşebentler (punta)') + 0.2
# ---- 6 ARKA + SOL DUVAR SANDVİÇİ
adim('Arka ve sol duvar yalıtımı + iç saclar', 'Yüzey yüzey: PU arka levhaları (alçak / yüksek, kesilmiş) dış arka sacın önüne, iç arka sac 1 / 2 önüne; sol duvarda PU levha ve iç sol duvar (15 PEM SP-M5 + köpük kapağı üretimde preslenir).',
     'PU arka × 2 · iç arka 1 / 2 · PU sol · iç sol duvar + 15 PEM')
kamera_genel(['g_pu_arka_yuksek', 'g_pu_arka_alcak', 'g_pu_sol'], olcek=0.7)
for a in ['g_pu_arka_yuksek', 'g_pu_arka_alcak']: t = yerlestir([a], ['ust', 'on'], t, '%s → dış arka sacın önüne (kesilmiş levha)' % P[a]['ac'])
for a in ['g_ic_arka_1', 'g_ic_arka_2']: t = yerlestir([a], ['ust', 'on'], t, '%s → PU levhanın önüne' % P[a]['ac'], pem=PEM_SAC.get(a, []))
t = yerlestir(['g_pu_sol'], ['ust', 'on'], t, 'PU sol levha → dış sol yanın içine')
t = yerlestir(['g_ic_sol_duvar'], [('on', (60.0, 0.0, 0.0)), 'ust', 'on'], t, 'İç sol duvar → PU sol levhanın önüne', pem=PEM_SAC.get('g_ic_sol_duvar', []), kamera_yakin=True) + 0.2
# ---- 7 BÖLMELER (soldan sağa, her biri sandviç)
adim('Bölmeler 1–5', 'Her bölme bir sandviç: sac A yukarıdan (PEM SP-M5 + köpük kapağı üretimde preslenir) → kovanlar (kablo kanalı geçişi, 1–2 büküm) sütundan yana sürülür, sac A\'ya köşe TIG → PU levha (kesilmiş) sütundan yana → sac B (PEM\'li) sütundan yana kapanır, kovanlara köşe TIG. Bölme 5\'i teknik bölme sol duvarı kapatır.',
     'sac A × 5 · kovan × 12 (köşe TIG) · PU × 5 · sac B × 4 + teknik sol duvar · PEM SP-M5 × 111 + köpük kapağı · gider silikonu')
ilk = True
for k in range(1, 6):
    kamera_genel(['g_bolme_%d_sac_a' % k, 'g_bolme_%d_pu' % k], yon=(0.6, 0.5, 0.65), olcek=0.75)
    a = 'g_bolme_%d_sac_a' % k
    t = yerlestir([a], ['ust', 'on'], t, 'Bölme %d sac A → iç taban + iç arka' % k, pem=PEM_SAC.get(a, []), kamera_yakin=ilk)
    for a in sorted(x for x in SAC if x.startswith('g_bolme_%d_kovan' % k)):
        kk = 'kaynak_%s_a' % a[2:]
        yerlestir([a], [('on', YAN), 'sag', 'ust'], t, '%s → sac A deliğine, köşe TIG' % P[a]['ac'], grup_kaynak=[kk] if kk in P else [], kamera_yakin=ilk); ilk = False
    t = bitti()
    t = yerlestir(['g_bolme_%d_pu' % k], [('on', YAN), 'sag', 'ust'], t, 'Bölme %d PU levhası (kesilmiş) → sac A\'ya, kovanlar boşluklarından geçer' % k)
    b = 'g_bolme_%d_sac_b' % k if k < 5 else 'g_teknik_sol_duvar'
    kb = [x for x in P if x.startswith('kaynak_bolme_%d_kovan' % k) and x.endswith('_b')]
    t = yerlestir([b], [('on', YAN), 'sag', 'ust'], t, '%s → PU levhanın üstüne kapanır, kovanlara köşe TIG' % P[b]['ac'], pem=PEM_SAC.get(b, []), grup_kaynak=kb)
for k in range(1, 6):
    if 'silikon_gider_%d' % k in P: buyu('silikon_gider_%d' % k, t, 0.6)
olay(t, 'Gider geçişi silikonları sıkılır'); t += 0.9
adim('Soğutma grubu + elektrik kutuları', 'Bölmeler bitince, sağ yan kapanmadan: soğutma grubu (kompresör + kondenser + fan, tek ürün) sağ alt bölmeye yukarıdan iner, braketleri köşebent aralıklarına oturur; B elektrik kutusu rafın üstünden önden dış arka saca; istasyon kutusu.',
     'soğutma grubu · B elektrik kutusu · istasyon kutusu')
kamera_genel(['sogutma_grubu', 'elektrik_kutusu'], olcek=0.9)
t = yerlestir(['sogutma_grubu'], ['ust', 'on', 'sag'], t, 'Soğutma grubu → sağ alt bölme (braketler köşebent aralıklarına)', kamera_yakin=True)
t = yerlestir(['elektrik_kutusu'], ['on', ('on', (0.0, 25.0, 0.0)), ('on', (0.0, 29.0, 0.0)), 'ust'], t, 'B elektrik kutusu → soğutma grubu rafının üstünden teknik bölme arka duvarına', kamera_yakin=True)
t = yerlestir(['istasyon_kutusu'], ['ust', 'on'], t, 'İstasyon kutusu') + 0.2
adim('Sağ yan sac', 'Sağ yan sac (1 büküm) yukarıdan iner; alt köşebentlere ve arka saca punta.', 'sağ yan · punta')
kamera_genel(['g_dis_sag_yan'], olcek=0.9)
t = yerlestir(['g_dis_sag_yan'], ['ust', 'sag'], t, 'Dış sağ yan → taban + köşebentler (punta)')
t += 0.2
# ---- 9 SOĞUTMA
adim('Evaporatörler', 'Evaporatör 1 ve 2 (fan + serpantin + tava, braketleriyle tek ürün) çekmece sütunlarından içeri sürülür, iç arka saca oturur.',
     'evaporatör × 2')
kamera_genel(['evaporator_1', 'evaporator_2'], olcek=0.7)
for a in ['evaporator_1', 'evaporator_2']: t = yerlestir([a], ['on', 'ust'], t, '%s → iç arka saca (önden)' % P[a]['ac'], kamera_yakin=(a == 'evaporator_1'))
# ---- 10 İÇ KANALLAR + KABLOLAR + TAHRİK (ön çerçeveden önce)
adim('İç kanallar + kablolar', 'İç kablo kanalı parçaları sütun sütun önden; enerji zinciri kanalı + zemin contası, kablo klipsi. Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir.',
     'iç kanal parçası × %d · zincir kanalı · klips · güç / bilgi kabloları' % len([a for a in P if a.startswith('ic_kanal_')]))
kamera_genel([a for a in P if a.startswith('ic_kanal_')], yon=(0.35, 0.4, 0.9), olcek=0.6)
KANAL_BUYU = []
for a in sorted(x for x in P if x.startswith('ic_kanal_')):
    n0 = len(PLAN_SORUN); yon_sec([a], ['on', 'ust'])
    if len(PLAN_SORUN) > n0: PLAN_SORUN.pop(); KANAL_BUYU.append(a); continue
    yerlestir([a], ['on', 'ust'], t, None, sure_bekle=0.0)
t = bitti()
for a in KANAL_BUYU: buyu(a, t, 0.7)
if KANAL_BUYU: olay(t, '%d kanal parçası kovan / bölme geçişinden geçirilerek birleştirilir (kanal boyunca)' % len(KANAL_BUYU)); t += 0.8
t = bitti()
t = yerlestir(['zincir_kanal'], ['on', 'alt'], t, 'Enerji zinciri kanalı + zemin contası')
t = buyu('guc_kablo', t, 0.8)
if 'evap_kablo' in P: t = buyu('evap_kablo', t - 0.4, 0.8)
olay(t - 0.8, 'Güç (kırmızı) ve evaporatör (mavi) kabloları kanal boyunca çekilir'); t += 0.3
KOL = {}
for ck in CEKD: KOL.setdefault(ck.split('_')[1], []).append(ck)
adim('Tahrik üniteleri', 'Her çekmece için (ön çerçeveden önce): motor braketi önden arka duvara, 2 × DIN 7991 M5 × 6 → arka iç sacdaki PEM SP-M5; step motor (katalog) göbeğiyle braket deliğine, 4 × DIN 7991 M3 × 6; GT3 kasnak mile + DIN 913 M3 × 4 setskur.',
     'motor braketi × 21 + M5 × 6 × 42 · step motor × 21 + M3 × 6 × 84 · kasnak × 21 + setskur × 21')
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
    olay(t, 'Sütun %s: step motor redüktör göbeğiyle braket deliğine (eksen boyunca) · 4 × DIN 7991 M3 × 6 → motor yüzündeki M3 dişler' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_motor_vida'), 0.3, tt=t - 0.2)
    t = bitti() + 0.1
    for ck in KOL[k]: tak(ck + '_kasnak', t, 0.5, 12.0)
    t = bitti()
    for ck in KOL[k]: tak(ck + '_setskur', t, 0.4, 15.0)
    olay(t - 0.5, 'Sütun %s: GT3 motor kasnağı mile (eksen boyunca) · DIN 913 M3 × 4 setskur radyal deliğe' % k)
    if ilk: yakin(merkez(KOL[k][0] + '_kasnak'), 0.3, tt=t - 0.5); ilk = False
    t = bitti() + 0.15
for a in sorted(x for x in P if x.startswith('b_kanal_') and x != 'b_kanal_988'): yerlestir([a], ['on', 'ust'], t, 'Sütun dikey kablo kanalı → iç arka sac (motor rakorlarının yanına)')
t = bitti()
adim('Arka kablo kanalı + gider hortumu', 'Arka kablo kanalı parçaları bölme kovanlarından geçirilerek birleştirilir; evaporatör gider hortumu kanal boyunca çekilir; kablo klipsi.', 'B arka kanal · gider hortumu · klips')
kamera_genel(['b_kanal_988', 'gider_hortumu'], olcek=0.7)
t = buyu('b_kanal_988', t, 1.0); olay(t - 1.0, 'Arka kablo kanalı: parçalar kovanlardan geçirilip birleştirilir (kanal boyunca)')
t = buyu('gider_hortumu', t, 0.8); olay(t - 0.8, 'Gider hortumu kanal boyunca çekilir'); t += 0.2
t = yerlestir(['kablo_klips'], ['on', 'ust'], t, 'Kablo klipsi')
# ---- 11 İÇ TAVAN + ISI KALKANI + TEKNİK KAPAMA (iskelet üst kirişlerinden önce)
adim('İç tavan + ısı kalkanı + teknik kapama', 'Üst köşebentler (1 büküm) yan saclara (punta); iç tavan 1 / 2 bölmelerin üstüne; PU tavan levhaları (kiriş kanalları açık, kesilmiş); fırın üstünde PU tavan, ısı kalkanı U (2 büküm) + ışınım sacı, köşe PU\'ları, 12 PTFE takoz; teknik bölmede ara arka sac ve PU levhalar.',
     'iç tavan × 2 · PU fırın tavanı · ısı kalkanı U · ışınım sacı · PU köşe × 2 · PU B5 üst · takoz × 12 · teknik PU × 4 · ara arka sac')
kamera_genel(['g_ic_tavan_1', 'g_ic_tavan_2', 'g_isi_kalkani_u'], olcek=0.7)
for a in ['g_ic_tavan_1', 'g_ic_tavan_2', 'g_pu_tavan_yuksek', 'g_pu_tavan_topping', 'g_pu_tavan_firin', 'g_pu_isi_kalkani_kose_sol_0', 'g_pu_isi_kalkani_kose_sag_0', 'g_isi_kalkani_u', 'g_isi_kalkani_isinim_08', 'g_pu_b5_ust']:
    t = yerlestir([a], ['ust', 'on'], t, '%s → yerine' % P[a]['ac'])
t = yerlestir(['takozlar'], ['ust', 'on'], t, '12 PTFE takoz → ısı kalkanı üstü')
for a in ['g_tk_ara_arka_sac', 'g_tk_ara_pu', 'depo_arka_sac', 'g_tk_depo_arka_pu', 'g_tk_depo_sag_pu', 'g_tk_depo_tavan_pu', 'depo_ic_sac']:
    t = yerlestir([a], ['ust', 'on', 'sag'], t, '%s → teknik bölme' % P[a]['ac'])
for a in sorted(x for x in SAC if x.startswith('g_kosebent') and '_ust_' in x): yerlestir([a], ['ust', 'on'], t, '%s → yan sac üst köşesi (punta)' % P[a]['ac'])
t = bitti() + 0.2
# ---- 12 MODÜLER İSKELET
adim('Modüler iskelet', '3 ara dikme ve 6 taşıyıcı dikme yukarıdan PU / iç sac boşluklarından GFRP takozlara (dış tabana) iner; arka ve ön merdiven çerçeve (kaynaklı alt montaj) iner, ara dikme başları üst kirişe TIG. Taşıyıcı üst çerçeve dikmelere iner, dikme başları TIG. Üstte GFRP şeritler ve A / K bağlantısı için 8 × M8 perçin somun.',
     'ara dikme × 3 · merdiven çerçeve × 2 (TIG) · taşıyıcı dikme × 6 + üst çerçeve (TIG) · GFRP şerit × 2 · M8 perçin somun × 8')
ISK = ['moduler_cerceve_arka', 'moduler_cerceve_on', 'tasiyici_ust'] + [a for a in P if a.startswith(('moduler_dikme', 'tasiyici_dikme'))]
kamera_genel(ISK, olcek=0.7)
MD = sorted(x for x in P if x.startswith('moduler_dikme'))
for a in MD: yerlestir([a], ['ust'], t, 'Ara dikme → GFRP takoz (dış taban)', sure_bekle=0.05)
TD = sorted(a for a in P if a.startswith('tasiyici_dikme') and HI[a][1] < 750)
for a in TD: yerlestir([a], ['ust'], t, 'Taşıyıcı dikme → dış taban', sure_bekle=0.05)
t = bitti()
t = yerlestir(['moduler_cerceve_arka'], ['ust'], t, 'Arka merdiven çerçeve → GFRP takozlar · ara dikme başı TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_arka'] if x in P])
t = yerlestir(['moduler_cerceve_on'], ['ust'], t, 'Ön merdiven çerçeve → GFRP takozlar · ara dikme başları TIG', grup_kaynak=[x for x in ['kaynak_moduler_dikme_1421_on', 'kaynak_moduler_dikme_2076_on'] if x in P])
yakin(np.array([1436, 753, -110]), 0.4, tt=t - 0.5)
t = yerlestir(['tasiyici_ust', 'tasiyici_dikme_3386_600', 'tasiyici_plaka_-484', 'tasiyici_plaka_-574'], ['ust'], t, 'Taşıyıcı üst çerçeve → dikmelere: dikme başları TIG', grup_kaynak=['kaynak_' + a for a in TD])
for a in ['gfrp_ust_arka', 'gfrp_ust_on']: t = yerlestir([a], ['ust'], t, 'GFRP üst şerit → üst kiriş')
t = tak('percin_ust', t, 0.6, 40.0, 'M8 perçin somun × 12 → üst kirişler (A kaidesi ve K iskeleti cıvataları için)') + 0.3
# ---- 13 TAVAN
adim('Tavan', '3 ek laması; dış tavan 1 / 2 GFRP şeritlerin üstüne (punta); ek yeri silikonu.',
     'ek laması × 3 · dış tavan × 2 · silikon')
kamera_genel(['g_dis_tavan_1', 'g_dis_tavan_2'], olcek=0.7)
for a in ['g_dis_tavan_ek_lamasi_1', 'g_dis_tavan_ek_lamasi_2', 'g_dis_tavan_ek_lamasi_3']: yerlestir([a], ['ust', 'on'], t, '%s (punta)' % P[a]['ac'])
t = bitti()
for a in ['g_dis_tavan_1', 'g_dis_tavan_2']: t = yerlestir([a], ['ust'], t, '%s → GFRP şeritler + köşebentler üstüne (punta)' % P[a]['ac'])
t = buyu('silikon_ek_yeri', t, 0.6); olay(t - 0.6, 'Dış kabuk ek yeri silikonu (taban / arka / tavan)'); t += 0.3
# ---- 14 ÖN ÇERÇEVE
adim('Ön çerçeve + avara üniteleri', '430 ferritik ön çerçeve iki parça (lazer, düz). Tezgâhta: her çekmecenin avara ünitesi (kol + sensör laması + mil + kasnak + reed sensörler, kaynaklı alt montaj; çerçeve ağzından geçmeyecek kadar uzun) ön flanşından çerçevenin arkasına TIG köşe 2 × 8 mm. Çerçeve 1 (K1–K2) ve 2 (K3–K6) avaralarıyla birlikte önden gelir; ek yeri arkadan ek lamasıyla.', 'ön çerçeve 1 / 2 · ek laması · avara ünitesi × 21 · TIG 2 × 8 mm × 21')
kamera_genel(['g_on_cerceve_1', 'g_on_cerceve_2'], yon=(0.3, 0.35, 0.9), olcek=0.7)
t = yerlestir(['g_on_cerceve_ek_lamasi'], ['on'], t, 'Ön çerçeve ek laması → bölme 2 önüne')
for cer, kol in (('g_on_cerceve_1', ('K1', 'K2')), ('g_on_cerceve_2', ('K3', 'K5', 'K6'))):
    av = [ck + '_avara' for ck in sorted(CEKD) if ck.split('_')[1] in kol]; ka = [ck + '_kaynak' for ck in sorted(CEKD) if ck.split('_')[1] in kol]
    t = yerlestir([cer] + av + ka, ['on'], t, '%s + %d avara ünitesi (tezgâhta arkasına TIG) → bölme ve kovan önlerine' % (P[cer]['ac'], len(av)), tezgah_kaynak=ka, kamera_yakin=(cer == 'g_on_cerceve_1'))
t = yerlestir(['g_cerceve_derz_dolgusu'], ['on'], t, 'Ön çerçeve derz dolgu şeridi → çerçeve 1 ↔ 2 arası')
t += 0.3
# ---- 16–18 RAYLAR · TAHRİK · ÇEKMECELER (sütun sütun)
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
adim('Çekmeceler', 'İLK çekmecenin tam montajı (her vida, PEM, kaynak tek tek) ayrı sayfada: "Tek çekmece montajı" (bu sayfanın başındaki bağlantı). Burada 21 çekmece bitmiş alt montaj olarak sütun sütun ray ekseni boyunca 900 mm sürülür; GT3 kayış kasnaklara sarılır; çekmece açılır, kayış çenesi: alt gövde (alttan) + üst çene (yandan) + 2 × ISO 7380 M3 × 12 (üstten) + 2 × ISO 4032 M3 somun (alttan); çekmece kapanır; reed ve motor kabloları kanala çekilir.',
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
    olay(t, 'Kayış çenesi: alt gövde (alttan) → üst çene (yandan, kayışın üstüne) → 2 × ISO 7380 M3 × 12 (üstten: tabla + üst çene + kayış + alt gövde) → 2 × ISO 4032 M3 somun (alttan)')
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
# ---- 19 SOĞUK DEPO + ÖN PANELLER
adim('Soğuk depo + ön paneller', 'Izgara tutucuları, depo rayları ve depo çekmecesi (ön panel + PU + conta) önden; soğutma bölmesinin ön ızgarası; depo önündeki acil stop.',
     'ızgara tutucuları · depo rayları · depo çekmecesi · ön ızgara · acil stop')
kamera_genel(['depo_cekmece', 'sogutma_on_izgara'], yon=(0.4, 0.35, 0.9), olcek=0.8)
t = yerlestir(['izgara_tutucu'], ['on'], t, 'Izgara tutucuları → ön çerçeve')
t = yerlestir(['depo_ray'], ['on'], t, 'Depo sabit rayları')
t = yerlestir(['depo_cekmece'], ['on'], t, 'Depo çekmecesi ray ekseni boyunca')
t = yerlestir(['sogutma_on_izgara'], ['on'], t, 'Soğutma bölmesi ön ızgarası → tutuculara')
t = yerlestir(['acil_stop'], ['on'], t, 'Acil stop → depo ön paneli') + 0.6
kam(t, ([6.0, 2.6, 5.4], [2.57, 0.45, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
eksik = [a for a in P if a not in GOR]
print('süre %.1f s · adım %d · öğe %d · zamanlanmamış %d %s' % (TOPLAM, len(ADIM), len(P), len(eksik), eksik[:20]))
print('PLAN SORUNU', len(PLAN_SORUN)); [print('  ', s) for s in PLAN_SORUN[:60]]
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM, PLAN_SORUN=PLAN_SORUN,
                 CEKD=CEKD, SAC_AD=list(SAC), HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN), open('plan_b3.pkl', 'wb'))
print('%.0f s' % (time.time() - T0))
