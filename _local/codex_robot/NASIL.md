# Son robot + QR çalışması

Robot kaynağı `codex-main-robot-v16`, commit `ec6bff4bb35e7f17084caa249b084b2c00f6db83`. UR10e gerçek eklem çerçeveleri + Robotiq gövdesi + ortak kısa turkuaz parmaklar. `assets/ur10e_short.glb`, `assets/rig.json`, `viewer/rig.js`. URDF/STEP bu web çalışmasının kaynağı değildir; mevcut GLB ve eklem verisi eksiksiz saklandı.

Makine: son yerel step55 v9w, SHA256 `346fd56761bf5e7d4b7810316d31e56d7d5c8f01ac8b5e0d5e4826cf0f781a13`. Eski v16 denetimi eski makinedeydi; son makine denetimi ayrı yapıldı ve henüz GEÇMEDİ.

## Koordinatlar

Web/ana GLB: metre, Y yukarı, X hat boyunca; Z robot tarafına pozitif. CAD mm değerini 1000'e böl. Isaac FK: metre, Z yukarı; web dönüşümü `(x,y,z) -> (x,z,-y)`. Eklem açıları radyan, çene komutu derece. Ray araba X mutlak metredir.

Ray 936–5100 mm, robot rayı 500 mm öne alınmış, montaj adaptörü ayrıca 100 mm öne uzanır. Taban montaj kotu 130 mm. `assets/isaac_handoff_v16.json` tam q/rail/jaw ve koordinat sözleşmesidir. QR: X 3757–5230 mm; robot yüzü Z 1750 mm; derinlik 324 mm, 3 sütun × 4 sıra, raf tabanları 588 / 850 / 1112 / 1374 mm, üst 1636 mm.

`assets/qr_grid_v13.json` QR geometrisi ve erişim uçlarıdır. `assets/order_v16.json` 11857 zaman damgalı robot pozu; `assets/workflow_v16.json` sipariş olayları ve hız sınırları. `sources/` üreteç ve denetimler, `viewer/` web kinematik ve oynatma kodu. Tarihsel denemeler ayrı isimleriyle korunur; bir geçmiş JSON'un PASS olması son makine için PASS değildir.

## Birleşmiş oynatma

Ana sayfa aynı `otonom/hat/makine.html`; yeni GLB `otonom/hat3d/robot-integrated-v17/hat3_robot_v17.glb.gz`. Makine + robot + QR AYNI GLB dosyasında; ayrı sahne değildir. Gzip açılır, SHA256 kontrol edilir; `siparis_birlesik_*` klipleri oynatılır. `oynat`, süre çubuğu, hız düğmeleri ve serbest kamera kullanılır. Son makinenin 6 özgün klibi de GLB'de durur. Üreteç `arastirma/_uretec/robot_integrated_v17/build.mjs`; `MACHINE_NATIVE` doğrulanmış ham GLB yolunu göstermeli. Hedef ürünler rijit/ideal tutuş; düşme veya fiziksel kavrama doğrulaması yok.

## Yayını engelleyen mevcut arayüzler

A tabla ön saydam kapağı; E ön kapak + sac kalıp; `ELK_IC__kanal`; `ELK_ZEMIN__kablo_veri`. Somut örnekler `otonom/hat3d/robot-integrated-v17/collision_audit.json`. Claude'un makine dosyalarına dokunulmadı. Bu birleşik sürüm YAYINLANMADI; taslak inceleme içindir.
