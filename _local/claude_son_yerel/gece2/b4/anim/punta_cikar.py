import os, sys, json
W=r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec'
os.environ.setdefault('AUTOKITCH_SAC_STANDART', os.path.join(W,'h3','yama_v9','sac_standart'))
os.environ['ADIM5']=os.path.join(W,'h3','yama_v9','veri')
sys.path.insert(0, os.path.join(W,'h3')); sys.path.insert(0, W)
sys.stdout.reconfigure(encoding='utf-8')
import h3_b_sac_v1 as B
B.kur()
G=B.G
out=[]
for s in G.SAC:
    for k in getattr(s,'puntalar',[]): out.append(k)
print(len(G.SAC), 'sac ·', len(out), 'punta kaydı', sum(k['adet'] for k in out))
json.dump(out, open('puntalar_B.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
for k in out[:8]: print(k['parcalar'], k['adet'], k['not_'])
