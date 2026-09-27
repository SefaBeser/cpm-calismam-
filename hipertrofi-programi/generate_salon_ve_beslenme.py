#!/usr/bin/env python3
"""Salon antrenman PDF + basit beslenme/takviye PDF."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from days_data import DAY1, DAY2, DAY3, DAY4, DAY5, FOUR_DAY

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

NAVY = HexColor("#1B365D")
NAVY_DARK = HexColor("#12243F")
PALE = HexColor("#F4F7FB")
LINE = HexColor("#D5DEEA")
ACCENT = HexColor("#C4A35A")
SOFT_RED = HexColor("#7A2430")
GREEN = HexColor("#1F6B4A")
MUTED = HexColor("#4A5568")
PAGE_W, PAGE_H = A4
S = None
OUT = Path(__file__).resolve().parent


def P(text, style="body"):
    return Paragraph(text, S[style])


def styles():
    return {
        "th": ParagraphStyle("th", fontName="DejaVuBold", fontSize=8, leading=11, textColor=white, alignment=TA_CENTER),
        "td": ParagraphStyle("td", fontName="DejaVu", fontSize=8.2, leading=11.2, textColor=HexColor("#1C2330"), alignment=TA_LEFT),
        "tdc": ParagraphStyle("tdc", fontName="DejaVu", fontSize=8.2, leading=11.2, textColor=HexColor("#1C2330"), alignment=TA_CENTER),
        "tdb": ParagraphStyle("tdb", fontName="DejaVuBold", fontSize=8.3, leading=11.2, textColor=NAVY, alignment=TA_LEFT),
        "body": ParagraphStyle("body", fontName="DejaVu", fontSize=9.2, leading=13.4, textColor=HexColor("#1C2330"), alignment=TA_JUSTIFY, spaceAfter=2.2 * mm),
        "small": ParagraphStyle("small", fontName="DejaVu", fontSize=8, leading=11.4, textColor=MUTED, alignment=TA_JUSTIFY, spaceAfter=1.5 * mm),
        "center": ParagraphStyle("center", fontName="DejaVu", fontSize=8.5, leading=12, textColor=MUTED, alignment=TA_CENTER),
        "h3": ParagraphStyle("h3", fontName="DejaVuBold", fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=2 * mm, spaceAfter=1.5 * mm),
        "cue": ParagraphStyle("cue", fontName="DejaVu", fontSize=8, leading=11.2, textColor=HexColor("#334155"), spaceAfter=0.8 * mm),
        "ref": ParagraphStyle("ref", fontName="DejaVu", fontSize=7.4, leading=10.4, textColor=HexColor("#2A3340"), leftIndent=9, firstLineIndent=-9, spaceAfter=1.2 * mm),
    }


def heading_bar(title, subtitle=None):
    data = [[P(title, "th")]]
    if subtitle:
        sub = ParagraphStyle("subbar", fontName="DejaVu", fontSize=7.8, leading=10.5, textColor=HexColor("#D5E4F7"), alignment=TA_CENTER)
        data.append([Paragraph(subtitle, sub)])
    t = Table(data, colWidths=[178 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 4 if subtitle else 7),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def simple_table(headers, rows, widths, first_bold=True):
    data = [[P(h, "th") for h in headers]]
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            if first_bold and i == 0:
                st = "tdb"
            elif i == 1 and first_bold:
                st = "td"
            elif i >= 1:
                st = "tdc" if i != 1 else "td"
            else:
                st = "td"
            if i == 1:
                st = "td"
            cells.append(Paragraph(str(val), S[st]))
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items):
    return ListFlowable(
        [ListItem(P(i, "body"), leftIndent=6, bulletColor=NAVY, value="•") for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=10,
        bulletFontName="DejaVu",
        bulletFontSize=9,
        spaceAfter=1.5 * mm,
    )


def box(title, text, bg, fg=NAVY):
    inner = []
    title_s = ParagraphStyle("bt", fontName="DejaVuBold", fontSize=9, leading=12, textColor=fg)
    body_s = ParagraphStyle("bb", fontName="DejaVu", fontSize=8.3, leading=12, textColor=fg, alignment=TA_JUSTIFY)
    data = [[Paragraph(title, title_s)], [Paragraph(text, body_s)]]
    t = Table(data, colWidths=[178 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 6),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
            ]
        )
    )
    return t


def header_footer(label):
    def _hf(canv, doc):
        canv.saveState()
        if doc.page > 1:
            canv.setFillColor(NAVY)
            canv.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
            canv.setFillColor(ACCENT)
            canv.rect(0, PAGE_H - 12.7 * mm, PAGE_W, 0.7 * mm, fill=1, stroke=0)
            canv.setFillColor(white)
            canv.setFont("DejaVu", 7.4)
            canv.drawString(16 * mm, PAGE_H - 8.2 * mm, label)
            canv.drawRightString(PAGE_W - 16 * mm, PAGE_H - 8.2 * mm, "187 cm · 94 kg")
            canv.setFillColor(PALE)
            canv.rect(0, 0, PAGE_W, 10 * mm, fill=1, stroke=0)
            canv.setFillColor(MUTED)
            canv.setFont("DejaVu", 7.2)
            canv.drawString(16 * mm, 4.2 * mm, "Tıbbi / diyetisyen tavsiyesi değildir.")
            canv.drawRightString(PAGE_W - 16 * mm, 4.2 * mm, str(doc.page))
        canv.restoreState()

    return _hf


def cover(title, lines, kicker="UYGULAMA DOSYASI"):
    def _cover(canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY_DARK)
        canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H * 0.42, PAGE_W, PAGE_H * 0.58, fill=1, stroke=0)
        canv.setFillColor(ACCENT)
        canv.rect(0, PAGE_H * 0.42 - 2.2 * mm, PAGE_W, 2.2 * mm, fill=1, stroke=0)
        canv.setFillColor(white)
        canv.setFont("DejaVuBold", 8.5)
        canv.drawCentredString(PAGE_W / 2, PAGE_H - 28 * mm, kicker)
        canv.setFont("DejaVuBold", 22)
        for i, line in enumerate(title.split("\n")):
            canv.drawCentredString(PAGE_W / 2, PAGE_H - 50 * mm - i * 11 * mm, line)
        canv.setFillColor(HexColor("#D9E4F2"))
        canv.setFont("DejaVu", 10.5)
        canv.drawCentredString(PAGE_W / 2, PAGE_H - 78 * mm, "187 cm  ·  94 kg  ·  5 gün salon (1 bacak)")
        y = PAGE_H * 0.42 - 16 * mm
        canv.setFillColor(white)
        canv.setFont("DejaVuBold", 9)
        canv.drawString(22 * mm, y, "Bu dosyada:")
        canv.setFont("DejaVu", 8.5)
        yy = y - 7 * mm
        canv.setFillColor(HexColor("#E8EEF6"))
        for line in lines:
            canv.drawString(22 * mm, yy, "•  " + line)
            yy -= 5.8 * mm
        canv.setFillColor(ACCENT)
        canv.setFont("DejaVu", 7.5)
        canv.drawCentredString(PAGE_W / 2, 16 * mm, "Kanıta dayalı uzun PDF ayrıdır. Bu dosya salonda / mutfakta kullanılmak içindir.")
        canv.restoreState()

    return _cover


def clean_sets(s):
    s = str(s).replace("çalışma ", "")
    return s


def day_card(day, short_title):
    rows = []
    for i, ex in enumerate(day["ex"], 1):
        rows.append([str(i), ex["name"], clean_sets(ex["sets"]), ex["reps"], ex["rest"], ex["rir"]])
    bits = [
        heading_bar(short_title, day["sub"]),
        Spacer(1, 3 * mm),
        simple_table(["#", "Hareket", "Set", "Tekrar", "Dinlenme", "RIR"], rows, [10 * mm, 72 * mm, 22 * mm, 26 * mm, 26 * mm, 22 * mm]),
        Spacer(1, 2.5 * mm),
        P("<b>Form (kısa)</b>", "h3"),
    ]
    for ex in day["ex"]:
        bits.append(P(f"<b>{ex['name'].split('(')[0].strip()}:</b> {ex['cues']}", "cue"))
        if ex.get("swap"):
            bits.append(P(f"Yedek: {ex['swap']}", "small"))
    bits.append(Spacer(1, 2 * mm))
    bits.append(P("Isınma: 5–8 dk yürüyüş/bike + ilk harekette 1–2 rampa seti (yazılmaz). Compound RIR 1–3, izolasyon son set 0–1. Cheat / drop / partner yok.", "small"))
    return bits


def build_training():
    story = [PageBreak()]
    story.append(heading_bar("Haftalık yerleşim", "5 gün hedef · 4 gün yedek"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Gün", "Seans", "Süre", "Not"],
            [
                ["Pazartesi", "Sırt & biceps A", "70–80 dk", "Pulldown + 3 row + curl"],
                ["Salı", "Göğüs & omuz A", "70–80 dk", "Incline + düz press + lateral"],
                ["Çarşamba", "Bacak (5 hareket)", "55–70 dk", "ATLAMAYIN"],
                ["Perşembe", "Sırt & biceps B", "70–80 dk", "Kablo çekiş + arka omuz"],
                ["Cuma", "Göğüs & omuz B", "65–75 dk", "4 günde bu gün düşer"],
                ["Cmt–Paz", "İstirahat", "—", "7–10 bin adım"],
            ],
            [32 * mm, 42 * mm, 28 * mm, 76 * mm],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        box(
            "4 güne düşersen",
            "Cuma’yı iptal et. Perşembe’yi ‘üst karma’ yap (bu PDF’in son kartı). Çarşamba bacağı asla kesme. Sırt A + göğüs A + bacak + üst karma = 4 gün.",
            HexColor("#F8EDEE"),
            SOFT_RED,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>Salon kuralları</b>", "h3"))
    story.append(
        bullets(
            [
                "<b>RIR:</b> 2 = düzgün formla 2 tekrar daha yapabilirdim. Çok eklemli 1–3, izolasyon son set 0–1.",
                "<b>Dinlenme:</b> compound 2,5–3 dk, izolasyon 75–90 sn.",
                "<b>ROM:</b> pulldown tepede geril, squat/press’te bel yuvarlanmasın, pec deck’te göğsü aç. Cheat yok.",
                "<b>İlerleme:</b> bandın üstünü (ör. 3×12) bitirince kilo ekle, tekrar 8’e dön.",
                "<b>Bacak enerjin biterse:</b> extension’ı 2 sete in; squat, press, curl, hyper kalsın.",
                "<b>Gün 1 bel yorulursa:</b> barbell row’u 2 sete in; pulldown ve göğüs destekli kalsın. Cheat row yok.",
                "<b>Üst gün uzarsa:</b> Gün 4 hammer’ı, Gün 5 pec deck’in 3. setini kes. İlk iki compound kalsın.",
            ]
        )
    )
    story.append(P("Gerekçeler ve kaynakça uzun PDF’tedir. Bu dosya yalnızca uygulama kartıdır.", "small"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        box(
            "Akşam duruş (~12 dk, ev)",
            "Bütün gün oturuyorsun. Salon duruşu ‘düzeltmez’; akşam kısa rutin + adım işe yarar. Sit-up yok. Ağrı/uyuşma varsa bu kartı bırak, hekime sor. Kart PDF’in sonundadır.",
            HexColor("#EAF2EA"),
            GREEN,
        )
    )

    cards = [
        (DAY1, "GÜN 1 — SIRT & BICEPS A  ·  Pazartesi"),
        (DAY2, "GÜN 2 — GÖĞÜS & OMUZ A  ·  Salı"),
        (DAY3, "GÜN 3 — BACAK  ·  Çarşamba"),
        (DAY4, "GÜN 4 — SIRT & BICEPS B  ·  Perşembe"),
        (DAY5, "GÜN 5 — GÖĞÜS & OMUZ B  ·  Cuma"),
        (FOUR_DAY, "4 GÜNLÜK HAFTA — ÜST KARMA  ·  Gün 5 yerine"),
    ]
    for day, title in cards:
        story.append(PageBreak())
        story.extend(day_card(day, title))
    story.append(PageBreak())
    story.extend(evening_posture_card())
    return story


def evening_posture_card():
    rows = [
        ["1", "Kapı aralığı göğüs esnetme", "2×30–40 sn", "Göğüs/omuz içi (oturunca kısalır)"],
        ["2", "Yarım diz kalça flexör esnetme", "2×40 sn / bacak", "Kalça önü (APT / sandalye)"],
        ["3", "Glute bridge (yere sırtüstü)", "2×10–12", "Kalça; bel boşluğunu şişirme"],
        ["4", "Duvar kaydırma (wall slide)", "2×8–10", "Kürek + göğüs kafesi açılma"],
        ["5", "Çene içeri (chin tuck)", "2×8, 3 sn tut", "İleri kafa duruşu"],
        ["6", "Dead bug", "2×6 / taraf", "Karın anti-ekstansiyon; sit-up yok"],
    ]
    return [
        heading_bar("AKŞAM DURUŞ  ·  ev, iş günleri", "~12 dk  ·  07:00 antrenmanı yormaz  ·  ağırlık yok"),
        Spacer(1, 3 * mm),
        P(
            "Duruş ‘bir hareketle düzelmez’. Masa başı günü göğsü ve kalça önünü kısaltır, küreği ve "
            "kalçayı uyuşturur. Bu kart germe + düşük yük. Salon zaten row, face pull, reverse pec, "
            "squat ve hyperextension veriyor; akşam ekstra bar yok. Yemekten 20–30 dk sonra veya "
            "duş öncesi. Pazartesi barbell row belin doluysa 3 ve 6’yı atla, 1–2–4–5 kalsın. "
            "Kısa gösterim videoları: klasör <b>durus-videolari/</b> (6 dikey klip)."
        ),
        simple_table(
            ["#", "Hareket", "Doz", "Neden"],
            rows,
            [10 * mm, 62 * mm, 38 * mm, 68 * mm],
        ),
        Spacer(1, 2 * mm),
        P("<b>Nasıl</b>", "h3"),
        P("<b>Kapı esnetme:</b> Önkol kapı kenarında, gövde hafif öne, bel çukuru artmasın.", "cue"),
        P("<b>Kalça flexör:</b> Arka diz yerde, ön diz 90°. Kalçayı öne sık, bel boşluğunu şişirme.", "cue"),
        P("<b>Bridge:</b> Topuklar yerde, kalçayı kaldır, üstte 1 sn. Boyun rahat. Ağırlık yok.", "cue"),
        P("<b>Wall slide:</b> Sırt ve kalça duvara. Kollar W→Y, bel duvardan ayrılmasın.", "cue"),
        P("<b>Chin tuck:</b> Çifte çene, kafayı duvara yaklaştırır gibi. Omuzlar aşağı.", "cue"),
        P("<b>Dead bug:</b> Bel yere yapışık. Zıt kol–bacak yavaş. Bel kalkarsa ROM küçült.", "cue"),
        Spacer(1, 2 * mm),
        P(
            "Günde 8–10 bin adım bu karttan daha çok ‘oturmayı’ bozar. Sit-up, rus twist, ağır "
            "superman yok. Bu tıbbi fizyoterapi değildir.",
            "small",
        ),
    ]


def build_nutrition():
    story = [PageBreak()]
    story.append(heading_bar("1. Dürüst çerçeve", "Senin günün, eski 5 öğün şablon değil"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Hafta içi 06:30 kalkış, 07:00 salon, sonra iş; öğlene kadar yemek yok. Öğle: yumurta, "
            "peynir, zeytin, hindi füme, salatalık, domates. Akşam: pilav, tavuk, salata. Kreatin "
            "rastgele; arada abur cubur. Antrenmansız günde uyanış 07:45, yemek aynı. "
            "Önceki PDF kahvaltı + ara + rice cream + gece varsayıyordu — senin gününe uymaz. "
            "Öğün saati sihir değildir; tutman gereken <b>günlük protein ve kalori</b>dir."
        )
    )
    story.append(
        box(
            "Asıl sorun öğün sayısı değil",
            "İki öğünle de 160–180 g protein ve 2500–2800 kcal olur; porsiyonlar şu an büyük ihtimalle bunun altında. Sabah aç antrenman serbest. Spor çıkışı whey (protein). Rice cream istersen işte öğleden sonra tek başına — kolay karbonhidrat, kas sihri değil.",
            HexColor("#EAF2EA"),
            GREEN,
        )
    )

    story.append(heading_bar("2. Hedef sayılar", "187 cm · 94 kg · ilk 8–12 hafta"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Öğe", "Hedef", "Neden (kısa)"],
            [
                ["Kalori", "2500–2800 kcal", "Hafif açık; bel çevresi yavaş insin, antrenman düşmesin"],
                ["Protein", "160–180 g (hedef 170 g)", "1,7–1,9 g/kg; ISSN 1,4–2,0 g/kg"],
                ["Karbonhidrat", "220–280 g", "Akşam pilav + isteğe öğleden sonra rice cream"],
                ["Yağ", "70–90 g", "Peynir, zeytin, zeytinyağı; öğleyi şişirme, akşam ölç"],
                ["Su", "3–3,5 L", "Sabah salonda 0,5 L; öğle ve akşam rest"],
                ["Adım", "7–10 bin / gün", "İş–salon dışında en temiz ek harcama"],
                ["Tartı", "0,25–0,5 kg / hafta ↓", "Daha hızlı kesim 07:00 antrenmanını bozar"],
            ],
            [32 * mm, 48 * mm, 98 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        box(
            "Nasıl ayarla",
            "2 hafta tartı yerindeyse akşam pilavından 3–4 yemek kaşığı kes (proteinden değil). Uyku ve salon kilosu düşerse pilava 3 kaşık ekle veya 1 muz koy. Öğün saatini değiştirme.",
            HexColor("#EAF2EA"),
            GREEN,
        )
    )

    story.append(heading_bar("3. Antrenman günü — senin saatlerin", "~2600 kcal · ~170 g protein · tartı kullan"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Saat", "Ne", "≈ P / KH / Y"],
            [
                [
                    "06:30",
                    "Su + isteğe kahve (süt az veya yok). Yemek yok. Aç antrenman serbest.",
                    "—",
                ],
                [
                    "07:00–08:15 salon",
                    "Antrenman. Çantada shaker: 1 ölçek whey + su. Çıkışta 2 dk’da iç. Yemek değil.",
                    "28 / 3 / 2",
                ],
                [
                    "12:30–13:30 öğle",
                    "4 yumurta, 100 g hindi füme, 60–80 g peynir, 6–8 zeytin, salatalık+domates, 2 dilim ekmek, 200 g yoğurt. 5 g kreatin bu öğünle (su veya yoğurt).",
                    "78 / 45 / 42",
                ],
                [
                    "15:00–16:30 işte (isteğe)",
                    "Rice cream 50–60 g kuru + su veya süt, shaker’da. Tek başına. Pişirme yok. Protein değil; kaçırılan karbonhidrat/kalori.",
                    "2 / 45 / 1",
                ],
                [
                    "19:00–21:00 akşam",
                    "220–250 g tavuk (pişmiş), 500 g pilav (pişmiş, tart), bol salata, 1 tatlı kaşığı zeytinyağı. İsteğe 1 meyve.",
                    "70 / 140 / 18",
                ],
            ],
            [32 * mm, 100 * mm, 46 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "Kabaca whey + öğle + rice cream 55 g + akşam ≈ 177 g protein, ~235 g karbonhidrat, ~63 g yağ, ~2600 kcal. "
            "Rice cream yoksa pilavı 550 g’a çıkar veya öğleye 1 muz koy. Zeytini 15–20 adede çıkarma.",
            "small",
        )
    )
    story.append(
        bullets(
            [
                "<b>Whey atarsan:</b> öğleye +2 yumurta ve +50 g hindi ekle (aynı ~25–30 g protein).",
                "<b>Ekmek yemiyorsan:</b> öğleye 200 g yoğurt kalır; karbonhidratı akşam pilavında topla (500 g pişmiş).",
                "<b>İş yerinde ısıtma yok:</b> öğle zaten soğuk kahvaltılık; akşam evde pilav–tavuk yeter.",
                "<b>Antrenmansız gün (07:45):</b> whey yok. Rice cream yarıya (30 g) veya yok. Öğle + akşam aynı. Kreatin öğle ile 5 g.",
            ]
        )
    )

    story.append(heading_bar("4. Porsiyon kılavuzu (senin yemeklerin)", "Büyüt, menüyü değiştirme"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        simple_table(
            ["Ne", "Şu an muhtemel", "Hedef porsiyon"],
            [
                ["Yumurta (öğle)", "2–3", "4 (isteğe +1 beyaz)"],
                ["Hindi füme", "2–3 dilim", "100 g (etiket / 5–6 dilim)"],
                ["Peynir", "1 kibrit kutusu", "60–80 g"],
                ["Zeytin", "avuca göre", "6–8 adet, daha fazla değil"],
                ["Ekmek", "yok veya 1 dilim", "2 dilim (veya yoksa pilavı büyüt)"],
                ["Yoğurt", "yok", "200 g öğle — protein + tokluk"],
                ["Tavuk (akşam, pişmiş)", "1 küçük parça", "220–250 g"],
                ["Pilav (akşam, pişmiş)", "4–5 kaşık", "500 g (rice cream varsa 450 g yeter)"],
            ],
            [42 * mm, 52 * mm, 84 * mm],
        )
    )

    story.append(heading_bar("5. Abur cubur ve kaçış günü", "Yasak yok, yerini bil"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "Haftada 2–3 kez, <b>akşam yemeğinden sonra</b>, tek porsiyon (1 paket cips değil; "
            "1 çikolata, 1 dilim börek, 1 kâse dondurma). O gün pilavı ~100 g pişmiş azalt <b>ve "
            "rice cream’i atla</b>. Öğle yerine abur cubur yok — öğle senin protein omurgan."
        )
    )

    story.append(heading_bar("6. Takviyeler", "Az, senin çantana sığan"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Takviye", "Doz", "Ne zaman", "Not"],
            [
                [
                    "Kreatin monohidrat",
                    "5 g her gün",
                    "Öğle yemeğiyle (unutma)",
                    "Saat sihir değil. Antrenmansız günde de. Yükleme yok.",
                ],
                [
                    "Whey",
                    "1 ölçek (25–30 g protein)",
                    "Salon çıkışı, shaker + su",
                    "Kahvaltı değil. 2. ölçek şart değil. Atarsan öğleyi büyüt.",
                ],
                [
                    "Rice cream",
                    "50–60 g kuru (antrenman günü)",
                    "İşte ~15:00–16:30, tek başına shaker",
                    "Kolay KH/kcal. Protein yok. Abur cubur olan gün atla veya 30 g. Antrenmansız 30 g veya yok.",
                ],
                [
                    "Kafein / kahve",
                    "1 kahve",
                    "06:30, antrenman öncesi",
                    "Aç seansı kolaylaştırır. Sütü abartma. Akşam kahve yok.",
                ],
                [
                    "D vitamini",
                    "Hekim / kan testi",
                    "Öğle yemekle",
                    "Rastgele mega doz yok.",
                ],
                [
                    "Omega-3",
                    "1–2 g EPA+DHA",
                    "Akşam yemekle",
                    "Haftada 2 yağlı balık varsa şart değil.",
                ],
            ],
            [40 * mm, 32 * mm, 42 * mm, 64 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        P(
            "<b>Alma:</b> BCAA, fat burner, testosteron booster, glutamin şovu, 2. pre-workout. "
            "Kreatin ‘HCL / etil ester’ şart değil. Biraz su tutabilir; yağ değil. Böbrek hastalığın "
            "yoksa ISSN 3–5 g’ı sağlıklı erişkinde güvenli sayar. Hastalık/ilaç varsa hekim.",
            "body",
        )
    )

    story.append(heading_bar("7. Haftalık alışveriş", "İki öğün iskeleti"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullets(
            [
                "Yumurta 20–25 adet; hindi füme ~700 g; beyaz peynir; yoğurt 2 kg",
                "Tavuk 1,5–1,8 kg (pişmiş hedef 220–250 g × 7); pirinç (pilav akşamları büyük)",
                "Ekmek, salatalık, domates, salata yeşilliği, zeytin (az), zeytinyağı",
                "Whey (bitene), kreatin 5 g/gün, rice cream kutusu (antrenman günü 50–60 g kuru)",
            ]
        )
    )
    story.append(
        box(
            "Hafta içi zaman çizelgesi (senin günün)",
            "06:30 kalk + kahve · 07:00 salon · çıkışta whey · iş · 13:00 öğle kahvaltılık + kreatin 5 g · 15:30 rice cream 50–60 g (shaker, işte) · 20:00 pilav–tavuk–salata. Antrenmansız: 07:45 kalk, öğle ve akşam aynı, whey yok, rice cream yok veya 30 g, kreatin öğlede.",
            PALE,
            NAVY,
        )
    )

    story.append(Spacer(1, 4 * mm))
    story.append(heading_bar("8. Kısa kaynaklar", "Beslenme ve takviye"))
    story.append(Spacer(1, 2 * mm))
    for r in [
        "[1] Jäger R ve ark. ISSN Position Stand: protein and exercise. J Int Soc Sports Nutr. 2017;14:20. PMID: 28642676.",
        "[2] Morton RW ve ark. Protein supplementation + resistance training meta-analysis. Br J Sports Med. 2018;52:376–384. PMID: 28698222.",
        "[3] Kreider RB ve ark. ISSN creatine position stand. J Int Soc Sports Nutr. 2017;14:18. PMID: 28615996.",
        "[4] Donnelly JE ve ark. ACSM weight loss physical activity. Med Sci Sports Exerc. 2009;41:459–471. PMID: 19127177.",
        "[5] WHO guidelines on physical activity and sedentary behaviour. 2020.",
        "[6] Endocrine Society. Vitamin D for the Prevention of Disease. J Clin Endocrinol Metab. 2024.",
        "[7] Guest NS ve ark. ISSN caffeine position stand. J Int Soc Sports Nutr. 2021;18:1.",
        "[8] ACSM 2026 resistance training — tutarlı antrenman + yeterli protein; öğün saati ikincil.",
        "[9] Schoenfeld BJ, Aragon AA. How much protein can the body use in a single meal? J Int Soc Sports Nutr. 2018;15:10. (büyük öğünler boşa gitmez).",
    ]:
        story.append(P(r, "ref"))
    story.append(Spacer(1, 3 * mm))
    story.append(P("Bu bir diyet listesi şablonudur, kişiye özel tıbbi beslenme tedavisi değildir. Böbrek, karaciğer, gut, safra, diyabet veya ilaç kullanıyorsan takviyeyi hekime sor.", "center"))
    return story
def write_pdf(path, title, subject, story, cover_fn, label):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=14 * mm,
        title=title,
        author="Uygulama rehberi",
        subject=subject,
    )
    doc.build(story, onFirstPage=cover_fn, onLaterPages=header_footer(label))
    print("Wrote", path)


def main():
    global S
    S = styles()
    write_pdf(
        OUT / "Gunluk_Antrenman_Programi.pdf",
        "Günlük Antrenman Programı",
        "5 günlük salon kartları",
        build_training(),
        cover(
            "Günlük Antrenman\nProgramı",
            [
                "Pazartesi–Cuma seans kartları (set, tekrar, dinlenme, RIR)",
                "Kısa form ipuçları ve yedek hareket",
                "4 günlük hafta için üst karma kartı",
                "Akşam duruş kartı (~12 dk, ev)",
                "Bacak günü atlanmaz",
            ],
        ),
        "GÜNLÜK ANTRENMAN PROGRAMI",
    )
    write_pdf(
        OUT / "Beslenme_ve_Takviye_Programi.pdf",
        "Beslenme ve Takviye Programı",
        "94 kg iki öğün + spor çıkışı whey",
        build_nutrition(),
        cover(
            "Beslenme ve\nTakviye Programı",
            [
                "Aç 07:00 antrenman · öğle kahvaltılık · akşam pilav-tavuk",
                "2500–2800 kcal · 160–180 g protein · 2 öğün",
                "Whey salon çıkışı · rice cream işte 50–60 g · kreatin öğle 5 g",
                "Abur cubur: haftada 2–3, akşamdan sonra",
            ],
            kicker="BASİT BESLENME",
        ),
        "BESLENME VE TAKVİYE PROGRAMI",
    )


if __name__ == "__main__":
    main()
