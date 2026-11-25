
import csv
import io

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.services.report_service import (
    get_production_report,
    get_quality_report
)


def export_report_csv(db):
    production = get_production_report(db)
    quality = get_quality_report(db)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Metric", "Value"])

    for key, value in production.items():
        writer.writerow([key, value])

    for key, value in quality.items():
        writer.writerow([key, value])

    return output.getvalue()


def export_report_pdf(db):
    production = get_production_report(db)
    quality = get_quality_report(db)

    output = io.BytesIO()

    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setTitle("Food Plant Operations Report")

    pdf.drawString(50, 800, "Food Plant Operations Report")
    pdf.drawString(50, 765, "Production Report")

    y = 735

    for key, value in production.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 25

    y -= 20

    pdf.drawString(50, y, "Quality Report")
    y -= 30

    for key, value in quality.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 25

    pdf.save()

    output.seek(0)

    return output.getvalue()
