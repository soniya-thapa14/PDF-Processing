from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors

def create_table(output_path = "sample_files/table.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize = A4, leftmargin = 2*cm, rightmargin = 2*cm, topmargin =2*cm, bottommargin = 2*cm)
    style = getSampleStyleSheet()
    story =[]
    story.append(Paragraph("Monthly Sales Report", style["Title"]))
    story.append(Spacer(1,14))

    data = [
        ["Region", "Sales", "Customers", "Growth"],
        ["North", "$18,000", "50", "45%"],
        ["South", "$14,500", "39", "5%"],
        ["East", "$7,200", "25", "15%"],
        ["West", "$5,230", "13", "8%"],
        ["Total", "$45,230", "128", "23%"],
    ]

    table = Table(data, colWidths =[4*cm,4*cm,4*cm,4*cm])

    table.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 12),

        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1), (-1,-1), 10),


        ("GRID",        (0,0), (-1,-1),0.5, colors.black),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))

    story.append(table)
    doc.build(story)
    print(f"Created: {output_path}")
create_table()


