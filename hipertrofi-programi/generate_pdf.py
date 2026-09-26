#!/usr/bin/env python3
"""Kanıta dayalı hipertrofi programı PDF üreticisi."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from days_data import DAY1, DAY2, DAY3, DAY4, DAY5, FOUR_DAY, DAYS

from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Flowable,
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
pdfmetrics.registerFont(TTFont("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerifBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))

NAVY = HexColor("#1B365D")
NAVY_DARK = HexColor("#12243F")
BLUE = HexColor("#2457A0")
PALE = HexColor("#F4F7FB")
LINE = HexColor("#D5DEEA")
ACCENT = HexColor("#C4A35A")
SOFT_RED = HexColor("#7A2430")
GREEN = HexColor("#1F6B4A")
MUTED = HexColor("#4A5568")
PAGE_W, PAGE_H = A4


class ColoredBox(Flowable):
    def __init__(self, text, width, bg, fg=NAVY, title=None):
        super().__init__()
        self.text = text
        self.box_width = width
        self.bg = bg
        self.fg = fg
        self.title = title
        self._body = ParagraphStyle(
            "boxbody",
            fontName="DejaVu",
            fontSize=8.4,
            leading=12.2,
            textColor=fg,
            alignment=TA_JUSTIFY,
        )
        self._title = ParagraphStyle(
            "boxtitle",
            fontName="DejaVuBold",
            fontSize=9.2,
            leading=12,
            textColor=fg,
        )

    def wrap(self, aw, ah):
        inner = self.box_width - 12 * mm
        self._flow = []
        h = 8 * mm
        if self.title:
            p = Paragraph(self.title, self._title)
            w, ph = p.wrap(inner, ah)
            self._flow.append(("t", p, ph))
            h += ph + 1.5 * mm
        p = Paragraph(self.text, self._body)
        w, ph = p.wrap(inner, ah)
        self._flow.append(("b", p, ph))
        h += ph
        self.width = self.box_width
        self.height = h
        return self.width, self.height

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(0.4)
        self.canv.roundRect(0, 0, self.width, self.height, 3.5, fill=1, stroke=1)
        y = self.height - 4 * mm
        for kind, p, ph in self._flow:
            y -= ph
            p.drawOn(self.canv, 6 * mm, y)
            if kind == "t":
                y -= 1.5 * mm


def styles():
    return {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", fontName="DejaVuBold", fontSize=9, leading=12,
            textColor=ACCENT, alignment=TA_CENTER, tracking=1.2,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", fontName="DejaVuBold", fontSize=24, leading=30,
            textColor=white, alignment=TA_CENTER,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontName="DejaVu", fontSize=11, leading=16,
            textColor=HexColor("#D9E4F2"), alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1", fontName="DejaVuBold", fontSize=14.5, leading=19,
            textColor=NAVY, spaceBefore=2 * mm, spaceAfter=3 * mm,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="DejaVuBold", fontSize=11.5, leading=15,
            textColor=BLUE, spaceBefore=3.5 * mm, spaceAfter=2 * mm,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="DejaVuBold", fontSize=10, leading=13.5,
            textColor=NAVY, spaceBefore=2.5 * mm, spaceAfter=1.2 * mm,
        ),
        "body": ParagraphStyle(
            "body", fontName="DejaVu", fontSize=9, leading=13.2,
            textColor=HexColor("#1C2330"), alignment=TA_JUSTIFY, spaceAfter=2.2 * mm,
        ),
        "center": ParagraphStyle(
            "center", fontName="DejaVu", fontSize=9, leading=13,
            textColor=MUTED, alignment=TA_CENTER,
        ),
        "small": ParagraphStyle(
            "small", fontName="DejaVu", fontSize=8, leading=11.4,
            textColor=MUTED, alignment=TA_JUSTIFY, spaceAfter=1.6 * mm,
        ),
        "ref": ParagraphStyle(
            "ref", fontName="DejaVu", fontSize=7.6, leading=10.6,
            textColor=HexColor("#2A3340"), leftIndent=10, firstLineIndent=-10,
            spaceAfter=1.4 * mm,
        ),
        "th": ParagraphStyle(
            "th", fontName="DejaVuBold", fontSize=7.4, leading=10,
            textColor=white, alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td", fontName="DejaVu", fontSize=7.6, leading=10.4,
            textColor=HexColor("#1C2330"), alignment=TA_LEFT,
        ),
        "tdc": ParagraphStyle(
            "tdc", fontName="DejaVu", fontSize=7.6, leading=10.4,
            textColor=HexColor("#1C2330"), alignment=TA_CENTER,
        ),
        "tdb": ParagraphStyle(
            "tdb", fontName="DejaVuBold", fontSize=7.7, leading=10.4,
            textColor=NAVY, alignment=TA_LEFT,
        ),
        "why": ParagraphStyle(
            "why", fontName="DejaVu", fontSize=8.2, leading=11.8,
            textColor=HexColor("#243044"), alignment=TA_JUSTIFY, spaceAfter=1.2 * mm,
        ),
        "cue": ParagraphStyle(
            "cue", fontName="DejaVu", fontSize=8, leading=11.4,
            textColor=HexColor("#334155"), alignment=TA_LEFT, spaceAfter=0.6 * mm,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="DejaVu", fontSize=7.4, leading=9,
            textColor=HexColor("#6B7280"),
        ),
        "toc": ParagraphStyle(
            "toc", fontName="DejaVu", fontSize=10, leading=16,
            textColor=NAVY, leftIndent=2 * mm,
        ),
    }


S = None  # filled in main


def P(text, style="body"):
    return Paragraph(text, S[style])


def heading_bar(title, subtitle=None):
    data = [[P(title, "th")]]
    if subtitle:
        sub = ParagraphStyle(
            "subbar", fontName="DejaVu", fontSize=7.6, leading=10,
            textColor=HexColor("#D5E4F7"), alignment=TA_CENTER,
        )
        data.append([Paragraph(subtitle, sub)])
    t = Table(data, colWidths=[178 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 3 if subtitle else 6),
                ("TOPPADDING", (0, 1), (-1, 1), 0),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def simple_table(headers, rows, widths):
    head = [P(h, "th") for h in headers]
    data = [head]
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            st = "tdb" if i == 0 else ("tdc" if i > 0 and i != 1 else "td")
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
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    t.setStyle(TableStyle(cmds))
    return t


def exercise_block(ex):
    widths = [62 * mm, 18 * mm, 22 * mm, 26 * mm, 18 * mm, 32 * mm]
    headers = ["Hareket", "Set", "Tekrar", "Dinlenme", "RIR", "Hedef"]
    row = [ex["name"], ex["sets"], ex["reps"], ex["rest"], ex["rir"], ex["target"]]
    tbl = simple_table(headers, [row], widths)
    bits = [tbl, Spacer(1, 1.6 * mm)]
    bits.append(P(f"<b>Neden bu hareket?</b> {ex['why']}", "why"))
    bits.append(P(f"<b>Uygulama:</b> {ex['cues']}", "cue"))
    if ex.get("swap"):
        bits.append(P(f"<b>Yedek:</b> {ex['swap']}", "cue"))
    bits.append(P(f"<b>Kanıt derecesi:</b> {ex['grade']}", "cue"))
    bits.append(Spacer(1, 3.2 * mm))
    return KeepTogether(bits)


def bullets(items):
    return ListFlowable(
        [
            ListItem(P(i, "body"), leftIndent=8, bulletColor=NAVY, value="•")
            for i in items
        ],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        bulletFontName="DejaVu",
        bulletFontSize=9,
        spaceBefore=0,
        spaceAfter=2 * mm,
    )


def header_footer(canv, doc):
    canv.saveState()
    if doc.page > 1:
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
        canv.setFillColor(ACCENT)
        canv.rect(0, PAGE_H - 12.7 * mm, PAGE_W, 0.7 * mm, fill=1, stroke=0)
        canv.setFillColor(white)
        canv.setFont("DejaVu", 7.4)
        canv.drawString(16 * mm, PAGE_H - 8.2 * mm, "KANITA DAYALI HİPERTROFİ PROGRAMI")
        canv.drawRightString(PAGE_W - 16 * mm, PAGE_H - 8.2 * mm, "5 gün · 1 bacak · 4 gün yedek")
        canv.setFillColor(PALE)
        canv.rect(0, 0, PAGE_W, 10 * mm, fill=1, stroke=0)
        canv.setFillColor(MUTED)
        canv.setFont("DejaVu", 7.2)
        canv.drawString(16 * mm, 4.2 * mm, "Tıbbi tavsiye değildir. Kaynaklar belgenin sonundadır.")
        canv.drawRightString(PAGE_W - 16 * mm, 4.2 * mm, f"{doc.page}")
    canv.restoreState()


def cover_page(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY_DARK)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canv.setFillColor(NAVY)
    canv.rect(0, PAGE_H * 0.38, PAGE_W, PAGE_H * 0.62, fill=1, stroke=0)
    canv.setFillColor(ACCENT)
    canv.rect(0, PAGE_H * 0.38 - 2.2 * mm, PAGE_W, 2.2 * mm, fill=1, stroke=0)
    canv.setFillColor(white)
    canv.setFont("DejaVuBold", 8.5)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 28 * mm, "BİREYSELLEŞTİRİLMİŞ DİRENÇ ANTRENMANI")
    canv.setFont("DejaVuBold", 22)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 48 * mm, "Kanıta Dayalı")
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 58 * mm, "Hipertrofi Programı")
    canv.setFont("DejaVu", 11)
    canv.setFillColor(HexColor("#D9E4F2"))
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 72 * mm, "5 gün  ·  Çekiş / İtiş / Bacak / Çekiş / İtiş")
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 79 * mm, "187 cm · 94 kg  ·  4 günlük hafta yedeği ile")

    y = PAGE_H * 0.38 - 16 * mm
    canv.setFillColor(white)
    canv.setFont("DejaVuBold", 9)
    canv.drawString(22 * mm, y, "Bu belge neyi içerir?")
    canv.setFont("DejaVu", 8.4)
    lines = [
        "• Haftanın 5 antrenman günü (1 tam bacak) + 4 günlük yedek",
        "• Her hareketin programa alınma gerekçesi ve kanıt derecesi",
        "• Orijinal programdan çıkarılan teknikler ve nedenleri",
        "• Beslenme, adım sayısı, ilerleme ve 8 haftalık takip notları",
        "• Numaralı kaynakça (kılavuz, meta-analiz, RCT, EMG/biyomekanik)",
    ]
    yy = y - 7 * mm
    canv.setFillColor(HexColor("#E8EEF6"))
    for line in lines:
        canv.drawString(22 * mm, yy, line)
        yy -= 5.6 * mm

    canv.setFillColor(ACCENT)
    canv.setFont("DejaVu", 7.6)
    canv.drawCentredString(PAGE_W / 2, 18 * mm, "Eylül 2026  ·  Hiçbir program evrensel olarak kusursuz değildir; bu program ilkeler + bireysel boşluklara göredir.")
    canv.restoreState()


# ---------------------------------------------------------------------------
# Kaynakça
# ---------------------------------------------------------------------------
REFS = [
    "[1] Mcleod JC ve ark. ACSM Position Stand. Resistance Training Prescription for Muscle Function, Hypertrophy, and Physical Performance in Healthy Adults: An Overview of Reviews. Med Sci Sports Exerc. 2026;58(4):851–872. PMID: 41843416. PMC: PMC12965823. https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823/",
    "[2] Schoenfeld BJ, Ogborn D, Krieger JW. Dose-response relationship between weekly resistance training volume and increases in muscle mass: a systematic review and meta-analysis. J Sports Sci. 2017;35(11):1073–1082. PMID: 27433992.",
    "[3] Schoenfeld BJ, Contreras B, Krieger J ve ark. Resistance Training Volume Enhances Muscle Hypertrophy but Not Strength in Trained Men. Med Sci Sports Exerc. 2019;51(1):94–103. PMID: 30160419.",
    "[4] Schoenfeld BJ, Ogborn D, Krieger JW. Effects of Resistance Training Frequency on Measures of Muscle Hypertrophy: A Systematic Review and Meta-Analysis. Sports Med. 2016;46(11):1689–1697. PMID: 27102172.",
    "[5] Schoenfeld BJ, Grgic J, Krieger J. How many times per week should a muscle be trained to maximize muscle hypertrophy? A systematic review and meta-analysis. J Sports Sci. 2019;37(11):1286–1295. PMID: 30558493.",
    "[6] Grgic J, Schoenfeld BJ, Orazem J, Sabol F. Effects of resistance training performed to repetition failure or non-failure on muscular strength and hypertrophy: A systematic review and meta-analysis. J Sport Health Sci. 2022;11(2):202–211. PMID: 33497853. https://doi.org/10.1016/j.jshs.2021.01.007",
    "[7] Refalo MC, Helms ER, Trexler ET, Hamilton DL, Fyfe JJ. Influence of Resistance Training Proximity-to-Failure on Skeletal Muscle Hypertrophy: A Systematic Review with Meta-analysis. Sports Med. 2023;53(3):649–665. PMID: 36334240. PMC: PMC9935748.",
    "[8] Schoenfeld BJ, Pope ZK, Benik FM ve ark. Longer Interset Rest Periods Enhance Muscle Strength and Hypertrophy in Resistance-Trained Men. J Strength Cond Res. 2016;30(7):1805–1812. PMID: 26605807.",
    "[9] Wolf M, Androulakis-Korakakis P, Fisher J, Schoenfeld B, Steele J. Partial Vs Full Range of Motion Resistance Training: A Systematic Review and Meta-Analysis. Int J Strength Cond. 2023;3(1). https://journal.iusca.org/index.php/Journal/article/view/182",
    "[10] Kassiano W, Costa B, Kunevaliki G ve ark. Greater Gastrocnemius Muscle Hypertrophy After Partial Range of Motion Training Performed at Long Muscle Lengths. J Strength Cond Res. 2023;37(9):1746–1753.",
    "[11] Maeo S, Wu Y, Huang M ve ark. Triceps brachii hypertrophy is substantially greater after elbow extension training performed in the overhead versus neutral arm position. Eur J Sport Sci. 2023;23(4):450–458. PMID: 35819335. https://doi.org/10.1080/17461391.2022.2100279",
    "[12] Maeo S, Huang M, Wu Y ve ark. Greater Hamstrings Muscle Hypertrophy but Similar Damage Protection after Training at Long versus Short Muscle Lengths. Med Sci Sports Exerc. 2021;53(4):825–837. PMID: 33009197.",
    "[13] Plotkin DL, Coleman M, Van Every DW ve ark. Hip thrust and back squat training elicit similar gluteus muscle hypertrophy and transfer similarly to the deadlift. Front Physiol. 2023;14:1279170. https://doi.org/10.3389/fphys.2023.1279170",
    "[14] Fenwick CMJ, Brown SHM, McGill SM. Comparison of different rowing exercises: trunk muscle activation and lumbar spine motion, load, and stiffness. J Strength Cond Res. 2009;23(5):1408–1417. PMID: 19620925.",
    "[15] Rodríguez-Ridao D, Antequera-Vique JA, Martín-Fuentes I, Muyor JM. Effect of Five Bench Inclinations on the Electromyographic Activity of the Pectoralis Major, Anterior Deltoid, and Triceps Brachii during the Bench Press Exercise. Int J Environ Res Public Health. 2020;17(19):7339. PMC: PMC7579505. https://doi.org/10.3390/ijerph17197339",
    "[16] Coratella G, Tornatore G, Longo S, Esposito F, Cè E. An Electromyographic Analysis of Lateral Raise Variations and Frontal Raise in Competitive Bodybuilders. Int J Environ Res Public Health. 2020;17(17):6015. https://doi.org/10.3390/ijerph17176015",
    "[17] Andersen V, Fimland MS, Wiik E, Skoglund A, Saeterbakken AH. Effects of grip width on muscle strength and activation in the lat pull-down. J Strength Cond Res. 2014;28(4):1135–1142. https://doi.org/10.1097/JSC.0000000000000232",
    "[18] Marchetti PH, Uchida MC. Effects of the pullover exercise on the pectoralis major and latissimus dorsi muscles as evaluated by EMG. J Appl Biomech. 2011;27(4):380–384. PMID: 21975179.",
    "[19] Nunes JP, Grgic J, Cunha PM ve ark. What influence does resistance exercise order have on muscular strength gains and muscle hypertrophy? A systematic review and meta-analysis. Eur J Sport Sci. 2021;21(2):149–157. https://doi.org/10.1080/17461391.2020.1733672",
    "[20] Coleman M, Harrison K, Arias R ve ark. Effects of Drop Sets on Skeletal Muscle Hypertrophy: A Systematic Review and Meta-analysis. Sports Med Open. 2023;9:66. https://doi.org/10.1186/s40798-023-00620-5",
    "[21] Morton RW, Murphy KT, McKellar SR ve ark. A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults. Br J Sports Med. 2018;52(6):376–384. PMID: 28698222. PMC: PMC5867436.",
    "[22] Jäger R, Kerksick CM, Campbell BI ve ark. International Society of Sports Nutrition Position Stand: protein and exercise. J Int Soc Sports Nutr. 2017;14:20. PMID: 28642676. https://doi.org/10.1186/s12970-017-0177-8",
    "[23] Donnelly JE, Blair SN, Jakicic JM ve ark. ACSM Position Stand. Appropriate physical activity intervention strategies for weight loss and prevention of weight regain for adults. Med Sci Sports Exerc. 2009;41(2):459–471. PMID: 19127177.",
    "[24] World Health Organization. WHO guidelines on physical activity and sedentary behaviour. Geneva: WHO; 2020. https://www.who.int/publications/i/item/9789240015128",
    "[25] Helms ER, Cronin J, Storey A, Zourdos MC. Application of the Repetitions in Reserve-Based Rating of Perceived Exertion Scale for Resistance Training. Strength Cond J. 2016;38(4):42–49. https://doi.org/10.1519/SSC.0000000000000218",
    "[26] Speirs DE, Bennett MA, Finn CV, Turner AP. Unilateral vs. Bilateral Squat Training for Strength, Sprints, and Agility in Academy Rugby Players. J Strength Cond Res. 2016;30(2):386–392. PMID: 26244881.",
    "[27] Axler CT, McGill SM. Low back loads over a variety of abdominal exercises: searching for the safest abdominal challenge. Med Sci Sports Exerc. 1997;29(6):804–811. PMID: 9219209.",
    "[28] Reinold MM, Escamilla RF, Wilk KE. Current concepts in the scientific and clinical rationale behind exercises for glenohumeral and scapulothoracic musculature. J Orthop Sports Phys Ther. 2009;39(2):105–117. PMID: 19194023.",
    "[29] Schoenfeld BJ. The mechanisms of muscle hypertrophy and their application to resistance training. J Strength Cond Res. 2010;24(10):2857–2872. PMID: 20847704.",
    "[30] ACSM. Resistance training guidelines update (2026 özet). https://acsm.org/resistance-training-guidelines-update-2026/",
    "[31] ACSM yıllık toplantı özeti. Fascia Stretch Training-7 Induces Similar Metabolic Response, But Lower Mechanical Stress. Med Sci Sports Exerc. 2018;50(5S):S2649.",
    "[32] Enes A, Alves RC, Schoenfeld BJ ve ark. Rest-pause and drop-set training elicit similar strength and hypertrophy adaptations compared with traditional sets in resistance-trained males. Appl Physiol Nutr Metab. 2021;46(11):1417–1424. PMID: 34197702.",
]


def day_story(day):
    story = [heading_bar(day["title"], day["sub"]), Spacer(1, 3 * mm), P(day["intro"])]
    for ex in day["ex"]:
        story.append(exercise_block(ex))
    return story


def build_story():
    story = []
    story.append(PageBreak())  # cover drawn on page 1 via onFirstPage; this starts page 2

    # --- Nasil okunur ---
    story.append(heading_bar("1. Bu belge nasıl okunmalı?", "Kanıt hiyerarşisi · sınırlar · güvenlik"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        ColoredBox(
            "Bu bir antrenman rehberidir, tıbbi teşhis veya tedavi değildir. Bel, diz, omuz, göğüs "
            "ağrısı, nefes darlığı, baş dönmesi veya bilinen hastalığın varsa önce hekime danış. "
            "Fotoğraftan yağ yüzdesi, hormon bozukluğu veya jinekomasti teşhisi konmaz.",
            178 * mm,
            HexColor("#F8EDEE"),
            SOFT_RED,
            title="Güvenlik uyarısı",
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "<b>Kusursuz program iddiası yoktur.</b> ACSM 2026, direnç antrenmanında asıl sıçramanın "
            "‘hiç yapmamaktan düzenli yapmaya’ geçişte olduğunu; ekipman türü, karmaşık periyodizasyon "
            "ve her sette tükenişin ortalama yetişkinde sonucu tutarlı değiştirmediğini belirtir [1,30]. "
            "Bu dosya, senin fotoğrafındaki boşluklara (bel çevresi, lat genişliği, yan omuz, bacak/kalça) "
            "ve keyif aldığın sırt–biceps gününe göre <b>ilkeleri bireyselleştirir</b>."
        )
    )
    story.append(P("<b>Kanıt dereceleri</b> (her hareketin altında yazılıdır):"))
    story.append(
        bullets(
            [
                "<b>A —</b> Kılavuz, sistematik derleme veya meta-analiz (hacim, sıklık, ROM, protein, aktivite).",
                "<b>B —</b> Hipertrofiyi MRI/ultrason ile ölçen randomize veya çapraz-kol çalışma.",
                "<b>C —</b> EMG veya biyomekanik. Kasın o anda ‘yandığını’ gösterir; büyüyeceğini kanıtlamaz.",
                "<b>D —</b> Klinik pratik veya dolaylı çıkarım. Yetersizse metinde açıkça yazılır.",
            ]
        )
    )
    story.append(
        P(
            "EMG çalışması (ör. incline press, lateral raise, pulldown tutuşu) <b>hangi başın daha "
            "aktif göründüğünü</b> söyler. Büyüme iddiası için mümkün olduğunca MRI/ultrason RCT’si "
            "kullanıldı (triceps overhead [11], seated leg curl [12], hip thrust vs squat [13], "
            "baldır uzun kas boyu [10])."
        )
    )

    # --- Fotograf ---
    story.append(heading_bar("2. Fotoğrafa göre hedef", "Neden bu split, neden bu öncelikler"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Ön/yan/arka karelerde duran taban: trapez, kolda ve göğüste eski antrenman izi, kullanılabilir "
            "omuz iskeleti. Görüntüyü yöneten unsur bel çevresi yumuşak dokusu. Kas olarak geride kalanlar: "
            "<b>lat genişliği, yan deltoid, bacak ve kalça, üst sırt kalınlığı</b>. Biceps görsel darboğaz değil. "
            "<b>Boy 187 cm, kilo 94 kg</b> (BMI ≈ 26,9). Protein ve enerji hedefleri bölüm 12’de bu sayılara göredir."
        )
    )
    story.append(
        simple_table(
            ["Öncelik", "Neden (fotoğraf)", "Programdaki cevap", "Ana kaynak"],
            [
                [
                    "Bacak + kalça",
                    "Şort hattı dolgun değil; orijinal programda yok",
                    "Bacak 1 tam gün (hacim o seansa yığılır)",
                    "[1,13,24]",
                ],
                [
                    "Yan omuz",
                    "Omuz–bel oranı dar",
                    "7 doğrudan lateral set + press",
                    "[2,16]",
                ],
                [
                    "Lat / V kesiti",
                    "Arkadan sırt ve bel yakın genişlikte",
                    "Pulldown tam ROM + kablo row",
                    "[9,17]",
                ],
                [
                    "Bel çevresi",
                    "Yandan karın önde",
                    "Açık + adım; crunch ile yakılmaz",
                    "[23,24]",
                ],
                [
                    "Bel güvenliği",
                    "Pelvis önde, cheat row riski",
                    "Göğüs destekli row, RIR, nötr bel",
                    "[14,6]",
                ],
            ],
            [32 * mm, 48 * mm, 52 * mm, 46 * mm],
        )
    )
    story.append(Spacer(1, 2.5 * mm))
    story.append(
        P(
            "<b>Neden 5 gün ve neden tek bacak günü?</b> Hedefin 5 salon günü; bacağı 1 güne "
            "sığdırabiliyorsun. Üst vücut (sırt, göğüs, yan omuz) böylece haftada 2 kez uyarılır [4,5]. "
            "Bacak 1× kalır — bu, ACSM/DSÖ’nün ≥2 gün tercihine göre ikinci plandadır [1,24]. Telafi: "
            "o tek seansa ~12–16 ağır alt vücut seti yığmak. Hacim eşitlenince sıklığın kendisi sihir "
            "değildir [5]; 1 dolu bacak günü, 0 bacak gününden kat kat iyidir ve 4 üst + 1 bacak, "
            "orijinal 4× üst şablonundan daha dengelidir. 2. bir bacak günü ileride (ör. 6. ay) eklenebilir."
        )
    )

    story.append(
        KeepTogether(
            [
                simple_table(
                    ["Gün", "Odak", "Örnek yerleşme"],
                    [
                        ["1  Sırt & biceps A", "Pulldown, destekli row, curl", "Pazartesi"],
                        ["2  Göğüs & omuz A", "Incline, lateral, fly, overhead tri", "Salı"],
                        ["3  Bacak", "Leg press, RDL, thrust, split squat, curl", "Çarşamba"],
                        ["4  Sırt & biceps B", "V-bar pulldown, seated row, arka omuz", "Perşembe"],
                        ["5  Göğüs & omuz B", "Press, shoulder press, lateral", "Cuma"],
                        ["—", "İstirahat + yürüme (7–10 bin adım)", "Cmt–Paz"],
                    ],
                    [42 * mm, 78 * mm, 58 * mm],
                ),
                Spacer(1, 2 * mm),
                P(
                    "<b>4 günlük hafta:</b> Gün 5’i (göğüs & omuz B) iptal et, yerine ‘Üst karma’yı koy "
                    "(bölüm 9 salon kartı). <b>Bacak gününü asla kesme.</b> Tutarsız 6 gün, tutarlı "
                    "4–5 günden kötüdür [1,30]."
                ),
            ]
        )
    )

    # --- Kurallar ---
    story.append(heading_bar("3. Her seansın kuralları", "RIR, dinlenme, ROM, ısınma, ilerleme"))
    story.append(Spacer(1, 3 * mm))
    story.append(P("<b>RIR (yedekte kalan tekrar)</b> [6,7,25]"))
    story.append(
        P(
            "RIR 2 ≈ ‘düzgün formla 2 tekrar daha yapabilirdim’. ACSM, anlık kas tükenişinin "
            "ortalama yetişkinde sonucu tutarlı değiştirmediğini belirtir [1]. Grgic meta-analizi "
            "tükeniş vs tükenişe gitmeme arasında hipertrofide net üstünlük göstermez [6]; Refalo "
            "anlık failure’ın şart olmadığını söyler [7]. <b>Çok eklemli setler RIR 1–3; makine "
            "izolasyonunun son seti RIR 0–1.</b> Partnerli forced rep ve cheat yok."
        )
    )
    story.append(P("<b>Dinlenme</b> [8]"))
    story.append(
        P(
            "Antrenmanlı erkeklerde 3 dk dinlenme, 1 dk’ya göre squat/bench kuvvetini ve uyluk "
            "önü kalınlığını daha fazla artırmıştır [8]. Compound’larda 2,5–3 dk, izolasyonda "
            "75–90 sn. FST-7’nin 10 sn’si mekanik işi düşürür [31]."
        )
    )
    story.append(P("<b>ROM</b> [9,10]"))
    story.append(
        P(
            "Tam veya uzun (gerilmiş) ROM, kısa kas boyundaki kısmi ROM’dan üstün veya eşittir [9]. "
            "Pulldown tepesinde lat’i esnet; calf’ta topuğu indir; fly’da göğsü aç."
        )
    )
    story.append(P("<b>Isınma</b>"))
    story.append(
        P(
            "5–8 dk yürüyüş veya bike. İlk compound için 1–2 rampa seti (ör. pulldown 2×10 hafif). "
            "Bunlar çalışma seti sayılmaz. 10 dakikalık stretching devresi hipertrofi için gerekli değildir [1]."
        )
    )
    story.append(P("<b>İlerleme (double progression)</b> [1,29]"))
    story.append(
        P(
            "Hedef tekrar bandının üstünü (ör. 3×12) tüm çalışma setlerinde RIR kuralıyla bitirince "
            "yükü 2–5 kg veya 1 kablo plakası artır, tekrar alt banda (8) dön. 2 haftadır kilo ve "
            "tekrar yerindeyse uyku/stres bak; hemen drop set ekleme [20]. 7. veya 8. hafta deload: "
            "setleri ~2/3’e çek, RIR 3–4, yeni hareket yok."
        )
    )
    story.append(P("<b>Seans hacmi</b>"))
    story.append(
        P(
            "Üst günler ≈ 14–18, bacak günü ≈ 18–22 çalışma seti. Bacak 1× olduğu için o seans "
            "bilerek daha uzundur (75–90 dk). Süre 95 dakikayı geçerse leg extension ve karını kes, "
            "leg press + RDL + thrust + split squat’ı tut [2,3]."
        )
    )

    story += day_story(DAY1)
    story += day_story(DAY2)
    story += day_story(DAY3)
    story += day_story(DAY4)
    story += day_story(DAY5)
    story += day_story(FOUR_DAY)

    # --- Salon karti ---
    story.append(heading_bar("9. Salon kartı", "Telefona indirip salonda açmak için — yalnızca set/tekrar"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Aşağıdaki tablolar gerekçe metinleri olmadan tüm programdır. 5 günlük haftada 1–5; "
            "4 günlük haftada 1, 2, 3 ve ‘Üst karma’. RIR ve dinlenme bölüm 3’e uyar."
        )
    )

    def compact(day_label, exercises):
        rows = []
        for i, ex in enumerate(exercises, 1):
            rows.append(
                [
                    str(i),
                    ex["name"],
                    ex["sets"],
                    ex["reps"],
                    ex["rest"],
                    ex["rir"],
                ]
            )
        story.append(P(f"<b>{day_label}</b>", "h3"))
        story.append(
            simple_table(
                ["#", "Hareket", "Set", "Tekrar", "Dinlenme", "RIR"],
                rows,
                [10 * mm, 78 * mm, 22 * mm, 24 * mm, 24 * mm, 20 * mm],
            )
        )
        story.append(Spacer(1, 2.2 * mm))

    compact("Gün 1 — Sırt & biceps A", DAY1["ex"])
    compact("Gün 2 — Göğüs & omuz A", DAY2["ex"])
    compact("Gün 3 — Bacak (atlamayın)", DAY3["ex"])
    compact("Gün 4 — Sırt & biceps B  (5 günlük hafta)", DAY4["ex"])
    compact("Gün 5 — Göğüs & omuz B  (5 günlük hafta)", DAY5["ex"])
    compact("4 günlük hafta — Üst karma (Gün 5 yerine)", FOUR_DAY["ex"])

    # --- Hacim ozeti ---
    story.append(heading_bar("10. Haftalık çalışma seti özeti (5 günlük hafta)", "Isınma hariç"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Kas", "Doğrudan set/hafta", "Hedef bant [1–3]", "Not"],
            [
                ["Lat / üst sırt", "14–16", "10–16", "2 çekiş günü; FST-7 yok"],
                ["Göğüs", "10", "8–12", "Incline 3 + fly 2 + press 3 + crossover 2"],
                ["Yan deltoid", "7 + press", "8–12", "Lateral 4+3"],
                ["Arka deltoid", "6 + row", "6–10", "Face pull + reverse pec deck"],
                ["Triceps", "5 + press", "6–10", "Overhead 3 + pushdown 2 [11]"],
                ["Biceps", "7 + çekiş", "8–12", "Görsel öncelik değil"],
                ["Quadriceps", "9–12", "10–16 (1× gün)", "Tek seansa yığılmış [5]"],
                ["Glute", "9–12", "8–12", "Thrust + RDL + split squat + press"],
                ["Hamstring", "6 + mentşe", "8–12", "Seated curl tercih [12]"],
                ["Calf", "3–5", "6–10", "1× gün; zaman kalırsa seated +2"],
                ["Karın", "4", "4–8", "Yağ kaybı aracı değil [23]"],
            ],
            [32 * mm, 38 * mm, 32 * mm, 76 * mm],
        )
    )
    story.append(Spacer(1, 2.2 * mm))
    story.append(
        P(
            "Bacak 1× olduğu için calf/karın ikinci bir günde yok; hacim o seanstadır. 4 günlük "
            "haftada sırt ve göğüs karma günle 2× kalır; yan omuz ~4+3 yerine ~4+3 (karma 3 set) "
            "benzer bantta durur."
        )
    )

    # --- Orijinalden cikanlar ---
    story.append(heading_bar("11. Orijinal programdan ne çıktı, neden?", "Aynı keyif, daha az risk, eşit veya daha iyi uyaran"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Çıkan öğe", "Neden çıktı", "Kaynak"],
            [
                [
                    "FST-7 (7×10, 10 sn dinlenme)",
                    "Akut çalışmada benzer metabolik yanıt, daha az mekanik iş ve daha yüksek yorgunluk. Fasya gerilerek büyüme iddiası kanıtlanmamış.",
                    "[31,29]",
                ],
                [
                    "Her sette drop / rest-pause şovu",
                    "Eşit hacimde geleneksel setle benzer hipertrofi; avantaj zaman. Yorgunluk ve form bozulması artar.",
                    "[20,32]",
                ],
                [
                    "Barbell row’da cheat",
                    "Öne eğik row zaten en yüksek lomber kompresyonu üretir. Cheat, bel momentini artırır, lat gerilimini azaltır.",
                    "[14,29]",
                ],
                [
                    "Partnerli forced rep / ağır negatif",
                    "Tükeniş şart değil. Eksantrik yük hipertrofiye katkı verebilir [1] ama omuzda kontrol kaybı pahalıdır.",
                    "[1,6,7]",
                ],
                [
                    "Pulldown ROM %80, stretch yok",
                    "Uzun kas boyu / tam ROM lehinedir. Kısa kısmi ROM geride kalır.",
                    "[9]",
                ],
                [
                    "Front raise, fazla shrug",
                    "Front raise ön deltoid + üst pektoralis (zaten press’te var) [16]. Shrug trap’i row’larla da çalışır.",
                    "[16]",
                ],
                [
                    "Biceps drop + 6–8 izolasyon",
                    "Biceps darboğaz değil. Direkt 5 set + çekiş, ~10 setlik banda yeter.",
                    "[2]",
                ],
                [
                    "0 bacak günü (orijinal internet programı)",
                    "Tek dolu bacak seansı eklendi. 2× sıklık kanıtı daha güçlü [4,24]; 1 günde ~12–16 set yığmak 0’dan iyidir [5].",
                    "[1,4,5,24]",
                ],
            ],
            [42 * mm, 96 * mm, 40 * mm],
        )
    )

    # --- Beslenme ---
    story.append(heading_bar("12. Beslenme ve adım — 187 cm / 94 kg", "Fotoğrafı antrenmandan hızlı değiştiren kısım"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "<b>Kilon ve boyun.</b> 94 / 1,87² ≈ <b>BMI 26,9</b> (kilolu aralık). Bu bir hastalık "
            "teşhisi değil; bel çevresi fotoğrafı da aynı hikâyeyi anlatır. Hedef ‘kuru 94’ değil, "
            "yağsız kütleyi koruyarak bel çevresini yavaş indirmektir."
        )
    )
    story.append(
        P(
            "<b>Protein hedefi: 150–190 g/gün</b> (1,6–2,0 g/kg × 94 kg). ISSN 1,4–2,0 g/kg der [22]; "
            "Morton meta-analizi ≈1,6 g/kg civarında plato gösterir [21]. Pratik: <b>160–180 g</b> "
            "(öğün başına 30–45 g, 4–5 öğün) [22]. Diyet sıkılaşırsa 190–200 g’a çıkarmak yağsız "
            "kütleyi korumaya yardım eder [22]."
        )
    )
    story.append(
        P(
            "<b>Kalori (yaş bilinmediği için aralık).</b> Mifflin-St Jeor erkek: 10×94 + 6,25×187 − 5×yaş + 5. "
            "Yaş 28–38 varsayılırsa BMR ≈ 1920–1980 kcal. 5 gün direnç + günlük yürüyüşle TDEE kaba "
            "tahmin <b>≈ 2700–3100 kcal</b>. İlk 8–12 hafta: <b>2500–2800 kcal</b> (günde ~200–400 açık). "
            "Haftalık tartı 0,25–0,5 kg düşsün; 1 kg/hafta hızlıdır ve sırt antrenmanını bozar [23]. "
            "Kilo 2 hafta yerindeyse 150–200 kcal kes; performans ve uyku bozulursa 150 kcal ekle."
        )
    )
    story.append(
        P(
            "<b>Yürüme.</b> DSÖ, büyük kas gruplarını haftada ≥2 gün güçlendirmenin yanında "
            "haftalık 150–300 dk orta şiddetli aerobiği önerir [24]. Pratik hedef: <b>günde 7–10 bin "
            "adım</b> veya haftada 150–250+ dk tempolu yürüyüş [23,24]. Bu, ‘kardio kas yer’ "
            "mitinin yerine geçer; düşük şiddetli yürüyüş toparlanmayı bozmadan enerji harcar."
        )
    )
    story.append(
        P(
            "<b>Uyku ve alkol.</b> Bunların RCT’sini programa yazmak zorunda değil; pratikte 7–9 saat "
            "uyku ilerlemeyi, alkol ise protein sentezi ve kalori dengesini bozar. Kanıt derecesi "
            "burada genel fizyoloji, programın A/B çekirdeği değil."
        )
    )

    # --- Takip ---
    story.append(heading_bar("13. 8 haftalık takip", "Ayna pump’ı değil, sayı"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        bullets(
            [
                "Her seans: hareket, kilo, tekrar, RIR notu. Defter yoksa program işlemiyor demektir.",
                "Aynı 4 kare (ön/yan/arka, aynı ışık, sabah) 4. ve 8. hafta.",
                "Göbek hizası mezura, 2 haftada bir, sabah.",
                "Başarı: incline/leg press/pulldown’da tekrar veya kilo artışı + bel çevresinde yavaş düşüş.",
                "Başarısızlık sinyali: 3 haftadır yük yok, uyku bozuldu, eklem ağrısı — hacmi kes, drop ekleme.",
                "8. hafta sonunda: fotoğraf tekrarı. Yan omuz/lat hâlâ gerideyse lateral veya pulldown’a +1 set; "
                "biceps’e değil.",
            ]
        )
    )

    story.append(heading_bar("14. Mini ısınma ve seans içi düzen", "Uygulama detayı"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "<b>Bacak günü:</b> 5–8 dk bike, 1 set bodyweight squat, 1 hafif RDL. Bu seans 75–90 dk; "
            "telefon molası yok. <b>Üst günler:</b> kol çemberi 10+10, 1 hafif pulldown veya band face pull."
        )
    )
    story.append(
        P(
            "<b>Sıra.</b> Nunes meta-analizi: hipertrofi için çok eklem→izolasyon ile tersi benzerdir; "
            "<b>kuvvet, seansın başındaki harekette daha çok artar</b> [19]. Bu yüzden pulldown, press, "
            "leg press ve hip thrust günün başındadır. Yan omuz öncelikli olduğu için lateral, tamamen "
            "sona bırakılmaz."
        )
    )

    # --- Kaynakca ---
    story.append(heading_bar("15. Kaynakça", "Köşeli parantezler bu listeye karşılık gelir"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Birincil kaynaklar hakemli dergi veya kurum kılavuzudur. Blog, antrenör sözü ve "
            "‘fasya gerilimi mucizesi’ iddiaları listeye alınmadı. DOI/PMID verilenler doğrulanabilir.",
            "small",
        )
    )
    for r in REFS:
        story.append(P(r, "ref"))

    story.append(Spacer(1, 4 * mm))
    story.append(
        ColoredBox(
            "Özet: 5 gün (çekiş–itiş–bacak–çekiş–itiş), üst vücut 2×, bacak 1 dolu seans, "
            "kas başına kabaca 10+ ağır set, 8–15 tekrar, RIR 1–3, tam/uzun ROM, cheat/FST-7/drop yok. "
            "94 kg için protein 160–180 g, kalori 2500–2800 bandı, günde 7–10 bin adım. 4 günlük haftada "
            "bacak kalır, Gün 5 ‘üst karma’ya döner. Hareket markası ikincildir [1].",
            178 * mm,
            HexColor("#EAF2EA"),
            GREEN,
            title="Tek paragraf özet",
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        P(
            "Hazırlanış: Eylül 2026. Fotoğraf + 187 cm / 94 kg + 5 gün (1 bacak) tercihi. "
            "Genel popülasyon kılavuzu olarak kopyalanmamalı.",
            "center",
        )
    )
    return story


def main():
    global S
    S = styles()
    out = "/workspace/hipertrofi-programi/Kanita_Dayali_Hipertrofi_Programi.pdf"
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=14 * mm,
        title="Kanıta Dayalı Hipertrofi Programı",
        author="Bireyselleştirilmiş antrenman rehberi",
        subject="5 günlük çekiş/itiş/bacak hipertrofi programı (1 bacak günü, 4 gün yedek)",
    )
    doc.build(build_story(), onFirstPage=cover_page, onLaterPages=header_footer)
    print("Wrote", out)


if __name__ == "__main__":
    main()
