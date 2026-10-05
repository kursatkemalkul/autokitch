# -*- coding: utf-8 -*-
"""yol çakışması olan hareket gruplarına gerçekçi yön arar (g6_montaj.py içinden çağrılır).
Grup = aynı hareket listesine sahip parçalar (aynı gel() çağrısı). Adaylar sırayla: özgün yön → yukarıdan → önden → arkadan → yanlardan →
iki aşamalı yol (açık taraftan yaklaş + kısa son oturma) → kısa yaklaşma. Bağlantı elemanları (vida, pul, somun, saplama) YALNIZ kendi
eksenlerinde (iki işaret, kısa boylar)."""
import re, json
import numpy as np
import yol_denetim as Y

YON = {'ust': (0, 1, 0), 'on': (0, 0, 1), 'arka': (0, 0, -1), 'sol': (-1, 0, 0), 'sag': (1, 0, 0), 'alt': (0, -1, 0)}
YON_METIN = {'ust': 'yukarıdan indirilir', 'on': 'önden', 'arka': 'arkadan', 'sol': 'soldan', 'sag': 'sağdan', 'alt': 'alttan'}
BAG_RX = r'(vida|civata|cıvata|somun|_pul|pul_|saplama|_pem|pem_|percin|perçin|arayuz_|_bolt|_M\d)'


def bag_mi(P, a):
    return P[a]['tur'] in ('baglanti', 'arayuz') or bool(re.search(BAG_RX, a, re.I))


def eksen(P, a):
    V = P[a]['V']; w = V.max(0) - V.min(0)
    if re.search(r'(pul|somun|washer|nut)', a, re.I): return int(np.argmin(w))
    return int(np.argmax(w))


def gel_indeks(HAR, GOR, a):
    for i, h in enumerate(HAR[a]):
        if abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 and abs(h[0] - GOR[a]) < 1e-6: return i
    for i, h in enumerate(HAR[a]):
        if abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9: return i
    return None


def adaylar(P, grup, d0):
    m0 = float(np.linalg.norm(d0)); m = max(m0, 0.3)
    out = []
    if all(bag_mi(P, a) for a in grup):
        ax = eksen(P, grup[0]); 
        for L in (max(m0, 0.04), 0.06, 0.03, 0.015):
            for sg in (1, -1):
                v = np.zeros(3); v[ax] = sg * L
                out.append(('eksen', [(0, 1, v)]))
        return out
    out.append(('ozgun', [(0, 1, np.array(d0, float))]))
    for k in ('ust', 'on', 'arka', 'sol', 'sag'):
        out.append((k, [(0, 1, np.array(YON[k], float) * m)]))
    # iki aşamalı: açık taraftan yaklaş (uzun) + son oturma (kısa)
    for k1 in ('on', 'ust', 'arka'):
        for k2 in ('ust', 'on', 'arka', 'sol', 'sag', 'alt'):
            if k1 == k2 or np.dot(YON[k1], YON[k2]) < -0.5: continue
            out.append((k1 + '+' + k2, [(0, 0.6, np.array(YON[k1], float) * m), (0.6, 1, np.array(YON[k2], float) * 0.06)]))
    for k in ('ust', 'on', 'arka', 'sol', 'sag', 'alt'):
        out.append((k, [(0, 1, np.array(YON[k], float) * 0.06)]))
    return out


def uygula_aday(HAR, grup, gi, aday, t0, t1):
    for a in grup:
        i = gi[a]; H = [h for j, h in enumerate(HAR[a]) if j != i]
        for f0, f1, v in aday:
            H.append([round(t0 + f0 * (t1 - t0), 3), round(t0 + f1 * (t1 - t0), 3)] + [round(float(x), 5) for x in v])
        HAR[a] = H


def grup_temiz(D, grup):
    gs = set(grup)
    D.yenile(grup)
    for a in grup:
        ia = D.idx[a]
        aday = np.where(np.all(D.L <= D.H[ia] + 1e-4, 1) & np.all(D.H >= D.L[ia] - 1e-4, 1))[0]
        for jb in aday:
            b = D.ads[jb]
            if b in gs: continue
            key = (a, b) if a < b else (b, a)
            if key in D.haric: continue
            # yalnız grubun KENDİ hareket penceresi (b'nin başka zamandaki hareketi b'nin grubunda denetlenir)
            r = D.cift(a, b, pencere=(min(h[0] for h in D.HAR[a]), max(h[1] for h in D.HAR[a])))
            if r: return False, (a, b)
    return True, None


def duzelt(P, HAR, ROT, GOR, KAY, GIZLI, haric, kilitli=(), log=print):
    D = Y.Denetci(P, HAR, ROT, GOR, KAY, GIZLI, haric)
    D.ciftsay = 0
    res = D.denetle(ilerleme=True)
    once = list(res)
    imza = {}
    for a in D.ads:
        if a in KAY or not D.pw(a): continue
        imza.setdefault(json.dumps(HAR[a]) + json.dumps(ROT.get(a, [])), []).append(a)
    sig = {a: k for k, v in imza.items() for a in v}
    gruplar = {}
    for r in res:
        m = r.get('hareket', r['a'])
        if m not in sig: m = r['b'] if r['b'] in sig else None
        if m is None: continue
        gruplar.setdefault(sig[m], set()).add(m)
    degisen, cozulmeyen = [], []
    for k in sorted(gruplar, key=lambda k: min(GOR[a] for a in imza[k])):
        grup = sorted(imza[k])
        if any(a in kilitli for a in grup) or any(ROT.get(a) for a in grup):
            cozulmeyen.append((grup, 'kilitli/dönen')); continue
        gi = {a: gel_indeks(HAR, GOR, a) for a in grup}
        if all(P[a]['m'] in ('guc', 'bilgi', 'hava') for a in grup) and all(v is not None for v in gi.values()):
            h0 = HAR[grup[0]][gi[grup[0]]]
            for a in grup: HAR[a][gi[a]] = [h0[0], h0[1], 0.0, 0.0, 0.0]; KAY.add(a)
            D.yenile(grup)
            degisen.append(dict(grup=grup, t0=h0[0], t1=h0[1], eski=[round(x, 3) for x in h0[2:5]], yeni='cekme', yol=[[0, 1, [0, 0, 0]]]))
            log('  kablo/hortum kanal içinden çekilir (yerinde) %s' % grup[0]); continue
        if any(v is None for v in gi.values()): cozulmeyen.append((grup, 'gel yok')); continue
        h0 = HAR[grup[0]][gi[grup[0]]]; t0, t1 = h0[0], h0[1]; d0 = h0[2:5]
        yedek = {a: [list(h) for h in HAR[a]] for a in grup}
        bulundu = None
        import time as _t; _ts = _t.time()
        log('  grup %s (%d) t=%.2f' % (grup[0][:40], len(grup), t0))
        for et, ad in adaylar(P, grup, d0):
            if _t.time() - _ts > 20: log('    süre aşıldı'); break
            for a in grup: HAR[a] = [list(h) for h in yedek[a]]
            uygula_aday(HAR, grup, gi, ad, t0, t1)
            ok, neden = grup_temiz(D, grup)
            if ok: bulundu = (et, ad); break
        if bulundu is None:
            # kapalı gövdede gerçekçi giriş yolu yok → parça YERİNDE belirir (içinden geçme gösterilmez); açık madde olarak raporlanır
            for a in grup:
                HAR[a] = [list(h) for h in yedek[a]]; HAR[a][gi[a]] = [t0, t1, 0.0, 0.0, 0.0]; KAY.add(a)
            D.yenile(grup)
            cozulmeyen.append((grup, 'yerinde'))
            degisen.append(dict(grup=grup, t0=t0, t1=t1, eski=[round(x, 3) for x in d0], yeni='yerinde', yol=[[0, 1, [0, 0, 0]]]))
            log('  YERİNDE (yol yok) %s (%d parça) t=%.2f' % (grup[0], len(grup), t0))
        elif bulundu[0] != 'ozgun':
            degisen.append(dict(grup=grup, t0=t0, t1=t1, eski=[round(x, 3) for x in d0], yeni=bulundu[0],
                                yol=[[f0, f1, [round(float(x), 3) for x in v]] for f0, f1, v in bulundu[1]]))
            log('  düzeltildi %-40s (%d) t=%.2f  %s → %s' % (grup[0][:40], len(grup), t0, d0, bulundu[0]))
    return once, degisen, cozulmeyen
