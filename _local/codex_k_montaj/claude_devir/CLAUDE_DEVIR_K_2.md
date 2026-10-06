# K MONTAJ — CLAUDE (bulut) → YEREL OTURUM DEVRİ · 6 Eki 2026

Her zaman Türkçe, kısa ve net yaz. Küçük kararları sorma; büyük kararlarda Kemal'e sor.
Önce oku: `KURALLAR.md`, `KOORDINASYON.md`, bu dosya.

**Kemal kuralı:**
- Her parça tek tek üretilip montajlanır (sac: açınım → büküm → yerine).
- Bağlantı elemanı tek tek, kendi ekseninde takılır.
- Parça BLOK olarak gelmez.
- Bağlantısız parça 0 olmalı. Kemal "yayınla" demeden yayın yok.

## Dal ve dosyalar
- Dal: `claude/k-montaj`. Codex devri `10f02d3b` üstündedir. Codex'in kendi devir notu: `_local/codex_k_montaj/claude_devir/DEVIR.md`.
- Çalışma klasörü: `_local/codex_k_montaj/k1/`.
- Zincir: `arastirma/_uretec/h3/yama_v9/` (`zincir.py`, `SIRA.md`, `86_k_baglanti.py`, `veri/86_k_baglanti.json`).

## Biten
1. **Codex paketi açıldı.** Komut: `python _local/codex_k_montaj/devir_paket.py --restore`. Çıkanlar:
   - `k1/plan_k_clip_full.pkl`
   - `k1/k_parca_clip_verified.pkl`
   - `k1/k_bil_clip.pkl`
   - model `electrical_clip_weld_candidate/A/hat3_v10ze.glb`
2. **Bağlantı denetimi.** Betik `k1/baglanti_claude.py`, çıktı `baglanti_claude.json`. Codex planında 212 bağlantısız taşıyıcı parça vardı.
3. **Temas ölçümü.** Betik `k1/k_temas.py`, çıktı `k_temas.json`. Her açık parçanın oturduğu yüzey ve aralık.
4. **Bağlantı planı.** Betik `k1/k_baglanti_plan.py`, çıktı `k_baglanti_plan.json`. Ardından `k1/k_86_veri.py` → `veri/86_k_baglanti.json`. Sonuç **212 / 212 çözüldü, açık 0**:
   - 135 vida
   - 76 somun / kör perçin somun
   - 6 saplama
   - 2 pim
   - 159 TIG / punta işareti
   - 112 beyanlı bağlantı (dişli, DIN, oluk, kızak, ürün içi, elle çıkan)
5. **Zincir adımı 86.** `hat3_v10ze` → `hat3_v10zf`. İki koşu bayt aynı, SHA256 `4fc05b06…`. `SIRA.md`'ye yazıldı.
   - Bıçak seti: tek merkez M8 saplama + kelebek somun + 2 pim.
   - Koruma braketleri kafa plakasına yaslandı.
   - Regülatör panel somunuyla bağlandı.
6. **Parça çıkarımı.** Betik `k1/k_parca_c.py`, çıktı `k_parca_c.pkl`. 1.406 parça; eski adlar korundu, eşleşmeyen 0.
   - Not: "adsız yeni bileşen 781" uyarısı çıkıyor. Bunlar K bölgesine giren komşu istasyon bileşenleri (B_KASA, kompresör…). Çevre olarak eklenmeli, düzeltilecek.

## Kalan (sırayla)
1. **Modeli yeniden üret.** `hat3_v10zf.glb` depoda yok; bulut makinesindeydi.
   ```
   python _local/codex_k_montaj/devir_paket.py --restore
   cd arastirma/_uretec/h3/yama_v9
   python zincir.py --is <iş>/k86A --uretec <repo>/arastirma/_uretec --adim 86 --girdi-dizin <repo>/_local/codex_k_montaj/electrical_clip_weld_candidate/A
   ```
   Aynı komutu `k86B` için de çalıştır. İki çıktı bayt aynı olmalı, SHA `4fc05b06…`.
2. **Parça çıkarımı.**
   ```
   cd _local/codex_k_montaj/k1
   python k_parca_c.py <iş>/k86A/hat3_v10zf.glb <iş>/k86A/hat3_v10zf_ent.json
   ```
   Önce `k_parca_c.py`'yi düzelt: "adsız yeni bileşen"leri (B / F / E / U / kompresör) çevreye `cevre_diger` adıyla ekle.
3. **Temas hesabı.** `python k_deg.py` → `k_deg.json`. Bulutta 2 saatte bitmedi. Yavaş; gerekirse Pool sayısını artır ya da örnek sayısını (400) düşür.
4. **Montaj planı.** `python k_montaj_c.py` → `plan_k_c.pkl`. Hiç çalışmadı; `PLAN SORUNU` 0 olana kadar düzelt.
   - Adım sırası ve yöntem betiğin içinde.
   - Pano grubu tezgâhta parça parça kurulur.
   - Bağlantı elemanları, değdikleri taşıyıcılar yerine gelince otomatik takılır.
5. **Çıktı ve denetim.**
   - E'deki `e_cikti.py`'yi (`_local/claude_son_yerel/gece2/e1/`) `k_cikti_c.py` olarak uyarla: `plan_k_c.pkl` → `otonom/hat3d/v3/k_montaj/`.
   - Sonra `baglanti_claude.py`'yi `plan_k_c.pkl` ile çalıştır. KAT listesine `veri/86_k_baglanti.json` → `beyan` kategorilerini ekle (E'deki gibi).
   - Hedefler:
     - yol çakışması 0
     - son konum beyansız 0
     - havada 0
     - bağlantısız (AÇIK) 0
     - geçici dayalı olanların metni yazılı
6. **Sayfa.** `otonom/hat/k-montaj.html`, şablon `e-montaj.html`. Tarayıcıda dene, ekran görüntüsünü Kemal'e gönder.
7. **Açık notlar (rapora yaz):**
   - SMC B240A şartlandırıcı braketi model proxy'si sade; gerçek kulak delikleri regülatör izinin dışında.
   - K kolu (Codex 70–79 + 86) ana zincire (main: v10l · E 68–69 + 80) henüz alınmadı.
   - X silindir uç kapağı vidaları itici sacından geçiyor; sacın içi açık mı, kontrol et.

## Kurallar
- Force push yok.
- `_local` siteye gitmez.
- Depo açık; gizli bilgi koyma.
- Büyük `.pkl` / GLB depoya konmaz.
- Süreç kapatırken `pkill -f` kullanma, PID ile kapat.
