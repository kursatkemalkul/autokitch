# -*- coding: utf-8 -*-
# ÇAKIŞMA TARAMASI — montajdaki bileşenlerin kutu (bbox) kesişimlerini bulur, iç içe geçenleri raporlar.
# Beklenen temaslar (ürün ↔ yuva, hamur ↔ tepsi, kap ↔ raf) filtrelenir; kalanlar gerçek hata adayıdır.
import os, sys, itertools, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
BEKLENEN = (("CEKMECE_RAYI_450", "ic_yan"), ("CEKMECE_RAYI_450", "cekmece_"),
            ("YANGIN_TUPU_2KG", "tup_yatagi"), ("YANGIN_TUPU_2KG", "tup_kayisi"),
            ("AMBALAJ_RAFI_700", "raf_tasiyici"), ("BIDON_5L", "raf_temizlik"),
("VANTUZ_D40_YUKARI", "vantuz_plakasi"), ("VNU_", "blank_yigini"), ("VNU_", "KUTU_KATLI"),
            ("PLG_araba_plakasi", "lineer_ray_D16"), ("PLG_araba_plakasi", "bilyali_vida"),
            ("kilit_silindiri", "panel_temizlik"),
            ("AMBALAJ_RAFI", "raf_tasiyici"), ("S1_ic_yan", "AMBALAJ_RAFI"),
            ("VANTUZ_D40", "vantuz_plakasi"), ("blank_yigini", "sarjor_"), ("blank_yigini", "VANTUZ_D40"),
            ("KUTU_KATLI", "kutu_dayama_ledgesi"), ("KUTU_KATLI", "kapak_kolu"), ("KUTU_KATLI", "kutu_varlik_sensoru"),
            ("PLG_lineer_rulman", "lineer_ray_D16"), ("PLG_vida_somunu", "bilyali_vida"),
            ("AMB_blank_yigini", "AMB_"), ("YANGIN_TUPU", "tup_yatagi"),
            ("YANGIN_TUPU", "tup_kayisi"), ("BIDON_5L", "raf_temizlik"), ("AMBALAJ_RAFI", "ic_yan"),
            ("UC_DOCK", "ROBOT_UCU"), ("TEPSI_D320", "tepsi_raf"), ("TEPSI_D320", "PZP400"), ("evaporator", "evap_fan"), ("KABLO_24V", "pu_arka"), ("kablo_kanali", "ayirici_pu"), ("RAY_DIS_PROFIL", "KAYIS_GT3"), ("KAYIS_GT3", "MTG_kasnak"), ("KABLO_24V", "KABLO_24V"), ("RAY_DIS_PROFIL", "CEKMECE_"), ("RAY_DIS_PROFIL", "CEKMECE2_"), ("RAY_DIS_PROFIL", "CEKMECE3_"), ("KAYIS_GT3", "CEKMECE3_"), ("KAP_14", "L_RAF"), ("KAP_14", "kaset_raf_saci"), ("conta_manyetik", "klape_mentese_mili"), ("mentese_kulagi", "klape_mentese_mili"), ("conta_manyetik", "kaset_raf_saci"), ("L_RAF", "kaset_raf_saci"), ("KAYIS_GT3", "CEKMECE2_"), ("RAY_DIS_PROFIL", "on_cerceve_saci"), ("SENSOR_REED", "on_cerceve_saci"), ("MTG_kasnak", "MTG_reduktor"), ("KLM_reduktor", "KLM_tahrik_kolu"), ("panel_sogutma_bukme", "panel_sogutma_"), ("dis_ust_on_donus", "sove_"), ("dis_ust_on_donus", "panel_sogutma"), ("dis_alt_on_donus", "sove_"), ("dis_alt_on_donus", "panel_bant_alt"), ("RAY_DIS_PROFIL", "RAY_DIS_PROFIL"), ("KAYIS_GT3", "CEKMECE_"),
            ("KUTU_KOLA", "YUVA_"), ("KUTU_KOLA", "tepsi_taban_saci"), ("SISE_KOLA", "tepsi_taban_saci"), ("YUVA_", "tepsi_taban_saci"), ("TEPSI_HAMUR", "tepsi_taban_saci"), ("HAMUR_TOPU", "TEPSI_HAMUR"), ("HAMUR_TOPU_110g", "TEPSI_LAHMACUN"), ("miknatis", "SENSOR_REED"), ("kayis_baglanti_pabucu", "KAYIS_GT3"), ("ray_ic_profil", "RAY_DIS_PROFIL"), ("SISE_KOLA", "YUVA_"), ("HAMUR_TOPU", "TEPSI_HAMUR"), ("KAP_14", "L_RAF"), ("conta_manyetik", "on_cerceve_saci"), ("conta_manyetik", "kutu_U"), ("kutu_U", "kutu_arka"), ("mentese_kulagi", "on_ic_sac"), ("mentese_kulagi", "on_pu"), ("conta_manyetik", "ray_teleskopik"), ("conta_manyetik", "on_ic_sac"), ("conta_manyetik", "mentese_kulagi"), ("conta_manyetik", "kutu_arka"), ("conta_manyetik", "sove"), ("klape_mentese_mili", "KLAPE2_"), ("CEKMECE2_", "on_cerceve_saci"), ("KLAPE2_", "on_cerceve_saci"), ("klape_mentese_mili", "KLAPE_H"), ("klape_kaset_kati_pivot_mil", "KLAPE_KASET_KATI"), ("KAP_govde", "KAP_"), ("KAP_taban_plakasi", "KAP_kizak"), ("KAP_kapak_mentese_mili", "KAP_kapak"), ("KAP_helezon", "KAP_kece"), ("KAP_helezon_POM", "KAP_helezon_topuz"), ("KAP_tarak", "KAP_kece"), ("LRAF_capraz", "LRAF_kapak_acma"), ("plint_U", "sog_"), ("plint_U", "ayar_"), ("TEPSI_PIDE", "KLAPE_H"), ("plint_U", "plint_"), ("SOKET_MOTOR", "kapak_saci"), ("KAP_14", "SOKET_MOTOR"), ("KLAPE_H", "sove"), ("KLAPE_H", "panel_ust"),
            ("KLP270_kapak", "klape_mentese_borusu"), ("KLP270_kapak", "BM_"),
            ("klape_mentese_borusu", "mentese_kulagi_D35"), ("klape_mentese_borusu", "BM_"),
            ("mentese_kulagi_D35", "BM_"), ("BM_motor_govde", "BM_"),
            ("alin_saci", "TEPSI_PIDE"),
            ("agiz_tabani", "alin_saci"), ("agiz_tavani", "alin_saci"),
            ("agiz_cep_kapagi", "agiz_cerceve"), ("agiz_cep_kapagi", "alin_saci"),
            ("FK3_pivot_mili", "FK3_mentese_kulagi"),      # mil kulagin deliginden gecer
            ("YK_arka_sac", "YK_kuru_baglanti"),           # rakor sacin deliginden gecer
            ("kesici_bicak_yatay", "kesici_bicak_dik"),    # bicak yildizi: merkezde gecmeli
            ("O3_kablo_kanali", "O3_agiz"), ("O3_kablo_kanali", "O3_tasyunu"),
            # OVEN v4 (O4_) — O3_ ile ayni geometri, bbox yanilmalari: C kesitli panel, delikli agiz tavani/kizak, kablo kanali kesigi
            ("O4_kablo_kanali", "O4_agiz"), ("O4_kablo_kanali", "O4_tasyunu"),
            ("O4_panel", "_donus_"), ("O4_panel", "MG_govde"), ("O4_panel", "MANDAL"), ("O4_panel", "O4_agiz_cerceve"),
            ("O4_ust_serit", "O4_panel"), ("O4_plenum_kutusu", "O4_egzoz_fani"), ("FIRIN_3_HAZNE", "firin_hazne"),
            ("FIRIN_3_HAZNE", "TEPSI_D320"), ("O4_agiz_cerceve", "O4_agiz_cep_kapagi"),
            ("O4_agiz_tavani", "O4_kesici_gobegi"), ("O4_agiz_tavani", "O4_kesici_kilavuz"), ("O4_kesici_kilavuz", "O4_kesici_kizak"),
            ("FK4_pivot_mili", "FK4_mentese_kulagi"), ("FK4_dis_sac", "FK4_ic_sac"), ("FK4_dis_sac", "FK4_donus"), ("FK4_dis_sac", "FK4_tasyunu"),   # C kesit bukme sac: bbox dolu, gercek ic bos
            ("O3_panel", "_donus_"), ("O3_panel", "gizli_mentese"), ("O3_panel", "bas_ac_mandali"),
            ("O3_panel", "O3_agiz_cerceve"), ("O3_ust_serit", "O3_panel"),
            ("O3_plenum_kutusu", "O3_egzoz_fani"), ("OMAKE_firin", "firin_hazne"),
            ("OMAKE_firin", "TEPSI_D320"), ("O3_agiz_cerceve", "O3_agiz_cep_kapagi"),
            ("dokum_bacasi", "agiz_tavani"), ("dokum_bacasi", "agiz_tabani"),
            ("dokum_bacasi", "oda_tabani"), ("dokum_bacasi", "L_RAF"), ("dokum_bacasi", "KAP_DETAY"),
            ("KAP_DETAY", "KPK_conta_manyetik"), ("KAP_DETAY", "KPK_on_ic_sac"),
            ("alin_saci", "SENSOR_REED"), ("alin_saci", "KPK_"), ("alin_saci", "KAP_DETAY"),
            ("bant_pu_dolgusu", "dokum_bacasi"), ("bant_pu_dolgusu", "sag_kanal_kablo"),
            ("bant_pu_dolgusu", "KAP_DETAY"), ("alin_saci_1.0", "agiz_cerceve"),
            ("agiz_tavani", "sag_kanal_kablo"), ("agiz_cerceve", "sag_kanal_kablo"),
            ("oda_tabani", "sag_kanal_kablo"), ("agiz_tabani", "sag_kanal_kablo"),
            ("KPK_conta_manyetik", "SENSOR_REED"), ("KPK_conta_manyetik", "KLM_"),
            ("KPK_on_pu", "KLM_"), ("KPK_on_ic_sac", "KLM_"),
            ("KPK_on_pu", "KPK_"), ("KPK_on_ic_sac", "KPK_"), ("KPK_conta_manyetik", "KPK_"),
            ("KPK_conta_manyetik", "alin_saci"), ("KPK_gizli_mentese", "sove"),
            ("tarak_omurgasi", "tarak_cubugu"), ("tarak_gobek", "tarak_cubugu"),   # kaynak birlesimi
            ("KAP_DETAY", "L_RAF"), ("KAP_DETAY", "kaset_raf_saci"), ("KAPD_kizak", "LRAF"),
            ("kare_ucu_12", "yayli_kare_soket"), ("yayli_kare_soket", "arka_duvar_kapak_saci"),
            ("kare_ucu_12", "arka_kapak_PC"), ("SMD_montaj_braketi", "SMD_"),
            ("CAT_tirnak_ucu", "CAT_lama"), ("P5_panel", "on_cerceve"),
            ("P5_panel", "_donus_"), ("P5_panel", "_agiz_"), ("P5_panel", "gizli_mentese"),
            ("P5_panel", "bas_ac_mandali"), ("P5_panel_atma", "atma_klape"), ("P5_panel_atma", "atma_hunisi"),
            ("cop_kutusu_59L_U", "cop_kutusu_"), ("cop_kutusu_59L_U", "cop_torba_kelepcesi"),
            ("PZP_kaide_govde", "PZP_motor"), ("uc_aski_plakasi", "UC_DOCK"), ("uc_aski_plakasi", "uc_tasiyici"),
            ("atma_hunisi", "atma_huni_yan"), ("atma_klapesi", "atma_klape_pivot"),
            ("KAP_YAG", "L_RAF"), ("VANTUZ", "plunger"), ("VANTUZ", "kapak_postu"), ("KUTU_KOLA", "tepsi_taban"),
            ("SISE_KOLA", "tepsi_taban"), ("YUVA_", "tepsi_taban"), ("HAMUR_TOPU", "kutu_U"))

# kutu bbox'i gercegi yansitmayan (ici bos / delikli) parcalar: ayni cekmecenin icindeki her sey beklenen
OYUK = ("CRY_", "kutu_U", "conta_manyetik", "TPS_silikon", "YUVA_", "tepsi_taban_saci", "KLP270_kapak",
        "KAPD_govde_profil", "KAPD_burun", "KAPD_arka_kapak", "KAPD_ust_kapak", "KAPD_agiz_contasi",
        "KAPD_helezon_POM", "KAPD_tarak_gobek", "KAPD_tarak_omurgasi",
        "KPK_on_dis_sac_1.5", "agiz_cerceve_sol_", "agiz_cerceve_sag_",
        "YK_govde_304", "O3_plenum_kutusu", "O3_agiz_cerceve_sol", "O3_agiz_cerceve_sag",   # C kesitli bukme: kutu anlamsiz   # acik helezon/kafes: kutu anlamsiz
        "_yatak_POM", "KAPD_kece_",   # mil uzerindeki halkalar: kutu mili kapsar
        "SMD_motor_kutusu_IP65", "SMD_yayli_kare_soket", "SMD_baski_yayi", "SMD_mil_kecesi", "SMD_kutu_flansi")
# delikli/bukme saclar: kutu (bbox) gercegi yansitmaz, her seyle kesisir gorunur
GENIS_OYUK = ("on_cerceve_saci", "panel_teknik_bukme", "panel_sogutma_bukme", "plint_U",
              "P3_panel_", "P3_sarjor_L_kilavuz", "P3_form_kalibi_plakasi", "P3_agiz_cerceve",
              "S1_panel_", "S1_tup_yatagi", "S1_ust_cephe_seridi", "PLG_araba_plakasi_10mm",
              "P3_agiz_tabani", "P3_agiz_tavani",
              "S1_raf_temizlik_2mm", "S1_raf_teknik_2mm",
              "S1_raf_tasiyici", "S1_yedek_uc_rafi_konsol",
              # STORE delikli hizalama saci: yuz sayisi OLCULDU — 1L 60 yuz (6 levha + 42 delik + 2 bacak),
              # icecek 81 yuz (6 + 63 + bacak). Delikler GERCEK; bbox U kesit oldugu icin her seyi kapsiyor.
              "hizalama_saci",
              # PICKUP: delikleri ARAC ILE DOGRULANDI (yuz sayisi 58 / 54 / 10 = beklenen)
              "PK_on_cerceve_2mm", "PK_bindirme_saci_2mm", "PK_pano_kapagi_2mm", "TG_on_kapi_pu_16",
              # C kesitli cephe panelleri: govde x XP0..XP0+1,5 (z 20..38,5) + on sac z 38,5..40.
              # Ortak mentese XP0+2 den basliyor -> gercek temas YOK, bbox bosluğu sayiyor.
              "O3_panel_", "P5_panel_",
              # TOPPING alt cephe seridi C kesit: madde yalniz y 123..124,5 (donus) ve z 38,5..40
              # (on sac). dis_alt (y 158..159,5, z<=0) ile GERCEK temas yok.
              "TOPPING_alt_cephe_seridi")   # L kesit — bbox bosluğu sayiyor   # kablo kanali gecis yarigi acilmis   # merkez kolon yarigi acilmis levhalar   # C/U kesitli parcalarin bbox yanilmasi
# klape mentese YATAGI: kulak mili sarar — temas BEKLENEN
BEKLENEN = tuple(BEKLENEN) + (
    ("mentese_kulagi", "klape_mentese_mili"),   # yatak: kulak mili sarar
    ("klape_mentese_braketi", "klape_mentese_mili"),   # yatak: braket Ø8,4 kertigine Ø8 mil oturur
    ("mentese_kulagi", "on_dis_sac"),           # kulak klapenin dis sacina KAYNAK
    ("klape_alt_conta", "conta_manyetik"),      # sabit alt conta klapenin contasina yaslanir
)

def cift_beklenen(a, b):
    for x, y in BEKLENEN:
        if (x in a and y in b) or (x in b and y in a): return True
    if any(o in a or o in b for o in OYUK) and a.split("/")[0] == b.split("/")[0]: return True
    if any(o in a or o in b for o in GENIS_OYUK): return True
    return False

def kesisim(b1, b2):
    d = [min(b1[i+3], b2[i+3]) - max(b1[i], b2[i]) for i in range(3)]
    if min(d) <= 0: return 0.0, d
    return d[0]*d[1]*d[2]*1e9, [x*1000 for x in d]        # mm³, mm

def tara(yol, ad_asm, esik_mm3=200.0, en_fazla=30):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); mcall(d, "EditRebuild3")
    comps = []
    def gez(c):                                     # alt montajlarin ICINE gir: gercek parca kutulari
        ch = list(c.GetChildren)
        if ch:
            for k in ch: gez(k)
        else: comps.append(c)
    gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    kutu = []
    for c in comps:
        try:
            b = c.GetBox(False, False)
            if b is not None and len(b) >= 6: kutu.append((c.Name2, b))
            else: print("   bbox okunamadi:", c.Name2)
        except Exception: pass
    print("%s — %d bilesen tarandi" % (ad_asm, len(kutu)))
    bulgu = []
    for (n1, b1), (n2, b2) in itertools.combinations(kutu, 2):
        hac, ort = kesisim(b1, b2)
        if hac < esik_mm3: continue
        if cift_beklenen(n1, n2): continue
        bulgu.append((hac, n1, n2, ort))
    bulgu.sort(key=lambda x: -x[0])
    print("  esik ustu cakisma: %d" % len(bulgu))
    for hac, n1, n2, ort in bulgu[:en_fazla]:
        print("   %12.0f mm3 | ortusme x%.1f y%.1f z%.1f | %s  <->  %s" % (hac, ort[0], ort[1], ort[2], n1.rsplit('-',1)[0], n2.rsplit('-',1)[0]))
    # kalınlık kontrolü: çok ince veya sıfır kalınlıklı parçalar
    ince = [(n, [(b[i+3]-b[i])*1000 for i in range(3)]) for n, b in kutu]
    suphe = [(n, o) for n, o in ince if min(o) < 0.4]
    if suphe:
        print("  ince/suphe parca (<0,4 mm):")
        for n, o in suphe[:10]: print("   %s  %.2f x %.2f x %.2f mm" % (n.rsplit('-',1)[0], o[0], o[1], o[2]))
    sw.CloseDoc(d.GetTitle)
    return bulgu

if __name__ == "__main__":
    hedef = sys.argv[1] if len(sys.argv) > 1 else "STORE"
    yollar = {"STORE": (os.path.join(ARA, "1_STORE", "STORE.SLDASM"), "STORE"),
              "TOPPING": (os.path.join(ARA, "3_TOPPING", "TOPPING.SLDASM"), "TOPPING"),
              "PRESS": (os.path.join(ARA, "2_PRESS", "PRESS.SLDASM"), "PRESS"),
              "OVEN": (os.path.join(ARA, "4_OVEN", "OVEN.SLDASM"), "OVEN"),
              "PACK": (os.path.join(ARA, "5_PACK", "PACK.SLDASM"), "PACK"),
              "STORE2": (os.path.join(ARA, "1_STORE_v2", "STORE_v2.SLDASM"), "STORE_v2"),
              "STORE3": (os.path.join(ARA, "1_STORE_v3", "STORE_v3.SLDASM"), "STORE_v3")}
    if hedef in yollar: yol, ad = yollar[hedef]
    else: yol, ad = hedef, os.path.splitext(os.path.basename(hedef))[0]     # dogrudan .SLDASM yolu da verilebilir
    tara(yol, ad)
