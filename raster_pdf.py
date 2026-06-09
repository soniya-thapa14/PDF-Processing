from PIL import Image, ImageDraw,ImageFont
import img2pdf

def create_raster_pdf(output_pdf = 'sample_files/raster.pdf'):
    width,height = 2480, 3580
    img = Image.new('RGB',(width,height),color =(255,255,255))
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("arial.ttf",65)
    font_heading = ImageFont.truetype("arial.ttf", 55)
    font_body = ImageFont.truetype("arial.ttf", 40)
    font_small = ImageFont.truetype("arial.ttf",35)
    draw.rectangle((0,0,width,180), fill = "black")
    draw.text((100,50), "Monthly Sales Report", font = font_title, fill = "white")
    
    draw.text((80,200), "Sales Overview", font = font_heading, fill=(0,0,0))
    draw.line([80, 310, width-80, 310], fill=(200, 200, 200), width=3)

    kpis = [
            ("Total Sales",     "$45,230",  (52, 152, 219)),
            ("New Customers",   "128",      (46, 204, 113)),
            ("Revenue Growth",  "23%",      (231, 76,  60)),
            ("Avg Order Value", "$353",     (155, 89, 182)),
    ]

    box_w,box_h = 600,220
    start_x = 80
    start_y = 350

    for i, (label,value,color) in enumerate(kpis):
        x = start_x + i*(box_w + 40)
        draw.rectangle((x, start_y, x+box_w, start_y+box_h), fill =color)
        draw.text((x+20, start_y+20), label,font = font_heading, fill =(255,255,255))
        draw.text((x+20, start_y+130), value, font=font_small, fill=(255, 255, 255))

        draw.text((80, 620), "Performance Summary", font=font_heading, fill=(30, 80, 160))
        draw.line([80, 690, 620, 690], fill=(30, 80, 160), width=4)

        lines = [
        "This month demonstrated exceptional performance across all regional",
        "divisions. The northern region led overall contributions with 45% of",
        "total revenue, followed closely by the southern division at 32%.",
        "",
        "Customer acquisition costs decreased by 12% compared to last quarter,",
        "while customer lifetime value increased by 18%. These metrics indicate",
        "strong improvements in both marketing efficiency and product quality.",
        "",
        "The top performing product category was Electronics, accounting for",
        "$18,500 of total sales. Software subscriptions followed at $12,300,",
        "showing a 34% increase from the previous month.",
        "",
        "Looking ahead to February, the sales team has identified three key",
        "growth opportunities in the enterprise segment. Projections suggest",
        "a further 15% increase in revenue if current trends continue.",
    ]

    y = 730
    for line in lines:
        draw.text((80,y), line, font= font_body, fill=(30,30,30))
        y += 65

        draw.text((80, 1800), "Regional Sales Breakdown", font=font_heading, fill=(30, 80, 160))
        draw.line([80,1870,700,1870], fill =(80,80,80), width = 4)

    bars = {
        "North": 45,
        "South": 32,
        "East": 15,
        "West": 8
    }
    y= 1900

    for region, value in bars.items():
        draw.text((90, y), f"{region} : {value}%", font=font_body, fill=(0, 0, 0))
        y += 60
    
    draw.line([0, height-120, width, height-120], fill=(30, 80, 160), width=5)
    draw.rectangle([0, height-120, width, height], fill="black")
    draw.text((80, height-90), "Confidential  |  Sales Department  |  January 2024",
              font=font_small, fill="white")

    img.save("raster_page.png")
    print("Image created: raster_page.png")

    with open(output_pdf, "wb") as f:
      f.write(img2pdf.convert("raster_page.png"))
    print(f"Raster PDF created: {output_pdf}")
create_raster_pdf()




