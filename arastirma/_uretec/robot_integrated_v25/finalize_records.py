"""Record passed step94 without rewriting unrelated coordination/chain bytes."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[3]
A=R/'otonom/hat3d/robot-integrated-v25'
proof=json.loads((A/'repeat_build.json').read_text())
assert proof['step']==94 and proof['byte_identical'] and len(proof['runs'])==2
for name in ['layout_scan','routing_audit','integration_audit','geometry_audit','qr_column_audit']:
    assert json.loads((A/(name+'.json')).read_text())['passed'],name
sha=proof['runs'][0]['hat3_robot_v25.glb.gz']['sha256'][:12]
chain=R/'arastirma/_uretec/h3/yama_v9/zincir.py'
data=chain.read_bytes();old=b'SON = "hat3_v10p_robot.glb"'
step=('ADIMLAR.append(("94", "QR solda ayni derinlik tek govde; kutu koridor icinden doner; olculen duvar/pano/zemin", ["hat3_v10l.glb"], "hat3_v10q_robot.glb",\n'
      '    [(".", \'python "{YAMA}/94_qr_donus.py" hat3_v10l.glb hat3_v10q_robot.glb\')]))\n'
      'SON = "hat3_v10q_robot.glb"').encode()
assert data.count(old)==1
chain.write_bytes(data.replace(old,step))
sira=R/'arastirma/_uretec/h3/yama_v9/SIRA.md'
row=f'\r\n| 94 | `94_qr_donus.py` | v10l → v10q_robot; web v25 | QR okuyucu/tus takimi solda160mm tek sutun, dolapla ayni333mm derinlik. Kutu once koridora cekilir, rayda sola tasinir ve duvarin ters tarafindan yatay doner; alma/birakma ayni. Duvar X5360, zemin dis kenari5640;250mm pano200mm gomulu. | Iki tam kosu native/meshopt/gzip bayt ayni; gzip{sha}; 12,506karede duvar56.09mm/pano72.07mm pay; yapilandirilan hiz/ivme sinirlari gecer.23yeni kablo/kanal katisi kapali;9hat>=2mm, USB>=14.24mm. Tum robot carpismasi/fizik, bina pano gomusu ve elektrik/emniyet onayi acik. |\r\n'
assert b'| 94 |' not in sira.read_bytes()
with sira.open('ab') as stream:stream.write(row.encode())
p=R/'KOORDINASYON.md';raw=p.read_bytes();lines=raw.splitlines(keepends=True)
for i,line in enumerate(lines):
    text=line.decode();ending='\r\n' if line.endswith(b'\r\n') else '\n'
    if text.startswith('| Robot + ray + QR dolabı + sipariş animasyonları |'):
        lines[i]=('| Robot + ray + QR dolabı + sipariş animasyonları | Codex | `coord/codex-qr-donus-v25` | v25/adım94: QR sütunu diğer uçta, dolapla aynı333mm derinlik;12göz korunur. Kutu koridorda sola dönerek aynı QR yerine bırakılır. Duvar48cm yaklaşır (X5360), kayıtlı kol/ürün56mm,pano72mm pay; pano200mm gömülü. İki tam koşu bayt aynı;23kapalı kablo/kanal katısı,9hat>=2mm. Hız/ivme kontrolü geçer. Tam robot/fizik, bina gömüsü ve elektrik/emniyet onayı açık. |'+ending).encode()
    elif text.startswith("- Codex'in alanı:"):
        lines[i]=(text.replace('_v24/','_v25/').replace('-v24/','-v25/').replace('zincir93','zincir94').rstrip('\r\n')+ending).encode()
    elif text.startswith('Robot entegrasyon adımı93,'):
        lines[i]=(text.replace('adımı93','adımı94').replace('adım90–92','adım90–93').replace('birleştirilince 93','birleştirilince 94').replace('sitedeki v24','sitedeki v25').rstrip('\r\n')+ending).encode()
    elif text.startswith('ZİNCİR KİLİDİ:'):
        assert 'CODEX · adım94' in text
        lines[i]=('ZİNCİR KİLİDİ: BOŞ'+ending).encode()
p.write_bytes(b''.join(lines))
print('Recorded terminal94 and released own coordination chain lock')
