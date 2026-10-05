# HAT v3 · GECE 2 · ADIM 8 · TAM DENETİM — hat3_v9h.glb (salt okuma, model değişmedi)

Denetlenen: `gece2/adim8/hat3_v9h.glb` (= worktree `otonom/hat3d/v3/hat3_v8.glb`, bayt aynı) · 10 023 katı bileşen (ROBOT/İNSAN/ZEMİN hariç) · taban v9f (9 983 bileşen) aynı araçla taranıp karşılaştırıldı · ayrıca v8zq (havada).
Süre: 05:07 → 05:35. Bütün betikler `gece2/adim8/denetim/` altında; `d*.py` betikleri bu klasörden çalıştırılır (göreli yol `cak/meta.json`).

## KALEM SONUÇLARI

| # | Kalem | Sonuç |
|---|---|---|
| 1 | Doğru çakışma (tüm model, 22 işçi, OCC + yüzey) | v9h: 1066 çakışma = **gerçek 108 · kasıtlı 902 · şüpheli 56** · temas 19 687 · hata 0. **v9f ile fark: YENİ 0, KALKAN 0** → adım 39 (servis) + 40 (acil stop) yeni çakışma getirmedi. Yeni parçalara ayrıca `yeni_cak.py`: 1 temas düzeyi (d4 kablo rakoru ↔ F_UST_KABIN__sac[93] 0,02 mm³), spiral servis halkası açık ağ (hacim ölçülemedi). |
| 1b | 41'lik eski liste (gece/m8t3, v8za) | 41'in **31'i hâlâ var**, **9'u kalktı** (kaşar/sucuk tüp-kapak-plaka-conta 7 adet, VALF_HARC#1↔#2 eski konumu, davlumbaz fan kablosu). 108 gerçeğin 77'si 41 listesinde yok ama **v9f'de de var (önceden var)**; döküm aşağıda. |
| 2 | Havada (temas ≤ 0,6 mm, üçgen kutusu grafiği, zemin y ≤ 1) | **12 grup / 99 bileşen**, hepsi v9f ve v8zq'da da var → **yeni 0**. Ölçülen boşluk (trimesh, köşe→yüzey): 10 grupta 1,0–10,5 mm (gerçek havada); 2 grupta 0 mm (değiyor, üçgen-kutu grafiği bağı kuramamış → olası sahte). Liste aşağıda. |
| 3 | Açık PU / yalıtım (1 mm z-tampon, 6 yön, kapaklar kapalı + kpk gizli) | Kapaklar kapalı: yalnız **B_KASA__pu 1 mm şerit** önden (x 2090,4–2091,4, y 729–786 ve 124–163; 96 mm²), v9f'de de var. kpk gizli: ek olarak K_BANT__pu_bant (PU taşıma bandı — yalıtım değil, bulgu değil). Arka −z 4 mm² gürültü. Yan/üst/alt 0. |
| 4 | Kablo ↔ kablo | 24: 12 kasıtlı (QR orta dikey kanal kapağı ↔ göz mandal kabloları 1,6 mm, kanal içinde) · **12 gerçek: QR göz ısıtıcı kabloları ↔ qrk_ana_hat_veri Cat6A 1,32–1,34 mm, 14 mm³** (x 4784/4806, z 1000, y 452–1453 her gözde). v9f'de de var. |
| 5 | Dış zarf | ELK_ZEMIN 101 bileşen (zemin altı kanal, y < 0, kasıtlı) ve 2 sıfır boyutlu ürün yer tutucu hariç **12 taşan**, hepsi v9f'de de var: 4 ELK_ZINCIR kablosu arka düzlemden **20 mm dışarı** (z −850; x 3930–3971, y 2110–2156 — bina beslemesi duvara giriyorsa kasıtlı) · 8 U_F_BACA flanş M6 cıvatası üstten **6 mm** (y 2206; x 2932–3268). Acil stop mantarları ön yüzden 27 mm (z 106) — hariç tutuldu. |
| 6 | A içi boş mu | **Evet.** x 737,5–1434,5 içinde yalnız açıcı (mek A/Açıcı: koni, z kızağı, kolon, motor), tabla geçişi (TOPPING/Tabla 39 bileşen y 893,5–1006) ve sıfır boyutlu ürün yer tutucuları (URUN__*, nokta 1086/1000/−170). Başka parça 0. |
| 7 | Hareketli parçalar | Acil stop 6 mantarın taşıyıcı kapağıyla 0→100° (2°) manifold süpürmesi + çekmece +z 700 öteleme: **TOPPING, F sol üst, K, E sağ üst mantarları TEMİZ.** B depo mantarı ve QR üst servis kapağı için bulgu (aşağıda). Çekmece kutu süpürmesi: 22 çekmece biriminden yalnız B depo engelli. |
| 8 | Etiket | 821 mesh, 11 187 372 indis: mek/kat/kpk aralık hatası **0**, 3'ün katı olmayan 0, çakışan aralık 0, mek < 56 (mekanizma_v3_8 "liste" = 56 = GLB içi) tamam, kat < 12 tamam, **etiketsiz üçgen 0**. |

## GERÇEK SORUNLAR (öncelik sırasıyla; hepsi v9f'de de var — adım 39/40 kaynaklı değil)

1. **QR üst servis kapağı en fazla ~44° açılıyor** (QR_GOVDE__on_seffaf servis_kapagi_ust, x 4372,5–5227,5 · y 1654–2047 · z 670; menteşe x 4381). 855 mm kanat, makine ön yüzü (z 79) ile QR yüzü (z 670) arası 591 mm: kanat ucu 46°'de E üst sağ kapağına (1160 mm³), 48°'den sonra U_KE taban sacına giriyor; mantar (5100, 1690) 52°'de E üst sol kapağına. Mantar ek kısıt getirmiyor; kısıt kanat genişliği (adım 2'de QR öne alınınca boşluk daraldı). Çözüm: iki kanat / sürgülü / kanat ≤ 590 mm.
2. **B depo çekmecesi mantarı QR'a çarpıyor** (mantar x 4340–4400 · y 720–780 · z 36–106): çekmece 570 mm çekilince QR yan_sac_sol (x 4370) + robot_yuzu_goz_saci + ELK_IC kanal 467/487/488; çekmece ön sacı da (x 4003–4399) 591 mm'de aynı yere giriyor. Depo kutusu ~550 mm derin → 15–20 mm pay kalıyor. Mantar x ≤ 4330'a alınırsa çekmece önü sınırı 591 mm'ye döner.
3. **TOPPING iç geçişler (önceden var, 41 listesinde yok)** — parça adları kutu eşlemesiyle, TOPPING içinde güvenilir değil; düğüm + konum esas:
   - PISTON_KUSBASI/SOS/HARC çubuğu ↔ TOPPING_MODUL__aluminyum (evap kaseti PU/soğuk iç kaplama) 10 mm / 1087 mm³ — konum (1842,1190,−682) (2254,1614,−682) (1716,1614,−682); aynı noktalarda PISTON düğümünün kendi içi 8 mm (1846,1190,−569 vb.) → piston duvar geçişinde delik yok.
   - TOPPING_MODUL__bakir ↔ evap kaseti iç/dış sac 3–7,8 mm, 900–2280 mm³ (2156,1441,−700) (2134,1446,−700) (1622,1440,−775) — evaporatör boruları kaset sacından geçiyor.
   - TOPPING_MODUL__silikon#8/#9 ↔ #10 5,1 mm / 1218 mm³ (2107,1143,−757).
   - soguk_ic_kaplama ↔ VALF_HARC#0 3,5 mm (1722,1614,−391); ↔ VALF_KUSBASI#0 2 mm (1805,1170,−385); celik↔paslanmaz 2,4 mm (1722/2259,1194,−150); paslanmaz↔saydam_celik 0,96 mm / 388 mm³ (1860,1160,−435 ve −558); motor#25↔#26 0,95 mm (1578,1520,−716).
   - TOPPING_MODUL__kart ↔ kart 32 çift 0,69–2,98 mm (x 2281–2386, y 1716–1733, z −715…−750) — sürücü kartları üst üste.
4. **QR ısıtıcı kablosu ↔ Cat6A ana hat** 12 çift 1,34 mm (kalem 4).
5. **Havada 12 grup** (boşluk → en yakın komşu): ELK_ISTASYON DOLAP sigorta+klemens 18 bileşen (4141–4320, 593–725, −700…−610) 0 mm · ELK_IC kanal 15 (2758–2795, 890–1136, −805…−665) 0 mm · ELK_IC kanal 12 (2973–3475, 885–1325, −795…−765) 1,0 mm → F_UST_KABIN sac · ic_kanal_B_P1z2 12 (4030–4207, 305–330, −492…−234) 1,5 mm · ELK_IC kanal 11 (3387–3925, 2030–2060, −793…−763) 3,1 mm · DOLAP evap fan kablosu 8 (1684–1786, 513–670) 4,0 mm · ELK_K sinyal kablosu 7 (4150–4211, 1682–1844) 1,8 mm · ELK_IC kanal 4+4+4 (2765–2795/1106–1136 · 3445–3475/1357–1480 · 2577–2786/845–875) 6,3–10,5 mm · ana pano RevPi DIO + AIO 2+2 (3770–3809, 1928–1978, −170…−149) 1,8 mm (DIN raya oturmuyor). 0 mm'lik 2 grup: komşuya köşe-yüzey değiyor, üçgen-kutu grafiği bağı kuramadı → olası sahte.
6. Zarf: ELK_ZINCIR 4 kablo z −850 (arka +20 mm), baca flanş cıvatası y 2206 (+6 mm).
7. B_KASA__pu 1 mm açık şerit önden x 2090,4–2091,4 (iki ön sac arası derz; v9f'de de var).

ŞÜPHELİ 56 (döküm `cak/cakisma.md`): 31 kpk kapalı-konum bindirmesi ≤ 0,09 mm (QR göz kapak mili ↔ kulak, K basaç ↔ köşe dikmesi, flipper), 6 tahrik diski mıknatısı 3,7 mm (cep yok), 4 döner valf ↔ blok 2 mm, 4 ürün yer tutucu, 1 TC kelepçe 0,74, 2 SAHTE olası (K sol sac ↔ yağ dönüş hortumu, OCC 0), 8 kablo demet.

## YENİDEN KOŞMA (S = scratchpad, D = S\gece2\adim8\denetim)

- Tüm model çakışma (≈ 12 dk, 22 çekirdek): `DENETIM_GLB=<glb> bash D/cak/calistir.sh` → D/cak/cakisma.json + cakisma.md (meta + işçi + OCC + yüzey + rapor). Taban için klasörü kopyala (D/cak_v9f gibi).
- Fark / 41 liste: `cd D && python d1_fark.py cak/cakisma.json cak_v9f/cakisma.json && python d1_karsilastir.py`
- Yeni parçalar: `cd D && python ../yeni_cak.py ../hat3_v9h.glb ../hat3_v9g_ent.json ../hat3_v9h_ent.json`
- Havada: `cd D && DENETIM_GLB=<glb> python d2_havada.py && python d2b_bosluk.py` (≈ 1,5 dk + 1 dk)
- PU: `cd D && DENETIM_GLB=<glb> python d3_pu.py` (≈ 1 dk, numba)
- Kablo↔kablo: `cd D && python d4_kablo.py` (cak/cakisma.json'dan)
- Zarf + A içi: `cd D && python d56_zarf_a.py [cak/meta.json]`
- Mantar + kapak süpürmesi: `cd D && DENETIM_GLB=<glb> python d7_mantar.py` (≈ 3 dk; meta.json aynı GLB'den olmalı) · çekmece: `python d7b_cekmece.py`
- Etiket: `cd D && python d8_etiket.py <glb> <mekanizma_v3_8.json>`

## KOŞULMAYAN / SINIRLI

- Kapakların genel açılma süpürmesi: menteşe pivotu GLB'de yok; yalnız mantar taşıyan 6 kapak, ekseni menteşe parçalarının ortasından (kapak ön yüzünde) alınarak koşuldu. Kapak paneli süpürmesinde menteşe yanındaki 2°'den başlayan girişler eksen yaklaşımından (sahte); yalnız uzak kenar girişleri (QR servis kapağı) anlamlı. Diğer ~60 kapak koşulmadı.
- Kaset / itici / kesici / QR göz kapısı süpürmeleri bu turda koşulmadı (kaset süpürmesi adım 3'te v8zq'da yapıldı; adım 39/40 o bölgelere dokunmadı).
- Havada testi üçgen kutusu yaklaşımı (eğik büyük üçgende fazla temas sayabilir → havada kaçabilir).
- Parça adları `parca_kutulari.json` kutu eşlemesiyle; TOPPING içinde yanlış ad verebilir (düğüm + konum esas alınmalı).
