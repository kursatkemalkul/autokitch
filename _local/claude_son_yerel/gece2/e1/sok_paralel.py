# -*- coding: utf-8 -*-
"""Sökerek montaj sırası · PARALEL (6 Eki 2026 · yerel oturum). e_montaj.sira_bul'un hızlı karşılığı.
Her tur: hâlâ yerinde olan (ve engeli değişmiş) bütün parçalar işçilerde aynı anda denenir; yolu serbest olanların HEPSİ birlikte sökülür
(her biri diğerleri yerindeyken serbest → hangi sırayla takılsa da geçerli). Ters sıra = montaj sırası.
Yol denetimi e_montaj/_altyapi.serbest ile aynı (yol_denetim_v2.ccd, model ağı Vm/Fm)."""
import os, sys, pickle, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_G = {}


def _hazirla(pkl):
    sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE)
    import yol_denetim_v2 as Y
    D = pickle.load(open(pkl, 'rb'))
    _G.update(Y=Y, P=D['P'], VEK={})
    _G['LO'] = {a: v['V'].min(0) for a, v in D['P'].items()}; _G['HI'] = {a: v['V'].max(0) for a, v in D['P'].items()}
    f_ = os.path.join(HERE, 'mek_ic_ice.json')
    _G['HARIC'] = set((a, b) for a, b, _ in json.load(open(f_, encoding='utf-8'))) if os.path.exists(f_) else set()


def _gercek(a, b, A0, v):
    """CCD temas buldu: hareket boyunca 2 mm adımla model ağlarında 0,3 mm toleranslı GERÇEK kesişim var mı (sıfır boşluklu kayma = yüzey teması değil)"""
    Y = _G['Y']; B = _tri(b); n = max(2, int(np.ceil(np.linalg.norm(v) * 1000.0 / 2.0)) + 1)
    lo_b = B.min((0, 1)); hi_b = B.max((0, 1))
    for s in np.linspace(0.0, 1.0, n):
        A = A0 + s * v; sa = np.all(A.min(1) <= hi_b, 1) & np.all(A.max(1) >= lo_b, 1)
        if not sa.any(): continue
        if int(Y.poz_kesisim(np.ascontiguousarray(A[sa]), np.ascontiguousarray(B), 3e-4).sum()): return True
    return False


def _tri(a):
    V = _G['VEK']
    if a not in V:
        p = _G['P'][a]; V[a] = _G['Y']._vekil(np.asarray(p.get('Vm', p['V'])) / 1000.0, np.asarray(p.get('Fm', p['F'])))
    return V[a]


def _serbest(a, ofs, yerinde, ofs2):
    Y, LO, HI = _G['Y'], _G['LO'], _G['HI']
    ofs = np.asarray(ofs, float); ofs2 = np.asarray(ofs2, float); v = (ofs2 - ofs) / 1000.0; sorun = []
    if np.linalg.norm(v) < 1e-9: return sorun
    A0 = _tri(a) + ofs / 1000.0
    l = (np.minimum(LO[a] + ofs2, LO[a] + ofs)) / 1000.0; h = (np.maximum(HI[a] + ofs2, HI[a] + ofs)) / 1000.0
    amn_ = np.minimum(A0.min(1), (A0 + v).min(1)); amx_ = np.maximum(A0.max(1), (A0 + v).max(1))
    for b in yerinde:
        if b == a or (a, b) in _G['HARIC'] or (b, a) in _G['HARIC']: continue
        if np.any(LO[b] / 1000.0 > h + 1e-4) or np.any(HI[b] / 1000.0 < l - 1e-4): continue
        sa = np.all(amn_ <= HI[b] / 1000.0 + 1e-4, 1) & np.all(amx_ >= LO[b] / 1000.0 - 1e-4, 1)
        if not sa.any(): continue
        B = _tri(b); smn = amn_[sa].min(0); smx = amx_[sa].max(0)
        sb = np.all(B.min(1) <= smx + 1e-4, 1) & np.all(B.max(1) >= smn - 1e-4, 1)
        if not sb.any(): continue
        lam = Y.ccd(np.ascontiguousarray(A0[sa]), np.ascontiguousarray(B[sb]), v.astype(np.float64), Y.SINIR)
        m = lam < 1.5
        if not m.any(): continue
        pts = lam[m][:, None] * v[None, :]
        der = np.linalg.norm(pts - v[None, :], axis=1)
        if der.max() > Y.OTURMA and _gercek(a, b, A0, v): sorun.append(b); return sorun   # ilk engelde dur (hız)
    return sorun


def _dene(is_):
    a, dig, adaylar = is_
    eng = set()
    for yol in adaylar:
        s_ = []
        for p0, p1 in zip(yol[:-1], yol[1:]):
            s_ = _serbest(a, p0, dig, p1)
            if s_: break
        if not s_: return a, [np.asarray(p).tolist() for p in yol], []
        eng |= set(s_)
    return a, None, sorted(eng)


def sira_bul_paralel(adlar, adaylar_f, tercih, pkl, isci=22, log=print):
    from concurrent.futures import ProcessPoolExecutor
    kal = list(adlar); cik = []; engel = {}; tur = 0
    with ProcessPoolExecutor(max_workers=isci, initializer=_hazirla, initargs=(pkl,)) as ex:
        while kal:
            tur += 1; kset = set(kal)
            dene = [a for a in kal if not (a in engel and engel[a] and not (set(engel[a]) - kset))]
            if not dene: dene = list(kal)
            isler = [(a, [b for b in kal if b != a], adaylar_f(a)) for a in sorted(dene, key=tercih)]
            sonuc = list(ex.map(_dene, isler, chunksize=1))
            ok = [(a, [np.asarray(p) for p in y]) for a, y, _ in sonuc if y is not None]
            for a, y, e in sonuc:
                if y is None: engel[a] = e
            if not ok:                                                         # kilitlenme: tercihe göre biri yolsuz çıkar (rapora)
                a = sorted(kal, key=tercih)[0]; ok = [(a, None)]
            ok.sort(key=lambda x: tercih(x[0]))
            for a, y in ok: cik.append((a, y)); kal.remove(a); engel.pop(a, None)
            log('  tur %d · denenen %d · sökülen %d · kalan %d%s' % (tur, len(dene), len(ok), len(kal), '' if ok[0][1] is not None else ' · KİLİT: %s yolsuz' % ok[0][0]))
    return list(reversed(cik))
