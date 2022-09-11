import pandas as pd
import base64
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from service.card_generator import pdfGenerator
from flask import Response


def generatePDF(form, files):
    template = open('static/card_template/template.html', 'r')

    id = form.get('id')
    name = form.get('name')
    role = form.get('role')
    photo = files['photo']
    photo_in_base64 = base64.b64encode(photo.read()).decode('UTF-8')
    image_tag = '<img src="data:image/png;base64,' + \
        photo_in_base64 + '" alt="profile picture" class="profile">'

    return pdfGenerator(template, id, name, role, image_tag)


def generateZIP(files):
    file = files['file']
    data = pd.read_excel(file, sheet_name=0)

    mem_zip = BytesIO()
    with ZipFile(mem_zip, mode='w', compression=ZIP_DEFLATED) as zip:
        for index, row in data.iterrows():
            template = open('static/card_template/template.html', 'r')
            id = str(row[0])
            name = row[1]
            role = row[2]
            photo = row[3]
            image_tag = '<img src="' + photo + '" alt="profile picture" class="profile">'
            pdf = pdfGenerator(template, id, name, role, image_tag)
            zip.writestr(id + '_' + name + '.pdf', data=pdf)

    return mem_zip.getvalue()


def createPDFResponse(pdf):
    response = Response(pdf)
    response.headers['Content-Disposition'] = "inline; 'ID Card Genarated'"
    response.mimetype = 'application/pdf'
    return response


def createZIPResponse(zip):
    response = Response(zip)
    response.headers['Content-Disposition'] = 'attachment; filename="id_cards.zip"'
    response.mimetype = 'application/zip'
    return response
