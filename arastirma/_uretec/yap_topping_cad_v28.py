# -*- coding: utf-8 -*-
"""topping_cad_v27 → topping_cad_v28 (29 Eyl 2026 · YEREL) — Kemal: "toppingde de delikler fln var neden".
HIWIN HGR15 raylarının katalog delikleri (Ø4,5 geçme + Ø7,5 × 5,3 havşa, hatve 60, uçtan 20) boştu → her deliğe katalog cıvatası:
DIN 912 M4 × 16 A2 (HIWIN HGR15 bağlantı cıvatası) · baş Ø7 × 4 havşanın dibine oturur, üstü ray yüzünün 1,3 mm altında (araba geçer) · 3 mm alyan yuvası ·
gövde Ø4 rayın altına kadar (dişli kısmı ray kirişinde, modelde çizilmez). Ray başına bir parça. Başka hiçbir parça değişmez. Önceki: topping_cad_v27.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v27.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""topping_cad_v27 (29 Eyl 2026): BANTLI TABLA',
      '"""topping_cad_v28 (29 Eyl 2026 · YEREL · yap_topping_cad_v28.py): RAY CIVATALARI — HGR15 havşalarına DIN 912 M4 × 16 (delikler boş kalmaz) · başka değişiklik yok' + NL +
      'v27 (29 Eyl 2026): BANTLI TABLA')
degis('''        ekle("lineer_ray_%s" % ad_, _r, "celik",
             bom=("Lineer ray HGR15 x %.0f" % H.RAY_UZUNLUK, 2, "paslanmaz sınıf [V: özel sipariş, fiyat/teslim sorulacak]", "HIWIN HGR15 GERÇEK profil (TraceParts STEP) · M4 havşa hatve 60 · 1,45 kg/m katalogla birebir") if ad_ == "on" else None)''',
      '''        ekle("lineer_ray_%s" % ad_, _r, "celik",
             bom=("Lineer ray HGR15 x %.0f" % H.RAY_UZUNLUK, 2, "paslanmaz sınıf [V: özel sipariş, fiyat/teslim sorulacak]", "HIWIN HGR15 GERÇEK profil (TraceParts STEP) · M4 havşa hatve 60 · 1,45 kg/m katalogla birebir") if ad_ == "on" else None)
        # v28 · RAY CIVATALARI (Kemal: delikler boş) — hiwin_ray() ile aynı desen: uçtan 20, hatve 60 · baş havşanın dibinde (30,2), üstü 34,2 < ray üstü 35,5
        _cv = None; _say = 0
        for i_ in range(_n):
            xd_ = H.RAY_X0 + 20.0 + i_ * 60.0
            if xd_ > H.RAY_X1 - 20.0: break
            _alyan = cq.Workplane("XZ").center(xd_, zc_).polygon(6, 3.0 / math.cos(math.radians(30.0))).extrude(-2.5).translate((0, 34.2 - 2.5, 0))
            b_ = sily(xd_, zc_, 3.5, 30.2, 34.2).cut(_alyan).union(sily(xd_, zc_, 2.0, 20.5, 30.2))
            _cv = b_ if _cv is None else _cv.union(b_); _say += 1
        ekle("lineer_ray_%s_civatalari" % ad_, _cv, "celik",
             bom=("Cıvata DIN 912 M4 × 16 · A2 paslanmaz (ray bağlantısı)", 2 * _say, "HIWIN HGR15 katalog bağlantı cıvatası · havşa Ø7,5 × 5,3 · hatve 60", "ray kirişine (dişli) · v28") if ad_ == "on" else None)''')
compile(s, "topping_cad_v28.py", "exec")
io.open(os.path.join(U, "topping_cad_v28.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v28.py yazildi")
