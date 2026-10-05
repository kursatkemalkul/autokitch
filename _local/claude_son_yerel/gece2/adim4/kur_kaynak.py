# -*- coding: utf-8 -*-
"""Adım 4 · yama zinciri kaynaklarını scratchpad'den W\\arastirma\\_uretec\\h3\\yama_v9\\kaynak\\ altına kopyalar (klasör düzeni AYNEN korunur).
Mutlak scratchpad / v7 worktree yolları yer tutucuya çevrilir (@@KOK_W@@ vb.); yap_hat3_montaj_v9.py çalışırken bunları iş klasörüyle doldurur.
python kur_kaynak.py <hedef_kaynak_klasoru>"""
import os, sys, shutil, re, io
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
HED = sys.argv[1]
KLAS = ["", "tg", "ug", "eg", "ba", "gece", "gece/m8", "gece/m8/kablo_is", "gece/m8t2", "gece/m8t3", "grup", "topfix", "paket", "kalt",
        "tpaket", "birlesim", "kalanlar", "elk2", "elk3", "elk4", "elk5", "salt", "derz", "gece2/adim2", "gece2/adim2/hava", "gece2/adim3"]
VERI = (".json", ".pkl", ".npy", ".npz", ".csv")
YER = [  # (eski, yer tutucu) — uzun olan önce
    ("C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v7/otonom/hat3d/v3/parca_kutulari.json", "@@PK_V7_F@@"),
    (r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v7\otonom\hat3d\v3\parca_kutulari.json", "@@PK_V7_W@@"),
    ("/c/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v7/otonom/hat3d/v3/parca_kutulari.json", "@@PK_V7_M@@"),
    (r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\mekanizma_v3.json", "@@MEK_V3_W@@"),
    (r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3", "@@H3_W@@"),
    (S, "@@KOK_W@@"),
    (S.replace("\\", "\\\\"), "@@KOK_WW@@"),
    (S.replace("\\", "/"), "@@KOK_F@@"),
    ("/c" + S[2:].replace("\\", "/"), "@@KOK_M@@"),
]
say = dict(py=0, sh=0, veri=0, yer=0)
for k in KLAS:
    kd = os.path.join(S, k)
    for f in sorted(os.listdir(kd)):
        p = os.path.join(kd, f)
        if not os.path.isfile(p): continue
        e = os.path.splitext(f)[1].lower()
        if e in (".py", ".sh"):
            s = io.open(p, encoding="utf-8", errors="surrogateescape").read()
            for a, b in YER:
                if a in s: say["yer"] += s.count(a); s = s.replace(a, b)
            q = os.path.join(HED, k, f); os.makedirs(os.path.dirname(q), exist_ok=True)
            io.open(q, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)
            say["py" if e == ".py" else "sh"] += 1
        elif e in VERI and os.path.getsize(p) <= 5_000_000 and not f.startswith(("m8_onbellek", "m8_parca")):
            q = os.path.join(HED, k, f); os.makedirs(os.path.dirname(q), exist_ok=True); shutil.copy2(p, q); say["veri"] += 1
# kaset üreteci yamaları (gece2 adım 3) + v7 parça kutuları (ara girdi)
U = os.path.join(HED, "_uretec_yama"); os.makedirs(U, exist_ok=True)
for f in ("kasar_cad_v15.py", "sucuk_cad_v9.py", "kaset_birlesim_v2.py", "kaset_kontrol_adim3.py"):
    shutil.copy2(os.path.join(S, "gece2", "adim3", "uretec_yama", f), os.path.join(U, f))
shutil.copy2(os.path.join(S, "gece2", "adim3", "URETEC_NOTU.md"), os.path.join(U, "URETEC_NOTU.md"))
os.makedirs(os.path.join(HED, "_v7"), exist_ok=True)
shutil.copy2(r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v7\otonom\hat3d\v3\parca_kutulari.json", os.path.join(HED, "_v7", "parca_kutulari.json"))
shutil.copy2(r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\mekanizma_v3.json", os.path.join(HED, "_v7", "mekanizma_v3.json"))
print(say)
# kalan mutlak yol taraması
for r, ds, fs in os.walk(HED):
    for f in fs:
        if f.endswith((".py", ".sh")):
            s = io.open(os.path.join(r, f), encoding="utf-8", errors="surrogateescape").read()
            for m in re.finditer(r"(?i)(c:[\\/]+users|/c/users)[^\n\"']{0,120}", s):
                print("MUTLAK", os.path.relpath(os.path.join(r, f), HED), m.group(0)[:140])
# v9 · a1_kaset: üreteç klasörü YAMA_URETEC'ten, _uretec_yama en önde
p = os.path.join(HED, "gece2", "adim3", "a1_kaset.py"); s = io.open(p, encoding="utf-8").read()
a = '''U = os.path.join(HERE, "u", "arastirma", "_uretec")
for q in (os.path.join(S, "gece"), S, U): sys.path.insert(0, q)'''
b = '''U = os.environ.get("YAMA_URETEC") or os.path.join(HERE, "u", "arastirma", "_uretec")   # v9 zinciri: derleme ağacının arastirma/_uretec'i (YAMA_URETEC)
for q in (os.path.join(S, "gece"), S, U, os.path.join(S, "_uretec_yama")): sys.path.insert(0, q)   # v9: kasar_cad_v15 / sucuk_cad_v9 / kaset_birlesim_v2 = kaynak/_uretec_yama (en önde)'''
if a in s: s = s.replace(a, b); io.open(p, "w", encoding="utf-8", newline="").write(s); print("a1_kaset yamalandı")
