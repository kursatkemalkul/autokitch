#!/bin/bash
# TOPPING paketi zinciri: taban GLB -> hat3_v8zf.glb (tp5 kanal: yapilmadi, rapora bakiniz)
set -e
cd "$(dirname "$0")"
TABAN=${1:-../hat3_v8ze.glb}; CIKIS=${2:-../hat3_v8zf.glb}
python tp1_duvar.py "$TABAN" tp1.glb
python tp2_evap.py tp1.glb tp2.glb
python tp3_pnomatik.py tp2.glb tp3.glb
python tp4_motor.py tp3.glb tp4.glb
# tp6_anim.py ZINCIRDEN CIKARILDI (Kemal: siparis animasyonu istenmiyor; animasyonlara dokunulmaz)
python ../tg/glb_sikistir.py tp4.glb "$CIKIS"
python ../paket/p_dogrula.py "$CIKIS" | head -1
