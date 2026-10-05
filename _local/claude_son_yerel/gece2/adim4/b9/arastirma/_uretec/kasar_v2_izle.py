"""Replay the actual cheese PhysX recording in the same detailed machine."""
from pathlib import Path
src=Path(__file__).with_name('sucuk_v2_izle.py').read_text(encoding='utf-8')
# First evaluate the previous viewer's asserted construction without launching it.
ns={'__file__':str(Path(__file__).with_name('sucuk_v2_izle.py'))}
exec(src[:src.rfind('exec(compile')],ns)
src=ns['src']
def rep(a,b):
    global src
    assert src.count(a)==1,(a,src.count(a));src=src.replace(a,b)
rep("default='full_candidate_balanced_03'","default='candidate_04'")
rep("ROOT/'arastirma/3_TOPPING/sucuk_v2/runs'","ROOT/'arastirma/3_TOPPING/kasar_v2/runs'")
rep("'SUCUK V2 - AYRI DENEY'","'KASAR V2 - CAD v15 DENEY'")
rep('height=485)','height=640)')
rep("'6-10 mm / sonumlu temas / gida verileri VARSAYIM'","'Kisa rende cubuklari / gida verileri VARSAYIM'")
rep("'Stok %.1f g | hedef 70 g'","'Stok %.1f g | hedef 55 g'")
rep("'Hesap: sucuk_v2_deney.py\\nYeni vida ucu / SDF temas. Ezilme testi degildir.'", "'Hesap: kasar_v2_deney.py\\nKismi stok / SDF temas. Ezilme ve yapisma testi degil.'")
src=src.replace('KUP_SUCUK','KASAR_KABI').replace('/SUCUK_CUBES/','/KASAR_SHREDS/')
src=src.replace('/V2_candidate_tube','/KASAR_V2_candidate_tube')
src=src.replace('[1.93,-.65,.67]','[1.80,-.52,.71]').replace('[1.46,.26,.31]','[1.25,.27,.35]')
rep('last=time.monotonic()',"print('KASAR_REPLAY_READY',args.tag,len(paths),'bodies',flush=True)\nlast=time.monotonic()")
exec(compile(src,__file__,'exec'),globals())
