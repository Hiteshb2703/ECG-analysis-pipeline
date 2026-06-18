# pdf_report.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import numpy as np

def header_footer(canvas, doc):
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(40, 820, "ECG Diagnostic Report")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(550, 20, f"Page {doc.page}")

def create_ecg_report(features, interpretation_text, plot_path=None, filename="ECG_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=60,
        bottomMargin=40,
        onFirstPage=header_footer,
        onLaterPages=header_footer
    )
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SectionTitle", fontSize=13, leading=16, spaceAfter=6, spaceBefore=12, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="NormalText", fontSize=10, leading=13))

    story = []
    story.append(Paragraph("Patient Information", styles["SectionTitle"]))

    patient_table_data = [
        ["Name:", features.get("patient_name", "N/A"), "Age:", features.get("patient_age", "N/A")],
        ["Date:", datetime.now().strftime("%d-%m-%Y"), "ID:", features.get("patient_id", "N/A")],
    ]

    patient_table = Table(patient_table_data, colWidths=[50, 150, 40, 120])
    patient_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("ECG Features", styles["SectionTitle"]))

    feature_data = [["Feature", "Value"]]
    for k, v in features.items():
        if k.startswith("patient_"):
            continue
        if k in ["RR_intervals_s", "QRS_widths_s", "ST_intervals_s"]:
            continue
        feature_data.append([k.replace("_", " ").title(), str(v)])

    def safe_val(arr, func):
        return func(arr) if len(arr) > 0 and not np.all(np.isnan(arr)) else 0.0

    feature_data.append(["RR Intervals (s)", f"Mean: {safe_val(features.get('RR_intervals_s', []), np.mean):.3f}"])
    feature_data.append(["QRS Widths (s)", f"Mean: {safe_val(features.get('QRS_widths_s', []), np.mean):.3f}"])
    feature_data.append(["ST Intervals (s)", f"Mean: {safe_val(features.get('ST_intervals_s', []), np.nanmean):.3f}"])
    feature_table = Table(feature_data, colWidths=[200, 200])
    feature_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (1,1), (-1,-1), [colors.whitesmoke, colors.lightyellow]),
        ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
    ]))

    story.append(feature_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("Automated Interpretation", styles["SectionTitle"]))

    for line in interpretation_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        story.append(Paragraph(line, styles["NormalText"]))
        story.append(Spacer(1, 4))

    if plot_path:
        story.append(Paragraph("ECG Waveform", styles["SectionTitle"]))
        story.append(Image(plot_path, width=500, height=200))
        story.append(Spacer(1, 20))

    doc.build(story)
    print(f"PDF saved as: {filename}")
