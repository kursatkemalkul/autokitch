import io
f = 't3_montaj_v4.py'
s = io.open(f, encoding='utf-8').read()
i = s.index('# ---- 7 KURU BÖLME'); j = s.index('# ---- 12 SOĞUTMA')
s = s[:i] + io.open('v4_bolum.py', encoding='utf-8').read() + s[j:]
L = s.split('\n')
for k, l in enumerate(L):
    if l.startswith("adim('Arka servis sacı kapanır'"):
        L[k] = ("adim('Arka servis sacı kapanır', 'Servis sacı alt montajıyla birlikte arkadan gelir; 17 havşa başlı vida M5 × 12 çökertilmiş (dimple) deliklerden yan, tavan ve taban "
                "dönüşlerinin iç yüzündeki kaynak burçlarına. Dış yüz düz. Bakımda sac tek parça çıkar; evaporatörler tabana bağlı kalır.',")
        L[k + 1] = "     'servis sacı alt montajı · havşa vida M5 × 12 × 17 → kaynak burcu')"
    if "olay(t - 1.0, 'DIN 7991 M5 × 6 × 17" in l:
        L[k] = l.replace("'DIN 7991 M5 × 6 × 17 → dönüşlerdeki PEM SP-M5'", "'Havşa vida M5 × 12 × 17 → dönüşlerdeki kaynak burçları (baş dış yüzle aynı düzlemde)'")
    if l.startswith("t = koy('x_ekseni', AD((-1700"):
        L[k] = "t = koy('x_ekseni', AD((-1700, 0, 0), ON9, lift=(5, 10)), 'X ekseni (raylar + araba + tabla) → A tarafındaki tabla geçiş ağzından kayar, sağ uçta motora bağlanır')"
    if l.startswith("adim('X ekseni + kapaklar'"):
        L[k] = ("adim('X ekseni + kapaklar', 'X ekseni parçalı gelir: motoru kuru bölme adımında sağ arka köşeye konmuştu; raylar + araba + bantlı tabla A tarafındaki tabla geçiş ağzından kayarak girer "
                "ve motora bağlanır. Sensör braketleri alttan. Ön alt braket, orta kayıt, gizli menteşe gövdeleri ve bas-aç mandalları ön kasaya; kanatlar 90° açık, menteşe tarafından yaklaşır, pimlere iner ve kapanır.',")
    if "olay(t, 'Raf askı burcu POM" in l and 'astar' in l: pass
s = '\n'.join(L)
io.open(f, 'w', encoding='utf-8').write(s)
print('ok')
