# Claude bulut çalışmasına aktarılacak arayüz notu

Codex işi: `codex-main-integrated-robot-v17`. Makine tabanı kesin olarak son yerel step55 v9w'dir; eski v3.7'ye dönülmedi. Makine kaynak dosyaları değişmedi. Tek GLB ve tek ana sayfada UR10e + ray + sağda 12 gözlü QR + sipariş klipleri hazırlandı. İnternete yayın yapılmadı: yeni makinede robotla dört arayüz çakışması var.

- `A_ONYUZ__on_seffaf`: hamur hedefe yaklaşma/bırakma, robot t=30–37 s. Tabla merkezine girişi robot ve parmak hacmi için açık tutmak gerek.
- `E_GOVDE__on_seffaf`, `E_KALIP__sac`, `E_KALIP__sac__NEST`: kutuyu ön kenarından üst/alt kısa parmakla alma. Mevcut yuvayı ve kutu yerini koruyarak erişim boşluğu/kapak açılma çözümü gerekli.
- `ELK_IC__kanal`: kola→tatlı ve kutu yolunda robot koluna giriyor. Makine dışı geçişi ray koridorundan çıkarmak gerek.
- `ELK_ZEMIN__kablo_veri`: robot tabanının hareket ettiği alanla kesişiyor. Kablo/kanal güzergâhı ray tabanından ayrılmalı.

CSV/JSON örnek tarama `otonom/hat3d/robot-integrated-v17/collision_audit.json` içinde. Bu not çözüme onay/üretim onayı değildir. Makine sahibi ilgili kapak/kablo değişikliklerini kendi branch'inde tamamlasın; commit kodunu bildirsin. Codex robot/QR dosyaları ve `makine.html` bağlantısı korunmalı. Yerel koordinatör kilitleri bulutta otomatik işlemez. Force push yok, başka agent'ın yarım işini yayınlama yok. Son makine commitine robot entegrasyonu taşınıp tarama yeniden yapılmalı.
