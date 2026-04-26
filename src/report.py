from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(username, prediction, suggestions):
    file_name = f"{username}_report.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Student Report for {username}", styles['Title']))
    content.append(Paragraph(f"Predicted GPA: {prediction}", styles['Normal']))

    content.append(Paragraph("Recommendations:", styles['Heading2']))

    for s in suggestions:
        content.append(Paragraph(f"- {s}", styles['Normal']))

    doc.build(content)

    return file_name