import datetime
import os
from fpdf import FPDF
from class_tester import nmea_str
from visualization import IMAGE

OUTPUT_PDF = 'report.pdf'  # pdf file name


def make_pdf_report():
    """
    Creates PDF file with final report consist of visual representation and list of NMEA messages
    """
    pdf = FPDF()
    pdf.set_font("Arial", size=18)  # font for Title
    pdf.add_page()
    pdf.cell(200, 10,
             txt='NMEA report, created on {utc}'.format(
                 utc=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), align='C')
    pdf.ln(150)
    pdf.image(os.getcwd()+'/output/'+IMAGE, x=10, y=20, w=195)  # visual representation
    pdf.ln(10)
    pdf.cell(200, 10, txt='List of NMEA messages:', align='C')
    pdf.set_font("Arial", size=12)  # font for NMEA's
    for s in nmea_str:  # print every msg
        pdf.ln(10)
        pdf.cell(200, 10, txt='{}'.format(s), align='C')
    pdf.output(OUTPUT_PDF)
    os.rename(OUTPUT_PDF, os.getcwd()+'/output/'+OUTPUT_PDF)


if __name__ == '__main__':
    make_pdf_report()
