# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET 3D/AR v3 (20 Eyl 2026) — Picnic hopper formu, bizim olcude, tam detay
Kemal: "bu ne dumduz kare, ben sana tam detayli, radyusu vidasina kadar."
Referans: Kemal'in gonderdigi iki Picnic CHEESE HOPPER fotografi.

FORM (fotograflardan):
  · govde: sabit kesitli ekstruzyon — ustte dik duvar, buyuk radyusla iceri donup helezon teknesine (yarim daire) baglanir
  · iki UC PLAKASI: duz seffaf yanaklar, masaya kadar iner ve AYAK olur (arada kemer bosluk), koseler radyuslu
  · ust flans + radyus koseli kapak
  · on plakada SEFFAF CIKIS TUPU, icinden helezon gecer, mil ucu disari cikar
  · helezon: mil O20 + kalin kanat O56, hatve 48
  · ust bolmede TEL KARISTIRICI (paslanmaz tel cerceve) + yatak gobekleri, on tarafta beyaz tutamak
  · tutamakta emniyet PIMI + ipli HALKA + vida · on plakada asma deligi · kucuk sari uyari etiketleri
  · teknenin altinda paslanmaz SAPLAMA + somun · arka plakada tahrik kaplinleri (hac govde) + vidalar
  · uzun yuzlerde YAZILI sari bantlar (ad bandi + montaj bandi) — doku olarak GLB'ye gomulu

OLCULER (16 Eyl karari): STANDART KASET zarf 140 x 400 x 360 · KASAR KABI zarf 280 x 400 x 360.
Hacim bu dosyada kesitten SAYISAL hesaplanir ve yazdirilir (uydurma yok).
Cikti: otonom/kaset3d/kaset_v3.glb/.usdz · kasar_v3.glb/.usdz   (onceki surumler silinmez)
"""
import io, json, math, os, re, struct, zipfile
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d")
MM = 0.001


# ======================= VEKTOR =======================
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def unit(a):
    L = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / L, a[1] / L, a[2] / L)


class Mesh(object):
    def __init__(self):
        self.P, self.N, self.I, self.UV = [], [], [], None

    def v(self, p, n, uv=None):
        self.P.append(p); self.N.append(unit(n))
        if uv is not None:
            if self.UV is None: self.UV = []
            self.UV.append(uv)
        return len(self.P) - 1

    def quad(self, a, b, c, d, na, nb=None, nc=None, nd=None, uv=None):
        nb = nb or na; nc = nc or na; nd = nd or na
        u = uv or [None] * 4
        i0 = self.v(a, na, u[0]); i1 = self.v(b, nb, u[1]); i2 = self.v(c, nc, u[2]); i3 = self.v(d, nd, u[3])
        self.I += [i0, i1, i2, i0, i2, i3]

    def ekle(self, o):
        off = len(self.P)
        self.P += o.P; self.N += o.N; self.I += [i + off for i in o.I]
        return self

    def duzelt(self):
        """ucgen sarimini verilen normallere uydur (isik dogru dussun)"""
        I = self.I
        for k in range(0, len(I), 3):
            a, b, c = I[k], I[k + 1], I[k + 2]
            g = cross(sub(self.P[b], self.P[a]), sub(self.P[c], self.P[a]))
            n = add(add(self.N[a], self.N[b]), self.N[c])
            if dot(g, n) < 0: I[k + 1], I[k + 2] = c, b
        return self


# ======================= TEMEL SEKILLER =======================
def kutu(x0, x1, y0, y1, z0, z1):
    m = Mesh()
    m.quad((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), (0, 0, 1))
    m.quad((x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (0, 0, -1))
    m.quad((x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (1, 0, 0))
    m.quad((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (-1, 0, 0))
    m.quad((x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0), (0, 1, 0))
    m.quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (0, -1, 0))
    return m


def _taban(eksen):
    e = unit(eksen)
    yard = (1, 0, 0) if abs(e[0]) < 0.9 else (0, 1, 0)
    u = unit(cross(e, yard)); w = cross(e, u)
    return e, u, w


def silindir(p0, p1, r0, r1=None, seg=28, kapak=True, ic=False):
    """p0→p1 arasi silindir / koni · duzgun (smooth) normaller · ic=True: normaller iceri"""
    r1 = r0 if r1 is None else r1
    e, u, w = _taban(sub(p1, p0))
    L = math.sqrt(dot(sub(p1, p0), sub(p1, p0)))
    egim = (r0 - r1) / (L or 1.0)
    m = Mesh(); s = -1.0 if ic else 1.0
    halka0, halka1 = [], []
    for i in range(seg + 1):
        a = 2 * math.pi * i / seg
        d = add(mul(u, math.cos(a)), mul(w, math.sin(a)))
        n = mul(unit(add(d, mul(e, egim))), s)
        halka0.append(m.v(add(p0, mul(d, r0)), n)); halka1.append(m.v(add(p1, mul(d, r1)), n))
    for i in range(seg):
        m.I += [halka0[i], halka0[i + 1], halka1[i + 1], halka0[i], halka1[i + 1], halka1[i]]
    if kapak:
        for p, r, nn in ((p0, r0, mul(e, -1)), (p1, r1, e)):
            if r < 1e-7: continue
            c = m.v(p, nn); ring = []
            for i in range(seg + 1):
                a = 2 * math.pi * i / seg
                ring.append(m.v(add(p, mul(add(mul(u, math.cos(a)), mul(w, math.sin(a))), r)), nn))
            for i in range(seg): m.I += [c, ring[i], ring[i + 1]]
    return m.duzelt()


def halka_yuz(merkez, eksen, r_ic, r_dis, seg=32):
    """duz halka (annulus)"""
    e, u, w = _taban(eksen); m = Mesh()
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        d0 = add(mul(u, math.cos(a0)), mul(w, math.sin(a0))); d1 = add(mul(u, math.cos(a1)), mul(w, math.sin(a1)))
        m.quad(add(merkez, mul(d0, r_ic)), add(merkez, mul(d0, r_dis)), add(merkez, mul(d1, r_dis)), add(merkez, mul(d1, r_ic)), e)
    return m.duzelt()


def boru(p0, p1, r_dis, r_ic, seg=36):
    m = silindir(p0, p1, r_dis, seg=seg, kapak=False)
    m.ekle(silindir(p0, p1, r_ic, seg=seg, kapak=False, ic=True))
    e = unit(sub(p1, p0))
    m.ekle(halka_yuz(p1, e, r_ic, r_dis, seg)); m.ekle(halka_yuz(p0, mul(e, -1), r_ic, r_dis, seg))
    return m


def torus(merkez, eksen, R, r, seg=40, kes=14):
    e, u, w = _taban(eksen); m = Mesh(); idx = []
    for i in range(seg + 1):
        a = 2 * math.pi * i / seg
        d = add(mul(u, math.cos(a)), mul(w, math.sin(a))); c = add(merkez, mul(d, R)); sat = []
        for j in range(kes + 1):
            b = 2 * math.pi * j / kes
            n = add(mul(d, math.cos(b)), mul(e, math.sin(b)))
            sat.append(m.v(add(c, mul(n, r)), n))
        idx.append(sat)
    for i in range(seg):
        for j in range(kes):
            m.I += [idx[i][j], idx[i + 1][j], idx[i + 1][j + 1], idx[i][j], idx[i + 1][j + 1], idx[i][j + 1]]
    return m.duzelt()


def helezon(r_mil, r_dis, z0, z1, hatve, cy, kal=3.0 * MM, seg=28):
    """kalin kanatli helezon · eksen z · analitik helikoid normalleri"""
    m = Mesh(); c = hatve / (2 * math.pi)
    tur = (z1 - z0) / hatve; n = max(8, int(tur * seg)); k = kal / 2.0
    on, arka = [], []
    for i in range(n + 1):
        a = 2 * math.pi * tur * i / n; z = z0 + (z1 - z0) * i / float(n)
        ca, sa = math.cos(a), math.sin(a); sat_o, sat_a = [], []
        for r in (r_mil, r_dis):
            nn = unit((c * sa, -c * ca, r))
            sat_o.append(m.v((r * ca, cy + r * sa, z + k), nn)); sat_a.append(m.v((r * ca, cy + r * sa, z - k), mul(nn, -1)))
        on.append(sat_o); arka.append(sat_a)
    for i in range(n):
        m.I += [on[i][0], on[i][1], on[i + 1][1], on[i][0], on[i + 1][1], on[i + 1][0]]
        m.I += [arka[i][0], arka[i + 1][1], arka[i][1], arka[i][0], arka[i + 1][0], arka[i + 1][1]]
    ken = []
    for i in range(n + 1):
        a = 2 * math.pi * tur * i / n; z = z0 + (z1 - z0) * i / float(n); nn = (math.cos(a), math.sin(a), 0)
        ken.append((m.v((r_dis * math.cos(a), cy + r_dis * math.sin(a), z + k), nn), m.v((r_dis * math.cos(a), cy + r_dis * math.sin(a), z - k), nn)))
    for i in range(n):
        m.I += [ken[i][0], ken[i][1], ken[i + 1][1], ken[i][0], ken[i + 1][1], ken[i + 1][0]]
    return m.duzelt()


# ======================= GOVDE KESITI =======================
def yari_gen(y, hw, rt, y1, cy):
    """kesitin y kotundaki yari genisligi: dik duvar → yumusak (C1) gecis → tekne yarim dairesi"""
    if y >= y1: return hw
    if y >= cy:
        t = (y1 - y) / (y1 - cy); s = t * t * (3 - 2 * t)
        return hw - (hw - rt) * s
    d = rt * rt - (y - cy) ** 2
    return math.sqrt(d) if d > 0 else 0.0


def profil(hw, rt, y_ust, y1, cy, nb=30, na=40):
    sag = [(hw, y_ust)]
    for i in range(nb + 1):
        y = y1 + (cy - y1) * i / float(nb); sag.append((yari_gen(y, hw, rt, y1, cy), y))
    pts = list(sag)
    for i in range(1, na):
        a = -math.pi * i / na; pts.append((rt * math.cos(a), cy + rt * math.sin(a)))
    for x, y in reversed(sag): pts.append((-x, y))
    return pts


def ekstruzyon(pts, z0, z1, isaret=1.0):
    """acik profil · saat yonunde gezilir → dis normal = tegetin solu"""
    m = Mesh(); n = len(pts); r0, r1 = [], []
    for i in range(n):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        nn = mul(unit((-ty, tx, 0)), isaret)
        r0.append(m.v((pts[i][0], pts[i][1], z0), nn)); r1.append(m.v((pts[i][0], pts[i][1], z1), nn))
    for i in range(n - 1):
        m.I += [r0[i], r1[i], r1[i + 1], r0[i], r1[i + 1], r0[i + 1]]
    return m.duzelt()


def hacim_litre(hw_i, rt_i, y1, cy, y_dolum, boy):
    alan, dy, y = 0.0, 0.0005, cy - rt_i
    while y < y_dolum:
        alan += 2 * yari_gen(y + dy / 2, hw_i, rt_i, y1, cy) * dy; y += dy
    return alan * boy * 1000.0


# ======================= UC PLAKASI (ayakli, radyus koseli) =======================
def uc_plakasi(W, y_ust, zf, zb, rc, rb, ayak, kemer_h, nx=120):
    hw = W / 2.0; a = hw - ayak

    def ust(x):
        ax = abs(x)
        if ax <= hw - rc: return y_ust
        d = rc * rc - (ax - (hw - rc)) ** 2
        return y_ust - rc + math.sqrt(max(0.0, d))

    def alt(x):
        ax = abs(x)
        if ax < a: return kemer_h * (max(0.0, 1 - (ax / a) ** 3.0)) ** (1 / 3.0)
        if ax <= hw - rb: return 0.0
        d = rb * rb - (ax - (hw - rb)) ** 2
        return rb - math.sqrt(max(0.0, d))

    xs = set()
    for i in range(nx + 1): xs.add(-hw + W * i / float(nx))
    for k in range(25):                                   # koselerde ve kemer uclarinda sik ornek
        t = k / 24.0
        for s in (1, -1):
            xs.add(s * (hw - rc + rc * math.sin(t * math.pi / 2))); xs.add(s * (hw - rb + rb * math.sin(t * math.pi / 2)))
            xs.add(s * (a - a * 0.12 * (1 - t) ** 2))
    xs = sorted(xs); m = Mesh()
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        m.quad((x0, alt(x0), zf), (x1, alt(x1), zf), (x1, ust(x1), zf), (x0, ust(x0), zf), (0, 0, 1))
        m.quad((x1, alt(x1), zb), (x0, alt(x0), zb), (x0, ust(x0), zb), (x1, ust(x1), zb), (0, 0, -1))
    dongu = [(x, ust(x)) for x in xs] + [(x, alt(x)) for x in reversed(xs)]
    n = len(dongu)
    for i in range(n):
        p, q = dongu[i], dongu[(i + 1) % n]
        if abs(p[0] - q[0]) < 1e-9 and abs(p[1] - q[1]) < 1e-9: continue
        tx, ty = q[0] - p[0], q[1] - p[1]; nn = unit((-ty, tx, 0))   # ust kenar soldan saga: saat yonu → dis = sol
        m.quad((p[0], p[1], zf), (q[0], q[1], zf), (q[0], q[1], zb), (p[0], p[1], zb), nn)
    return m.duzelt()


# ======================= RADYUS KOSELI DIKDORTGEN (kapak, flans) =======================
def rr_dongu(w, d, r, nk=10):
    pts = []
    for cx, cz, a0 in ((w / 2 - r, d / 2 - r, 0), (-w / 2 + r, d / 2 - r, 90), (-w / 2 + r, -d / 2 + r, 180), (w / 2 - r, -d / 2 + r, 270)):
        for k in range(nk + 1):
            a = math.radians(a0 + 90.0 * k / nk)
            pts.append((cx + r * math.cos(a), cz + r * math.sin(a), math.cos(a), math.sin(a)))
    return pts


def rr_plaka(w, d, r, y0, y1):
    L = rr_dongu(w, d, r); m = Mesh(); n = len(L)
    for y, nn in ((y1, (0, 1, 0)), (y0, (0, -1, 0))):
        c = m.v((0, y, 0), nn); ring = [m.v((p[0], y, p[1]), nn) for p in L]
        for i in range(n): m.I += [c, ring[i], ring[(i + 1) % n]]
    a = [m.v((p[0], y0, p[1]), (p[2], 0, p[3])) for p in L]; b = [m.v((p[0], y1, p[1]), (p[2], 0, p[3])) for p in L]
    for i in range(n):
        j = (i + 1) % n; m.I += [a[i], a[j], b[j], a[i], b[j], b[i]]
    return m.duzelt()


def rr_cerceve(w, d, r, wi, di, ri, y0, y1):
    Lo, Li = rr_dongu(w, d, r), rr_dongu(wi, di, ri); m = Mesh(); n = len(Lo)
    for i in range(n):
        j = (i + 1) % n
        m.quad((Li[i][0], y1, Li[i][1]), (Lo[i][0], y1, Lo[i][1]), (Lo[j][0], y1, Lo[j][1]), (Li[j][0], y1, Li[j][1]), (0, 1, 0))
        m.quad((Li[i][0], y0, Li[i][1]), (Lo[i][0], y0, Lo[i][1]), (Lo[j][0], y0, Lo[j][1]), (Li[j][0], y0, Li[j][1]), (0, -1, 0))
        m.quad((Lo[i][0], y0, Lo[i][1]), (Lo[j][0], y0, Lo[j][1]), (Lo[j][0], y1, Lo[j][1]), (Lo[i][0], y1, Lo[i][1]),
               (Lo[i][2], 0, Lo[i][3]), (Lo[j][2], 0, Lo[j][3]), (Lo[j][2], 0, Lo[j][3]), (Lo[i][2], 0, Lo[i][3]))
        m.quad((Li[i][0], y0, Li[i][1]), (Li[j][0], y0, Li[j][1]), (Li[j][0], y1, Li[j][1]), (Li[i][0], y1, Li[i][1]),
               (-Li[i][2], 0, -Li[i][3]), (-Li[j][2], 0, -Li[j][3]), (-Li[j][2], 0, -Li[j][3]), (-Li[i][2], 0, -Li[i][3]))
    return m.duzelt()


# ======================= KUCUK PARCALAR =======================
def vida(x, y, z, yon):
    """bombeli basli vida, z ekseninde · yon=+1 on yuze, -1 arka yuze bakar"""
    bas = silindir((x, y, z), (x, y, z + yon * 2.2 * MM), 3.4 * MM, 2.6 * MM, seg=18)
    zz = z + yon * 2.25 * MM; t = 0.25 * MM * yon
    yiv = kutu(x - 2.2 * MM, x + 2.2 * MM, y - 0.4 * MM, y + 0.4 * MM, min(zz, zz + t), max(zz, zz + t))
    yiv.ekle(kutu(x - 0.4 * MM, x + 0.4 * MM, y - 2.2 * MM, y + 2.2 * MM, min(zz, zz + t), max(zz, zz + t)))
    return bas, yiv


def hac_kaplin(x, y, z, yon, r_gobek, boy, kol):
    """tahrik kaplini: gobek + 4 tirnak (hac) — fotograftaki beyaz hac govdeler"""
    m = silindir((x, y, z), (x, y, z + yon * boy), r_gobek, seg=26)
    z0, z1 = sorted((z + yon * boy * 0.35, z + yon * boy))
    m.ekle(kutu(x - kol, x + kol, y - 3.2 * MM, y + 3.2 * MM, z0, z1)); m.ekle(kutu(x - 3.2 * MM, x + 3.2 * MM, y - kol, y + kol, z0, z1))
    return m


def tel_cerceve(y_eks, R, z_a, z_b, aci, r_tel=2.0 * MM):
    """karistirici tel cercevesi: eksenin iki yaninda R uzaklikta boyuna teller + radyal kollar"""
    ca, sa = math.cos(aci), math.sin(aci); m = Mesh()
    nok = lambda s, z: (s * R * ca, y_eks + s * R * sa, z)
    for s in (1, -1): m.ekle(silindir(nok(s, z_a), nok(s, z_b), r_tel, seg=10))
    for z in (z_a, (z_a + z_b) / 2.0, z_b): m.ekle(silindir(nok(1, z), nok(-1, z), r_tel, seg=10))
    return m


# ======================= ETIKET DOKULARI =======================
def _font(sz, kalin=True):
    for n in (("arialbd.ttf", "segoeuib.ttf") if kalin else ("arial.ttf", "segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()


SARI_RGB = (250, 190, 22)


def doku_ad(ad, alt, ok_sol=True):
    W, H = 1560, 192; im = Image.new("RGB", (W, H), SARI_RGB); d = ImageDraw.Draw(im)
    if ok_sol:
        d.polygon([(34, H // 2), (86, H // 2 - 40), (86, H // 2 + 40)], fill=(255, 255, 255)); tx = 116
    else:
        d.polygon([(W - 34, H // 2), (W - 86, H // 2 - 40), (W - 86, H // 2 + 40)], fill=(255, 255, 255)); tx = 210
    d.text((tx, 28), ad, font=_font(92), fill=(255, 255, 255))
    d.text((tx + 4, 134), alt, font=_font(34, False), fill=(255, 250, 225))
    kx = W - 190 if ok_sol else 30
    d.rounded_rectangle([kx, 26, kx + 140, H - 26], radius=22, fill=(255, 255, 255))
    d.text((kx + 70, H // 2), "AK", font=_font(78), fill=SARI_RGB, anchor="mm")
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()


def doku_montaj(adimlar):
    W, H = 1560, 192; im = Image.new("RGB", (W, H), SARI_RGB); d = ImageDraw.Draw(im)
    d.text((26, H // 2), "MONTAJ", font=_font(44), fill=(255, 255, 255), anchor="lm")
    x0 = 250; gen = (W - x0 - 20) // len(adimlar)
    for i, t in enumerate(adimlar):
        x = x0 + i * gen
        d.rounded_rectangle([x, 22, x + gen - 16, H - 22], radius=18, fill=(255, 255, 255))
        d.ellipse([x + 14, 40, x + 78, 104], fill=SARI_RGB); d.text((x + 46, 72), str(i + 1), font=_font(46), fill=(255, 255, 255), anchor="mm")
        for j, sat in enumerate(t.split("|")):
            d.text((x + 92, 52 + j * 40), sat, font=_font(30), fill=(40, 40, 44), anchor="lm")
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()


def etiket_yuzu(x, y0, y1, z_sol, z_sag, nx):
    """x sabit duz yuz · z_sol: bakan kisinin SOLUNA dusen z (yazi soldan saga dogru okunur)"""
    m = Mesh()
    m.quad((x, y0, z_sol), (x, y0, z_sag), (x, y1, z_sag), (x, y1, z_sol), (nx, 0, 0), uv=[(0, 1), (1, 1), (1, 0), (0, 0)])
    return m.duzelt()


# ======================= MODEL =======================
def kaset_modeli(W_mm, D_mm, H_mm, ad, kasar=False):
    W, D, H = W_mm * MM, D_mm * MM, H_mm * MM
    et, tp = 3 * MM, 5 * MM                               # govde cidari · uc plakasi
    flans = 3 * MM                                        # flans disari tasmasi (zarf = W)
    hw, rt = W / 2 - flans, 34 * MM                       # govde dis yari genislik · tekne dis yaricapi
    cy = 72 * MM                                          # helezon ekseni (tekne alti 38 → ayak kemeri 24'un ustunde)
    y_ust = H - 8 * MM                                    # govde ust kenari (kapak 4 + tutamak 4 zarfin icinde)
    y1 = cy + 86 * MM                                     # dik duvarin bittigi kot
    zf, zb = D / 2, -D / 2                                # on (+z) · arka (−z, makine tarafi)
    r_mil, r_kan, hatve = 10 * MM, 28 * MM, 48 * MM
    y_kar = 0.235 if not kasar else 0.245                 # karistirici ekseni
    R_kar = 46 * MM if not kasar else 92 * MM

    P = []
    def ekle(adi, mesh, mal): P.append((adi, mesh, mal))

    # --- 1 govde: dis + ic yuzey (3 mm cidar) ---
    ekle("govde_dis", ekstruzyon(profil(hw, rt, y_ust, y1, cy), zb + tp, zf - tp, 1.0), "cam")
    ekle("govde_ic", ekstruzyon(profil(hw - et, rt - et, y_ust, y1, cy), zb + tp, zf - tp, -1.0), "cam")

    # --- 2 uc plakalari (ayakli) ---
    for adi, za, zc in (("plaka_on", zf, zf - tp), ("plaka_arka", zb + tp, zb)):
        ekle(adi, uc_plakasi(W, y_ust, za, zc, rc=12 * MM, rb=8 * MM, ayak=(26 if not kasar else 34) * MM, kemer_h=24 * MM), "cam")

    # --- 3 flans + kapak (radyus koseli) ---
    ekle("flans", rr_cerceve(W, D, 12 * MM, 2 * (hw - et), D - 2 * tp, 6 * MM, y_ust - 4 * MM, y_ust), "cam")
    ekle("kapak", rr_plaka(W, D, 12 * MM, y_ust, y_ust + 4 * MM), "cam")
    ekle("kapak_tutamak", rr_plaka(min(W - 50 * MM, 120 * MM), 22 * MM, 9 * MM, y_ust + 4 * MM, y_ust + 8 * MM), "cam")

    # --- 4 seffaf cikis tupu (on) ---
    ekle("cikis_tupu", boru((0, cy, zf), (0, cy, zf + 46 * MM), rt, rt - et), "cam")

    # --- 5 helezon: mil + kanat + uc ---
    ekle("helezon_mil", silindir((0, cy, zb - 4 * MM), (0, cy, zf + 58 * MM), r_mil, seg=24), "pom")
    ekle("helezon_uc", silindir((0, cy, zf + 58 * MM), (0, cy, zf + 70 * MM), r_mil, 5 * MM, seg=24), "pom")
    ekle("helezon_kanat", helezon(r_mil, r_kan, zb + tp + 6 * MM, zf + 40 * MM, hatve, cy), "pom")

    # --- 6 arka: helezon tahrik kaplini + flans + vidalar ---
    ekle("kaplin_helezon", hac_kaplin(0, cy, zb, -1, 15 * MM, 24 * MM, 21 * MM), "pom")
    ekle("kaplin_flans", silindir((0, cy, zb), (0, cy, zb - 5 * MM), 27 * MM, seg=30), "pom")
    for a in (45, 135, 225, 315):
        b, y = vida(24 * MM * math.cos(math.radians(a)) * 0.82, cy + 24 * MM * math.sin(math.radians(a)) * 0.82, zb - 5 * MM, -1)
        ekle("vida_kaplin_%d" % a, b, "celik"); ekle("yiv_kaplin_%d" % a, y, "koyu")

    # --- 7 karistirici: mil + tel cerceveler + gobekler + on tutamak ---
    ekle("kar_mil", silindir((0, y_kar, zb - 6 * MM), (0, y_kar, zf + 8 * MM), 4 * MM, seg=16), "celik")
    for k, aci in enumerate((math.radians(35), math.radians(125))):
        ekle("kar_tel_%d" % k, tel_cerceve(y_kar, R_kar, zb + 34 * MM, zf - 34 * MM, aci), "celik")
    ekle("kar_gobek_arka", hac_kaplin(0, y_kar, zb, -1, 12 * MM, 20 * MM, 17 * MM), "pom")
    ekle("kar_gobek_on", silindir((0, y_kar, zf), (0, y_kar, zf + 12 * MM), 14 * MM, 12 * MM, seg=26), "pom")
    ekle("kar_tutamak", silindir((0, y_kar, zf + 12 * MM), (0, y_kar, zf + 62 * MM), 10.5 * MM, seg=26), "pom")
    ekle("kar_tutamak_uc", silindir((0, y_kar, zf + 62 * MM), (0, y_kar, zf + 66 * MM), 10.5 * MM, 8 * MM, seg=26), "pom")
    for s in (1, -1):
        b, y = vida(s * 9 * MM, y_kar - 9 * MM * 0, zf + 12 * MM * 0 + 0, 1)
    for s in (1, -1):                                      # on gobegi plakaya baglayan 2 vida (gobek flansinda)
        ekle("gobek_kulak_%d" % s, silindir((s * 19 * MM, y_kar, zf), (s * 19 * MM, y_kar, zf + 4 * MM), 6 * MM, seg=18), "pom")
        b, y = vida(s * 19 * MM, y_kar, zf + 4 * MM, 1); ekle("vida_gobek_%d" % s, b, "celik"); ekle("yiv_gobek_%d" % s, y, "koyu")

    # --- 8 emniyet pimi + kelepce + ipli halka + vida (fotograf 2) ---
    zp = zf + 20 * MM
    ekle("pim", silindir((-15 * MM, y_kar, zp), (15 * MM, y_kar, zp), 2.4 * MM, seg=12), "pom")
    ekle("pim_bas", silindir((15 * MM, y_kar, zp), (19 * MM, y_kar, zp), 4.5 * MM, seg=14), "pom")
    ekle("kelepce", kutu(12 * MM, 26 * MM, y_kar - 16 * MM, y_kar - 8 * MM, zp - 4 * MM, zp + 4 * MM), "pom")
    b, y = vida(21 * MM, y_kar - 12 * MM, zp + 4 * MM, 1); ekle("vida_kelepce", b, "celik"); ekle("yiv_kelepce", y, "koyu")
    ekle("ip", silindir((14 * MM, y_kar - 16 * MM, zp), (4 * MM, y_kar - 34 * MM, zp + 2 * MM), 0.9 * MM, seg=8), "pom")
    ekle("ip_halka", torus((-6 * MM, y_kar - 42 * MM, zp + 2 * MM), (0.2, 0.1, 1), 12 * MM, 1.3 * MM), "pom")

    # --- 9 on plakada asma deligi (kalin seffaf bilezik) ---
    ekle("asma_deligi", torus((-W / 2 + 30 * MM, y_ust - 34 * MM, zf - tp / 2), (0, 0, 1), 15 * MM, 3.2 * MM), "cam")

    # --- 10 tekne altinda paslanmaz saplama + somun ---
    ys = cy - rt
    ekle("saplama", silindir((0, ys + 2 * MM, zb + 60 * MM), (0, ys - 12 * MM, zb + 60 * MM), 3 * MM, seg=14), "celik")
    ekle("somun", silindir((0, ys, zb + 60 * MM), (0, ys - 5 * MM, zb + 60 * MM), 6 * MM, seg=6), "celik")

    # --- 11 sari etiketler ---
    e0, e1 = y_ust - 56 * MM, y_ust - 8 * MM; ez = D / 2 - tp - 3 * MM
    ekle("bant_ad", etiket_yuzu(-hw - 0.4 * MM, e0, e1, -ez, ez, -1), "etiket_ad")            # −x yuzu: bakanin solu = −z (makine yonu) → ok SOLA
    ekle("bant_montaj", etiket_yuzu(hw + 0.4 * MM, e0, e1, ez, -ez, 1), "etiket_montaj")      # +x yuzu: bakanin solu = +z
    for adi, xx, nx in (("bant_ad_arka", -hw - 0.2 * MM, 1), ("bant_montaj_arka", hw + 0.2 * MM, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0)); ekle(adi, ar.duzelt(), "sari_arka")
    ekle("uyari_1", kutu(-34 * MM, -12 * MM, y_kar + 18 * MM, y_kar + 40 * MM, zf, zf + 0.4 * MM), "sari")
    ekle("uyari_2", kutu(-W / 2 + 8 * MM, -W / 2 + 28 * MM, cy + 30 * MM, cy + 50 * MM, zf, zf + 0.4 * MM), "sari")

    hacim = hacim_litre(hw - et, rt - et, y1, cy, y_ust - 20 * MM, D - 2 * tp)
    return P, hacim


# ======================= glTF =======================
MALZEME = {
    "cam":   dict(renk=(0.82, 0.89, 0.95, 0.32), met=0.0, ruf=0.05, saydam=True),
    "pom":   dict(renk=(0.95, 0.95, 0.93, 1.0), met=0.0, ruf=0.42),
    "celik": dict(renk=(0.78, 0.80, 0.83, 1.0), met=0.95, ruf=0.28),
    "koyu":  dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.2, ruf=0.6),
    "sari":  dict(renk=(0.98, 0.75, 0.09, 1.0), met=0.0, ruf=0.5),
    "etiket_ad": dict(renk=(1, 1, 1, 1), met=0.0, ruf=0.5, doku="ad", tekyuz=True),
    "etiket_montaj": dict(renk=(1, 1, 1, 1), met=0.0, ruf=0.5, doku="montaj", tekyuz=True),
    "sari_arka": dict(renk=(0.93, 0.70, 0.08, 1.0), met=0.0, ruf=0.6, tekyuz=True),
}


def glb_yaz(yol, parcalar, dokular):
    adlar = list(MALZEME.keys()); blob = []; views = []; accs = []; meshes = []; nodes = []; off = [0]

    def gomu(b, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(b)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(b); off[0] += len(b); return len(views) - 1

    for adi, m, mal in parcalar:
        vp = gomu(b"".join(struct.pack("<3f", *p) for p in m.P), 34962)
        vn = gomu(b"".join(struct.pack("<3f", *n) for n in m.N), 34962)
        vi = gomu(b"".join(struct.pack("<I", i) for i in m.I), 34963)
        mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if m.UV:
            vu = gomu(b"".join(struct.pack("<2f", *u) for u in m.UV), 34962)
            accs.append({"bufferView": vu, "componentType": 5126, "count": len(m.UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": adlar.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": adi})

    images, textures, doku_idx = [], [], {}
    for k, veri in dokular.items():
        images.append({"bufferView": gomu(veri), "mimeType": "image/png"}); textures.append({"source": len(images) - 1, "sampler": 0}); doku_idx[k] = len(textures) - 1
    mats = []
    for k in adlar:
        d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
        if d.get("doku"): pbr["baseColorTexture"] = {"index": doku_idx[d["doku"]]}
        mm = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": not d.get("tekyuz", False)}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH kaset_3d_v3"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}],
         "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
         "images": images, "textures": textures, "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js); f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


# ======================= USDZ (iOS AR Quick Look) =======================
# 20 Eyl 2026 DUZELTME: elle yazilan .usda'da "gobek_kulak_-1" gibi GECERSIZ prim adlari vardi → iPhone "acilamadi" dedi.
# Artik Pixar'in resmi kutuphanesi (pip install usd-core) ile yaziliyor: ikili .usdc + gomulu PNG dokular,
# UsdUtils.CreateNewARKitUsdzPackage ile paketlenir ve UsdUtils.ComplianceChecker(arkit=True) ile DENETLENIR.
def _temiz_ad(a):
    a = re.sub(r"[^A-Za-z0-9_]", "_", a.replace("-", "e"))          # "-1" → "e1" (eksi)
    return a if re.match(r"^[A-Za-z_]", a) else "_" + a


def usdz_yaz(yol, kok, parcalar, dokular):
    import shutil, tempfile
    from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Vt, UsdUtils
    tmp = tempfile.mkdtemp(prefix="ak_usdz_")                        # ASCII yol: USD araclari Turkce karakterli yolda takilmasin
    usdc = os.path.join(tmp, kok + ".usdc")
    for k, veri in dokular.items():
        with open(os.path.join(tmp, k + ".png"), "wb") as f: f.write(veri)
    st = Usd.Stage.CreateNew(usdc)
    UsdGeom.SetStageUpAxis(st, UsdGeom.Tokens.y); UsdGeom.SetStageMetersPerUnit(st, 1.0)
    kokp = UsdGeom.Xform.Define(st, "/" + kok); st.SetDefaultPrim(kokp.GetPrim()); Usd.ModelAPI(kokp.GetPrim()).SetKind("component")
    mats = {}
    for k, d in MALZEME.items():
        yolm = "/%s/Mat/%s" % (kok, k)
        mat = UsdShade.Material.Define(st, yolm); sh = UsdShade.Shader.Define(st, yolm + "/PBR"); sh.CreateIdAttr("UsdPreviewSurface")
        r = d["renk"]
        if d.get("doku"):
            rd = UsdShade.Shader.Define(st, yolm + "/stOku"); rd.CreateIdAttr("UsdPrimvarReader_float2")
            rd.CreateInput("varname", Sdf.ValueTypeNames.String).Set("st"); rd.CreateOutput("result", Sdf.ValueTypeNames.Float2)
            tx = UsdShade.Shader.Define(st, yolm + "/doku"); tx.CreateIdAttr("UsdUVTexture")
            tx.CreateInput("file", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath("./" + d["doku"] + ".png"))
            tx.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(rd.ConnectableAPI(), "result")
            tx.CreateInput("wrapS", Sdf.ValueTypeNames.Token).Set("clamp"); tx.CreateInput("wrapT", Sdf.ValueTypeNames.Token).Set("clamp")
            tx.CreateInput("sourceColorSpace", Sdf.ValueTypeNames.Token).Set("sRGB"); tx.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
            sh.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(tx.ConnectableAPI(), "rgb")
        else:
            sh.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(r[0], r[1], r[2]))
        sh.CreateInput("opacity", Sdf.ValueTypeNames.Float).Set(float(r[3]))
        sh.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(float(d["ruf"])); sh.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(float(d["met"]))
        mat.CreateSurfaceOutput().ConnectToSource(sh.ConnectableAPI(), "surface"); mats[k] = mat
    kullanilan = set()
    for adi, m, mal in parcalar:
        ad = _temiz_ad(adi)
        while ad in kullanilan: ad += "_"
        kullanilan.add(ad)
        me = UsdGeom.Mesh.Define(st, "/%s/%s" % (kok, ad))
        me.CreatePointsAttr(Vt.Vec3fArray([Gf.Vec3f(*q) for q in m.P]))
        me.CreateFaceVertexCountsAttr(Vt.IntArray([3] * (len(m.I) // 3))); me.CreateFaceVertexIndicesAttr(Vt.IntArray(list(m.I)))
        me.CreateNormalsAttr(Vt.Vec3fArray([Gf.Vec3f(*q) for q in m.N])); me.SetNormalsInterpolation(UsdGeom.Tokens.vertex)
        me.CreateSubdivisionSchemeAttr(UsdGeom.Tokens.none); me.CreateDoubleSidedAttr(not MALZEME[mal].get("tekyuz", False))
        mn = [min(q[i] for q in m.P) for i in range(3)]; mx = [max(q[i] for q in m.P) for i in range(3)]
        me.CreateExtentAttr(Vt.Vec3fArray([Gf.Vec3f(*mn), Gf.Vec3f(*mx)]))
        if m.UV:                                                     # glTF'te v yukaridan asagi, USD'de asagidan yukari
            UsdGeom.PrimvarsAPI(me).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex).Set(
                Vt.Vec2fArray([Gf.Vec2f(u[0], 1.0 - u[1]) for u in m.UV]))
        UsdShade.MaterialBindingAPI.Apply(me.GetPrim()).Bind(mats[mal])
    st.GetRootLayer().Save()
    cikti = os.path.join(tmp, kok + ".usdz")
    if not UsdUtils.CreateNewARKitUsdzPackage(Sdf.AssetPath(usdc), cikti): raise RuntimeError("ARKit paketi olusturulamadi: " + kok)
    from pxr import UsdValidation
    geri = Usd.Stage.Open(cikti); prim = len(list(geri.Traverse())) if geri else 0
    anahtar = set(["UsdzValidators", "UsdUtilsValidators", "UsdGeomValidators", "UsdShadeValidators", "UsdCoreValidators"])
    secili = [mm for mm in UsdValidation.ValidationRegistry().GetAllValidatorMetadata() if set(mm.GetKeywords()) & anahtar]
    ctx = UsdValidation.ValidationContext(secili, False)
    sorun, uyarilar = [], []
    for e in ctx.Validate(geri):
        satir = "%s: %s" % (e.GetName(), e.GetMessage())
        (sorun if e.GetType() == UsdValidation.ValidationErrorType.Error else uyarilar).append(satir)
    icerik = zipfile.ZipFile(cikti).namelist()
    for hedef in yol if isinstance(yol, (list, tuple)) else [yol]: shutil.copyfile(cikti, hedef)
    boy = os.path.getsize(cikti); shutil.rmtree(tmp, ignore_errors=True)
    return boy, prim, sorun, uyarilar + ["paket icerigi: " + ", ".join(icerik)]


# ======================= URET =======================
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    MONTAJ = ["HELEZONU|TEKNEYE SÜR", "KARIŞTIRICIYI|TAK", "PİMİ|KİLİTLE", "KASETİ|YUVAYA SÜR"]
    for dosya, W, D, H, ad, kasar in (("kaset_v3", 140.0, 400.0, 360.0, "HARÇ KASETİ", False), ("kasar_v3", 280.0, 400.0, 360.0, "KAŞAR KABI", True)):
        parcalar, hacim = kaset_modeli(W, D, H, ad, kasar)
        dokular = {"ad": doku_ad(ad, "bu yönde tak  ·  %d × %d × %d mm  ·  %s L" % (W, D, H, ("%.1f" % hacim).replace(".", ",")), ok_sol=True),
                   "montaj": doku_montaj(MONTAJ)}
        b1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), parcalar, dokular)
        b2, prim, sorun, uyari = usdz_yaz([os.path.join(OUT, dosya + ".usdz"), os.path.join(OUT, dosya + "_ar2.usdz")], dosya, parcalar, dokular)
        ucgen = sum(len(m.I) // 3 for _, m, _ in parcalar)
        print("%s · %d parca · %d ucgen · glb %.0f KB · usdz %.0f KB · KULLANILABILIR HACIM %.1f L (dolum cizgisi ust kenardan 20 mm asagi)"
              % (dosya, len(parcalar), ucgen, b1 / 1024.0, b2 / 1024.0, hacim))
        print("   USDZ geri acildi: %d prim · USD denetimi (usdz + geometri + malzeme): %s" % (prim, "GECTI (hata yok)" if not sorun else "KALDI"))
        for x in sorun: print("   HATA:", x)
        for x in uyari: print("   uyari:", x)
