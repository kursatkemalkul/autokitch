# -*- coding: utf-8 -*-
"""m8c adım 2: kablo / hortum / boru denetimi (SALT OKUMA). Girdi: _kay.pkl (kablo_cikar.py) + ortam.py. Çıktı: _bulgu.pkl"""
import sys, os, pickle, math, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ortam as O
G = O.G
KAY = pickle.load(open(os.path.join(HERE, '_kay.pkl'), 'rb'))
for d in KAY:
    d['aktif'] = not (d['base'] in ('ROBOT_KABLOSU', 'ROBOT_ENERJI_ZINCIRI') and d['Ls'] < 60) and d['base'] != 'ROBOT_ENERJI_ZINCIRI' and d['Ls'] >= 2
    d['tup'] = d['aktif'] and d['ntri'] > 12
LINK = {(d['pid'], d['comp']): d for d in KAY}
LINSET = np.array(sorted(p * 1000000 + c for p, c in LINK))


def is_lin(own): return np.isin(own[:, 0] * 1000000 + own[:, 1], LINSET)


def mat(pid):
    n = G.prims[pid]['name']; return n.split('__')[1] if '__' in n else ''


def base(pid): return G.prims[pid]['name'].split('__')[0]


def P2(v): return [round(float(x), 1) for x in v]


# ---------- kanal / oluk kutuları
KANAL = []
for pid, (tl, kut) in O.KOMP.items():
    if mat(pid) == 'kanal' or base(pid) in ('ELK_ZEMIN_KANALI', 'ROBOT_ZINCIR_OLUGU', 'ROBOT_ENERJI_ZINCIRI'):
        for c, (lo, hi, n) in kut.items(): KANAL.append((O.ad(pid, c), lo, hi))
print('kanal', len(KANAL))


def kanalda(p, e=1.0):
    for a, lo, hi in KANAL:
        if (p >= lo - e).all() and (p <= hi + e).all(): return a
    return None


# ---------- kelepçe adayları
KEL = []
for pid, (tl, kut) in O.KOMP.items():
    b = base(pid); m = mat(pid)
    if not (b.startswith('ELK_') or b in ('K_YAG', 'K_ELEKTRIK', 'ROBOT_KABLOSU', 'ROBOT_KABLO_KOPRUSU', 'HAVA_KOMPRESOR', 'B_KABLO')): continue
    if m not in ('celik', 'paslanmaz', 'plastik'): continue
    for c, (lo, hi, n) in kut.items():
        if (hi - lo).max() < 45 and n < 2000:
            KEL.append(dict(pid=pid, c=c, lo=lo, hi=hi, n=n))
KELSET = np.array(sorted(q['pid'] * 1000000 + q['c'] for q in KEL))
print('kelepce adayi', len(KEL))

# ---------- rakor / geçiş elemanları
RAK = []
for pid, (tl, kut) in O.KOMP.items():
    m = mat(pid)
    for c, (lo, hi, n) in kut.items():
        if m == 'rakor':
            RAK.append(dict(pid=pid, c=c, lo=lo, hi=hi, ad=O.ad(pid, c)))
        elif m in ('conta', 'silikon', 'koyu', 'plastik', 'pom', 'paslanmaz') and (hi - lo).max() < 80:
            a = O.ad(pid, c)
            if re.search(r'rakor|kovan|lastik|bilezik|gecis|grommet', a, re.I):
                RAK.append(dict(pid=pid, c=c, lo=lo, hi=hi, ad=a))
print('rakor/gecis', len(RAK))


def seg_dist(p, A, Bq):
    d = Bq - A; L2 = (d * d).sum(1); t = np.clip(((p - A) * d).sum(1) / np.maximum(L2, 1e-9), 0, 1)
    Q = A + t[:, None] * d; return np.linalg.norm(Q - p, axis=1), t


SEGS = []
for k, d in enumerate(KAY):
    for i, q in enumerate(d['S']): SEGS.append((k, i, q['a'], q['b']))
SA = np.array([s[2] for s in SEGS]); SB = np.array([s[3] for s in SEGS]); SK = np.array([s[0] for s in SEGS])

B = []


def bul(tur, d, konum, aciklama, oneri, agirlik=2, **ek):
    B.append(dict(tur=tur, dugum=d['prim'] if d else ek.pop('dugum', ''), parca=(d['ad'] or d['id']) if d else ek.pop('parca', ''),
                  bilesen=d['id'] if d else ek.pop('bilesen', ''),
                  istasyon=d['ist'] if d else ek.pop('istasyon', ''), konum_mm=P2(konum) if konum is not None else None,
                  aciklama=aciklama, oneri=oneri, agirlik=agirlik, **ek))


def own_h(own):
    return lambda o: (o[:, 0] == own[0]) & (o[:, 1] == own[1])


# =============================== 1 · SÜREKLİLİK (serbest uçlar)
for d in KAY:
    if not d['tup']: continue
    own = (d['pid'], d['comp'])
    d['uc_ad'] = []
    for ui, (E, v, r, si, *_x) in enumerate(d['uclar']):
        pr = E + v * (r * 0.6)
        h = O.en_yakin(pr, r + 4.0, haric=own_h(own))
        if h is None:
            # serit çıkarımının kaçırdığı kısa uç parçası var mı? (kendi köşeleri, segment eksenlerinden uzak)
            p_ = G.prims[d['pid']]; V = np.unique(p_['X'][p_['T'][d['tri_idx']]].reshape(-1, 3), axis=0)
            V = V[np.linalg.norm(V - E, axis=1) < r + 40]
            ac = np.ones(len(V), bool)
            for w in d['S']:
                dv = w['b'] - w['a']; L2 = max(dv @ dv, 1e-9); t = np.clip((V - w['a']) @ dv / L2, 0, 1)
                ac &= np.linalg.norm(w['a'] + t[:, None] * dv - V, axis=1) > w['r'] * 1.5 + 1.0
            if ac.any():
                far = V[ac][np.argmax(np.linalg.norm(V[ac] - E, axis=1))]
                h = O.en_yakin(far, r + 4.0, haric=own_h(own))
                if h is not None: E = far
        if h is None:
            h2 = O.en_yakin(E, r + 30.0, haric=own_h(own))
            yak = ("en yakın %.0f mm: %s" % (h2[0], O.ad(*O.OWN[h2[1]]))) if h2 else "30 mm içinde hiçbir şey yok"
            d['uc_ad'].append(None)
            bul('sureklilik/bosta_uc', d, E, "serbest uç boşta (uç yönü %s): uç yüzünün önünde r+4 mm içinde cihaz / kanal / rakor yok · %s" % (P2(v), yak),
                "ucu bağlı olması gereken cihaz yüzüne / kanal parmak yuvasına uzat ya da cihaz taşındıysa yolu yeniden çek", 3)
        else:
            d['uc_ad'].append(O.ad(*O.OWN[h[1]]))
print('uclar tamam')

# =============================== 2 · GEÇİŞLER
GEC = {}
for d in KAY:
    if not d['tup']: continue
    own = (d['pid'], d['comp'])
    serb = {(int(si), int(np.linalg.norm(E - d['S'][si]['a']) > np.linalg.norm(E - d['S'][si]['b']))) for E, v, r, si, *_x in d['uclar']}
    for i, q in enumerate(d['S']):
        a, b = q['a'].copy(), q['b'].copy(); L = np.linalg.norm(b - a); r = q['r']
        if L < 1e-6: continue
        u = (b - a) / L
        if (i, 0) in serb: a = a + u * min(2.0 + r, L / 2)
        if (i, 1) in serb: b = b - u * min(2.0 + r, L / 2)
        for t, tri in O.seg_kesis(a, b, haric=own_h(own)):
            o = O.OWN[tri]; key = (d['id'], int(o[0]), int(o[1]))
            p = a + t * (b - a)
            if key not in GEC: GEC[key] = [d, p, 1]
            else: GEC[key][2] += 1
print('gecis vurus', len(GEC))
SACMAT = ('sac', 'paslanmaz', 'pu', 'yalitim', 'celik', 'aluminyum', 'plastik', 'kabuk', 'qr_govde', 'pano', 'conta', 'silikon', 'koyu', 'yalitim_gorunur', 'on_seffaf', 'pom', 'kanal', 'din', 'cihaz', 'cihaz_koyu', 'motor', 'sensor')
for (cid, pid, c), (d, p, nh) in GEC.items():
    a = O.ad(pid, c); m = mat(pid)
    if (pid, c) in LINK:
        d2 = LINK[(pid, c)]
        if d['id'] < d2['id']:
            bul('gecis/kablo_kablo', d, p, "kablo eksenini başka kablo / hortum kesiyor: %s" % (d2['ad'] or d2['id']),
                "kesişme noktasında birini ≥ (r1 + r2 + 2) mm kaydır ya da ikisini aynı demete al", 2, karsi=d2['id'])
        continue
    if np.isin(pid * 1000000 + c, KELSET):
        bul('gecis/kelepce', d, p, "kablo ekseni küçük çelik / kelepçe parçasından geçiyor: %s" % a, "kelepçeyi kablonun yeni eksenine al ya da sil", 2)
        continue
    rk = [k for k in RAK if (p >= k['lo'] - (d['r'] + 15)).all() and (p <= k['hi'] + (d['r'] + 15)).all() and not (k['pid'] == pid and k['c'] == c)]
    if m == 'rakor' or re.search('rakor|kovan|lastik', a):
        bul('gecis/rakor_tikali', d, p, "kablo rakor / kovan gövdesini kesiyor (rakor ekseni kabloyla çakışmıyor): %s" % a,
            "rakoru kablo eksenine ortala (ya da kabloyu rakor eksenine kaydır)", 2)
    elif rk:
        bul('gecis/rakor_var_delik_yok', d, p, "kablo %s'i kesiyor; yakında rakor / geçiş var (%s) ama bu katıda delik yok" % (a, rk[0]['ad']),
            "rakor ekseninde bu parçada Ø(rakor boynu + 0,5) delik aç", 2)
    else:
        bul('gecis/deliksiz', d, p, "kablo %s içinden deliksiz + rakorsuz geçiyor (%d vuruş)" % (a, nh),
            "yolu bu parçanın etrafından dik açılı çek ya da geçiş noktasında IP68 rakor + delik ekle", 3 if m in SACMAT else 2)
print('gecis tamam')

# =============================== 2b · gömülü / sürtünen
GOM = {}
for d in KAY:
    if not d['tup']: continue
    own = (d['pid'], d['comp'])
    hf = lambda o, own=own: ((o[:, 0] == own[0]) & (o[:, 1] == own[1])) | is_lin(o)
    UC = [E for E, v, r, si, *_x in d['uclar']]
    for q_ in d['S']:
        a, b = q_['a'], q_['b']; Ls = np.linalg.norm(b - a); r = q_['r']
        if Ls < 1e-6: continue
        k = max(1, int(Ls / 5.0))
        for j in range(k + 1):
            q = a + (b - a) * j / k
            if any(np.linalg.norm(q - E) < 2 * r + 4 for E in UC): continue
            h = O.en_yakin(q, 0.55 * r, haric=hf)
            if h is None: continue
            o = O.OWN[h[1]]; key = (d['id'], int(o[0]), int(o[1]))
            if key not in GOM: GOM[key] = [d, q, 0, h[0]]
            GOM[key][2] += 1; GOM[key][3] = min(GOM[key][3], h[0])
for (cid, pid, c), (d, q, n, dm) in GOM.items():
    if (cid, pid, c) in GEC: continue
    if np.isin(pid * 1000000 + c, KELSET): continue
    a = O.ad(pid, c)
    bul('gecis/gomulu', d, q, "kablo %s'e gömülü / sürtünüyor (~%d mm boyunca eksenden %.1f mm'de katı yüzey, r %.1f)" % (a, n * 5, dm, d['r']),
        "kabloyu yüzeyden r + 0,5 mm uzaklaştır (yüzeye dayalı, içine girmeyen)", 2)
print('gomulu tamam')

# =============================== 3 · TUTUCULAR
SR = np.array([KAY[s_[0]]['S'][s_[1]]['r'] for s_ in SEGS])
for k in KEL:
    cen = (k['lo'] + k['hi']) / 2
    own = (k['pid'], k['c'])
    tl, kut = O.KOMP[k['pid']]
    p = G.prims[k['pid']]; m = (tl == k['c']) & G.gorunur(p)
    V = np.unique(p['X'][p['T'][m]].reshape(-1, 3), axis=0)
    if len(V) > 120: V = V[np.linspace(0, len(V) - 1, 120).astype(int)]
    best = (1e9, None)
    near = np.where(np.all((np.minimum(SA, SB) <= k['hi'] + 30) & (np.maximum(SA, SB) >= k['lo'] - 30), axis=1))[0]
    for j in near:
        dd, _ = seg_dist(V, np.repeat(SA[j][None], len(V), 0), np.repeat(SB[j][None], len(V), 0))
        g = dd.min() - SR[j]
        if g < best[0]: best = (g, j)
    if best[1] is None:
        dd, t = seg_dist(cen, SA, SB); j = int(np.argmin(dd)); best = (dd[j], j)
    dk = KAY[SK[best[1]]]
    k['kablo'] = dk['id'] if best[0] < 2.0 else None
    k['kd'] = float(best[0]); k['yakin_kablo'] = dk['id']
    dd = [best[0] + SR[best[1]]]; j = 0
    temas = None
    hf = lambda o, own=own: ((o[:, 0] == own[0]) & (o[:, 1] == own[1])) | is_lin(o) | np.isin(o[:, 0] * 1000000 + o[:, 1], KELSET)
    for v in V:
        h = O.en_yakin(v, 0.8, haric=hf)
        if h is not None: temas = O.ad(*O.OWN[h[1]]); break
    k['temas'] = temas
    nm = O.ad(k['pid'], k['c']); k['ad'] = nm
    if k['kablo'] is None and re.search('kelepce|aski|klips|kablo_bag', nm, re.I):
        bul('tutucu/kablosuz_kelepce', None, cen, "kelepçe kablosuz: halkası hiçbir kabloyu sarmıyor, en yakın kablo yüzeyi %.0f mm (%s)" % (k['kd'], dk['ad'] or dk['id']),
            "kablo taşındıysa kelepçeyi yeni yoluna taşı, değilse sil", 3, dugum=p['name'], parca=nm, istasyon=dk['ist'], bilesen='%s#%d' % (p['name'], k['c']))
    elif k['kablo'] is None and temas is None:
        bul('tutucu/havada_kucuk_parca', None, cen, "küçük çelik/plastik parça hiçbir şeye değmiyor ve kabloya da ait değil (en yakın kablo yüzeyi %.0f mm: %s)" % (k['kd'], dk['ad'] or dk['id']),
            "sahipsiz parça: kablo taşınmasından artık kaldıysa sil", 2, dugum=p['name'], parca=nm, istasyon=dk['ist'], bilesen='%s#%d' % (p['name'], k['c']))
    elif k['kablo'] is not None and temas is None:
        bul('tutucu/havada_kelepce', None, cen, "kelepçe kabloyu tutuyor ama hiçbir sac / gövdeye değmiyor (0,8 mm içinde yüzey yok) · kablo %s" % (dk['ad'] or dk['id']),
            "kelepçe dilini en yakın sac yüzüne uzat (M4 vida / perçin somunu) ya da kabloyu yüzeye yasla", 3, dugum=p['name'], parca=nm, istasyon=dk['ist'], bilesen='%s#%d' % (p['name'], k['c']))
print('kelepce tamam')

# =============================== 3b · boş rakor
for k in RAK:
    cen = (k['lo'] + k['hi']) / 2; ext = (k['hi'] - k['lo']).max() / 2
    dd, t = seg_dist(cen, SA, SB)
    j = int(np.argmin(dd))
    if dd[j] > ext + 2:
        dk = KAY[SK[j]]
        if not re.search('rakor|lastik|bilezik|G\\d|kablo', k['ad'], re.I): continue
        bul('gecis/bos_rakor', None, cen, "rakor / geçiş elemanından kablo/hortum geçmiyor (en yakın eksen %.0f mm: %s)" % (dd[j], dk['ad'] or dk['id']),
            "kabloyu rakor ekseninden geçir ya da rakor + deliği kaldır (kablo taşındıysa yeni geçiş noktasına al)", 2,
            dugum=G.prims[k['pid']]['name'], parca=k['ad'], istasyon=dk['ist'], bilesen='%s#%d' % (G.prims[k['pid']]['name'], k['c']))
print('rakor tamam')

# =============================== 4 · DAĞINIKLIK
for d in KAY:
    if not d['tup']: continue
    for q in d['S']:
        v = q['b'] - q['a']; L = np.linalg.norm(v)
        if L < max(15.0, 4 * q['r']): continue
        c = np.abs(v / L).max(); ang = math.degrees(math.acos(min(1.0, c)))
        if ang > 3:
            ax = int(np.argmax(np.abs(v)))
            kose = [q['b'][k_] if k_ == ax else q['a'][k_] for k_ in range(3)]
            bul('daginik/egik', d, (q['a'] + q['b']) / 2, "eğik segment %.0f mm, en yakın eksenden %.0f° sapma (%s → %s)" % (L, ang, P2(q['a']), P2(q['b'])),
                "dik açılı böl: %s → köşe %s → %s" % (P2(q['a']), P2(kose), P2(q['b'])), 1)
    if len(d['uclar']) == 2:
        man = np.abs(d['uclar'][0][0] - d['uclar'][1][0]).sum()
        if d['Ls'] > 300 and man > 1 and d['Ls'] / man > 1.6:
            bul('daginik/dolasan', d, d['uclar'][0][0], "yol %.0f mm, uçlar arası dik mesafe toplamı %.0f mm (oran %.1f) · %d segment" % (d['Ls'], man, d['Ls'] / man, len(d['S'])),
                "uçlar arasında en çok 3 köşeli dik yol dene; engel nedeniyle dolaşıyorsa ortak kanaldan geçir", 1)
    acik = 0.0; parca = []
    for q in d['S']:
        L = np.linalg.norm(q['b'] - q['a'])
        if L < 1: continue
        if kanalda((q['a'] + q['b']) / 2) is None:
            acik += L
            if L > 250: parca.append((P2(q['a']), P2(q['b']), int(round(L))))
    d['acik'] = acik
    if parca:
        kel = [k for k in KEL if k.get('kablo') == d['id']]
        bul('daginik/acik_uzun', d, (d['S'][0]['a'] + d['S'][0]['b']) / 2, "kanal dışında açıkta toplam %.0f mm · ≥250 mm açık parçalar: %s · kelepçe %d" % (acik, parca[:5], len(kel)),
            "istasyonun ortak kanalına al ya da her ≤250 mm'de duvar kelepçesi", 1, kelepce=len(kel))

PAR = {}
n = len(SEGS)
for i in range(n):
    ki, si, a, b = SEGS[i]; di = KAY[ki]
    if not di['tup']: continue
    v = b - a; L = np.linalg.norm(v)
    if L < 120: continue
    ax = int(np.argmax(np.abs(v)))
    if np.abs(v / L)[ax] < 0.99: continue
    oth = [q for q in range(3) if q != ax]
    for j in range(i + 1, n):
        kj, sj, c, e = SEGS[j]
        if kj == ki: continue
        dj = KAY[kj]
        if not dj['tup'] or dj['base'] != di['base'] and not (di['base'].startswith('ELK') and dj['base'].startswith('ELK')): continue
        w = e - c; Lw = np.linalg.norm(w)
        if Lw < 120 or np.abs(w / Lw)[ax] < 0.99: continue
        lat = np.linalg.norm(((a + b) / 2)[oth] - ((c + e) / 2)[oth])
        if lat > 50 or lat < di['S'][si]['r'] + dj['S'][sj]['r'] + 0.5: continue
        lo = max(min(a[ax], b[ax]), min(c[ax], e[ax])); hi = min(max(a[ax], b[ax]), max(c[ax], e[ax]))
        if hi - lo < 120: continue
        m1 = (a + b) / 2 + (c + e) / 2; m1 = m1 / 2; m1[ax] = (lo + hi) / 2
        if kanalda(m1) is not None: continue
        key = tuple(sorted((di['id'], dj['id'])))
        if key not in PAR or PAR[key][0] < hi - lo:
            PAR[key] = (hi - lo, lat, "xyz"[ax], m1, di, dj, lo, hi)
print('paralel cift', len(PAR))
for key, (ov, lat, ax, m1, di, dj, lo, hi) in PAR.items():
    bul('daginik/paralel', di, m1, "%s ile %s ekseninde %.0f mm boyunca (%s %.0f–%.0f), yanal %.0f mm arayla AYRI gidiyor" % (dj['ad'] or dj['id'], ax, ov, ax, lo, hi, lat),
        "aynı kelepçe sırasında tek demet yap (spiral sargı / ortak P-kelepçe): ortak eksen %s, yanal konum %s" % (ax, P2(m1)), 1, karsi=dj['id'])

pickle.dump(dict(B=B, KAY=[{k: v for k, v in d.items() if k != 'tri_idx'} for d in KAY],
                 KEL=KEL, RAK=RAK, KANAL=KANAL), open(os.path.join(HERE, '_bulgu.pkl'), 'wb'))
print(collections.Counter(b['tur'] for b in B))
