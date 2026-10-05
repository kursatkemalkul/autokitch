import io
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3\yap_hat3_montaj_v3.py"
H2 = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat2-v4\arastirma\_uretec\h2\yap_hat2_montaj_v4.py"
for P, a, b in ((H3, "X EKSENİ MOTORU + 2 AÇICI MOTORU BAĞLANDI (A arka duvarı → G9 çok delikli rakor → TOPPING panosu · açıcıda esnek PUR + servis halkası) · cihaz envanteri: 43 cihazın tamamı kablolu",
                 "X EKSENİ MOTORU BAĞLANDI (A arka duvarı → G9 rakoru → TOPPING panosu) · AÇICI HAZIR ALINIR: yalnız görsel, motor kablosu yok · cihaz envanteri: tüm cihazlar kablolu"),
                (H3, "kablosuz kalan X ekseni motoru + 2 açıcı motoru bağlandı (A arka duvarı boyunca → G9 çok delikli rakor → TOPPING panosu)",
                 "kablosuz kalan X ekseni motoru bağlandı (A arka duvarı boyunca → G9 rakoru → TOPPING panosu) · açıcı hazır alınır, yalnız görsel"),
                (H2, "X ekseni + açıcı motorları dahil)", "X ekseni motoru dahil · AÇICI HAZIR ALINIR: yalnız görsel, kablosu yok)")):
    s = io.open(P, encoding="utf-8").read(); assert s.count(a) == 1, (P[-25:], a[:50]); io.open(P, "w", encoding="utf-8").write(s.replace(a, b))
print("ok")
