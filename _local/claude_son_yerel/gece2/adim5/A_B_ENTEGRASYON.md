# A + B ÜRETİM SACI · ENTEGRASYON NOTU (adım 5a → 5-entegrasyon)

4 Eki 2026 · Claude · YEREL. Ana GLB'ye (otonom/hat3d/v3/hat3_v8.glb) DOKUNULMADI. Bu not, bir sonraki "5-entegrasyon" adımının yapacaklarını listeler.

Üreteçler (worktree, deterministik, göreli yol): `arastirma/_uretec/h3/h3_a_sac_v1.py`, `arastirma/_uretec/h3/h3_b_sac_v1.py`
Ortak kütüphane: `h3_sac_v1.py` (değişmedi). Standart klasörü: `AUTOKITCH_SAC_STANDART` ortam değişkeni → `<scratchpad>/sac_standart` (K ile aynı).
Bağımsız çıktılar + denetim: `<scratchpad>/gece2/adim5/` (`A_sac_v1.glb`, `B_sac_v1.glb`, `A_parca.csv`, `B_parca.csv`, `A_rapor.json`, `B_rapor.json`,
`acinim_A/`, `acinim_B/` her sacın açınım JSON'u, `A_*.jpg`, `B_*.jpg`, `sac_denetim_ortak.py`, `a_sac_denetim_v1.py`, `b_sac_denetim_v1.py`).

Kullanım (montaj tarafı):
```python
import h3_a_sac_v1 as A            # A: yerel x (dünya = x + 736) → A.dunya_listesi(A.govde_parcalari())
import h3_b_sac_v1 as B            # B: dünya koordinatı → B.dunya_listesi(B.govde_parcalari())
# her parça: ad · sh (OCC katı) · tur (sac / profil / kaynak / baglanti / pu) · mal · bom · sac (açınım özeti) · meta
# ARAYÜZ elemanları (karşı taraftaki cıvata, pul, PEM): A.G.ARAYUZ / B.G.ARAYUZ — gövdeye KATILMAZ, karşı parçanın deliği için listedir
```

---------------------------------------------------------------------------------------------------------------------------------

## A (AÇICI KABUĞU)

### Silinecek düğümler (v8zq GLB)
| düğüm | ne | not |
|---|---|---|
| `A_GOVDE__sac` | 4 kutu sac (sol / sağ / arka / tavan) | yerine 4 bükümlü panel |
| `A_GOVDE__paslanmaz` | 30 × 30 çerçeve + ön alt bant (dolu blok) | yerine kaynaklı iskelet (dikme + üst halka + tapa + kulak) |
| `A_GOVDE__plastik` | boş (v8 zincirinde boşaltıldı) | sil |
| `KAIDE_A__paslanmaz` | 7 kaide borusu (40 × 100) | yerine kaynaklı kaide (aynı kesit, çerçeve 3,5 / 15 mm içeri) |
| `KAIDE_A__sac` | 4 mm plaka + 1,5 mekanizma sacı | yerine delik kaynaklı plaka + damlama sacı (aynı kotlar 888 / 892 / 893,5) |
| `A_ONYUZ__on_seffaf`, `A_ONYUZ__on_seffaf__SERVIS_KAPAGI`, `A_ONYUZ__paslanmaz`, `A_ONYUZ__plastik` | eski tek kapak + menteşe + bas-aç | yerine çift cidarlı kapak (dış tava 1,5 + iç tava 1,0) + 3 gizli menteşe + 3 bas-aç (dikmelerin içinde) |
| `A_MODULER__paslanmaz`, `U_A_GOVDE__*` | boş | sil |

### Yeni düğümler (öneri: mevcut adlandırma düzeni)
- `A_GOVDE__sac` ← tur sac (kapak hariç) + profil + kaynak · `A_GOVDE__paslanmaz` ← tur baglanti (PEM, vida, pul, somun, menteşe gövdesi) ·
  `A_GOVDE__conta` ← servis tapaları (silikon) · `A_ONYUZ__on_seffaf` ← `kapakla_doner(ad)` True olan bütün parçalar (dış + iç tava, kanat yarıları,
  karşılık plakaları, kapaktaki PEM / vida) — kapak animasyonu için `kpk` aralığı bu düğümün tamamı.
- Kapak menteşe ekseni: dünya x 736 · z 79 (sanal pivot, ön-sol köşe), y ekseni, dışa 0–180° (eski kapakla aynı pivot).
- `mek` = A/Gövde (kapak dahil) · `kat` = GOVDE.
- `parca_kutulari.json`: `S.parca_kutusu_satiri(p)` ile (eski A_GOVDE / KAIDE_A / A_ONYUZ satırları çıkar).

### Kalan (değişmeyen) parçaların yeni gövdeye bağlanması
| mevcut parça | bağlantı | gövdede hazır | karşı tarafta gereken (ARAYÜZ) |
|---|---|---|---|
| Açıcı kolonu (`TOPPING_MODUL__sac[29]` + `__ACICI` parçaları, ayak x 1026–1146 · z −660…−505) | 4 × ISO 4762 M8 + DIN 125 | kaide plakasının altında 4 × PEM SP-M8-2, damlama sacında Ø9 (eksenler dünya x 1041 / 1131 · z −645 / −520) | kolon taban flanşında 4 × Ø9 (90 × 125 eksen) — açıcı satın alınırken istenir ya da 6 mm adaptör plakası |
| Tabla rayı tabanı (`TOPPING_MODUL__sac[8]`, x 836–2495) | 4 × ISO 4762 M6 | 4 × PEM SP-M6 (dünya x 880 / 1300 · z −320 / −20 — rayın üstündeki serbest bantlar) | ray tabanında 4 × Ø6,6 |
| TOPPING sol duvarı (PU'lu soğuk oda) | 4 × ISO 4762 M8 × 16 + DIN 9021, **A içinden** | A sağ yan sacında 4 × Ø9 (y 1300 / 2000 · z −300 / −700) | TOPPING sol dış sacında Ø10,5 + **PEM SP-M8** (köpüklemeden önce, gövde PU tarafında + köpük kapağı) |
| B tavanı / B_MODULER üst kirişleri | 6 × ISO 4762 M8 × 25 + DIN 9021 (kaide borusunun içinden) | kaide borusu alt duvarı Ø9, üst duvarı Ø16; plaka + damlama sacında Ø16 + gömme silikon tapa (dünya x 761 / 1086 / 1411 · z −706 / −110) | B dış tavanında Ø9 (**h3_b_sac_v1'de hazır**) · GFRP pedde Ø9 · B_MODULER üst kiriş üst duvarında M8 kapalı uçlu perçin somun |
| Tabla / araba / koni (hareketli) | yok | sağ yan sacta TABLA GEÇİŞ AĞZI (y 893,4–1042 · z −510…+4, R6) — v8zq ile aynı | — |

- A'da elektrik / hava / kablo geçişi YOK (kural). X ekseni motoru TOPPING ucunda (v8zc'den beri).
- İç hacim: kabuğun iç ölçüsü aynı; yalnız 4 dikme (30 × 30) panel dönüşlerine yer açmak için köşeden 3,5 mm / 15 mm içeri alındı (K ile aynı) —
  açıcı ve tabla yoluyla çakışma yok (denetim).

---------------------------------------------------------------------------------------------------------------------------------

## B (ÇEKMECELİ SOĞUK DOLAP GÖVDESİ)

### Silinecek düğümler (v8zq GLB)
| düğüm | ne | yerine |
|---|---|---|
| `B_KASA__sac` | 42 kutu sac (dış kabuk, iç kabuk, bölmeler, kovanlar, ısı kalkanı, 4 eski elektrik kovanı) | 63 bükümlü / lazer sac (dış kabuk 2 parçalı + ek lamaları + köşebentler · iç kabuk · bölmeler · U / L kovanlar · ısı kalkanı U + ışınım sacı · teknik kapama · ara katman arka sacı) |
| `B_KASA__pu` | 21 PU bloğu | yeni PU blokları (aynı bölgeler − yeni saclar − gömülü elemanlar − geçiş içleri − PEM kapakları − dış köşe olukları) |
| `B_KASA__on_cerceve` | tek parça çerçeve (3661 mm) | 2 parça 430 çerçeve (ek x 2091) + 35 mm ek laması |
| `B_KASA__koyu` | 12 ısı kalkanı takozu | 12 PTFE + cam elyaf takoz (aynı yer) |

**KALIR (dokunulmaz):** `B_KASA__celik` (14 ayak), `B_MODULER__*` (alt şase + PU'ya gömülü dikme / kiriş + GFRP pedler), `B_TASIYICI__celik`, `B_DEPO__*`,
`B_SOGUTMA__*`, `B_ELEKTRIK__*`, `B_KABLO__kanal`, bütün `CEK_*` (çekmeceler + raylar + kapaklar + fitiller), `ELK_*`, `DUZ_B_SERPANTIN`.

### Yeni düğümler (öneri)
- `B_KASA__sac` ← tur sac (dış kabuk `dis_*`, `kosebent_*`, iç kabuk `ic_*`, `bolme_*`, `teknik_sol_duvar`, `isi_kalkani_*`, `tk_ara_arka_sac`) ·
  `B_KASA__on_cerceve` ← `on_cerceve_1/2` + `on_cerceve_ek_lamasi` (malzeme: çerçeve, opak, kapak DEĞİL) · `B_KASA__pu` ← tur pu ·
  `B_KASA__koyu` ← takozlar · `B_KASA__paslanmaz` (yeni) ← PEM SP-M5 (126) + kaynak dolguları · `B_KASA__conta` (yeni) ← PEM köpük kapakları,
  ek yeri ve gider silikonları.
- `mek` = B/Gövde · `kat` = GOVDE · `kpk` yok (B gövdesinde kapak yok; çekmece kapakları CEK_* düğümlerinde).
- PU düğümü: sahnede görünmez olmalı (zaten kapalı); x-ray / kesit görünümünde sarı.

### Kalan parçaların yeni gövdeye bağlanması
| mevcut parça | bağlantı | gövdede hazır | karşı tarafta gereken (ARAYÜZ) |
|---|---|---|---|
| 42 sabit çekmece rayı (`CEK_*__celik`, sol / sağ duvar yüzleri 798,5 · 1418,5 · 1453,5 · 2073,5 · 2108,5 · 2728,5 · 2763,5 · 3383,5 · 3418,5 · 3993,5) | her ray 3 × DIN 7991 M5 × 10 A2 | duvar saclarında 126 × PEM SP-M5-1 (z −580 / −330 / −45 · y = ray alt + 22,85) + PE köpük kapağı | sabit ray gövdesinde 3 × Ø5,5 + 90° havşa (aynı eksen) |
| B_MODULER alt şase boyunaları (z −790…−730 · −140…−80) | 10 × ISO 4762 M8 × 20 + DIN 9021 (B içinden, köpüklemeden önce) | dış tabanda 10 × Ø9 (x 1100 / 1750 / 2400 / 3050 / 3700) | şase üst duvarında 10 × M8 perçin somun |
| A kaidesi (h3_a_sac_v1) | 6 × M8 (A tarafından) | dış tavanda 6 × Ø9 (x 761 / 1086 / 1411 · z −706 / −110) | B_MODULER üst kirişte M8 kapalı uçlu perçin somun + GFRP pedde Ø9 |
| K iskeleti (h3_k_sac_v1) | 2 × M8 (K tarafından) | dış tavanda 2 × Ø9 (x 4016,5 · z −480 / −570) | B_TASIYICI çapraz kiriş 2 üst duvarında M8 perçin somun (K notu ile aynı) |
| B_KABLO kanalı (arka iç yüzde) | — | bölmelerde 1 mm boşluklu U kovan (kanal köşesine büküm R'si girmesin) | yok |
| Gider kılıfı (`B_SOGUTMA__plastik`, Ø24) | silikon halka | bölme saclarında Ø24,4 · B5'te alta açık U çentik + silikon | yok |
| Modüler / taşıyıcı dikmeler (bölmelerin içinde) | PU'ya gömülü | iç taban + iç tavanda 31 × 31 geçiş (bölme altında) | yok |
| ELK zemin kovanı (x 4065–4115) | contalı | Secop 1. emiş penceresinin içinden geçer (ayrı ağız yok) | yok |
| B elektrik kutusu montaj sacı (`B_ELEKTRIK__sac`, arka iç yüz) | — | sağ yan sacın arka dönüşünde y 455–745 çentik | yok |
| Depo tavan iç sacı (`B_DEPO__sac`, +37,5'e uzanır) | — | çerçevede 311 × 1,4 yuva | yok |
| E gövdesi (x ≥ 4400) | — | sağ yan dış yüz düz (E kabuğuna yüz yüze) | B ↔ E bağlantısı E kaidesi / alt şase üzerinden (E sahibi) |

### Kaldırılanlar / değişenler (bilerek)
- Eski elektrik ana hat kovanları (TOPPING altı x 2419,8–2500 ve B5 üstü) — v8zj'den beri içlerinden kablo geçmiyor (v8zq'da boş) → kaldırıldı, PU doldu.
- Yan saclar artık tava değil: yalnız arka dönüş; tavan / taban bağlantısı köşebentle (GFRP pedleri yan sacın iç yüzüne dayalı olduğundan sürekli dönüş konamadı).
- İç kabuk ve bölme ön kenarları çerçeveye ALIN (büküm dış yayı çerçeve köşesinde açık oluk / görünür PU bırakıyordu).
- İç kabuk köşeleri bükümlü R değil TIG (B_KABLO dikey kanalları ve ray braketleri iç köşeye dik oturuyor; bükümlü R3 köşe onlara 1,1 mm giriyordu).
- Ray vidası z'leri −627 / −327 / −27 → −580 / −330 / −45 (taşıyıcı dikmeler bölme içinde z −635…−605).

---------------------------------------------------------------------------------------------------------------------------------

## DENETİM SONUCU (bağımsız · `sac_denetim_ortak.py` · v8zq'ya karşı)

| madde | A | B |
|---|---|---|
| parça | 298 gövde parçası (37 sac · 15 boru · 146 bağlantı elemanı · 100 kaynak dikişi) + 32 arayüz elemanı | 401 gövde parçası (63 sac · 19 PU bloğu · 279 bağlantı / dolgu elemanı · 40 kaynak dolgusu) + 146 arayüz elemanı |
| kütle | sac 96,9 kg + boru 32,0 kg | sac 266,4 kg (PU hariç) |
| açınım (açınımdan yeniden büküm + kalınlık + kesit R) | 37 / 37 GEÇTİ | 63 / 63 GEÇTİ |
| DFM (abkant sırası dahil) | 0 HATA · 0 UYARI | 0 HATA · 0 UYARI |
| en büyük levha | 1443 × 733 (kapak dış tava) | 2309 × 869 (tavan 2) — 3000 × 1500 içinde |
| dış zarf (bugünkü ± 0,5) | 736–1436 · 788–2200 · −830…+79 → fark 0,0 | 736–4400 · 123–788 · −830…+39 → fark 0,0 |
| gövde ↔ gövde hacim kesişimi | 0 (35 izinli = PEM gömme başı sacın içinde, işaretli) | 0 |
| gövde ↔ v8zq iç / komşu parçalar (govde_denetim_dogru.cift: manifold + yoğun örnekleme + derinlik > 0,05) | ÇAKIŞMA 0 · İNCELE 0 (6683 bileşen) | ÇAKIŞMA 0 · İNCELE 0 (6646 bileşen) |
| havada (temas grafiği ≤ 0,6 → zemine bağlı) | 0 / 298 | 0 / 401 |
| PU görünmez (her PU yüzü 10 mm aralıkla, 0,4 dışarı → sac / PU / gömülü eleman içinde mi) | — (A'da PU yok) | 341 819 nokta · açıkta 0 |

Bilinen kabuller (B): (1) iç köşeler ve kovan çevreleri TIG + taşlama — dikiş katıları yalnız köpüğe açılan köşe ağızlarında modellendi
(`*_kose_kaynagi_*`), diğer dikişler etiket (CSV "KAYNAK (etiket)") · (2) ek yeri alın aralıkları, gider halkaları ve 4 arka köşe cebi gıda
silikonuyla köpüklemeden önce kapatılır (katı olarak modellendi) · (3) PEM SP-M5 gövdelerine PE köpük kapağı · (4) < 20 mm³ ara boşluklar
(pul deliği çevresi) köpüksüz · (5) v8zq'daki gider kılıfı bölme kovanları açık ağ olduğu için PU denetiminde kılıf zarfı (Ø24) örtücü sayıldı.
