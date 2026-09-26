# Kanıta Dayalı Hipertrofi Programı

Tek dosyalık PDF: 4 günlük üst/alt program, her hareketin gerekçesi, salon kartı ve numaralı kaynakça.

## Dosya

- [`Kanita_Dayali_Hipertrofi_Programi.pdf`](Kanita_Dayali_Hipertrofi_Programi.pdf) — dağıtılacak belge
- [`generate_pdf.py`](generate_pdf.py) — PDF üreticisi (ReportLab + DejaVu)

## Yeniden üretmek

```bash
python3 generate_pdf.py
```

Gerekenler: `reportlab`, sistemde DejaVu Sans/Serif (`/usr/share/fonts/truetype/dejavu/`).
