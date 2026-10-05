import json,numpy as np,sys,collections
sys.path.insert(0,'.')
import m8t2_ana as A, m8t2_yol as Y, m8t2_rota_eski as RE
def bolge(m):
    x,y,z=m
    if y>2100 and x>3300: return 'T/UF1'
    if y>2100: return 'UF2-4'
    if y>1250: return 'GV/FB'
    if y>1095: return 'RU'
    if y>744 and x<2460: return 'RL'
    if y>740: return 'FA'
    if y>60: return 'TS'
    return 'zemin'
if sys.argv[1]=='eski':
    O,_=RE.eski(); YL={a:(r,np.array(p)) for a,(r,m,p) in O.items()}
else:
    d=json.load(open(sys.argv[1]))
    YL={a:(k['r'],Y.kur(k,[tuple(p) for p in d[a]['prm']])) for a,k in A.K.items()}
c=Y.carpisma(YL)
pairs=set((a,b,bolge(m)) for a,b,m,dd in c)
print(len(c),'segment-cifti', len(pairs),'kablo-cifti/bolge', collections.Counter(p[2] for p in pairs))
