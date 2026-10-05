
## ADIM 37 v2 · TOPPING GÖVDESİ DÜZELTMELERİ (4 Eki 2026 · Claude · Kemal onayı) — adım 37 artık `h3_topping_sac_v2` çağırır

Üreteç `h3/h3_topping_sac_v2.py` (v1 DEĞİŞMEDİ, üstüne yazılmadı). Zincir 37 → 50 bu üreteçle yeniden koştu (37'den sonraki betikler değişmedi).

| # | değişiklik | nasıl |
|---|---|---|
| D1 | servis sacı 17 havşa vidası | servis sacı + arkadaki dönüş flanşı birlikte **çökertilir (dimple)**, iç içe koni (DIN 7991 baş konisiyle aynı) · dış yüz düz · dönüşteki PEM SP-M5 yerine **kaynak burcu M5 Ø14 × 9** (alt yüzü dimple'a havşalı, 2 punta) · vida DIN 7991 M5 × 6 → **M5 × 12** (ucu burcun arka yüzünde, diş 6,75) |
| D2 | soğuk oda iç sacı | 4 düz sac + TIG YERİNE **bükümlü kenarlı** 4 sac (304 1,0 · iç R 3): sol / sağ arka kenarı arka iç sacın arkasına (raf ve üst raf hizasında kesik), üst kenarı tavan iç sacının üstüne, ön kenarı çerçevenin arkasına · tavan arka kenarı aşağı, ön kenarı yukarı · arka iç sac düz · **48 perçin**: 28 × ISO 15983 Ø3,2 içeriden + 20 × ISO 15984 havşa Ø3,2 çerçeveden (yüzeyle aynı düzlem) · her perçinde **POM-C ısı kesici pul Ø9 × 1** · gıda tarafı 7 köşe silikon fitili + 3 ön derz · PU yerinde köpük DEĞİL: **4 kesilmiş levha** (arka / sol / sağ / tavan; flanş, perçin, pul yuvaları açık) + dış saca 0,5 mm **yapıştırıcı** (eski zincir_T_tamamla T2 artık üreteçte) |
| D3 | evaporatör ayakları | servis sacındaki 4 sekme (v8zq TOPPING_MODUL__sac 87 / 88 / 94 / 95, DEGISEN ile silinir) yerine aynı düzlemde **2,5 mm L ayak** (kaset gövdesine üreticide kaynaklı) → kuru bölme tabanına **ISO 7380 M5 × 6 → PEM SP-M5-1** · servis sacı tek başına sökülür · evaporatör yeri aynı |
| D4 | kondenser kanalı | kuru bölme tabanında Ø32,8 delik yerine **135 × 33 geçiş deliği** (dirsekli boru taban inerken içinden geçer) + **kanal geçiş kapağı** 1,5 (sağdan açık yarık, 2 × ISO 7380 M5 → PEM) |
| T1 | TOPPING → B pulu | DIN 9021 → **ISO 7092 Ø15** (Ø16 servis deliğinden geçer) |

Denetim: g2g (gövde ↔ gövde, yeni parçalar) yalnız beyanlı (FHP gömme başı, burç punta kaynağı) · yeni parçalar ↔ model 0 (A M8 uçları 37'de yuva açılır; POM burç ↔ PU levha çiftleri v1'den beri aynı gömülü kesit) · topping_sac_denetim_v2 (scratchpad gece2/t3/den2).
Montajı engelleyen diğer maddeler model değişikliği İSTEMEDİ (animasyonda çözüldü): kaşar / sucuk çıkış ağzı ve mandal gövdeye ait sabit parça (alttan / yukarıdan), kaset önden dil kanalında sürülür (dil kanalı zaten önden açık yuva) · sos / harç: çıkış borusu + yayıcı alttan kovana, hortum üst raf deliğinden, mevcut kelepçe ile bağlanır · X ekseni parçalı: motor kuru bölme adımında yukarıdan köşeye, raylar + araba A tarafından · raf PU levhası köşebentten önce yukarıdan.
