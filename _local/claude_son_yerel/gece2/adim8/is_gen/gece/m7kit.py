# -*- coding: utf-8 -*-
"""m7: glbkit uzantisi — eklenen parcaya acik kat/mek etiketi + aralik silme + dugum oteleme (animasyon kanallariyla)."""
import numpy as np
from glbkit import Glb as _G


class Glb(_G):
    def ekle_etiket(s, p, X_mm, T_new, kat=None, mek=None, kpk=False):
        n = s.ekle(p, X_mm, T_new, kpk)
        p.setdefault("ekL", []).append((kat, mek))
        return n

    def aralik(s, p, a, n):
        m = np.zeros(len(p["T"]), bool); m[a:a + n] = True; return m & s.gorunur(p)

    def etiket_of(s, p, tri, key="kat"):
        lst = p["pr"].get("extras", {}).get(key) or []
        i = tri * 3
        for k in range(0, len(lst), 3):
            if lst[k + 1] <= i < lst[k + 1] + lst[k + 2]: return lst[k]
        return lst[-3] if lst else None

    def dugum_otele(s, ad, d_mm):
        """animasyonlu dugum: translation + tum translation kanal ciktilari + d (mm). Koseler yerel kalir."""
        J = s.J; d = np.array(d_mm, float) / 1000.0
        ni = [i for i, nd in enumerate(J["nodes"]) if nd.get("name") == ad]
        assert len(ni) == 1, ad
        ni = ni[0]; nd = J["nodes"][ni]
        assert not any(k in nd for k in ("matrix", "scale")), ad
        nd["translation"] = (np.array(nd.get("translation", [0, 0, 0]), float) + d).tolist()
        for p in s.prims:
            if p["nd"] is nd: p["t"] = np.array(nd["translation"], float); p["X"] = p["X"] + d * 1000.0
        acc = set()
        for an in J.get("animations", []):
            for c in an["channels"]:
                if c["target"]["node"] == ni and c["target"]["path"] == "translation":
                    acc.add(an["samplers"][c["sampler"]]["output"])
        s._otelenen_acc = getattr(s, "_otelenen_acc", {})
        for a in acc:
            if a in s._otelenen_acc:
                raise RuntimeError("paylasilan cikti erisimcisi %d (%s / %s)" % (a, s._otelenen_acc[a], ad))
            s._otelenen_acc[a] = ad
            A = J["accessors"][a]; v = J["bufferViews"][A["bufferView"]]
            off = v.get("byteOffset", 0) + A.get("byteOffset", 0); n = A["count"]
            arr = np.frombuffer(bytes(s.BIN[off:off + n * 12]), np.float32).reshape(-1, 3).copy() + d.astype(np.float32)
            s.BIN[off:off + n * 12] = arr.tobytes()
            if "min" in A: A["min"] = arr.min(0).tolist(); A["max"] = arr.max(0).tolist()
        return len(acc)

    def kaydet(s, yol):
        # ekle_etiket ile gelen acik etiketleri glbkit.kaydet'in 'son etiket' kuralina uygula: her ek parcadan once listeye sahte giris
        for p in s.prims:
            if not p.get("ekX"): continue
            ex = p["pr"].setdefault("extras", {})
            L = p.get("ekL", [None] * len(p["ekX"]))
            L = L + [(None, None)] * (len(p["ekX"]) - len(L))
            p["_ekL"] = L
        # glbkit.kaydet kat/mek icin ex[key][-3] kullanir; burada parca parca yaziyoruz
        for p in s.prims:
            if not p.get("ekX"): continue
            pr = p["pr"]; ex = pr.get("extras", {})
            X0 = p["X"]; T0 = p["T"].reshape(-1).astype(np.uint32)
            N0 = s._oku(pr["attributes"]["NORMAL"]).astype(np.float32)
            for k_ in pr["attributes"]:
                if k_ not in ("POSITION", "NORMAL"): raise RuntimeError("ek oznitelik var: " + k_)
            X = np.vstack([X0] + p["ekX"]); N = np.vstack([N0] + [n.astype(np.float32) for n in p["ekN"]])
            I = [T0]; base = len(X0); ibase = len(T0)
            for Xf, kp, (kt, mk) in zip(p["ekX"], p["ekK"], p["_ekL"]):
                k = len(Xf); I.append(np.arange(base, base + k, dtype=np.uint32))
                for key, val in (("kat", kt), ("mek", mk)):
                    if ex.get(key):
                        lab = ex[key][-3] if val is None else val
                        ex[key] = ex[key] + [lab, ibase, k]
                if kp: ex["kpk"] = ex.get("kpk", []) + [ibase, k]
                base += k; ibase += k
            if ex: pr["extras"] = ex
            Xm = ((X / 1000.0) - p["t"]).astype(np.float32)
            pr["attributes"] = {"POSITION": s._ekle_arr(Xm, "VEC3", 34962), "NORMAL": s._ekle_arr(N.astype(np.float32), "VEC3", 34962)}
            pr["indices"] = s._ekle_arr(np.concatenate(I).astype(np.uint32), "SCALAR", 34963)
            p["ekX"] = None; p["degX"] = False; p["degT"] = False
        _G.kaydet(s, yol)
