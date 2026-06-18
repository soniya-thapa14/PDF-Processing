"""Generate a ~45 page vector PDF replicating a city zoning/development ordinance."""

import os
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "zoning_ordinance.pdf")

random.seed(42)

ZONE_DISTRICTS = [
    "RS-1 (Residential Single-Family Low Density)",
    "RS-2 (Residential Single-Family Medium Density)",
    "RM-6 (Residential Multi-Family)",
    "RM-16 (Residential Multi-Family High Density)",
    "CB (Community Business)",
    "HB (Highway Business)",
    "CI (Commercial-Industrial)",
    "LI (Light Industrial)",
    "HI (Heavy Industrial)",
    "INST (Institutional)",
    "O (Office)",
    "UV (Urban Village)",
    "RB (Regional Business)",
    "NC (Neighborhood Corridor)",
    "EXP (Expansion)",
]

USES = [
    "single-family dwelling", "two-family dwelling", "multi-family dwelling",
    "accessory dwelling unit", "group home", "nursing home",
    "retail sales", "restaurant", "office", "medical clinic",
    "day care center", "place of worship", "school",
    "hotel/motel", "gas station", "auto repair",
    "light manufacturing", "warehouse", "outdoor storage",
    "parking structure", "mixed-use development", "planned unit development",
]

DEFINITIONS = [
    ("Accessory Structure", "A structure detached from and subordinate to the principal structure on the same lot, customarily incidental to the principal use."),
    ("Adaptive Reuse", "The renovation and reuse of pre-existing buildings for new purposes, including conversion of non-residential structures to residential use."),
    ("Base Flood Elevation (BFE)", "The computed elevation to which floodwater is anticipated to rise during the base flood, as shown on the Flood Insurance Rate Map."),
    ("Buffer", "An area of land, together with a specified type and amount of planting thereon, and any structures required between land uses to eliminate or minimize conflicts."),
    ("Building Coverage", "The percentage of a lot area covered by the footprint of all buildings and structures on the lot, measured from the exterior walls."),
    ("Building Height", "The vertical distance from the average finished grade at the building perimeter to the highest point of the roof for flat roofs, or to the mean height between eaves and ridge for pitched roofs."),
    ("Conditional Use", "A use that is permitted in a zoning district only upon showing that such use in a specified location will comply with all conditions and standards."),
    ("Density", "The number of dwelling units per acre of land developed or used for residential purposes, calculated on net buildable area."),
    ("Development", "Any man-made change to improved or unimproved real estate, including but not limited to buildings, mining, dredging, filling, grading, paving, excavation, or drilling."),
    ("Dwelling Unit", "A single unit providing complete, independent living facilities for one or more persons, including permanent provisions for living, sleeping, eating, cooking, and sanitation."),
    ("Easement", "A grant of one or more property rights by the property owner to or for the use by the public, a corporation, or another person or entity."),
    ("Facade", "The exterior wall of a building exposed to public view, or that wall viewed by persons not within the building."),
    ("Floor Area Ratio (FAR)", "The ratio of the total floor area of all buildings on a lot to the total area of the lot."),
    ("Frontage", "The portion of a lot abutting a public street or right-of-way, measured along the street line."),
    ("Grade, Finished", "The final elevation of the ground surface after development, conforming to the approved grading plan."),
    ("Greenway", "A linear open space established along either a natural corridor, such as a riverfront or stream valley, or overland along a defined route."),
    ("Hardship", "A condition peculiar to the property in question that would deny the property owner all reasonable use of the land if the literal provisions of the ordinance were applied."),
    ("Impervious Surface", "Any material that substantially reduces or prevents the infiltration of stormwater into previously undeveloped land, including buildings, roads, and parking areas."),
    ("Infill Development", "Development of vacant or underutilized parcels within existing developed areas that are already largely served by infrastructure."),
    ("Junkyard", "Any land or structure used for the storage, collection, processing, purchase, sale, or abandonment of waste materials, scrap metals, or discarded goods."),
    ("Landscape Buffer", "A strip of land with a specified width and planted with trees, shrubs, and groundcover to provide a visual and physical separation."),
    ("Lot Coverage", "The total horizontal area within the lot lines of a lot that is covered by any building, structure, or impervious surface."),
    ("Mixed-Use Development", "A single building or development containing more than one type of land use, or a single development of more than one building with more than one type of use."),
    ("Nonconforming Use", "Any building, structure, or use of land lawfully existing at the time of adoption of this ordinance that does not conform to the current regulations."),
    ("Open Space", "Land area not covered by buildings, parking areas, driveways, or other impervious surfaces, which is available for recreation, landscaping, or natural resource preservation."),
    ("Planned Unit Development (PUD)", "A development designed and built as a unified project, with a comprehensive development plan, allowing flexibility in lot sizes, setbacks, and building placement."),
    ("Quasi-Judicial Decision", "A decision involving the application of adopted standards to specific facts, made through an evidentiary hearing process."),
    ("Right-of-Way", "A strip of land acquired by reservation, dedication, prescription, or condemnation and intended to be occupied by a road, trail, water line, or other public use."),
    ("Setback", "The minimum distance by which any building or structure must be separated from a lot line, measured perpendicularly from the lot line."),
    ("Site Plan", "A scaled drawing and supporting text showing the relationship between lot lines and the existing or proposed uses, buildings, and structures."),
    ("Special Flood Hazard Area", "The land in the floodplain subject to a one percent or greater chance of flooding in any given year, designated as Zone A or Zone V on FIRM maps."),
    ("Stormwater Management", "The collection, conveyance, storage, treatment, and disposal of stormwater runoff in a manner to prevent accelerated channel erosion and flooding."),
    ("Tree Canopy", "The area of ground covered by the spread of the branches and leaves of a tree, measured at the drip line."),
    ("Urban Growth Boundary", "A mapped line that delineates the area around an urban area within which urban growth shall be encouraged and outside of which urban growth shall not occur."),
    ("Variance", "Permission to depart from the literal requirements of this ordinance where strict enforcement would cause undue hardship owing to circumstances unique to the property."),
    ("Watershed Protection District", "An overlay zoning district applied to lands draining to public water supply reservoirs and intake points, imposing additional development restrictions."),
]


def generate_legal_paragraph(min_sentences=3, max_sentences=8):
    """Generate realistic-looking zoning ordinance text."""
    templates = [
        "No {use} shall be permitted within {dist} feet of any {boundary} in the {zone} district unless a conditional use permit has been obtained pursuant to Section 7-{a}-{b}.",
        "The minimum lot area for any {use} in the {zone} district shall be {area} square feet, with a minimum lot width of {width} feet measured at the building setback line.",
        "All structures shall maintain a minimum front yard setback of {front} feet, a side yard setback of {side} feet on each side, and a rear yard setback of {rear} feet from the respective lot lines.",
        "Building height in the {zone} district shall not exceed {height} feet or {stories} stories, whichever is less, except as provided in Sec. 7-{a}-{b}(c)({n}).",
        "Off-street parking shall be provided at a ratio of {ratio} spaces per {unit} of {measure}, calculated in accordance with the standards set forth in Article {art}.",
        "Prior to the issuance of any building permit, the applicant shall submit a site plan prepared in accordance with Sec. 7-{a}-{b} demonstrating compliance with all applicable dimensional requirements.",
        "Any nonconforming {use} that has been discontinued for a continuous period of {months} months or more shall not thereafter be reestablished, and any future use of such premises shall conform to this chapter.",
        "The Board of Adjustment may authorize a variance from the strict application of this section upon finding that all of the following conditions are met pursuant to Sec. 7-11-{b}(a).",
        "Landscaping shall be installed in accordance with the approved landscape plan prior to the issuance of a certificate of occupancy, or a performance guarantee shall be posted as provided in Sec. 7-{a}-{b}.",
        "The maximum impervious surface coverage in the {zone} district shall not exceed {coverage} percent of the gross lot area, inclusive of all buildings, parking areas, and other impervious surfaces.",
        "Where a buffer is required between a {use} and an adjacent residential district, such buffer shall have a minimum width of {width} feet and shall be planted in accordance with the Type {type} buffer standards.",
        "No certificate of occupancy shall be issued until the Zoning Administrator has verified that all conditions of approval imposed by the decision-making body have been satisfied in full.",
        "Development within the Watershed Protection Overlay District shall comply with the additional restrictions set forth in Sec. 7-{a}-{b}, including limitations on impervious surface and built-upon area.",
        "The Planning and Zoning Commission shall review all applications for conditional use permits and shall approve, approve with conditions, or deny such applications based on the criteria in Sec. 7-{a}-{b}.",
        "Accessory structures shall not exceed {height} feet in height, shall not be located in any required front yard or side yard, and shall maintain a minimum rear yard setback of {rear} feet.",
        "Fences and walls in residential districts shall not exceed {height_fence} feet in height in front yards and {height_rear} feet in height in side and rear yards, measured from finished grade.",
        "Signs shall comply with the provisions of Article {art}, and no sign shall be erected, altered, or relocated without first obtaining a sign permit from the Zoning Administrator.",
        "Home occupations shall be clearly incidental and secondary to the use of the dwelling for residential purposes, and shall comply with all performance standards in Sec. 7-{a}-{b}(d).",
        "The Technical Review Committee shall review all major subdivision and site plan applications for compliance with this chapter and all other applicable city standards prior to consideration by the Planning Commission.",
        "Stormwater management facilities shall be designed to control the post-development peak discharge rate to the pre-development rate for the 2-year, 10-year, and 25-year storm events.",
    ]
    num = random.randint(min_sentences, max_sentences)
    sentences = []
    for _ in range(num):
        tmpl = random.choice(templates)
        text = tmpl.format(
            use=random.choice(USES),
            dist=random.choice([25, 50, 75, 100, 150, 200, 300]),
            boundary=random.choice(["property line", "lot line", "street centerline", "residential zone boundary"]),
            zone=random.choice(ZONE_DISTRICTS).split(" ")[0],
            area=random.choice([5000, 7500, 10000, 15000, 20000, 43560]),
            width=random.choice([50, 60, 70, 80, 100, 150]),
            front=random.choice([15, 20, 25, 30, 35]),
            side=random.choice([5, 8, 10, 12, 15]),
            rear=random.choice([15, 20, 25, 30, 35]),
            height=random.choice([35, 40, 45, 50, 60, 75]),
            stories=random.choice([2, 3, 4, 5, 6]),
            ratio=random.choice(["1", "1.5", "2", "3", "4", "5"]),
            unit=random.choice(["1,000 square feet", "dwelling unit", "guest room", "seat", "employee"]),
            measure=random.choice(["gross floor area", "net leasable area", "lot area"]),
            art=random.choice(["5", "6", "7", "8", "9", "10"]),
            a=random.randint(2, 11),
            b=random.randint(1, 8),
            n=random.randint(1, 5),
            months=random.choice([6, 12, 18, 24]),
            coverage=random.choice([24, 30, 36, 50, 60, 70, 80]),
            type=random.choice(["A", "B", "C", "D"]),
            height_fence=random.choice([3, 4]),
            height_rear=random.choice([6, 7, 8]),
        )
        sentences.append(text)
    return " ".join(sentences)


def build_styles():
    """Create document styles."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='TitlePage',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=12,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name='ArticleHeading',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=24,
        spaceAfter=12,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name='SubsectionHeading',
        parent=styles['Heading3'],
        fontSize=11,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name='BodyJustified',
        parent=styles['BodyText'],
        alignment=TA_JUSTIFY,
        spaceBefore=4,
        spaceAfter=4,
        firstLineIndent=24,
    ))
    styles.add(ParagraphStyle(
        name='IndentedItem',
        parent=styles['BodyText'],
        leftIndent=36,
        spaceBefore=2,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='DeepIndent',
        parent=styles['BodyText'],
        leftIndent=72,
        spaceBefore=2,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='DefinitionTerm',
        parent=styles['BodyText'],
        fontName='Helvetica-Bold',
        spaceBefore=6,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='DefinitionBody',
        parent=styles['BodyText'],
        leftIndent=24,
        spaceBefore=0,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
    ))
    return styles


ARTICLES = [
    {
        "title": "GENERAL PROVISIONS",
        "sections": [
            "Title and Authority",
            "Purpose and Intent",
            "Jurisdiction and Applicability",
            "Relationship to Other Regulations",
            "Severability",
            "Effective Date",
        ],
    },
    {
        "title": "ZONING DISTRICTS ESTABLISHED",
        "sections": [
            "Establishment of Districts",
            "Zoning Map",
            "District Boundaries",
            "Annexed Territory",
            "Overlay Districts",
            "Planned Development Districts",
            "Special Purpose Districts",
        ],
    },
    {
        "title": "RESIDENTIAL DISTRICTS",
        "sections": [
            "Purpose of Residential Districts",
            "RS-1 Single-Family Low Density",
            "RS-2 Single-Family Medium Density",
            "RM-6 Multi-Family District",
            "RM-16 Multi-Family High Density",
            "Dimensional Requirements",
            "Accessory Uses and Structures",
            "Home Occupations",
        ],
    },
    {
        "title": "COMMERCIAL AND BUSINESS DISTRICTS",
        "sections": [
            "Purpose of Commercial Districts",
            "CB Community Business District",
            "HB Highway Business District",
            "O Office District",
            "NC Neighborhood Corridor District",
            "RB Regional Business District",
            "Performance Standards",
        ],
    },
    {
        "title": "INDUSTRIAL DISTRICTS",
        "sections": [
            "Purpose of Industrial Districts",
            "LI Light Industrial District",
            "HI Heavy Industrial District",
            "CI Commercial-Industrial District",
            "EXP Expansion District",
            "Performance Standards for Industrial Uses",
        ],
    },
    {
        "title": "USE REGULATIONS",
        "sections": [
            "Table of Permitted Uses",
            "Conditional Uses",
            "Accessory Uses",
            "Temporary Uses",
            "Nonconforming Uses",
            "Nonconforming Structures",
            "Change of Use",
            "Abandonment and Discontinuance",
        ],
    },
    {
        "title": "DEVELOPMENT STANDARDS",
        "sections": [
            "Off-Street Parking Requirements",
            "Landscaping and Screening",
            "Signs",
            "Lighting Standards",
            "Stormwater Management",
            "Tree Protection",
            "Hillside Development Standards",
        ],
    },
    {
        "title": "ADMINISTRATION AND ENFORCEMENT",
        "sections": [
            "Zoning Administrator",
            "Board of Adjustment",
            "Planning and Zoning Commission",
            "Variances",
            "Appeals",
            "Violations and Penalties",
            "Amendments",
            "Definitions",
        ],
    },
]


def build_title_page(story, styles):
    """Add title page content."""
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("CITY OF MOUNTAIN VIEW", styles['TitlePage']))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("UNIFIED DEVELOPMENT ORDINANCE", styles['TitlePage']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Chapter 7: Zoning", styles['Subtitle']))
    story.append(Paragraph("As Amended Through Ordinance No. 4892", styles['Subtitle']))
    story.append(Paragraph("Effective January 1, 2024", styles['Subtitle']))
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph(
        "Adopted by the Mountain View City Council<br/>"
        "Pursuant to N.C.G.S. Chapter 160D<br/>"
        "Planning and Development Regulation",
        styles['Subtitle']
    ))
    story.append(PageBreak())


def build_toc_page(story, styles):
    """Add a manually-built table of contents."""
    story.append(Paragraph("TABLE OF CONTENTS", styles['TitlePage']))
    story.append(Spacer(1, 0.4 * inch))
    for i, article in enumerate(ARTICLES, start=1):
        story.append(Paragraph(
            f"<b>Article {i}. {article['title']}</b>",
            styles['BodyJustified']
        ))
        for j, sec in enumerate(article['sections'], start=1):
            story.append(Paragraph(
                f"&nbsp;&nbsp;&nbsp;&nbsp;Sec. 7-{i}-{j}. {sec}",
                styles['IndentedItem']
            ))
    story.append(PageBreak())


def build_definitions_section(story, styles, article_num, section_num):
    """Build the definitions section with 30+ terms."""
    story.append(Paragraph(
        f"Sec. 7-{article_num}-{section_num}. \u2014 Definitions.",
        styles['SectionHeading']
    ))
    story.append(Paragraph(
        "For purposes of this chapter, the following terms shall have the meanings ascribed herein. "
        "Where terms are not defined in this section, they shall have ordinarily accepted meanings such as "
        "the context implies. See also Sec. 7-1-2 for rules of interpretation.",
        styles['BodyJustified']
    ))
    story.append(Spacer(1, 6))
    for term, definition in DEFINITIONS:
        story.append(Paragraph(f"{term}.", styles['DefinitionTerm']))
        story.append(Paragraph(definition, styles['DefinitionBody']))


def build_section_content(story, styles, article_num, section_num, section_title):
    """Generate content for a regular section with subsections."""
    story.append(Paragraph(
        f"Sec. 7-{article_num}-{section_num}. \u2014 {section_title}.",
        styles['SectionHeading']
    ))

    story.append(Paragraph(generate_legal_paragraph(2, 4), styles['BodyJustified']))

    num_subsections = random.randint(2, 5)
    subsection_labels = "abcdefgh"

    for k in range(num_subsections):
        label = subsection_labels[k]
        story.append(Paragraph(
            f"({label}) {generate_legal_paragraph(1, 2)}",
            styles['IndentedItem']
        ))

        if random.random() > 0.6:
            num_items = random.randint(2, 3)
            for m in range(1, num_items + 1):
                xref = ""
                if random.random() > 0.6:
                    ref_art = random.randint(1, 8)
                    ref_sec = random.randint(1, 8)
                    ref_sub = random.choice("abcde")
                    xref = f" See Section 7-{ref_art}-{ref_sec}({ref_sub})({random.randint(1,4)})."
                story.append(Paragraph(
                    f"({m}) {generate_legal_paragraph(1, 2)}{xref}",
                    styles['DeepIndent']
                ))

    if random.random() > 0.55:
        story.append(Paragraph(generate_legal_paragraph(2, 4), styles['BodyJustified']))


def build_dimensional_table_text(story, styles, article_num, section_num):
    """Build a section with dimensional requirements as formatted text."""
    story.append(Paragraph(
        f"Sec. 7-{article_num}-{section_num}. \u2014 Dimensional Requirements.",
        styles['SectionHeading']
    ))
    story.append(Paragraph(
        "The following dimensional requirements shall apply to all development within the respective "
        "zoning districts. Where a conflict exists between these standards and the standards of an "
        "overlay district, the more restrictive standard shall apply. See Section 7-2-5 for overlay "
        "district standards.",
        styles['BodyJustified']
    ))

    districts_data = [
        ("RS-1", "20,000", "100", "35", "15", "30", "35", "30%"),
        ("RS-2", "10,000", "70", "25", "10", "25", "35", "40%"),
        ("RM-6", "7,500", "60", "20", "8", "20", "45", "50%"),
        ("RM-16", "5,000", "50", "15", "8", "15", "60", "60%"),
        ("CB", "None", "None", "0", "0", "20", "50", "80%"),
        ("HB", "20,000", "100", "30", "15", "25", "45", "70%"),
    ]

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>District | Min Lot (sf) | Min Width (ft) | Front (ft) | Side (ft) | Rear (ft) | Max Ht (ft) | Max Coverage</b>",
        styles['IndentedItem']
    ))
    story.append(Spacer(1, 4))
    for row in districts_data:
        story.append(Paragraph(
            f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]}",
            styles['IndentedItem']
        ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(generate_legal_paragraph(3, 5), styles['BodyJustified']))


def build_document():
    """Build the complete PDF document."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = build_styles()
    story = []

    build_title_page(story, styles)
    build_toc_page(story, styles)

    for i, article in enumerate(ARTICLES, start=1):
        story.append(Paragraph(
            f"ARTICLE {i}. {article['title']}",
            styles['ArticleHeading']
        ))

        for j, section_title in enumerate(article['sections'], start=1):
            if section_title == "Definitions":
                build_definitions_section(story, styles, i, j)
            elif "Dimensional" in section_title:
                build_dimensional_table_text(story, styles, i, j)
            else:
                build_section_content(story, styles, i, j, section_title)

        if i < len(ARTICLES):
            story.append(Spacer(1, 0.3 * inch))

    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_document()
