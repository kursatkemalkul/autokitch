# -*- coding: utf-8 -*-
"""yolculuk_v47 → yolculuk_tp10_v2 (AYRI SÜRÜM v2 · ana hat değişmez): ürün TOPPING'den sonra ön odadaki giriş bandı → uzatılmış fırın → K.
v1'den fark: çit fırının dışında değil — ürün DİSKTE 79 mm arkaya kaydırılır (AKTARMA adımında, itici AÇIK konu), fırında −249'da düz gider,
K bandı üstündeki 20° giriş çiti −170'e geri alır (FT.urun_z). Fırın + giriş bandı ruloları kendi ekseninde döner (dünya koordinatı)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


d('    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider, bıçak burunlu bant ürünü fırın bandına alır; tabla açıcının altına döner."))',
  '    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider; ürün diskte 79 mm arkaya kaydırılır (fırın bandının eksenine — itici AÇIK konu) ve fırının ön odasındaki giriş bandına itilir; tabla açıcının altına döner."))')
d('    ADIM.append((T_F0, "FIRIN", "Konveyör fırın — animasyonda HIZLANDIRILMIŞ: gerçekte ~4 dk pişer, burada 10 s."))',
  '    ADIM.append((T_F0, "FIRIN", "TP10 kesitli fırın, gövdesi 1500\'e uzatıldı: bant gövde dışına çıkmaz, ısıtılan 1316 mm, aynı anda 4 ürün. Çıkışta K bandı üstündeki 20° çit ürünü hat eksenine (−170) geri alır. Animasyonda HIZLANDIRILMIŞ: gerçekte 3,5 dk, burada 10 s."))')
d('''            u = (t - T_AKT) / (T_F0 - T_AKT); return (OX + TH2.X_AKTARMA + 60.0 * u, OY + 108.0 - 2.0 * u, ZT)''',
  '''            u = (t - T_AKT) / (T_F0 - T_AKT); return (OX + TH2.X_AKTARMA, OY + 108.0, ZT + (FT.Z_URUN_FIRIN - ZT) * u)   # TP10 v2: diskte arkaya kayma''')
d('''            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA + 60.0; return (x0 + (3940.0 - x0) * u, KS.FIRIN_BANDI, ZT)''',
  '''            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA; x_ = x0 + (3940.0 - x0) * u
            return (x_, OY + 108.0 if x_ <= FT.X_DISK_KENAR else KS.FIRIN_BANDI, FT.urun_z(x_))''')
d('''            x, y, z = KS.urun_merkez(max(0.0, tK)); return (X_K + x, y, z)''',
  '''            x, y, z = KS.urun_merkez(max(0.0, tK)); xw = X_K + x; return (xw, y, FT.urun_z(xw) if xw < FT.CC_B[0] + 1.0 else z)''')
d('''    ROL = {"BANT_BURUN": ((OX + 1815.0, OY + 106.0 - 1.5 - 10.0, 0.0), 10.0), "BANT_TAHRIK": ((OX + 2195.0, OY + 106.0 - 1.5 - 30.0, 0.0), 30.0)}''',
  '''    ROL = {}                                                          # TP10 SÜRÜMÜ: TOPPING'in aktarma bandı yok''')
d('''    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):''',
  '''    # TP10 SÜRÜMÜ v2 · fırın + giriş bandı ruloları KENDİ EKSENİNDE (ağ pivota göre yerel) · bant yüzey hızıyla · dünya koordinatı
    ROL_F = {"RULO_TP_GIRIS": ((FT.RULO_X[0], FT.RULO_Y, 0.0), FT.SARIM_R), "RULO_TP_CIKIS": ((FT.RULO_X[1], FT.RULO_Y, 0.0), FT.SARIM_R),
             "RULO_GB_BURUN": ((FT.GB_XB, FT.GB_RY, 0.0), 11.5), "RULO_GB_TAHRIK": ((FT.GB_XT, FT.GB_RY, 0.0), 11.5)}
    for g, (P_, r_) in ROL_F.items():
        ton = {}
        for a_, m_, mal_ in parcalar:
            if a_.startswith("F_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == g:
                y_ = Mesh(); y_.P = [(q[0] - P_[0] * MM, q[1] - P_[1] * MM, q[2] - P_[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
                ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
        if not ton:
            continue
        ad = "F_DONER__" + g
        fR = lambda t, r_=r_: qax((0, 0, 1), -math.degrees(BANT(t) / r_))
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in P_), tonlar=ton))
        kanal(ad, lambda t, P_=P_: tuple(c * MM for c in P_))
        kanal(ad, fR, "rotation")
        KONTROL.append((ad, lambda t, P_=P_: tuple(c * MM for c in P_), fR, ton))
    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):''')
s = s.replace("# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU",
              "# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU (TP10 SÜRÜMÜ v2: yolculuk_tp10_v2)", 1)
io.open(os.path.join(U, "yolculuk_tp10_v2.py"), "w", encoding="utf-8").write(s)
print("yolculuk_tp10_v2.py yazildi")
