"""Step62: exact step61 machine + fixed 3x4 QR, migrated devices, safety mounting.
Units: CAD mm, glTF metres, Y up. This is a reviewed layout, NOT safety certification.
Run build.py source.glb output.glb; add_robot.mjs then adds the native UR10e.
"""
from pathlib import Path
import sys, json, hashlib, copy
import numpy as np
import cadquery as cq
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'h3'/'yama_v9'))
from sac_ent import Ham
SOURCE_SHA='948b20c4520cf917711a8dea730ea037379793b11bb6e975c649155c83ef9c1d'
P=[]; MIG=[]; OPEN=[]
def box(lo,hi):
    return cq.Solid.makeBox(*[b-a for a,b in zip(lo,hi)],cq.Vector(*lo))
def cyl(x,y,z,r,h):
    return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(0,0,1))
def add(name,lo,hi,kind='steel',join='TIG',holes=()):
    sh=box(lo,hi)
    for x,y,r in holes: sh=sh.cut(cyl(x,y,lo[2]-1,r,hi[2]-lo[2]+2))
    P.append(dict(ad=name,sh=sh,kind=kind,join=join,holes=list(holes)))
    return P[-1]
def screws(name,centres,z0,thickness):
    # M5 x30 through device20 + bracket3 + washer1 + nut5; 1mm protrusion.
    for k,(x,y) in enumerate(centres):
        add(name+f'_M5_{k}',(x-4.25,y-4.25,z0+thickness+1),(x+4.25,y+4.25,z0+thickness+6),'steel','M5 ISO4762 A2-80 (manufacturer requirement)')
        P[-1]['sh']=cyl(x,y,z0+thickness+1,4.25,5).cut(cyl(x,y,z0+thickness+3,2.1,4))
        add(name+f'_washer_{k}',(x-5,y-5,z0+thickness),(x+5,y+5,z0+thickness+1),'steel','ISO7089')
        P[-1]['sh']=cyl(x,y,z0+thickness,5,1).cut(cyl(x,y,z0+thickness-1,2.75,3))
        add(name+f'_stem_{k}',(x-2.5,y-2.5,z0+thickness-29),(x+2.5,y+2.5,z0+thickness+1),'steel','M5x30')
        P[-1]['sh']=cyl(x,y,z0+thickness-29,2.5,30)
        add(name+f'_nut_{k}',(x-4,y-4,z0-8),(x+4,y+4,z0-3),'steel','ISO10511 M5')
        P[-1]['sh']=cyl(x,y,z0-8,4,5).cut(cyl(x,y,z0-9,2.5,7))
def lock(name,x,y,z):
    # AZM40Z-I1-ST-1P2P-PH; actual envelope119.5x40x20 and100mm body mounting pitch.
    # Right-hand fixed body, actuator left, matching the manufacturer drawing mirrored.
    body=[(x+20,y+10),(x+20,y+110)]
    act=[(x-27,y+87.25),(x-27,y+111.75)]
    add(name+'_fixed_bracket',(x,y-6,z-3),(x+40,y+125.5,z),'steel','TIG fixed front post',[(a,b,2.75) for a,b in body])
    add(name+'_AZM40Z',(x,y,z),(x+40,y+119.5,z+20),'yellow','bolted fixed bracket',[(a,b,2.75) for a,b in body])
    add(name+'_door_bracket',(x-47,y+79.5,z-3),(x-7,y+119.5,z),'steel','TIG door frame',[(a,b,2.75) for a,b in act])
    add(name+'_AZM40_B1',(x-47,y+79.5,z),(x-7,y+119.5,z+20),'black','bolted door bracket',[(a,b,2.75) for a,b in act])
    # Catalogue tongue represented separately. Internal bolt/solenoid intentionally omitted.
    add(name+'_tongue',(x-7,y+94.5,z+5),(x,y+104.5,z+13),'black','actuator tongue')
    screws(name+'_body',body,z,20); screws(name+'_actuator',act,z,20)
def qr():
    xs=[3769.,4256.,4743.]; floors=[588.,850.,1112.,1374.]
    # Hollow formed partitions: 3mm skins, not12mm solid sheet. Same tested envelopes.
    for i,x in enumerate([3757.,4244.,4731.,5218.]):
        a,b=(0,2050) if i in (0,3) else (585,1624)
        add(f'QR62_column_{i}_left',(x,a,1750),(x+3,b,2074))
        add(f'QR62_column_{i}_right',(x+9,a,1750),(x+12,b,2074))
        add(f'QR62_column_{i}_robot_lip',(x+3,a,1750),(x+9,b,1753))
        add(f'QR62_column_{i}_customer_lip',(x+3,a,2071),(x+9,b,2074))
    for c,x in enumerate(xs):
        for y in [20,588,850,1112,1374,1627,1653,2050]:
            # Roof underside1624: exactly the tested highest bay clearance.
            add(f'QR62_shelf_{c}_{y}',(x,y-3,1750),(x+475,y,2074))
        for r,y in enumerate(floors):
            end=x+475; name=f'QR62_BAY_{r*3+c+1:02d}'
            # All customer hardware is OUTSIDE the tested robot/product envelope z<=2074.
            add(name+'_fixed_post',(end-40,y,2074),(end,y+250,2077),holes=[(end-20,y+70,4.5),(end-20,y+170,4.5)])
            add(name+'_door',(x+3,y+3,2074),(end-43,y+247,2077),'clear','hinged customer door',[(end-67,y+147.25,4.5),(end-67,y+171.75,4.5)])
            # Metal door edging is outside the acrylic pane: no solid intersections.
            for side,lo,hi in [('bottom',(x+3,y,2074),(end-43,y+3,2077)),('top',(x+3,y+247,2074),(end-43,y+250,2077)),('left',(x,y,2074),(x+3,y+250,2077))]:
                add(name+'_door_'+side,lo,hi,'steel','door edge frame')
            # Actuator attaches to this right-hand frame (same door, welded bracket).
            add(name+'_door_right',(end-47,y+3,2077),(end-40,y+247,2080),'steel','door frame')
            for j,h in enumerate([y+35,y+215]):
                # Mechanical hinge barrel, anchored by welded leaves; pin belongs to hinge.
                add(name+f'_hinge_leaf_{j}',(x-3,h-10,2074),(x,h+10,2080),'steel','TIG fixed column')
                add(name+f'_hinge_pin_{j}',(x,h-10,2077),(x+6,h+10,2083),'steel','retained hinge pin')
            lock(name,end-40,y+60,2080)
            # Cable connector goes down from lock, then into hollow covered channel.
            add(name+'_M12',(end-16,y+46.5,2084),(end-4,y+60,2096),'black','lock connector')
            P[-1]['sh']=cq.Solid.makeCylinder(6,13.5,cq.Vector(end-10,y+46.5,2090),cq.Vector(0,1,0))
            add(name+'_lock_cable',(end-12,y+40,2090),(end-8,y+46.5,2112),'black','M12 cable into covered duct')
            P[-1]['sh']=cyl(end-10,y+42,2090,2,22).fuse(cq.Solid.makeCylinder(2,4.5,cq.Vector(end-10,y+42,2090),cq.Vector(0,1,0)))
            add(name+'_duct_clip',(end-15,y+230,2077),(end,y+233,2110),'steel','TIG fixed front post')
        add(f'QR62_cable_duct_{c}',(x+460,588,2110),(x+475,1640,2125),'black','fixed front post clips')
        duct=P[-1];duct['sh']=duct['sh'].cut(box((x+461,587,2111),(x+474,1641,2124)))
        for y in floors:duct['sh']=duct['sh'].cut(cyl(x+465,y+42,2109,3,4))
    # Upper service section: fixed supports for migrated exact-size devices.
    add('QR62_main_panel_backplate',(3810,1653,2052),(4140,1940,2055))
    add('QR62_lock_board_backplate',(4610,1653,2043),(4920,2047,2046))
    for y in [1653,2044]: add(f'QR62_board_standoff_{y}',(4610,y,2046),(4920,y+3,2055))
    for y in [1653,2045]: add(f'QR62_upper_back_cross_{y}',(3769,y,2055),(5218,y+2,2071.5))
    add('QR62_upper_service_cover',(3769,1653,1750),(5218,2047,1751.5),'steel','removable; service fastening still pending')
    add('QR62_lower_service_cover',(3769,20,1750),(5218,585,1751.5),'steel','removable; service fastening still pending')
    panel=add('QR62_customer_upper_face',(3769,1653,2071.5),(5218,2047,2073),'steel','TIG upper cabinet')
    for lo,hi in [((4259,1687.5,2030),(4301,1712.5,2090)),((4140,1676.75,2030),(4222.5,1759.25,2090))]:panel['sh']=panel['sh'].cut(box(lo,hi))
    add('QR62_scanner_backplate',(4240,1653,2035),(4320,1730,2038))
    add('QR62_reader_backplate',(4130,1655,2055.6),(4233,1769,2058.6))
    # Lower controller reserve and original fan envelopes. QR has NO heating.
    for section,xx,yy in [('lower',5010,290),('upper',5000,1885)]:
        add('QR62_'+section+'_fan_support',(xx,yy,1751.5),(xx+150,yy+150,1754.5),'steel','TIG cabinet wall')
        add('QR62_'+section+'_fan',(xx,yy,1754.5),(xx+150,yy+150,1794.5),'black','original150x150x40 fan envelope; airflow/fasteners pending')
    OPEN.extend(['customer hinge/handle catalogue finalisation and door stop details',
      'upper/lower service cover fasteners and ventilation openings not yet production detailed',
      'fan airflow and installation details pending'])
def gate():
    # Gate on right corridor edge. Enclosure safety distance requires actual stopping-time measurement.
    x=5600; za,zb=700,1700
    for z in [za-40,zb]:
        add(f'CELL62_post_{z}',(x,6,z),(x+40,2050,z+40))
        add(f'CELL62_foot_{z}',(x-30,0,z-30),(x+70,6,z+70),'steel','floor anchors pending')
    for y in [40,2000]: add(f'CELL62_gate_bar_{y}',(x, y,za+3),(x+30,y+30,zb-3),'steel','gate TIG')
    for z in [za+3,zb-33]:add(f'CELL62_gate_side_{z}',(x,70,z),(x+30,2000,z+30),'steel','gate TIG')
    add('CELL62_gate_screen',(x+12,70,za+33),(x+15,2000,zb-33),'clear','guard panel; bolting pending')
    # Cell gate also uses monitored lock. Emergency escape lever will be required on inside.
    # Local mounting along gate plane is rotated after building so device axis is correct.
    start=len(P); lock('CELL62',0,1000,0)
    for p in P[start:]:p['sh']=p['sh'].rotate((0,0,0),(0,1,0),-90).translate((x-3,0,zb))
    for p in P[:start]:
        if p['ad'] in ['CELL62_post_1700','CELL62_gate_side_1667']:
            centres=[(1010,1720),(1110,1720)] if 'post' in p['ad'] else [(1087.25,1673),(1111.75,1673)]
            for yy,zz in centres:p['sh']=p['sh'].cut(cq.Solid.makeCylinder(4.5,80,cq.Vector(x-30,yy,zz),cq.Vector(1,0,0)))
    for y in [200,1820]:
        fixed=box((x+40,y,685),(x+43,y+10,701.5)).fuse(box((x+40,y+20,685),(x+43,y+30,701.5)))
        for ya in [y,y+20]:
            shell=cq.Solid.makeCylinder(3,10,cq.Vector(x+43,ya,701.5),cq.Vector(0,1,0))
            fixed=fixed.fuse(shell)
        moving=box((x+30,y+10.2,703),(x+43,y+19.8,718)).fuse(cq.Solid.makeCylinder(3,9.6,cq.Vector(x+43,y+10.2,701.5),cq.Vector(0,1,0)))
        hole=cq.Solid.makeCylinder(1.6,32,cq.Vector(x+43,y-1,701.5),cq.Vector(0,1,0))
        add(f'CELL62_hinge_fixed_{y}',(x+40,y,685),(x+46,y+30,705));P[-1]['sh']=fixed.cut(hole)
        add(f'CELL62_hinge_moving_{y}',(x+30,y+10.2,700),(x+46,y+19.8,718),'steel','TIG gate');P[-1]['sh']=moving.cut(hole)
        add(f'CELL62_hinge_pin_{y}',(x+41.5,y-2,700),(x+44.5,y+32,703),'steel','retained hinge pin')
        P[-1]['sh']=cq.Solid.makeCylinder(1.5,30,cq.Vector(x+43,y,701.5),cq.Vector(0,1,0)).fuse(cq.Solid.makeCylinder(2.5,2,cq.Vector(x+43,y-2,701.5),cq.Vector(0,1,0))).fuse(cq.Solid.makeCylinder(2.5,2,cq.Vector(x+43,y+30,701.5),cq.Vector(0,1,0)))
    OPEN.extend(['cell gate escape-release lever, hinges, floor anchors and complete fixed guarding pending',
      'safety circuit / PL verification / stopping time / safety-rated bay clearance measurement pending',
      'production robot identity: this layout retains approved UR10e; FR5 reference in standard document needs reconciliation'])
def migrate(h):
    # Preserve exact top electronic assemblies: only rigid translations, no rescaling.
    moves={'ELK_QR_KUTU':(-620,0,1175),'QR_UPS':(-465,0,1175),
           'QR_KILIT_KARTI':(-305,0,940),'QR_MUSTERI_PANELI':(-200,0,900),
           'QR_ROBOT_KONTROL':(-600,0,1100)}
    for n in h.J['nodes']:
        name=n.get('name','')
        for pre,d in moves.items():
            if name.startswith(pre+'__'):
                if pre=='QR_MUSTERI_PANELI' and '__plastik' in name:d=(-600,0,900)
                if pre=='QR_MUSTERI_PANELI' and '__paslanmaz' in name:d=(-811.75,0,900)
                n['translation']=(np.array(n.get('translation',[0,0,0]))+np.array(d)/1000).tolist()
                MIG.append(dict(node=name,delta_mm=d,scaled=False))
    remove=set()
    for i,n in enumerate(h.J['nodes']):
        name=n.get('name','')
        if name.startswith(('QR_','ELK_QR')) and not any(name.startswith(p+'__') for p in moves): remove.add(i)
    for s in h.J['scenes']:s['nodes']=[i for i in s['nodes'] if i not in remove]
    for a in h.J.get('animations',[]):
        a['channels']=[c for c in a['channels'] if c['target']['node'] not in remove and not h.J['nodes'][c['target']['node']].get('name','').startswith(('QR_','ELK_QR'))]
    return remove
def main():
    gi,go=map(Path,sys.argv[1:3]); raw=gi.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'must use exact Claude step61'
    h=Ham(str(gi)); original_nodes=copy.deepcopy(h.J['nodes']); oldbin=bytes(h.BIN)
    removed=migrate(h); qr();gate()
    templates={'steel':'U_F_GOVDE__paslanmaz','black':'K_GOVDE__siyah',
      'yellow':'ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO','clear':'QR_GOZLER__on_seffaf__GOZ_00_KAPI'}
    # Each part gets own mesh/node so audit/selection is unambiguous.
    for p in P:
        control=any(k in p['ad'] for k in ['AZM40','M12','lock_cable','duct','fan'])
        h.koy(p['ad'],[p],kat=6 if control else 0,mek=47 if control else 43,sablon=templates[p['kind']])
        h.J['nodes'][-1]['extras']={'connection':p['join'],'scope':'robot_qr_step62','physicalSafetyCertified':False}
    unchanged=[i for i,n in enumerate(original_nodes) if not n.get('name','').startswith(('QR_','ELK_QR'))]
    assert all(h.J['nodes'][i]==original_nodes[i] for i in unchanged),'machine node changed'
    assert bytes(h.BIN[:len(oldbin)])==oldbin,'source geometry binary changed'
    h.J['asset']['generator']='AUTOKITCH step62 QR3x4 safety layout (manufacturing details open)'
    h.J['scenes'][h.J.get('scene',0)].setdefault('extras',{})['robotQRStep62']={'cabinet':[3,4],'heating':False,'source':SOURCE_SHA,'production_ready':False}
    h.yaz(str(go))
    report={'source_sha256':SOURCE_SHA,'source_machine_nodes_unchanged':len(unchanged),'source_binary_preserved':True,
      'bay_count':12,'grid':[3,4],'heating':False,'floors_mm':[588,850,1112,1374],'opening_mm':250,
      'robot_face_z_mm':1750,'customer_face_z_mm':2074,'top_mm':2050,
      'migrated':MIG,'removed_old_nodes':len(removed),'parts':[], 'open':OPEN,'production_ready':False}
    for p in P:
        b=p['sh'].BoundingBox();report['parts'].append({'name':p['ad'],'kind':p['kind'],'join':p['join'],'holes':p['holes'],
          'bounds_mm':[[b.xmin,b.ymin,b.zmin],[b.xmax,b.ymax,b.zmax]]})
    go.with_suffix('.layout.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('BUILD',len(P),'parts;',len(MIG),'migrated nodes; manufacturing/safety open=',len(OPEN),flush=True)
if __name__=='__main__':
    main()
    # Same OCC/Windows shutdown workaround used by the other chain steps.
    import os
    sys.stdout.flush();os._exit(0)
