# -*- coding: utf-8 -*-
"""Fırın üstü kabin tabanı ısı geçişi (teyit adımı 1) — yama_ud.isi_dengesi() ile aynı yöntem: seri dirençler.
Kesit (f_kabin_yeni.py): fırın üst sacı y 1305 → hava boşluğu 21 mm → 0,5 mm 304 kılıf (1326) → taş yünü t (1326,5–1346,5 @20) → 1,5 mm 304 taban (1346,5–1348) → kabin havası.
Boşluk: alttan ısıtılan yatay hava katmanı (Globe–Dropkin Nu = 0,069 Ra^(1/3) Pr^0,074) + ışınım (iki gri paralel levha).
Üst yüz h_o 4 W/m²K (yama_ud: üst yüz h 4) · taş yünü λ 0,040 W/mK (yama_ud: ROCKWOOL ProRox sınıfı @ 50–60 °C).
VARSAYIM: ε fırın üst sacı 0,25 (paslanmaz, ısıl kararmış) · ε kılıf 0,15 (304) — yama_ud ile aynı 0,15."""
SIG = 5.67e-8
A = 1.497 * 0.886            # taban alanı m² (x 2501,5–3998,5 · z −828,5…+57) ≈ 1,33 (yama_ud 1,33)


def hava(T1, T2, L):
    Tm = (T1 + T2) / 2 + 273.15
    nu = 1.5e-5 * (Tm / 293.0) ** 1.75; al = nu / 0.71; k = 0.0257 * (Tm / 293.0) ** 0.8
    Ra = 9.81 / Tm * max(T1 - T2, 0.1) * L ** 3 / (nu * al)
    Nu = max(1.0, 0.069 * Ra ** (1 / 3) * 0.71 ** 0.074)
    return Nu * k / L


def isinim(T1, T2, e1=0.25, e2=0.15):
    e = 1 / (1 / e1 + 1 / e2 - 1); a, b = T1 + 273.15, T2 + 273.15
    return e * SIG * (a * a + b * b) * (a + b)


def coz(Ts, Thava, t_yun, L_bos=0.021, lam=0.040, ho=4.0):
    """Ts fırın üst yüzü · Thava kabin havası · t_yun m (0 = yalıtımsız, boşluk 41,5 mm) → q W/m², Q W, taban üst yüzü °C"""
    if t_yun == 0: L_bos = 0.0415
    Tk = (Ts + Thava) / 2
    for _ in range(200):
        hb = hava(Ts, Tk, L_bos) + isinim(Ts, Tk)
        R = 1 / hb + t_yun / lam + 1 / ho
        q = (Ts - Thava) / R
        Tk = Ts - q / hb
    Tust = Thava + q / ho
    return q, q * A, Tust, 1 / R


if __name__ == "__main__":
    print("A = %.3f m²" % A)
    print("Ts(°C) Thava(°C) | t=0 Q W, taban °C | t=20 Q, taban | t=30 Q, taban | t=40 Q, taban | t=50 Q, taban")
    for Ts in (50, 60, 80, 100, 120, 150):
        for Th in (35, 40):
            row = []
            for t in (0, 0.020, 0.030, 0.040, 0.050):
                q, Q, Tu, U = coz(Ts, Th, t)
                row.append("%5.0f W %5.1f °C (U %.2f)" % (Q, Tu, U))
            print("%5d %5d | " % (Ts, Th) + " | ".join(row))
    # davlumbaz fanı kabin havasını emerse kabin havası artışı (Systemair RS 30-15 sileo, model notu 210 m³/h @ 228 Pa)
    for V in (100.0, 210.0):
        print("V %.0f m³/h → ρc·V = %.1f W/K" % (V, 1.11 * 1007 * V / 3600))
