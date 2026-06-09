from vectorpdf_canvas import create_canvas_pdf
from vectorpdf_platypus import create_platypus_pdf
from raster_pdf import create_raster_pdf
from create_table import create_table
from pdf_extraction import extract_vector_pdf, extract_raster_pdf,extract_pdf_tables

def main():
    print("Starting PDF pipeline...")

    create_canvas_pdf()
    create_platypus_pdf()
    create_raster_pdf()
    create_table()

    extract_vector_pdf('sample_files/Doc.pdf')
    extract_raster_pdf('sample_files/raster.pdf')
    extract_pdf_tables('sample_files/table.pdf')

    print("All tasks completed!")
