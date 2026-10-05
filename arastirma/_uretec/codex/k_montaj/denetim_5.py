from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'_local/codex_k_montaj'
plan=json.loads((O/'montaj_plani.json').read_text(encoding='utf8'));step=json.loads((O/'step70_audit.json').read_text(encoding='utf8'))
checks=[{'rule':'İki adım70 koşusu bayt aynı','status':'PASS' if step['two_runs_byte_identical'] else 'FAIL'}, {'rule':'32 saplama çıkıntısı','status':'PASS' if step['fastener_audit']['passed'] else 'FAIL'}, {'rule':'Hedef saplamalar dışındaki geometri korunur','status':'PASS' if not step['changed_nodes_outside_32_target_studs'] else 'FAIL'}]
for rule in ['Güncel kaynakla açınım/son geometri eşleşmesi','Kurulum yolları 2mm örneklem ve sıfır çakışma','Son animasyon konumu ±0,01mm','Her taşıyıcı hemen bağlı veya uyarılı geçici dayalı','Geçici dayalı parçaya yük binmemesi','Bütün cihazlarda vida/delik/karşı diş ve erişim','Güncel saclarda imal edilebilirlik','İstasyon kapsam kilidi ve son birleşmiş model']:
 checks.append({'rule':rule,'status':'NOT_VERIFIED'})
r={'source_step':61,'step70_ready_for_later_integration':step['passed'],'assembly_completed':False,'checks':checks,'publish_allowed':all(x['status']=='PASS' for x in checks)}
(O/'denetim_5.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False));sys.exit(0 if r['publish_allowed'] else 2)
