from vectorpdf_canvas import create_vector_pdf
from vectorpdf_platypus import create_vector_pdf
from raster_pdf import create_raster_pdf
from create_table import create_table
from pdf_extraction import extract_vector_pdf, extract_raster_pdf,extract_pdf_tables

def main():
    print("Starting PDF pipeline...")

    create_vector_pdf()
    create_vector_pdf()
    create_raster_pdf()
    create_table()
    extract_vector_pdf()
    extract_raster_pdf()
    extract_pdf_tables()

    print("All tasks completed!")

if __name__ == "__main__":
    main()