import json, io, sys
ref = sys.argv[1]; yeni = sys.argv[2]
K = {}
n = None
for k in range(4):
    J = json.load(io.open("%s/havada_par_%d.json" % (ref, k), encoding="utf-8")); n = J["n"]
    for a, v in J["kom"].items(): K[a] = v
Y = json.load(io.open("%s/havada_par_hiz.json" % yeni, encoding="utf-8"))
print("n", n, Y["n"], "aday", len(K), len(Y["kom"]))
fark = [a for a in K if K[a] != Y["kom"].get(a)]
print("kom farkli aday:", len(fark), fark[:5])
for a in fark[:3]: print(a, sorted(set(K[a]) ^ set(Y["kom"][a])))
r1 = json.load(io.open("%s/havada_hizli_v1.json" % ref, encoding="utf-8")); r2 = json.load(io.open("%s/havada_hizli_v1.json" % yeni, encoding="utf-8"))
print("havada_hizli ayni:", r1 == r2, r1, r2)
