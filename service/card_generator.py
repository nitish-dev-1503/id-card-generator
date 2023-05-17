import pdfkit


def pdfGenerator(file, id, name, role, image_url):
    fileAsString = file.read()
    fileAsString = fileAsString.replace('@ID', id)
    fileAsString = fileAsString.replace('@NAME', name)
    fileAsString = fileAsString.replace('@ROLE', role)
    fileAsString = fileAsString.replace('@PICTURE', image_url)

    return convertToPdf(fileAsString)


def convertToPdf(template):
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    options = {'page-height': '525px', 'page-width': '360px', 'margin-left': '0mm',
               'margin-right': '0mm', 'margin-top': '0mm', 'margin-bottom': '0mm'}

    return pdfkit.from_string(template, configuration=config, options=options)
