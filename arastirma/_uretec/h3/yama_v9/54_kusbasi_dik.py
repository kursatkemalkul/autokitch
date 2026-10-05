# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 54 · KUŞBAŞI HUNİSİ TAM DİK KENAR (4 Eki 2026 · Claude · YEREL · Kemal: "o aralık boş olmalı; UNO haznesini arkaya doğru DÜZ yap,
pipe aşağıya insin ve UNO çıkabilsin")
python 54_kusbasi_dik.py girdi.glb cikti.glb      (zincir: hat3_v9u.glb → hat3_v9v.glb)

Adım 53'te alt 2. UNO (KUŞBAŞI) hunisinde yalnız ön-sağ köşe cebi (x ≥ 1879,1 · z ≥ −201) vardı: hazne kıyma hortumunu (orta UNO düşme hattı,
x 1911,5 · z −170, D32 hortum dış Ø41,6) iki yandan sarıyordu. Yeni hazne EKSANTRİK: sağ (hortum tarafı) duvarı ÖNDEN ARKAYA TAM BOY DİK düz
düzlem x = 1880,0 (Ø64 boyun dış yüzüyle teğet → boyundan üst kenara kadar tek düz yüz; analizdeki "tam dik kenar" seçeneği) ·
sol / ön / arka / üst ölçüler, boyun (1848, −387, r 32), dikey köşeler R25, et 1,5 adım 53 ile aynı (53_menu7.hazne fonksiyonunun kopyası).
Hortum, düşme noktası, raf / taban delikleri DEĞİŞMEZ. Etiket (kat / mek / kpk) eski hazneden.
Denetim (bu betikte): eski hazne tek bileşen olarak bulunur · yeni kabuk kapalı · iç hacim ≥ 2 günlük ihtiyacın brüt karşılığı (3,4 L / 0,90)."""
import os, sys, time, json, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))

ESKI = ('TOPPING_MODUL__paslanmaz', (1753.0, 1284.0, -560.0), (1943.0, 1499.0, -120.0))    # adım 53 kuşbaşı hunisi (cepli)
NX, Y0, Y1, YT, X0 = 1848.0, 1284.0, 1464.0, 1499.0, 1753.0
X_DIK = 1880.0                                    # sağ dik duvar dış yüzü (boyun dış yüzü 1848 + 32)
NECK_Z, NECK_R, ET, KOSE_R = -387.0, 32.0, 1.5, 25.0
HZ0, HZ1 = -560.0, -120.0
IHTIYAC_L = 3.4                                   # 2 gün kuşbaşı (ANALIZ.md: 2,9 kg · 0,853 g/ml)
DOLUM = 0.90                                      # kullanılabilir = brüt × 0,90


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


def mf_ucg(m):
    M = m.to_mesh(); V = np.asarray(M.vert_properties)[:, :3].astype(float); T = np.asarray(M.tri_verts).astype(np.int64)
    return V[T]


def kutu_mf(lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    return mf.Manifold.cube(hi - lo).translate(lo)


def rrect(x0, x1, z0, z1, r, k=10):
    P = []
    for cx, cz, a0 in [(x1 - r, z0 + r, -90), (x1 - r, z1 - r, 0), (x0 + r, z1 - r, 90), (x0 + r, z0 + r, 180)]:
        for a in np.linspace(a0, a0 + 90, k): P.append((cx + r * np.cos(np.radians(a)), cz + r * np.sin(np.radians(a))))
    return np.array(P)


def kat_y(P2, y):
    return np.c_[P2[:, 0], np.full(len(P2), y), P2[:, 1]]


def daire(cx, cz, r, n=64):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False); return np.c_[cx + r * np.cos(t), cz + r * np.sin(t)]


def hazne(nx, y0, y1, yt, x0, x1):
    """53_menu7.hazne (cepsiz) — kare-yuvarlak geçiş hunisi (dışbükey zarf) + düz kutu, dikey köşe R25, et 1,5, üstü açık"""
    dis = mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R), y0), kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), y1)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), y1), kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), yt)].tolist())
    ri = rrect(x0 + ET, x1 - ET, HZ0 + ET, HZ1 - ET, KOSE_R - ET)
    ic = mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R - ET), y0), kat_y(ri, y1)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(ri, y1), kat_y(ri, yt + 5.0)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R - ET), y0 - 5.0), kat_y(daire(nx, NECK_Z, NECK_R - ET), y0)].tolist())
    kab = dis - ic
    bosluk = ic ^ kutu_mf((x0 - 50, y0, HZ0 - 50), (x1 + 50, yt, HZ1 + 50))
    assert kab.status() == mf.Error.NoError and kab.genus() >= 0
    return kab, bosluk


g = Glb(gi)
b = g.bilesen(ESKI[0], lo=np.array(ESKI[1]), hi=np.array(ESKI[2]), tol=0.3)
kat, mek, kpk = g.etiket_b(b)
KOD = [m["kod"] for m in g.J["scenes"][0]["extras"]["mekanizmalar"]]
assert KOD[mek] == "TOPPING/Kuşbaşı", "ADIM 54 DUR: hazne etiketi %s" % KOD[mek]
eski_n = len(ucg(b))
kab, bos = hazne(NX, Y0, Y1, YT, X0, X_DIK)
lo, hi = kab.bounding_box()[:3], kab.bounding_box()[3:]
assert abs(hi[0] - X_DIK) < 0.01 and abs(lo[0] - X0) < 0.01, "kutu"
hacim = bos.volume() / 1e6
assert hacim * DOLUM >= IHTIYAC_L, "ADIM 54 DUR: hacim yetmiyor %.2f L" % hacim
g.sil_b(b); g.ekle_dugum(ESKI[0], mf_ucg(kab), kat=kat, mek=mek, kpk=kpk)
LOG("kuşbaşı hunisi: eski %d üçgen (cepli) → yeni %d üçgen · sağ dik duvar x %.1f (boyundan üste düz) · kutu %s … %s · iç hacim %.2f L brüt / %.2f L kullanılabilir (ihtiyaç %.1f L)"
    % (eski_n, kab.num_tri(), X_DIK, np.round(lo, 1).tolist(), np.round(hi, 1).tolist(), hacim, hacim * DOLUM, IHTIYAC_L))
tmp = go + ".d54.glb"; g.kaydet(tmp); del g
r = subprocess.run([sys.executable, os.path.join(HERE, "50_sikilastir.py"), tmp, go]); assert r.returncode == 0
os.remove(tmp)
KAYIT = dict(adim=54, ad="kuşbaşı hunisi tam dik kenar", eski=dict(dugum=ESKI[0], kutu=[ESKI[1], ESKI[2]], ucgen=eski_n),
             yeni=dict(kutu=[np.round(lo, 2).tolist(), np.round(hi, 2).tolist()], x_dik=X_DIK, ic_hacim_L=round(hacim, 3),
                       kullanilabilir_L=round(hacim * DOLUM, 3), ihtiyac_L=IHTIYAC_L, ucgen=int(kab.num_tri())), log=SE.LOG)
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=float)
LOG("ADIM 54 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
