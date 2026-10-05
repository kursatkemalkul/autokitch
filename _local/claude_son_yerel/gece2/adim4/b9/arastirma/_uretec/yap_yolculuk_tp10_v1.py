# -*- coding: utf-8 -*-
"""yolculuk_v47 → yolculuk_tp10_v1 (AYRI SÜRÜM · ana hat değişmez): ürün TOPPING'den sonra giriş bandı → TP10 → K.
Değişen: TOPPING'in aktarma bandı yok (makaraları dönmez) · TP10 + giriş bandı ruloları kendi ekseninde döner ·
ürün fırında çitlerin itmesiyle z'de kayar (FT.urun_z: −170 → −249 → −170) · adım metinleri."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


d('    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider, bıçak burunlu bant ürünü fırın bandına alır; tabla açıcının altına döner."))',
  '    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider; 70 mm\'lik giriş bandı (TOPPING\'in 420 mm\'lik aktarma bandının yerine) ürünü TP10 bandına verir; tabla açıcının altına döner."))')
d('    ADIM.append((T_F0, "FIRIN", "Konveyör fırın — animasyonda HIZLANDIRILMIŞ: gerçekte ~4 dk pişer, burada 10 s."))',
  '    ADIM.append((T_F0, "FIRIN", "Sveba Dahlen TP10 · kızılötesi · ısıtılan ≈892 mm · aynı anda ≈3 ürün. Girişte 20° çit ürünü 79 mm arkaya (fırın bandının eksenine) iter, çıkışta ikinci çit K\'nin eksenine geri alır. Animasyonda HIZLANDIRILMIŞ: gerçekte 3,5 dk, burada 10 s."))')
d('''            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA + 60.0; return (x0 + (3940.0 - x0) * u, KS.FIRIN_BANDI, ZT)''',
  '''            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA + 60.0; x_ = x0 + (3940.0 - x0) * u; return (x_, KS.FIRIN_BANDI, FT.urun_z(x_))''')
d('''            x, y, z = KS.urun_merkez(max(0.0, tK)); return (X_K + x, y, z)''',
  '''            x, y, z = KS.urun_merkez(max(0.0, tK)); xw = X_K + x; return (xw, y, FT.urun_z(xw) if xw < FT.CC_B[0] + 1.0 else z)''')
d('''    ROL = {"BANT_BURUN": ((OX + 1815.0, OY + 106.0 - 1.5 - 10.0, 0.0), 10.0), "BANT_TAHRIK": ((OX + 2195.0, OY + 106.0 - 1.5 - 30.0, 0.0), 30.0)}''',
  '''    ROL = {}                                                          # TP10 SÜRÜMÜ: TOPPING'in aktarma bandı yok''')
d('''    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):''',
  '''    # TP10 SÜRÜMÜ · fırın + giriş bandı ruloları KENDİ EKSENİNDE (ağ pivota göre yerel) · bant yüzey hızıyla
    ROL_F = {"RULO_TP_GIRIS": ((FT.hx(-FT.RULO_X), FT.YG0 + FT.RULO_Y, 0.0), FT.RULO_R + FT.BANT_K),
             "RULO_TP_CIKIS": ((FT.hx(FT.RULO_X), FT.YG0 + FT.RULO_Y, 0.0), FT.RULO_R + FT.BANT_K),
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
              "# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU (TP10 SÜRÜMÜ: yolculuk_tp10_v1)", 1)
io.open(os.path.join(U, "yolculuk_tp10_v1.py"), "w", encoding="utf-8").write(s)
print("yolculuk_tp10_v1.py yazildi")
