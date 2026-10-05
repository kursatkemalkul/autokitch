# -*- coding: utf-8 -*-
"""q1 · ÜRÜN YIĞINLARI MAKİNE KADEMESİNDE (iş 6). Yalnız GLB etiketi (mek) değişir; geometri / kat (URUN) aynı.
Sayfa makine kademesi = istasyonlar A,B,TOPPING,F,K,E,U,Elektrik (+Çevre/Zemin) → Çevre/Ürün olan makine içi yığınlar gizleniyordu.
  D_PIZZA_YEDEK_UST (fırın üstü pizza kutusu yığını, F üst kabin içinde)  → F/Gövde
  U_KUTU_YEDEK (U içinde, F üstü kutu yedeği) · U_ICECEK_YEDEK (U içinde içecek yedeği) → U/Gövde
  URUN__top (B çekmecesindeki hamur topu, sabit görsel)                    → B/Çekmeceler
Animasyonlu URUN__* (sipariş akışı, ölçek 0) Çevre/Ürün'de kalır. Düğüm ADI ile çalışır → TOPPING çıktısına tekrar uygulanabilir.
python q1_urun.py giris.glb cikis.glb"""
import sys
from _env import *
import glbkit
gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)
MEK = [m["kod"] for m in G.J["scenes"][0]["extras"]["mekanizmalar"]]
HEDEF = {"D_PIZZA_YEDEK_UST__karton": "F/Gövde", "U_KUTU_YEDEK__karton": "U/Gövde",
         "U_ICECEK_YEDEK__karton": "U/Gövde", "URUN__top": "B/Çekmeceler"}
n = 0
for p in G.prims:
    if p["name"] not in HEDEF: continue
    ex = p["pr"].setdefault("extras", {})
    eski = sorted(set(ex.get("mek", [])[0::3]))
    assert all(MEK[i] == "Çevre/Ürün" for i in eski) or all(MEK[i] == HEDEF[p["name"]] for i in eski), (p["name"], eski)
    ex["mek"] = [MEK.index(HEDEF[p["name"]]), 0, len(p["T"]) * 3]
    print("  %-28s %s -> %s (%d ucgen)" % (p["name"], [MEK[i] for i in eski], HEDEF[p["name"]], len(p["T"])))
    n += 1
assert n == 4, n
G.kaydet(go); print("yazildi", go)
