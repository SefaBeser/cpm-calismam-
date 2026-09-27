"""5-günlük (1 bacak) program verisi."""

DAY1 = {
    "title": "4. GÜN 1 — SIRT & BICEPS A",
    "sub": "Pulldown + 3 row  ·  70–80 dk  ·  kol hareketleri aynı",
    "intro": (
        "Sırt hareketleri senin listen: lat pulldown, barbell row, göğüs destekli row, tek kol "
        "DB row. Kablo row ve düz kol pulldown yok. Üç row da yatay çekiş — çeşit şart değil, "
        "fark destek türü [1]. Barbell row, karşılaştırılan row’lar içinde en yüksek lomber "
        "kompresyonu verir [14]; bu yüzden pulldown’dan hemen sonra, cheat’siz ve RIR 2–3 ile "
        "yapılır. Biceps günün sonundaki curl’ler aynı kalır. Göğüs bu günde yok."
    ),
    "ex": [
        {
            "name": "Lat pulldown (orta pronated tutuş, tam ROM)",
            "sets": "3 çalışma (+1–2 ısınma)",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Latissimus, biceps, alt trap",
            "why": (
                "V kesiti için en doğrudan dikey çekiş. Orta tutuşta lat EMG’si dar/geniş ile benzer, "
                "6RM yük biraz daha yüksektir [17]. Orijinal ‘ROM %80, stretch yok’ notu literatürün "
                "tersinedir [9]. Tükeniş her sette şart değil [1,6,7]."
            ),
            "cues": (
                "Göğüs açık, hafif geri yat. Bar üst göğse. Tepede lat’i esnet, sallama yok."
            ),
            "swap": "Nötr V-bar pulldown, assisted pull-up. Behind-the-neck yok.",
            "grade": "A (ROM, sıklık) + C (tutuş EMG).",
        },
        {
            "name": "Barbell row (önden, bel nötr)",
            "sets": "3",
            "reps": "6–10",
            "rest": "2,5–3 dk",
            "rir": "2–3",
            "target": "Üst sırt, lat, erektör",
            "why": (
                "Serbest ağırlık yatay çekiş; sırt kalınlığı için yükü taşır. Fenwick: ayakta öne "
                "eğik row, destekli varyantlardan daha yüksek lomber kompresyon üretir [14]. "
                "Pulldown’dan sonra, bel henüz taze iken yapılır. Cheat / ‘lat için kambur’ yok "
                "[29]. İlk haftalar ego kilo yok."
            ),
            "cues": (
                "Diz az kırık, gövde ~30–45°. Bel nötr, göğüs açık. Bar alt kaburga / kalça üstüne. "
                "Sırt yuvarlanınca set biter, kilo düşer."
            ),
            "swap": "Bel rahatsızsa bu 3 seti göğüs destekliye ekle. Pendlay yalnızca bel nötrse.",
            "grade": "A (hacim) + C (lomber yük [14]).",
        },
        {
            "name": "Göğüs destekli row (chest-supported / makine)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Orta trap, romboid, lat, arka deltoid",
            "why": (
                "Aynı yatay çekişi barbell’den daha düşük bel yüküyle verir [14]. Bar’dan sonra "
                "kalınlık hacmini tamamlar; pelvis önde durduğu için destekli varyant burada asıl "
                "kalite setidir."
            ),
            "cues": "Göğüs yastığa yapışık. Çekiş dirsekle. Cheat yok. RIR 1–2 [6,7].",
            "swap": "Chest-supported T-bar, seated machine row.",
            "grade": "A (çekiş hacmi) + C (omurga biyomekaniği).",
        },
        {
            "name": "Tek kol dumbbell row (bench destekli)",
            "sets": "3",
            "reps": "8–10 / kol",
            "rest": "90–120 sn",
            "rir": "1–2",
            "target": "Lat, orta sırt (tek taraf)",
            "why": (
                "Kablo row’un serbest ağırlık karşılığı. Tek kol asimetriyi görünür kılar. Bench’e "
                "el–diz destek, ayakta iki elle DB row’dan daha az bel ister [14]. ‘Lat için kambur’ "
                "bel fleksiyonu değildir."
            ),
            "cues": "Bir el ve aynı taraf diz bench’te. Bel nötr, çekiş kalça hizasına. Sol ve sağ ayrı sayılır.",
            "swap": "Kablo tek kol row. Ayakta desteksiz DB row yok.",
            "grade": "A + C [14].",
        },
        {
            "name": "Dumbbell supinated curl",
            "sets": "3",
            "reps": "10–12",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Biceps brachii",
            "why": (
                "Çekişler biceps’e dolaylı hacim verir; doğrudan ~8–12 set/hafta yeter [2]. Biceps "
                "görsel darboğazın değil. Momentum gerilimi azaltır [29]."
            ),
            "cues": "Dirsek gövde yanında, sallanma yok.",
            "swap": "Kablo curl, barbell curl (bilek rahatsa).",
            "grade": "A (hacim).",
        },
        {
            "name": "Hammer curl",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Brachialis, brachioradialis",
            "why": "Nötr tutuş brachialis/önkol. Orijinal drop set eşit hacimde üstün hipertrofi vermez [20].",
            "cues": "Başparmak yukarı, drop yok.",
            "swap": "Rope hammer curl.",
            "grade": "A [20] + C (anatomi).",
        },
    ],
}

DAY2 = {
    "title": "5. GÜN 2 — GÖĞÜS & OMUZ A",
    "sub": "6 hareket  ·  üst göğüs + düz press + yan omuz  ·  70–80 dk",
    "intro": (
        "Gün 1 ile aynı uzunluk: 6 hareket. Incline’dan sonra düz press eklenir ki seans tek "
        "press ile bitmesin; açı farkı üst vs orta pektoralis [15]. Lateral raise, front raise’den "
        "daha seçici orta deltoid uyarır [16]. Sıra: compound önce, çünkü kuvvet seansın başındaki "
        "harekette daha çok artar; hipertrofi sıra değişince benzerdir [19]."
    ),
    "ex": [
        {
            "name": "Incline press (makine veya dumbbell, ~30°)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–3",
            "target": "Üst pektoralis, ön deltoid, triceps",
            "why": (
                "30° civarı üst göğsü vurgularken 45–56° kadar ön deltoidi öne almaz [15]. Tam/uzun "
                "ROM kısmi kısa ROM’dan en az eşit veya daha iyidir [9]. Partnerli forced rep yok [6]."
            ),
            "cues": "Kürek bench’e sabit. Bar üst–orta göğse insin. Dirsekler aşırı açılmasın.",
            "swap": "Smith incline. Omuz rahatsızsa makine.",
            "grade": "A (hacim/ROM) + C (açı EMG). Incline üst göğüs MRI RCT’si sınırlıdır.",
        },
        {
            "name": "Göğüs press makinesi (düz)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Pektoralis, ön deltoid, triceps",
            "why": (
                "İkinci göğüs compound’u. ACSM ekipman türünün hipertrofiyi tutarlı değiştirmediğini "
                "belirtir [1]; makine, incline’dan sonra omuz stabilitesini kolaylaştırır. Gün 5’teki "
                "press ile 2× sıklık kalır [5]."
            ),
            "cues": "Kürek arkada. Kilidi çarpmadan uzat. Partnerli negatif yok [6].",
            "swap": "DB flat press, Smith düz. Dip yedek (Gün 5).",
            "grade": "A (hacim + sıklık).",
        },
        {
            "name": "Kablo lateral raise",
            "sets": "4",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan (orta) deltoid",
            "why": (
                "Omuz genişliği belin daha dar görünmesini sağlar. Orijinal programda yan omuz "
                "~4 set/haftaydı; hedef ~10+ ağır set [1,2]. Bu 4 set + Gün 5’teki 4 set ≈ 8 doğrudan "
                "+ press katkısı. Lateral, front raise’den daha seçici [16]."
            ),
            "cues": "Kol ~30° önde, 90°yi aşma, gövde sallanmasın.",
            "swap": "Seated DB lateral, makine lateral. Upright row yok.",
            "grade": "A (hacim) + C (EMG). Lateral vs press hipertrofi RCT’si yok.",
        },
        {
            "name": "Pec deck",
            "sets": "2",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Pektoralis (uzun kas boyu)",
            "why": (
                "Kablo fly’ın makine karşılığı. ACSM ekipman türünün hipertrofiyi tutarlı "
                "değiştirmediğini belirtir [1]. Açık pozisyondaki gerilme, kısa ‘sıkış’tan üstün "
                "veya eşittir [9,10]. Gün 5’te pec deck tekrarlanır (2× sıklık); kopya değil, "
                "lateral raise ile aynı mantık."
            ),
            "cues": "Kürek arkada, dirsek hafif kırık. Omuz öne gitmesin. Gerilmede dur, gövde kıpırdamasın.",
            "swap": "Kablo fly yalnızca pec deck yoksa.",
            "grade": "A (hacim + ROM).",
        },
        {
            "name": "Face pull (ip, yüz hizası)",
            "sets": "3",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Arka deltoid, dış rotatorlar, orta trap",
            "why": (
                "Press hacmine karşı denge. Klinik glenohumeral/skapular örüntü [28]. Hipertrofi "
                "RCT’si zayıf; daha doğrudan yedek reverse pec deck (Gün 4)."
            ),
            "cues": "İp kulak hizası, dış rotasyon, momentum yok.",
            "swap": "Reverse pec deck, reverse fly.",
            "grade": "D/C [28].",
        },
        {
            "name": "Overhead kablo triceps extension",
            "sets": "3",
            "reps": "10–12",
            "rest": "90 sn",
            "rir": "1–2",
            "target": "Triceps, özellikle uzun baş",
            "why": (
                "MRI’lı 12 haftalık çapraz-kol çalışmada baş üstü ekstansiyon, nötr kola göre daha "
                "fazla triceps büyümesi verdi (uzun baş +28,5% vs +19,6%) ve daha düşük yükle [11]."
            ),
            "cues": "Üst kol kulak yanında sabit. Bel çukuru artmasın.",
            "swap": "Overhead DB extension. Pushdown yedek (Gün 5).",
            "grade": "B (Maeo 2023, MRI).",
        },
    ],
}

DAY3 = {
    "title": "6. GÜN 3 — BACAK (5 hareket · ~55–70 dk)",
    "sub": "Squat, leg press, curl, extension, hyperextension  ·  atlama",
    "intro": (
        "Tek bacak günü, yalnızca yapabildiğin makinelere indirildi: squat + leg press (quad/kalça), "
        "leg curl (hamstring), extension (quad izolasyon), hyperextension (kalça–ham–erektör). "
        "Hip thrust, lunge, RDL, calf ve karın yok; 8 hareketlik seans enerjiyi bitirirdi. "
        "15 çalışma seti, 1× sıklık için yeterli bir dozdur [2,5]. Seated curl varsa prone’a tercih "
        "et [12]. 4 günlük haftada <b>bu günü asla kesme</b>."
    ),
    "ex": [
        {
            "name": "Squat (bar, Smith veya goblet)",
            "sets": "3",
            "reps": "8–12",
            "rest": "3 dk",
            "rir": "2–3",
            "target": "Quadriceps, glute, addüktör",
            "why": (
                "Günün en yorucu, en becerili hareketi olduğu için başta [19]. Plotkin: squat paterni "
                "kalçada hip thrust kadar, uyluk önünde daha fazla kesit artışı verir [13]. "
                "İlk haftalar RIR 2–3; ego squat yok. Smith/goblet serbest bara denk sayılır [1]."
            ),
            "cues": (
                "Topuklar yerde, dizler parmak yönünde. Derin ama bel yuvarlanmadan. "
                "Göğüs açık. Çıkışta kalçayı kilitleyip bel boşluğunu şişirme."
            ),
            "swap": "Smith squat, goblet squat, hack squat. Bel rahatsızsa bu 3 seti leg press’e ekle.",
            "grade": "A (hacim) + B (Plotkin 2023).",
        },
        {
            "name": "Leg press",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–3",
            "target": "Quadriceps, glute",
            "why": (
                "Squat’tan sonra hacmi güvenli tamamlar. Bel yastığa yaslı olduğu için squat kadar "
                "omurga becerisi istemez [1]. 3+3 = 6 compound quad seti; 1× gün için omurga budur [2]."
            ),
            "cues": "Bel yastıktan kalkmasın. Kontrollü in, kilidi çarpmadan uzat. Ayaklar omuz genişliği.",
            "swap": "Yoksa squat’a 2 set daha ekle. Hack squat.",
            "grade": "A (hacim) + B (squat paterni [13]).",
        },
        {
            "name": "Leg curl (oturarak varsa oturarak)",
            "sets": "3",
            "reps": "10–12",
            "rest": "90–120 sn",
            "rir": "0–2",
            "target": "Hamstring",
            "why": (
                "Hamstringi doğrudan büker. Seated (kalça bükük) curl, 12 haftalık MRI’da prone’dan "
                "daha fazla hamstring hacmi vermiştir (+14% vs +9%) [12]. Makine yüzüstüyse yine yap; "
                "3 set yeter. RDL olmadığı için bu 3 set kesilmez."
            ),
            "cues": "Kalça pad’e yapışık. Tam uzat, kontrollü bük. Kalçayı kaldırma.",
            "swap": "Lying / standing curl. Hepsi kabul.",
            "grade": "B (Maeo 2021, MRI).",
        },
        {
            "name": "Leg extension",
            "sets": "3",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Quadriceps (rektus femoris)",
            "why": (
                "Squat ve press rektus femorisi her zaman yeterince uzatmaz. 3 izolasyon seti haftalık "
                "quad’ı ~9–12 sete tamamlar [1,2]. Son sette RIR 0–1 olabilir."
            ),
            "cues": "Sırt yaslı. Üstte 0,5 sn. Diz ağrırsa ROM’u kısalt, kilo düş.",
            "swap": "Enerji biterse 2 sete in; squat ve press’i kesme.",
            "grade": "A (hacim tamamlama).",
        },
        {
            "name": "Hyperextension (plaka tutarak)",
            "sets": "3",
            "reps": "10–15",
            "rest": "90 sn",
            "rir": "1–3",
            "target": "Glute, hamstring, erektör",
            "why": (
                "RDL ve hip thrust’ın senin makine listendeki karşılığı. Kalçadan bükülen (belden "
                "kırılmayan) hyperextension arka zinciri yükler. Orijinal programdaki ‘kilo tutarak "
                "hyper’ notu burada kontrollü ve RIR’li haliyle durur. Bel yuvarlayarak ‘kambur "
                "hyper’ yok."
            ),
            "cues": (
                "Pad kalça kemiğinin hemen altında. Göğüs açık, bel nötr. Aşağı inerken kalça "
                "geriye, yukarı çıkarken kalçayı sık. Üstte bel boşluğunu şişirme. 5–10 kg plaka "
                "göğüste yeter; ilk hafta vücut ağırlığı da olur."
            ),
            "swap": "45° back extension. Reverse hyper yoksa bu kalır.",
            "grade": "A (arka zincir hacmi) + C/D (mentşe). RDL/hip thrust kadar doğrudan RCT’si yok; elindeki mentşe bu.",
        },
    ],
}

DAY4 = {
    "title": "7. GÜN 4 — SIRT & BICEPS B",
    "sub": "6 hareket  ·  pulldown + DB row + hammer  ·  70–80 dk",
    "intro": (
        "Sırtı haftada 2 kez uyarmak için [4,5]. Tek kol kablo yerine Gün 1’deki bench destekli "
        "DB row (2× sıklık; çeşit şart değil [1,5]). Düz kol pulldown çıktı — kanıtı zayıf [18]; "
        "lat dozu pulldown’a +1 set olarak gitti. 6. hareket hammer curl: Gün 1 ile aynı kol "
        "paterni. Enerji biterse hammer kesilir; pulldown 4 set kalır."
    ),
    "ex": [
        {
            "name": "Nötr tutuş lat pulldown (V-bar)",
            "sets": "4",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Latissimus, biceps",
            "why": (
                "Tutuş genişliği lat EMG’sini büyük değiştirmez [17]. Düz kol pulldown kesildi; "
                "1 set buraya eklendi (3→4). 4. set RIR 2; form düşünce kes."
            ),
            "cues": "Tam gerilme, göğüs açık. 1–2 RIR.",
            "swap": "Pronated pulldown (Gün 1’den farklı tutuş yeter).",
            "grade": "A (sıklık) + C (EMG).",
        },
        {
            "name": "Seated kablo row (dar veya D-handle)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2–2,5 dk",
            "rir": "1–2",
            "target": "Orta sırt, lat",
            "why": "Göğüs destekli / barbell row’dan farklı açı. Oturarak bel shear’i ayakta öne eğik row’dan düşüktür [14].",
            "cues": "Göğüs açık, bel nötr. Çekiş gövdeye, sallama yok.",
            "swap": "Makine row (Gün 1’den farklı tutuş).",
            "grade": "A + C [14].",
        },
        {
            "name": "Tek kol dumbbell row (bench destekli)",
            "sets": "3",
            "reps": "8–10 / kol",
            "rest": "90–120 sn",
            "rir": "1–2",
            "target": "Lat, orta sırt (tek taraf)",
            "why": (
                "Kablo row yerine senin DB row’un. Gün 1 ile aynı hareket; 2× sıklık hipertrofide "
                "çeşitten daha tutarlıdır [4,5]. Bench el–diz destek, ayakta desteksiz DB row yok [14]."
            ),
            "cues": "Bir el ve aynı taraf diz bench’te. Bel nötr, çekiş kalça hizasına. Sol ve sağ ayrı sayılır.",
            "swap": "Kablo tek kol row yalnızca bench yoksa.",
            "grade": "A + C [14].",
        },
        {
            "name": "Reverse pec deck veya reverse fly",
            "sets": "3",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "0–2",
            "target": "Arka deltoid",
            "why": (
                "Face pull (Gün 2) daha çok dış rotasyon; bu daha doğrudan arka deltoid izolasyonu. "
                "Coratella varyantları deltoid başlarını farklı vurgular [16]."
            ),
            "cues": "Kollar hafif kırık, shrug yok.",
            "swap": "Kablo reverse fly.",
            "grade": "A (izolasyon hacmi) + C [16].",
        },
        {
            "name": "Kablo curl",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Biceps",
            "why": "Gün 1’deki 5 set + bu 2 set + hammer 2 ≈ 9 doğrudan + çekişler ≈ 10–12/hafta [2].",
            "cues": "Dirsek sabit, tempo kontrollü.",
            "swap": "DB curl (Gün 1’den farklı açı, ör. incline curl).",
            "grade": "A (hacim).",
        },
        {
            "name": "Hammer curl",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Brachialis, brachioradialis",
            "why": (
                "Düz kol pulldown’ın ikamesi olarak 6. hareket. Lat değil; o doz pulldown’daki "
                "+1 settedir. Hammer Gün 1’de var — 2× sıklık, drop yok [20]."
            ),
            "cues": "Başparmak yukarı, sallanma yok.",
            "swap": "Rope hammer. Enerji biterse bu 2 seti kes; pulldown 4 kalsın.",
            "grade": "A [20] + C (anatomi).",
        },
    ],
}

DAY5 = {
    "title": "8. GÜN 5 — GÖĞÜS & OMUZ B",
    "sub": "5 hareket  ·  crossover yok; pec + lateral ekstra  ·  65–75 dk",
    "intro": (
        "Göğüs ve yan omuzu 2× tamamlar [4,5]. Crossover çıktı: aynı göğüs izolasyonu pec deck’te "
        "zaten var (Gün 2+5). 2 seti pec deck (+1) ve lateral’e (+1) bölündü — yan omuz senin "
        "görsel önceliğin [16]. 4 günlük haftada bu gün düşer; yerine ‘üst karma’ yapılır."
    ),
    "ex": [
        {
            "name": "Göğüs press makinesi (düz veya hafif incline)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Pektoralis, ön deltoid, triceps",
            "why": (
                "Göğsü ikinci kez uyarmak. Hacim eşitlenince sıklık sihir değil ama 2× dağıtım "
                "performansı taşır [5]. Makine, haftanın 5. gününde omuz stabilitesini kolaylaştırır [1]."
            ),
            "cues": "Kürek arkada. Partnerli negatif yok [6].",
            "swap": "DB flat press, Smith. Dip ancak omuz rahatsa.",
            "grade": "A (sıklık + hacim).",
        },
        {
            "name": "Shoulder press makine",
            "sets": "3",
            "reps": "8–10",
            "rest": "2,5 dk",
            "rir": "1–3",
            "target": "Ön/yan deltoid, triceps",
            "why": (
                "Dikey press, yan omuz izolasyonunun taşıyamadığı yükü verir. ACSM kuvvet için "
                "daha ağır yükleri (≥~8–10 tekrarlık zor set) öne çıkarır [1]. Tükeniş + partner yok."
            ),
            "cues": "Negatif kontrollü. Kilo omuzda kalsın, bel çukuru artmasın.",
            "swap": "Smith press, DB seated press.",
            "grade": "A (yük + hacim).",
        },
        {
            "name": "Kablo veya dumbbell lateral raise",
            "sets": "4",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan deltoid",
            "why": (
                "Gün 2’deki 4 setin ikinci yarısı + crossover’dan gelen 1 set [2,16]. "
                "Yorgunlukta kilo düşer, form düşmez."
            ),
            "cues": "Gün 2 ile aynı teknik.",
            "swap": "Makine lateral.",
            "grade": "A + C [16].",
        },
        {
            "name": "Pec deck",
            "sets": "3",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "0–2",
            "target": "Pektoralis (uzun kas boyu)",
            "why": (
                "Gün 2 pec deck ile 2× sıklık [4,5]. Crossover’ın 1 seti buraya eklendi (2→3). "
                "Açık pozisyondaki gerilme kısa ‘sıkış’tan üstün veya eşittir [9,10]. Enerji "
                "biterse 3. seti kes."
            ),
            "cues": "Kürek arkada, dirsek hafif kırık. Omuz öne gitmesin. Üstte 0,5 sn şart değil.",
            "swap": "Kablo fly yalnızca pec deck yoksa.",
            "grade": "A (hacim + ROM).",
        },
        {
            "name": "Kablo pushdown (V-bar veya ip)",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Triceps (lateral/medial baş)",
            "why": (
                "Overhead (Gün 2) uzun baş için üstün [11]; pushdown diğer başları ve ek hacmi verir. "
                "2 set yeter, orijinal programın tek triceps’i buraya sıkıştırılmaz."
            ),
            "cues": "Dirsek gövde yanında. 1 sn sıkış şart değil.",
            "swap": "Tek kol pushdown.",
            "grade": "A (hacim) + B (overhead önceliği [11]).",
        },
    ],
}

FOUR_DAY = {
    "title": "8b. 4 GÜNLÜK HAFTA — ÜST KARMA (Gün 5 yerine)",
    "sub": "Bacağı asla kesme  ·  55–70 dk  ·  Cuma veya Perşembe",
    "intro": (
        "4 güne düşersen varsayılan: Gün 1 Sırt A, Gün 2 Göğüs A, Gün 3 Bacak, Gün 4 bu karma. "
        "Gün 4’teki ikinci sırt seansı (Sırt B) o hafta yapılmaz; karma güne 3 set pulldown ve "
        "3 set row konur ki sırt ve göğüs yine 2× kalsın [4,5]."
    ),
    "ex": [
        {
            "name": "Shoulder press makine (veya göğüs press)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Deltoid, pektoralis, triceps",
            "why": (
                "Gün 2’de incline + düz press zaten var; burada dikey press göğsü 2× tutar ve "
                "omuzu Gün 5 düşmesin diye taşır [5]. Göğüs gerideyse düz press seç."
            ),
            "cues": "Gün 2/5 ile aynı teknik. Bel çukuru artmasın.",
            "swap": "Smith press, DB seated press.",
            "grade": "A (sıklık).",
        },
        {
            "name": "Lat pulldown (tam ROM)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Lat",
            "why": "Sırt B düştüğü için ikinci dikey çekiş burada [4].",
            "cues": "Tam gerilme [9].",
            "swap": "V-bar pulldown.",
            "grade": "A.",
        },
        {
            "name": "Göğüs destekli veya seated row",
            "sets": "3",
            "reps": "8–12",
            "rest": "2 dk",
            "rir": "1–2",
            "target": "Orta sırt",
            "why": "İkinci yatay çekiş [14].",
            "cues": "Bel nötr, cheat yok.",
            "swap": "Makine row.",
            "grade": "A + C.",
        },
        {
            "name": "Kablo lateral raise",
            "sets": "3",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Yan deltoid",
            "why": "Gün 5 düşünce yan omuz 4 sete düşmesin [2,16].",
            "cues": "Form bozulunca kilo düş.",
            "swap": "DB lateral.",
            "grade": "A + C.",
        },
        {
            "name": "Overhead triceps veya curl (o hafta hangi kol gerideyse)",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Triceps veya biceps",
            "why": "Zaman kısaysa tek izolasyon. Overhead triceps kanıtı daha güçlü [11].",
            "cues": "Birini seç, ikisini şişirme.",
            "swap": "Pushdown veya hammer.",
            "grade": "B (triceps) / A (biceps hacmi).",
        },
    ],
}

DAYS = [DAY1, DAY2, DAY3, DAY4, DAY5]
