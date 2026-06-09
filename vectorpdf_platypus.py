
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

def create_platypus_pdf(output_path ="sample_files/Doc.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize = A4, leftMargin = 2*cm,rightMargin = 2*cm, topMargin = 2*cm, bottomMargin = 2*cm)
    style = getSampleStyleSheet()
    story =[]
    story.append(Paragraph("Vector PDF Document", style["Title"]))

    para1 = """Artificial intelligence is transforming the way we interact with technology and
the world around us. From voice assistants that understand natural language to
recommendation systems that predict our preferences, AI has become deeply embedded
in our daily lives. Machine learning algorithms now power everything from medical
diagnosis tools to autonomous vehicles, enabling machines to learn from data and
make decisions with minimal human intervention."""

    para2 = """The history of artificial intelligence dates back to the 1950s, when pioneers like
Alan Turing began exploring the concept of machine intelligence. Turing proposed
his famous test as a measure of machine intelligence, asking whether a machine
could exhibit behavior indistinguishable from a human. Since then, the field has
evolved dramatically, moving from simple rule-based systems to complex neural
networks capable of recognizing patterns in vast amounts of data."""

    para3 = """Deep learning, a subset of machine learning, has been particularly revolutionary.
Inspired by the structure of the human brain, deep neural networks consist of
multiple layers of interconnected nodes that process information in increasingly
abstract ways. These networks have achieved remarkable results in areas such as
image recognition, natural language processing, and game playing, often
surpassing human level performance on specific tasks."""

    para4 = """Despite these advances, artificial intelligence still faces significant challenges.
Questions about bias, fairness, transparency and accountability remain at the
forefront of AI research and policy discussions. As AI systems become more
powerful and pervasive, ensuring they are safe, ethical and beneficial to all
of humanity becomes increasingly important and complex."""

    paragraph = [para1,para2,para3,para4]
    for p in paragraph:
        story.append(Paragraph(p, style["Normal"]))
    doc.build(story)
    print(f"Created: {output_path}")
create_platypus_pdf()


