# -*- coding: utf-8 -*-
p = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat\mekanizma-v3.js"
s = open(p, encoding="utf-8").read()
a = "hazir = false; kuruluyor = null; kayit = []; mod = null; bildir(); bekle().then(() => { if (P.agac && D) agacKur(); });"
assert a in s
s = s.replace(a, "hazir = false; kuruluyor = null; kayit = []; mod = null; vurgu.clear(); bildir(); bekle().then(() => { if (P.agac && D) agacKur(); disiplinKur(); });")
b = "      bekle().then(() => {\n        agacKur();\n"
assert b in s
s = s.replace(b, "      bekle().then(() => {\n        agacKur(); disiplinKur();\n")
L = s.split("\n")
i = [k for k, x in enumerate(L) if x.startswith("    const not = el('div', 'mk-not', ")][0]
eski = L[i][len("    const not = el('div', 'mk-not', "):-2]
L[i] = ("    const not = el('div', 'mk-not', DISIPLIN ? 'İstasyon başlığına bas ya da 3B\\'de istasyona çift tıkla: istasyon tam montajıyla açılır. "
        "Üniteye bas: yalnız o ünite (motoru, sensörü, silindiri içinde; kablosu istasyonun Elektrik ünitesinde). "
        "Disiplin vurgusu (Motor · Sensör · Hava · Elektrik …) modelin üstündeki düğmelerden.' : " + eski + ");")
s = "\n".join(L)
s = s.replace("_kayit: () => kayit, _liste: () => LISTE", "_kayit: () => kayit, _liste: () => LISTE, vurgu: () => [...vurgu], disiplinSec")
s = s.replace("/* mekanizma-v3.js · v1 (1 Eki 2026)", "/* mekanizma-v3.js · v2 (3 Eki 2026: disiplin vurgusu + MEK3_JSON) · v1 (1 Eki 2026)", 1)
open(p, "w", encoding="utf-8").write(s)
print("tamam")
