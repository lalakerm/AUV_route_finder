import datetime
import os, shutil
from fpdf import FPDF
from NMEA.visualization import IMAGE

OUTPUT_PDF = 'report.pdf'  # pdf file name


def make_pdf_report(pic_opt, nmea_str, output):
    """
    Creates PDF file with final report consist of visual representation and list of NMEA messages
    """
    pdf = FPDF()
    pdf.set_font("Arial", size=18)  # font for Title
    pdf.add_page()
    pdf.cell(200, 10,
             txt='NMEA report, created on {utc}'.format(
                 utc=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt='with NMEA_report_maker.py', align='C')
    if pic_opt:
        pdf.ln(150)
        pdf.image(os.getcwd()+output+IMAGE, x=10, y=30, w=195)  # visual representation
        pdf.ln(10)
    pdf.cell(200, 10, txt='List of NMEA messages:', align='C')
    pdf.set_font("Arial", size=12)  # font for NMEA's
    for s in nmea_str:  # print every msg
        pdf.ln(10)
        pdf.cell(200, 10, txt='{}'.format(s), align='C')
    pdf.output(OUTPUT_PDF)
    shutil.move(OUTPUT_PDF, os.getcwd()+output+OUTPUT_PDF)
