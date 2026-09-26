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
                ["Pazartesi", "Sırt & biceps A", "65–75 dk", "Keyif aldığın çekiş günü"],
                ["Salı", "Göğüs & omuz A", "65–75 dk", "Incline + lateral"],
                ["Çarşamba", "Bacak (5 hareket)", "55–70 dk", "ATLAMAYIN"],
                ["Perşembe", "Sırt & biceps B", "60–70 dk", "İkinci çekiş"],
                ["Cuma", "Göğüs & omuz B", "60–70 dk", "4 günde bu gün düşer"],
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
                "<b>ROM:</b> pulldown tepede geril, squat/press’te bel yuvarlanmasın, fly’da göğsü aç. Cheat yok.",
                "<b>İlerleme:</b> bandın üstünü (ör. 3×12) bitirince kilo ekle, tekrar 8’e dön.",
                "<b>Bacak enerjin biterse:</b> extension’ı 2 sete in; squat, press, curl, hyper kalsın.",
            ]
        )
    )
    story.append(P("Gerekçeler ve kaynakça uzun PDF’tedir. Bu dosya yalnızca uygulama kartıdır.", "small"))

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
    return story


def build_nutrition():
    story = [PageBreak()]
    story.append(heading_bar("1. Hedef sayılar", "187 cm · 94 kg · ilk 8–12 hafta"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Öğe", "Hedef", "Neden (kısa)"],
            [
                ["Kalori", "2500–2800 kcal", "Hafif açık; bel çevresi yavaş insin, antrenman düşmesin"],
                ["Protein", "160–180 g (hedef 170 g)", "1,7–1,9 g/kg; ISSN 1,4–2,0 g/kg"],
                ["Karbonhidrat", "280–340 g", "5 gün ağırlık için yakıt; rice cream buraya girer"],
                ["Yağ", "70–90 g", "Hormonal/yemek doyumu; ~0,8–1 g/kg"],
                ["Su", "3–3,5 L + antrenman", "Kreatin ‘böbrek yakmaz’; su konfor içindir"],
                ["Adım", "7–10 bin / gün", "Bel çevresi için en temiz ek enerji harcaması"],
                ["Tartı", "0,25–0,5 kg / hafta ↓", "Daha hızlı kesim toparlanmayı bozar"],
            ],
            [32 * mm, 48 * mm, 98 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(
        box(
            "Nasıl ayarla",
            "2 hafta tartı yerindeyse 150–200 kcal kes (pirinç/yağdan, proteinden değil). Uyku ve salon kilosu düşerse 150 kcal ekle. Öğün saatleri sihir değildir; toplam gün yeter.",
            HexColor("#EAF2EA"),
            GREEN,
        )
    )

    story.append(heading_bar("2. Örnek antrenman günü (~2650 kcal · ~170 g protein)", "Gramlar pişmiş/yenilebilir tahmindir; tartı kullan"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Öğün", "Ne ye", "≈ P / KH / Y"],
            [
                [
                    "Kahvaltı",
                    "3 yumurta + 2 beyaz, 50 g yulaf (kuru), 200 ml süt veya 150 g yoğurt, 1 meyve",
                    "40 / 55 / 18",
                ],
                [
                    "Öğle",
                    "180 g tavuk/hindi (pişmiş), 250 g pirinç (pişmiş), bol salata, 1 tatlı kaşığı zeytinyağı",
                    "50 / 70 / 12",
                ],
                [
                    "Ara",
                    "200 g yoğurt + 1 meyve  VEYA  30 g peynir + 2 galeta",
                    "18 / 20 / 6",
                ],
                [
                    "Antrenman çevresi",
                    "Rice cream 60–70 g (kuru, etikete bak) + 1 ölçek whey (25–30 g protein) + 5 g kreatin. İsteğe 1 muz",
                    "32 / 80 / 3",
                ],
                [
                    "Akşam",
                    "180 g kıyma, balık veya tavuk; 300 g patates veya 90 g makarna (kuru); sebze; 1 tk zeytinyağı",
                    "42 / 65 / 22",
                ],
                [
                    "İsteğe gece",
                    "150–200 g yoğurt  veya  yarım ölçek whey (kalori bandı doluysa atla)",
                    "15 / 10 / 4",
                ],
            ],
            [36 * mm, 96 * mm, 46 * mm],
        )
    )
    story.append(Spacer(1, 2 * mm))
    story.append(P("Gece öğünü isteğe bağlıdır; kalori bandı doluysa atla. Gece hariç kabaca 170 g protein, ~290–320 g karbonhidrat, ~65 g yağ, ~2650 kcal. Pirinç/patates/yağ kaşığı ile 2500–2800’ü ayarla. Rice cream etiketindeki karbonhidrat 60–70 g üründe farklıysa porsiyonu ~70–80 g KH gelecek şekilde kes.", "small"))

    story.append(heading_bar("3. İstediğin gibi değiştir", "Protein kaynağı serbest, porsiyon benzer kalsın"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        simple_table(
            ["Bunun yerine", "Şunu koy (benzer protein)"],
            [
                ["180 g tavuk", "180 g hindi, 200 g yağsız kıyma, 200 g levrek/somon (yağ artar), 5–6 yumurta"],
                ["Yulaf", "2 dilim ekmek, 60 g granola (şekere dikkat), 200 g patates"],
                ["Pirinç", "Makarna, bulgur, patates, lavaş"],
                ["Yoğurt", "Ayran + peynir, süzme yoğurt, lor"],
                ["Whey", "200 g yoğurt + 30 g peynir, veya 150 g tavuk (öğüne ekle)"],
                ["Rice cream", "60–70 g yulaf, 1 büyük muz + 40 g bal, 200 g pişmiş pirinç"],
            ],
            [48 * mm, 130 * mm],
            first_bold=True,
        )
    )
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>İstirahat günü:</b> proteini aynı tut. Rice cream’i çıkar veya yarıya indir; akşam karbonhidratı biraz kıs. Adım hedefini tut.", "body"))

    story.append(heading_bar("4. Takviyeler", "Az, ucuz, kanıtı olan"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        box(
            "Kural",
            "Takviye yemeğin yerini tutmaz. 170 g proteini önce yemekle doldur; toz sadece açığı kapatır. Kreatin kullanmaya devam et — bu listedeki en güçlü performans takviyesidir.",
            HexColor("#EAF2EA"),
            GREEN,
        )
    )
    story.append(Spacer(1, 2.5 * mm))
    story.append(
        simple_table(
            ["Takviye", "Doz", "Ne zaman", "Not"],
            [
                [
                    "Kreatin monohidrat (kullanıyorsun)",
                    "5 g her gün",
                    "Fark etmez; rice cream + whey ile pratik",
                    "ISSN: 3–5 g idame. Yükleme şart değil. Her gün, antrenmansız günde de.",
                ],
                [
                    "Whey protein",
                    "1 ölçek (25–30 g protein)",
                    "Antrenman çevresi veya protein açık olan öğün",
                    "Gıda muadili. Günde 2 ölçek şart değil. Laktoz rahatsızsa isolate.",
                ],
                [
                    "Rice cream (pirinç kreması)",
                    "50–70 g kuru (etiket)",
                    "Antrenmandan 30–60 dk önce veya hemen sonra",
                    "Takviye değil, kolay karbonhidrat. Şeker şuruplu ‘dessert’ versiyonlara dikkat.",
                ],
                [
                    "D vitamini",
                    "Hekim / kan testi",
                    "Sabah, yemekle",
                    "Kapalı salon + kışta eksik sık. Rastgele mega doz yok. 25(OH)D baktır.",
                ],
                [
                    "Omega-3 (balık yağı)",
                    "1–2 g EPA+DHA",
                    "Yemekle",
                    "Haftada 2 yağlı balık yiyorsan şart değil.",
                ],
                [
                    "Kafein (isteğe)",
                    "150–250 mg",
                    "Antrenmandan 30–45 dk önce",
                    "Kahve yeter. Akşam antrenmanda uyku bozulursa kes.",
                ],
                [
                    "C vitamini / basit multi",
                    "Günlük DRI civarı",
                    "Kahvaltı",
                    "Performans sihri yok; sebze azsa sigorta. Mega doz C gerekmez.",
                ],
            ],
            [40 * mm, 32 * mm, 42 * mm, 64 * mm],
        )
    )
    story.append(Spacer(1, 2.5 * mm))
    story.append(P("<b>Alma (bu hedefler için gerek yok):</b> BCAA (protein zaten yüksek), ‘fat burner’, testosteron booster, fazla glutamin, kreatin yükleme şovu, 2. bir pre-workout eğer kahve içiyorsan.", "body"))
    story.append(
        P(
            "<b>Kreatin pratik:</b> her sabah veya shake’e 5 g monohidrat. Marka ‘HCL / etil ester’ şart değil. Biraz su tutabilir; bu yağ değil. Böbrek hastalığın yoksa ISSN sağlıklı erişkinde 3–5 g’ı güvenli sayar. Hastalık/ilaç varsa hekim.",
            "body",
        )
    )

    story.append(heading_bar("5. Haftalık alışveriş iskeleti", "Tek kişi, 5 antrenman günü"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullets(
            [
                "Tavuk/hindi 1,2–1,5 kg; kıyma veya balık 0,8–1 kg; yumurta 15–21 adet",
                "Yoğurt 2 kg, peynir, süt",
                "Pirinç, makarna, yulaf, patates, rice cream kutusu",
                "Zeytinyağı, sebze (donuk da olur), meyve 7–10 adet",
                "Whey (bitene kadar), kreatin (saf monohidrat), isteğe D vitamini / balık yağı",
            ]
        )
    )
    story.append(
        box(
            "Antrenman günü zaman çizelgesi (örnek, akşam salon)",
            "07:30 kahvaltı · 13:00 öğle · 16:30 ara · 18:00 rice cream + whey + kreatin · 18:45–20:15 salon · 21:00 akşam yemeği. Öğle antrenmanıysa rice cream’i öğle ile salon arasına al, akşam yemeğini normal tut.",
            PALE,
            NAVY,
        )
    )

    story.append(Spacer(1, 4 * mm))
    story.append(heading_bar("6. Kısa kaynaklar", "Beslenme ve takviye"))
    story.append(Spacer(1, 2 * mm))
    for r in [
        "[1] Jäger R ve ark. ISSN Position Stand: protein and exercise. J Int Soc Sports Nutr. 2017;14:20. PMID: 28642676.",
        "[2] Morton RW ve ark. Protein supplementation + resistance training meta-analysis. Br J Sports Med. 2018;52:376–384. PMID: 28698222.",
        "[3] Kreider RB ve ark. ISSN creatine position stand. J Int Soc Sports Nutr. 2017;14:18. PMID: 28615996. PMC: PMC5469049.",
        "[4] Donnelly JE ve ark. ACSM weight loss physical activity. Med Sci Sports Exerc. 2009;41:459–471. PMID: 19127177.",
        "[5] WHO guidelines on physical activity and sedentary behaviour. 2020.",
        "[6] Endocrine Society. Vitamin D for the Prevention of Disease. J Clin Endocrinol Metab. 2024. (sağlıklı <75 yaşta rastgele yüksek doz önerilmez; test/hekim).",
        "[7] Guest NS ve ark. ISSN caffeine position stand. J Int Soc Sports Nutr. 2021;18:1. (kafein 3–6 mg/kg; burada düşük–orta doz).",
        "[8] ACSM 2026 resistance training position stand — tutarlı antrenman + yeterli protein, sihirli toz değil.",
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
                "Bacak günü atlanmaz",
            ],
        ),
        "GÜNLÜK ANTRENMAN PROGRAMI",
    )
    write_pdf(
        OUT / "Beslenme_ve_Takviye_Programi.pdf",
        "Beslenme ve Takviye Programı",
        "94 kg basit beslenme + kreatin, whey, rice cream",
        build_nutrition(),
        cover(
            "Beslenme ve\nTakviye Programı",
            [
                "2500–2800 kcal · 160–180 g protein",
                "Örnek gün (rice cream + whey antrenman çevresi)",
                "Kreatin 5 g/gün, whey, D vitamini, omega-3, kafein",
                "Alınmayacak tozlar (BCAA, fat burner…)",
            ],
            kicker="BASİT BESLENME",
        ),
        "BESLENME VE TAKVİYE PROGRAMI",
    )


if __name__ == "__main__":
    main()
