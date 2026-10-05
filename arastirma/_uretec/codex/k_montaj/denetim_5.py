from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'_local/codex_k_montaj'
plan=json.loads((O/'montaj_plani.json').read_text(encoding='utf8'));step=json.loads((O/'step70_audit.json').read_text(encoding='utf8'))
checks=[{'rule':'İki adım70 koşusu bayt aynı','status':'PASS' if step['two_runs_byte_identical'] else 'FAIL'}, {'rule':'32 saplama çıkıntısı','status':'PASS' if step['fastener_audit']['passed'] else 'FAIL'}, {'rule':'Hedef saplamalar dışındaki geometri korunur','status':'PASS' if not step['changed_nodes_outside_32_target_studs'] else 'FAIL'}]
evidence={}
for number in (71,72,73):
 p=O/f'step{number}_audit.json'
 if p.exists():
  r=json.loads(p.read_text(encoding='utf8'));evidence[f'step{number}']=r
  checks.append({'rule':f'Yerel {number}: iki koşu, K kapsamı ve alt montaj denetimi','status':'PASS' if r['passed'] else 'FAIL','scope':'Alt montaj; tam §5 değildir'})
for name in ('support_motion_audit','source_bending_audit','k71_context_audit','k72_context_audit','k73_context_audit'):
 p=O/f'{name}.json'
 if p.exists():evidence[name]=json.loads(p.read_text(encoding='utf8'))
for rule in ['Bütün K parçalarında açınım/son geometri eşleşmesi','Bütün kurulum yolları 2mm örneklem ve sıfır çakışma','Bütün montajın son animasyon konumu ±0,01mm','Her taşıyıcı hemen bağlı veya uyarılı geçici dayalı','Geçici dayalı parçaya yük binmemesi','Bütün cihazlarda vida/delik/karşı diş ve erişim','Bütün güncel saclarda imal edilebilirlik','Son birleşmiş modelden animasyon ve yayın']:
 checks.append({'rule':rule,'status':'NOT_VERIFIED'})
r={'source_step':61,'step70_ready_for_later_integration':step['passed'],'assembly_completed':False,'checks':checks,'partial_evidence':evidence,'publish_allowed':all(x['status']=='PASS' for x in checks)}
(O/'denetim_5.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False));sys.exit(0 if r['publish_allowed'] else 2)
