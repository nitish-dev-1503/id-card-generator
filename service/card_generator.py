import pdfkit
import imgkit


def convertToPdf(template):
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    options = {'page-height': '525px', 'page-width': '360px', 'margin-left': '0mm',
               'margin-right': '0mm', 'margin-top': '0mm', 'margin-bottom': '0mm'}
    return pdfkit.from_string(template, configuration=config, options=options)


def convertToJpg(template):
    options = {'width': 448, 'disable-smart-width': ''}
    return imgkit.from_string(template, False, options=options)
