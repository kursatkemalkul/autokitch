import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import store_cad_v14 as S
for k in ("SECOP_X", "SECOP_Z", "SECOP_Y0", "RAY_SEC", "PED_Z", "S0_K4", "TAVA", "K4X", "K4_SAG", "KAN_UST", "KAN_UST_F", "KAN_X", "KAN_Z", "ZP1_ON",
          "EV_Z", "FAN_Z", "FAN_X", "EVAP", "Z_ON0", "Z_ON1", "Z_CON0", "Z_CER0", "Z_CER1", "Y_TABAN", "Y_TAVAN", "Y_TAVAN_F", "TABAN_T", "X_IC0", "X_IC1", "X_IC0S",
          "PERDE_Z", "SECOP_BOS", "SECOP_RAY_T", "TAKOZ_H", "ON_ALT", "ON_UST", "HAVA_Z", "HAVA_GECIS", "YIGIN_SINIR", "STROK", "WO", "BIND", "FUGA", "BOLME", "XI", "YUZ0",
          "DEPO_KUTU_D", "DEPO_KUTU_UST", "DEPO_SUCUK_W", "TUB", "KUTU_KENAR", "DR_Z", "DR_R", "DR_KILIF", "DR_EGIM", "VALF", "ISINIM_Y", "ARKA_YARIK_Y", "PLINT_FLANS", "KC", "HH_KOL", "Y0_KOL"):
    print(k, "=", getattr(S, k, "YOK"))
S.modul()
for p in S.PARCALAR:
    if p["birim"] in ("B_SOGUTMA", "B_ELEKTRIK", "B_DEPO") or p["ad"].startswith(("evaporator", "fan_", "damlama", "k4_")):
        b = p["wp"].val().BoundingBox()
        print("  %-12s %-44s x %7.1f %7.1f  y %6.1f %6.1f  z %7.1f %7.1f  %s" % (p["birim"], p["ad"][:44], b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax, p["grup"]))
