# -*- coding: utf-8 -*-
"""A (AÇICI) MONTAJ ANİMASYONU v3 — çekmece v3 / B v3 yöntemiyle (plan_A.md ile birebir) · 4 Eki 2026 · yerel
Girdi: a3_parca.pkl (hat3_v9l + zincir_A_tamamla), acinim_A (sac_morf_a) · Çıktı: plan_a3.pkl → a3_cikti.py (denetim + GLB/JSON)
Her parça kendi YAKLAŞMA ÇİZGİSİNDE belirir: sac → düz açınım (lazer) → bükümler (abkant, sırayla) → PEM preslenir → tek doğru (ya da iki bacak) boyunca yerine.
Yön, plan anında sürekli çarpışma denetimiyle (aday yollar sırayla) seçilir. Kapak: menteşe ekseni (x 736 · z 79) etrafında döner."""
import sys, os, json, pickle, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_a as SM
T0 = time.time()
D0 = pickle.load(open('a3_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']
XA = 736.0
PIV = (0.736, 0.079)            # kapak menteşe ekseni (m) — y ekseni boyunca

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ (son konum = model kutusu ±0,01)
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); SAC[ad] = s
    old = P[ad]
    if s.bukum: V, F = s.dunya(s.yerel({})), s.F
    else: V, F = old['V'], old['F']
    P[ad] = dict(old, V=V, F=F, model_lo=old['V'].min(0), model_hi=old['V'].max(0))
print('sac', len(SAC))

AD_TR = {'kaide_ust_plaka_4': 'Kaide plakası 4 mm', 'kaide_damlama_saci': 'Damlama sacı 1,5', 'sol_yan_sac': 'Sol yan sac 1,5', 'sag_yan_sac_tabla_gecisi': 'Sağ yan sac 1,5 (tabla geçiş ağzı)',
         'ust_sac': 'Üst sac 1,5', 'arka_sac': 'Arka sac 1,5', 'onyuz_kapak_A': 'Kapak dış tava 1,5', 'onyuz_kapak_A_ic_tava': 'Kapak iç tava 1,0',
         'kaide_on_boru': 'Kaide ön boru', 'kaide_arka_boru': 'Kaide arka boru', 'kaide_sol_boru': 'Kaide sol boru', 'kaide_sag_boru': 'Kaide sağ boru',
         'kaide_enine_boru': 'Kaide enine boru', 'kaide_boyuna_boru_sol': 'Kaide boyuna boru (sol)', 'kaide_boyuna_boru_sag': 'Kaide boyuna boru (sağ)',
         'ust_halka_on': 'Üst halka ön', 'ust_halka_arka': 'Üst halka arka', 'ust_halka_sol': 'Üst halka sol', 'ust_halka_sag': 'Üst halka sağ'}
BK = {'arka_donus': 'arka dönüş', 'on_donus': 'ön dönüş', 'alt_donus': 'alt dönüş', 'ust_donus': 'üst dönüş', 'sag_donus': 'sağ dönüş', 'sol_donus': 'sol dönüş', 'kaynak_ayagi': 'kaynak ayağı'}
def bk(x): return BK.get(x, x.replace('_', ' '))
def tr(a):
    if a in AD_TR: return AD_TR[a]
    if a.startswith('kose_dikmesi'):
        p = a.split('_'); yer = ('sol' if p[2] == '20' else 'sağ') + (' ön' if p[3] == '42' else ' arka')
        return ('Dikme tapası 2 mm (%s)' % yer) if a.endswith('_tapa') else ('Köşe dikmesi %s' % yer)
    if a.startswith('govde_kulak'):
        p = a.split('_'); return 'Kulak 3 mm (%s %s, %s)' % ({'sol': 'sol', 'sag': 'sağ', 'ust': 'üst'}[p[2]], {'on': 'ön', 'arka': 'arka'}[p[3]], p[4])
    return tr(a)
CEVRE = [a for a in P if a.startswith('cevre')]
KAPAK = [a for a in P if P[a].get('kpk')]


def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2


def birles_V(adlar):
    VV, FF, n = [], [], 0
    for a in adlar: VV.append(P[a]['V']); FF.append(P[a]['F'] + n); n += len(P[a]['V'])
    return np.vstack(VV), np.vstack(FF)


# PEM / saplama → sac (ince eksen + yön)
def ince(s):
    l, h = kutu(s); return int(np.argmin(h - l))


PEM_SAC = {}
DIS = {'sol_yan_sac': (-1.0, 0, 0), 'sag_yan_sac_tabla_gecisi': (1.0, 0, 0), 'ust_sac': (0, 1.0, 0), 'arka_sac': (0, 0, -1.0),
       'kaide_ust_plaka_4': (0, -1.0, 0), 'onyuz_kapak_A_ic_tava': (0, 0, 1.0)}     # FHP: panelin dış yüz normali · SP: somun gövdesinin tarafı
def pem_bagla(p, s):
    P[p]['sac'] = s; P[p]['yan'] = np.array(DIS[s])          # yan = presleme başlangıç tarafı (FHP dıştan, SP gövde tarafından)
    PEM_SAC.setdefault(s, []).append(p)


for a in list(P):
    if a.startswith('kaide_ust_plaka_pem'): pem_bagla(a, 'kaide_ust_plaka_4')
    elif a.startswith('onyuz_kapak_A_mentese') and '_pem_' in a: pem_bagla(a, 'onyuz_kapak_A_ic_tava')
    elif a.endswith('_saplama'):
        if a.startswith('govde_kulak_sol'): s = 'sol_yan_sac'
        elif a.startswith('govde_kulak_sag'): s = 'sag_yan_sac_tabla_gecisi'
        elif a.startswith('govde_kulak_ust'): s = 'ust_sac'
        else: s = 'arka_sac'
        pem_bagla(a, s)
for a in list(P):
    if a.endswith(('_bag_pul', '_bag_somun')) or (a.startswith('govde_bag_arka') and a.endswith(('_pul', '_somun'))):
        sap = a.rsplit('_', 1)[0] + '_saplama'
        P[a]['eks'] = np.array(DIS[P[sap]['sac']]); P[a]['karsi'] = sap      # içeriden panele doğru
    elif a.startswith('arayuz_ab_'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith(('arayuz_acici', 'arayuz_tabla')): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('arayuz_m8_T'): P[a]['eks'] = np.array([1.0, 0, 0])
    elif a.startswith('kaide_servis_tapasi'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.endswith(('_sabit_vida_a', '_sabit_vida_b')): P[a]['eks'] = np.array([-1.0, 0, 0])
    elif a.endswith(('_kanat_vida_a', '_kanat_vida_b')): P[a]['eks'] = np.array([0, 0, 1.0])
    elif a.endswith('_sabit') or '_basac_' in a: P[a]['eks'] = np.array([0, 0, -1.0])

# ------------------------------------------------------------------ 2. animasyonda üretilen punta işaretleri (modelde yok · 0,1 mm · beyanlı)
def punta(ad, p, eks, ac):
    V, F = G.mesh(G.silindir(p, eks, 2.5, 0.1, 20)); P[ad] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac=ac, uretilen=True)
PUNTA_DAM = []
for x in (40.0, 350.0, 660.0):
    for z in (20.0, -400.0, -780.0):
        ad = 'punta_damlama_%d_%d' % (x, -z); punta(ad, (x + XA, 893.5, z), (0, 1, 0), 'punta: damlama sacı → kaide plakası'); PUNTA_DAM.append(ad)
PUNTA_KAP = []
zp = 59.0 + 1.0 + 7.5
for i, x in enumerate(np.arange(60, 680, 120)):
    ad = 'punta_kapak_alt_%d' % i; punta(ad, (x + XA, 788.0, zp), (0, -1, 0), 'punta: iç tava ↔ dış tava'); PUNTA_KAP.append(ad)
    ad = 'punta_kapak_ust_%d' % i; punta(ad, (x + XA, 2197.0, zp), (0, 1, 0), 'punta: iç tava ↔ dış tava'); PUNTA_KAP.append(ad)
for i, y in enumerate(np.arange(860, 2190, 160)):
    ad = 'punta_kapak_sol_%d' % i; punta(ad, (XA, y, zp), (-1, 0, 0), 'punta: iç tava ↔ dış tava'); PUNTA_KAP.append(ad)
    ad = 'punta_kapak_sag_%d' % i; punta(ad, (XA + 698.5, y, zp), (1, 0, 0), 'punta: iç tava ↔ dış tava'); PUNTA_KAP.append(ad)
PUNTA_KAR = {}
for i, yb in enumerate((1000.0, 1560.0, 2100.0)):
    L = []
    for k, (dx, dy) in enumerate(((-7, -13), (7, 13))):
        ad = 'punta_karsilik_%d_%d' % (i, k); punta(ad, (676.0 + dx + XA, yb + dy, 61.5), (0, 0, 1), 'punta: karşılık plakası → iç tava'); L.append(ad)
    PUNTA_KAR[i] = L
for a in PUNTA_KAP + sum(PUNTA_KAR.values(), []): P[a]['kpk'] = 1
KAPAK = [a for a in P if P[a].get('kpk')]
print('öğe', len(P))

# ------------------------------------------------------------------ 3. zaman çizelgesi altyapısı (b3_montaj ile aynı model)
HAR = {a: [] for a in P}; GOR = {}; MF = {}; FRAMES = {}; VU = {a: [] for a in P}; ISTISNA = set(); ROT = {}
ADIM, OLAY, KAM, ACN = [], [], [], []
CUR = {}; YER = {}
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
YERINDE = []
def buyu(a, t0, sure=0.6):
    basla(a, np.zeros(3), t0); ISTISNA.add(a); MF[a] = dict(buyu=[round(t0, 3), round(t0 + sure, 3)]); VU[a].append([round(t0, 3), round(t0 + sure + 0.8, 3)])
    YER[a] = t0 + sure; YERINDE.append(a)
    return t0 + sure

# ------------------------------------------------------------------ 4. plan anı yol denetimi (b3_montaj.serbest ile aynı)
VEK = {}
def tri(a):
    if a not in VEK: VEK[a] = Y._vekil(P[a]['V'] / 1000.0, np.asarray(P[a]['F']))
    return VEK[a]
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
HARIC_PLAN = set(); HARIC_NEDEN = {}
def serbest(adlar, ofs, yerinde, ofs2=None):
    ofs = np.asarray(ofs, float); ofs2 = np.zeros(3) if ofs2 is None else np.asarray(ofs2, float)
    v = (ofs2 - ofs) / 1000.0; sorun = []
    if np.linalg.norm(v) < 1e-9: return sorun
    for a in adlar:
        A0 = tri(a) + ofs / 1000.0
        l = (np.minimum(LO[a] + ofs2, LO[a] + ofs)) / 1000.0; h = (np.maximum(HI[a] + ofs2, HI[a] + ofs)) / 1000.0
        for b in yerinde:
            if b in adlar or (a, b) in HARIC_PLAN or (b, a) in HARIC_PLAN: continue
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
PLAN_SORUN = []
def YOL(*bacak):
    """bacak: son konuma göre ara noktalar (ilk = başlangıç) · YOL((0,500,0)) = yukarıdan tek doğru · YOL((0,0,300),(0,5,0)) = önden 5 mm yukarıda, sonra iner"""
    pts = [np.asarray(b, float) for b in bacak]
    out = []; acc = np.zeros(3)
    for p in reversed(pts): acc = acc + p; out.append(acc.copy())
    return list(reversed(out)) + [np.zeros(3)]
def yol_sec(adlar, adaylar, denetle=True):
    ilk = None
    for yol in adaylar:
        s = []
        if denetle:
            for p0, p1 in zip(yol[:-1], yol[1:]): s += serbest(adlar, p0, YERINDE, ofs2=p1)
        if ilk is None: ilk = (yol, s)
        if not s: return yol
    PLAN_SORUN.append(dict(parca=list(adlar)[:4], sorun=ilk[1][:4]))
    return ilk[0]

# ------------------------------------------------------------------ 5. yerleştirici (aynı adımdaki bağımsız parçalar alan çakışmazsa paralel)
AKTIF = []
def alan_bos(lo, hi, t0, t1):
    tt = t0
    while True:
        eng = [x for x in AKTIF if x[2] < tt + (t1 - t0) - 1e-6 and x[3] > tt + 1e-6 and np.all(x[0] <= hi + 5) and np.all(x[1] >= lo - 5)]
        if not eng: return tt
        tt = max(x[3] for x in eng)
HIZ = 1000.0
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
def yerlestir(adlar, adaylar, t_min, metin, pem=(), grup_kaynak=(), tezgah_kaynak=(), tezgah_punta=(), sure_bekle=0.15, kamera_yakin=False, denetle=True, ad_ac=None):
    a0 = adlar[0]
    kar = sac_kareleri(a0) if a0 in SAC else None
    yol = yol_sec(list(adlar) + list(pem), adaylar, denetle); ofs = yol[0]
    L = float(sum(np.linalg.norm(b - a) for a, b in zip(yol[:-1], yol[1:])))
    tum = list(adlar) + list(pem)
    lo = np.min([LO[a] for a in tum], 0); hi = np.max([HI[a] for a in tum], 0)
    if kar:
        X = np.vstack([P[a0]['V'] + k for k in kar]); lo = np.minimum(lo, X.min(0)); hi = np.maximum(hi, X.max(0))
    rlo = np.min([lo + p for p in yol], 0); rhi = np.max([hi + p for p in yol], 0)
    sure_uret = 0.0
    if a0 in SAC: sure_uret = 0.45 + len(SAC[a0].bukum) * 0.5 + (0.55 if pem else 0.0)
    if tezgah_kaynak: sure_uret += 0.8
    if tezgah_punta: sure_uret += 0.8
    sure_tasi = max(0.4 * (len(yol) - 1), L / HIZ)
    ts = alan_bos(rlo, rhi, t_min, t_min + sure_uret + sure_bekle + sure_tasi)
    for a in tum: basla(a, ofs, ts)
    tt = ts
    if a0 in SAC:
        s = SAC[a0]; nb = len(s.bukum); acp = ad_ac or tr(a0)
        olay(tt, '%s · LAZER: düz açınım %.0f × %.0f mm (kontur + delikler)' % (acp, s.levha['boy'], s.levha['en']))
        ACN.append(dict(ad=a0, ac=acp, t=s.t, t0=round(tt, 3), t1=round(tt + sure_uret, 3), levha=[s.levha['boy'], s.levha['en']],
                        bukum=[dict(no=b['no'], aci=b['aci'], ack=bk(b['ad'])) for b in sorted(s.bukum, key=lambda b: b['no'])]))
        tt += 0.45
        if kar:
            FRAMES[a0] = kar; seg = []
            for i, b in enumerate(sorted(s.bukum, key=lambda b: b['no'])):
                seg.append([round(tt, 3), round(tt + 0.42, 3), 6 * i, 6 * i + 6])
                olay(tt, '%s · ABKANT büküm %d / %d: %s · %d° · iç R %.2f' % (acp, b['no'], nb, bk(b['ad']), round(b['aci']), b['R']))
                tt += 0.5
            MF[a0] = dict(seg=seg)
        if pem:
            for p in pem:
                e_ = np.asarray(P[p]['yan'], float) * 30.0
                basla(p, ofs + e_, tt); git(p, ofs, tt, 0.45); vurgu([p], tt + 0.3, tt + 1.0)
            import collections as _c
            say = _c.Counter(('PEM SP-M8' if '_M8_' in p else 'PEM SP-M6') if 'plaka_pem' in p else ('PEM FHP-M5-12' if p.startswith('govde_bag_arka') else ('PEM FHP-M5-15' if p.endswith('_saplama') else 'PEM SP-M5')) for p in pem)
            olay(tt, '%s · PEM presleme: %s' % (acp, ' + '.join('%d × %s' % (n, k) for k, n in say.items())))
            tt += 0.55
    if tezgah_kaynak:
        for k_ in tezgah_kaynak:
            basla(k_, ofs, tt); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, 'Havada TIG: %s' % P[tezgah_kaynak[0]]['ac'].split('·')[0].strip()); tt += 0.8
    if tezgah_punta:
        for k_ in tezgah_punta:
            basla(k_, ofs, tt); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, P[tezgah_punta[0]]['ac'] + ' × %d' % len(tezgah_punta)); tt += 0.8
    tt += sure_bekle
    tum2 = tum + list(tezgah_kaynak) + list(tezgah_punta)
    for p0, p1 in zip(yol[:-1], yol[1:]):
        su = max(sure_tasi * float(np.linalg.norm(p1 - p0)) / max(L, 1e-6), 0.3)
        for a in tum2: git(a, CUR[a] + (p1 - p0), tt, su)
        tt += su
    if metin: olay(tt - 0.2, metin)
    vurgu(list(adlar), tt, tt + 1.1)
    for k_ in grup_kaynak: buyu(k_, tt, 0.6)
    for a in tum2: YER[a] = tt
    YERINDE.extend(tum2); YERINDE.extend(grup_kaynak)
    AKTIF.append((rlo, rhi, ts, tt + 0.05))
    if kamera_yakin:
        c = (np.min([LO[a] for a in adlar], 0) + np.max([HI[a] for a in adlar], 0)) / 2000.0
        d = np.array([0.5, 0.45, 0.75]); d /= np.linalg.norm(d)
        kam(ts, ((c + d * 0.9).round(3).tolist(), c.round(3).tolist()))
    return tt
def tak(a, t0, sure=0.5, yol=30.0, metin=None, ofs0=None):
    """bağlantı elemanı kendi ekseninde (P[a]['eks'] = giriş yönü)"""
    e_ = np.asarray(P[a]['eks'], float); o0 = np.zeros(3) if ofs0 is None else np.asarray(ofs0, float)
    basla(a, o0 - e_ * yol, t0); git(a, o0, t0, sure); vurgu([a], t0 + sure * 0.5, t0 + sure + 0.8)
    YER[a] = t0 + sure
    if ofs0 is None: YERINDE.append(a)
    if metin: olay(t0, metin)
    return t0 + sure
def bitti(): return max([YER[a] for a in YER] + [t])
def kamera_genel(adlar, yon=(0.45, 0.5, 0.75), olcek=1.25, tt=None, ofs=None):
    lo = np.min([LO[a] for a in adlar], 0) / 1000.0; hi = np.max([HI[a] for a in adlar], 0) / 1000.0
    c = (lo + hi) / 2 + (0 if ofs is None else np.asarray(ofs, float) / 1000.0); r = float(np.linalg.norm(hi - lo)) * olcek + 0.4
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    kam(t if tt is None else tt, ((c + d * r).round(3).tolist(), c.round(3).tolist()))
def yakin(nokta_mm, uz=0.35, yon=(0.55, 0.42, 0.72), tt=None):
    c = np.asarray(nokta_mm, float) / 1000.0; d = np.asarray(yon, float); d /= np.linalg.norm(d)
    kam(t if tt is None else tt, ((c + d * uz).round(3).tolist(), c.round(3).tolist()))

# ------------------------------------------------------------------ çevre: B (baştan) · TOPPING (hat bağlantısında)
for a in CEVRE:
    if a.startswith('cevre_B'): basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a)
# beyanlı plan istisnaları (son konumda geçme / temas)
for a in [a for a in P if a.startswith('kaide_ust_plaka_pem')]:
    HARIC_PLAN.add((a, 'kaide_ust_plaka_4'))
for a in [a for a in P if a.endswith('_saplama')]: HARIC_PLAN.add((a, P[a]['sac']))

# ================================================================== PLAN (plan_A.md sırası)
KAM.append([0.0, [2.55, 2.35, 2.6], [1.09, 1.2, -0.38]])
t = 0.4
KAIDE_UST = YOL((0, 450, 0))
# ---- 1 KAİDE
adim('Kaide çerçevesi', 'Kaide 304 dikdörtgen borudan (100 × 40 × 2, kesim boyunda) B dolabının tavanı üstünde kurulur: önce ön ve arka boru, sonra aralarına sol, sağ ve enine boru; ortada iki boyuna boru. Her boru ucu karşı boruya iki dikey TIG köşe dikişiyle kaynaklanır (üst / alt alın taşlanır).',
     'ön / arka boru 690 × 2 · sol / sağ / enine boru 792 × 3 · boyuna boru 285 × 2 · TIG köşe dikişi × 20')
kamera_genel(['kaide_on_boru', 'kaide_arka_boru', 'kaide_sol_boru', 'kaide_sag_boru'], yon=(0.45, 0.7, 0.75), olcek=0.75)
for a in ('kaide_on_boru', 'kaide_arka_boru'):
    t = yerlestir([a], [KAIDE_UST], t, '%s (100 × 40 × 2, kesim boyu 690) → B tavanı üstüne' % tr(a), sure_bekle=0.1)
KAY = lambda pre: sorted(k for k in P if k.startswith(pre) and P[k]['tur'] == 'kaynak')
ilk = True
for a in ('kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru'):
    tt = yerlestir([a], [KAIDE_UST], t, '%s ↔ ön + arka boru: uçlarda 4 TIG köşe dikişi' % tr(a), grup_kaynak=KAY(a + '_kaynak'), sure_bekle=0.05)
    if ilk: yakin(merkez('kaide_sol_boru_kaynak_-17_0'), 0.38, yon=(0.5, 0.75, -0.45), tt=tt - 0.3); ilk = False
t = bitti() + 0.2
for a in ('kaide_boyuna_boru_sol', 'kaide_boyuna_boru_sag'):
    yerlestir([a], [KAIDE_UST], t, '%s ↔ yan + enine boru: 4 TIG köşe dikişi' % tr(a), grup_kaynak=KAY(a + '_kaynak'), sure_bekle=0.05)
t = bitti() + 0.5
# ---- 2 PLAKA + DAMLAMA
adim('Kaide plakası + damlama sacı', '4 mm kaide plakası lazerde düz kesilir (A → B Ø16 servis delikleri, delik kaynağı yarıkları, PEM delikleri); altından 4 × PEM SP-M8 (açıcı kolonu) ve 4 × PEM SP-M6 (tabla rayı) preslenir. Plaka borulara iner, 16 yarıktan delik kaynağıyla borulara kaynaklanır (yüz taşlanır). 1,5 mm damlama sacı (dikme çentikli) üstüne iner, 9 punta.',
     'kaide plakası 4 mm · PEM SP-M8 × 4 · PEM SP-M6 × 4 · delik kaynağı × 16 · damlama sacı 1,5 · punta × 9')
kamera_genel(['kaide_ust_plaka_4'], yon=(0.4, 0.8, 0.7), olcek=0.8)
pem_pl = sorted(PEM_SAC['kaide_ust_plaka_4'])
t = yerlestir(['kaide_ust_plaka_4'], [YOL((0, 420, 0))], t, 'Kaide plakası → borular (PEM\'ler altta)', pem=pem_pl, kamera_yakin=False)
yakin(merkez('kaide_ust_plaka_delik_kaynagi_0'), 0.42, yon=(0.35, 0.85, 0.4), tt=t - 0.2)
for k in KAY('kaide_ust_plaka_delik_kaynagi'): buyu(k, t, 0.6)
olay(t, 'Delik kaynağı × 16: plaka yarıkları ↔ kaide boruları (TIG, yüz taşlanır)'); t += 1.0
kamera_genel(['kaide_damlama_saci'], yon=(0.4, 0.8, 0.7), olcek=0.8)
t = yerlestir(['kaide_damlama_saci'], [YOL((0, 380, 0))], t, 'Damlama sacı → kaide plakası üstüne')
for k in PUNTA_DAM: buyu(k, t, 0.5)
olay(t, 'Punta × 9: damlama sacı → kaide plakası'); t += 1.0
# ---- 3 A → B
adim('A → B bağlantısı', '6 × ISO 4762 M8 × 25 + ISO 7092 M8 pul (Ø15) damlama sacı, plaka ve kaide borusu üst duvarındaki Ø16 servis deliğinden iner; baş boru alt duvarına oturur, cıvata B dış tavanı (Ø9), GFRP ped ve B üst kirişindeki M8 perçin somuna girer. Sonra 6 gıda sınıfı silikon tapa Ø16 delikleri kapatır.',
     'ISO 4762 M8 × 25 × 6 · ISO 7092 M8 pul × 6 → B kirişindeki M8 perçin somun · silikon tapa Ø16 × 6')
ABp = sorted(a for a in P if a.startswith('arayuz_ab_') and a.endswith('_pul')); ABv = sorted(a for a in P if a.startswith('arayuz_ab_') and not a.endswith('_pul'))
yakin(merkez(ABv[0]) + np.array([0, 60, 0]), 0.42, tt=t)
for i, (p, v) in enumerate(zip(ABp, ABv)):
    tak(p, t + i * 0.15, 0.6, 130.0); tak(v, t + 0.35 + i * 0.15, 0.7, 140.0)
olay(t, 'Pul ISO 7092 M8 (Ø15) + ISO 4762 M8 × 25: Ø16 servis deliğinden boru içine → boru alt duvarı Ø9 → B dış tavanı → B kirişindeki M8 perçin somun (alyan 6)')
t = bitti() + 0.3
for i, a in enumerate(sorted(a for a in P if a.startswith('kaide_servis_tapasi'))): tak(a, t + i * 0.1, 0.45, 25.0)
olay(t, 'Silikon tapa Ø16 × 6 → plaka + damlama sacı servis delikleri (sıkı geçme, yüzle aynı)'); t = bitti() + 0.5
# ---- 4 İSKELET
adim('İskelet', '4 köşe dikmesi (kare boru 30 × 30 × 2, kesim boyunda; sol ön dikmede menteşe pencereleri + vida delikleri, sağ ön dikmede bas-aç delikleri) damlama sacının çentiklerinden kaide plakasına iner; her biri 2 TIG dikişiyle damlama sacına + plakaya (sızdırmaz). Tepelerine 2 mm tapa (alın kaynağı, taşlanır). Üst halka: ön + arka kuşak, sonra sol + sağ kuşak dikmelerin arasına; uçlarda TIG.',
     'köşe dikmesi × 4 · TIG × 8 · tapa × 4 · üst halka ön / arka / sol / sağ · TIG × 8')
DIK = ['kose_dikmesi_20_42', 'kose_dikmesi_680_42', 'kose_dikmesi_20_-800', 'kose_dikmesi_680_-800']
kamera_genel(DIK + ['kaide_ust_plaka_4'], yon=(0.5, 0.45, 0.8), olcek=0.75)
ilk = True
for a in DIK:
    tt = yerlestir([a], [YOL((0, 1500, 0))], t, '%s → damlama çentiğinden plakaya · 2 TIG (dikme ↔ damlama + plaka)' % tr(a), grup_kaynak=KAY('kaide_damlama_dikme_kaynagi_' + a[len('kose_dikmesi_'):] + '_'), sure_bekle=0.05)
    if ilk: yakin(merkez('kaide_damlama_dikme_kaynagi_20_42_a'), 0.35, tt=tt - 0.4); ilk = False
t = bitti() + 0.2
kamera_genel(DIK, yon=(0.5, 0.6, 0.8), olcek=0.7)
for a in DIK: yerlestir([a + '_tapa'], [YOL((0, 150, 0))], t, 'Tapa 2 mm → dikme tepesi (alın kaynağı, taşlanır)', sure_bekle=0.05)
t = bitti() + 0.2
for a, k in (('ust_halka_on', 'ust_halka_kaynak_-42_'), ('ust_halka_arka', 'ust_halka_kaynak_800_')):
    yerlestir([a], [YOL((0, 300, 0))], t, '%s → dikmelerin arasına · 2 TIG (alt köşe)' % tr(a), grup_kaynak=KAY(k), sure_bekle=0.05)
t = bitti()
yakin(merkez('ust_halka_kaynak_-42_35_0'), 0.35, tt=t - 0.5)
for a, k in (('ust_halka_sol', 'ust_halka_yan_kaynak_20_'), ('ust_halka_sag', 'ust_halka_yan_kaynak_680_')):
    yerlestir([a], [YOL((0, 300, 0))], t, '%s → dikmelerin arasına · 2 TIG (alt köşe)' % tr(a), grup_kaynak=KAY(k), sure_bekle=0.05)
t = bitti() + 0.5
# ---- 5 KULAKLAR
adim('Kulaklar', '22 bağlantı kulağı (3 mm sac): lazerde kesilir, abkantta tek büküm (L); kaynak ayağı dikmenin / üst halkanın iç yüzüne iki TIG dikişiyle. Saplama ayağındaki delik panelin PEM saplamasını alır.',
     'kulak × 22 (yan dikmelerde 16, üst halkada 6) · TIG × 44')
kamera_genel(DIK, yon=(0.55, 0.45, 0.75), olcek=0.7)
KUL = sorted(a for a in SAC if a.startswith('govde_kulak'))
def kulak_yol(a):
    c = merkez(a); s = 1.0 if c[2] < -400 else -1.0          # ön kulak arkadan (−z), arka kulak önden (+z) — kutunun içinden
    return [YOL((0, 0, 120 * s)), YOL((0, 0, 60 * s)), YOL((0, -120, 0)), YOL((0, 120, 0))]
ilk = True
for grp in ('govde_kulak_sol_on', 'govde_kulak_sol_arka', 'govde_kulak_sag_on', 'govde_kulak_sag_arka', 'govde_kulak_ust_on', 'govde_kulak_ust_arka'):
    for a in [x for x in KUL if x.startswith(grp + '_')]:
        tt = yerlestir([a], kulak_yol(a), t, 'Kulak 3 mm → iç yüze · 2 TIG', grup_kaynak=[a + '_kaynak_a', a + '_kaynak_b'], sure_bekle=0.05, ad_ac=tr(a))
        if ilk: yakin(merkez(a), 0.3, tt=tt - 0.4); ilk = False
    t = t + 0.6
t = bitti() + 0.5
# ---- 6–9 PANELLER
def yan_tak(a, t0, vek, sure=0.5):
    """yanal sürme (yarığa): vek = başlangıç ötelemesi"""
    basla(a, np.asarray(vek, float), t0); git(a, np.zeros(3), t0, sure); vurgu([a], t0 + sure * 0.5, t0 + sure + 0.8); YER[a] = t0 + sure; YERINDE.append(a)
    return t0 + sure
def panel(ad, adaylar, baslik, metin, liste, kam_yon, olcek=0.75, somun_once=None):
    global t
    adim(baslik, metin, liste)
    sap = sorted(PEM_SAC[ad])
    if somun_once:
        yakin(merkez('govde_bag_arka_sol_1450_somun'), 0.32, yon=(-0.35, 0.3, -0.9), tt=t)
        for i, s_ in enumerate(sap):
            b = s_.rsplit('_', 1)[0]; v = somun_once(b)
            yan_tak(b + '_pul', t + i * 0.1, v); yan_tak(b + '_somun', t + 0.25 + i * 0.1, v)
        olay(t, '%d × (DIN 9021 M5 pul + ISO 10511 M5 somun) dikme / boru ↔ arka sac yarığına yandan sürülür (SW8 anahtarla tutulur)' % len(sap))
        t = bitti() + 1.0
    kamera_genel([ad], yon=kam_yon, olcek=olcek * 1.3, ofs=adaylar[0][0] * 0.5, tt=t - (0.3 if somun_once else 1.0))
    t = yerlestir([ad], adaylar, t, '%s → saplamalar %s' % (tr(ad), 'yan / üst sac dönüş deliklerinden pul + somuna' if somun_once else 'kulak deliklerine'), pem=sap)
    if not somun_once:
        sk = [x for x in sap if '_arka_' in x][0]
        yakin(merkez(sk), 0.2, yon=tuple(-np.array(DIS[ad]) * 0.7 + np.array([0.0, 0.35, 0.6])), tt=t + 0.2)
        t += 1.2
    else:
        kamera_genel([ad], yon=(0.25, 0.35, 0.95), olcek=0.55, tt=t - 0.2)
    if somun_once:
        vurgu([s_.rsplit('_', 1)[0] + x for s_ in sap for x in ('_pul', '_somun')], t, t + 1.4)
        olay(t, 'Somunlar SW8 ile döndürülür: saplamaya sarılır, sıkılır (arka yüzde vida başı yok)'); t += 1.4
    else:
        for i, s_ in enumerate(sap):
            b = s_.rsplit('_', 1)[0]
            tak(b + '_pul', t + i * 0.12, 0.4, 25.0); tak(b + '_somun', t + 0.3 + i * 0.12, 0.45, 25.0)
        olay(t, '%d × (DIN 9021 M5 pul + ISO 10511 M5 fiberli somun) içeriden → PEM FHP-M5 saplamalara (dışta vida başı yok)' % len(sap))
    t = bitti() + 0.5
panel('sol_yan_sac', [YOL((-700, 0, 0))], 'Sol yan sac', 'Sol yan sac (1,5 mm) lazerde kesilir, abkantta arka (22) ve ön (16,5) iç dönüşleri bükülür, 8 PEM FHP-M5-15 saplama dış yüzden preslenir (baş yüzle aynı). Panel soldan saplama ekseni boyunca gelir, saplamalar kulak deliklerine girer; içeriden pul + fiberli somun.',
      'sol yan sac · 2 büküm · PEM FHP-M5-15 × 8 · DIN 9021 pul × 8 · ISO 10511 somun × 8', (-0.75, 0.4, 0.6))
panel('sag_yan_sac_tabla_gecisi', [YOL((700, 0, 0))], 'Sağ yan sac', 'Sağ yan sac (tabla geçiş ağzı R6, A ↔ TOPPING Ø9 delikleri): lazer → 2 büküm → 8 PEM FHP-M5-15. Sağdan saplama ekseni boyunca gelir; içeriden pul + fiberli somun.',
      'sağ yan sac · 2 büküm · PEM FHP-M5-15 × 8 · pul × 8 · somun × 8', (0.75, 0.4, 0.6))
panel('ust_sac', [YOL((0, 650, 0))], 'Üst sac', 'Üst sac: lazer → ön + arka aşağı dönüş (2 büküm) → 6 PEM FHP-M5-15. Yukarıdan iner, saplamalar üst halka kulaklarına; alttan pul + fiberli somun.',
      'üst sac · 2 büküm · PEM FHP-M5-15 × 6 · pul × 6 · somun × 6', (0.4, 0.85, 0.6))
panel('arka_sac', [YOL((0, 0, -700))], 'Arka sac', 'Arka sac: lazer → alt dönüş (1 büküm, B tavanına oturur) → 13 PEM FHP-M5-12. Önce 13 pul + somun içeriden, dikme / kaide borusu / üst halka ile arka dönüşler arasındaki 13,5 mm yarığa yandan sürülür (saplama dikmenin tam arkasında, eksenden somun takılamaz). Arka sac arkadan gelir; saplamalar yan sacların ve üst sacın arka dönüş deliklerinden pul + somuna girer; somunlar SW8 ile döndürülüp sıkılır.',
      'arka sac · 1 büküm · PEM FHP-M5-12 × 13 · pul × 13 · somun × 13', (0.45, 0.4, -0.8),
      somun_once=lambda b: (50.0, 0, 0) if '_sol_' in b else ((-50.0, 0, 0) if '_sag_' in b else (0, -50.0, 0)))
# ---- 10 AÇICI
adim('Açıcı', 'Satın alınan açıcı (dönme kafası + kolon + motor, TEK ÜRÜN) açık önden 5 mm yukarıda sürülür, kolon flanşı damlama sacına iner. 4 × DIN 125 M8 pul + ISO 4762 M8 × 20: flanş Ø9 → damlama sacı Ø9 → plakanın altındaki PEM SP-M8. A içinden kablo / kanal geçmez.',
     'açıcı (tek ürün) · DIN 125 M8 pul × 4 · ISO 4762 M8 × 20 × 4 → PEM SP-M8')
kamera_genel(['acici', 'acici_kolon'], yon=(0.35, 0.35, 0.9), olcek=1.6)
t = yerlestir(['acici', 'acici_kolon'], [YOL((0, 0, 900), (0, 5, 0)), YOL((0, 0, 900), (0, 8, 0))], t, 'Açıcı → kolon flanşı damlama sacına')
ACp = sorted(a for a in P if a.startswith('arayuz_acici') and a.endswith('_pul')); ACv = sorted(a for a in P if a.startswith('arayuz_acici') and not a.endswith('_pul'))
yakin(merkez(ACv[0]), 0.32, tt=t)
for i, (p, v) in enumerate(zip(ACp, ACv)): tak(p, t + i * 0.15, 0.4, 40.0); tak(v, t + 0.3 + i * 0.15, 0.55, 45.0)
olay(t, 'DIN 125 M8 pul + ISO 4762 M8 × 20 × 4 → kolon flanşı Ø9 → damlama Ø9 → PEM SP-M8 (plaka altı)')
t = bitti() + 0.6
# ---- 11 HAT BAĞLANTISI
adim('Hat bağlantısı (TOPPING)', 'TOPPING (silik) A\'nın sağına gelir. 4 × ISO 4762 M8 × 16 + DIN 9021 pul A İÇİNDEN sağ yan sacın Ø9 deliğinden → TOPPING sol dış sacındaki PEM SP-M8 (TOPPING tarafı PU\'lu, içeriden erişim yok). TOPPING ile gelen tabla rayının taban sacı (silik) tabla geçiş ağzından girer: 4 × ISO 4762 M6 × 16 → ray tabanı Ø6,6 → damlama Ø6,6 → kaide plakasındaki PEM SP-M6.',
     'TOPPING (silik) · DIN 9021 M8 pul × 4 · ISO 4762 M8 × 16 × 4 → PEM SP-M8 · tabla rayı (silik) · ISO 4762 M6 × 16 × 4 → PEM SP-M6')
for a in ('cevre_T_govde', 'cevre_T_pem', 'cevre_T_ray'): basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'TOPPING (silik) A\'nın sağında · tabla rayı tabanı geçiş ağzından')
kamera_genel(['sag_yan_sac_tabla_gecisi', 'cevre_T_ray'], yon=(0.2, 0.45, 0.9), olcek=0.45)
t += 0.8
Tp = sorted(a for a in P if a.startswith('arayuz_m8_T') and a.endswith('_pul')); Tv = sorted(a for a in P if a.startswith('arayuz_m8_T') and not a.endswith('_pul'))
yakin(merkez(Tv[0]), 0.26, yon=(-0.8, 0.25, 0.55), tt=t)
for i, (p, v) in enumerate(zip(Tp, Tv)): tak(p, t + i * 0.15, 0.4, 30.0); tak(v, t + 0.3 + i * 0.15, 0.55, 40.0)
olay(t, 'DIN 9021 M8 pul + ISO 4762 M8 × 16 × 4: A içinden sağ yan sac Ø9 → TOPPING sol dış sacı → PEM SP-M8')
t = bitti() + 0.4
Rv = sorted(a for a in P if a.startswith('arayuz_tabla'))
yakin(merkez(Rv[0]), 0.35, yon=(0.4, 0.75, 0.55), tt=t)
for i, v in enumerate(Rv): tak(v, t + i * 0.15, 0.55, 40.0)
olay(t, 'ISO 4762 M6 × 16 × 4 → tabla rayı tabanı Ø6,6 → damlama Ø6,6 → PEM SP-M6 (kaide plakası)')
t = bitti() + 0.6
# ---- 12 KAPAK ALT MONTAJI + MENTEŞE GÖVDELERİ
adim('Kapak alt montajı + menteşe gövdeleri', 'Kapak havada, A\'nın önünde kurulur: dış tava (1,5) lazer → 4 büküm → köşeler TIG; iç tava (1,0) lazer → 4 büküm → 6 × PEM SP-M5 (menteşe kanatları için); 3 karşılık plakası iç tavaya 2\'şer punta; iç tava dış tavanın içine → 30 punta; 3 menteşe kanadı → 6 × ISO 7380 M5 × 6 → PEM. Dolapta: 3 gizli menteşe gövdesi sol ön dikmenin pencerelerine + 6 × ISO 7380 M5 × 12 içeriden; 3 bas-aç sağ ön dikmenin deliklerine (geçme).',
     'dış tava · 4 büküm · TIG × 4 · iç tava · 4 büküm · PEM SP-M5 × 6 · karşılık × 3 · punta × 36 · menteşe kanadı × 3 + M5 × 6 × 6 · menteşe gövdesi × 3 + M5 × 12 × 6 · bas-aç × 3')
OFK = np.array([0, 30.0, 900.0])          # kapak alt montaj yeri (A'nın önünde, havada)
KAPGRUP = list(KAPAK)
kamera_genel(['onyuz_kapak_A'], yon=(0.35, 0.3, 0.9), olcek=0.95, tt=t - 1.0)
KAM[-1][1] = (np.array(KAM[-1][1]) + OFK / 1000).round(3).tolist(); KAM[-1][2] = (np.array(KAM[-1][2]) + OFK / 1000).round(3).tolist()
KYOL = [YOL(OFK)]
kk = KAY('onyuz_kapak_A_kose_kaynagi')
# dış tava: açınım → büküm → köşe TIG (alt montaj yerinde kalır)
# yerlestir son konumu 0 kabul eder → alt montaj için yolu OFK'da bitir: kendi küçük sürümümüz
def kap_yerlestir(adlar, t0, metin, gelis, pem=(), tk=(), tp=(), yer=None):
    yer = OFK if yer is None else yer
    a0 = adlar[0]; kar = sac_kareleri(a0) if a0 in SAC else None
    tum = list(adlar) + list(pem)
    o_bas = yer + np.asarray(gelis, float)
    for a in tum: basla(a, o_bas, t0)
    tt = t0
    if a0 in SAC:
        s = SAC[a0]; nb = len(s.bukum); su = 0.45 + nb * 0.5 + (0.55 if pem else 0) + (0.8 if tk else 0) + (0.8 if tp else 0)
        olay(tt, '%s · LAZER: düz açınım %.0f × %.0f mm' % (tr(a0), s.levha['boy'], s.levha['en']))
        ACN.append(dict(ad=a0, ac=tr(a0), t=s.t, t0=round(tt, 3), t1=round(tt + su, 3), levha=[s.levha['boy'], s.levha['en']],
                        bukum=[dict(no=b['no'], aci=b['aci'], ack=bk(b['ad'])) for b in sorted(s.bukum, key=lambda b: b['no'])]))
        tt += 0.45
        if kar:
            FRAMES[a0] = kar; seg = []
            for i, b in enumerate(sorted(s.bukum, key=lambda b: b['no'])):
                seg.append([round(tt, 3), round(tt + 0.42, 3), 6 * i, 6 * i + 6])
                olay(tt, '%s · ABKANT büküm %d / %d: %s · %d°' % (tr(a0), b['no'], nb, bk(b['ad']), round(b['aci']))); tt += 0.5
            MF[a0] = dict(seg=seg)
        if pem:
            for p in pem:
                e_ = np.asarray(P[p]['yan'], float) * 30.0; basla(p, o_bas + e_, tt); git(p, o_bas, tt, 0.45); vurgu([p], tt + 0.3, tt + 1.0)
            olay(tt, '%s · PEM presleme: %d × PEM SP-M5-1' % (tr(a0), len(pem))); tt += 0.55
    if tk:
        for k_ in tk: basla(k_, o_bas, tt); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, 'Havada TIG: dış tava köşeleri (bindirme) × %d' % len(tk)); tt += 0.8
    if tp:
        for k_ in tp: basla(k_, o_bas, tt); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(tt, 3), round(tt + 0.6, 3)]); VU[k_].append([round(tt, 3), round(tt + 1.4, 3)])
        olay(tt, '%s × %d' % (P[tp[0]]['ac'], len(tp))); tt += 0.8
    tt += 0.1
    L = float(np.linalg.norm(gelis)); su = max(0.4, L / HIZ)
    for a in tum + list(tk) + list(tp): git(a, yer, tt, su)
    tt += su
    if metin: olay(tt - 0.2, metin)
    vurgu(list(adlar), tt, tt + 1.0)
    return tt
t = kap_yerlestir(['onyuz_kapak_A'], t, 'Dış tava hazır (alt montaj yeri)', (0, 0, 0), tk=kk)
W1 = np.array([0, 0, -260.0])
t = kap_yerlestir(['onyuz_kapak_A_ic_tava'], t, 'İç tava hazır (dış tavanın 260 mm gerisinde)', (0, 0, 0), pem=sorted(PEM_SAC['onyuz_kapak_A_ic_tava']), yer=OFK + W1)
ICT = ['onyuz_kapak_A_ic_tava'] + sorted(PEM_SAC['onyuz_kapak_A_ic_tava'])
for i in range(3):
    a = 'onyuz_kapak_A_karsilik_%d' % i; t_ = t + i * 0.2
    basla(a, OFK + W1 + np.array([0, 0, 110.0]), t_); git(a, OFK + W1, t_, 0.5); vurgu([a], t_ + 0.4, t_ + 1.2)
    for k_ in PUNTA_KAR[i]: basla(k_, OFK + W1, t_ + 0.7); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(t_ + 0.7, 3), round(t_ + 1.2, 3)]); VU[k_].append([round(t_ + 0.7, 3), round(t_ + 1.9, 3)])
olay(t, "Karşılık plakası × 3 → iç tavanın ön yüzü (bas-aç karşısı) · ikişer punta")
t += 1.8
GR = ICT + ['onyuz_kapak_A_karsilik_%d' % i for i in range(3)] + sum(PUNTA_KAR.values(), [])
for a in GR: git(a, OFK, t, 0.8)
olay(t, 'İç tava (karşılıklarla) dış tavanın içine'); t += 0.9
for k_ in PUNTA_KAP: basla(k_, OFK, t); ISTISNA.add(k_); MF[k_] = dict(buyu=[round(t, 3), round(t + 0.6, 3)]); VU[k_].append([round(t, 3), round(t + 1.4, 3)])
olay(t, 'İç tava ↔ dış tava dönüşleri: 30 punta (≈ 150 aralık)'); t += 1.2
yakin(np.array([768, 950, 58]) + OFK, 0.26, yon=(0.5, 0.3, -0.81), tt=t)
for i in range(3):
    a = 'onyuz_kapak_A_mentese_%d_kanat' % i
    basla(a, OFK + np.array([0, 0, -40.0]), t + i * 0.25); git(a, OFK, t + i * 0.25, 0.5); vurgu([a], t + i * 0.25 + 0.4, t + i * 0.25 + 1.2)
    for k, v in enumerate(('a', 'b')): tak('onyuz_kapak_A_mentese_%d_kanat_vida_%s' % (i, v), t + 0.6 + i * 0.25 + k * 0.12, 0.4, 20.0, ofs0=OFK)
olay(t, 'Menteşe kanadı × 3 → iç tava arka yüzü · 2\'şer ISO 7380 M5 × 6 → PEM SP-M5')
t = t + 1.8
# dolap tarafı: menteşe gövdeleri + vidalar · bas-aç
yakin(np.array([760, 1500, 44]), 0.45, yon=(0.55, 0.3, 0.75), tt=t)
for i in range(3):
    tak('onyuz_kapak_A_mentese_%d_sabit' % i, t + i * 0.25, 0.5, 60.0)
    for k, v in enumerate(('a', 'b')): tak('onyuz_kapak_A_mentese_%d_sabit_vida_%s' % (i, v), t + 0.7 + i * 0.25 + k * 0.12, 0.45, 25.0)
olay(t, 'Gizli menteşe gövdesi × 3 → sol ön dikmenin ön penceresine · 2\'şer ISO 7380 M5 × 12 içeriden (dikme iç yan duvarı → gövde dişi)')
t = bitti() + 0.3
yakin(np.array([1412, 1560, 50]), 0.45, yon=(-0.4, 0.3, 0.85), tt=t)
for i in range(3): tak('onyuz_kapak_A_basac_%d' % i, t + i * 0.2, 0.45, 40.0)
olay(t, 'Bas-aç × 3 → sağ ön dikmenin Ø12,2 deliklerine (geçme, O-ring)')
t = bitti() + 0.5
# ---- 13 KAPAK TAKILIR (menteşe tarafından)
adim('Kapak takılır', 'Kapak alt montajı havada 90° açılır, menteşe tarafından dolaba yaklaşır, kanatlar gövdelere yukarıdan iner (kaldır-çıkar menteşe); kapak kapanır, bas-aç mandalları karşılık plakalarına kilitlenir.',
     'kapak alt montajı · 3 gizli menteşe · 3 bas-aç')
kam(t, ([-1.25, 2.55, 3.35], [0.95, 1.45, 0.75]))
t0k = t; s_ac = 1.2; DY = 25.0
for a in KAPGRUP:
    if a not in GOR: raise SystemExit('kapak parçası zamanlanmamış: %s' % a)
    ROT[a] = [[round(t0k, 3), round(t0k + s_ac, 3), -90.0, PIV[0], PIV[1]]]
olay(t0k, 'Kapak havada 90° açılır (menteşe ekseni sol ön köşe)')
t1 = t0k + s_ac + 0.1
for a in KAPGRUP: git(a, np.array([0, DY, 0]), t1, 1.0)
olay(t1, 'Menteşe tarafından dolaba yaklaşır')
t2 = t1 + 1.1
for a in KAPGRUP: git(a, np.zeros(3), t2, 0.5)
olay(t2, 'Kanatlar gövdelerin pimine yukarıdan iner (kaldır-çıkar)')
t3 = t2 + 0.7
for a in KAPGRUP: ROT[a].append([round(t3, 3), round(t3 + 1.4, 3), 90.0, PIV[0], PIV[1]])
for a in KAPGRUP: ROT[a].append([round(t0k, 3), round(t3 + 1.4, 3), 0.0, PIV[0], PIV[1]])        # denetim: bu aralık poz-poz (dönme dahil) denetlensin
olay(t3, 'Kapak kapanır · bas-aç mandalları karşılık plakalarına kilitlenir')
kam(t2 - 0.3, ([-0.35, 2.0, 1.75], [0.85, 1.45, 0.1]))
vurgu(['onyuz_kapak_A_basac_0', 'onyuz_kapak_A_basac_1', 'onyuz_kapak_A_basac_2'] + ['onyuz_kapak_A_mentese_%d_kanat' % i for i in range(3)], t3 + 1.2, t3 + 2.2)
t = t3 + 1.4
for a in KAPGRUP: YER[a] = t; YERINDE.append(a)
t += 0.8
kam(t, ([2.45, 2.1, 2.75], [1.09, 1.35, -0.38]))
TOPLAM = round(bitti() + 2.0, 3)
# ---- zaman ölçeği (izlenebilir hız): bütün zamanlar × OLC
OLC = 1.75
def _o(x): return round(x * OLC, 3)
for a in HAR: HAR[a] = [[_o(h[0]), _o(h[1])] + h[2:] for h in HAR[a]]
for a in GOR: GOR[a] = _o(GOR[a])
for a in MF:
    if 'seg' in MF[a]: MF[a]['seg'] = [[_o(x[0]), _o(x[1]), x[2], x[3]] for x in MF[a]['seg']]
    if 'buyu' in MF[a]: MF[a]['buyu'] = [_o(MF[a]['buyu'][0]), _o(MF[a]['buyu'][1])]
for a in VU: VU[a] = [[_o(v[0]), _o(v[1])] for v in VU[a]]
for x in ADIM: x['t0'] = _o(x['t0'])
OLAY = [[_o(o[0]), o[1]] for o in OLAY]
KAM = [[_o(k[0]), k[1], k[2]] for k in KAM]
for x in ACN: x['t0'] = _o(x['t0']); x['t1'] = _o(x['t1'])
for a in ROT: ROT[a] = [[_o(r[0]), _o(r[1])] + r[2:] for r in ROT[a]]
TOPLAM = _o(TOPLAM)
eksik = [a for a in P if a not in GOR]
print('süre %.1f s · adım %d · öğe %d · zamanlanmamış %d %s' % (TOPLAM, len(ADIM), len(P), len(eksik), eksik[:20]))
print('PLAN SORUNU', len(PLAN_SORUN)); [print('  ', s) for s in PLAN_SORUN[:60]]
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ROT=ROT, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM, PLAN_SORUN=PLAN_SORUN,
                 SAC_AD=list(SAC), CEVRE=CEVRE, KAPAK=KAPGRUP, HARIC_PLAN=sorted(HARIC_PLAN), HARIC_NEDEN=HARIC_NEDEN), open('plan_a3.pkl', 'wb'))
print('%.0f s' % (time.time() - T0))
