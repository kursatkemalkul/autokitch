# -*- coding: utf-8 -*-
"""h3_hiz_ornek.py · ÖRNEKLEMELİ profil (yalnız ölçüm): ana iş parçacığının yığını her 0,2 sn'de okunur.
Kullanım: python h3_hiz_ornek.py <betik.py> <cikti_on_eki> [arg...]
Çıktı: <on_ek>_satir.txt — betiğin kendi satırları (kümülatif, sn) + en çok zaman alan fonksiyonlar (öz + kümülatif) · print satırlarına geçen süre."""
import builtins, collections, io, os, runpy, sys, threading, time

betik, onek = os.path.abspath(sys.argv[1]), sys.argv[2]
sys.argv = [betik] + sys.argv[3:]
T0 = time.time()
_print = builtins.print


def tprint(*a, **k):
    if k.get("file") in (None, sys.stdout): _print("[%7.1f]" % (time.time() - T0), *a, **k)
    else: _print(*a, **k)


builtins.print = tprint
DT = 0.2
SATIR = collections.Counter(); FONK_OZ = collections.Counter(); FONK_KUM = collections.Counter(); N = [0]
ana = threading.main_thread().ident
dur = [False]


def ornekle():
    son = time.time()
    while not dur[0]:
        time.sleep(DT)
        f = sys._current_frames().get(ana)
        t = time.time(); w = (t - son) / DT; son = t                        # GIL tutan uzun C çağrısından sonra geçen sürenin tamamı (DT birimi)
        if f is None: continue
        N[0] += 1
        gor = set(); ilk = True
        while f is not None:
            co = f.f_code; anah = "%s:%s" % (os.path.basename(co.co_filename), co.co_name)
            if ilk: FONK_OZ[anah + ":%d" % f.f_lineno] += w; ilk = False
            if anah not in gor: FONK_KUM[anah] += w; gor.add(anah)
            if co.co_filename == betik: SATIR[f.f_lineno] += w
            f = f.f_back


class _Cik(BaseException):
    pass


def _exit(c=0):
    raise _Cik(c)


os._exit = _exit
sys.path.insert(0, os.path.dirname(betik))
th = threading.Thread(target=ornekle, daemon=True); th.start()
try:
    runpy.run_path(betik, run_name="__main__")
except (_Cik, SystemExit):
    pass
finally:
    dur[0] = True; th.join()
    L = io.open(betik, encoding="utf-8").read().splitlines()
    o = io.StringIO()
    o.write("toplam %.1f sn · %d örnek (%.1f sn aralık)\n\n== BETİK SATIRLARI (kümülatif sn, > 2 sn) ==\n" % (time.time() - T0, N[0], DT))
    for ln, c in sorted(SATIR.items()):
        if c * DT >= 2.0: o.write("%7.1f  %5d  %s\n" % (c * DT, ln, L[ln - 1].strip()[:150] if ln - 1 < len(L) else ""))
    o.write("\n== FONKSİYON KÜMÜLATİF (ilk 80) ==\n")
    for k, c in FONK_KUM.most_common(80): o.write("%7.1f  %s\n" % (c * DT, k))
    o.write("\n== ÖZ SATIR (yığının tepesi, ilk 80) ==\n")
    for k, c in FONK_OZ.most_common(80): o.write("%7.1f  %s\n" % (c * DT, k))
    io.open(onek + "_satir.txt", "w", encoding="utf-8").write(o.getvalue())
    _print("[%7.1f] ORNEK BITTI" % (time.time() - T0)); sys.stdout.flush()
