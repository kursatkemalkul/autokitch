# 06 · GÜVENLİK DEVRESİ — PANO İÇİ UYGULAMA (7 Eki 2026 gece · Claude)

**Asıl belge:** güvenlik oturumu `claude-guvenlik-yerel/_local/guvenlik_ce/02_GUVENLIK_DEVRESI.md` (v2 553a7762): 16 güvenlik fonksiyonu (SF1–SF9 + alt maddeler), PL d/e hesapları (`pl_hesap.py`), TwinSAFE donanımı, `GS_*` sinyal adları. Bu dosya o belgeyi **elektrik projesine yerleştirir**: hangi klemens hangi panoda, STO grupları nasıl kablolanır, acil stop + kapı anahtarları + robot zinciri tek hatta nasıl görünür. Tekrar etmez.

## 1. TEK ŞEMA (acil stop + kapı anahtarları + robot)
```
                                   ANA PANO (U_F) · TwinSAFE EL6910 (FSoE, EtherCAT hat 1 üstünde)
 ACİL STOP XB4BS8442 + 2. NC ───2k──► EL1904-1 ─┐
 RESET (mavi, aydınlatmalı) ────1k──► EL1904-5 │
 A  RSS36 ──────────────────────2k──► EL1904-1 │
 TOPPING RSS36 K1→K2 (seri) ────2k──► EL1904-2 │          ┌─► EL2904-1.1 ──► MS6-SV-E (hava: boşalt / yumuşak dolum)      [SF1 SF2 SF4a SF5]
 F  RSS36 sol→sağ (seri) ───────2k──► EL1904-2 │          ├─► EL2904-1.2 ──► K AZM40 kilit aç (bıçak üst + kilitli + hava boş) [SF4b]
 K  AZM40 (kapalı+kilitli) ─────2k──► EL1904-3 ├─ EL6910 ─┼─► EL2904-1.3/1.4 ──► ROBOT acil stop girişi (2k)                [SF1]
 E  RSS36 ×3 (seri; ust_sag kapısı 121e ile kalktı, 4. kanal KALDIRILDI) ────────────2k──► EL1904-3 │  mantık  ├─► EL2904-2.1/2.2 ──► ROBOT koruyucu durdurma (2k)               [SF7 SF8a]
 HÜCRE KAPISI AZM40 ────────────2k──► EL1904-4 │          ├─► EL2904-2.3 ──► hücre kapısı AZM40 kilit aç (robot duruyor + ray STO) [SF7c]
 ROBOT "sistem acil" çıkışı ────2k──► EL1904-4 │          ├─► EL2904-3.3 ──► QR müşteri mandalları ortak 24 V (röle)       [SF8b İPTAL: perde şalteri yok, bkz. §1b]
 K bıçak üst (1k) + kilit pimi (2k) ► EL1904-5 │          ├─► EL2904-3.4 ──► açıcı emniyet girişi                          [SF6]
 ROBOT "duruyor" çıkışı ────────2k──► EL1904-6 │          └─► FSoE ──► EL2911 (istasyon panolarında) güç grubu kesme = STO:
 QR müşteri kapıları AZM40 ×12 (seri) ►2k──► EL1904-6 │                 TOPPING(+F bant) · K · E · RAY · QR kapak            [SF1 SF2 SF3 SF4a SF5 SF7 SF8c]
```
- Her 2k = iki kanal, test darbeli (EL1904 çıkış test sinyalleriyle çapraz devre tespiti).
- EL2911: istasyon panosunda, o istasyonun 48 V (ya da 24 V) motor beslemesi EL2911'in güç kontaklarından geçer; grup kesilince EL70xx/EL7342/EL7211 terminalleri güçsüz kalır (STO). Beckhoff "etkileşimsiz terminal" listesi kontrolü eksen oturumunda (AÇIK).
- Fırın ısıtması güvenlik zincirinde değil (SF1: sıcak fırın tehlike yaratmaz) — DO_F_ISITICI standart PLC'den.

## 1b. QR ZİP-PERDE · SF8d (9 Eki 2026 · YÖNETİCİ SON KARAR: şaltersiz)
- **SF8d:** herhangi bir müşteri kapısı kilitsizken robot QR yüz bölgesi dışında ya da <= 250 mm/s (PLr d). Zincir: 12 × AZM40 (müşteri kapısı kilidi + kilit izleme, seri) → EL1904-6 (W047) → EL6910 → EL2904 → UR10e güvenli giriş (indirgenmiş mod düzlemi), Kat 3.
- **İPTAL:** perde konum şalteri (modele sığmıyor), W048 (12 × 2NC), SF8b (robot kapağı açıkken mandal gücü kesik), EL1904×6 / EL2904×3 ek modülleri GEREKMEZ — mevcut EL1904-6 / EL2904 çıkışı kullanılır.
- **Enkoder** (Faulhaber 2342 + EL7342) güvenlik zincirinde DEĞİL: program çapraz kontrolü (alt konum ↔ uç sensörü çelişkisi / kapanmama → `PERDE_TUTARSIZ`, o göz kilitli). (c) 'yalnız enkoder' tek başına PL <= b → yetmez (hesap 07).
- **PL d**, PFHd ≈ 2,0E-7 (UR10e girişi %91) — `perde_pl_hesap.py` → `07_QR_PERDE_PL_HESABI.md` (PLr risk grafiği, kaynaklar).
- **Kalan risk:** yırtık / delik perde hiçbir güvenlik elemanıyla görülmez → açılış listesi 'perde sağlam' maddesi (HMI).
- **İSTEK (Robot oturumu):** UR güvenlik yapılandırması: bu girişte QR yüz bölgesi sınırı + indirgenmiş mod 250 mm/s.

## 2. KABLOLAMA (bkz. 04 · W030–W050)
| Zincir | Kablo | Yol | Not |
|---|---|---|---|
| Acil stop (TEK buton, **F sağ üst kapak** — adım 58, x 3625 / y 1600, yerden 1,60 m; güvenlik v3 7893d385) + reset | W040 ÖLFLEX 110 CY 7G0,5 · istasyon F | kapağın menteşe tarafından esnek döngü → F kutusu → ana pano (ikisi de U_F içinde) | KARAR (E oturumu 7 Eki): tek buton, modeldeki yer F sağ üst kapak; KURALLAR §6'daki "B ön kapağı" metni hatalı (düzeltme E oturumunda). Buton XB4BS8442 + 2. NC (ZBE102); kapak açıkken de erişilebilir / çalışır. |
| A RSS36 | W045 M12 8 pin | A|TOPPING dikme içinden (A boş kabuk kuralı) | A+B oturumu küçük iş |
| TOPPING / F / E RSS36 zincirleri | W041 W042 W044 | istasyon iç kanalı → üst hat → ana pano | zincir ≤ 30 m, 31 sensör |
| K AZM40 | W043 | K panosu üstünden ana panoya (kilit bobini EL2904'ten) | |
| Hücre kapısı AZM40 | W046 | Codex ince duvar → zemin üstü kanal | |
| Robot güvenlik I/O | W030 W031 ekranlı | ana pano ↔ robot kutusu (QR rezerv bölmesi), Cat.6A yanında | FR5: 16 DI/16 DO + güvenlik girişleri çift kanal (NPN varsayılan; PNP için geniş gerilimli 2 kW kutu) [K] — Codex teyit |
| QR müşteri kapıları AZM40 ×12 seri zincir (W047) | W047 | QR içi orta dikey kanal | 9 Eki: RSS36 yerine AZM40 (kilit + izleme); W048 İPTAL |
| MS6-SV-E | W049 | ana pano → F üst kabin kompresör çıkışı | ayda ≥ 1 test çevrimi (DO_HAT_HAVA_TEST_ISTEK) |

## 3. BESLEME
- Güvenlik cihazları 24 V PELV, ana panoda ayrı sigorta (X3:3-4, 2 A); QUINT4-CAP ile kesintide reset gerekmeden kapanma.
- EL2911 grup beslemeleri her istasyonun kendi NDR'sinden (TOPPING 2 × NDR-240-48 → 2 × EL2911 — iki kaynak paralellenmez, her kol kendi güvenli çıkışı; E 2 × NDR-240-24 → 2 × EL2911 (9 Eki 24 V), K NDR-120-24, QR NDR-120-24, RAY NDR-480-48).

## 4. AÇIK
1. ~~Acil stop yeri~~ KAPANDI: F sağ üst kapak (adım 58; KURALLAR §6 metni düzeltilecek).
2. EL2911 ↔ EL70xx uygunluğu ve E'de grup sayısı (eksen oturumu).
3. Robot modeli (FR5 / UR10e) ve güvenlik I/O tipi (Codex).
4. Açıcı emniyet girişi şartnamesi (PL d, PFHd ≤ 5E-7) satın alma şartnamesine.
5. Bölge bölge hava boşaltma istenirse istasyon başına valf (model değişikliği).
