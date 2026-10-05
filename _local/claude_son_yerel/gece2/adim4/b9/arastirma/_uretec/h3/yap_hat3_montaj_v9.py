# -*- coding: utf-8 -*-
"""HAT v3.9 MONTAJ (gece 2 · adım 4 · 4 Eki 2026 · Claude · YEREL) — "programlara aktarma": bugünkü model (v8zq) montaj programından üretilir.

v9 = montaj v7 (CAD montajı, deterministik: iki ayrı derlemede hat3_v7.glb bayt bayt aynı)
   + YAMA ZİNCİRİ h3/yama_v9/ (2–4 Ekim'de doğrudan GLB'ye yapılan bütün değişiklikler, ÖZGÜN betiklerle ÖZGÜN sırada · 32 adım · SIRA.md)
   → otonom/hat3d/v3/hat3_v9.glb  (= hat3_v8zq; karşılaştırma: h3/yama_v9/karsilastir.py)

NEDEN montaj v8 değil: yap_hat3_montaj_v8.py (A ↔ U_A ara çerçevesi + v3.8b/c metin yaması) hiç başarıyla derlenmedi —
  h3_kapak_v1.bolge_A, v3.8b'nin kaldırdığı emniyet sensörünü/hedefini düşürmeye çalışıp AssertionError veriyor (4 Eki derlemesi: 00:43).
  Aynı değişiklikler modele zaten GLB betikleriyle girmişti (zincir adım 00 glb_parca_sil + adım 01 glb_duzenle + adım 02 a_govde_yeni);
  sonraki 30 adımın betikleri o GLB'nin üçgen dizinine / düğüm sırasına göre yazıldığı için taban, zincirin gerçek tabanı olan montaj v7 GLB'sidir.

Kullanım (derleme ağacında; ana kirli klasörde DEĞİL):
  cd <ağaç>/arastirma/_uretec
  python h3/yap_hat3_montaj_v9.py                 # montaj v7 + zincir (≈ 40 dk montaj + ≈ 15 dk zincir)
  python h3/yap_hat3_montaj_v9.py --taban-hazir   # montaj v7 GLB'si zaten varsa (otonom/hat3d/v3/hat3_v7.glb) yalnız zincir
  python h3/yap_hat3_montaj_v9.py --referans <hat3_v8zq.glb>   # sonunda parça parça karşılaştırma
Elektrik üreteci ÇALIŞMAZ (h3/_elk önbelleği, montaj v7 ile aynı).
İZLENMEYEN BAĞIMLILIK: h3_sac_v1 (K üretim sacı) sac_standart_v1.json + sac_kararlar_v1.json'u <ağaç>/../../../../sac_standart'tan okur
  (scratchpad/b3'te var, worktree'de YOK → varsayılana düşer, K_GOVDE 4 düğümü farklı çıkar). v9: salt okunur kopyası h3/yama_v9/sac_standart,
  AUTOKITCH_SAC_STANDART ortam değişkeni verilmemişse o kullanılır."""
import argparse, os, runpy, subprocess, sys, time

H3 = os.path.dirname(os.path.abspath(__file__))
URETEC = os.path.dirname(H3)
CIKTI = os.path.normpath(os.path.join(URETEC, "..", "..", "otonom", "hat3d", "v3"))
YAMA = os.path.join(H3, "yama_v9")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--taban-hazir", action="store_true")
    ap.add_argument("--is", dest="is_dizin", default=os.path.normpath(os.path.join(URETEC, "..", "..", "_local", "yama_v9_is")))   # _local/ git dışı
    ap.add_argument("--referans")
    a = ap.parse_args()
    t0 = time.time()
    taban = os.path.join(CIKTI, "hat3_v7.glb")
    if not a.taban_hazir:
        print("1 · montaj v7 (yap_hat3_montaj_v7 → hat3_montaj_v7.py → h3_hiz_montaj)", flush=True)
        runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v7.py"), run_name="__yap__")
        env = dict(os.environ)
        env.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(YAMA, "sac_standart"))   # K sacı (h3_sac_v1) standart + kararlar; yoksa varsayılana düşer → K gövdesi FARKLI çıkar
        r = subprocess.run([sys.executable, "-u", os.path.join(H3, "h3_hiz_montaj.py"), os.path.join(H3, "hat3_montaj_v7.py")], cwd=URETEC, env=env)
        if r.returncode != 0 or not os.path.exists(taban): raise SystemExit("montaj v7 başarısız (çıkış %d)" % r.returncode)
        print("   montaj v7 · %.0f sn" % (time.time() - t0), flush=True)
    assert os.path.exists(taban), taban
    cikis = os.path.join(CIKTI, "hat3_v9.glb")
    print("2 · yama zinciri (yama_v9/SIRA.md) → %s" % cikis, flush=True)
    r = subprocess.run([sys.executable, "-u", os.path.join(YAMA, "zincir.py"), "--is", a.is_dizin, "--taban", taban, "--cikis", cikis,
                        "--uretec", URETEC, "--h3", H3])
    if r.returncode != 0 or not os.path.exists(cikis): raise SystemExit("yama zinciri başarısız (çıkış %d)" % r.returncode)
    if a.referans:
        print("3 · karşılaştırma ↔ %s" % a.referans, flush=True)
        subprocess.run([sys.executable, os.path.join(YAMA, "karsilastir.py"), cikis, a.referans, os.path.join(a.is_dizin, "KARSILASTIRMA.md")])
    print("HAT v3.9 · hat3_v9.glb yazıldı · toplam %.0f sn" % (time.time() - t0))


if __name__ == "__main__":
    main()
