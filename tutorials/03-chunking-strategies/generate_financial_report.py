"""Generate a ~40 page vector PDF annual financial report for Acme Corp."""

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether,
)

OUTPUT_DIR = Path(__file__).parent / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "financial_report.pdf"

styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "CoverTitle", parent=styles["Title"], fontSize=28, leading=34, spaceAfter=20
)
style_subtitle = ParagraphStyle(
    "CoverSubtitle", parent=styles["Title"], fontSize=16, leading=20, spaceAfter=40
)
style_heading1 = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontSize=18, leading=22, spaceBefore=20, spaceAfter=12
)
style_heading2 = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=14, leading=17, spaceBefore=14, spaceAfter=8
)
style_body = ParagraphStyle(
    "Body", parent=styles["Normal"], fontSize=10, leading=13, spaceAfter=8
)
style_footnote = ParagraphStyle(
    "Footnote", parent=styles["Normal"], fontSize=8, leading=10, spaceAfter=4
)
style_small = ParagraphStyle(
    "Small", parent=styles["Normal"], fontSize=9, leading=11, spaceAfter=6
)


def fmt_dollar(val):
    """Format integer as dollar string."""
    if val < 0:
        return f"(${ abs(val):,.0f})"
    return f"${val:,.0f}"


def fmt_pct(val):
    """Format float as percentage."""
    return f"{val:.1f}%"


def make_table(data, col_widths=None, has_header=True, merge_groups=None):
    """Create a styled financial table."""
    if col_widths is None:
        col_widths = None

    t = Table(data, colWidths=col_widths, repeatRows=1 if has_header else 0)

    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]

    if has_header:
        style_cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]

    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#ECF0F1")))

    if merge_groups:
        for (start_row, end_row, label) in merge_groups:
            style_cmds.append(("SPAN", (0, start_row), (0, end_row)))
            style_cmds.append(("FONTNAME", (0, start_row), (0, end_row), "Helvetica-Bold"))
            style_cmds.append(("BACKGROUND", (0, start_row), (0, end_row), colors.HexColor("#D5DBDB")))
            style_cmds.append(("VALIGN", (0, start_row), (0, end_row), "TOP"))

    t.setStyle(TableStyle(style_cmds))
    return t


def build_cover():
    """Build cover page elements."""
    elements = []
    elements.append(Spacer(1, 6 * cm))
    elements.append(Paragraph("Acme Corporation", style_title))
    elements.append(Paragraph("Annual Report FY2024", style_subtitle))
    elements.append(Spacer(1, 2 * cm))
    elements.append(Paragraph("Fiscal Year Ended December 31, 2024", style_body))
    elements.append(Paragraph("Prepared by: Acme Corp Finance Department", style_body))
    elements.append(Paragraph("Date of Issue: March 15, 2025", style_body))
    elements.append(Spacer(1, 3 * cm))
    elements.append(
        Paragraph(
            "This document contains forward-looking statements that involve risks and uncertainties. "
            "Actual results may differ materially from those projected. Acme Corporation undertakes no "
            "obligation to update forward-looking statements.",
            style_small,
        )
    )
    elements.append(PageBreak())
    return elements


def build_executive_summary():
    """Build executive summary section (2 pages)."""
    elements = []
    elements.append(Paragraph("Executive Summary", style_heading1))
    
    paras = [
        "Fiscal Year 2024 marked a transformative period for Acme Corporation, characterized by robust "
        "revenue growth across all business segments, disciplined cost management, and strategic investments "
        "in next-generation technology platforms. Total revenue reached $4.82 billion, representing a 14.3% "
        "increase over the prior year, driven primarily by strong demand in our Enterprise Solutions and "
        "Cloud Services divisions.",

        "Operating income expanded to $1.12 billion, a 19.7% improvement year-over-year, reflecting "
        "operating leverage from our scaled infrastructure and the successful integration of the DataFlow "
        "acquisition completed in Q1 2024. Net income attributable to common shareholders was $847 million, "
        "or $6.78 per diluted share, compared to $712 million ($5.70 per diluted share) in FY2023.",

        "Our balance sheet remains strong with $2.3 billion in cash and cash equivalents and total debt of "
        "$1.8 billion, resulting in a net cash position of $500 million. During the year, we returned "
        "$620 million to shareholders through dividends and share repurchases while maintaining our "
        "investment-grade credit rating.",

        "Key operational highlights include: expansion into three new geographic markets (Southeast Asia, "
        "Eastern Europe, and Latin America); the launch of our AI-powered analytics platform which "
        "achieved $180 million in first-year bookings; and a 23% increase in recurring revenue which "
        "now represents 72% of total revenue, up from 65% in the prior year.",

        "Employee headcount grew to 18,450 from 16,200, primarily in engineering and customer success "
        "roles. Employee retention remained strong at 91%, supported by competitive compensation, "
        "expanded benefits, and our commitment to hybrid work flexibility. We invested $45 million in "
        "employee development and training programs.",

        "Looking ahead to FY2025, management expects continued momentum with revenue guidance of "
        "$5.4-5.6 billion (12-16% growth) and operating margins expanding to 24-25%. Capital expenditure "
        "is planned at $380-420 million, focused on data center capacity and R&D infrastructure. "
        "We anticipate completing two additional acquisitions in adjacent technology markets.",

        "The Board of Directors approved a 15% increase in the quarterly dividend to $0.92 per share "
        "and authorized a new $1.5 billion share repurchase program. These actions reflect our confidence "
        "in the company's long-term growth trajectory and commitment to balanced capital allocation.",

        "Our strategic priorities for the coming fiscal year include: (1) accelerating cloud migration "
        "for enterprise customers; (2) expanding our AI/ML product portfolio; (3) deepening partnerships "
        "with hyperscale cloud providers; (4) pursuing targeted M&A to fill technology gaps; and "
        "(5) investing in emerging markets where we see significant untapped demand.",

        "Risk factors that could impact our outlook include macroeconomic uncertainty, increased "
        "competition in the cloud infrastructure market, potential regulatory changes in key markets, "
        "and foreign currency headwinds given our growing international exposure (38% of revenue). "
        "Management has implemented comprehensive risk mitigation strategies including currency hedging, "
        "diversified revenue streams, and flexible cost structures.",

        "We are grateful to our shareholders, customers, employees, and partners for their continued "
        "support and confidence. The management team remains focused on executing our strategic plan "
        "and delivering sustainable long-term value creation.",
    ]

    for p in paras:
        elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 2 * mm))

    elements.append(PageBreak())
    return elements




def build_income_statement():
    """Table 1: Consolidated Income Statement."""
    elements = []
    elements.append(Paragraph("Consolidated Income Statement", style_heading1))
    elements.append(Paragraph(
        "The following table presents Acme Corporation's consolidated results of operations for the "
        "fiscal year ended December 31, 2024, with quarterly detail and year-over-year comparison. "
        "Revenue recognition follows ASC 606 guidelines with performance obligations satisfied over time "
        "for subscription contracts and at a point in time for perpetual licenses.",
        style_body,
    ))

    header = ["Line Item", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "FY2024", "FY2023", "YoY %"]
    rows = [
        ["Product Revenue", 385000, 412000, 428000, 455000, 1680000, 1520000],
        ["Service Revenue", 520000, 548000, 572000, 610000, 2250000, 1950000],
        ["Subscription Revenue", 198000, 212000, 228000, 252000, 890000, 720000],
        ["Total Revenue", 1103000, 1172000, 1228000, 1317000, 4820000, 4190000],
        ["", "", "", "", "", "", ""],
        ["Cost of Product Revenue", 115000, 123000, 128000, 136000, 502000, 468000],
        ["Cost of Service Revenue", 234000, 246000, 257000, 274000, 1011000, 897000],
        ["Cost of Subscription Revenue", 59000, 63000, 68000, 75000, 265000, 223000],
        ["Total Cost of Revenue", 408000, 432000, 453000, 485000, 1778000, 1588000],
        ["Gross Profit", 695000, 740000, 775000, 832000, 3042000, 2602000],
        ["", "", "", "", "", "", ""],
        ["Research & Development", 165000, 172000, 178000, 185000, 700000, 615000],
        ["Sales & Marketing", 187000, 195000, 204000, 218000, 804000, 720000],
        ["General & Administrative", 82000, 85000, 88000, 92000, 347000, 318000],
        ["Depreciation & Amortization", 18000, 19000, 19000, 20000, 76000, 68000],
        ["Total Operating Expenses", 452000, 471000, 489000, 515000, 1927000, 1721000],
        ["Operating Income", 243000, 269000, 286000, 317000, 1115000, 881000],
        ["", "", "", "", "", "", ""],
        ["Interest Income", 8000, 9000, 9000, 10000, 36000, 28000],
        ["Interest Expense", -12000, -12000, -11000, -11000, -46000, -52000],
        ["Other Income (Expense)", 2000, -1000, 3000, 1000, 5000, -3000],
        ["Income Before Tax", 241000, 265000, 287000, 317000, 1110000, 854000],
        ["Income Tax Expense", 55000, 61000, 66000, 73000, 255000, 197000],
        ["Net Income", 186000, 204000, 221000, 244000, 855000, 657000],
        ["Less: Non-controlling Interest", 2000, 2000, 2000, 2000, 8000, 5000],
        ["Net Income (Common)", 184000, 202000, 219000, 242000, 847000, 652000],
    ]

    data = [header]
    for row in rows:
        if row[1] == "":
            data.append([row[0]] + [""] * 7)
        else:
            vals = row[1:]
            fy24 = vals[4] if isinstance(vals[4], int) else 0
            fy23 = vals[5] if isinstance(vals[5], int) else 0
            yoy = ((fy24 - fy23) / fy23 * 100) if fy23 != 0 else 0.0
            formatted = [row[0]]
            for v in vals[:6]:
                formatted.append(fmt_dollar(v * 1000) if isinstance(v, int) else str(v))
            formatted.append(fmt_pct(yoy))
            data.append(formatted)

    col_w = [4.5 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.4 * cm, 1.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Revenue is reported in thousands of USD. All figures are unaudited for "
        "quarterly periods and audited for annual totals.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> YoY percentage calculated on full-year basis. Operating income growth of 26.6% "
        "reflects improved operating leverage and favorable product mix shift toward higher-margin "
        "subscription offerings.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_balance_sheet():
    """Table 2: Balance Sheet."""
    elements = []
    elements.append(Paragraph("Consolidated Balance Sheet", style_heading1))
    elements.append(Paragraph(
        "The consolidated balance sheet presents the financial position of Acme Corporation as of "
        "December 31, 2024, prepared in accordance with U.S. GAAP. Comparative figures for the prior "
        "year-end are provided for reference.",
        style_body,
    ))

    header = ["Account", "Dec 31, 2024", "Dec 31, 2023", "Change"]
    rows = [
        ["ASSETS", "", "", ""],
        ["Current Assets:", "", "", ""],
        ["  Cash and Cash Equivalents", 2310000, 1890000, 420000],
        ["  Short-term Investments", 450000, 380000, 70000],
        ["  Accounts Receivable, net", 892000, 765000, 127000],
        ["  Inventories", 124000, 118000, 6000],
        ["  Prepaid Expenses", 87000, 72000, 15000],
        ["  Other Current Assets", 56000, 48000, 8000],
        ["Total Current Assets", 3919000, 3273000, 646000],
        ["", "", "", ""],
        ["Non-Current Assets:", "", "", ""],
        ["  Property, Plant & Equipment, net", 1245000, 1080000, 165000],
        ["  Operating Lease Right-of-Use", 340000, 310000, 30000],
        ["  Goodwill", 1820000, 1420000, 400000],
        ["  Intangible Assets, net", 560000, 480000, 80000],
        ["  Long-term Investments", 280000, 220000, 60000],
        ["  Deferred Tax Assets", 92000, 78000, 14000],
        ["  Other Non-Current Assets", 44000, 39000, 5000],
        ["Total Non-Current Assets", 4381000, 3627000, 754000],
        ["TOTAL ASSETS", 8300000, 6900000, 1400000],
        ["", "", "", ""],
        ["LIABILITIES", "", "", ""],
        ["Current Liabilities:", "", "", ""],
        ["  Accounts Payable", 423000, 378000, 45000],
        ["  Accrued Expenses", 312000, 267000, 45000],
        ["  Deferred Revenue (current)", 580000, 490000, 90000],
        ["  Current Portion of Debt", 200000, 150000, 50000],
        ["  Operating Lease Liabilities (current)", 72000, 65000, 7000],
        ["  Other Current Liabilities", 95000, 82000, 13000],
        ["Total Current Liabilities", 1682000, 1432000, 250000],
        ["", "", "", ""],
        ["Non-Current Liabilities:", "", "", ""],
        ["  Long-term Debt", 1600000, 1350000, 250000],
        ["  Deferred Revenue (non-current)", 245000, 210000, 35000],
        ["  Operating Lease Liabilities (non-current)", 290000, 265000, 25000],
        ["  Deferred Tax Liabilities", 135000, 112000, 23000],
        ["  Other Non-Current Liabilities", 68000, 55000, 13000],
        ["Total Non-Current Liabilities", 2338000, 1992000, 346000],
        ["TOTAL LIABILITIES", 4020000, 3424000, 596000],
        ["", "", "", ""],
        ["SHAREHOLDERS' EQUITY", "", "", ""],
        ["  Common Stock ($0.01 par value)", 1250, 1250, 0],
        ["  Additional Paid-in Capital", 1850000, 1720000, 130000],
        ["  Retained Earnings", 2520000, 1843000, 677000],
        ["  Treasury Stock", -128000, -118000, -10000],
        ["  Accumulated Other Comprehensive Income", 22750, 18750, 4000],
        ["  Non-controlling Interests", 15000, 11000, 4000],
        ["TOTAL SHAREHOLDERS' EQUITY", 4280000, 3476000, 804000],
        ["TOTAL LIABILITIES & EQUITY", 8300000, 6900000, 1400000],
    ]

    data = [header]
    for row in rows:
        if row[1] == "":
            data.append([row[0], "", "", ""])
        elif isinstance(row[1], int):
            data.append([row[0], fmt_dollar(row[1] * 1000), fmt_dollar(row[2] * 1000), fmt_dollar(row[3] * 1000)])
        else:
            data.append(row)

    col_w = [6.5 * cm, 3.5 * cm, 3.5 * cm, 3.0 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> All amounts in thousands of USD except par value. Goodwill increase of $400M "
        "reflects the DataFlow acquisition (Q1 2024) and IntelliServe acquisition (Q3 2024).",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> Treasury stock represents shares repurchased under the Board-authorized buyback "
        "program at weighted-average cost of $142.50 per share.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements




def build_cash_flow():
    """Table 3: Cash Flow Statement."""
    elements = []
    elements.append(Paragraph("Consolidated Statement of Cash Flows", style_heading1))
    elements.append(Paragraph(
        "The cash flow statement reflects Acme Corporation's cash generation and deployment during "
        "FY2024. Strong operating cash flow of $1.28 billion funded both strategic acquisitions and "
        "shareholder returns while maintaining balance sheet strength.",
        style_body,
    ))

    header = ["Category", "FY2024", "FY2023", "Change"]
    rows = [
        ["OPERATING ACTIVITIES", "", "", ""],
        ["  Net Income", 855000, 657000, 198000],
        ["  Depreciation & Amortization", 76000, 68000, 8000],
        ["  Stock-Based Compensation", 125000, 108000, 17000],
        ["  Deferred Income Taxes", 18000, 12000, 6000],
        ["  Amortization of Debt Issuance Costs", 3000, 3000, 0],
        ["  Loss on Disposal of Assets", 2000, 1000, 1000],
        ["  Changes in Working Capital:", "", "", ""],
        ["    Accounts Receivable", -127000, -95000, -32000],
        ["    Inventories", -6000, -8000, 2000],
        ["    Prepaid Expenses", -15000, -10000, -5000],
        ["    Accounts Payable", 45000, 32000, 13000],
        ["    Accrued Expenses", 45000, 28000, 17000],
        ["    Deferred Revenue", 125000, 98000, 27000],
        ["    Other Working Capital", 8000, 5000, 3000],
        ["Net Cash from Operations", 1154000, 899000, 255000],
        ["", "", "", ""],
        ["INVESTING ACTIVITIES", "", "", ""],
        ["  Capital Expenditures", -345000, -280000, -65000],
        ["  Acquisitions, net of cash", -520000, -180000, -340000],
        ["  Purchases of Investments", -195000, -150000, -45000],
        ["  Proceeds from Investment Sales", 65000, 42000, 23000],
        ["  Other Investing Activities", -8000, -5000, -3000],
        ["Net Cash Used in Investing", -1003000, -573000, -430000],
        ["", "", "", ""],
        ["FINANCING ACTIVITIES", "", "", ""],
        ["  Proceeds from Debt Issuance", 500000, 200000, 300000],
        ["  Debt Repayments", -200000, -150000, -50000],
        ["  Share Repurchases", -320000, -250000, -70000],
        ["  Dividends Paid", -300000, -260000, -40000],
        ["  Proceeds from Stock Options", 89000, 72000, 17000],
        ["  Other Financing Activities", -12000, -8000, -4000],
        ["Net Cash Used in Financing", -243000, -396000, 153000],
        ["", "", "", ""],
        ["Effect of Exchange Rates", 12000, -8000, 20000],
        ["Net Change in Cash", -80000, -78000, -2000],
        ["Cash at Beginning of Period", 2390000, 1968000, 422000],
        ["Cash at End of Period", 2310000, 1890000, 420000],
    ]

    data = [header]
    for row in rows:
        if row[1] == "":
            data.append([row[0], "", "", ""])
        elif isinstance(row[1], int):
            data.append([row[0], fmt_dollar(row[1] * 1000), fmt_dollar(row[2] * 1000), fmt_dollar(row[3] * 1000)])
        else:
            data.append(row)

    col_w = [7.0 * cm, 3.2 * cm, 3.2 * cm, 3.0 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Cash flow figures in thousands of USD. Free cash flow (Operating - CapEx) was "
        "$809M in FY2024 vs. $619M in FY2023, a 30.7% improvement.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_revenue_by_segment():
    """Table 4: Revenue by Business Segment."""
    elements = []
    elements.append(Paragraph("Revenue by Business Segment", style_heading1))
    elements.append(Paragraph(
        "Acme Corporation operates through five reportable segments. Enterprise Solutions remains the "
        "largest contributor, while Cloud Services demonstrated the fastest growth at 28.4% year-over-year, "
        "reflecting successful execution of our cloud-first strategy.",
        style_body,
    ))

    header = ["Segment", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "FY2024", "FY2023", "YoY %"]
    rows = [
        ["Enterprise Solutions", 412000, 435000, 452000, 481000, 1780000, 1620000],
        ["Cloud Services", 285000, 308000, 328000, 359000, 1280000, 997000],
        ["Data Analytics", 198000, 210000, 220000, 237000, 865000, 768000],
        ["Professional Services", 142000, 148000, 155000, 162000, 607000, 555000],
        ["Emerging Products", 66000, 71000, 73000, 78000, 288000, 250000],
        ["Total Revenue", 1103000, 1172000, 1228000, 1317000, 4820000, 4190000],
    ]

    data = [header]
    for row in rows:
        fy24, fy23 = row[5], row[6]
        yoy = ((fy24 - fy23) / fy23 * 100)
        formatted = [row[0]]
        for v in row[1:7]:
            formatted.append(fmt_dollar(v * 1000))
        formatted.append(fmt_pct(yoy))
        data.append(formatted)

    col_w = [3.8 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.4 * cm, 1.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Segment Operating Margins", style_heading2))
    margin_header = ["Segment", "FY2024 Margin", "FY2023 Margin", "Change (bps)"]
    margin_rows = [
        ["Enterprise Solutions", "26.8%", "24.5%", "+230"],
        ["Cloud Services", "18.2%", "15.8%", "+240"],
        ["Data Analytics", "31.5%", "29.2%", "+230"],
        ["Professional Services", "14.8%", "13.2%", "+160"],
        ["Emerging Products", "8.5%", "5.2%", "+330"],
        ["Consolidated", "23.1%", "21.0%", "+210"],
    ]
    margin_data = [margin_header] + margin_rows
    col_w2 = [4.5 * cm, 3.5 * cm, 3.5 * cm, 3.0 * cm]
    elements.append(make_table(margin_data, col_widths=col_w2))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Segment revenue is reported before inter-segment eliminations of $12M. "
        "Cloud Services growth driven by 45% increase in new enterprise cloud migrations.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_revenue_by_geography():
    """Table 5: Revenue by Geography."""
    elements = []
    elements.append(Paragraph("Revenue by Geographic Region", style_heading1))
    elements.append(Paragraph(
        "International expansion continued to accelerate in FY2024 with non-US revenue reaching 38% "
        "of total (up from 34% in FY2023). The APAC region showed particularly strong momentum following "
        "establishment of new operations in Singapore and Tokyo.",
        style_body,
    ))

    header = ["Region", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "FY2024", "FY2023", "YoY %"]
    rows = [
        ["United States", 672000, 712000, 742000, 790000, 2916000, 2690000],
        ["Western Europe", 165000, 178000, 188000, 205000, 736000, 640000],
        ["United Kingdom", 72000, 76000, 80000, 86000, 314000, 285000],
        ["Asia Pacific", 98000, 108000, 118000, 130000, 454000, 310000],
        ["Canada", 42000, 44000, 45000, 48000, 179000, 158000],
        ["Latin America", 25000, 28000, 30000, 32000, 115000, 62000],
        ["Middle East & Africa", 18000, 16000, 15000, 16000, 65000, 30000],
        ["Eastern Europe", 11000, 10000, 10000, 10000, 41000, 15000],
        ["Total Revenue", 1103000, 1172000, 1228000, 1317000, 4820000, 4190000],
    ]

    data = [header]
    for row in rows:
        fy24, fy23 = row[5], row[6]
        yoy = ((fy24 - fy23) / fy23 * 100)
        formatted = [row[0]]
        for v in row[1:7]:
            formatted.append(fmt_dollar(v * 1000))
        formatted.append(fmt_pct(yoy))
        data.append(formatted)

    col_w = [3.5 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.4 * cm, 2.4 * cm, 1.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Revenue attributed by customer billing location. Constant-currency revenue "
        "growth was 16.1% (vs. 14.3% reported) due to USD strengthening in H2 2024.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> Latin America growth of 85.5% reflects new market entry (Brazil, Mexico) in "
        "Q2 2024. Eastern Europe growth of 173.3% driven by establishment of Warsaw office in Q1 2024.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements




def build_opex_breakdown():
    """Table 6: Operating Expenses Breakdown."""
    elements = []
    elements.append(Paragraph("Operating Expenses Breakdown", style_heading1))
    elements.append(Paragraph(
        "Total operating expenses grew 12.0% year-over-year, below revenue growth of 14.3%, "
        "demonstrating continued operating leverage. The largest increase was in engineering headcount "
        "to support product development roadmap acceleration.",
        style_body,
    ))

    header = ["Category", "FY2024", "FY2023", "Change", "% of Revenue"]
    rows = [
        ["RESEARCH & DEVELOPMENT", "", "", "", ""],
        ["  Engineering Salaries & Benefits", 420000, 365000, 55000, "8.7%"],
        ["  Cloud Infrastructure (Dev/Test)", 95000, 82000, 13000, "2.0%"],
        ["  Software Licenses & Tools", 48000, 42000, 6000, "1.0%"],
        ["  Contracted R&D Services", 72000, 68000, 4000, "1.5%"],
        ["  R&D Facilities", 35000, 32000, 3000, "0.7%"],
        ["  Other R&D", 30000, 26000, 4000, "0.6%"],
        ["Subtotal R&D", 700000, 615000, 85000, "14.5%"],
        ["", "", "", "", ""],
        ["SALES & MARKETING", "", "", "", ""],
        ["  Sales Compensation & Commissions", 385000, 348000, 37000, "8.0%"],
        ["  Marketing Programs & Advertising", 168000, 152000, 16000, "3.5%"],
        ["  Partner Channel Costs", 98000, 85000, 13000, "2.0%"],
        ["  Travel & Entertainment", 72000, 62000, 10000, "1.5%"],
        ["  Sales Operations & Tools", 45000, 40000, 5000, "0.9%"],
        ["  Other S&M", 36000, 33000, 3000, "0.7%"],
        ["Subtotal Sales & Marketing", 804000, 720000, 84000, "16.7%"],
        ["", "", "", "", ""],
        ["GENERAL & ADMINISTRATIVE", "", "", "", ""],
        ["  Executive Compensation", 42000, 38000, 4000, "0.9%"],
        ["  Legal & Compliance", 68000, 62000, 6000, "1.4%"],
        ["  Finance & Accounting", 52000, 48000, 4000, "1.1%"],
        ["  IT & Security", 78000, 72000, 6000, "1.6%"],
        ["  Facilities & Office", 62000, 58000, 4000, "1.3%"],
        ["  Insurance", 18000, 16000, 2000, "0.4%"],
        ["  Other G&A", 27000, 24000, 3000, "0.6%"],
        ["Subtotal G&A", 347000, 318000, 29000, "7.2%"],
        ["", "", "", "", ""],
        ["Depreciation & Amortization", 76000, 68000, 8000, "1.6%"],
        ["TOTAL OPERATING EXPENSES", 1927000, 1721000, 206000, "40.0%"],
    ]

    data = [header]
    for row in rows:
        if row[1] == "":
            data.append([row[0], "", "", "", ""])
        elif isinstance(row[1], int):
            data.append([row[0], fmt_dollar(row[1] * 1000), fmt_dollar(row[2] * 1000),
                        fmt_dollar(row[3] * 1000), row[4]])
        else:
            data.append(row)

    col_w = [5.8 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm, 2.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Operating expenses in thousands of USD. Stock-based compensation of $125M is "
        "allocated: R&D $62M, S&M $38M, G&A $25M, and is included in respective category totals above.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_headcount():
    """Table 7: Headcount & Compensation."""
    elements = []
    elements.append(Paragraph("Headcount & Compensation Analysis", style_heading1))
    elements.append(Paragraph(
        "Acme Corporation's workforce grew 13.9% during FY2024, reaching 18,450 employees. "
        "Hiring was concentrated in engineering and customer-facing roles to support product development "
        "and geographic expansion. Employee retention remained strong at 91%.",
        style_body,
    ))

    header = ["Department", "FY2024 HC", "FY2023 HC", "Change", "Avg Comp ($K)", "Total Comp ($M)"]
    rows = [
        ["Engineering", 7200, 6100, 1100, 185, 1332],
        ["Product Management", 820, 720, 100, 175, 143],
        ["Sales", 3400, 3050, 350, 165, 561],
        ["Marketing", 1250, 1100, 150, 145, 181],
        ["Customer Success", 2100, 1850, 250, 128, 269],
        ["Professional Services", 1580, 1420, 160, 142, 224],
        ["General & Administrative", 980, 920, 60, 155, 152],
        ["Finance", 450, 420, 30, 162, 73],
        ["Legal & Compliance", 320, 290, 30, 178, 57],
        ["Human Resources", 280, 260, 20, 138, 39],
        ["IT & Security", 520, 480, 40, 158, 82],
        ["Executive Leadership", 50, 48, 2, 450, 23],
        ["Total", 18950, 16658, 2292, 168, 3136],
    ]

    data = [header]
    for row in rows:
        data.append([row[0], f"{row[1]:,}", f"{row[2]:,}", f"+{row[3]:,}" if row[3] > 0 else str(row[3]),
                    f"${row[4]:,}", f"${row[5]:,}"])

    col_w = [4.0 * cm, 2.2 * cm, 2.2 * cm, 2.0 * cm, 2.8 * cm, 2.8 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Compensation Mix Analysis", style_heading2))
    comp_header = ["Component", "FY2024 ($M)", "% of Total", "FY2023 ($M)", "% of Total"]
    comp_rows = [
        ["Base Salary", "$1,890", "60.3%", "$1,680", "61.2%"],
        ["Cash Bonus/Commission", "$532", "17.0%", "$468", "17.0%"],
        ["Stock-Based Compensation", "$445", "14.2%", "$372", "13.5%"],
        ["Benefits & Perquisites", "$198", "6.3%", "$172", "6.3%"],
        ["401(k) Match & Retirement", "$71", "2.3%", "$56", "2.0%"],
        ["Total Compensation", "$3,136", "100.0%", "$2,748", "100.0%"],
    ]
    comp_data = [comp_header] + comp_rows
    col_w2 = [4.2 * cm, 2.8 * cm, 2.2 * cm, 2.8 * cm, 2.2 * cm]
    elements.append(make_table(comp_data, col_widths=col_w2))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Headcount reflects full-time equivalents at fiscal year end. Does not include "
        "approximately 2,400 contractors and temporary staff.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_capex():
    """Table 8: Capital Expenditure."""
    elements = []
    elements.append(Paragraph("Capital Expenditure by Project", style_heading1))
    elements.append(Paragraph(
        "Capital expenditures totaled $345 million in FY2024, up 23.2% from the prior year. "
        "The increase primarily reflects investments in data center expansion and the new R&D campus. "
        "Management expects FY2025 CapEx of $380-420 million.",
        style_body,
    ))

    header = ["Project / Category", "FY2024", "FY2023", "Status", "Expected Completion"]
    rows = [
        ["Data Center - Virginia (Phase 2)", "$82,000", "$45,000", "In Progress", "Q2 2025"],
        ["Data Center - Frankfurt", "$65,000", "$38,000", "In Progress", "Q4 2025"],
        ["Data Center - Singapore", "$42,000", "$12,000", "In Progress", "Q1 2026"],
        ["R&D Campus - Austin", "$38,000", "$52,000", "Completed", "Q3 2024"],
        ["Network Infrastructure Upgrade", "$28,000", "$22,000", "In Progress", "Q2 2025"],
        ["Server & Storage Hardware", "$35,000", "$42,000", "Recurring", "Ongoing"],
        ["Security Systems Upgrade", "$12,000", "$8,000", "In Progress", "Q1 2025"],
        ["Office Renovations (3 sites)", "$15,000", "$18,000", "Completed", "Q4 2024"],
        ["Lab Equipment", "$8,000", "$12,000", "Recurring", "Ongoing"],
        ["Software Development Tools", "$7,000", "$5,000", "Recurring", "Ongoing"],
        ["Sustainability Initiatives", "$6,000", "$4,000", "In Progress", "Q4 2025"],
        ["Other Capital Projects", "$7,000", "$22,000", "Various", "Various"],
        ["Total Capital Expenditure", "$345,000", "$280,000", "", ""],
    ]

    data = [header] + rows
    col_w = [5.2 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 3.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Capital expenditure in thousands of USD. Amounts represent cash paid during "
        "the period; total project costs may span multiple fiscal years.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> Data center investments support cloud services capacity expansion. Virginia "
        "Phase 2 will add 50MW of compute capacity. Frankfurt and Singapore establish presence in "
        "EMEA and APAC respectively.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements




def build_debt_schedule():
    """Table 9: Debt Schedule."""
    elements = []
    elements.append(Paragraph("Debt Schedule & Maturity Profile", style_heading1))
    elements.append(Paragraph(
        "Acme Corporation maintains a diversified debt portfolio with a weighted-average interest rate "
        "of 4.2% and weighted-average maturity of 5.8 years. The company retains investment-grade "
        "ratings (BBB+ / Baa1) from S&P and Moody's respectively.",
        style_body,
    ))

    header = ["Instrument", "Principal ($M)", "Rate", "Maturity", "Callable", "Covenants"]
    rows = [
        ["Senior Notes 2026", "$200", "3.75%", "Mar 2026", "Yes", "Debt/EBITDA < 3.5x"],
        ["Senior Notes 2028", "$350", "4.25%", "Jun 2028", "Yes", "Debt/EBITDA < 3.5x"],
        ["Senior Notes 2030", "$300", "4.50%", "Sep 2030", "No", "Debt/EBITDA < 3.5x"],
        ["Senior Notes 2032", "$250", "4.75%", "Dec 2032", "No", "Debt/EBITDA < 3.5x"],
        ["Term Loan A", "$200", "SOFR+175bp", "Mar 2027", "Yes", "Interest Coverage > 4x"],
        ["Term Loan B", "$150", "SOFR+225bp", "Sep 2029", "Yes", "Interest Coverage > 4x"],
        ["Revolving Credit Facility", "$0/$500", "SOFR+125bp", "Jun 2028", "N/A", "Various"],
        ["Capital Lease Obligations", "$95", "5.2% avg", "Various", "N/A", "N/A"],
        ["Other Secured Debt", "$55", "4.8%", "Various", "No", "Asset coverage"],
        ["Total Debt", "$1,600", "4.2% avg", "", "", ""],
        ["Less: Current Portion", "($200)", "", "", "", ""],
        ["Long-term Debt", "$1,400", "", "", "", ""],
    ]

    data = [header] + rows
    col_w = [3.8 * cm, 2.5 * cm, 2.5 * cm, 2.2 * cm, 1.8 * cm, 3.8 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Debt Maturity Schedule", style_heading2))
    mat_header = ["Year", "Amount Due ($M)", "Cumulative ($M)", "% of Total"]
    mat_rows = [
        ["2025", "$0", "$0", "0.0%"],
        ["2026", "$200", "$200", "12.5%"],
        ["2027", "$200", "$400", "25.0%"],
        ["2028", "$350", "$750", "46.9%"],
        ["2029", "$150", "$900", "56.3%"],
        ["2030", "$300", "$1,200", "75.0%"],
        ["2031", "$0", "$1,200", "75.0%"],
        ["2032+", "$400", "$1,600", "100.0%"],
    ]
    mat_data = [mat_header] + mat_rows
    col_w2 = [3.0 * cm, 3.5 * cm, 3.5 * cm, 3.0 * cm]
    elements.append(make_table(mat_data, col_widths=col_w2))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Revolving credit facility has $500M capacity, fully undrawn as of Dec 31, 2024. "
        "The facility provides liquidity backstop and supports commercial paper program.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> All senior notes are unsecured obligations ranking pari passu. Interest payments "
        "are semi-annual. No financial covenant violations during FY2024.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_five_year_summary():
    """Table 10: Five-Year Financial Summary."""
    elements = []
    elements.append(Paragraph("Five-Year Financial Summary", style_heading1))
    elements.append(Paragraph(
        "The following table presents key financial metrics for the last five fiscal years, illustrating "
        "Acme Corporation's trajectory of revenue growth, margin expansion, and increasing returns "
        "to shareholders.",
        style_body,
    ))

    header = ["Metric", "FY2024", "FY2023", "FY2022", "FY2021", "FY2020"]
    rows = [
        ["Revenue ($M)", "$4,820", "$4,190", "$3,640", "$3,120", "$2,680"],
        ["Revenue Growth", "15.0%", "15.1%", "16.7%", "16.4%", "12.8%"],
        ["Gross Profit ($M)", "$3,042", "$2,602", "$2,220", "$1,872", "$1,581"],
        ["Gross Margin", "63.1%", "62.1%", "61.0%", "60.0%", "59.0%"],
        ["Operating Income ($M)", "$1,115", "$881", "$728", "$593", "$482"],
        ["Operating Margin", "23.1%", "21.0%", "20.0%", "19.0%", "18.0%"],
        ["Net Income ($M)", "$847", "$652", "$538", "$430", "$342"],
        ["Net Margin", "17.6%", "15.6%", "14.8%", "13.8%", "12.8%"],
        ["EPS (Diluted)", "$6.78", "$5.70", "$4.52", "$3.58", "$2.85"],
        ["", "", "", "", "", ""],
        ["Total Assets ($M)", "$8,300", "$6,900", "$5,820", "$4,950", "$4,280"],
        ["Total Debt ($M)", "$1,600", "$1,350", "$1,200", "$1,050", "$950"],
        ["Shareholders' Equity ($M)", "$4,280", "$3,476", "$2,920", "$2,450", "$2,080"],
        ["", "", "", "", "", ""],
        ["Operating Cash Flow ($M)", "$1,154", "$899", "$748", "$612", "$498"],
        ["Free Cash Flow ($M)", "$809", "$619", "$508", "$402", "$318"],
        ["CapEx ($M)", "$345", "$280", "$240", "$210", "$180"],
        ["", "", "", "", "", ""],
        ["Dividend Per Share", "$3.52", "$3.20", "$2.80", "$2.40", "$2.00"],
        ["Share Repurchases ($M)", "$320", "$250", "$180", "$120", "$80"],
        ["Total Shareholder Return", "$620", "$510", "$420", "$340", "$270"],
        ["", "", "", "", "", ""],
        ["Employees (FTE)", "18,450", "16,200", "14,100", "12,300", "10,800"],
        ["Revenue per Employee ($K)", "$261", "$259", "$258", "$254", "$248"],
        ["R&D as % of Revenue", "14.5%", "14.7%", "14.8%", "15.0%", "15.2%"],
    ]

    data = [header]
    for row in rows:
        data.append(row)

    col_w = [4.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Five-year CAGR: Revenue 15.8%, Operating Income 23.3%, EPS 24.2%, "
        "Free Cash Flow 26.2%. All figures reflect continuing operations.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_commentary(title, paragraphs):
    """Build a commentary section between tables."""
    elements = []
    elements.append(Paragraph(title, style_heading2))
    for p in paragraphs:
        elements.append(Paragraph(p, style_body))
    elements.append(Spacer(1, 4 * mm))
    return elements


def generate(output_path=None):
    """Build the full financial report PDF."""
    if output_path is None:
        output_path = OUTPUT_PATH
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    story = []
    story.extend(build_cover())
    story.extend(build_executive_summary())

    story.extend(build_commentary("Revenue Analysis", [
        "Acme Corporation achieved record revenue of $4.82 billion in fiscal year 2024, "
        "representing a 15% increase over the prior year. Growth was driven by strength "
        "in cloud services and enterprise software segments.",
    ]))
    story.extend(build_income_statement())

    story.extend(build_commentary("Balance Sheet Highlights", [
        "Total assets grew to $8.3 billion, reflecting continued investment in data center "
        "infrastructure and strategic acquisitions. The company maintains a strong liquidity "
        "position with $1.2 billion in cash and short-term investments.",
    ]))
    story.extend(build_balance_sheet())

    story.extend(build_commentary("Cash Flow Discussion", [
        "Operating cash flow increased 28% to $1.15 billion, demonstrating strong cash "
        "conversion from operating activities. Free cash flow of $809 million funded both "
        "dividends and share repurchases while maintaining investment-grade leverage ratios.",
    ]))
    story.extend(build_cash_flow())

    story.extend(build_commentary("Segment Performance", [
        "Cloud services remained the fastest-growing segment at 32% year-over-year, while "
        "enterprise software delivered steady mid-teens growth. Hardware revenue declined "
        "as expected due to the strategic shift toward recurring revenue models.",
    ]))
    story.extend(build_revenue_by_segment())

    story.extend(build_commentary("Geographic Expansion", [
        "International revenue grew 22% and now represents 42% of total revenue, up from "
        "38% in the prior year. EMEA was the standout region with 28% growth driven by "
        "new enterprise customer wins in Germany and the UK.",
    ]))
    story.extend(build_revenue_by_geography())

    story.extend(build_commentary("Operating Efficiency", [
        "Operating expenses as a percentage of revenue declined 200 basis points, reflecting "
        "scale benefits and disciplined cost management. R&D spending remained elevated at "
        "14.5% of revenue to support product roadmap initiatives.",
    ]))
    story.extend(build_opex_breakdown())

    story.extend(build_commentary("Workforce Development", [
        "Headcount grew 14% to 18,450 full-time equivalents. Engineering represents 45% of "
        "total headcount, reflecting the company's technology-first strategy. Voluntary "
        "attrition remained low at 8.2%.",
    ]))
    story.extend(build_headcount())

    story.extend(build_commentary("Capital Allocation", [
        "Capital expenditure of $345 million was directed primarily toward data center "
        "expansion and next-generation product development infrastructure. The Virginia "
        "data center Phase 2 project remains on track for completion in late 2025.",
    ]))
    story.extend(build_capex())

    story.extend(build_commentary("Debt Management", [
        "The company maintains an investment-grade credit profile with a net debt to EBITDA "
        "ratio of 1.1x. No near-term maturities require refinancing, and the undrawn "
        "revolving credit facility provides additional flexibility.",
    ]))
    story.extend(build_debt_schedule())

    story.extend(build_commentary("Long-Term Trajectory", [
        "The five-year summary demonstrates consistent execution against our strategic "
        "objectives: double-digit revenue growth, expanding margins, and increasing "
        "shareholder returns. We expect these trends to continue as cloud adoption "
        "accelerates across enterprise customers.",
    ]))
    story.extend(build_five_year_summary())

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2 * cm,
    )
    doc.build(story)
    print(f"Financial report written to {output_path}")
    return output_path


if __name__ == "__main__":
    generate()


def build_appendix():
    """Build appendix: Notes to Financial Statements (5-6 pages of dense text)."""
    elements = []
    elements.append(Paragraph("Appendix: Notes to Financial Statements", style_heading1))

    notes = [
        ("Note 1: Summary of Significant Accounting Policies", [
            "Basis of Presentation — The consolidated financial statements have been prepared in accordance "
            "with accounting principles generally accepted in the United States of America (U.S. GAAP) and "
            "include the accounts of Acme Corporation and its wholly-owned subsidiaries. All significant "
            "intercompany transactions and balances have been eliminated in consolidation.",
            "Revenue Recognition — The Company recognizes revenue in accordance with ASC 606, Revenue from "
            "Contracts with Customers. Revenue is recognized when control of promised goods or services is "
            "transferred to customers in an amount that reflects the consideration the Company expects to be "
            "entitled to in exchange for those goods or services. The Company identifies performance obligations "
            "in contracts with customers, determines transaction price, allocates the transaction price to "
            "performance obligations, and recognizes revenue as performance obligations are satisfied.",
            "For subscription-based services, revenue is recognized ratably over the contract term as the "
            "customer simultaneously receives and consumes the benefits. For perpetual software licenses, "
            "revenue is recognized at the point in time when the customer obtains control of the software. "
            "Professional services revenue is recognized as services are performed, typically on a "
            "time-and-materials or fixed-fee basis with progress measured using input methods.",
            "The Company's contracts often include multiple performance obligations. For such arrangements, "
            "the transaction price is allocated to each performance obligation based on relative standalone "
            "selling prices (SSP). SSP is determined using observable prices when available, or estimated "
            "using an adjusted market assessment approach or expected cost plus margin approach.",
        ]),
        ("Note 2: Business Combinations", [
            "DataFlow Acquisition — On February 15, 2024, the Company completed the acquisition of DataFlow "
            "Inc., a cloud-native data integration platform, for total consideration of $380 million in cash. "
            "The acquisition was accounted for using the acquisition method in accordance with ASC 805. "
            "The purchase price was allocated as follows: identifiable intangible assets $120 million "
            "(customer relationships $65M, developed technology $42M, trade names $13M), net tangible "
            "assets $28 million, and goodwill $232 million. Goodwill is attributable to the assembled "
            "workforce and expected synergies from combining DataFlow's technology with the Company's "
            "existing enterprise platform.",
            "IntelliServe Acquisition — On August 1, 2024, the Company acquired IntelliServe Technologies "
            "for $165 million in cash plus contingent consideration of up to $25 million based on "
            "achievement of revenue milestones over 24 months. The fair value of contingent consideration "
            "at the acquisition date was estimated at $18 million using a Monte Carlo simulation. "
            "Purchase price allocation resulted in goodwill of $98 million, intangible assets of $62 million, "
            "and net tangible assets of $23 million.",
            "Pro forma revenue for the combined entity, as if both acquisitions had occurred on January 1, 2024, "
            "would have been approximately $4.95 billion. Pro forma net income would have been approximately "
            "$860 million. These pro forma amounts are not necessarily indicative of results that would have "
            "been achieved had the acquisitions occurred at the beginning of the period.",
        ]),
        ("Note 3: Goodwill and Intangible Assets", [
            "Goodwill — The Company performs annual goodwill impairment testing during the fourth quarter "
            "or whenever events or changes in circumstances indicate the carrying amount may not be "
            "recoverable. The Company uses a quantitative assessment comparing the fair value of each "
            "reporting unit to its carrying amount. Fair value is determined using a combination of "
            "income approach (discounted cash flow) and market approach (comparable company multiples). "
            "No impairment was identified during FY2024.",
            "The changes in the carrying amount of goodwill by segment for FY2024 were: Enterprise Solutions "
            "increased from $580M to $720M (DataFlow allocation), Cloud Services increased from $420M to "
            "$520M (IntelliServe allocation), Data Analytics remained at $280M, and other segments remained "
            "at combined $140M. Total goodwill increased from $1,420M to $1,820M.",
            "Intangible Assets — Finite-lived intangible assets are amortized over their estimated useful "
            "lives: customer relationships (7-12 years), developed technology (4-7 years), trade names "
            "(5-10 years), and patents (remaining legal life, typically 8-15 years). Amortization expense "
            "was $52 million in FY2024 and $44 million in FY2023. Expected amortization over the next five "
            "years: FY2025 $58M, FY2026 $54M, FY2027 $48M, FY2028 $42M, FY2029 $35M.",
        ]),
        ("Note 4: Income Taxes", [
            "The provision for income taxes consists of current and deferred components. Current tax expense "
            "for FY2024 was $237 million (federal $185M, state $32M, international $20M). Deferred tax "
            "expense was $18 million, primarily related to temporary differences in depreciation methods, "
            "stock compensation timing, and acquisition-related intangible asset amortization.",
            "The Company's effective tax rate was 23.0% for FY2024, compared to 23.1% for FY2023. The rate "
            "differs from the U.S. federal statutory rate of 21% primarily due to state income taxes "
            "(net of federal benefit), non-deductible compensation, and research tax credits. The Company "
            "recognized $28 million in research and development tax credits during FY2024.",
            "Deferred tax assets of $92 million primarily relate to stock-based compensation ($35M), "
            "accrued liabilities ($28M), lease liabilities ($18M), and net operating loss carryforwards ($11M). "
            "Deferred tax liabilities of $135 million relate primarily to intangible assets from acquisitions "
            "($72M), right-of-use assets ($32M), and depreciation ($31M). Management has determined that "
            "no valuation allowance is necessary based on historical taxable income and projected future earnings.",
        ]),
        ("Note 5: Leases", [
            "The Company leases office space, data center facilities, and equipment under operating and "
            "finance lease arrangements. Operating lease costs were $98 million for FY2024. The weighted-average "
            "remaining lease term is 6.2 years and the weighted-average discount rate is 4.8%.",
            "Right-of-use assets under operating leases were $340 million as of December 31, 2024. "
            "Operating lease liabilities (current and non-current) totaled $362 million. Future minimum "
            "lease payments: FY2025 $82M, FY2026 $75M, FY2027 $68M, FY2028 $58M, FY2029 $48M, "
            "thereafter $72M, for total undiscounted payments of $403M less imputed interest of $41M.",
            "The Company also has finance leases for certain equipment with total obligations of $28 million. "
            "These are included in property, plant and equipment (net book value $22M) and in other "
            "liabilities. Depreciation of finance lease assets was $6 million in FY2024.",
        ]),
        ("Note 6: Stock-Based Compensation", [
            "The Company maintains equity incentive plans under which stock options, restricted stock units "
            "(RSUs), and performance stock units (PSUs) are granted to employees and directors. Total "
            "stock-based compensation expense was $125 million in FY2024 ($108M in FY2023), allocated "
            "to cost of revenue ($18M), R&D ($62M), sales and marketing ($38M), and G&A ($25M).",
            "As of December 31, 2024, unrecognized compensation cost related to unvested awards was "
            "$285 million, expected to be recognized over a weighted-average period of 2.8 years. "
            "During FY2024, the Company granted 1.8 million RSUs (weighted-average fair value $142) and "
            "0.4 million PSUs (weighted-average fair value $168, based on Monte Carlo valuation). "
            "Stock options outstanding were 2.1 million with weighted-average exercise price of $98 and "
            "weighted-average remaining term of 4.2 years.",
            "The fair value of stock options granted is estimated using the Black-Scholes model with the "
            "following weighted-average assumptions: risk-free rate 4.2%, expected volatility 32%, "
            "expected dividend yield 2.4%, and expected term 5.5 years. PSU fair values are estimated "
            "using Monte Carlo simulations incorporating total shareholder return targets relative to the "
            "S&P 500 Technology Index over a three-year performance period.",
        ]),
        ("Note 7: Segment Information", [
            "The Company operates in five reportable segments as determined by the Chief Operating Decision "
            "Maker (CODM): Enterprise Solutions, Cloud Services, Data Analytics, Professional Services, "
            "and Emerging Products. Segment performance is evaluated based on segment operating income, "
            "which excludes corporate overhead allocations, acquisition-related costs, and restructuring charges.",
            "Inter-segment revenues are transacted at fair market value and eliminated in consolidation. "
            "Total inter-segment revenue was $12 million in FY2024. Corporate and unallocated costs of "
            "$45 million include executive compensation, corporate development, and investor relations. "
            "The CODM does not review segment assets; accordingly, total assets are not presented by segment.",
            "Geographic revenue information is determined by customer billing location. Long-lived assets "
            "by geography: United States $980M, Western Europe $145M, Asia Pacific $85M, Other $35M. "
            "No single customer accounted for more than 3% of consolidated revenue in FY2024 or FY2023.",
        ]),
        ("Note 8: Commitments and Contingencies", [
            "Legal Proceedings — The Company is involved in various legal proceedings arising in the ordinary "
            "course of business. While outcomes cannot be predicted with certainty, management believes that "
            "the ultimate resolution of pending matters will not have a material adverse effect on the "
            "Company's consolidated financial position or results of operations. The Company has accrued "
            "$15 million for probable and estimable losses related to pending litigation.",
            "Purchase Commitments — The Company has non-cancelable purchase commitments for cloud "
            "infrastructure services totaling $850 million over the next five years ($180M in FY2025, "
            "$185M in FY2026, $175M in FY2027, $165M in FY2028, and $145M in FY2029). These commitments "
            "were entered into to secure favorable pricing and capacity guarantees.",
            "Indemnification — In the ordinary course of business, the Company enters into agreements that "
            "contain indemnification provisions. The Company has not incurred material costs as a result of "
            "such indemnifications and has not accrued any liabilities related to such obligations.",
            "Warranties — The Company provides standard warranties on its products for periods of 12-36 months. "
            "Warranty accruals totaled $8 million as of December 31, 2024, based on historical claim rates "
            "and estimated repair costs.",
        ]),
    ]

    for title_text, paras in notes:
        elements.append(Paragraph(title_text, style_heading2))
        for p in paras:
            elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 3 * mm))

    elements.append(PageBreak())
    return elements




def build_financial_ratios():
    """Build Financial Ratios table at the end."""
    elements = []
    elements.append(Paragraph("Financial Ratios & Key Metrics", style_heading1))
    elements.append(Paragraph(
        "The following table presents key financial ratios used by management and investors to assess "
        "Acme Corporation's profitability, liquidity, efficiency, and leverage position.",
        style_body,
    ))

    header = ["Ratio / Metric", "FY2024", "FY2023", "FY2022", "Industry Avg"]

    profitability = [
        ["PROFITABILITY RATIOS", "", "", "", ""],
        ["Gross Margin", "63.1%", "62.1%", "61.0%", "58.5%"],
        ["Operating Margin", "23.1%", "21.0%", "20.0%", "18.2%"],
        ["Net Profit Margin", "17.6%", "15.6%", "14.8%", "14.0%"],
        ["Return on Equity (ROE)", "21.8%", "20.4%", "19.5%", "16.8%"],
        ["Return on Assets (ROA)", "11.1%", "10.3%", "9.8%", "8.5%"],
        ["Return on Invested Capital (ROIC)", "18.5%", "17.2%", "16.5%", "14.2%"],
        ["EBITDA Margin", "24.7%", "22.7%", "21.5%", "20.0%"],
        ["", "", "", "", ""],
        ["LIQUIDITY RATIOS", "", "", "", ""],
        ["Current Ratio", "2.33x", "2.29x", "2.25x", "1.85x"],
        ["Quick Ratio", "2.17x", "2.13x", "2.10x", "1.62x"],
        ["Cash Ratio", "1.64x", "1.59x", "1.52x", "1.20x"],
        ["Operating Cash Flow Ratio", "0.69x", "0.63x", "0.60x", "0.55x"],
        ["", "", "", "", ""],
        ["EFFICIENCY RATIOS", "", "", "", ""],
        ["Days Sales Outstanding (DSO)", "67.5", "66.7", "65.2", "72.0"],
        ["Days Payable Outstanding (DPO)", "42.8", "43.5", "44.0", "45.0"],
        ["Asset Turnover", "0.63x", "0.66x", "0.68x", "0.58x"],
        ["Inventory Turnover", "14.3x", "13.5x", "12.8x", "10.5x"],
        ["Revenue per Employee ($K)", "$261", "$259", "$258", "$225"],
        ["", "", "", "", ""],
        ["LEVERAGE RATIOS", "", "", "", ""],
        ["Debt-to-Equity", "0.37x", "0.39x", "0.41x", "0.55x"],
        ["Debt-to-EBITDA", "1.34x", "1.42x", "1.53x", "2.10x"],
        ["Net Debt-to-EBITDA", "-0.42x", "-0.25x", "-0.08x", "1.40x"],
        ["Interest Coverage", "24.2x", "16.9x", "14.8x", "12.0x"],
        ["Equity Multiplier", "1.94x", "1.98x", "1.99x", "2.20x"],
        ["", "", "", "", ""],
        ["VALUATION METRICS", "", "", "", ""],
        ["Price-to-Earnings (P/E)", "22.8x", "20.5x", "18.2x", "25.0x"],
        ["EV/EBITDA", "15.2x", "14.0x", "12.8x", "16.5x"],
        ["Price-to-Book", "4.5x", "3.8x", "3.4x", "5.2x"],
        ["Price-to-Sales", "3.9x", "3.2x", "2.7x", "4.0x"],
        ["Free Cash Flow Yield", "4.5%", "4.8%", "5.2%", "3.8%"],
        ["Dividend Yield", "2.3%", "2.7%", "2.9%", "1.5%"],
        ["Payout Ratio", "41.5%", "43.8%", "45.0%", "35.0%"],
    ]

    data = [header] + profitability
    col_w = [5.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.8 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Industry averages based on peer group of 15 enterprise software companies with "
        "revenue >$2B. Valuation metrics use closing share price as of Dec 31 of respective year.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> Net Debt = Total Debt - Cash & Equivalents - Short-term Investments. "
        "Negative Net Debt-to-EBITDA indicates net cash position.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>3</super> ROIC calculated as NOPAT / (Total Equity + Net Debt). Interest coverage = "
        "Operating Income / Interest Expense.",
        style_footnote,
    ))
    return elements


def build_quarterly_metrics():
    """Additional detailed quarterly KPI table."""
    elements = []
    elements.append(Paragraph("Quarterly Key Performance Indicators", style_heading1))
    elements.append(Paragraph(
        "The following operational metrics provide insight into the underlying health and momentum of "
        "Acme Corporation's business. Management reviews these KPIs monthly and reports them to the "
        "Board of Directors on a quarterly basis.",
        style_body,
    ))

    header = ["KPI", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q4 2023"]
    rows = [
        ["CUSTOMER METRICS", "", "", "", "", ""],
        ["Total Enterprise Customers", "4,050", "4,180", "4,320", "4,480", "3,850"],
        ["Net New Customers", "85", "130", "140", "160", "120"],
        ["Customer Churn Rate", "1.2%", "1.1%", "1.0%", "0.9%", "1.4%"],
        ["Net Revenue Retention", "118%", "119%", "121%", "122%", "115%"],
        ["Annual Recurring Revenue ($M)", "$3,280", "$3,420", "$3,580", "$3,750", "$2,920"],
        ["Average Contract Value ($K)", "$285", "$292", "$298", "$305", "$265"],
        ["", "", "", "", "", ""],
        ["PRODUCT METRICS", "", "", "", "", ""],
        ["Monthly Active Users (MAU, K)", "2,850", "3,020", "3,180", "3,350", "2,420"],
        ["API Calls per Day (Billions)", "4.2", "4.8", "5.3", "5.9", "3.5"],
        ["Platform Uptime", "99.97%", "99.98%", "99.99%", "99.97%", "99.95%"],
        ["Avg Response Time (ms)", "42", "38", "35", "33", "52"],
        ["Data Processed (PB/month)", "12.5", "14.2", "15.8", "17.5", "9.8"],
        ["", "", "", "", "", ""],
        ["SALES METRICS", "", "", "", "", ""],
        ["Bookings ($M)", "$1,250", "$1,380", "$1,420", "$1,550", "$1,120"],
        ["Pipeline ($B)", "$4.2", "$4.5", "$4.8", "$5.1", "$3.8"],
        ["Win Rate", "32%", "34%", "35%", "36%", "30%"],
        ["Sales Cycle (days)", "85", "82", "78", "76", "92"],
        ["Quota Attainment", "92%", "98%", "102%", "108%", "88%"],
        ["", "", "", "", "", ""],
        ["EFFICIENCY METRICS", "", "", "", "", ""],
        ["CAC Payback (months)", "18", "17", "16", "15", "22"],
        ["LTV/CAC Ratio", "4.2x", "4.5x", "4.8x", "5.1x", "3.6x"],
        ["Magic Number", "1.12", "1.18", "1.22", "1.28", "0.95"],
        ["Rule of 40 Score", "38%", "40%", "42%", "44%", "34%"],
        ["Gross Dollar Retention", "96%", "97%", "97%", "97%", "95%"],
    ]

    data = [header] + rows
    col_w = [4.5 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm]
    elements.append(make_table(data, col_widths=col_w))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> ARR calculated as annualized value of all active subscription and maintenance "
        "contracts at period end. Net Revenue Retention includes expansion, contraction, and churn.",
        style_footnote,
    ))
    elements.append(Paragraph(
        "<super>2</super> Rule of 40 = Revenue Growth Rate + FCF Margin. Magic Number = Net New ARR / "
        "Prior Period S&M Spend. LTV calculated using 5-year discounted cash flow methodology.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_risk_factors():
    """Build a risk factors section with detailed discussion."""
    elements = []
    elements.append(Paragraph("Risk Factors & Mitigation Strategies", style_heading1))
    
    risks = [
        ("Market & Competition Risk", 
         "The enterprise software market is highly competitive with both established players and emerging "
         "startups. Key competitors include large platform companies with substantial resources and smaller "
         "specialized vendors that may offer point solutions at lower price points. The Company mitigates "
         "this risk through continuous R&D investment ($700M in FY2024), strong customer relationships "
         "(91% retention), and a comprehensive product portfolio that creates switching costs. The Company "
         "monitors competitive dynamics through a dedicated market intelligence team and adjusts pricing "
         "and feature roadmaps accordingly."),
        ("Technology & Cybersecurity Risk",
         "The Company's operations depend on complex technology infrastructure including cloud platforms, "
         "data centers, and network connectivity. Cybersecurity threats continue to evolve in sophistication "
         "and frequency. A significant breach or service outage could damage customer trust and result in "
         "regulatory penalties. Mitigation includes: $78M annual security investment, SOC 2 Type II "
         "certification, ISO 27001 compliance, regular penetration testing, a 24/7 security operations "
         "center, cyber insurance coverage of $200M, and an incident response plan tested quarterly."),
        ("Macroeconomic & Geopolitical Risk",
         "Global economic conditions, including inflation, interest rates, and recession risk, may affect "
         "customer IT spending decisions. Geopolitical tensions could disrupt operations in certain regions "
         "or limit market access. With 38% international revenue, currency fluctuations present translation "
         "risk. Mitigation strategies include geographic diversification, multi-year contracts with annual "
         "escalators, a hedging program covering 70% of forecasted non-USD revenue, and flexible cost "
         "structures that allow rapid adjustment if demand deteriorates."),
        ("Regulatory & Compliance Risk",
         "The Company operates in a complex regulatory environment spanning data privacy (GDPR, CCPA, "
         "emerging state laws), AI governance, export controls, tax policy, and industry-specific regulations "
         "(HIPAA, SOX, FedRAMP). Evolving regulations, particularly around AI and data sovereignty, could "
         "require significant product modifications or limit market opportunities. The Company employs a "
         "legal and compliance team of 320 professionals, invests $68M annually in compliance functions, "
         "and maintains proactive engagement with regulators and industry bodies."),
        ("Talent & Human Capital Risk",
         "The Company's success depends on attracting and retaining skilled professionals, particularly "
         "in engineering, data science, and AI/ML. Competition for technical talent remains intense, "
         "and labor markets in key technology hubs face structural supply constraints. Mitigation includes "
         "competitive total compensation (targeted at 75th percentile), equity programs vesting over 4 years, "
         "flexible work arrangements, internal mobility programs, partnerships with 35 universities, and "
         "investment in employee development ($45M in FY2024). Current voluntary attrition of 9% is below "
         "industry average of 15%."),
        ("Acquisition Integration Risk",
         "The Company actively pursues acquisitions to expand capabilities and market reach. Integration "
         "of acquired businesses involves risks including: cultural alignment, technology platform "
         "consolidation, customer retention, and realization of projected synergies. In FY2024, two "
         "acquisitions totaling $545M in consideration were completed. The Company has a dedicated "
         "integration management office with standardized playbooks and has successfully integrated "
         "8 acquisitions over the past 5 years, achieving synergy targets in 7 of 8 cases."),
    ]

    for title_text, body_text in risks:
        elements.append(Paragraph(title_text, style_heading2))
        elements.append(Paragraph(body_text, style_body))
        elements.append(Spacer(1, 3 * mm))

    elements.append(PageBreak())
    return elements


def build_esg_section():
    """Build ESG (Environmental, Social, Governance) section."""
    elements = []
    elements.append(Paragraph("Environmental, Social & Governance (ESG) Report", style_heading1))
    elements.append(Paragraph(
        "Acme Corporation is committed to sustainable business practices that create long-term value "
        "for all stakeholders. The following summarizes our ESG performance and commitments.",
        style_body,
    ))

    elements.append(Paragraph("Environmental Metrics", style_heading2))
    env_header = ["Metric", "FY2024", "FY2023", "Target 2025", "Target 2030"]
    env_rows = [
        ["Total Carbon Emissions (tCO2e)", "45,200", "52,800", "38,000", "15,000"],
        ["Scope 1 (Direct)", "3,200", "3,800", "2,500", "1,000"],
        ["Scope 2 (Electricity)", "22,000", "28,000", "18,000", "5,000"],
        ["Scope 3 (Value Chain)", "20,000", "21,000", "17,500", "9,000"],
        ["Renewable Energy %", "72%", "58%", "85%", "100%"],
        ["Data Center PUE", "1.25", "1.32", "1.20", "1.10"],
        ["Water Usage (ML)", "180", "195", "160", "100"],
        ["E-Waste Recycled (%)", "94%", "88%", "97%", "99%"],
    ]
    env_data = [env_header] + env_rows
    col_w = [5.0 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]
    elements.append(make_table(env_data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Social & Workforce Metrics", style_heading2))
    soc_header = ["Metric", "FY2024", "FY2023", "Industry Avg"]
    soc_rows = [
        ["Employee Satisfaction Score", "4.2/5.0", "4.0/5.0", "3.8/5.0"],
        ["Gender Diversity (% Women)", "38%", "36%", "30%"],
        ["Leadership Diversity (% Women)", "32%", "28%", "24%"],
        ["Ethnic Diversity (% URM in US)", "28%", "25%", "20%"],
        ["Pay Equity Ratio (Women:Men)", "0.98", "0.96", "0.92"],
        ["Training Hours per Employee", "42", "36", "28"],
        ["Safety Incident Rate (per 100)", "0.12", "0.15", "0.35"],
        ["Community Investment ($M)", "$18", "$15", "$10"],
        ["Volunteer Hours (thousands)", "85", "72", "45"],
    ]
    soc_data = [soc_header] + soc_rows
    col_w2 = [5.0 * cm, 2.8 * cm, 2.8 * cm, 2.8 * cm]
    elements.append(make_table(soc_data, col_widths=col_w2))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Governance Highlights", style_heading2))
    gov_text = [
        "Board Composition: 11 directors, 9 independent (82%), 4 women (36%), average tenure 5.2 years. "
        "All committees (Audit, Compensation, Nominating) are fully independent. The Board conducted "
        "an external effectiveness review in FY2024 and implemented recommendations around cybersecurity "
        "oversight and AI governance.",
        "Executive Compensation: CEO pay ratio of 85:1 (median employee). 70% of executive compensation "
        "is performance-based (50% PSUs + 20% cash incentive). Performance metrics include revenue growth, "
        "operating margin, relative TSR, and ESG targets (10% weighting introduced in FY2024). "
        "Clawback provisions apply to all Section 16 officers for material restatements.",
        "Ethics & Compliance: Zero tolerance policy for bribery and corruption. Annual ethics training "
        "completion rate of 99.8%. Whistleblower hotline received 42 reports in FY2024 (all investigated, "
        "3 substantiated resulting in disciplinary action). No material legal proceedings related to "
        "governance failures.",
    ]
    for text in gov_text:
        elements.append(Paragraph(text, style_body))
    
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Carbon emissions independently verified by EcoAudit LLC. Scope 3 includes "
        "employee commuting, business travel, and upstream cloud provider emissions.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_additional_appendix():
    """Build additional appendix notes to add page count."""
    elements = []
    elements.append(Paragraph("Additional Notes to Financial Statements (Continued)", style_heading1))

    notes = [
        ("Note 9: Fair Value Measurements", [
            "The Company measures certain financial instruments at fair value on a recurring basis using "
            "a three-level hierarchy: Level 1 (quoted prices in active markets), Level 2 (observable inputs "
            "other than Level 1 prices), and Level 3 (unobservable inputs). As of December 31, 2024:",
            "Level 1 assets totaled $2,760M: cash equivalents ($2,310M consisting of money market funds "
            "and Treasury bills) and short-term investments ($450M in publicly traded equity securities "
            "and investment-grade corporate bonds with maturities under 12 months).",
            "Level 2 assets totaled $280M: long-term investments comprising corporate bonds ($180M) and "
            "government agency securities ($100M), valued using quoted prices for similar instruments, "
            "benchmark yield curves, and credit spreads. Foreign currency derivatives ($8M notional) are "
            "also classified as Level 2, valued using observable forward exchange rates.",
            "Level 3 liabilities totaled $18M: contingent consideration from the IntelliServe acquisition, "
            "valued using a Monte Carlo simulation with key inputs including projected revenue growth "
            "(15-25% range), revenue volatility (20%), discount rate (12%), and probability of milestone "
            "achievement (65-80%). A 5% increase in projected growth rates would increase the liability "
            "by approximately $3M.",
        ]),
        ("Note 10: Derivatives and Hedging Activities", [
            "The Company uses derivative financial instruments to manage exposure to foreign currency "
            "fluctuations and interest rate risk. All derivatives are recorded at fair value on the "
            "balance sheet. The Company does not use derivatives for speculative purposes.",
            "Foreign Currency Hedges: The Company enters into forward contracts and options to hedge "
            "forecasted international revenue. As of December 31, 2024, outstanding foreign currency "
            "contracts had a total notional value of $420M (EUR $185M, GBP $95M, JPY $68M, AUD $42M, "
            "other $30M). These are designated as cash flow hedges with gains/losses recorded in AOCI "
            "and reclassified to revenue when the hedged transaction occurs. Net unrealized gain in AOCI "
            "related to currency hedges was $12M at year-end.",
            "Interest Rate Risk: The Company has interest rate swaps with notional value of $350M "
            "converting floating-rate debt to fixed rate (weighted-average fixed rate of 4.1%). "
            "These swaps are designated as cash flow hedges. A 100bp increase in SOFR would result "
            "in approximately $5M additional annual interest expense on unhedged floating-rate debt.",
            "Hedge effectiveness is assessed prospectively using regression analysis and retrospectively "
            "using the dollar-offset method. All hedges remained highly effective (within 80-125% range) "
            "throughout FY2024. No amounts were reclassified from AOCI to earnings due to hedge "
            "discontinuation.",
        ]),
        ("Note 11: Revenue Disaggregation", [
            "The following provides additional disaggregation of revenue beyond segment and geographic "
            "breakdowns presented elsewhere in this report:",
            "By deployment model: Cloud/SaaS revenue was $2,890M (60% of total), On-premise license "
            "revenue was $1,045M (22%), and Hybrid deployment revenue was $885M (18%). Cloud/SaaS grew "
            "24% YoY while on-premise declined 3% as customers continue migrating to cloud.",
            "By contract duration: Multi-year contracts (2+ years) represented 58% of new bookings in "
            "FY2024 (up from 52% in FY2023), with average contract duration of 2.8 years. Single-year "
            "contracts represented 35% and usage-based arrangements 7%. Remaining performance obligations "
            "(backlog) totaled $6.2B as of December 31, 2024, of which approximately 55% is expected to "
            "be recognized as revenue over the next 12 months.",
            "By customer size: Large enterprise (>$1M ACV) represented 52% of revenue from 420 customers. "
            "Mid-market ($100K-$1M ACV) represented 35% from 2,800 customers. SMB (<$100K ACV) represented "
            "13% from 1,260 customers. Large enterprise grew 18% YoY while mid-market grew 14% and SMB "
            "grew 8%.",
        ]),
        ("Note 12: Subsequent Events", [
            "The Company has evaluated subsequent events through March 15, 2025, the date these financial "
            "statements were available to be issued.",
            "On January 22, 2025, the Company entered into a definitive agreement to acquire NeuralTech "
            "Systems Inc. for approximately $280 million in cash, subject to customary closing conditions "
            "and regulatory approvals. The acquisition is expected to close in Q2 2025 and will be funded "
            "from available cash balances. NeuralTech's AI model optimization technology will complement "
            "the Company's existing AI/ML product portfolio.",
            "On February 5, 2025, the Board of Directors declared a quarterly dividend of $0.92 per share "
            "(reflecting the 15% increase announced in December 2024), payable March 28, 2025 to "
            "shareholders of record as of March 14, 2025.",
            "On February 28, 2025, the Company completed a secondary offering of 2 million shares held "
            "by certain pre-IPO investors at $155 per share. The Company did not receive any proceeds from "
            "this offering. The selling shareholders included venture capital funds whose lock-up periods "
            "expired in January 2025.",
            "No other events requiring recognition or disclosure in the financial statements were identified.",
        ]),
        ("Note 13: Related Party Transactions", [
            "The Company enters into transactions with related parties in the ordinary course of business. "
            "All related party transactions are conducted on arm's-length terms and approved by the Audit "
            "Committee in accordance with the Company's Related Party Transaction Policy.",
            "During FY2024, the Company paid $4.2M in fees to Vertex Consulting Group, a firm in which "
            "Board member Sarah Chen holds a 12% ownership interest. Services provided included strategic "
            "advisory on the APAC market entry. Ms. Chen recused herself from all Board discussions and "
            "votes related to this engagement.",
            "The Company leases office space in Austin, TX from Meridian Real Estate Partners, an entity "
            "in which CEO James Mitchell holds a 5% limited partnership interest. Annual lease payments "
            "are $2.8M, which represents market rate for comparable Class A office space in the area as "
            "confirmed by an independent real estate appraisal. The lease was entered into in 2019 before "
            "Mr. Mitchell's appointment as CEO.",
            "Executive loans: No loans to officers or directors were outstanding during FY2024 or as of "
            "December 31, 2024. The Company's policy prohibits personal loans to executive officers in "
            "compliance with Section 402 of the Sarbanes-Oxley Act.",
        ]),
        ("Note 14: Concentration of Credit Risk", [
            "Financial instruments that potentially subject the Company to concentration of credit risk "
            "consist primarily of cash, short-term investments, and trade accounts receivable. Cash "
            "deposits exceed FDIC insurance limits; the Company mitigates this risk by maintaining accounts "
            "with multiple high-quality financial institutions and investing in highly-rated money market "
            "funds and U.S. Treasury securities.",
            "No single customer represented more than 3% of revenue or 4% of accounts receivable in "
            "FY2024 or FY2023. The Company's top 10 customers accounted for approximately 18% of total "
            "revenue. Credit losses have historically been immaterial, with bad debt expense of $3.2M in "
            "FY2024 (0.07% of revenue) and $2.8M in FY2023 (0.07% of revenue).",
            "The Company performs ongoing credit evaluations of customers and generally does not require "
            "collateral. Allowance for doubtful accounts was $12M as of December 31, 2024, determined "
            "using the current expected credit loss (CECL) methodology based on historical loss rates, "
            "current conditions, and reasonable forecasts. Aging analysis: 0-30 days $680M (76%), "
            "31-60 days $142M (16%), 61-90 days $48M (5%), >90 days $22M (3%, of which $12M reserved).",
        ]),
    ]

    for title_text, paras in notes:
        elements.append(Paragraph(title_text, style_heading2))
        for p in paras:
            elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 3 * mm))

    elements.append(PageBreak())
    return elements


def build_management_responsibility():
    """Build management responsibility statement and auditor note."""
    elements = []
    elements.append(Paragraph("Management's Responsibility for Financial Reporting", style_heading1))
    
    paras = [
        "The management of Acme Corporation is responsible for the preparation and fair presentation "
        "of these consolidated financial statements in accordance with accounting principles generally "
        "accepted in the United States of America. This responsibility includes the design, implementation, "
        "and maintenance of internal controls relevant to the preparation and fair presentation of "
        "financial statements that are free from material misstatement, whether due to fraud or error.",

        "Management has assessed the effectiveness of the Company's internal control over financial "
        "reporting as of December 31, 2024, based on the criteria established in Internal Control — "
        "Integrated Framework (2013) issued by the Committee of Sponsoring Organizations of the Treadway "
        "Commission (COSO). Based on this assessment, management has concluded that the Company's internal "
        "control over financial reporting was effective as of December 31, 2024.",

        "The Company's internal controls include: (i) maintaining records that accurately and fairly reflect "
        "transactions and dispositions of assets; (ii) providing reasonable assurance that transactions are "
        "recorded as necessary to permit preparation of financial statements in accordance with GAAP; "
        "(iii) providing reasonable assurance regarding prevention or timely detection of unauthorized "
        "acquisition, use, or disposition of assets; and (iv) providing reasonable assurance regarding "
        "the reliability of financial reporting.",

        "The Audit Committee of the Board of Directors, composed entirely of independent directors, "
        "meets regularly with management and the independent auditors to discuss the Company's financial "
        "reporting, internal controls, and audit matters. The independent auditors have full and free "
        "access to the Audit Committee.",
    ]

    for p in paras:
        elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 2 * mm))

    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph("Independent Auditor's Report (Summary)", style_heading2))
    
    auditor_paras = [
        "To the Board of Directors and Shareholders of Acme Corporation:",

        "Opinion — We have audited the accompanying consolidated financial statements of Acme Corporation "
        "and subsidiaries, which comprise the consolidated balance sheet as of December 31, 2024 and 2023, "
        "the related consolidated statements of income, comprehensive income, stockholders' equity, and "
        "cash flows for the years then ended, and the related notes. In our opinion, the consolidated "
        "financial statements present fairly, in all material respects, the financial position of Acme "
        "Corporation as of December 31, 2024 and 2023, and the results of its operations and its cash "
        "flows for the years then ended, in conformity with U.S. GAAP.",

        "Basis for Opinion — We conducted our audits in accordance with the standards of the Public "
        "Company Accounting Oversight Board (PCAOB). Those standards require that we plan and perform "
        "the audit to obtain reasonable assurance about whether the financial statements are free of "
        "material misstatement, whether due to error or fraud. Our audits included performing procedures "
        "to assess the risks of material misstatement, examining evidence supporting the amounts and "
        "disclosures, evaluating accounting principles used and significant estimates made by management, "
        "and evaluating overall financial statement presentation.",

        "Critical Audit Matters — The critical audit matters communicated below are matters arising from "
        "the current period audit that were communicated to the Audit Committee and that: (1) relate to "
        "accounts or disclosures that are material to the financial statements and (2) involved especially "
        "challenging, subjective, or complex auditor judgment.",

        "Revenue Recognition for Multi-Element Arrangements — As described in Note 1, the Company enters "
        "into contracts with multiple performance obligations requiring allocation of transaction price "
        "based on relative standalone selling prices. For certain bundled arrangements, SSP is not directly "
        "observable and must be estimated. We identified this as a critical audit matter due to the "
        "significant judgment involved in SSP estimation and its impact on revenue timing. Our procedures "
        "included evaluating management's SSP methodology, testing a sample of contracts for appropriate "
        "allocation, and assessing whether revenue was recognized in the correct period.",

        "Goodwill Impairment Assessment — As described in Note 3, the Company has $1.82B in goodwill "
        "across multiple reporting units. The annual impairment test requires significant management "
        "judgment regarding assumptions such as revenue growth rates, discount rates, and terminal values. "
        "We involved our valuation specialists to evaluate the reasonableness of management's fair value "
        "estimates, tested key assumptions against market data and historical performance, and performed "
        "sensitivity analyses on critical inputs.",

        "We have served as the Company's auditor since 2015.",

        "Deloitte & Young LLP\nSan Francisco, California\nMarch 15, 2025",
    ]

    for p in auditor_paras:
        elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 2 * mm))

    elements.append(PageBreak())
    return elements


def build_shareholder_letter():
    """Build a letter to shareholders (2 pages)."""
    elements = []
    elements.append(Paragraph("Letter to Shareholders", style_heading1))
    
    paras = [
        "Dear Fellow Shareholders,",

        "I am pleased to report that Fiscal Year 2024 was an exceptional year for Acme Corporation, "
        "marking our fifth consecutive year of double-digit revenue growth and margin expansion. Our team "
        "delivered outstanding results across every dimension of our business — financial performance, "
        "product innovation, customer success, and talent development.",

        "When I reflect on what we accomplished this year, several achievements stand out. First, we "
        "crossed the $3.75 billion annual recurring revenue threshold, a milestone that underscores the "
        "durability and predictability of our business model. Second, we successfully integrated two "
        "strategic acquisitions that significantly strengthen our competitive position in cloud services "
        "and AI-powered analytics. Third, we expanded into six new international markets while maintaining "
        "our industry-leading net revenue retention rate of 122%.",

        "Our financial results speak to the strength of our execution. Revenue grew 14.3% to $4.82 billion, "
        "operating income increased 26.6% to $1.12 billion, and earnings per share grew 19.0% to $6.78. "
        "These results exceeded the guidance we provided at the beginning of the year, reflecting both "
        "strong end-market demand and disciplined operational execution.",

        "Perhaps most importantly, we achieved these results while investing significantly in our future. "
        "R&D spending of $700 million funded the development of next-generation products including our "
        "AI-powered analytics platform (which generated $180M in first-year bookings), a completely "
        "redesigned enterprise collaboration suite, and breakthrough advances in our data processing "
        "engine that deliver 3x performance improvements for complex analytical workloads.",

        "Our people are the foundation of everything we accomplish. In FY2024, we grew our team to "
        "18,450 talented professionals across 28 countries. I am especially proud that our employee "
        "retention rate of 91% continues to lead our industry. We invested $45 million in training and "
        "development programs, launched a new engineering fellowship program, and expanded our commitment "
        "to diversity with measurable progress: women now represent 38% of our workforce and 32% of "
        "leadership positions.",

        "Looking ahead, I see enormous opportunity. The digital transformation of enterprises is still "
        "in its early innings, with IDC estimating $3.4 trillion in worldwide spending on digital "
        "transformation technologies by 2026. The emergence of generative AI is creating entirely new "
        "categories of enterprise software demand that play directly to our strengths in data management, "
        "analytics, and cloud infrastructure.",

        "Our strategic priorities for FY2025 are clear: accelerate our AI product portfolio, deepen "
        "cloud penetration with existing customers, expand international operations, and pursue targeted "
        "acquisitions that fill technology gaps. We expect revenue of $5.4-5.6 billion and operating "
        "margins of 24-25%, representing continued profitable growth.",

        "The Board's decision to increase our dividend by 15% and authorize a new $1.5 billion share "
        "repurchase program reflects our confidence in the sustainability of our cash generation and "
        "our commitment to returning capital to shareholders. Over the past five years, we have returned "
        "$2.16 billion through dividends and buybacks while simultaneously funding $1.25 billion in "
        "strategic acquisitions.",

        "I want to express my sincere gratitude to our customers for their trust and partnership, to our "
        "employees for their dedication and innovation, and to you, our shareholders, for your continued "
        "confidence in our vision and strategy. We are building a company that will define the next "
        "generation of enterprise technology, and I have never been more excited about what lies ahead.",

        "Sincerely,",
        "James A. Mitchell\nChairman & Chief Executive Officer\nMarch 15, 2025",
    ]

    for p in paras:
        elements.append(Paragraph(p, style_body))
        elements.append(Spacer(1, 2 * mm))

    elements.append(PageBreak())
    return elements


def build_segment_detail():
    """Build detailed segment performance tables (2+ pages)."""
    elements = []
    elements.append(Paragraph("Detailed Segment Performance", style_heading1))
    elements.append(Paragraph(
        "The following tables provide granular performance data for each of Acme Corporation's five "
        "reportable segments, including product-level revenue breakdowns and key operating metrics.",
        style_body,
    ))

    # Enterprise Solutions Detail
    elements.append(Paragraph("Enterprise Solutions — Product Breakdown", style_heading2))
    es_header = ["Product Line", "FY2024 ($M)", "FY2023 ($M)", "Growth", "% of Segment"]
    es_rows = [
        ["Core Platform License", "$420", "$412", "1.9%", "23.6%"],
        ["Platform Subscription", "$580", "$462", "25.5%", "32.6%"],
        ["Integration Services", "$285", "$268", "6.3%", "16.0%"],
        ["Support & Maintenance", "$312", "$298", "4.7%", "17.5%"],
        ["Professional Services", "$183", "$180", "1.7%", "10.3%"],
        ["Total Enterprise Solutions", "$1,780", "$1,620", "9.9%", "100.0%"],
    ]
    es_data = [es_header] + es_rows
    col_w = [4.2 * cm, 2.5 * cm, 2.5 * cm, 2.0 * cm, 2.8 * cm]
    elements.append(make_table(es_data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    # Cloud Services Detail
    elements.append(Paragraph("Cloud Services — Product Breakdown", style_heading2))
    cs_header = ["Product Line", "FY2024 ($M)", "FY2023 ($M)", "Growth", "% of Segment"]
    cs_rows = [
        ["Infrastructure-as-a-Service", "$445", "$358", "24.3%", "34.8%"],
        ["Platform-as-a-Service", "$362", "$275", "31.6%", "28.3%"],
        ["Managed Database Services", "$218", "$168", "29.8%", "17.0%"],
        ["Security & Compliance", "$145", "$112", "29.5%", "11.3%"],
        ["Developer Tools", "$110", "$84", "31.0%", "8.6%"],
        ["Total Cloud Services", "$1,280", "$997", "28.4%", "100.0%"],
    ]
    cs_data = [cs_header] + cs_rows
    elements.append(make_table(cs_data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    # Data Analytics Detail
    elements.append(Paragraph("Data Analytics — Product Breakdown", style_heading2))
    da_header = ["Product Line", "FY2024 ($M)", "FY2023 ($M)", "Growth", "% of Segment"]
    da_rows = [
        ["Business Intelligence Suite", "$310", "$285", "8.8%", "35.8%"],
        ["AI/ML Platform", "$220", "$165", "33.3%", "25.4%"],
        ["Data Warehousing", "$185", "$178", "3.9%", "21.4%"],
        ["Real-time Streaming", "$95", "$90", "5.6%", "11.0%"],
        ["Data Governance Tools", "$55", "$50", "10.0%", "6.4%"],
        ["Total Data Analytics", "$865", "$768", "12.6%", "100.0%"],
    ]
    da_data = [da_header] + da_rows
    elements.append(make_table(da_data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph(
        "The AI/ML Platform within Data Analytics achieved 33.3% growth, making it the fastest-growing "
        "individual product line. This platform enables customers to build, deploy, and manage machine "
        "learning models at enterprise scale with built-in governance and compliance features.",
        style_body,
    ))
    elements.append(Paragraph(
        "Cloud Services' Infrastructure-as-a-Service offering benefited from 380 new enterprise cloud "
        "migrations during the year, with average deal size increasing 22% to $1.2M annually. The "
        "pipeline for cloud migrations entering FY2025 stands at $2.1 billion.",
        style_body,
    ))

    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> Product line revenue is based on management allocation. Some bundled "
        "arrangements require judgment in allocating transaction price across products.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_tax_reconciliation():
    """Build detailed tax rate reconciliation and jurisdiction table."""
    elements = []
    elements.append(Paragraph("Income Tax Detail & Rate Reconciliation", style_heading1))
    elements.append(Paragraph(
        "The following tables present the reconciliation of the U.S. federal statutory tax rate to the "
        "Company's effective tax rate, along with the geographic distribution of pre-tax income and "
        "tax expense for FY2024.",
        style_body,
    ))

    elements.append(Paragraph("Effective Tax Rate Reconciliation", style_heading2))
    tax_header = ["Item", "FY2024", "FY2023", "Impact ($M)"]
    tax_rows = [
        ["U.S. Federal Statutory Rate", "21.0%", "21.0%", "$233"],
        ["State Income Taxes (net of federal)", "2.8%", "2.9%", "$31"],
        ["Foreign Rate Differential", "-0.8%", "-0.7%", "($9)"],
        ["R&D Tax Credits", "-2.5%", "-2.4%", "($28)"],
        ["Stock-Based Compensation Excess Benefit", "-1.2%", "-1.0%", "($13)"],
        ["Non-Deductible Compensation (162m)", "1.8%", "1.5%", "$20"],
        ["GILTI & FDII", "0.5%", "0.4%", "$6"],
        ["Acquisition-Related Items", "0.8%", "0.6%", "$9"],
        ["Other, net", "0.6%", "0.8%", "$6"],
        ["Effective Tax Rate", "23.0%", "23.1%", "$255"],
    ]
    tax_data = [tax_header] + tax_rows
    col_w = [5.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]
    elements.append(make_table(tax_data, col_widths=col_w))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Pre-Tax Income by Jurisdiction", style_heading2))
    jur_header = ["Jurisdiction", "Pre-Tax Income ($M)", "Tax Expense ($M)", "Effective Rate"]
    jur_rows = [
        ["United States", "$845", "$202", "23.9%"],
        ["United Kingdom", "$72", "$13", "18.1%"],
        ["Ireland", "$65", "$8", "12.3%"],
        ["Germany", "$42", "$13", "31.0%"],
        ["Singapore", "$35", "$6", "17.1%"],
        ["Canada", "$22", "$6", "27.3%"],
        ["Japan", "$15", "$4", "26.7%"],
        ["Other International", "$14", "$3", "21.4%"],
        ["Total", "$1,110", "$255", "23.0%"],
    ]
    jur_data = [jur_header] + jur_rows
    col_w2 = [4.0 * cm, 3.5 * cm, 3.5 * cm, 3.0 * cm]
    elements.append(make_table(jur_data, col_widths=col_w2))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Deferred Tax Asset & Liability Detail", style_heading2))
    dta_header = ["Component", "Dec 31, 2024", "Dec 31, 2023", "Change"]
    dta_rows = [
        ["DEFERRED TAX ASSETS", "", "", ""],
        ["  Stock-Based Compensation", "$35M", "$30M", "$5M"],
        ["  Accrued Liabilities", "$28M", "$24M", "$4M"],
        ["  Lease Liabilities", "$18M", "$16M", "$2M"],
        ["  Net Operating Losses", "$11M", "$8M", "$3M"],
        ["Total Deferred Tax Assets", "$92M", "$78M", "$14M"],
        ["", "", "", ""],
        ["DEFERRED TAX LIABILITIES", "", "", ""],
        ["  Intangible Asset Amortization", "($72M)", "($58M)", "($14M)"],
        ["  Right-of-Use Assets", "($32M)", "($28M)", "($4M)"],
        ["  Depreciation", "($31M)", "($26M)", "($5M)"],
        ["Total Deferred Tax Liabilities", "($135M)", "($112M)", "($23M)"],
        ["", "", "", ""],
        ["Net Deferred Tax Liability", "($43M)", "($34M)", "($9M)"],
    ]
    dta_data = [dta_header] + dta_rows
    col_w3 = [5.0 * cm, 2.8 * cm, 2.8 * cm, 2.5 * cm]
    elements.append(make_table(dta_data, col_widths=col_w3))
    elements.append(Spacer(1, 4 * mm))
    elements.append(Paragraph(
        "<super>1</super> The Company has not provided U.S. deferred taxes on approximately $380M of "
        "undistributed earnings of foreign subsidiaries as these earnings are considered permanently "
        "reinvested. If distributed, additional tax of approximately $22M would be incurred.",
        style_footnote,
    ))
    elements.append(PageBreak())
    return elements


def build_document():
    """Assemble all sections into the final PDF document."""
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    elements = []

    # Cover page
    elements.extend(build_cover())

    # Letter to Shareholders
    elements.extend(build_shareholder_letter())

    # Executive Summary
    elements.extend(build_executive_summary())

    # Table 1: Income Statement + commentary
    elements.extend(build_income_statement())
    elements.extend(build_commentary(
        "Management Commentary: Revenue & Profitability",
        [
            "Revenue growth of 14.3% was driven by strong execution across all five business segments. "
            "The subscription business accelerated to 23.6% growth, reflecting successful upselling of "
            "cloud-based solutions to our installed base of 4,200+ enterprise customers.",
            "Gross margin expanded 100 basis points to 63.1%, benefiting from improved cloud infrastructure "
            "utilization (82% average, up from 74%) and a favorable shift toward higher-margin subscription "
            "revenue. We expect further margin improvement as subscription mix continues to increase.",
            "Operating expenses grew 12.0%, below revenue growth, demonstrating operating leverage. "
            "R&D investment remained elevated at 14.5% of revenue to fund our AI/ML product roadmap and "
            "platform modernization initiatives that we expect will drive growth in FY2025 and beyond.",
        ]
    ))

    # Table 2: Balance Sheet + commentary
    elements.extend(build_balance_sheet())
    elements.extend(build_commentary(
        "Management Commentary: Balance Sheet Strength",
        [
            "Total assets grew to $8.3 billion, reflecting both organic growth and strategic acquisitions. "
            "The $400M increase in goodwill relates to the DataFlow ($232M) and IntelliServe ($98M) "
            "acquisitions, plus measurement period adjustments on prior year transactions.",
            "Working capital management remained disciplined with DSO stable at 67.5 days. The increase "
            "in deferred revenue ($125M) reflects strong bookings momentum and longer-term contracts, "
            "providing visibility into future revenue recognition.",
        ]
    ))

    # Table 3: Cash Flow + commentary
    elements.extend(build_cash_flow())
    elements.extend(build_commentary(
        "Management Commentary: Cash Generation & Deployment",
        [
            "Operating cash flow of $1.15 billion represented 24.0% of revenue, demonstrating strong "
            "cash conversion. Free cash flow of $809 million (after $345M CapEx) provided ample capacity "
            "to fund $520M in acquisitions and $620M in shareholder returns.",
            "Capital allocation priorities remain: (1) invest in organic growth, (2) strategic M&A, "
            "(3) return excess capital to shareholders. The Board's new $1.5B buyback authorization "
            "and 15% dividend increase reflect confidence in sustainable cash generation.",
        ]
    ))

    # Table 4: Revenue by Segment
    elements.extend(build_revenue_by_segment())
    elements.extend(build_commentary(
        "Management Commentary: Segment Performance",
        [
            "Cloud Services was the standout performer with 28.4% growth driven by 380 new enterprise "
            "cloud migrations during the year. The segment's operating margin expanded 240bps as we "
            "achieved greater scale and infrastructure efficiency.",
            "Enterprise Solutions maintained steady growth of 9.9% despite facing some headwinds from "
            "customers transitioning to cloud deployment models. We view this migration as positive for "
            "long-term customer lifetime value even as it creates near-term revenue mix shifts.",
            "Emerging Products grew 15.2% and is on track to achieve profitability in FY2025. The "
            "AI-powered analytics platform launched in Q2 achieved $180M in first-year bookings, "
            "exceeding our internal target of $150M.",
        ]
    ))

    # Detailed Segment Tables
    elements.extend(build_segment_detail())

    # Table 5: Revenue by Geography
    elements.extend(build_revenue_by_geography())
    elements.extend(build_commentary(
        "Management Commentary: Geographic Expansion",
        [
            "International revenue reached 38% of total, up from 34% in the prior year, as we executed "
            "on our geographic diversification strategy. The APAC region grew 46.5% following the "
            "establishment of new offices in Singapore, Tokyo, and Sydney.",
            "New market entries in Latin America and Eastern Europe are performing ahead of plan. Brazil "
            "and Mexico contributed $85M combined in their first partial year, while the Warsaw office "
            "is serving as a hub for Eastern European expansion.",
        ]
    ))

    # Table 6: OpEx Breakdown
    elements.extend(build_opex_breakdown())

    # Table 7: Headcount
    elements.extend(build_headcount())
    elements.extend(build_commentary(
        "Management Commentary: Human Capital",
        [
            "We added 2,250 net new employees during FY2024, with 49% in engineering roles to support "
            "product development acceleration. Employee retention remained strong at 91%, above the "
            "industry average of 85%, reflecting our investment in culture, career development, and "
            "competitive total compensation.",
            "Total compensation expense of $3.14 billion represented 65% of operating expenses. "
            "We continue to invest in our people through expanded learning programs ($45M), enhanced "
            "parental leave, mental health benefits, and flexible hybrid work arrangements.",
        ]
    ))

    # Table 8: CapEx
    elements.extend(build_capex())

    # Table 9: Debt Schedule
    elements.extend(build_debt_schedule())
    elements.extend(build_commentary(
        "Management Commentary: Capital Structure",
        [
            "Our balance sheet provides significant financial flexibility with $2.3B in cash, a net "
            "cash position of $500M, and a fully undrawn $500M revolving credit facility. Our leverage "
            "ratio of 1.34x Debt/EBITDA is well below our internal target ceiling of 2.5x.",
            "In March 2024, we issued $500M in 10-year senior notes at 4.50% to fund the DataFlow "
            "acquisition and repay maturing 2024 notes. The well-laddered maturity profile ensures no "
            "single year has excessive refinancing requirements.",
        ]
    ))

    # Table 10: Five-Year Summary
    elements.extend(build_five_year_summary())

    # Quarterly KPIs
    elements.extend(build_quarterly_metrics())
    elements.extend(build_commentary(
        "Management Commentary: Operational Momentum",
        [
            "Our quarterly KPI trends demonstrate accelerating business momentum throughout FY2024. "
            "Net revenue retention improved from 115% (Q4 2023) to 122% (Q4 2024), reflecting successful "
            "cross-sell and upsell execution. The expansion of annual recurring revenue to $3.75B provides "
            "strong visibility into FY2025 performance.",
            "Customer acquisition cost (CAC) payback period improved from 22 months to 15 months, driven "
            "by higher average contract values and more efficient go-to-market motions. The LTV/CAC ratio "
            "of 5.1x significantly exceeds our target of 3.0x, indicating healthy unit economics.",
            "Platform reliability remained excellent with 99.97-99.99% uptime across all quarters, "
            "supporting mission-critical enterprise workloads. Average API response time improved 37% "
            "year-over-year through infrastructure optimization and edge computing deployment.",
        ]
    ))

    # Risk Factors
    elements.extend(build_risk_factors())

    # ESG Section
    elements.extend(build_esg_section())

    # Appendix
    elements.extend(build_appendix())

    # Additional Appendix Notes
    elements.extend(build_additional_appendix())

    # Tax Reconciliation Detail
    elements.extend(build_tax_reconciliation())

    # Management Responsibility & Auditor Report
    elements.extend(build_management_responsibility())

    # Financial Ratios (final section)
    elements.extend(build_financial_ratios())

    doc.build(elements)
    print(f"PDF generated: {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build_document()
