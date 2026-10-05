import sys, time
sys.path.insert(0, '.')
import tgeo as G
t = time.time()
S = G.dis_kabuk(); print({k: round(v.Volume()) for k, v in S.items()}, round(time.time() - t, 1))
S, A = G.cep(); print({k: round(v.Volume()) for k, v in S.items()})
print({k: round(v.Volume()) for k, v in G.teknik().items()})
g, k = G.menteseler(); f = G.on_cerceve(g); print('cerceve', round(f.Volume()), f.isValid())
for kn in ('K1', 'K2'):
    o = G.kanat(kn, list(k.values())); print({a: round(b.Volume()) for a, b in o.items()})
K, C, R, H = G.kuru_duzen(); print(len(K), len(C), len(R), len(H), round(time.time() - t, 1))
