from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
p=ROOT/'otonom/hat/makine.html';s=p.read_text(encoding='utf8')
if 'robot-integrated-v18/panel.js' in s:
 print('Main page already integrated');raise SystemExit(0)
s=s.replace('  animasyon(D.animasyon, D.siparis);','  // Robot v18 module owns the single playback clock and recipe selector.')
start=s.index('function animasyon(A, SIP) {');end=s.index('\n</script>',start)
s=s[:start]+s[end:]
start=s.index('<script>\n(async()=>{');s=s[:start]+"<script type=\"module\" src=\"robot-integrated-v18/panel.js?v=18\"></script></body></html>\n"
s=s.replace('animation-name="siparis_kasarli"','animation-name="siparis_birlesik_kasarli"')
s=s.replace('Adım 62 robot ve ısıtıcısız 3x4 QR yerleşim incelemesi','Adım 62 makine ve QR, ray üzerinde UR10e sipariş hareketleri')
css='''<style>.robot-panel{padding:8px 16px;color:#dce3ea;font:13px/1.45 system-ui}.robot-panel label{display:block;margin:9px 0}.robot-panel select,.robot-panel input{display:block;width:100%;padding:7px;background:#232932;color:#e6ebf0;border:1px solid #526174;border-radius:6px}.robot-panel button{padding:7px 9px;margin:4px 3px 4px 0;background:#263648;color:#fff;border:1px solid #526174;border-radius:6px}.robot-panel button:disabled{opacity:.45}.robot-panel p{margin:8px 0}#robot-load{color:#7dd3fc}.sip button{border-radius:6px}</style>'''
s=s.replace('</head>',css+'</head>')
p.write_text(s,encoding='utf8')
print('Main page now loads v18, one clock, eight robot clips and full panel')
