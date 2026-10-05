# -*- coding: utf-8 -*-
"""h3_elk_voksel için BİREBİR aynı sonucu veren, daha hızlı + daha az bellekli parçalar (h3_hiz_montaj elektrik koşusunda takılır).
  · ornekle(P, T, h): _ornekle ile aynı noktalar (sıra farklı) — aynı formül, aynı işlem sırası (a + u·(b−a) + v·(c−a)),
    aynı n = ceil(L / (0,45 h)); L tamsayı sınırına 1e-9'dan yakınsa np.linalg.norm ile tek tek (eski kodla aynı).
  · isaretle(P, T, h, o, N): bul() içindeki "örnekle → hücre indisi → alt ızgara işaretle" bloğunun aynısı, PARÇA PARÇA
    (eski blok 6–9 M noktalık dizileri bir kerede ayırıyordu → 1 Eki v3.6 elektrik koşuları ArrayMemoryError ile düştü).
    İndisler aynı ifadeyle (np.floor((X − o) / h + 0.5)) hesaplanır, int32 saklanır (değerler küçük, birebir) → a0, a1, sub AYNI.
  · yamala(EV): EV.bul kaynağında o bloğu bulur ve isaretle çağrısıyla değiştirir; metin bulunamazsa (dosya değişmişse) DOKUNMAZ."""
import inspect, math, textwrap
import numpy as np


def _n_hesap(P, T, h):
    A = P[T[:, 0]]; B = P[T[:, 1]]; C = P[T[:, 2]]
    def nrm(d): return np.sqrt((d[:, 0] * d[:, 0] + d[:, 1] * d[:, 1]) + d[:, 2] * d[:, 2])
    L = np.maximum(np.maximum(nrm(B - A), nrm(C - A)), nrm(C - B))
    q = L / (h * 0.45)
    n = np.ceil(q).astype(np.int64)
    for k in np.nonzero(np.abs(q - np.round(q)) < 1e-9)[0]:                         # tamsayı sınırı: eski kodun kendi hesabı
        a, b, c = P[T[k, 0]], P[T[k, 1]], P[T[k, 2]]
        Lk = max(np.linalg.norm(b - a), np.linalg.norm(c - a), np.linalg.norm(c - b))
        n[k] = int(math.ceil(Lk / (h * 0.45)))
    return A, B, C, n


def _parcalar(P, T, h, en_cok=400000):
    """_ornekle'nin noktaları, ≤ en_cok noktalık parçalar hâlinde"""
    yield P
    if not len(T): return
    A, B, C, n = _n_hesap(P, T, h)
    tek = n <= 1
    if tek.any():
        yield (A[tek] + B[tek] + C[tek]) / 3.0
    for nn in np.unique(n[~tek]):
        s = np.nonzero(n == nn)[0]
        i, j = np.meshgrid(np.arange(nn + 1), np.arange(nn + 1))
        m = (i + j) <= nn
        u, v = i[m] / nn, j[m] / nn
        adim = max(1, en_cok // len(u))
        for k in range(0, len(s), adim):
            ss = s[k:k + adim]
            a = A[ss][:, None, :]; ba = (B[ss] - A[ss])[:, None, :]; ca = (C[ss] - A[ss])[:, None, :]
            yield (a + u[None, :, None] * ba + v[None, :, None] * ca).reshape(-1, 3)


def ornekle(P, T, h):
    return np.vstack(list(_parcalar(P, T, h)))


def isaretle(P, T, h, o, N):
    """eski blok:  X = _ornekle(P, Tr, h) · I = np.floor((X - o) / h + 0.5).astype(int) · a0/a1 · if np.any(a1 <= a0): continue · m · J · sub
    döner None (continue) ya da (a0, a1, sub)"""
    Is = []; lo = None; hi = None
    for X in _parcalar(P, T, h):
        if not len(X): continue
        I = np.floor((X - o) / h + 0.5).astype(int)
        mn = I.min(axis=0); mx = I.max(axis=0)
        lo = mn if lo is None else np.minimum(lo, mn); hi = mx if hi is None else np.maximum(hi, mx)
        Is.append(I.astype(np.int32))
    a0 = np.maximum(lo - 1, 0); a1 = np.minimum(hi + 2, N)
    if np.any(a1 <= a0): return None
    sub = np.zeros(a1 - a0, bool)
    for I in Is:
        I = I.astype(int)
        m = np.all((I >= a0) & (I < a1), axis=1); J = I[m] - a0
        sub[J[:, 0], J[:, 1], J[:, 2]] = True
    return a0, a1, sub


ESKI_BLOK = """        X = _ornekle(P, Tr, h)
        I = np.floor((X - o) / h + 0.5).astype(int)
        a0 = np.maximum(I.min(axis=0) - 1, 0); a1 = np.minimum(I.max(axis=0) + 2, N)
        if np.any(a1 <= a0): continue
        m = np.all((I >= a0) & (I < a1), axis=1); J = I[m] - a0
        sub = np.zeros(a1 - a0, bool); sub[J[:, 0], J[:, 1], J[:, 2]] = True
"""
YENI_BLOK = """        _r_hz = _HZ_isaretle(P, Tr, h, o, N)
        if _r_hz is None: continue
        a0, a1, sub = _r_hz
"""


def yamala(EV, log=print):
    try:
        kaynak = inspect.getsource(EV.bul)
    except Exception as e:
        log("hız · voksel yaması YOK (kaynak okunamadı: %s)" % e); return False
    if kaynak.count(ESKI_BLOK) != 1:
        EV._ornekle = ornekle                                                        # en azından örnekleme (aynı noktalar)
        log("hız · voksel: bul() bloğu değişmiş → yalnız _ornekle yaması"); return False
    g = EV.__dict__
    g["_HZ_isaretle"] = isaretle
    kod = compile(textwrap.dedent(kaynak.replace(ESKI_BLOK, YENI_BLOK)), EV.__file__, "exec")
    yerel = {}
    exec(kod, g, yerel)
    EV.bul = yerel["bul"]
    EV._ornekle = ornekle
    return True
