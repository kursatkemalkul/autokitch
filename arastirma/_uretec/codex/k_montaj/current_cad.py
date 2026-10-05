"""Reconstruct only explicitly measured native parameter changes; no model edits."""
import json
def factory_from_source(K, out):
    components=json.loads((out/'source_components.json').read_text(encoding='utf8'))['components']
    doors=[r for r in components if r['node']=='K_GOVDE__on_seffaf' and r['hi'][1]-r['lo'][1]>1400 and r['hi'][0]-r['lo'][0]>390]
    exterior=max(doors,key=lambda r:r['hi'][2])
    K.KAPAK_X=(exterior['lo'][0]-4000, exterior['hi'][0]-4000)
    assert abs(K.KAPAK_X[0]-3)<.01 and abs(K.KAPAK_X[1]-399)<.01, K.KAPAK_X
    # GLB float32 coordinate quantization is not a new manufacturing dimension.
    K.KAPAK_X=(3.,399.)
    g=K.kur()
    # Source step36 drilled the two U_KE mounting PEM holes in K's roof.
    # Nominal pilot reconstruction only. Source step36 has a stepped pressed
    # seat; the surface-screen report correctly excludes this roof. Step73
    # has its own roof definition; do not use this pilot as source equivalence.
    roof=next(s for s in g.SAC if s.ad=='ust_sac')
    for x in (100.,300.):
        _,c,_=K.S.pem_somun('SP','M8',(x,1860.5,-700.),(0,-1,0),1.5)
        roof.paneller[0].delik(x,700.,c['delik'],tip='pem_somun',pem_tip='SP',kenar_min=c['kenar'],min_sac=1.5)
    return g
