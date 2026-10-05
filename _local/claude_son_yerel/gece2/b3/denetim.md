# B MONTAJ v3 — DENETİM (4 Eki 2026)

Sayfa: http://127.0.0.1:8766/claude-hat3-v8/otonom/hat/b-montaj.html · süre 196 s · 21 adım · 705 öğe · model hat3_v9l (zincir 00–44, değiştirilmedi)

## SONUÇ: YOL TEMİZ, MODEL AÇIKLARI VAR (Kemal kararı — yayına hazır değil)

| ölçüt | değer |
|---|---|
| yol çakışması (2 mm, üçgen CCD, 4815 çift) | **0** (aşağıdaki beyanlı istisnalar hariç) |
| büküm kareleri | 0 sorun |
| yerinde belirme | 0 (istisna: kayış, kablolar, gider hortumu, kovandan geçen arka kanal, kaynak dikişi, silikon) |
| havada | 10: g_dis_arka_ek_lamasi, g_isi_kalkani_isinim_08, ic_kanal_57, istasyon_kutusu, sase_boy_arka, sase_boy_on, tasiyici_dikme_3386_600, tasiyici_plaka_-484, tasiyici_plaka_-574, zincir_kanal |
| son kare ↔ model (tarayıcı, bbox) | 705 öğe, en büyük fark 0,0005 mm |
| bükümlü sac (açınımdan kurulan ağ) ↔ model kutusu | en büyük 0.0201 mm (ent kutusu 0,01 yuvarlamalı) |
| son konumda kesişim | evap_kablo ↔ ic_kanal_31 (32 üçgen, modelde önceden var) · kayış ↔ kasnak (model teması) |
| tarayıcı taraması (0,25 s, 785 kare) | konsol hatası 0 |

## BEYANLI İSTİSNALAR

- g_bolme_1_kovan_0 ↔ g_bolme_1_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_1_kovan_1 ↔ g_bolme_1_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_1_kovan_2 ↔ g_bolme_1_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_1_pu ↔ kapak_bolme_1_sac_a — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_1_pu ↔ kapak_bolme_1_sac_b — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_2_kovan_0 ↔ g_bolme_2_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_2_kovan_1 ↔ g_bolme_2_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_2_pu ↔ kapak_bolme_2_sac_a — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_2_pu ↔ kapak_bolme_2_sac_b — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_3_kovan_0 ↔ g_bolme_3_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_3_pu ↔ kapak_bolme_3_sac_a — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_3_pu ↔ kapak_bolme_3_sac_b — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_4_kovan_0 ↔ g_bolme_4_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_4_kovan_1 ↔ g_bolme_4_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_4_kovan_2 ↔ g_bolme_4_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_4_pu ↔ kapak_bolme_4_sac_a — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_4_pu ↔ kapak_bolme_4_sac_b — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_5_kovan_0 ↔ g_bolme_5_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_5_kovan_0_ust_L ↔ g_bolme_5_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_5_kovan_1 ↔ g_bolme_5_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_5_kovan_1_ust_L ↔ g_bolme_5_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_5_kovan_2 ↔ g_bolme_5_pu — kovan PU levhadaki yuvasından sıfır boşlukla geçer (model teması; levha yuvası +0,5 mm kesilir)
- g_bolme_5_pu ↔ kapak_bolme_5_sac_a — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_bolme_5_pu ↔ kapak_bolme_5_sac_b — köpük kapağı PU levhadaki cebine oturur (son 1 mm, model teması)
- g_kosebent_sag_ust_2 ↔ g_tk_depo_arka_pu — MODEL AÇIĞI: PU levha köşebendin büküm dış köşesini ve ön ucunu sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz
- g_kosebent_sag_ust_2 ↔ g_tk_depo_sag_pu — MODEL AÇIĞI: PU levha köşebendin büküm dış köşesini ve ön ucunu sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz
- g_kosebent_sol_ust_1 ↔ g_pu_sol — MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz
- g_kosebent_sol_ust_2 ↔ g_pu_sol — MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz
- g_kosebent_sol_ust_3 ↔ g_pu_sol — MODEL AÇIĞI: PU sol levha köşebendin büküm dış köşesini sarıyor (köpük modeli) — kesilmiş levha olarak takılamaz
- g_dis_arka_2 ↔ g_pu_arka_alcak — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_arka_1 ↔ g_pu_arka_yuksek — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_arka_2 ↔ g_pu_arka_yuksek — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_arka_ek_lamasi ↔ g_pu_arka_yuksek — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_arka_1 ↔ g_pu_sol — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_sol_yan ↔ g_pu_sol — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_kosebent_sol_alt_1 ↔ g_pu_sol — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_kosebent_sol_alt_2 ↔ g_pu_sol — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_kosebent_sol_alt_3 ↔ g_pu_sol — MODEL AÇIĞI: PU (köpük modelinden kesilmiş levha) sac flanşının / köşebendin altına sarıyor — levha olarak takılamaz, levha bölümü yeniden kesilmeli
- g_dis_taban_1 ↔ percin_sase — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- g_dis_taban_2 ↔ percin_sase — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- percin_sase ↔ sase_boy_arka — perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)
- percin_sase ↔ sase_boy_on — perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)
- g_dis_tavan_1 ↔ percin_ust — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- g_dis_tavan_2 ↔ percin_ust — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- gfrp_ust_arka ↔ percin_ust — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- gfrp_ust_on ↔ percin_ust — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- moduler_cerceve_arka ↔ percin_ust — perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)
- moduler_cerceve_on ↔ percin_ust — perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)
- percin_ust ↔ tasiyici_plaka_-484 — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- percin_ust ↔ tasiyici_plaka_-574 — perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)
- percin_ust ↔ tasiyici_ust — perçin somun deliğe düz gövdeyle girer, sıkılınca alt kısmı şişer (model sıkılmış hâli gösterir)
- CEK_K1_lahm_1_kasnak ↔ CEK_K1_lahm_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K1_lahm_1_avara ↔ CEK_K1_lahm_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K1_lahm_1_cene_alt ↔ CEK_K1_lahm_1_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_1_cene_ust ↔ CEK_K1_lahm_1_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_1_cene_vida ↔ CEK_K1_lahm_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K1_lahm_2_kasnak ↔ CEK_K1_lahm_2_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K1_lahm_2_avara ↔ CEK_K1_lahm_2_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K1_lahm_2_cene_alt ↔ CEK_K1_lahm_2_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_2_cene_ust ↔ CEK_K1_lahm_2_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_2_cene_vida ↔ CEK_K1_lahm_2_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K1_lahm_3_kasnak ↔ CEK_K1_lahm_3_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K1_lahm_3_avara ↔ CEK_K1_lahm_3_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K1_lahm_3_cene_alt ↔ CEK_K1_lahm_3_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_3_cene_ust ↔ CEK_K1_lahm_3_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_3_cene_vida ↔ CEK_K1_lahm_3_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K1_lahm_4_kasnak ↔ CEK_K1_lahm_4_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K1_lahm_4_avara ↔ CEK_K1_lahm_4_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K1_lahm_4_cene_alt ↔ CEK_K1_lahm_4_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_4_cene_ust ↔ CEK_K1_lahm_4_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_4_cene_vida ↔ CEK_K1_lahm_4_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K1_lahm_5_kasnak ↔ CEK_K1_lahm_5_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K1_lahm_5_avara ↔ CEK_K1_lahm_5_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K1_lahm_5_cene_alt ↔ CEK_K1_lahm_5_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_5_cene_ust ↔ CEK_K1_lahm_5_kayis — kayış çene arasında sıkışır
- CEK_K1_lahm_5_cene_vida ↔ CEK_K1_lahm_5_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K2_lahm_1_kasnak ↔ CEK_K2_lahm_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K2_lahm_1_avara ↔ CEK_K2_lahm_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K2_lahm_1_cene_alt ↔ CEK_K2_lahm_1_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_1_cene_ust ↔ CEK_K2_lahm_1_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_1_cene_vida ↔ CEK_K2_lahm_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K2_lahm_2_kasnak ↔ CEK_K2_lahm_2_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K2_lahm_2_avara ↔ CEK_K2_lahm_2_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K2_lahm_2_cene_alt ↔ CEK_K2_lahm_2_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_2_cene_ust ↔ CEK_K2_lahm_2_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_2_cene_vida ↔ CEK_K2_lahm_2_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K2_lahm_3_kasnak ↔ CEK_K2_lahm_3_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K2_lahm_3_avara ↔ CEK_K2_lahm_3_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K2_lahm_3_cene_alt ↔ CEK_K2_lahm_3_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_3_cene_ust ↔ CEK_K2_lahm_3_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_3_cene_vida ↔ CEK_K2_lahm_3_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K2_lahm_4_kasnak ↔ CEK_K2_lahm_4_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K2_lahm_4_avara ↔ CEK_K2_lahm_4_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K2_lahm_4_cene_alt ↔ CEK_K2_lahm_4_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_4_cene_ust ↔ CEK_K2_lahm_4_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_4_cene_vida ↔ CEK_K2_lahm_4_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K2_lahm_5_kasnak ↔ CEK_K2_lahm_5_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K2_lahm_5_avara ↔ CEK_K2_lahm_5_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K2_lahm_5_cene_alt ↔ CEK_K2_lahm_5_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_5_cene_ust ↔ CEK_K2_lahm_5_kayis — kayış çene arasında sıkışır
- CEK_K2_lahm_5_cene_vida ↔ CEK_K2_lahm_5_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K3_hamur_1_kasnak ↔ CEK_K3_hamur_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K3_hamur_1_avara ↔ CEK_K3_hamur_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K3_hamur_1_cene_alt ↔ CEK_K3_hamur_1_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_1_cene_ust ↔ CEK_K3_hamur_1_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_1_cene_vida ↔ CEK_K3_hamur_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K3_hamur_2_kasnak ↔ CEK_K3_hamur_2_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K3_hamur_2_avara ↔ CEK_K3_hamur_2_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K3_hamur_2_cene_alt ↔ CEK_K3_hamur_2_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_2_cene_ust ↔ CEK_K3_hamur_2_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_2_cene_vida ↔ CEK_K3_hamur_2_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K3_hamur_3_kasnak ↔ CEK_K3_hamur_3_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K3_hamur_3_avara ↔ CEK_K3_hamur_3_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K3_hamur_3_cene_alt ↔ CEK_K3_hamur_3_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_3_cene_ust ↔ CEK_K3_hamur_3_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_3_cene_vida ↔ CEK_K3_hamur_3_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K3_hamur_4_kasnak ↔ CEK_K3_hamur_4_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K3_hamur_4_avara ↔ CEK_K3_hamur_4_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K3_hamur_4_cene_alt ↔ CEK_K3_hamur_4_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_4_cene_ust ↔ CEK_K3_hamur_4_kayis — kayış çene arasında sıkışır
- CEK_K3_hamur_4_cene_vida ↔ CEK_K3_hamur_4_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K5_hamur_1_kasnak ↔ CEK_K5_hamur_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K5_hamur_1_avara ↔ CEK_K5_hamur_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K5_hamur_1_cene_alt ↔ CEK_K5_hamur_1_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_1_cene_ust ↔ CEK_K5_hamur_1_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_1_cene_vida ↔ CEK_K5_hamur_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K5_hamur_2_kasnak ↔ CEK_K5_hamur_2_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K5_hamur_2_avara ↔ CEK_K5_hamur_2_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K5_hamur_2_cene_alt ↔ CEK_K5_hamur_2_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_2_cene_ust ↔ CEK_K5_hamur_2_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_2_cene_vida ↔ CEK_K5_hamur_2_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K5_hamur_3_kasnak ↔ CEK_K5_hamur_3_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K5_hamur_3_avara ↔ CEK_K5_hamur_3_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K5_hamur_3_cene_alt ↔ CEK_K5_hamur_3_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_3_cene_ust ↔ CEK_K5_hamur_3_kayis — kayış çene arasında sıkışır
- CEK_K5_hamur_3_cene_vida ↔ CEK_K5_hamur_3_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K5_ic1_1_kasnak ↔ CEK_K5_ic1_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K5_ic1_1_avara ↔ CEK_K5_ic1_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K5_ic1_1_cene_alt ↔ CEK_K5_ic1_1_kayis — kayış çene arasında sıkışır
- CEK_K5_ic1_1_cene_ust ↔ CEK_K5_ic1_1_kayis — kayış çene arasında sıkışır
- CEK_K5_ic1_1_cene_vida ↔ CEK_K5_ic1_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K6_ic1_1_kasnak ↔ CEK_K6_ic1_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K6_ic1_1_avara ↔ CEK_K6_ic1_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K6_ic1_1_cene_alt ↔ CEK_K6_ic1_1_kayis — kayış çene arasında sıkışır
- CEK_K6_ic1_1_cene_ust ↔ CEK_K6_ic1_1_kayis — kayış çene arasında sıkışır
- CEK_K6_ic1_1_cene_vida ↔ CEK_K6_ic1_1_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K6_ic1_2_kasnak ↔ CEK_K6_ic1_2_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K6_ic1_2_avara ↔ CEK_K6_ic1_2_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K6_ic1_2_cene_alt ↔ CEK_K6_ic1_2_kayis — kayış çene arasında sıkışır
- CEK_K6_ic1_2_cene_ust ↔ CEK_K6_ic1_2_kayis — kayış çene arasında sıkışır
- CEK_K6_ic1_2_cene_vida ↔ CEK_K6_ic1_2_kayis — çene cıvatası kayış deliğinden geçer
- CEK_K6_tatli_1_kasnak ↔ CEK_K6_tatli_1_kayis — kayış dişi motor kasnağına oturur (model teması)
- CEK_K6_tatli_1_avara ↔ CEK_K6_tatli_1_kayis — kayış dişi avara kasnağına oturur (model teması)
- CEK_K6_tatli_1_cene_alt ↔ CEK_K6_tatli_1_kayis — kayış çene arasında sıkışır
- CEK_K6_tatli_1_cene_ust ↔ CEK_K6_tatli_1_kayis — kayış çene arasında sıkışır
- CEK_K6_tatli_1_cene_vida ↔ CEK_K6_tatli_1_kayis — çene cıvatası kayış deliğinden geçer

## HAVADA LİSTESİ NEDENLERİ
- sase_boy_arka/on: ilk alt montaj, ayaklardan önce havada (çekmece v3 kuralı: alt montajlar havada)
- g_dis_arka_ek_lamasi, tasiyici_dikme_3386_600, tasiyici_plaka ×2: grubuyla aynı harekette geliyor (tezgâhta puntalı / kaynaklı); denetim aynı hareket grubunu temas saymıyor
- g_isi_kalkani_isinim_08, istasyon_kutusu, zincir_kanal, ic_kanal_57: modelde dayandığı parçaya > 0,6 mm boşluk ya da bağlantı elemanı yok — model açığı

## VİDA / DELİK / DİŞ

| eleman | adet | delik | karşı diş | kavrama mm | uç taşma mm |
|---|---|---|---|---|---|
| DIN 7991 M5 × 6 | 3/öğe | ray dış eleman havşası | PEM SP-M5-1 (bölme sacı) | 2.0 | 0.77 |
| DIN 7991 M5 × 6 | 2/öğe | motor braketi Ø5,5 + havşa | PEM SP-M5-1 (arka iç sac) | 2.0 | 0.77 |
| ISO 7380 M3 × 12 | 2/öğe | tabla + üst çene + alt gövde Ø3,4 | ISO 4032 M3 somun | 2.4 | 0.84 |
| ISO 4762 M8 | 10/öğe | dış taban Ø9 + pul | M8 kapalı uçlu perçin somun (şase üst duvarı) | 12.5 | 1.0 |

Tüm 21 çekmece için değerler aynı (ray vidaları 126, braket vidaları 42, çene cıvataları 42). Motor M3 × 6, setskur, PEM: tek çekmece v3 ile aynı geometri (denetim_v3.md).
Şase cıvatası M8: perçin somun modelde AÇIK uçlu (ucu 1,0 mm geçer, boru içine). BOM "kapalı uçlu" diyor — kapalı uçluysa M8 × 16 olmalı (Kemal kararı).

## MODEL AÇIKLARI (bu turda modele işlenmedi)
1. PU levhalar köpük modelinden kesildi: pu_arka_yuksek / alcak dış arka flanşlarının, pu_sol sol köşebentlerin ve yan sacın, tk_depo_arka / sag PU sağ üst köşebendin büküm dış köşesini sarıyor → kesilmiş levha olarak takılamaz. Levha bölümü yeniden kesilmeli.
2. Bağlantı elemanı modelde yok: dikme / merdiven çerçeve ↔ dış taban (GFRP takoz üstünde serbest), evaporatör braketi ↔ iç arka sac, soğutma grubu, elektrik kutusu, istasyon kutusu, iç kanallar, ısı kalkanı ışınım sacı.
3. Punta noktaları ve kaynak dikişleri modelde yok (animasyonda dikişler gösteriliyor, puntalar yalnız metinde).
4. evap_kablo ↔ ic_kanal_31 kesişimi (32 üçgen).

## PLAN SORUNU (plan anı yol seçimi)
0 (yukarıdaki beyanlarla).
