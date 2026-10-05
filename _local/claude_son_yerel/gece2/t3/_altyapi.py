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
        if ilk is None: ilk = (yol, s); tum = []
        tum.append((np.round(yol[0]).tolist(), sorted(set(b for a_, b in s))[:3]))
        if not s: return yol
    PLAN_SORUN.append(dict(parca=list(adlar)[:4], sorun=ilk[1][:4], tum=tum[:8]))
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
            say = _c.Counter(P[p]['pem_ad'] for p in pem)
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

