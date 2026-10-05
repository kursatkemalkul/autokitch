# AUTOKITCH · Claude + Codex ortak çalışma kuralları

Kemal'in kararı (5 Eki 2026): iki ajan aynı anda, farklı istasyonlarda çalışır. Depo düzenlemesi proje bitince yapılacak; o zamana kadar dosya taşınmaz.

**İşe başlamadan `KURALLAR.md`'yi oku** (üretilebilirlik, montaj animasyonu, makine emniyeti / hijyen, Kemal kararları). Bitirince oradaki §5 denetimini çalıştır; tutmazsa yayımlama.

## 1. Kim neyi yapıyor (çalışmaya başlamadan önce bu tabloyu güncelle, commit + push et)

| İş | Kim | Branch | Durum |
|---|---|---|---|
| Robot + ray + QR dolabı + sipariş animasyonları | Codex | `coord/codex-main-integrated-robot-v17` | çalışıyor |
| TOPPING montaj animasyonu v5 | Claude | `claude/topping-montaj-v5` | yayında (açık 3 küçük madde) |
| Standart önlemleri · makine (STANDART_DURUM.md madde 1, 3–8, 12–14): acil stop B ön kapağı, kapı kilit anahtarları, A ışık perdesi kablosu, hava boşaltma, R290 bölmesi, F filtresi, hijyen noktaları — zincir 58+ | Claude | `claude/standart-makine` | sırada |
| TOPPING bağsız 63 parça + geçici dayalı 2 parça (KURALLAR §2.3 kural 10) | Claude | `claude/topping-montaj-v5` | sırada |
| Standart önlemleri · robot + QR (madde 10–11): hücre kapısı emniyet anahtarı, robot gözdeyken QR müşteri kapısı kilitli + geri bildirim | Codex | `coord/codex-robot-qr-safety-v1` | çalışıyor: emniyet mantığı + güvenli I/O arayüzü; makine/zincir değişmez |
| Güvenlik devresi şeması (acil stop + kapı anahtarları + robot, tek röle / güvenlik PLC) | Claude + Codex | — | makine anahtarları bitince |

Bir işe başlamadan önce tabloda başka bir ajanın aynı istasyonu ya da aynı dosyaları almadığını kontrol et.

## 2. Dosya sahipliği

- Her ajan yalnız kendi işinin dosyalarına yazar. Başkasının alanındaki dosyayı değiştirmek gerekirse önce Kemal'e sorulur.
- Codex'in alanı: `arastirma/_uretec/robot_integrated_v17/`, `otonom/hat/robot-integrated-v17/`, `otonom/hat3d/robot-integrated-v17/`, `otonom/hat/makine.html`.
- İstasyon montaj animasyonu alanı (istasyonu alan ajanın): `otonom/hat/<ist>-montaj.html`, `otonom/hat3d/v3/<ist>_montaj/`, kendi üreteç klasörü.
- Ortak dosyalar (`otonom/hat/ist_montaj/montaj-oynatici.js`, `otonom/hat/hat.css`, `index.html`): değiştirmeden önce tabloya not düş, değişikliği küçük tut, geri uyumlu yap.

## 3. Model zinciri (`arastirma/_uretec/h3/yama_v9/zincir.py`) — aynı anda tek yazar

- Zincire yeni adım (58, 59 …) yalnız bir ajan yazar. Yazmaya başlamadan bu dosyanın en altındaki **ZİNCİR KİLİDİ** satırını kendi adınla doldur, commit + push et; adım bitince (iki koşu bayt aynı, SIRA.md kaydı) boşalt.
- Kilit doluyken öteki ajan model değiştirmez; gerekiyorsa kilit sahibine / Kemal'e yazar.
- Son model: `_local/claude_son_yerel/hat3_v9y.glb.gz` (adım 57). Yeni adım çıkınca bu satır güncellenir.

## 4. Branch, birleştirme, yayın

- Her iş kendi branch'inde: `claude/<iş>` ya da `codex/<iş>`. Force push yok. Başkasının branch'ine push yok.
- Main'e yalnız yayınlanacak dosyalar birleştirilir; birleştiren, öteki ajanın main'deki değişikliklerini korur (merge, rebase değil).
- Site `kk-archive` deposundaki `deploy` iş akışıyla yayınlanır; autokitch'e push etmek siteyi güncellemez. Main'e birleştirdikten sonra iş akışı elle tetiklenir:
  `gh api -X POST repos/kursatkemalkul/kk-archive/actions/workflows/deploy.yml/dispatches -f ref=main`
- `_local/` siteye kopyalanmaz (güvenlik). Sitede gereken hiçbir dosya `_local/` altına konmaz.

## 5. Güvenlik

- Depo herkese açık. Oturum kayıtları `_local/claude_oturum/` altında durur (Kemal: kalsın); `_local/` siteye kopyalanmaz. Parola, anahtar, kişisel bilgi depoya konmaz.
- Büyük ara dosyalar (`.pkl`, 100 MB üstü GLB) depoya konmaz; GLB gerekirse kayıpsız `.gz` olarak.

ZİNCİR KİLİDİ: Claude · adım 58 (acil stop, F sağ üst kapak) · 5 Eki 2026
