# -*- coding: utf-8 -*-
import io, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"


def yama(dosya, ciftler):
    P = os.path.join(H3, dosya)
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (dosya, a[:90], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı:", dosya, len(ciftler))


# voksel: yüz yüz üçgenleme yedeği (süpürülmüş hortumlar bütün halinde üçgenlenemeyince engel görünmüyordu) + A* sınırı
yama("h3_elk_voksel.py", [
    ('''    if ad not in _TESS:
        try:
            v, t = s.tessellate(0.4, 0.3)
            P = np.array([(p.x, p.y, p.z) for p in v], dtype=float)
            _TESS[ad] = (P, np.array(t, dtype=int).reshape(-1, 3) if len(t) else np.zeros((0, 3), int))
        except Exception:
            _TESS[ad] = (np.zeros((0, 3)), np.zeros((0, 3), int))
    return _TESS[ad]''',
     '''    if ad not in _TESS:
        P, T = None, None
        try:
            v, t = s.tessellate(0.4, 0.3)
            if len(t):
                P = np.array([(p.x, p.y, p.z) for p in v], dtype=float); T = np.array(t, dtype=int).reshape(-1, 3)
        except Exception:
            P = None
        if P is None:                                                         # yüz yüz (bozuk yüz atlanır)
            Ps, Ts, n0 = [], [], 0
            for f in s.Faces():
                try:
                    v, t = f.tessellate(0.4, 0.3)
                except Exception:
                    continue
                if not len(t): continue
                Ps.append(np.array([(p.x, p.y, p.z) for p in v], dtype=float)); Ts.append(np.array(t, dtype=int).reshape(-1, 3) + n0); n0 += len(v)
            P = np.vstack(Ps) if Ps else np.zeros((0, 3)); T = np.vstack(Ts) if Ts else np.zeros((0, 3), int)
        _TESS[ad] = (P, T)
    return _TESS[ad]'''),
    ('        if say > 4000000: return None, "A* sınırı"', '        if say > 8000000: return None, "A* sınırı"'),
])
# kelepçe: yüzey arama menzili 150 (uzun dilli kelepçe = konsol)
yama("h3_elk_rota.py", [('def kelepce_yeri(p, eksen, r, maks=90.0, haric=()):', 'def kelepce_yeri(p, eksen, r, maks=150.0, haric=()):')])

P = os.path.join(H3, "h3_elk_ist_v1.py")
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:90], s.count(a))
    s = s.replace(a, b)


# 1 · sucuk motorları: önce motor bloğunun sağına çık (helezon motoru ile rotor ucu arası dar)
rep('''    for i, (xs, nm, S) in enumerate(SUR):
        cihaz("TOPPING_motor_%s_surucu_%d" % (nm, i), S, (xs, 1452.0, -699.5), 3.0, "C", itme=(1, -6.0), on=(xs, 1452.0, -684.0),''',
    '''    for i, (xs, nm, S) in enumerate(SUR):
        cihaz("TOPPING_motor_%s_surucu_%d" % (nm, i), S, (xs, 1452.0, -699.5), 3.0, "C", itme=(1, -6.0), on=(xs, 1452.0, -684.0),
              via=[(2360.0, S[1] - 6.3, -807.0)] if S[0] > 2200.0 else (),''')
# 2 · F yükleme bandı motoru: fırın gövde sacı arka yüzünden rakor G8 → arkadan G6 (y 1121,5) → KD1
rep('''    gecis("G6_F_TOPPING_duvari", (2516.5, 1230.0, -800.0), "x", [("TC", "dis_yan_sag"), ("FU", "f_ust_yan_sol")], "F", r=4.0, t=48.0, yon="+", bom=RK_BOM(1))
    cihaz("F_yukleme_bandi_motoru", (2780.0, 1121.5, -495.5), KD1(1230.0, -800.0), 4.0, "F", itme=(2, -6.0),
          via=[(2535.0, 1230.0, -800.0), ((2455.0, 1230.0, -800.0), ("TOPPING_MODUL|dis_yan_sag", "F_UST_KABIN|f_ust_yan_sol"))],
          bolge=(2449.0, 4000.0, 788.0, 1860.5, -828.5, 59.0), bom=("Motor kablosu 4 × 1 (yükleme bandı → TOPPING KD1)", 1, "", ""))''',
    '''    gecis("G8_firin_govde_arka", (2780.0, 1121.5, -651.0), "z", [("FT", "govde_kabugu")], "F", r=4.0, t=1.5, yon="-", bom=RK_BOM(2))
    gecis("G6_F_TOPPING_duvari", (2516.5, 1121.5, -800.0), "x", [("TC", "dis_yan_sag"), ("FU", "f_ust_yan_sol")], "F", r=4.0, t=48.0, yon="+")
    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.8), (2780.0, 1121.5, -800.0), (2449.2, 1121.5, -800.0)], 4.0, "F",
          haric=("F_TP10_GOVDE|govde_kabugu", "TOPPING_MODUL|dis_yan_sag", "F_UST_KABIN|f_ust_yan_sol"),
          bom=("Motor kablosu 4 × 1 (yükleme bandı → fırın gövdesi arkası → TOPPING KD1)", 1, "", ""))''')
# 3 · x sağ limit: sensör önünden sağa, cepte dik → KD1 (tekneye girmez)
rep('''    sabit("TOPPING_tabla_bos_sensoru",''',
    '''    sabit("TOPPING_sensor_x_limit_sag", [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2455.0, 920.0, -16.0), (2455.0, 1076.0, -16.0),
                                           (2455.0, 1076.0, -795.0), (2449.2, 1076.0, -795.0)], 2.0, "C")
    sabit("TOPPING_tabla_bos_sensoru",''')
# 4 · A: dikey kablo kanalı (sağ ön köşe, arabanın üstünde) + 8 port dağıtıcı kutusu kanalın üstünde · elle çizilmiş kısa yollar
i0 = s.index("    # A: emniyet sensörleri + ışık perdesi + TOPPING x eksen sensörleri")
i1 = s.index("    # ======================================================= K")
s = s[:i0] + '''    # A: emniyet sensörleri + ışık perdesi + TOPPING x sol limit / x sıfır sensörleri → A sağ ön köşede DİKEY KABLO KANALI (arabanın geçtiği bandın üstünde,
    #    y 1050–1545) + üstünde M12 dağıtıcı kutusu (8 port) → tek ana kablo A|TOPPING duvarı rakoru G7 → TOPPING panosu
    kanal_kutu("kanal_A_sag_on_dikey", 1406.0, 1434.0, 1050.0, 1545.0, -40.0, -8.0, "A",
               ("Kablo kanalı PVC kapaklı 28 × 32 (A sağ ön köşe, kapak −x yönüne)", 1, "A|TOPPING duvarına konsollu", ""))
    parca("A_sensor_dagitici_kutusu", kut(1406.0, 1434.0, 1545.0, 1655.0, -40.0, -10.0), "cihaz_koyu", "A",
          ("M12 pasif dağıtıcı kutusu 8 port (Murrelektronik Exact12 tipi) · kanalın üstünde, A|TOPPING duvarına 2 vida", 1, "110 × 28 × 30", "VARSAYIM: föyden teyit"))
    gecis("G7_A_TOPPING_duvari", (1436.0, 1520.0, -680.0), "x", [("TC", "dis_yan_sol")], "A", r=4.0, t=31.5, yon="-", bom=RK_BOM(1))
    sabit("A_sensor_ana_kablosu", [(1415.0, 1600.0, -40.3), (1415.0, 1600.0, -680.0), (1415.0, 1520.0, -680.0), (1480.0, 1520.0, -680.0),
                                   (1480.0, 1870.0, -680.0), (1480.0, 1870.0, -715.0), (1480.0, 1879.8, -715.0)], 4.0, "A", haric=("TOPPING_MODUL|dis_yan_sol",),
          bom=("Ana kablo M12 8 kutuplu (dağıtıcı → TOPPING panosu)", 1, "", ""))
    AK_BOM = ("Sensör kablosu M12 / M8 PUR (A emniyet · ışık perdesi · x eksen sensörleri → A kanalı)", 6, "", "")
    sabit("A_emniyet_ust", [(1386.5, 1594.0, 28.8), (1386.5, 1594.0, 0.0), (1414.0, 1594.0, 0.0), (1414.0, 1594.0, -9.8)], 2.5, "A", bom=AK_BOM)
    sabit("A_emniyet_alt", [(1386.5, 954.0, 28.8), (1386.5, 954.0, 6.0), (1386.5, 1100.0, 6.0), (1414.0, 1100.0, 6.0), (1414.0, 1100.0, -7.8)], 2.5, "A")
    sabit("A_isik_perdesi_ust", [(1206.3, 1175.0, 49.5), (1400.0, 1175.0, 49.5), (1400.0, 1175.0, 0.0), (1420.0, 1175.0, 0.0), (1420.0, 1175.0, -7.8)], 2.5, "A")
    sabit("A_isik_perdesi_alt", [(1206.3, 846.0, 49.5), (1360.0, 846.0, 49.5), (1360.0, 1070.0, 49.5), (1360.0, 1070.0, 0.0), (1426.0, 1070.0, 0.0),
                                 (1426.0, 1070.0, -7.8)], 2.5, "A")
    sabit("TOPPING_sensor_x_limit_sol", [(1056.0, 920.0, -18.7), (1056.0, 920.0, -16.0), (1056.0, 1150.0, -16.0), (1056.0, 1150.0, 49.5), (1390.0, 1150.0, 49.5),
                                         (1390.0, 1150.0, 0.0), (1409.0, 1150.0, 0.0), (1409.0, 1150.0, -7.8)], 2.0, "C")
    sabit("TOPPING_sensor_x_home", [(1086.0, 920.0, -18.7), (1086.0, 920.0, -16.0), (1086.0, 1140.0, -16.0), (1086.0, 1140.0, 49.5), (1395.0, 1140.0, 49.5),
                                    (1395.0, 1140.0, 0.0), (1416.0, 1140.0, 0.0), (1416.0, 1140.0, -7.8)], 2.0, "C")

''' + s[i1:]
# 5 · K klemens yaklaşma noktaları kademeli (komşu uçlar sıkışmasın)
rep('''    KT_ON = lambda i: (4176.0 + 8.6 * i, 1598.0, -786.0)''', '''    KT_ON = lambda i: (4176.0 + 8.6 * i, 1598.0 - 10.0 * (i % 2), -786.0)''')
io.open(P, "w", encoding="utf-8").write(s)
print("tamam")
