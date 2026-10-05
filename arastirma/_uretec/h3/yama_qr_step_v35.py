# -*- coding: utf-8 -*-
"""YAMA v3.5 (1 Eki 2026 · Claude · YEREL) — h3_elk_qr_v1.py: QR ANA PANOSUNDAKİ 5 DIN CİHAZI KUTU YERİNE ÜRETİCİ STEP'İ.
  · ana_salter_iSW_4P_40A          → Schneider A9S65440 (a9s65440.stp)
  · kacak_akim_iID_4P_40A_30mA     → Schneider A9R21440 (a9r21440.stp)
  · guc_24V_NDR-120-24             → MEAN WELL NDR-120-24 (ndr-120-24.stp)
  · hmi_ana_bilgisayar_RevPi_Connect_4 → KUNBUS PR100378 (pr100378_without_wlan.stp · PR100378 = WLAN'sız)
  · ag_anahtari_FL_SWITCH_1008N    → Phoenix Contact 1085256 (1085256.stp)
  · sigorta_iC60N_1PN_C16_* (A9F79616) KUTU KALIR: "ZARF — katalog STEP'i bulunamadı (kod teyit)"
  · iki ray GERÇEK genişliklerle yeniden dizilir (çakışma yok) · parça adları AYNI · BOM satırları "üretici STEP (dosya, kaynak URL) · gerçek ölçü"
  · yükleyici: h3/katalog_step_v1.py (önbellek h3/_katalog_cache/*.brep · STEP'ler arastirma/katalog/step'e konmalı; önbellek varsa STEP gerekmez)

KULLANIM
  python yama_qr_step_v35.py                 → h3_elk_qr_v1.py yerinde yamalanır (önce _elk_qr_v1_onceki_v34.py yedeği)
  python yama_qr_step_v35.py --kontrol       → yalnız uygulanabilir mi bakar (dosyaya dokunmaz)
  python yama_qr_step_v35.py --hedef X.py    → yamalı metin X.py'ye yazılır, kaynak dokunulmaz (test_qr_step_v35.py böyle kullanır)
SONRA: h3_elektrik_v1.py (kur + denetim + kaydet) → montaj (EL.yukle önbellekten) — bu yama onları ÇALIŞTIRMAZ."""
import io, os, sys
sys.dont_write_bytecode = True
D = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(D, "h3_elk_qr_v1.py")
YEDEK = os.path.join(D, "_elk_qr_v1_onceki_v34.py")
ISARET = "import katalog_step_v1 as KS"

ESKI_CIHAZ = '''    xa = x0 + 17.0
    din("ana_salter_iSW_4P_40A", xa, 72.0, 90.0, 70.0, RAY_A_Y, bom=("Ana şalter Schneider Acti9 iSW 4P 40 A", 1, "katalog [ölçü VARSAYIM]", "bina beslemesi 400 V 3F"))
    din("kacak_akim_iID_4P_40A_30mA", xa + 72.0, 72.0, 90.0, 75.0, RAY_A_Y, bom=("Kaçak akım Schneider Acti9 iID 4P 40 A 30 mA tip A", 1, "katalog", ""))
    SG = ["TOPPING", "DOLAP", "K", "E", "ROBOT", "QR"]
    for i, s in enumerate(SG):
        din("sigorta_iC60N_1PN_C16_%s" % s, xa + 144.0 + 36.0 * i, 36.0, 90.0, 75.0, RAY_A_Y,
            bom=("Sigorta Schneider Acti9 iC60N 1P+N C16", len(SG), "katalog", "istasyon başına 1 · fazlara dengeli dağıtım") if i == 0 else None)
    din("guc_24V_NDR-120-24", xa, 40.0, 125.2, 113.5, RAY_B_Y, bom=("Mean Well NDR-120-24", 1, "föy 40 × 125,2 × 113,5", "ana bilgisayar + switch + modem (UPS çıkışından)"))
    din("hmi_ana_bilgisayar_RevPi_Connect_4", xa + 46.0, 45.0, 96.0, 110.5, RAY_B_Y, "cihaz_koyu",
        bom=("ANA BİLGİSAYAR Kunbus Revolution Pi Connect 4 (Raspberry Pi CM4 tabanlı endüstriyel, EKRANSIZ, DIN, 24 V, 2 × Ethernet, RTC, WDT)", 1, "katalog [ölçü VARSAYIM]",
             "sipariş sırası + istasyon koordinasyonu + web paneli (iPad / telefon: modemin Wi-Fi'ı ya da uzaktan VPN) · PLC'lerle Ethernet (S7 / Modbus TCP)"))
    din("ag_anahtari_FL_SWITCH_1008N", xa + 97.0, 35.0, 99.0, 105.0, RAY_B_Y, "cihaz_koyu",
        bom=("Endüstriyel switch Phoenix Contact FL SWITCH 1008N (8 × RJ45)", 1, "katalog [ölçü VARSAYIM]", "ana bilgisayar · 4 istasyon PLC · robot · QR kartı · modem"))
    for i in range(16):
        din("klemens_PT2_5_%02d" % i, xa + 140.0 + 5.2 * i, 5.2, 60.0, 45.0, RAY_B_Y, bom=("Klemens Phoenix PT 2,5 (+ PE)", 16, "", "") if i == 0 else None)
'''

YENI_CIHAZ = '''    # v3.5 (1 Eki · Claude · YEREL) · ÜRETİCİ STEP'LERİ: 5 cihaz kutu değil gerçek katı (h3/katalog_step_v1.py · önbellek h3/_katalog_cache) ·
    #   cihazın ray oluğu rayın önüne (RAY_Z[0] 887,5) ve ortasına oturur · sol kenar = verilen x · raylar GERÇEK genişlikle yeniden dizildi (adlar aynı)
    #   dizilim (gerçek genişlik): ray A  iSW 4612,0–4682,8 · iID 4683,8–4755,5 · 6 × iC60N 4756,5–4972,5 (ray 4607–4983)
    #                              ray B  NDR 4612,0–4652,0 · RevPi 4658,0–4703,0 · switch 4709,0–4731,5 · 16 klemens 4739,5–4822,7
    import katalog_step_v1 as KS

    def din_step(ad, kod, xa, yc, mal="cihaz", bom=None):
        """üretici STEP'i (KS.cihaz_step: önü −z, kapağa bakar) · döner: cihazın sağ kenarı (xa + gerçek genişlik)"""
        ekle(ad, KS.cihaz_step(kod, xa, yc, RAY_Z[1], yon=-1), mal, B1, bom)
        return xa + KS.olcu(kod)[0]
    ARALIK_A = 1.0                                         # ray A: Acti9 cihazları arası (gerçek genişlik + 1 ≈ 9 mm modül adımı · iC60N kutuları bitişik, v3.4 gibi)
    ARALIK_B = (6.0, 6.0, 8.0)                             # ray B: v3.4 dizilişindeki boşluklar korunur (NDR | RevPi | switch | klemens)
    xa = x0 + 17.0
    # ---- ray A (y RAY_A_Y): iSW 4P · iID 4P · 6 × iC60N 1P+N
    xs = din_step("ana_salter_iSW_4P_40A", "A9S65440", xa, RAY_A_Y,
                  bom=("Ana şalter Schneider Acti9 iSW 4P 40 A (A9S65440)", 1, KS.bom_kaynak("A9S65440"), "bina beslemesi 400 V 3F"))
    xs = din_step("kacak_akim_iID_4P_40A_30mA", "A9R21440", xs + ARALIK_A, RAY_A_Y,
                  bom=("Kaçak akım Schneider Acti9 iID 4P 40 A 30 mA tip A (A9R21440)", 1, KS.bom_kaynak("A9R21440"), ""))
    SG = ["TOPPING", "DOLAP", "K", "E", "ROBOT", "QR"]
    xg = xs + ARALIK_A
    for i, s in enumerate(SG):
        din("sigorta_iC60N_1PN_C16_%s" % s, xg + 36.0 * i, 36.0, 90.0, 75.0, RAY_A_Y,
            bom=("Sigorta Schneider Acti9 iC60N 1P+N C16 (A9F79616)", len(SG), "ZARF — katalog STEP'i bulunamadı (kod teyit) · kutu 36 × 90 × 75 [VARSAYIM]",
                 "istasyon başına 1 · fazlara dengeli dağıtım") if i == 0 else None)
    # ---- ray B (y RAY_B_Y): NDR-120 · RevPi Connect 4 · FL SWITCH 1008N · 16 klemens
    xb = din_step("guc_24V_NDR-120-24", "NDR-120-24", xa, RAY_B_Y,
                  bom=("Mean Well NDR-120-24", 1, KS.bom_kaynak("NDR-120-24"), "ana bilgisayar + switch + modem (UPS çıkışından)"))
    xb = din_step("hmi_ana_bilgisayar_RevPi_Connect_4", "PR100378", xb + ARALIK_B[0], RAY_B_Y, "cihaz_koyu",
                  bom=("ANA BİLGİSAYAR Kunbus Revolution Pi Connect 4 PR100378 (4 GB RAM · 32 GB eMMC · WLAN'sız · Raspberry Pi CM4 tabanlı endüstriyel, EKRANSIZ, DIN, 24 V, 2 × Ethernet, RTC, WDT)", 1,
                       KS.bom_kaynak("PR100378"),
                       "sipariş sırası + istasyon koordinasyonu + web paneli (iPad / telefon: modemin Wi-Fi'ı ya da uzaktan VPN) · PLC'lerle Ethernet (S7 / Modbus TCP)"))
    xb = din_step("ag_anahtari_FL_SWITCH_1008N", "1085256", xb + ARALIK_B[1], RAY_B_Y, "cihaz_koyu",
                  bom=("Endüstriyel switch Phoenix Contact FL SWITCH 1008N (1085256 · 8 × RJ45)", 1, KS.bom_kaynak("1085256"), "ana bilgisayar · 4 istasyon PLC · robot · QR kartı · modem"))
    xk = xb + ARALIK_B[2]
    for i in range(16):
        din("klemens_PT2_5_%02d" % i, xk + 5.2 * i, 5.2, 60.0, 45.0, RAY_B_Y, bom=("Klemens Phoenix PT 2,5 (+ PE)", 16, "", "") if i == 0 else None)
'''

ESKI_DOC = '''kangal ile sağ yan sac arası) → giriş (b) toplama kutusu (tekmeliğin arkası, kangalın önü) · hepsi 304 1,5, 60 yüksek, üstten kapaklı."""'''
YENI_DOC = '''kangal ile sağ yan sac arası) → giriş (b) toplama kutusu (tekmeliğin arkası, kangalın önü) · hepsi 304 1,5, 60 yüksek, üstten kapaklı.
v3.5 (1 Eki 2026 · Claude · YEREL) — ANA PANO CİHAZLARI ÜRETİCİ STEP'İ (Kemal: "motor koy deyince kutu modelleyip bırakıyorsun" → gerçek katalog parçası):
  iSW A9S65440 · iID A9R21440 · NDR-120-24 · RevPi Connect 4 PR100378 (WLAN'sız) · FL SWITCH 1008N 1085256 → h3/katalog_step_v1.py (yön + ray oluğu tablosu,
  görünmeyen iç katılar atılır, dış ölçü aynı) · raylar gerçek genişliklerle yeniden dizildi · iC60N 1P+N C16 (A9F79616) ZARF kaldı (katalog STEP'i bulunamadı)."""'''

R = [(ESKI_CIHAZ, YENI_CIHAZ), (ESKI_DOC, YENI_DOC)]


def yamali(s):
    """yamalı metni döndürür (her eski parça tam 1 kez geçmeli)"""
    assert ISARET not in s, "zaten yamalı (katalog_step_v1 içe aktarılıyor)"
    for a, b in R:
        n = s.count(a)
        assert n == 1, ("eşleşme sayısı %d (beklenen 1) · dosya değişmiş olabilir" % n, a.strip().splitlines()[0][:100])
        s = s.replace(a, b)
    return s


def uygula(kaynak=KAYNAK, hedef=None, kontrol=False):
    s = io.open(kaynak, encoding="utf-8").read()
    if ISARET in s and hedef is None:
        print("h3_elk_qr_v1.py zaten yamalı — bir şey yapılmadı"); return None
    y = yamali(s)
    compile(y, hedef or kaynak, "exec")                                               # sözdizimi denetimi
    if kontrol:
        print("yama uygulanabilir (%d parça) · dosyaya dokunulmadı" % len(R)); return y
    # yükleyici + önbellek hazır mı (STEP ya da .brep) — eksikse yamadan ÖNCE dur
    if D not in sys.path: sys.path.insert(0, D)
    import katalog_step_v1 as KS
    for kod in KS.KODLAR: KS.olcu(kod)
    if hedef is None:
        if not os.path.isfile(YEDEK): io.open(YEDEK, "w", encoding="utf-8").write(s)
        io.open(kaynak, "w", encoding="utf-8").write(y)
        print("h3_elk_qr_v1.py yamalandı (v3.5 · 5 üretici STEP) · yedek: %s" % os.path.basename(YEDEK))
    else:
        io.open(hedef, "w", encoding="utf-8").write(y)
        print("yamalı kopya yazıldı: %s (kaynak dokunulmadı)" % hedef)
    return y


if __name__ == "__main__":
    a = sys.argv[1:]
    hedef = a[a.index("--hedef") + 1] if "--hedef" in a else None
    uygula(hedef=os.path.abspath(hedef) if hedef else None, kontrol="--kontrol" in a)
    sys.stdout.flush(); os._exit(0)
