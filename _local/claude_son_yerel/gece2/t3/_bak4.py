import pickle, numpy as np, sys, trimesh
sys.stdout.reconfigure(encoding='utf-8')
D = pickle.load(open('t3_parca.pkl','rb'))['P']
for a in ('kaset_kasar','kaset_sucuk'):
    m = trimesh.Trimesh(D[a]['V'], D[a]['F'], process=False)
    # slice below 1152.5: clip
    for y in (1144.5,1146,1148,1150,1151.5,1152.3):
        s = m.section(plane_origin=[0,y,0], plane_normal=[0,1,0])
        if s is None: print(a,y,'yok'); continue
        V=s.vertices; print(a, y, 'x', round(V[:,0].min(),1), round(V[:,0].max(),1), 'z', round(V[:,2].min(),1), round(V[:,2].max(),1))
        # x ranges for z > -116 (front of kovan) 
        f = V[V[:,2]>-116]
        if len(f): print('    front part x', round(f[:,0].min(),1), round(f[:,0].max(),1), 'z', round(f[:,2].min(),1), round(f[:,2].max(),1))
