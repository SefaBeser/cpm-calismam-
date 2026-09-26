"""5-günlük (1 bacak) program verisi."""

DAY1 = {
    "title": "4. GÜN 1 — SIRT & BICEPS A",
    "sub": "Öncelik: lat genişliği, sırt kalınlığı  ·  65–75 dk  ·  keyif aldığın güne en yakın gün",
    "intro": (
        "Bu, yaptığın sırt–biceps gününün kanıta göre sadeleştirilmiş hali. Lat pulldown tam ROM "
        "ile kalır [9,17]. Cheat row, drop ve FST-7 yok; mekanik gerilim asıl sürücüdür [20,29]. "
        "Göğüs bu günde yok — itiş Gün 2 ve Gün 5’tedir ki sırt performansın düşmesin [19]."
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
            "name": "Göğüs destekli row (chest-supported / makine)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Orta trap, romboid, lat, arka deltoid",
            "why": (
                "Yatay çekiş kalınlık için. Ayakta öne eğik row, karşılaştırılan üç row içinde en "
                "yüksek lomber kompresyonu verir [14]. Pelvis önde durduğu için destekli varyant "
                "aynı çekişi daha düşük bel yüküyle verir."
            ),
            "cues": "Göğüs yastığa yapışık. Çekiş dirsekle. Cheat yok. RIR 1–2 [6,7].",
            "swap": "Chest-supported T-bar, seated machine row. Barbell row yalnızca bel nötrse.",
            "grade": "A (çekiş hacmi) + C (omurga biyomekaniği).",
        },
        {
            "name": "Tek kol kablo row",
            "sets": "3",
            "reps": "8–10 / kol",
            "rest": "90–120 sn",
            "rir": "1–2",
            "target": "Lat (kalça hizası çekiş)",
            "why": (
                "Orijinal programın en mantıklı çekişlerinden; kaldı. Tek kol asimetriyi görünür kılar "
                "ve kablo lat uzunken gerilimi kesmez [9,14]. ‘Lat için kambur’ bel fleksiyonu değildir."
            ),
            "cues": "Bel nötr, el kalça yanına. Sol ve sağ ayrı sayılır.",
            "swap": "Bench destekli tek kol dumbbell row.",
            "grade": "A + C [14].",
        },
        {
            "name": "Düz kolla kablo pulldown (yüksek kablo)",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Lat / teres (omuz ekstansiyonu)",
            "why": (
                "Orijinal rope pullover’ın drop’suz hali. Barbell pullover EMG’si pektoralis lehinedir "
                "[18]; bu yüzden yüksek kablodan düz kol omuz ekstansiyonu olarak yapılır. RCT yok; "
                "kanıt yetersizse pulldown’a 1 set ekle."
            ),
            "cues": "Dirsek neredeyse kilit. İpi uyluğa indir. Drop yok [20].",
            "swap": "Ek lat pulldown seti.",
            "grade": "C/D [18].",
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
    "sub": "Öncelik: üst göğüs, yan omuz  ·  65–75 dk",
    "intro": (
        "Fotoğrafta yan deltoid bel çevresine göre geride. Lateral raise, front raise’den daha seçici "
        "orta deltoid uyarır [16]. Incline ~30° üst pektoralisi vurgular [15]. Sıra: compound önce, "
        "çünkü kuvvet seansın başındaki harekette daha çok artar; hipertrofi sıra değişince benzerdir [19]."
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
            "name": "Kablo lateral raise",
            "sets": "4",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan (orta) deltoid",
            "why": (
                "Omuz genişliği belin daha dar görünmesini sağlar. Orijinal programda yan omuz "
                "~4 set/haftaydı; hedef ~10+ ağır set [1,2]. Bu 4 set + Gün 5’teki 3 set ≈ 7 doğrudan "
                "+ press katkısı. Lateral, front raise’den daha seçici [16]."
            ),
            "cues": "Kol ~30° önde, 90°yi aşma, gövde sallanmasın.",
            "swap": "Seated DB lateral, makine lateral. Upright row yok.",
            "grade": "A (hacim) + C (EMG). Lateral vs press hipertrofi RCT’si yok.",
        },
        {
            "name": "Pec deck veya kablo fly (gerilme vurgulu)",
            "sets": "2",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Pektoralis (uzun kas boyu)",
            "why": (
                "Press’in yetiştiremediği göğüs hacmini tamamlar [1,2]. Uyaran ‘sıkış’tan çok açık "
                "pozisyondaki gerilmedir [9,10]. Tükenişe en yakın set burada olabilir [6]."
            ),
            "cues": "Dirsek hafif kırık, omuz öne savrulmasın. 3 sn negatif şart değil [1].",
            "swap": "Cable crossover.",
            "grade": "A (hacim + ROM). Fly vs press farkı net değildir.",
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
    "title": "6. GÜN 3 — BACAK (haftanın tek alt vücut günü)",
    "sub": "Quad + kalça + hamstring aynı seans  ·  75–90 dk  ·  atlama",
    "intro": (
        "5 günün 1’i bacak. ACSM ve DSÖ büyük kasları ≥2 gün/hafta ister [1,24]; sıklık "
        "meta-analizleri de 2×’i 1×’e tercih eder [4]. Tercihin 1 tam gündür: hacim eşitlenince "
        "1× hâlâ büyütür, yeter ki o güne yeterince ağır set yığılabilsin [5]. Bu yüzden iki kısa "
        "bacak günü yerine tek, dolu bir seans var. Quad için squat/press paterni, kalça için "
        "hip thrust, hamstring için seated curl (uzun kas boyu) aynı güne alındı [12,13]. "
        "4 günlük haftada <b>bu günü asla kesme</b>."
    ),
    "ex": [
        {
            "name": "Leg press (veya goblet / makine squat)",
            "sets": "4",
            "reps": "8–12",
            "rest": "3 dk",
            "rir": "1–3",
            "target": "Quadriceps, glute, addüktör",
            "why": (
                "Tek bacak gününde quad hacminin omurgası. ACSM ekipman türünün sonucu tutarlı "
                "değiştirmediğini belirtir [1]. Plotkin: squat paterni kalçada hip thrust kadar, "
                "uyluk önü ve addüktörde daha fazla kesit artışı [13]. 4 set, 1× sıklığı telafi eder [2]."
            ),
            "cues": "Bel yastıktan kalkmasın. Derin, kontrollü ROM [9]. Kilit çarpma yok.",
            "swap": "Hack squat, goblet squat, smith squat. Barbell squat ancak teknik hazırsa.",
            "grade": "A (hacim) + B (Plotkin 2023).",
        },
        {
            "name": "Romanian deadlift (dumbbell veya bar)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "2–3",
            "target": "Hamstring, glute, erektör",
            "why": (
                "Mentşe, hamstringi uzun kas boyunda yükler [9,12]. ‘Pelvik tilt tedavisi’ iddiası "
                "yok; amaç hipertrofi ve bel-güvenli kalça bükülmesidir. İlk haftalar RIR 3."
            ),
            "cues": "Diz az kırık, bar bacağı sıyırır, bel nötr. Yuvarlama yok.",
            "swap": "45° hiperextension (kalçadan, belden değil), cable pull-through.",
            "grade": "A (uzun kas boyu) + C/D (mentşe).",
        },
        {
            "name": "Hip thrust (bar, makine veya glute bridge)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Gluteus maximus",
            "why": (
                "MRI: hip thrust ve squat gluteusta benzer büyüme; squat quad’da önde [13]. "
                "Fotoğrafta kalça silik — ikisi de aynı günde."
            ),
            "cues": "Kürek bench’te, üstte kalça tam açılsın, bel aşırı çukur değil. İtme topukla.",
            "swap": "Makine hip thrust, tek bacak glute bridge.",
            "grade": "B (Plotkin 2023, MRI).",
        },
        {
            "name": "Bulgarian split squat veya reverse lunge",
            "sets": "3",
            "reps": "8–10 / bacak",
            "rest": "2 dk",
            "rir": "1–3",
            "target": "Quad, glute, tek bacak kontrolü",
            "why": (
                "Unilateral squat, çift bacakla karşılaştırılabilir kuvvet adaptasyonu verebilir [26]. "
                "Tek günde simetri ve ekstra quad/glute seti. İlk 2 hafta goblet ile öğren."
            ),
            "cues": "Arka ayak düşük destekte, gövde hafif öne. Diz rahatsa reverse lunge.",
            "swap": "Walking lunge, step-up, tutunarak split squat.",
            "grade": "B (Speirs 2016) + A (hacim).",
        },
        {
            "name": "Oturarak leg curl (seated)",
            "sets": "3",
            "reps": "10–12",
            "rest": "90–120 sn",
            "rir": "0–2",
            "target": "Hamstring (uzun kas boyu)",
            "why": (
                "12 haftalık MRI: seated curl prone’a göre tüm hamstring +14% vs +9% [12]. "
                "RDL mentşe, curl izolasyon; ikisi tamamlayıcıdır."
            ),
            "cues": "Kalça oturağa yapışık. Tam uzat, kontrollü bük.",
            "swap": "Lying curl yalnızca seated yoksa.",
            "grade": "B (Maeo 2021, MRI).",
        },
        {
            "name": "Leg extension",
            "sets": "2",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Quadriceps (rektus femoris)",
            "why": "Compound rektus femorisi her zaman yeterince uzatmaz. 2 set, ~12–14 quad set/haftayı tamamlar [1,2].",
            "cues": "Sırt yaslı. Üstte 0,5 sn. Diz ağrısında ROM kısalt.",
            "swap": "Zaman yoksa kes; leg press’i 4 sette tut.",
            "grade": "A (hacim tamamlama).",
        },
        {
            "name": "Standing calf raise (tam gerilme)",
            "sets": "3",
            "reps": "10–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Gastrocnemius",
            "why": (
                "Kassiano: uzun kas boyundaki (gerilmiş) çalışma medial gastrocnemius’ta tam ROM ve "
                "kısa kısımdan daha fazla büyüme [10]. Topuğu indir."
            ),
            "cues": "Basamak ucu, diz neredeyse kilit, altta 1 sn, zıplama yok.",
            "swap": "Leg press calf. Seated calf zaman kalırsa +2 set (soleus).",
            "grade": "B (Kassiano 2023).",
        },
        {
            "name": "Kablo crunch + plank",
            "sets": "2+2",
            "reps": "12–15 ve 30–45 sn",
            "rest": "60 sn",
            "rir": "1–3 / —",
            "target": "Rectus + anti-ekstansiyon",
            "why": (
                "Karın bel yağını yakmaz [23]. Sit-up lomber kompresyonu yüksektir [27]. 2 crunch "
                "(orijinal not: ağır ego yok) + 2 plank yeter."
            ),
            "cues": "Crunch’ta kaburga pelvise; plank’te kalça ne çökme ne çadır.",
            "swap": "Leg raise, dead bug. Sit-up yok.",
            "grade": "C [27] + A (spot reduction yok).",
        },
    ],
}

DAY4 = {
    "title": "7. GÜN 4 — SIRT & BICEPS B",
    "sub": "İkinci çekiş günü: hacim yayılır, 2× sıklık  ·  60–70 dk",
    "intro": (
        "Sırtı haftada 2 kez uyarmak için [4,5]. Hareketler Gün 1’in kopyası değil: nötr tutuş "
        "pulldown + farklı row açısı + arka deltoid izolasyonu. Biceps hacmi burada düşük tutulur; "
        "asıl iş Gün 1’dedir."
    ),
    "ex": [
        {
            "name": "Nötr tutuş lat pulldown (V-bar)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Latissimus, biceps",
            "why": (
                "Tutuş genişliği lat EMG’sini büyük değiştirmez [17]; nötr tutuş omuz rahatlığı ve "
                "çeşit için. İkinci uyaran, aynı hareketin kopyasından daha sürdürülebilirdir."
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
            "why": "Göğüs destekli row’dan farklı açı. Oturarak bel shear’i ayakta öne eğik row’dan düşüktür [14].",
            "cues": "Göğüs açık, bel nötr. Çekiş gövdeye, sallama yok.",
            "swap": "Makine row, chest-supported (Gün 1’den farklı tutuş).",
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
            "why": "Gün 1’deki 5 set + bu 2 set ≈ 7 doğrudan + çekişler ≈ 10–12/hafta [2]. Fazla curl yok.",
            "cues": "Dirsek sabit, tempo kontrollü.",
            "swap": "DB curl (Gün 1’den farklı açı, ör. incline curl).",
            "grade": "A (hacim).",
        },
    ],
}

DAY5 = {
    "title": "8. GÜN 5 — GÖĞÜS & OMUZ B",
    "sub": "İkinci itiş: düz press + yan omuz  ·  60–70 dk",
    "intro": (
        "Göğüs ve yan omuzu 2× tamamlar [4,5]. Omuz press, incline’tan sonra gelen dikey itiştir. "
        "4 günlük haftada bu gün düşer; yerine kısa bir ‘üst karma’ (bölüm 2) yapılır ki göğüs 1× kalmasın."
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
            "sets": "3",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan deltoid",
            "why": "Gün 2’deki 4 setin ikinci yarısı [2,16]. Yorgunlukta kilo düşer, form düşmez.",
            "cues": "Gün 2 ile aynı teknik.",
            "swap": "Makine lateral.",
            "grade": "A + C [16].",
        },
        {
            "name": "Cable crossover veya pec deck",
            "sets": "2",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "0–2",
            "target": "Pektoralis",
            "why": "Haftalık göğsü ~10 sete tamamlar (incline 3 + fly 2 + press 3 + crossover 2) [1,2].",
            "cues": "Gerilme vurgulu, omuz öne gitmesin.",
            "swap": "Pec deck (Gün 2’de fly yaptıysan crossover tercih et).",
            "grade": "A (hacim).",
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
            "name": "Incline press veya göğüs press makinesi",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Pektoralis",
            "why": "Göğsü 2× tutmak için. Gün 2 incline yaptıysan burada düz press seç [5].",
            "cues": "Gün 2/5 ile aynı teknik.",
            "swap": "Smith press.",
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
