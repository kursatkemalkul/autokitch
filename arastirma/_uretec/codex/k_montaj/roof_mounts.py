"""K roof's U interface: 3mm spacer + two 4mm threaded plates per location.

Actual external M8x16 shafts were measured at Y1847.5..1863.5 in source61.
The 8 mm threaded pack ends at Y1849.5: 2 mm protrusion = 1.6 M8 threads.
U remains untouched. No purchased nut is modified. All CAD coordinates mm.
"""
from lower_support import *

def build_roof():
    factory=K.kur(); roof=next(s for s in factory.SAC if s.ad=='ust_sac')
    for x in (100.,300.):roof.paneller[0].delik(x,700,9,tip='vida_deligi')
    rp=roof.parca();rp['sh']=rp['sh'].translate((4000,0,0));rp['wp']=cq.Workplane('XY').add(rp['sh'])
    parts=[rp];joins=[]
    for x in (4100.,4300.):
        z=-700.
        for i,(y,t,diam) in enumerate(((1849.5,4,6.8),(1853.5,4,6.8),(1857.5,3,9))):
            s=S.Sac(f'k73_tavan_baglanti_plakasi_{int(x)}_{i}',rol='braket',t=t,R=1.5*t,birim='K_GOVDE')
            q=s.taban([(x-12,-z-12),(x+12,-z-12),(x+12,-z+12),(x-12,-z+12)],O=(0,y,0),ex=(1,0,0),ey=(0,0,-1))
            q.delik(x,-z,diam,tip='dis_pilotu' if i<2 else 'vida_deligi')
            p=s.parca();p['dfm']=clean(s.dfm(abkant=False));p['flat']=s.acinim();parts.append(p)
        for seam_y in (1853.5,1857.5,1860.5):
          for edge in range(4):
            a=[(x-12,seam_y,z-12),(x+12,seam_y,z-12),(x+12,seam_y,z+12),(x-12,seam_y,z+12)][edge]
            b=[(x+12,seam_y,z-12),(x+12,seam_y,z+12),(x-12,seam_y,z+12),(x-12,seam_y,z-12)][edge]
            n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][edge]
            parts.append(S.kaynak_dikisi(a,b,n,(0,1,0),.8,ad=f'k73_tavan_kaynagi_{int(x)}_{seam_y}_{edge}',birim='K_GOVDE',not_='TIG 141 ER308LSi; dry underside; sealed perimeter'))
        joins.append({'id':f'UKE_K_{int(x)}','external_source_node':'U_KE_GOVDE__paslanmaz','external_screw_unchanged':True,'axis':[0,-1,0],'screw_seat_mm':[x,1863.5,z],'screw_tip_mm':[x,1847.5,z],'length_mm':16,'thread':'M8 tapped after welding; two 4mm plates','engagement_mm':8.,'protrusion_mm':2.,'protrusion_threads':1.6})
    return parts,{'step':73,'roof_dfm':clean(roof.dfm(abkant=True)),'connections':joins,'operation':'laser profiles and pilot holes; weld pack; tap M8 through both 4mm plates after welding','external_U_geometry_modified':False,'production_released':False},roof

if __name__=='__main__':
    parts,r,_=build_roof();S.glb_yaz(str(OUT/'k73_roof.glb'),parts)
    (OUT/'k73_roof.json').write_text(json.dumps(clean(r),ensure_ascii=False,indent=2),encoding='utf8')
    checks=r['roof_dfm']+[c for p in parts for c in p.get('dfm',[])]
    print('ROOF_PARTS',len(parts),'DFM_BAD',[c for c in checks if c['durum']!='GEÇTİ'],flush=True)
    sys.stdout.flush();os._exit(0 if all(c['durum']=='GEÇTİ' for c in checks) else 2)
