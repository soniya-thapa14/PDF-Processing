"""Generate a ~40 page vector PDF replicating a zoning permit-use matrix."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT_DIR = Path(__file__).parent / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "permit_use_matrix.pdf"

ZONE_GROUPS = {
    "Residential Single-Family": ["RS2", "RS4", "RS6", "RS8", "RS10"],
    "Residential Multi-Family": ["RM6", "RM8", "RM12", "RM16"],
    "Neighborhood Commercial": ["NB", "NC", "NSC"],
    "Office / Business": ["OFF", "OBP", "BP"],
    "Commercial": ["CB", "HB", "GC", "CC"],
    "Industrial": ["CI", "LI", "IND", "HI"],
}

ALL_ZONES = []
for zones in ZONE_GROUPS.values():
    ALL_ZONES.extend(zones)

USE_CATEGORIES = {
    "Residential Uses": [
        "Single-family detached dwelling",
        "Single-family attached dwelling",
        "Duplex / two-family dwelling",
        "Triplex / three-family dwelling",
        "Townhouse (3-8 units)",
        "Multi-family apartment (9-24 units)",
        "Multi-family apartment (25+ units)",
        "Accessory dwelling unit (ADU)",
        "Manufactured / mobile home",
        "Group home (6 or fewer residents)",
        "Group home (7-15 residents)",
        "Residential care facility",
        "Live-work unit",
    ],
    "Lodging Uses": [
        "Bed and breakfast (1-4 rooms)",
        "Bed and breakfast (5+ rooms)",
        "Hotel / motel (under 50 rooms)",
        "Hotel / motel (50-150 rooms)",
        "Hotel / motel (over 150 rooms)",
        "Extended-stay lodging",
        "Short-term vacation rental",
        "Boarding / rooming house",
        "Hostel / dormitory (non-institutional)",
        "Resort / conference center",
        "Recreational vehicle park (transient)",
        "Campground / glamping facility",
    ],
    "Retail Sales Uses": [
        "General retail (under 5,000 sf)",
        "General retail (5,000-25,000 sf)",
        "General retail (over 25,000 sf)",
        "Convenience store",
        "Grocery / supermarket",
        "Farmers market (permanent)",
        "Farmers market (temporary/seasonal)",
        "Pharmacy / drugstore",
        "Hardware / home improvement store",
        "Automobile parts / accessories",
        "Garden center / nursery",
        "Liquor store (off-premises consumption)",
    ],
    "Food & Beverage Service Uses": [
        "Restaurant (no drive-through)",
        "Restaurant (with drive-through)*",
        "Fast-food restaurant*",
        "Cafe / coffee shop",
        "Bakery (retail)",
        "Catering establishment",
        "Bar / tavern / lounge",
        "Brewpub / microbrewery (with taproom)",
        "Mobile food vendor (commissary)",
        "Banquet hall / event dining",
    ],
    "Office & Professional Uses": [
        "General office",
        "Medical / dental office",
        "Veterinary clinic (no outdoor kennels)",
        "Veterinary clinic (with outdoor kennels)",
        "Financial institution (bank / credit union)",
        "Real estate / insurance office",
        "Coworking space",
        "Research & development laboratory",
        "Data center / server farm",
    ],
    "Entertainment & Recreation Uses": [
        "Movie theater / cinema",
        "Live performance theater",
        "Indoor amusement / arcade",
        "Outdoor amusement park",
        "Bowling alley",
        "Fitness center / gym (under 5,000 sf)",
        "Fitness center / gym (over 5,000 sf)",
        "Swimming pool (commercial)",
        "Golf course",
        "Miniature golf / driving range",
        "Private club / lodge",
        "Dance studio / martial arts studio",
    ],
    "Automotive & Vehicle Uses": [
        "Automobile sales (new)",
        "Automobile sales (used)",
        "Automobile rental agency",
        "Automobile repair (minor / maintenance)",
        "Automobile repair (major / body work)",
        "Automobile washing facility",
        "Gasoline / fuel station",
        "Gasoline station with convenience store*",
        "Truck / heavy equipment sales",
        "Parking lot / garage (commercial)",
        "Electric vehicle charging station (primary use)",
        "Motorcycle / powersports sales",
        "Tire sales and installation",
        "Automobile upholstery / detailing",
    ],
    "Personal & Business Service Uses": [
        "Barber shop / beauty salon",
        "Dry cleaning / laundry (drop-off)",
        "Self-service laundromat",
        "Tailoring / alteration shop",
        "Pet grooming (no boarding)",
        "Pet boarding / kennel**",
        "Funeral home / mortuary",
        "Tattoo / body piercing studio",
        "Printing / copy center",
        "Self-storage facility\u2020",
        "Locksmith / key cutting service",
        "Shoe repair / leather goods",
        "Pawn shop / secondhand dealer",
        "Check cashing / payday loan service",
    ],
    "Educational & Institutional Uses": [
        "Elementary / middle school",
        "High school",
        "College / university",
        "Trade / vocational school",
        "Tutoring center (private)",
        "Day care center (7+ children)",
        "Family day care home (6 or fewer)",
        "Library (public)",
        "Museum / art gallery",
        "Religious assembly (under 300 seats)",
        "Religious assembly (300+ seats)",
        "Community center",
    ],
    "Healthcare & Social Service Uses": [
        "Hospital (general / acute care)",
        "Urgent care clinic",
        "Outpatient surgical center",
        "Medical laboratory",
        "Rehabilitation center (outpatient)",
        "Substance abuse treatment (outpatient)",
        "Substance abuse treatment (residential)",
        "Homeless shelter",
        "Counseling center",
        "Blood bank / plasma center",
    ],
    "Government & Utility Uses": [
        "Government office building",
        "Fire station",
        "Police station",
        "Post office",
        "Public works / maintenance yard",
        "Water treatment plant",
        "Wastewater treatment facility",
        "Electric substation",
        "Telecommunications tower\u2020",
        "Solar energy facility (ground-mounted)",
        "Wind energy facility (commercial)",
    ],
    "Manufacturing & Production Uses": [
        "Light manufacturing / assembly",
        "Heavy manufacturing",
        "Food / beverage processing",
        "Pharmaceutical manufacturing",
        "Textile / garment manufacturing",
        "Electronics manufacturing",
        "Furniture / cabinet manufacturing",
        "Metal fabrication / machine shop",
        "Concrete / asphalt batching plant",
        "Chemical manufacturing / processing",
        "Recycling processing facility",
    ],
    "Warehouse & Distribution Uses": [
        "Warehouse (general storage)",
        "Warehouse (cold storage / refrigerated)",
        "Distribution center / logistics hub",
        "Moving / storage company",
        "Wholesale establishment",
        "Freight terminal",
        "Truck terminal / cross-dock",
        "Container storage yard",
        "Mini-warehouse / self-storage\u2020",
    ],
    "Agriculture & Resource Uses": [
        "Crop production / farming",
        "Greenhouse / plant nursery (wholesale)",
        "Livestock raising (non-commercial)",
        "Equestrian facility / stable",
        "Community garden",
        "Agricultural supply / feed store",
        "Timber harvesting / sawmill",
        "Mining / quarrying / gravel extraction",
        "Composting facility (commercial)",
        "Aquaculture / fish hatchery",
        "Winery / vineyard with tasting room",
        "Agritourism / U-pick operation",
    ],
    "Transportation & Infrastructure Uses": [
        "Transit station / bus depot",
        "Heliport / helipad",
        "Airport / airstrip",
        "Railroad yard / rail siding",
        "Marine terminal / port facility",
        "Taxi / ride-share dispatch office",
        "Ambulance service",
        "Towing / impound yard",
        "Park-and-ride facility",
        "Electric vehicle charging station",
    ],
    "Parks & Open Space Uses": [
        "Public park / playground",
        "Private recreational facility",
        "Nature preserve / wildlife habitat",
        "Trail / greenway corridor",
        "Athletic field complex",
        "Dog park (off-leash area)",
        "Botanical garden / arboretum",
        "Cemetery / memorial park",
        "RV park / campground",
        "Outdoor amphitheater",
    ],
    "Communication & Technology Uses": [
        "Radio / television broadcasting studio",
        "Recording studio",
        "Motion picture / video production",
        "Internet service provider facility",
        "Satellite earth station",
        "Call center / telemarketing office",
        "Cloud computing data center",
        "Fiber optic switching station",
    ],
    "Waste & Recycling Uses": [
        "Solid waste transfer station",
        "Materials recovery facility",
        "Hazardous waste collection facility",
        "Construction debris recycling",
        "Scrap metal processing yard",
        "Electronic waste recycling",
        "Yard waste composting (municipal)",
        "Sanitary landfill",
    ],
    "Temporary & Seasonal Uses": [
        "Temporary construction office/trailer",
        "Seasonal retail sales (Christmas trees, fireworks)",
        "Outdoor art / craft fair (temporary)",
        "Carnival / circus (temporary, max 14 days)",
        "Temporary real estate sales office",
        "Food truck rally / pop-up market",
        "Seasonal agricultural stand",
        "Temporary outdoor dining (parklet)",
        "Special event tent (max 72 hours)",
        "Temporary homeless warming shelter",
    ],
    "Home-Based Business Uses": [
        "Home occupation (no customers on-site)",
        "Home occupation (customers by appointment)",
        "Home-based child care (1-6 children)",
        "Home-based tutoring / instruction",
        "Home-based beauty / barber service",
        "Cottage food production",
        "Home-based craft / artisan production",
        "Home-based professional consulting",
        "Home-based online retail (no showroom)",
    ],
    "Cannabis & Controlled Substance Uses": [
        "Cannabis dispensary (medical)",
        "Cannabis dispensary (recreational)",
        "Cannabis cultivation (indoor)",
        "Cannabis cultivation (outdoor / greenhouse)",
        "Cannabis processing / manufacturing",
        "Cannabis testing laboratory",
        "Cannabis distribution facility",
        "Cannabis consumption lounge",
        "Hemp processing facility",
        "Kratom / CBD retail shop",
    ],
    "Energy & Green Infrastructure Uses": [
        "Solar farm (utility-scale, >1 MW)",
        "Rooftop solar installation (commercial)",
        "Battery energy storage system",
        "Wind turbine (small, <100 kW)",
        "Wind farm (utility-scale)",
        "Geothermal heating/cooling plant",
        "Biogas / anaerobic digester facility",
        "Electric vehicle fleet charging depot",
        "Hydrogen fueling station",
        "District heating / cooling plant",
    ],
    "Marine & Water-Related Uses": [
        "Marina / boat dock",
        "Boat repair / dry dock",
        "Boat sales / rental",
        "Fishing pier / charter service",
        "Seafood processing plant",
        "Waterfront restaurant",
        "Kayak / canoe livery",
        "Yacht club / sailing school",
        "Bait and tackle shop",
    ],
}

FOOTNOTES = {
    "*": "Drive-through facilities require Site Plan Review and must comply with Sec. 17.24.050 stacking lane standards.",
    "**": "Kennels and boarding facilities must maintain 200-ft setback from any residential zone boundary per Sec. 17.32.080.",
    "\u2020": "Subject to additional development standards in Chapter 17.40 (Supplemental Use Regulations).",
}

import random

random.seed(42)


def generate_permit_value(use_name: str, zone: str) -> str:
    """Assign a permit status based on use type and zone characteristics."""
    residential_zones = {"RS2", "RS4", "RS6", "RS8", "RS10", "RM6", "RM8", "RM12", "RM16"}
    commercial_zones = {"NB", "NC", "NSC", "CB", "HB", "GC", "CC"}
    office_zones = {"OFF", "OBP", "BP"}
    industrial_zones = {"CI", "LI", "IND", "HI"}

    use_lower = use_name.lower()

    if "single-family" in use_lower or "duplex" in use_lower:
        if zone in {"RS2", "RS4", "RS6", "RS8", "RS10"}:
            return "P"
        if zone in {"RM6", "RM8", "RM12", "RM16"}:
            return "C" if "attached" in use_lower else "P"
        return "\u2014"

    if "multi-family" in use_lower or "townhouse" in use_lower or "triplex" in use_lower:
        if zone in {"RS2", "RS4", "RS6"}:
            return "\u2014"
        if zone in {"RS8", "RS10"}:
            return "C"
        if zone in {"RM6", "RM8", "RM12", "RM16"}:
            return "P"
        if zone in commercial_zones:
            return "C"
        return "\u2014"

    if "adu" in use_lower or "accessory dwelling" in use_lower:
        if zone in residential_zones:
            return "P"
        return "\u2014"

    if "manufacturing" in use_lower or "fabrication" in use_lower or "batching" in use_lower:
        if zone in residential_zones:
            return "\u2014"
        if zone in {"NB", "NC", "NSC", "OFF", "OBP", "BP"}:
            return "\u2014"
        if zone in {"CI", "LI"}:
            return "P" if "light" in use_lower else "C"
        if zone in {"IND", "HI"}:
            return "P"
        if zone in {"CB", "HB", "GC", "CC"}:
            return "S" if "light" in use_lower else "\u2014"
        return "\u2014"

    if "warehouse" in use_lower or "distribution" in use_lower or "freight" in use_lower:
        if zone in residential_zones or zone in {"NB", "NC", "NSC"}:
            return "\u2014"
        if zone in industrial_zones:
            return "P"
        if zone in {"CB", "HB", "GC", "CC"}:
            return "C"
        if zone in office_zones:
            return "S"
        return "\u2014"

    if "restaurant" in use_lower or "cafe" in use_lower or "bakery" in use_lower:
        if zone in residential_zones:
            return "\u2014"
        if zone in commercial_zones or zone in office_zones:
            return "P" if "drive-through" not in use_lower else "C"
        if zone in {"CI", "LI"}:
            return "C"
        return "\u2014"

    if "hotel" in use_lower or "motel" in use_lower or "lodging" in use_lower:
        if zone in residential_zones:
            return "\u2014"
        if zone in {"CB", "HB", "GC", "CC"}:
            return "P" if "under 50" in use_lower else "C"
        if zone in office_zones:
            return "C"
        return "\u2014"

    if "retail" in use_lower or "store" in use_lower or "market" in use_lower:
        if zone in residential_zones:
            return "\u2014"
        if zone in {"NB", "NC", "NSC"}:
            return "P" if "under 5,000" in use_lower or "convenience" in use_lower else "C"
        if zone in {"CB", "HB", "GC", "CC"}:
            return "P"
        if zone in office_zones:
            return "C" if "under 5,000" in use_lower else "\u2014"
        if zone in industrial_zones:
            return "C"
        return "\u2014"

    if "office" in use_lower or "coworking" in use_lower or "financial" in use_lower:
        if zone in residential_zones:
            return "\u2014" if zone in {"RS2", "RS4", "RS6"} else "C"
        if zone in office_zones or zone in commercial_zones:
            return "P"
        if zone in industrial_zones:
            return "C"
        return "C"

    if "school" in use_lower or "college" in use_lower or "university" in use_lower:
        if zone in residential_zones:
            return "C"
        if zone in commercial_zones or zone in office_zones:
            return "P"
        if zone in industrial_zones:
            return "S"
        return "C"

    if "hospital" in use_lower or "clinic" in use_lower or "medical" in use_lower:
        if zone in {"RS2", "RS4", "RS6"}:
            return "\u2014"
        if zone in {"RS8", "RS10", "RM6", "RM8", "RM12", "RM16"}:
            return "C"
        if zone in commercial_zones or zone in office_zones:
            return "P"
        if zone in industrial_zones:
            return "C"
        return "C"

    if "solar" in use_lower or "wind" in use_lower or "telecomm" in use_lower:
        if zone in residential_zones:
            return "S"
        return "C"

    if "airport" in use_lower or "heliport" in use_lower or "marine" in use_lower:
        if zone in industrial_zones:
            return "C"
        return "\u2014"

    if "agriculture" in use_lower or "crop" in use_lower or "farming" in use_lower or "garden" in use_lower:
        if zone in {"RS2", "RS4", "RS6", "RS8", "RS10"}:
            return "P"
        if zone in {"RM6", "RM8", "RM12", "RM16"}:
            return "C"
        return "\u2014"

    # Default logic based on zone compatibility
    r = random.random()
    if zone in residential_zones:
        if r < 0.55:
            return "\u2014"
        elif r < 0.80:
            return "C"
        elif r < 0.92:
            return "S"
        else:
            return "P"
    elif zone in commercial_zones:
        if r < 0.15:
            return "\u2014"
        elif r < 0.40:
            return "C"
        elif r < 0.55:
            return "S"
        else:
            return "P"
    elif zone in industrial_zones:
        if r < 0.25:
            return "\u2014"
        elif r < 0.50:
            return "C"
        elif r < 0.65:
            return "S"
        else:
            return "P"
    else:
        if r < 0.20:
            return "\u2014"
        elif r < 0.50:
            return "C"
        else:
            return "P"


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "MatrixTitle", parent=styles["Heading1"], fontSize=18, alignment=TA_CENTER, spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        "MatrixSubtitle", parent=styles["Heading2"], fontSize=12, alignment=TA_CENTER, spaceAfter=6
    )
    body_style = ParagraphStyle("MatrixBody", parent=styles["Normal"], fontSize=9, leading=12)
    small_style = ParagraphStyle("SmallBody", parent=styles["Normal"], fontSize=8, leading=10)
    footnote_style = ParagraphStyle("Footnote", parent=styles["Normal"], fontSize=7, leading=9, leftIndent=12)
    cell_style = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=7, alignment=TA_CENTER, leading=9)
    use_style = ParagraphStyle("UseCell", parent=styles["Normal"], fontSize=7, leading=9)
    cat_style = ParagraphStyle(
        "CatCell", parent=styles["Normal"], fontSize=7, leading=9, alignment=TA_CENTER
    )
    header_style = ParagraphStyle("HeaderCell", parent=styles["Normal"], fontSize=6.5, alignment=TA_CENTER, leading=8)
    appendix_title = ParagraphStyle("AppTitle", parent=styles["Heading2"], fontSize=14, spaceAfter=10)
    appendix_body = ParagraphStyle("AppBody", parent=styles["Normal"], fontSize=9, leading=12, spaceBefore=4, spaceAfter=4)

    elements = []

    # === HEADER / LEGEND PAGE ===
    elements.append(Spacer(1, 30 * mm))
    elements.append(Paragraph("CITY OF MAPLEWOOD", title_style))
    elements.append(Paragraph("UNIFIED DEVELOPMENT CODE", subtitle_style))
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph("Table 17.08.020 \u2014 Permitted Use Matrix", subtitle_style))
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph(
        "This table identifies the uses of land permitted in each zoning district. "
        "Each use is classified as Permitted (P), Conditional (C), requiring Special Use Permit (S), "
        "or Not Allowed (\u2014). Additional conditions and supplemental standards may apply as noted.",
        body_style,
    ))
    elements.append(Spacer(1, 8 * mm))

    legend_data = [
        ["Symbol", "Meaning", "Description"],
        ["P", "Permitted", "Use is allowed by right, subject to compliance with all applicable development standards."],
        ["C", "Conditional Use", "Use requires approval of a Conditional Use Permit per Chapter 17.60."],
        ["S", "Special Use Permit", "Use requires a Special Use Permit with public hearing per Chapter 17.62."],
        ["\u2014", "Not Allowed", "Use is not permitted in this zoning district under any circumstances."],
    ]
    legend_table = Table(legend_data, colWidths=[60, 100, 380])
    legend_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.5)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.97)]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(legend_table)
    elements.append(Spacer(1, 8 * mm))

    elements.append(Paragraph("<b>Zone District Abbreviations:</b>", body_style))
    elements.append(Spacer(1, 3 * mm))
    zone_desc = {
        "RS2": "Residential Single-Family (2,000 sf min lot)",
        "RS4": "Residential Single-Family (4,000 sf min lot)",
        "RS6": "Residential Single-Family (6,000 sf min lot)",
        "RS8": "Residential Single-Family (8,000 sf min lot)",
        "RS10": "Residential Single-Family (10,000 sf min lot)",
        "RM6": "Residential Multi-Family (6 units/acre max)",
        "RM8": "Residential Multi-Family (8 units/acre max)",
        "RM12": "Residential Multi-Family (12 units/acre max)",
        "RM16": "Residential Multi-Family (16 units/acre max)",
        "NB": "Neighborhood Business",
        "NC": "Neighborhood Commercial",
        "NSC": "Neighborhood Service Commercial",
        "OFF": "Office",
        "OBP": "Office Business Park",
        "BP": "Business Park",
        "CB": "Central Business",
        "HB": "Highway Business",
        "GC": "General Commercial",
        "CC": "Community Commercial",
        "CI": "Commercial-Industrial",
        "LI": "Light Industrial",
        "IND": "General Industrial",
        "HI": "Heavy Industrial",
    }
    zone_lines = []
    for code, desc in zone_desc.items():
        zone_lines.append(f"<b>{code}</b> \u2014 {desc}")
    for i in range(0, len(zone_lines), 3):
        chunk = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(zone_lines[i : i + 3])
        elements.append(Paragraph(chunk, small_style))
    elements.append(Spacer(1, 8 * mm))

    elements.append(Paragraph("<b>Footnote Symbols:</b>", body_style))
    for mark, text in FOOTNOTES.items():
        elements.append(Paragraph(f"<b>{mark}</b> &mdash; {text}", footnote_style))

    elements.append(PageBreak())

    # === TABLE PAGES ===
    num_zones = len(ALL_ZONES)
    col_widths = [22 * mm, 62 * mm] + [16 * mm] * num_zones

    categories = list(USE_CATEGORIES.items())
    # Split categories into groups to create multiple table pages
    cats_per_page = 1

    page_groups = []
    for i in range(0, len(categories), cats_per_page):
        page_groups.append(categories[i : i + cats_per_page])

    for pg_idx, cat_group in enumerate(page_groups):
        # Build multi-row header
        # Row 1: zone group names spanning appropriate columns
        header_row1 = ["", ""]
        spans_row1 = []
        col_offset = 2
        for group_name, group_zones in ZONE_GROUPS.items():
            short_name = group_name.replace("Residential ", "Res. ").replace("Neighborhood ", "Nbhd. ").replace("Commercial", "Comm.")
            header_row1.append(Paragraph(f"<b>{short_name}</b>", header_style))
            for _ in range(len(group_zones) - 1):
                header_row1.append("")
            span_end = col_offset + len(group_zones) - 1
            spans_row1.append(("SPAN", (col_offset, 0), (span_end, 0)))
            col_offset += len(group_zones)

        # Row 2: individual zone codes
        header_row2 = [
            Paragraph("<b>Category</b>", header_style),
            Paragraph("<b>Specific Use Type</b>", header_style),
        ]
        for z in ALL_ZONES:
            header_row2.append(Paragraph(f"<b>{z}</b>", header_style))

        table_data = [header_row1, header_row2]

        style_commands = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.3, 0.5)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), colors.Color(0.3, 0.4, 0.6)),
            ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
            ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.6, 0.6, 0.6)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ]
        style_commands.extend(spans_row1)

        current_row = 2
        for cat_name, uses in cat_group:
            cat_start_row = current_row
            for use_idx, use_name in enumerate(uses):
                row = ["", Paragraph(use_name, use_style)]
                for zone in ALL_ZONES:
                    val = generate_permit_value(use_name, zone)
                    row.append(Paragraph(val, cell_style))
                table_data.append(row)
                current_row += 1

            cat_end_row = current_row - 1
            # Put category name in the first cell and span vertically
            table_data[cat_start_row][0] = Paragraph(f"<b>{cat_name}</b>", cat_style)
            if cat_end_row > cat_start_row:
                style_commands.append(("SPAN", (0, cat_start_row), (0, cat_end_row)))
            style_commands.append(
                ("BACKGROUND", (0, cat_start_row), (0, cat_end_row), colors.Color(0.9, 0.92, 0.96))
            )
            # Alternate row shading within category
            for r in range(cat_start_row, cat_end_row + 1):
                if (r - cat_start_row) % 2 == 1:
                    style_commands.append(
                        ("BACKGROUND", (1, r), (-1, r), colors.Color(0.96, 0.96, 0.98))
                    )

        tbl = Table(table_data, colWidths=col_widths, repeatRows=2)
        tbl.setStyle(TableStyle(style_commands))
        elements.append(tbl)
        elements.append(Spacer(1, 4 * mm))

        # Footnotes at bottom of each table page
        elements.append(Paragraph("<b>Notes:</b>", ParagraphStyle("NoteHead", parent=styles["Normal"], fontSize=7, leading=9)))
        for mark, text in FOOTNOTES.items():
            elements.append(Paragraph(f"{mark} {text}", footnote_style))
        elements.append(Paragraph(
            f"<i>Table 17.08.020 (continued) \u2014 Page {pg_idx + 1} of {len(page_groups)}</i>",
            ParagraphStyle("PageRef", parent=styles["Normal"], fontSize=7, alignment=TA_CENTER, spaceBefore=4),
        ))
        elements.append(PageBreak())

    # === APPENDIX PAGES ===
    appendix_sections = [
        (
            "Chapter 17.40 \u2014 Supplemental Use Regulations",
            [
                "Sec. 17.40.010 \u2014 Purpose and Applicability",
                "The supplemental use regulations in this chapter apply to specific land uses identified "
                "in the Permitted Use Matrix (Table 17.08.020) with footnote markers. These regulations "
                "establish additional standards beyond the base zoning district requirements to ensure "
                "compatibility between land uses and to protect the health, safety, and welfare of the "
                "community. Compliance with all applicable supplemental standards is required prior to "
                "issuance of any building permit or certificate of occupancy.",
                "",
                "Sec. 17.40.020 \u2014 Self-Storage Facilities (\u2020)",
                "A. Self-storage facilities shall be permitted only in zones designated CI, LI, IND, or HI "
                "and shall comply with the following standards:",
                "   1. Maximum building height: 35 feet or 3 stories, whichever is less.",
                "   2. All storage units shall be accessed from interior hallways. No exterior-access "
                "      roll-up doors shall face any public right-of-way.",
                "   3. A minimum 15-foot landscaped buffer shall be provided along all property lines "
                "      abutting a residential zone district.",
                "   4. Outdoor storage of vehicles, boats, or recreational vehicles is prohibited unless "
                "      the facility provides a separate screened area meeting the requirements of "
                "      Sec. 17.44.060 (Screening Standards).",
                "   5. Office and manager\u2019s quarters may be permitted as an accessory use, not to exceed "
                "      1,200 square feet combined.",
                "   6. Operating hours for customer access shall be limited to 6:00 AM to 10:00 PM daily.",
                "",
                "Sec. 17.40.030 \u2014 Telecommunications Towers (\u2020)",
                "A. New telecommunications towers require a Special Use Permit and shall comply with:",
                "   1. Minimum setback from any residential property line: 1.5 times the tower height.",
                "   2. Co-location on existing structures (buildings, utility poles, water towers) shall be "
                "      explored and documented prior to approval of a new freestanding tower.",
                "   3. Freestanding towers shall not exceed 150 feet in height in any district.",
                "   4. Equipment cabinets at the base shall be screened with a minimum 8-foot opaque fence "
                "      and landscaping compliant with Sec. 17.44.040.",
                "   5. All towers shall be designed to accommodate at least two additional carriers.",
                "   6. Abandoned towers (no active carrier for 12 months) shall be removed within 90 days "
                "      of notification by the Zoning Administrator.",
            ],
        ),
        (
            "Chapter 17.60 \u2014 Conditional Use Permits",
            [
                "Sec. 17.60.010 \u2014 Purpose",
                "Conditional Use Permits provide a mechanism for the review of uses that may be appropriate "
                "in a given zoning district but require individual consideration due to potential impacts "
                "on surrounding properties. The Planning Commission shall review each application based on "
                "the specific characteristics of the proposed use, site, and neighborhood context.",
                "",
                "Sec. 17.60.020 \u2014 Application Requirements",
                "Applications for a Conditional Use Permit shall include:",
                "   1. A completed application form with property owner\u2019s authorization.",
                "   2. A site plan drawn to scale (minimum 1 inch = 20 feet) showing all existing and "
                "      proposed structures, parking areas, landscaping, and access points.",
                "   3. A floor plan showing the proposed use and its relationship to other uses on the site.",
                "   4. An operations statement describing hours of operation, number of employees, "
                "      expected traffic generation, noise sources, and odor/emission sources.",
                "   5. A traffic impact analysis for uses generating more than 100 peak-hour trips.",
                "   6. Payment of the applicable review fee per the adopted fee schedule.",
                "",
                "Sec. 17.60.030 \u2014 Review Criteria",
                "The Planning Commission shall approve a Conditional Use Permit only upon finding that:",
                "   a. The proposed use is consistent with the Comprehensive Plan and the purpose of the "
                "      applicable zoning district.",
                "   b. The use will not create undue adverse impacts on adjacent properties with respect to "
                "      noise, vibration, glare, odors, traffic, or visual appearance.",
                "   c. Adequate public facilities (water, sewer, roads, schools, parks) exist or will be "
                "      provided concurrent with the development.",
                "   d. The site is of adequate size and configuration to accommodate the proposed use and "
                "      meet all dimensional and parking requirements.",
                "   e. The proposed use will not substantially diminish property values in the vicinity.",
                "   f. The proposed use is compatible with the existing character of the neighborhood.",
                "",
                "Sec. 17.60.040 \u2014 Conditions of Approval",
                "The Planning Commission may attach reasonable conditions to any Conditional Use Permit "
                "approval, including but not limited to: limitations on hours of operation, requirements "
                "for additional landscaping or buffering, restrictions on exterior lighting, requirements "
                "for sound attenuation, limitations on signage, periodic review requirements, and "
                "performance bonds or other financial guarantees.",
            ],
        ),
        (
            "Chapter 17.62 \u2014 Special Use Permits",
            [
                "Sec. 17.62.010 \u2014 Purpose and Scope",
                "Special Use Permits are required for uses that have significant potential for impact on "
                "surrounding properties or the community at large. These uses require a higher level of "
                "scrutiny than Conditional Uses, including a public hearing before the City Council with "
                "a recommendation from the Planning Commission.",
                "",
                "Sec. 17.62.020 \u2014 Public Hearing Requirements",
                "   1. Notice of the public hearing shall be published in the official newspaper at least "
                "      15 days prior to the hearing date.",
                "   2. Written notice shall be mailed to all property owners within 500 feet of the "
                "      subject property at least 15 days prior to the hearing.",
                "   3. A sign shall be posted on the property at least 10 days prior to the hearing.",
                "   4. The applicant shall hold a neighborhood meeting at least 7 days prior to the "
                "      Planning Commission hearing to present the proposal and receive feedback.",
                "",
                "Sec. 17.62.030 \u2014 Duration and Renewal",
                "Special Use Permits shall be issued for a specified period not to exceed 5 years and "
                "may be renewed upon application demonstrating continued compliance with all conditions "
                "of approval. The Zoning Administrator may revoke a Special Use Permit upon finding that "
                "the use is not in compliance with the conditions of approval after providing 30 days "
                "written notice and opportunity for hearing.",
            ],
        ),
        (
            "Chapter 17.24 \u2014 Drive-Through Facility Standards",
            [
                "Sec. 17.24.050 \u2014 Stacking Lane Requirements (*)",
                "Drive-through facilities (restaurants, banks, pharmacies, car washes, and similar uses) "
                "shall comply with the following stacking lane standards:",
                "",
                "   1. Restaurant drive-through: minimum 10 vehicles (200 linear feet) measured from the "
                "      order point.",
                "   2. Bank / financial institution: minimum 5 vehicles (100 linear feet) per lane.",
                "   3. Pharmacy: minimum 4 vehicles (80 linear feet) per lane.",
                "   4. Car wash (automatic): minimum 6 vehicles (120 linear feet) per bay.",
                "   5. Car wash (self-service): minimum 3 vehicles (60 linear feet) per bay.",
                "",
                "Sec. 17.24.060 \u2014 Site Design Standards",
                "   A. Stacking lanes shall not impede access to parking spaces or internal drive aisles.",
                "   B. A bypass lane shall be provided to allow vehicles to exit the drive-through queue.",
                "   C. Menu boards and order speakers shall be oriented away from adjacent residential uses.",
                "   D. Drive-through canopies shall be architecturally compatible with the principal building.",
                "   E. Stacking lanes adjacent to residential zones shall be screened with a minimum "
                "      6-foot masonry wall and 5-foot landscaped buffer.",
                "",
                "Sec. 17.24.070 \u2014 Hours of Operation",
                "Drive-through facilities within 200 feet of a residential zone boundary shall limit "
                "drive-through operations to the hours of 6:00 AM to 11:00 PM unless the Planning "
                "Commission grants an extension based on demonstrated lack of noise impact.",
            ],
        ),
        (
            "Chapter 17.32 \u2014 Animal-Related Use Standards",
            [
                "Sec. 17.32.080 \u2014 Kennels and Boarding Facilities (**)",
                "Commercial kennels and pet boarding facilities shall comply with the following standards:",
                "",
                "   1. Minimum lot size: 1 acre.",
                "   2. Minimum setback from any residential zone boundary: 200 feet for all outdoor "
                "      exercise or kennel areas.",
                "   3. All animals shall be housed indoors between 8:00 PM and 7:00 AM.",
                "   4. Outdoor exercise areas shall be enclosed with a minimum 6-foot fence and shall "
                "      include sound-attenuation features (solid walls, earth berms, or equivalent).",
                "   5. A waste management plan shall be submitted and approved, addressing daily cleanup "
                "      procedures, storage of waste, and disposal methods.",
                "   6. Maximum number of animals: 30 dogs or 50 cats (or equivalent combination as "
                "      determined by the Zoning Administrator).",
                "   7. All facilities shall be licensed by the County Animal Control Division and shall "
                "      maintain current vaccination records for all boarded animals.",
                "",
                "Sec. 17.32.090 \u2014 Veterinary Clinics",
                "   A. Veterinary clinics without outdoor kennels are permitted in NB, NC, NSC, CB, HB, "
                "      GC, CC, OFF, and OBP districts as indicated in the Permitted Use Matrix.",
                "   B. Veterinary clinics with outdoor kennels shall meet the setback and operational "
                "      requirements of Sec. 17.32.080 above.",
                "   C. Emergency veterinary services operating between 10:00 PM and 7:00 AM shall "
                "      provide a sound impact study demonstrating compliance with the City\u2019s noise "
                "      ordinance (Chapter 8.24 of the Municipal Code).",
            ],
        ),
        (
            "Chapter 17.44 \u2014 Landscaping and Screening",
            [
                "Sec. 17.44.010 \u2014 Purpose",
                "Landscaping and screening requirements serve to: enhance the visual quality of "
                "development; provide transitions between incompatible land uses; reduce noise, glare, "
                "and visual impacts; control erosion and manage stormwater; and preserve and enhance "
                "property values throughout the community.",
                "",
                "Sec. 17.44.020 \u2014 General Requirements",
                "   1. All non-residential development and multi-family development of 4 or more units "
                "      shall provide landscaping in accordance with this chapter.",
                "   2. A minimum of 15% of the total lot area shall be landscaped for commercial uses; "
                "      20% for industrial uses; 25% for multi-family residential uses.",
                "   3. All required landscaping shall be irrigated with a permanent, automatic irrigation "
                "      system unless drought-tolerant plant materials are used exclusively.",
                "",
                "Sec. 17.44.040 \u2014 Buffer Yard Standards",
                "Buffer yards are required between incompatible land uses as follows:",
                "   Type A (minimum): 10-foot width, 1 canopy tree and 6 shrubs per 50 linear feet.",
                "   Type B (standard): 15-foot width, 2 canopy trees, 1 understory tree, and 10 shrubs "
                "   per 50 linear feet, plus a 4-foot berm or 6-foot fence.",
                "   Type C (enhanced): 25-foot width, 3 canopy trees, 2 understory trees, 15 shrubs, "
                "   and an evergreen hedge per 50 linear feet, plus a 6-foot masonry wall.",
                "",
                "Sec. 17.44.060 \u2014 Screening Standards",
                "   A. Mechanical equipment, dumpsters, loading areas, and outdoor storage shall be "
                "      screened from public view and from adjacent residential properties.",
                "   B. Screening shall consist of a solid wall, fence, or combination of berming and "
                "      dense evergreen plantings achieving year-round opacity.",
                "   C. Rooftop mechanical equipment shall be screened by a parapet or equipment screen "
                "      to a height at least equal to the tallest equipment element.",
            ],
        ),
        (
            "Chapter 17.48 \u2014 Parking and Loading Standards",
            [
                "Sec. 17.48.010 \u2014 Purpose",
                "Off-street parking and loading requirements ensure adequate vehicle accommodation "
                "for each land use, minimize traffic congestion, and promote safe pedestrian movement. "
                "All uses shall provide the minimum number of parking spaces specified in this chapter "
                "unless a reduction is granted through the shared parking or parking study provisions.",
                "",
                "Sec. 17.48.020 \u2014 Minimum Parking Ratios",
                "The following minimum parking ratios apply to new development and changes of use:",
                "   Single-family dwelling: 2 spaces per unit",
                "   Multi-family dwelling: 1.5 spaces per unit + 0.25 guest spaces per unit",
                "   General retail: 1 space per 250 sf of gross floor area",
                "   Restaurant: 1 space per 100 sf of dining area + 1 per 2 employees",
                "   General office: 1 space per 300 sf of gross floor area",
                "   Medical office: 1 space per 200 sf of gross floor area",
                "   Manufacturing: 1 space per 500 sf + 1 per company vehicle",
                "   Warehouse: 1 space per 1,000 sf of gross floor area",
                "   Hotel/motel: 1 space per room + 1 per 2 employees on largest shift",
                "   Church/assembly: 1 space per 4 seats in main assembly area",
                "   School (elementary): 1.5 spaces per classroom",
                "   School (high school): 1 space per classroom + 1 per 10 students",
                "",
                "Sec. 17.48.030 \u2014 Shared Parking",
                "Where two or more uses on the same or adjacent lots have different peak parking demand "
                "periods, the Zoning Administrator may approve a shared parking plan that reduces the "
                "total required spaces by up to 25%. The applicant shall provide a parking demand study "
                "prepared by a licensed traffic engineer demonstrating that adequate parking will be "
                "available during all hours of operation.",
                "",
                "Sec. 17.48.040 \u2014 Loading Space Requirements",
                "   A. Retail (10,000-50,000 sf): 1 loading space (12 ft x 35 ft x 14 ft clearance).",
                "   B. Retail (over 50,000 sf): 2 loading spaces.",
                "   C. Office (over 50,000 sf): 1 loading space.",
                "   D. Manufacturing/warehouse (any size): 1 loading space per 20,000 sf.",
                "   E. Loading spaces shall not be located in required front or side yard setbacks.",
                "   F. Loading areas shall be screened from public streets and residential properties.",
                "",
                "Sec. 17.48.050 \u2014 Bicycle Parking",
                "Non-residential development exceeding 5,000 sf and multi-family development of 10 or "
                "more units shall provide bicycle parking at a rate of 1 space per 10 vehicle spaces "
                "(minimum 4 spaces). At least 50% of required bicycle parking shall be covered. Bicycle "
                "parking facilities shall consist of inverted-U racks or equivalent designs that allow "
                "the frame and one wheel to be locked.",
            ],
        ),
        (
            "Chapter 17.52 \u2014 Sign Regulations",
            [
                "Sec. 17.52.010 \u2014 Purpose and Intent",
                "The sign regulations in this chapter balance the need for effective visual communication "
                "with the goals of community aesthetics, traffic safety, and property value protection. "
                "Signs shall be designed, constructed, installed, and maintained in accordance with the "
                "standards of this chapter and all applicable building codes.",
                "",
                "Sec. 17.52.020 \u2014 Exempt Signs",
                "The following signs are exempt from permit requirements but must comply with all other "
                "applicable standards:",
                "   1. Government signs (regulatory, directional, informational).",
                "   2. Address numerals not exceeding 12 inches in height.",
                "   3. Temporary real estate signs (one per street frontage, max 6 sf residential / "
                "      32 sf non-residential).",
                "   4. Political/campaign signs (removed within 7 days after election).",
                "   5. Holiday decorations displayed for not more than 45 consecutive days.",
                "   6. Memorial plaques or cornerstones not exceeding 4 sf.",
                "",
                "Sec. 17.52.030 \u2014 Prohibited Signs",
                "The following sign types are prohibited in all zoning districts:",
                "   A. Off-premises signs (billboards) except in the HB district with Special Use Permit.",
                "   B. Animated, flashing, or intermittently illuminated signs.",
                "   C. Signs placed on public property or within public rights-of-way (except government).",
                "   D. Roof-mounted signs that project above the roofline.",
                "   E. Vehicle-mounted signs displayed primarily for advertising (parked for > 24 hours).",
                "   F. Inflatable signs, pennants, streamers, and banners (except temporary event permits).",
                "",
                "Sec. 17.52.040 \u2014 Sign Area by Zoning District",
                "Maximum total sign area permitted per lot:",
                "   Residential districts: 4 sf (nameplate only)",
                "   NB, NC, NSC districts: 50 sf total, max 1.5 sf per linear foot of building frontage",
                "   OFF, OBP, BP districts: 75 sf total, max 2 sf per linear foot of building frontage",
                "   CB, HB, GC, CC districts: 150 sf total, max 2.5 sf per linear foot of frontage",
                "   CI, LI, IND, HI districts: 200 sf total, max 3 sf per linear foot of frontage",
                "",
                "Sec. 17.52.050 \u2014 Freestanding Sign Standards",
                "   A. Maximum height: 6 feet (residential), 20 feet (commercial), 30 feet (highway).",
                "   B. Minimum setback: 5 feet from all property lines.",
                "   C. Maximum area per face: 32 sf (neighborhood), 100 sf (commercial), 200 sf (highway).",
                "   D. Monument-style base required for all freestanding signs over 6 feet in height.",
                "   E. Internal illumination permitted; external illumination shall be shielded to prevent "
                "      light trespass onto adjacent properties.",
            ],
        ),
        (
            "Chapter 17.56 \u2014 Nonconforming Uses and Structures",
            [
                "Sec. 17.56.010 \u2014 Purpose and Intent",
                "This chapter establishes regulations governing nonconforming uses, structures, lots, "
                "and signs that lawfully existed prior to adoption of this Code but no longer conform to "
                "current requirements. The intent is to allow continuation of existing investments while "
                "encouraging eventual conformity through natural market forces and property transitions.",
                "",
                "Sec. 17.56.020 \u2014 Continuation of Nonconforming Uses",
                "A lawfully established nonconforming use may continue subject to the following:",
                "   1. The use shall not be expanded or extended to occupy additional floor area, land "
                "      area, or structures beyond that existing at the time the use became nonconforming.",
                "   2. The use shall not be changed to another nonconforming use.",
                "   3. If the nonconforming use is discontinued for a continuous period of 12 months, "
                "      the right to resume the use is lost and future use must conform to current zoning.",
                "   4. Routine maintenance and repair is permitted; structural alterations are prohibited "
                "      unless required by law or ordered by an authorized public official for safety.",
                "",
                "Sec. 17.56.030 \u2014 Nonconforming Structures",
                "A lawfully established structure that does not conform to current dimensional requirements "
                "(setbacks, height, lot coverage) may continue subject to:",
                "   1. No expansion that increases the degree of nonconformity.",
                "   2. If damaged or destroyed to the extent of more than 50% of its replacement value, "
                "      reconstruction shall conform to current requirements.",
                "   3. Interior remodeling is permitted provided no structural alteration increases the "
                "      building footprint or height.",
                "",
                "Sec. 17.56.040 \u2014 Nonconforming Lots of Record",
                "A lot that was legally created and recorded but does not meet current minimum lot size "
                "or width requirements may be developed with a permitted use subject to:",
                "   1. All other dimensional requirements (setbacks, height, coverage) are met, OR",
                "   2. A variance is obtained per Chapter 17.64 for dimensional requirements that cannot "
                "      be met due to the nonconforming lot dimensions.",
                "   3. The lot was not created in violation of subdivision regulations existing at the "
                "      time of its creation.",
            ],
        ),
        (
            "Chapter 17.64 \u2014 Variances and Appeals",
            [
                "Sec. 17.64.010 \u2014 Authority",
                "The Board of Zoning Appeals (BZA) is authorized to hear and decide applications for "
                "variances from the strict application of the dimensional and area regulations of this "
                "Code where literal enforcement would result in unnecessary hardship.",
                "",
                "Sec. 17.64.020 \u2014 Standards for Granting Variances",
                "A variance may be granted only upon finding that ALL of the following conditions exist:",
                "   1. The property has unique physical characteristics (topography, shape, size, "
                "      or natural features) not shared by surrounding properties.",
                "   2. The hardship is not self-created by the applicant or predecessor in title.",
                "   3. The variance is the minimum necessary to provide reasonable use of the property.",
                "   4. The variance will not be detrimental to adjacent properties or the public welfare.",
                "   5. The variance will not substantially impair the intent and purpose of the zoning "
                "      district or the Comprehensive Plan.",
                "",
                "Sec. 17.64.030 \u2014 Application and Hearing Process",
                "   A. Application filed with Zoning Administrator, including site plan and written "
                "      justification addressing all five variance criteria.",
                "   B. Staff review and report within 21 days of complete application.",
                "   C. Public notice: newspaper publication (15 days), mailed notice to properties "
                "      within 300 feet (15 days), posted sign on property (10 days).",
                "   D. BZA hearing with opportunity for public testimony.",
                "   E. Decision by BZA within 60 days of complete application.",
                "   F. Appeal of BZA decision to District Court within 30 days.",
                "",
                "Sec. 17.64.040 \u2014 Conditions of Variance Approval",
                "The BZA may attach reasonable conditions to variance approval including time limits, "
                "additional setbacks, screening, height restrictions, use limitations, or other "
                "conditions necessary to protect adjacent properties and the public interest. Violation "
                "of any condition shall void the variance.",
            ],
        ),
        (
            "Chapter 17.68 \u2014 Amendments and Rezoning",
            [
                "Sec. 17.68.010 \u2014 Purpose",
                "This chapter establishes the procedure for amendments to the text of this Code and to "
                "the Official Zoning Map. Amendments may be initiated by the City Council, Planning "
                "Commission, or by application of a property owner.",
                "",
                "Sec. 17.68.020 \u2014 Text Amendments",
                "   A. Text amendments may be initiated by resolution of the City Council or Planning "
                "      Commission, or by written petition of any citizen.",
                "   B. The Planning Commission shall hold a public hearing and provide a recommendation "
                "      to the City Council within 60 days.",
                "   C. The City Council shall act on the recommendation within 90 days.",
                "   D. Text amendments require a simple majority vote of the City Council.",
                "",
                "Sec. 17.68.030 \u2014 Map Amendments (Rezoning)",
                "Applications for rezoning shall include:",
                "   1. Legal description of the subject property.",
                "   2. Current and proposed zoning classification.",
                "   3. Statement of reasons for the proposed change.",
                "   4. Concept plan showing intended development if rezoned.",
                "   5. Traffic impact analysis if proposed use generates > 200 daily trips.",
                "   6. Environmental assessment if property contains wetlands, floodplain, or steep slopes.",
                "",
                "Sec. 17.68.040 \u2014 Review Criteria for Rezoning",
                "The Planning Commission and City Council shall consider:",
                "   A. Consistency with the Comprehensive Plan and future land use map.",
                "   B. Compatibility with existing development patterns in the vicinity.",
                "   C. Adequacy of public facilities and infrastructure to serve the proposed use.",
                "   D. Impact on property values in the surrounding area.",
                "   E. Whether changed conditions justify the proposed rezoning.",
                "   F. Whether the proposed rezoning results in spot zoning.",
                "",
                "Sec. 17.68.050 \u2014 Protest Provisions",
                "If a written protest against a proposed rezoning is filed by owners of 20% or more of "
                "the land area within the proposed change, or by owners of 20% or more of the land "
                "within 200 feet of the boundary of the proposed change (excluding streets and alleys), "
                "the rezoning requires a three-fourths supermajority vote of the City Council.",
            ],
        ),
    ]

    elements.append(Paragraph("APPENDIX A", title_style))
    elements.append(Paragraph("Supplemental Standards and Procedures", subtitle_style))
    elements.append(Spacer(1, 5 * mm))
    elements.append(Paragraph(
        "The following chapters provide detailed standards and procedures referenced in the "
        "Permitted Use Matrix. Uses marked with footnote symbols must comply with the applicable "
        "sections below in addition to base zoning district requirements.",
        body_style,
    ))
    elements.append(PageBreak())

    for section_title, paragraphs in appendix_sections:
        elements.append(Paragraph(section_title, appendix_title))
        elements.append(Spacer(1, 3 * mm))
        for para in paragraphs:
            if para == "":
                elements.append(Spacer(1, 3 * mm))
            elif para.startswith("Sec."):
                elements.append(Paragraph(f"<b>{para}</b>", appendix_body))
            else:
                elements.append(Paragraph(para, appendix_body))
        elements.append(PageBreak())

    doc.build(elements)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
