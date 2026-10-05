#!/bin/bash
# QR + TEZGAH + KABLO PAKETI · sirali zincir. Kullanim: bash calistir.sh TABAN.glb CIKTI.glb
# (TOPPING ciktisinin ustune yeniden uygulanabilir: tum adimlar DUGUM ADI + bilesen kutusu ile calisir, TOPPING dugumlerine dokunmaz)
# NOT: q4 cadquery kullanir; cikista Python bazen 127/139 doner (dosya yazildiktan sonra) -> cikis kodu yerine dosya varligi denetlenir.
set -u
D="$(cd "$(dirname "$0")" && pwd)"; cd "$D"
T="$1"; O="$2"
adim(){ rm -f "$3"; python "$1" "$2" "$3" 2>&1 | grep -v -i warn; [ -f "$3" ] || { echo "HATA: $1 cikti yok"; exit 1; }; }
adim q1_urun.py      "$T"     q1.glb
adim q2_harting.py   q1.glb   q2.glb
adim q3_qr.py        q2.glb   q3.glb
adim q4_k_kablo.py   q3.glb   q4.glb
adim q5_b_reed.py    q4.glb   q5.glb
adim q6_tezgah.py    q5.glb   q6.glb
python ../tg/glb_sikistir.py q6.glb "$O"
