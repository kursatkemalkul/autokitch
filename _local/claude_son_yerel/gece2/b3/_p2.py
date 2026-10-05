import pickle, numpy as np, sys, trimesh
from trimesh.intersections import mesh_plane
sys.stdout.reconfigure(encoding='utf-8')
D=pickle.load(open('b3_parca.pkl','rb')); P=D['P']
def sec(names, o, n, ax, lo=None, hi=None):
    for a in names:
        m=trimesh.Trimesh(P[a]['V'],P[a]['F'],process=False)
        s=mesh_plane(m, n, o)
        if not len(s): print('  %-26s -'%a); continue
        Q=s.reshape(-1,3)[:,ax]
        if lo is not None:
            k=np.all((Q>=lo)&(Q<=hi),1); Q=Q[k]
        if not len(Q): print('  %-26s (pencere dışı)'%a); continue
        u=np.unique(np.round(Q,2),axis=0)
        print('  %-26s'%a, np.round(Q.min(0),2), np.round(Q.max(0),2), 'nokta', len(u), u[:14].tolist() if len(u)<=14 else '')
print('--- sol duvar z=-400, pencere x 730-800, y 118-170 (alt köşe)')
sec(['g_dis_sol_yan','g_kosebent_sol_alt_2','g_pu_sol','g_ic_sol_duvar','g_dis_taban_1','g_pu_taban_0','g_ic_taban_1'],[0,0,-400],[0,0,1],[0,1],np.array([730,118]),np.array([800,170]))
print('--- sol duvar z=-400, pencere x 730-800, y 740-790 (üst köşe)')
sec(['g_dis_sol_yan','g_kosebent_sol_ust_2','g_pu_sol','g_ic_sol_duvar','g_dis_tavan_1','g_pu_tavan_yuksek','g_ic_tavan_1'],[0,0,-400],[0,0,1],[0,1],np.array([730,740]),np.array([800,790]))
print('--- arka x=1600 pencere y 118-170, z -835..-785')
sec(['g_dis_arka_1','g_pu_arka_yuksek','g_ic_arka_1','g_dis_taban_1','g_pu_taban_0','g_ic_taban_1'],[1600,0,0],[1,0,0],[1,2],np.array([118,-835]),np.array([170,-785]))
print('--- arka x=1600 pencere y 740-790')
sec(['g_dis_arka_1','g_pu_arka_yuksek','g_ic_arka_1','g_dis_tavan_1','g_pu_tavan_yuksek','g_ic_tavan_1'],[1600,0,0],[1,0,0],[1,2],np.array([740,-835]),np.array([790,-785]))
print('--- köşe y=450 pencere x 730-810 z -835..-785')
sec(['g_dis_sol_yan','g_dis_arka_1','g_pu_sol','g_pu_arka_yuksek','g_ic_sol_duvar','g_ic_arka_1'],[0,450,0],[0,1,0],[0,2],np.array([730,-835]),np.array([810,-785]))
