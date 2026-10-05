# -*- coding: utf-8 -*-
import json
W = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3"
M = json.load(open(W + r"\mekanizma_v3_8.json", encoding="utf-8"))
print("M keys", list(M.keys()))
for k, v in M.items():
    if isinstance(v, (str, int, float)): print(" ", k, "=", str(v)[:300])
    elif isinstance(v, dict): print(" ", k, "dict", len(v), list(v.items())[:4])
    else: print(" ", k, type(v).__name__, len(v), json.dumps(v[:3], ensure_ascii=False)[:600])
def ara(o, yol=""):
    if isinstance(o, dict):
        for k, v in o.items(): ara(v, yol + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): ara(v, yol + "[%d]" % i)
    elif isinstance(o, str) and ("Sos" in o or "SOS" in o or "sos" in o or "Harç" in o or "Kıyma" in o):
        print("   ", yol[:120], "=", o[:160])
ara(M)
P = json.load(open(W + r"\parca_kutulari.json", encoding="utf-8"))
print("P keys", list(P.keys()))
for k, v in P.items():
    if isinstance(v, dict): print(" ", k, "dict", len(v), json.dumps(list(v.items())[:2], ensure_ascii=False)[:500])
    else: print(" ", k, str(v)[:200])
print(json.dumps(P["parca"].get("TOPPING_MODUL", [])[:5], ensure_ascii=False))
print(len(P["parca"].get("TOPPING_MODUL", [])))
print(P["birim"].get("TOPPING_MODUL"))
