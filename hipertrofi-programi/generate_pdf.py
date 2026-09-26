#!/usr/bin/env python3
"""Kanıta dayalı hipertrofi programı PDF üreticisi."""

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
        canv.drawRightString(PAGE_W - 16 * mm, PAGE_H - 8.2 * mm, "Üst / Alt · 4 gün")
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
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 72 * mm, "4 gün  ·  Üst A / Alt A / Üst B / Alt B")
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 79 * mm, "Orijinal sırt–biceps şablonunun fotoğrafa göre revizyonu")

    y = PAGE_H * 0.38 - 16 * mm
    canv.setFillColor(white)
    canv.setFont("DejaVuBold", 9)
    canv.drawString(22 * mm, y, "Bu belge neyi içerir?")
    canv.setFont("DejaVu", 8.4)
    lines = [
        "• Haftanın 4 antrenman günü (set, tekrar, dinlenme, RIR, yedek hareket)",
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
# Program data
# ---------------------------------------------------------------------------

DAY1 = {
    "title": "4. GÜN 1 — ÜST A",
    "sub": "Öncelik: göğüs, yan omuz, sırt kalınlığı  ·  65–80 dk",
    "intro": (
        "Fotoğrafta yan deltoid ve göğüs hattı bel çevresine göre geride; sırtta ise "
        "kalınlık (row) genişlikten (pulldown) ayrı bir ihtiyaç. Bu gün yatay itiş + yatay çekiş "
        "üzerine kuruludur. Çok eklemli hareketler önce gelir; çünkü kuvvet kazancı seansın "
        "başındaki harekette daha büyüktür, hipertrofi ise sıra değişince benzer kalır [19]. "
        "Yan omuz, izole hareket olarak günün erken ikinci yarısına alınmıştır; en sona "
        "bırakılırsa yorgun omuzla form bozulur."
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
                "Klavikular (üst) pektoralis, eğimli press’te düz press’e göre daha yüksek EMG "
                "gösterir; 30° civarı üst göğsü vurgularken omuzu 45–56° kadar öne almaz [15]. "
                "Tam/uzun ROM hipertrofi için kısmi (kısa kas boyu) ROM’dan en azından eşit, "
                "çoğu ölçüde daha iyidir [9]. Ağır yük (≥ yaklaşık 8–12 tekrarlık zor set) hem "
                "kuvvet hem büyüme uyarısı verir [1]."
            ),
            "cues": (
                "Kürek kemikleri bench’e sabit, ayak tabanı yerde. Bar/dumbbell memenin üst–orta "
                "hizasına insin. Dirsekler 90°den fazla açılmasın. Partnerli zorlanmış tekrar yok."
            ),
            "swap": "Smith incline veya dip yerine bu kalır; omuz rahatsızsa makine tercih et.",
            "grade": "A (hacim/ROM/yük ilkeleri) + C (açı EMG’si). Incline’ın üst göğsü büyüttüğüne dair doğrudan MRI RCT’si sınırlıdır; EMG + bölgesel hipertrofi mantığına dayanır.",
        },
        {
            "name": "Göğüs destekli row (chest-supported / makine)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Orta trap, romboid, lat, arka deltoid",
            "why": (
                "Yatay çekiş üst sırt kalınlığını hedefler. Ayakta öne eğilerek row, lomber "
                "omurgaya üç row varyasyonu içinde en yüksek kompresyonu verir [14]. Fotoğrafta "
                "pelvis önde ve bel hattı yüklü durduğu için göğüs destekli varyant, sırt kasını "
                "uyarırken bel momentini düşürür. Bu bir ‘daha çok hipertrofi’ iddiası değil, "
                "aynı çekiş uyarısını daha düşük bel yüküyle vermek içindir [14]."
            ),
            "cues": (
                "Göğüs yastığa yapışık. Çekiş dirsekle, bar/kablo alt göğüs–üst karın hizasına. "
                "Bel yuvarlama ve ‘cheat’ yok. 1–2 tekrar yedekte bitir [6,7]."
            ),
            "swap": "Göğüs destekli T-bar, chest-supported dumbbell row, seated machine row. "
                    "Ayakta barbell row ancak bel nötr ve cheat’sizse yedektir.",
            "grade": "A (çekiş hacmi) + C (omurga yükü biyomekaniği).",
        },
        {
            "name": "Kablo lateral raise",
            "sets": "4",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan (orta) deltoid",
            "why": (
                "Fotoğrafta en yüksek görsel getirisi olan üst vücut boşluğu yan omuzdur; bel "
                "çevresi değişmeden bile omuz genişliği belin daha dar görünmesini sağlar. "
                "Lateral raise, orta deltoidi front raise’den daha seçici uyarır; front raise "
                "ön deltoid ve klavikular pektoralisi öne çıkarır [16]. Orijinal programda yan "
                "omuz haftalık ~4 settir; hipertrofi için kas başına ~10+ ağır set/hafta daha "
                "tutarlı sonuç verir [1,2]. Bu 4 set + Gün 3’teki 3 set ≈ 7 doğrudan set + press "
                "katkısıdır."
            ),
            "cues": (
                "Kolu ~30° önde (‘scaption’), serçe parmak hafif yukarı. 90°yi aşma. Gövde sallanmasın. "
                "Kablo, set boyunca gerilimi kesmez; dumbbell yedektir."
            ),
            "swap": "Seated dumbbell lateral raise, makine lateral. Upright row yok (omuz sıkışması riski, kanıt tartışmalı; gerek yok).",
            "grade": "A (haftalık hacim) + C (deltoid başı EMG). Orta deltoid hipertrofisi için lateral raise’in press’ten üstünlüğünü gösteren büyük RCT yoktur; seçicilik EMG’ye dayanır.",
        },
        {
            "name": "Pec deck veya kablo fly (gerilme vurgulu)",
            "sets": "2",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Pektoralis (uzun kas boyu)",
            "why": (
                "İzolasyon, press’in yetiştiremediği pektoralis hacmini tamamlar (~10 set/hafta "
                "hedefi) [1,2]. Fly’da uyaran, kolların önde birleştiği ‘sıkış’tan çok göğsün "
                "gerildiği açık pozisyondadır; uzun kas boyunda çalışan kısmi/tam ROM, kısa "
                "kas boyundaki kısmi ROM’dan üstündür [9,10]. Tükenişe en yakın set burada "
                "olabilir; makine/kablo, serbest ağırlığa göre daha stabildir [1,6]."
            ),
            "cues": (
                "Dirsek hafif kırık, omuz öne savrulmasın. Gerilmede 1 sn kontrol; tepede kiloları "
                "çakma. 3 sn negatif şart değil; kontrol yeter (TUT tek başına sonucu değiştirmiyor) [1]."
            ),
            "swap": "Cable crossover, dumbbell fly (sadece omuz rahatsa, alt noktada kontrol).",
            "grade": "A (hacim + ROM ilkeleri). Fly vs press hipertrofi farkı net değildir; press zaten vardır, fly hacim ve gerilme için eklenir.",
        },
        {
            "name": "Face pull (ip, yüz hizası)",
            "sets": "3",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Arka deltoid, dış rotatorlar, orta trap",
            "why": (
                "Arkadan sırt düz ve arka omuz silik. Yatay abdüksiyon + dış rotasyon, "
                "glenohumeral ve skapular kaslar için klinik olarak kullanılan bir örüntüdür [28]. "
                "Bu hareketin pektoralis press hacmine karşı ‘omuz sağlığı RCT’si’ yoktur; "
                "gerekçe denge ve arka zincir hacmidir. Hipertrofi kanıtı daha doğrudan olan "
                "yedek, reverse pec deck’tir (Gün 3)."
            ),
            "cues": (
                "İp kulak hizasına, baş ‘gagalanmasın’. Son noktada dış rotasyon (eller kulak arkası "
                "gibi). Bel kayması yok. Ağır yükle momentum yok."
            ),
            "swap": "Reverse pec deck, bent-over reverse fly.",
            "grade": "D/C (klinik omuz literatürü + EMG mantığı). Hipertrofi RCT’si zayıf; programda düşük maliyetli sigorta olarak durur.",
        },
        {
            "name": "Overhead kablo triceps extension",
            "sets": "3",
            "reps": "10–12",
            "rest": "90 sn",
            "rir": "1–2",
            "target": "Triceps, özellikle uzun baş",
            "why": (
                "Orijinal program triceps’i yalnızca pushdown ile (kısa–orta kas boyu) bitirir. "
                "MRI’lı 12 haftalık çapraz-kol çalışmasında, baş üstü dirsek ekstansiyonu nötr "
                "kola göre triceps hacmini belirgin daha fazla artırmıştır (uzun baş +28,5% vs "
                "+19,6%; tüm triceps +19,9% vs +13,9%), üstelik daha düşük mutlak yükle [11]. "
                "Bu, programdaki en doğrudan hipertrofi RCT’sine dayanan izolasyon seçimidir."
            ),
            "cues": (
                "Üst kol kulağın yanında sabit, sadece dirsek uzasın. Bel çukuru artmasın; kaburgalar "
                "inik. Omuz ağrırsa 1 kol ve daha dik açı dene."
            ),
            "swap": "Overhead dumbbell extension (iki el), kablo pushdown yalnızca yedek (Gün 3’te yok; overhead öncelikli).",
            "grade": "B (Maeo 2023, MRI, 12 hafta).",
        },
    ],
}

DAY2 = {
    "title": "5. GÜN 2 — ALT A",
    "sub": "Öncelik: quadriceps, kalça, arka zincir  ·  60–75 dk",
    "intro": (
        "Paylaştığın orijinal programda bacak yoktu. DSÖ ve ACSM, tüm büyük kas gruplarının "
        "haftada en az iki gün çalışmasını ister [1,24]. Squat paterni quadriceps ve addüktörde "
        "hip thrust’tan daha fazla kesit artışı üretmiştir; kalça hipertrofisi ise squat ile "
        "hip thrust arasında benzerdir [13]. Bu gün squat/press paterni, ertesi bacak günü "
        "mentşe + tek bacaktır. Böylece bacak da sırt gibi haftada 2 kez uyarılır [4,5]."
    ),
    "ex": [
        {
            "name": "Leg press (veya goblet / makine squat)",
            "sets": "3",
            "reps": "8–12",
            "rest": "3 dk",
            "rir": "1–3",
            "target": "Quadriceps, glute, addüktör",
            "why": (
                "Geri dönüşte serbest barbell squat zorunlu değildir; ACSM 2026 ekipman türünün "
                "(makine vs serbest) sonuçları tutarlı biçimde değiştirmediğini belirtir [1]. "
                "Leg press, sırtüstü destekle yüksek bacak hacmini bel shear’i azaltarak verir. "
                "Plotkin ve arkadaşlarında squat, kalçada hip thrust kadar büyümüş, uyluk önü ve "
                "addüktörde üstün çıkmıştır [13]. Derin, kontrollü ROM tercih edilir [9]."
            ),
            "cues": (
                "Ayaklar omuz genişliği, parmaklar hafif dış. Alt noktada bel yastıktan kalkmasın. "
                "Dizler parmak yönünde. Kilidi patlatarak çarpma yok."
            ),
            "swap": "Goblet squat, hack squat, smith squat (topuk hafif yüksekse ROM kolaylaşır). "
                    "Barbell back squat ancak bel ve teknik hazırsa.",
            "grade": "A (alt vücut sıklığı/hacmi) + B (squat paterni hipertrofisi, Plotkin 2023).",
        },
        {
            "name": "Romanian deadlift (dumbbell veya bar)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "2–3",
            "target": "Hamstring, glute, erektör",
            "why": (
                "Kalça mentşesi hamstringi uzun kas boyunda yükler; bu, kısa kas boyuna göre "
                "hipertrofi için avantajlı bir koşuldur [9,12]. Fotoğrafta kalça projeksiyonu "
                "zayıf ve pelvis önde duruyor; glute–hamstring kuvveti hem görüntü hem mentşe "
                "kontrolü için gerekir. Bu hareket ‘anterior pelvik tilt’i tedavi ettiğini iddia "
                "etmez; o iddianın kanıtı zayıftır. Amaç hipertrofi ve menteşe becerisidir."
            ),
            "cues": (
                "Diz az kırık ve sabit. Bar/dumbbell bacağı sıyırarak iner, sırt nötr. Gerilmeyi "
                "hamstringde hisset; belde yuvarlama yok. İlk haftalar hafif, RIR 3."
            ),
            "swap": "45° hiperextension (kalça bükerek, belde kırma yok), cable pull-through.",
            "grade": "A (uzun kas boyu) + C/D (mentşe biyomekaniği). RDL vs leg curl hipertrofi RCT’si sınırlıdır; ikisi de programdadır.",
        },
        {
            "name": "Walking lunge veya reverse lunge",
            "sets": "2",
            "reps": "8–10 / bacak",
            "rest": "2 dk",
            "rir": "1–3",
            "target": "Quad, glute, tek bacak kontrolü",
            "why": (
                "Tek bacak squat varyantları, çift bacak squat ile benzer kuvvet–beceri "
                "adaptasyonları üretebilir [26]. Fotoğrafta simetri ve kalça uzantısı için "
                "unilateral iş, bilateral press’in boşluğunu doldurur. Hacim düşük tutulur "
                "(2 set); DOMS’u ilk haftalarda patlatmamak için."
            ),
            "cues": (
                "Adım çok uzun olmasın. Ön diz öne kaçmasın, gövde dik. Denge bozulursa yerinde "
                "reverse lunge’a geç. Dumbbell yanlarda."
            ),
            "swap": "Reverse lunge, step-up (diz yüksekliği kontrolü), goblet split squat.",
            "grade": "B (unilateral vs bilateral, Speirs 2016 — ragbi; hipertrofi ikincil) + A (bacak hacmi).",
        },
        {
            "name": "Leg extension",
            "sets": "2",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Quadriceps (rektus femoris dahil)",
            "why": (
                "Compound squat paterni rektus femorisi (kalça fleksörü olan baş) her zaman "
                "yeterince uzatmaz. Leg extension, dizi izole ederek quad hacmini ~10 set/hafta "
                "hedefine tamamlar [1,2]. Son setler 0–1 RIR olabilir; makine stabildir [6]."
            ),
            "cues": "Sırt yaslı, ayak bileği pad’in arkasında. Üstte 0,5 sn tut, 2 sn indir. Kalça pad’den kalkmasın.",
            "swap": "Yoksa goblet squat’a 1 set ekle. Diz ağrısında ROM’u kısalt, yükü düşür.",
            "grade": "A (hacim tamamlama). Rektus femoris için extension’ın squat’tan üstün olabileceğine dair EMG/bölgesel veriler vardır; bu programda gerekçe hacimdir.",
        },
        {
            "name": "Standing calf raise (tam gerilme)",
            "sets": "3",
            "reps": "10–15",
            "rest": "75–90 sn",
            "rir": "0–2",
            "target": "Gastrocnemius",
            "why": (
                "Orijinal programda calf yok. Kassiano ve arkadaşları, baldırda uzun kas boyundaki "
                "(gerilmiş) kısmi ROM’un tam ROM ve kısa kas boyu kısmisinden daha fazla medial "
                "gastrocnemius büyümesi ürettiğini gösterdi [10]. Pratik çıkarım: topuğu iyice "
                "indir, gerilmeyi kaybetme; sadece parmak ucunda zıplama yapma."
            ),
            "cues": (
                "Basamağın ucunda, diz neredeyse kilit. Altta 1 sn gerilme. Zıplama yok. "
                "Ağırlık dizleri içeri yıkmasın."
            ),
            "swap": "Leg press calf, smith calf. Seated calf Gün 4’te (soleus).",
            "grade": "B (Kassiano 2023, ultrason, 8 hafta) + A (kas grubunu çalıştır).",
        },
        {
            "name": "Plank",
            "sets": "3",
            "reps": "30–45 sn",
            "rest": "60 sn",
            "rir": "—",
            "target": "Anterior core (anti-ekstansiyon)",
            "why": (
                "Karın hareketi bel çevresi yağını yakmaz (spot reduction yok). Crunch/sit-up "
                "lomber kompresyonu yüksek egzersizlerdendir [27]. Plank, omurgayı nötr tutarak "
                "dayanıklılık verir ve orijinal programındaki ‘omurga düz’ notuyla uyumludur. "
                "Rectus hipertrofisi için Gün 4’te düşük yükte kablo crunch vardır; bu günün "
                "işi anti-ekstansiyondur."
            ),
            "cues": (
                "Dirsek omuz altında, kalça ne çökme ne çadır. Kaburga inik. 45 sn kolaysa yük "
                "(plaka sırtta) veya 3-nokta plank; tekrarı 90–120 sn’ye şişirme."
            ),
            "swap": "Dead bug, ab wheel (sadece nötr bel korunursa).",
            "grade": "C (omurga yükü) + D (klinik core). Hipertrofi için plank crunch’tan üstün değildir.",
        },
    ],
}

DAY3 = {
    "title": "6. GÜN 3 — ÜST B  (SIRT & BICEPS ÖNCELİKLİ)",
    "sub": "Öncelik: lat genişliği, dikey press, biceps  ·  65–80 dk  ·  keyif aldığın güne en yakın gün",
    "intro": (
        "Bu gün, yaptığın ve keyif aldığın sırt–biceps şablonunun kanıta göre sadeleştirilmiş "
        "halidir. Lat pulldown tam ROM ile kalır [9,17]. Cheat barbell row, her sette drop, "
        "FST-7 ve ‘agresif tekrar’ çıkarıldı; mekanik gerilim hipertrofinin ana sürücüsüdür, "
        "metabolik şişirme teknikleri eşit hacimde üstün değildir [20,29]. Göğüs bu günde 3 set "
        "makine press ile ikinci kez uyarılır ki sıklık 2x olsun [4,5]."
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
                "V kesiti için en doğrudan dikey çekiş. Orta tutuş (yaklaşık 1,5× omuz genişliği) "
                "ile dar/geniş tutuş arasında lat EMG’si büyük ölçüde benzerdir; orta tutuş biraz "
                "daha yüksek 6RM yük taşır [17]. Orijinal 2. sırt günündeki ‘full stretch yok, "
                "ROM %80’ notu literatürün tersinedir: tam veya uzun ROM, kısa kısmi ROM’dan "
                "üstün veya eşittir [9]. Tükeniş her sette şart değildir [1,6,7]."
            ),
            "cues": (
                "Göğüs açık, hafif geri yat. Bar üst göğse, dirsekler aşağı–arkaya. Tepede kürek "
                "yukarı kaçmadan lat’i esnet. Sallama yok. 2 ısınma seti 10 tekrar hafif."
            ),
            "swap": "Nötr tutuş V-bar pulldown, assisted pull-up. Behind-the-neck pulldown yok.",
            "grade": "A (ROM, sıklık) + C (tutuş EMG). Pulldown vs pull-up hipertrofi farkı pratikte küçük kabul edilir [1].",
        },
        {
            "name": "Göğüs press makinesi (düz veya hafif incline)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5 dk",
            "rir": "1–2",
            "target": "Pektoralis, ön deltoid, triceps",
            "why": (
                "Göğsü haftada ikinci kez uyarmak için. Hacim eşitlendiğinde sıklığın kendisi "
                "sihir değildir ama 2x dağıtım toparlanmayı ve performansını kolaylaştırır [5]. "
                "Makine, yorgun sırt gününde omuz stabilitesini serbest barbell’den daha az "
                "sorgulatır [1]. Partnerli negatif/forced rep yok [6]."
            ),
            "cues": "Kürek arkada, göğüs yukarı. Tam in, kilidi çarpmadan uzat. Omuz öne yuvarlanmasın.",
            "swap": "Dumbbell flat press, Smith press. Dip ancak omuz rahatsa.",
            "grade": "A (sıklık + hacim). Hareket seçimi ekipmandan bağımsız [1].",
        },
        {
            "name": "Tek kol kablo row",
            "sets": "3",
            "reps": "8–10 / kol",
            "rest": "90–120 sn",
            "rir": "1–2",
            "target": "Lat (kalça hizası çekiş), orta sırt",
            "why": (
                "Orijinal programındaki en mantıklı çekişlerden biri; kaldı. Tek kol, sağ–sol "
                "farkını görünür kılar ve gövde rotasyonunu kontrollü anti-rotasyon olarak yükler "
                "[14]. Kablo, hareketin başında (lat uzunken) gerilimi kesmez; bu, uzun kas boyu "
                "ilkesiyle uyumludur [9]. ‘Lat için kambur’ cue’u bel fleksiyonuna çevrilmemeli."
            ),
            "cues": (
                "Göğüs açık, bel nötr. El kalça yanına, dirsek vücuttan geçmesin. Gerilmede omuz "
                "önden kontrolsüz gitmesin. Sol ve sağ ayrı sayılır."
            ),
            "swap": "Tek kol dumbbell row (bench destekli), seated D-handle row.",
            "grade": "A (çekiş hacmi, ROM) + C (tek kol row omurga/torsiyon [14]).",
        },
        {
            "name": "Kablo veya dumbbell lateral raise",
            "sets": "3",
            "reps": "12–15",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Yan deltoid",
            "why": (
                "Yan omuz hacmini ikinci güne yaymak [4]. Coratella ve arkadaşları, lateral raise "
                "varyantlarının orta deltoidi front raise’den daha iyi hedeflediğini gösterdi [16]. "
                "Orijinal omuz günündeki 2 set, bu profil için azdır [2]."
            ),
            "cues": "Gün 1 ile aynı teknik. Yorgunlukta kilosu düşer, form düşmez.",
            "swap": "Makine lateral.",
            "grade": "A + C [16].",
        },
        {
            "name": "Düz kolla kablo pulldown (yüksek kablo)",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Lat / teres (omuz ekstansiyonu)",
            "why": (
                "Orijinal rope pullover’ın sade hali: 2 düz set, drop yok. Uyarı: bench üstünde "
                "barbell pullover EMG’sinde pektoralis latissimus’tan daha aktif bulunmuştur [18]. "
                "Bu yüzden hareket, barı baş arkasına yatırmadan, yüksek kablodan düz kolla aşağı "
                "çekiş (omuz ekstansiyonu) olarak yapılır. Hipertrofi RCT’si yoktur; lat hacmini "
                "tamamlayan aksesuardır. Kanıt yetersizse pulldown’a 1 set eklemek eşdeğerdir."
            ),
            "cues": (
                "Dirsek neredeyse kilit, gövde 15–20° öne. İpi uyluk üstüne indir, lat’i kısalt. "
                "Bel çukuru yok. Drop set yok [20]."
            ),
            "swap": "Ek 1–2 set lat pulldown. Barbell pullover şart değil [18].",
            "grade": "C/D. Barbell pullover EMG’si pektoralis lehinedir [18]; kablo varyantı biyomekanik çıkarım.",
        },
        {
            "name": "Dumbbell supinated curl",
            "sets": "3",
            "reps": "10–12",
            "rest": "75–90 sn",
            "rir": "1–2",
            "target": "Biceps brachii",
            "why": (
                "Çekişler biceps’e dolaylı hacim verir; doğrudan 8–12 set/hafta yeter [2]. "
                "Supinasyon biceps’i nötr/hammer tutuştan daha spesifik yükler. Orijinaldeki 6 "
                "doğrudan set + 2. gün drop’ları fazlaydı; görsel darboğaz biceps değil. "
                "Momentum hipertrofiye mekanik gerilim kaybettirir [29]."
            ),
            "cues": "Dirsek gövde yanında. 1 sn sıkış şart değil. Sallanma yok. Her iki kol simetrik.",
            "swap": "Kablo curl, barbell curl (bilek rahatsa).",
            "grade": "A (hacim). Tutuş farkı büyük ölçüde anatomi/EMG’dir; büyüme RCT’si sınırlı.",
        },
        {
            "name": "Hammer curl",
            "sets": "2",
            "reps": "10–12",
            "rest": "75 sn",
            "rir": "1–2",
            "target": "Brachialis, brachioradialis",
            "why": (
                "Nötr tutuş brachialis ve önkolu öne çıkarır; kol kalınlığına biceps uzun başından "
                "farklı katkı yapar. Orijinaldeki son set drop çıkarılmıştır; drop set eşit "
                "hacimde geleneksel setten üstün hipertrofi vermez, yalnızca zaman kazandırır [20]."
            ),
            "cues": "Başparmak yukarı, dirsek sabit. Drop yok.",
            "swap": "Kablo hammer / rope curl.",
            "grade": "A (hacim, drop set meta-analiz [20]) + C (tutuş anatomisi).",
        },
        {
            "name": "Reverse pec deck veya reverse fly",
            "sets": "2",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "0–2",
            "target": "Arka deltoid",
            "why": (
                "Arka deltoid, row’larda ikinci plandadır. İzole yatay abdüksiyon onu doğrudan "
                "yükler. Face pull (Gün 1) daha çok dış rotasyon/skapula; bu hareket daha doğrudan "
                "hipertrofi izolasyonudur. Toplam arka omuz hacmi row’larla birlikte ~10 sete yaklaşır [2]."
            ),
            "cues": "Kollar hafif kırık, göğüs yastığa. Kürekleri ‘sıkıştırayım’ diye shrugging yok.",
            "swap": "Kablo reverse fly.",
            "grade": "A (izolasyon hacmi) + C (deltoid başı seçiciliği [16]).",
        },
    ],
}

DAY4 = {
    "title": "7. GÜN 4 — ALT B + KARIN",
    "sub": "Öncelik: kalça, hamstring, tek bacak, baldır, karın  ·  60–75 dk",
    "intro": (
        "İkinci bacak günü sıklık ilkesini tamamlar [4,24]. Hip thrust kalça kesitini squat kadar "
        "büyütür ama quad/addüktörde squat kadar işe yaramaz; bu yüzden tek başına bacak günü "
        "değildir, Gün 2’nin tamamlayıcısıdır [13]. Hamstring için oturarak leg curl, yüzüstü "
        "curl’den daha fazla kas hacmi artışı vermiştir [12]."
    ),
    "ex": [
        {
            "name": "Hip thrust (bar, makine veya glute bridge)",
            "sets": "3",
            "reps": "8–12",
            "rest": "2,5–3 dk",
            "rir": "1–2",
            "target": "Gluteus maximus",
            "why": (
                "9 haftalık MRI çalışmasında hip thrust ve back squat, gluteus maximus kesitinde "
                "benzer büyüme verdi; squat quad ve addüktörde öndeydi, kuvvet ise harekete özgüydü "
                "[13]. EMG’si yüksek diye hip thrust ‘daha iyi kalça hareketi’ değildir — büyüme "
                "benzerdir. Fotoğrafta kalça silik olduğu için hem squat paterni hem thrust vardır."
            ),
            "cues": (
                "Kürek bench’te, çene göğüste. Üstte kalça tam açılır, bel aşırı çukurlaşmaz. "
                "İtme topukla. Pad kalça kemiğinde."
            ),
            "swap": "Makine hip thrust, tek bacak glute bridge, kablo kickback (yalnızca thrust yoksa, daha zayıf yedek).",
            "grade": "B (Plotkin 2023, MRI).",
        },
        {
            "name": "Oturarak leg curl (seated)",
            "sets": "3",
            "reps": "10–12",
            "rest": "90–120 sn",
            "rir": "0–2",
            "target": "Hamstring (uzun kas boyu)",
            "why": (
                "Kalça fleksiyondayken (oturarak) biartiküler hamstringler daha uzundur. 12 haftalık "
                "MRI çalışmasında seated curl, prone curl’e göre tüm hamstring hacmini daha fazla "
                "artırdı (+14% vs +9%) [12]. Yüzüstü curl yok değil, seated tercih."
            ),
            "cues": "Kalça oturağa yapışık. Tam uzat, kontrollü bük. Bel pad’den kalkmasın.",
            "swap": "Lying curl yalnızca seated yoksa. Nordic (ileri düzey, yüksek DOMS) şart değil.",
            "grade": "B (Maeo 2021, MRI, 12 hafta).",
        },
        {
            "name": "Bulgarian split squat",
            "sets": "3",
            "reps": "8–10 / bacak",
            "rest": "2 dk",
            "rir": "1–3",
            "target": "Quad, glute, denge",
            "why": (
                "Tek bacak squat, akademi ragbi oyuncularında çift bacak squat ile karşılaştırılabilir "
                "kuvvet ve sprint/agility katkısı vermiştir [26]. Bireysel fotoğrafta unilateral iş, "
                "sağ–sol farkı ve kalça uzantısı için ikinci bacak gününün compound’udur. İlk 2 hafta "
                "goblet ile öğren, sonra dumbbell."
            ),
            "cues": (
                "Arka ayak düşük bench’te, gövde hafif öne. Ön diz öne savrulmasın. 10 cm’lik adım "
                "farkı diz vs kalça vurgusunu değiştirir; diz rahatsa gövdeyi biraz daha öne al."
            ),
            "swap": "Reverse lunge, step-up. Denge çok bozulursa TRX / tutunarak split squat.",
            "grade": "B (Speirs 2016; hipertrofi birincil sonlanım değil) + A (bacak sıklığı).",
        },
        {
            "name": "Seated calf raise",
            "sets": "3",
            "reps": "12–15",
            "rest": "75 sn",
            "rir": "0–2",
            "target": "Soleus (diz bükülü)",
            "why": (
                "Diz bükülüyken gastrocnemius gevşer, soleus öne çıkar (anatomi). Gün 2 standing "
                "gastrocnemius, bu gün soleus. Baldır da diğer kaslar gibi haftada 2 uyaran ister [4]. "
                "Alt noktada gerilme korunur [10]."
            ),
            "cues": "Tam in, zıplama yok. Üstte 0,5 sn. Ağırlıkla form bozulmasın.",
            "swap": "Standing calf’ın 2. varyantı, diz 20–30° kırık tutulursa.",
            "grade": "A (sıklık) + B (uzun kas boyu baldır [10]) + anatomi (soleus).",
        },
        {
            "name": "Kablo crunch",
            "sets": "2",
            "reps": "12–15",
            "rest": "60–75 sn",
            "rir": "1–3",
            "target": "Rectus abdominis",
            "why": (
                "Orijinal 3×20 ağır olmayan crunch makul; 2×12–15’e çekildi çünkü bel çevresi "
                "yağ kaybı crunch hacmiyle olmaz [23]. Hipertrofi için orta yük, omurga fleksiyanı "
                "kalçadan değil kaburgayı pelvis’e yaklaştırarak yapılır. Sit-up tipi yüksek "
                "kompresyonlu varyantlardan kaçın [27]. Asla ağır ‘ego’ crunch yok — orijinal not doğru."
            ),
            "cues": "Kalça sabit, hareket göğüs kemiğini kasığa yaklaştırmak. Boyun çekilmesin.",
            "swap": "Machine crunch. Sit-up / straight-leg throw-down yok.",
            "grade": "C (omurga yükü [27]) + A (karın da bir kastır ama spot reduction yok).",
        },
        {
            "name": "Lying leg raise (kontrollü)",
            "sets": "2",
            "reps": "10–15",
            "rest": "60–75 sn",
            "rir": "1–3",
            "target": "Alt rectus, kalça fleksörleri",
            "why": (
                "Orijinal programdaki 3. karın hareketi sadeleştirilerek kaldı. Bacak yere "
                "bırakılmadan gerilim korunur (orijinal not). Asıl bel-inceltme aracı bu değildir; "
                "haftalık adım ve enerji dengesi bel çevresini değiştirir [23,24]."
            ),
            "cues": "Eller kalça altında. Bel yere basılı. Bacak inerken yere değmeden dur. Sallanma yok.",
            "swap": "Captain’s chair knee raise. Bel ağırsa dead bug.",
            "grade": "D/C. Karın hipertrofisi için yeterli; yağ kaybı iddiası yok.",
        },
    ],
}

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
            "<b>lat genişliği, yan deltoid, bacak ve kalça, üst sırt kalınlığı</b>. Biceps görsel darboğaz değil; "
            "bu yüzden orijinal 6–8 curl seti kısaltıldı."
        )
    )
    story.append(
        simple_table(
            ["Öncelik", "Neden (fotoğraf)", "Programdaki cevap", "Ana kaynak"],
            [
                [
                    "Bacak + kalça",
                    "Şort hattı dolgun değil; orijinal programda yok",
                    "Haftada 2 alt vücut günü",
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
            "<b>Neden üst/alt 4 gün, neden 4× üst vücut değil?</b> Hipertrofi meta-analizleri kası "
            "haftada en az 2 kez çalıştırmayı destekler; hacim eşitlenince sıklığın kendisi küçük "
            "kalır ama 2x dağıtım yüksek hacmi taşınabilir kılar [4,5]. Orijinal 4 üst gün bacağı "
            "0×, sırtı 30+ sete çıkarıyordu. ACSM hipertrofi için kas başına kabaca ≥10 set/hafta "
            "der [1,30]; 30+ sırt seti geri dönüşte toparlanmayı bozar. Upper/lower her büyük grubu "
            "2× vurur ve salon gününü 4’te tutar."
        )
    )

    story.append(
        KeepTogether(
            [
                simple_table(
                    ["Gün", "Odak", "Örnek yerleşme"],
                    [
                        ["1  Üst A", "Göğüs, yan omuz, row", "Pazartesi"],
                        ["2  Alt A", "Leg press, RDL, lunge, calf, plank", "Salı"],
                        ["—", "İstirahat + yürüme", "Çarşamba"],
                        ["3  Üst B", "Pulldown, press, row, biceps", "Perşembe"],
                        ["4  Alt B", "Hip thrust, seated curl, split squat, karın", "Cuma"],
                        ["—", "İstirahat, adım hedefi", "Cmt–Paz"],
                    ],
                    [40 * mm, 78 * mm, 60 * mm],
                ),
                Spacer(1, 2 * mm),
                P(
                    "Beşinci gün şart değil. Tutarsız 6 gün, tutarlı 4 günden kötüdür [1,30]. İstersen "
                    "hafta sonuna 30–40 dk tempolu yürüyüş ekle, ekstra FST-7 ekleme [31]."
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
            "Her gün ≈ 16–20 çalışma seti. Bu, geri dönüş için yüksek ama orijinal FST-7’li sırt "
            "gününden düşük ve toparlanabilir bir banttır [2,3]. Setler arası telefon molası yok; "
            "süre 90 dakikayı geçerse izolasyonu kes, compound’u tut."
        )
    )

    story += day_story(DAY1)
    story += day_story(DAY2)
    story += day_story(DAY3)
    story += day_story(DAY4)

    # --- Salon karti ---
    story.append(heading_bar("8. Salon kartı", "Telefona indirip salonda açmak için — yalnızca set/tekrar"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "Aşağıdaki dört tablo, gerekçe metinleri olmadan tüm programdır. RIR ve dinlenme "
            "bölüm 3’teki kurallara uyar. Isınma setleri yazılmaz."
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

    compact("Gün 1 — Üst A (göğüs / yan omuz / row)", DAY1["ex"])
    compact("Gün 2 — Alt A (quad / mentşe)", DAY2["ex"])
    compact("Gün 3 — Üst B (sırt / biceps / press)", DAY3["ex"])
    compact("Gün 4 — Alt B (kalça / hamstring / karın)", DAY4["ex"])

    # --- Hacim ozeti ---
    story.append(heading_bar("9. Haftalık çalışma seti özeti", "Isınma setleri hariç, doğrudan + büyük katkı"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        simple_table(
            ["Kas", "Doğrudan set/hafta", "Hedef bant [1–3]", "Not"],
            [
                ["Lat / üst sırt", "11–14", "10–16", "Pulldown, row, pulldown-aksesuar"],
                ["Göğüs", "10", "8–12", "Incline 3 + fly 2 + press 3"],
                ["Yan deltoid", "7 + press", "8–12", "İlk 8 hafta 7 yeter; sonra +1 set"],
                ["Arka deltoid", "5 + row", "6–10", "Face pull + reverse pec deck"],
                ["Triceps", "3 + press", "6–10", "Overhead öncelikli [11]"],
                ["Biceps", "5 + çekiş", "8–12", "Görsel öncelik değil"],
                ["Quadriceps", "10–11", "10–14", "Leg press, lunge, extension, BSS"],
                ["Glute", "9–12", "8–12", "Thrust + RDL + lunge + BSS + press"],
                ["Hamstring", "6 + mentşe", "8–12", "Seated curl tercih [12]"],
                ["Calf", "6", "6–10", "Standing + seated, gerilme [10]"],
                ["Karın", "7", "4–10", "Yağ kaybı aracı değil [23]"],
            ],
            [32 * mm, 38 * mm, 32 * mm, 76 * mm],
        )
    )
    story.append(Spacer(1, 2.2 * mm))
    story.append(
        P(
            "Antrenmanlı erkeklerde 18–30 setlik üst bantlar da büyümeyi artırabilmiştir [3]; bu, "
            "‘daha fazla her zaman daha iyi’ demek değildir. Geri dönüşte 10–16 doğrudan set, 30+ "
            "sırt setinden daha sürdürülebilir bir dozdur [2,3]."
        )
    )

    # --- Orijinalden cikanlar ---
    story.append(heading_bar("10. Orijinal programdan ne çıktı, neden?", "Aynı keyif, daha az risk, eşit veya daha iyi uyaran"))
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
                    "Sadece üst vücut haftası",
                    "Büyük kas grupları (bacak dahil) ≥2 gün/hafta.",
                    "[1,24]",
                ],
            ],
            [42 * mm, 96 * mm, 40 * mm],
        )
    )

    # --- Beslenme ---
    story.append(heading_bar("11. Beslenme ve adım", "Fotoğrafı antrenmandan hızlı değiştiren kısım"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "<b>Protein.</b> ISSN, çoğu sporcu için 1,4–2,0 g/kg/gün yeterli der [22]. Morton "
            "meta-analizi, direnç antrenmanıyla birlikte ≈1,6 g/kg civarında kas/kuvvet kazancının "
            "plato bölgesine yaklaştığını gösterir [21]. Diyet döneminde yağsız kütleyi korumak "
            "için ISSN 2,3–3,1 g/kg yağsız kitleye kadar çıkmayı tartışır [22]; pratikte "
            "<b>1,6–2,2 g/kg vücut ağırlığı</b> bu profil için yeterli bir hedeftir. Öğün başına "
            "20–40 g kaliteli protein [22]."
        )
    )
    story.append(
        P(
            "<b>Enerji dengesi.</b> Bel çevresi yumuşak dokusu crunch ile seçilerek yakılmaz. "
            "ACSM 2009: 150–250 dk/hafta orta şiddetli aktivite kilo alımını önler, tek başına "
            "zayıf bir kayıp verir; klinik anlamlı kayıp genelde >250 dk/hafta veya diyetle "
            "birlikte gelir [23]. Geri dönüşte agresif açık, hem toparlanmayı hem sırt antrenmanının "
            "keyfini bozar. <b>İlk 8–12 hafta: idame veya günde ≈200–400 kcal açık</b>, protein yüksek, "
            "antrenman ilerliyor. Haftalık tartı ±0,25–0,5 kg düşüş makul bir banttır."
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
    story.append(heading_bar("12. 8 haftalık takip", "Ayna pump’ı değil, sayı"))
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

    story.append(heading_bar("13. Mini ısınma ve seans içi düzen", "Uygulama detayı"))
    story.append(Spacer(1, 3 * mm))
    story.append(
        P(
            "<b>Üst günler:</b> kol çemberi 10+10, 1 hafif pulldown veya band face pull, ardından rampa. "
            "<b>Alt günler:</b> 5 dk bike, 1 set bodyweight squat, 1 hafif RDL. Ağrı varsa (keskin, tek taraflı, "
            "yayılan) o hareketi yedeğe al; ‘acıyı sev’ uygulaması değildir."
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
    story.append(heading_bar("14. Kaynakça", "Köşeli parantezler bu listeye karşılık gelir"))
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
            "Özet: 4 gün, her büyük kas 2 kez, kas başına kabaca 10+ ağır set, 8–15 tekrar, "
            "RIR 1–3, tam/uzun ROM, 2–3 dk compound dinlenme, cheat/FST-7/drop şovu yok, bacak var, "
            "yan omuz ve lat öncelikli, protein 1,6–2,2 g/kg, bel için açık + adım. Bu cümlelerin her "
            "biri yukarıdaki A veya B kanıta bağlanır. Hareket markası (şu makine vs bu kablo) ise "
            "çoğunlukla C/D’dir ve ACSM’nin de söylediği gibi ikincildir [1].",
            178 * mm,
            HexColor("#EAF2EA"),
            GREEN,
            title="Tek paragraf özet",
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        P(
            "Hazırlanış: Eylül 2026. Kişisel fotoğraf + kullanıcının uyguladığı sırt–biceps şablonu "
            "üzerinden bireyselleştirildi. Genel popülasyon kılavuzu olarak kopyalanmamalı.",
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
        subject="4 günlük üst/alt hipertrofi programı ve kaynakçalı gerekçeler",
    )
    doc.build(build_story(), onFirstPage=cover_page, onLaterPages=header_footer)
    print("Wrote", out)


if __name__ == "__main__":
    main()
