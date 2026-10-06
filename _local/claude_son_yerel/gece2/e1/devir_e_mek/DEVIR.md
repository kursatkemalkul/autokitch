# E mekanizma montajı · devir notu (6 Eki 2026, bulut 2. oturum → yerel oturum)

Görev tanımı: Kemal'in "AUTOKITCH · E (kutu katlama) MEKANİZMA MONTAJI — 2. oturum" brifingi (dal `claude/e-mekanizma`, zincir adımları yalnız **81–85**).
Önce `KURALLAR.md` (§1, §2, §3, §5) ve `KOORDINASYON.md` okunur. A istasyonu, `claude/a-kontrol`, zincir 86+, `montaj-oynatici.js`, `hat.css`, `index.html`, `KURALLAR.md`'ye dokunulmaz.
Kemal "yayınla" demeden main'e birleştirme ve site dağıtımı yok.

## 1. Durum

| Adım | Betik | Girdi → çıktı | Durum | SHA256 (çıktı GLB) |
|---|---|---|---|---|
| 81 | `81_e_kalip_kopru.py` | v10l → v10m | bitti, zincirde, 2 koşu aynı | `1c61fa267827e2452e333acff2b3fe7208756f632d92821d346ebe3a8e8e270a` |
| 82 | `82_e_kapak.py` | v10m → v10n | bitti, zincirde, 2 koşu aynı | `2bd78569c95504a4d0558ba80ada0c74265b11b09fa486547e07d33f33ec47c8` |
| 83 | `83_e_kose.py` | v10n → v10o | bitti, zincirde, 2 koşu aynı | `5b24947154f00d7f6488554b99fb6d9d692097163f26ce29f3fff07144082b2e` |
| 84 | `84_e_parmak_itici.py` | v10o → v10p | **yarım**: son koşuda 10 vida denetimi tutmadı (aşağıda) · `zincir.py`'ye EKLENMEDİ | — |
| 85 | `85_e_besleyici.py` | v10p → v10q | **yazılmadı** | — |

`zincir.py` `SON = "hat3_v10o.glb"`. `SIRA.md`'ye 81–83 satırları **henüz yazılmadı** (SHA'lar yukarıda).
`e1/ent/` altına `hat3_v10m/n/o_ent.json` kopyalandı; `e_parca.py` `ENTF` listesine **henüz eklenmedi**.

Ortak araç: `yama_v9/e_mek_bag.py` (sınıf `Mek`): `vida`, `somunlu`, `motor` (eğik eksen: `merkez3`, `u_vec`), `setskur`, `pim`, `segman`, `somun_mil` (`ince`, `cep`),
`sap_vida`, `yeni` (yeni parça / kaynak, `tur="kaynak"`), `bitir` (denetim → delik → düğüm → kayıt). `pts` öğesi `(u, w)` ya da 3B `(x, y, z)` olabilir.
`vida(..., urun="A")`: A hazır ürün, vida ürünün kendi deliğinden geçer.
Denetim her adımda: baş / somun / segman / yeni parça hacmi boş · her vida tam olarak A + B'yi deliyor (`fazla` / `eksik`) · tutuş ≥ 1 × d · katalog boyu.

Parça adları: `yama_v9/veri/e_mek_parcalar.json` (252 ad). Üreten: `e1/e_mek_adlar.py` (girdi `e1/e_envanter.json`; envanter `e1/e_envanter.py`, `e_bil.pkl` gerekir — `e_cikar.py` üretir).
`e_mek_adlar.py`'de bir satırda `#` yorumundan sonra `ad(...)` yazma: yorum sonraki çağrıları yutar (iki kez başıma geldi).

## 2. Ortam

```
pip install trimesh manifold3d cadquery==2.8.0 scipy rtree numba matplotlib "numpy==2.2.6"
gunzip -c _local/claude_son_yerel/hat3_v10l.glb.gz > <iş>/e2/hat3_v10l.glb        # brifing §3 ile aynı
cd arastirma/_uretec/h3/yama_v9
python zincir.py --is <iş>/zc81 --uretec <depo>/arastirma/_uretec --adim 81-83 --girdi-dizin <iş>/e2
# tek adım doğrulama (iki ayrı klasörde, sonra cmp):
python zincir.py --is <iş>/zc84A --uretec <depo>/arastirma/_uretec --adim 84 --girdi-dizin <iş>/zc81
```
Hızlı deneme (zincirsiz): iş klasörüne girdi GLB + zincirin kurduğu `gece/`, `tg/`, `govde_denetim_dogru.py` kopyalanır, sonra
`YAMA_IS_KOK=<klasör> YAMA_URETEC=<depo>/arastirma/_uretec python yama_v9/84_e_parmak_itici.py hat3_v10o.glb hat3_v10p.glb > _84.log`.
Log süzme: `grep -v "^  vida\|^  yeni parça\|^  setskur\|^  segman\|^  motor \|^  sensör\|^  somunlu\|^  delik:\|^  pim" _84.log`.

Ölçüm araçları (bu klasörde): `probe.py` (ışın boyunca katı aralıkları: `harita(ad, eksen, koord, yön, [(u, w)])`),
`ciz_bolge.py` (bölge görünümleri, 3 izdüşüm), `ciz_aile.py`. Kullanım:
`cd <iş klasörü> && YAMA_IS_KOK=. YAMA_URETEC=<depo>/arastirma/_uretec python <bu klasör>/probe.py hat3_v10l.glb sonda/p85.txt`.
`sonda/` altında 81–85 için tüm sonda girdileri ve çıktıları var (`p85.out` besleyici için hazır ölçümler).

## 3. Adım 84'ün kalan 10 hatası (son log: `sonda/_84_son.log`)

1. `itici_ray_0/1_vida_6` arabayı (araba_0 / araba_2) deliyor: ray vidası başı rayın üstünde kalıyor. Çözüm: ray vidalarına `gomme=5.0` (MGN rayının havşa yuvası; baş rayın içinde).
2. `piston_somun_braketi_vida_0` flanşlı somuna 0,2 mm sürtüyor. Çözüm: noktaları `(4643, 1779)` ve `(4697, 1779)` yap.
3. 6 × `*_z_braketi_tasiyici_vida` "eksik itici_tasiyici": vida taşıyıcının üst flanşını (y 1848–1860,5, z −394…−380) deliyor ama bileşen `itici_tasiyici` kutusuna ait sayılmıyor.
   Önce `denetle_delik` mesajına `bulunan` listesini ekleyip hangi bileşeni deldiğine bak. Büyük olasılıkla flanş ayrı bileşen ve kutusu ad tablosunda yok →
   `e_mek_adlar.py`'de `itici_tasiyici`'ye `ek=[<bileşen no>]` ekle.
4. `parmak_kasnak_setskur` kayıştan geçiyor. Çözüm: setskuru kayışın sarmadığı motor tarafından radyal ver:
   yön `-(0.836, 0.549, 0)`, nokta `kasnak merkezi (4500.8, 1351.9) + 10 × (0.836, 0.549)`, z 12,5 (3B nokta).

Sonra 84'ü iki klasörde koş, `cmp`, `zincir.py`'ye 84 girdisini ekle, `SON = "hat3_v10p.glb"`.

## 4. Adım 85 (besleyici) · ölçülmüş bilgiler (`sonda/p85.out`)

- besleyici plakası 5 mm · 20 × 20 profiller ortası boş · raylar plaka altında 15 mm · sensör tutucu 3 mm L · mil yatağı 36 plakada.
- kasnak / mil setskurları z boyunca, (5130.5, 1356.5) noktasından (z −826 / −356 yüzlerinden).
- motor flanşı x 5142 → `motor(yon=XM, flans=5142, boy_flans=8, kav=4, dis="M4")`.
- motor gövdesi (4 mm flanş + 6 mm taban) sağ saca bağlanacak braket ister (sacda PEM S-M4).
- E3Z sensör tutucuları 3 mm üst plakalar (y 1104–1107 / 1127–1130); sensör altta asılı.
- bitici (itici_b): kızak plakaları 6 mm, arabalar 23,7, kollar 218 boy, kiriş 6 mm (çubuk deliği), kılavuz bloklar U kanal (4,8 duvar) + burç,
  orta blok halka (0,5–11 / 19,1–34,5, x 4795'ten) mil_orta çevresinde, kayış kelepçesi 15 × 42.
- vakum barı 5 mm şeritlerden çerçeve (z −535 / −715 / −795 sıraları, x ≈ 5080 sütunu) · vantuz flanşı 2,3 (4596, −706) · vakum bloğu 12 mm (4885, −790).
  Vantuz sapı → `sap_vida`.
- arayüz saplamaları (`arayuz_mek`, 34 adet, somunsuz): mümkün olanlara somun.
- itici üst braketi / yatak plakası PEM saplamaları, motor bloğu direkleri.

## 5. Sonraki işler (brifing §4.2–§4.6)

1. `SIRA.md` sonuna 81–85 satırları (ne, neden, SHA256, denetimler).
2. `e_parca.py`: `ENTF`'e `hat3_v10m…q_ent.json` ekle. Mekanizma parçalarını `veri/e_mek_parcalar.json` adlarıyla böl (`ek` birleşimleri dahil).
   `sinif()` anahtarlarına `setskur`, `segman`, `pim`, `kaynak` ekle. `burc` rolleri GEÇME.
3. `e_montaj.py`: yalnız `t = koy(USTM, …)` ve `t = koy(ALTM, …)` satırlarını mekanizma mekanizma tezgâh adımlarıyla değiştir.
   Sıra: taşıyıcı profil → ray → kızak → braket → motor → kayış → sensör; her vida `tak()` / `sira_tak()` ile, yön `P[a]['eks']`.
   GEÇİCİ DAYALI metinleri (KURALLAR §2.3 kural 10), kamera `kamera_genel(..., olcek=)`, hedef 3–4 dk.
4. `baglanti_denetim.py`: UNITE satırını sil. GEÇME kategorileri: burç, çatal sensör, vantuz, flanşlı somun, LM12, rulman diski.
5. Denetim (yol 0, son beyansız 0, havada 0, belirme 0, büküm 0, ACIK 0, UNITE 0; GEÇİCİ metinleri var). Sayı kötüleşirse düzelt ya da Kemal'e yaz, yayınlama.
6. Playwright ekran görüntüleri (5–6), `otonom/hat/e-montaj.html` notu (`?v=e3a`, zincir 00–85, açık maddeler).
7. Yeni son model `.glb.gz` → `_local/claude_son_yerel/` · `KOORDINASYON.md` satırı · commit · push · taslak PR.

## 6. Açık maddeler (rapora girecek)

- Köşe tutucular çerçeveye göre 2,77° eğik (üreteç). Bağlantılar eğik eksende kuruldu; üreteçte düzeltilmeli.
- Köşe pistonu vida mili kaplinin içine yalnız 4 mm giriyor → M3 setskur; mil +10 mm uzamalı.
- Köşe tutucu göbeği ↔ mil bindirmesi 4,6 mm (pim bunun içinde).
- İtici vida mili kasnağı göbeği 1,1 mm → radyal Ø3 pim; mil ucuna muylu + kama önerilir.
- Piston başı ↔ piston plakası yalnız köşe temasıyla bitişik → TIG köşe dikişi (3 parça).
- Kalıp orta blok 6 × 6 direkleri (81) üreteç soyutlaması.
- Kapak katlama: dişli kutusu + üst motor tek hazır ürün sayıldı (adaptör yeri yok).
- Flanşlı piston somunu braketle aynı katmanda → GEÇME sayıldı.

## 7. Bu oturumda yapılmamış / dikkat

- Taslak PR açılmadı (Kemal "dur" dedi). Dal push edildi.
- 84'ün yarım betiği depoda ama zincire bağlı değil.
- Büyük ara GLB'ler (300+ MB) depoya konmaz; zincir yeniden üretir (81–83 ≈ 2 dk).
