# TEK ÇEKMECE MONTAJ PLANI — B dolabı · K2 sütunu · 3. sıra (CEK_K2_lahm_3)

Model: hat3_v9j.glb · koordinat: x = sol→sağ, y = yukarı, z = ön (+) / arka (−) · ölçüler mm.
Bölme: sol bölme sacı x 1453,5 · sağ bölme sacı x 2073,5 · arka duvar z −790 · ön çerçeve z 23 (açıklık y ≈ 416–491).
Çevre (silik, hareketsiz, kutuya kırpılmış): bölme sacları + PU, arka duvar, ön çerçeve, B_MODULER dikmeleri, kablo kanalları,
PEM SP-M5 somunları, köpük kapakları, soğutma (evaporatör). Tezgâh: x 1520–2010, üst y 421,5, z 330–900.

Model gruplarının bölünmesi: CEK_K2_lahm_3 düğümleri bağlı bileşenlere ayrıldı (sabit / ara / iç ray, lamalar, braketler, kasnaklar,
reed'ler). Birleştirilenler (tek katalog parçası): step motor = gövde + mil + arka kapak + kablo rakoru; avara kasnağı = kasnak + mili.
avara braketi + sensör laması modelde tek kaynaklı parça (ortak köşeler) — tek parça bırakıldı.

| # | Parça | Geliş yönü (başladığı yer → hareket) | Neye oturur | Bağlantı |
|---|---|---|---|---|
| 1 | Motor braketi | tezgâhta, 120 yukarıdan → aşağı | tezgâh | — (alt montaj) |
| 1 | Step motor (+mil, arka kapak, rakor) + flanş | tezgâhta, +x 60 → −x, motor ekseninde | motor braketi | flanş vidaları |
| 1 | GT3 motor kasnağı | tezgâhta, −x 30 → +x, mil ekseninde | motor mili | setskur |
| 2 | Motor grubu (4 parça) | tezgâh (+x 150, −y 3, +z 1300) → 3 mm kalkar → −x 150 → −z 1300, ön çerçeve açıklığından | arka duvar | braket cıvataları |
| 3 | Sensör plakası | 40 yukarıdan → aşağı | arka duvar | cıvata |
| 3 | Sabit ray sol / sağ | +z 800 önden, çerçeve açıklığından → −z; sonra ±10 yandan → bölme sacına | bölme sacı | (4) vidalar |
| 4 | 6 × M5 × 10 havşa başlı | ray içinden ±40 → kendi ekseninde (x) | ray deliği → PEM SP-M5 | vida dişi PEM'e |
| 5 | Avara braketi + sensör laması | bölme içinden +x 30 → −x | sol bölme / ön çerçeve arkası | kulak cıvatası |
| 5 | Reed sensör arka / ön | 20 aşağıdan → yukarı | sensör lamasının altı | vida |
| 6 | Ara ray sol / sağ | +z 760 önden → −z, RAY EKSENİ boyunca | sabit rayın içi | bilyalı kafes |
| 7 | Çekmece gövdesi (sac tava) | tezgâh, 150 yukarıdan → aşağı | tezgâh | — |
| 7 | Silikon tepsi | 120 yukarıdan → aşağı | gövde tabanı | serbest |
| 8 | Kızak laması sol / sağ | ∓40 yandan → gövde yanına | gövde yan yüzü | vida |
| 8 | Kızak sol / sağ (iç profil) | ∓40 yandan → lamaya | kızak laması | vida |
| 8 | Kayış kelepçe laması | 40 yukarıdan → aşağı | gövde sol yüzü | vida |
| 8 | Mıknatıs yuvası | 40 yukarıdan → aşağı | kayış laması üstü | vida |
| 8 | Ön kapak braketi sol / sağ | +z 40 önden → −z | gövde ön yüzü | vida |
| 9 | ÇEKMECE (10 parça, tek grup) | tezgâh (+z 900) → −z 900, RAY EKSENİ boyunca düz | kızak ara rayın içinde, profil hizalı | ray |
| 10 | Avara kasnağı + mili | +z 60 önden → −z | avara braketi | mil cıvatası |
| 10 | GT3 kayış | yerinde sarılır (istisna, aşağıda) | iki kasnak + kelepçe | kelepçe, gergi |
| 11 | Ön panel | +z 240 önden → −z | ön çerçeve + ön braketler | vida |
| 11 | Ön kapak (şeffaf) | +z 240 önden → −z | ön panel / braketler | — |
| 12 | Reed kabloları + motor kablosu | kanal boyunca çekilir (istisna) | ELK_IC kanalı → dikey kanal | — |

Sıra gerekçeleri (denetimin bulduğu kısıtlar):
- Motor bölmenin içinde braketine HİÇBİR yönden giremiyor: braket motoru ≥ 15 mm sarıyor; tek açık yön +x ise dikey kablo
  kanalı (x 1643,5) kapatıyor → motor grubu tezgâhta kurulur, tek parça girer.
- Motor kasnağı mile soldan takılır → sol ray takılmadan önce (ray takılınca kasnakla bölme arasında 7 mm kalıyor; kasnak 11 mm).
- Kayış laması ön avara kasnağının üstünden geçemez (y 458–466,5 ↔ kasnak y ≤ 463,5) → avara kasnağı çekmeceden SONRA.
- Kapalı GT3 kayış iki flanşlı kasnağa rijit hareketle takılamaz (topolojik) → kayış en son sarılır.
- Avara braketinin kulağı çerçevenin arkasında (y 492,5–512,5) → braket önden giremez, bölmenin içinden yana kayarak gelir.
- Sağ sabit ray yana 25 mm açıkken evaporatöre (x ≤ 2053,5) çarpıyordu → yan pay 10 mm.
