import pandas as pd
import base64
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from service.card_generator import convertToPdf, convertToJpg
from flask import Response


def generateCardFromTemplate(form, files):
    template = open('static/card_template/template.html', 'r')

    id = form.get('id')
    name = form.get('name')
    role = form.get('role')
    photo = files['photo']
    photo_in_base64 = base64.b64encode(photo.read())
    image_url = 'data:image/png;base64,' + photo_in_base64.decode('UTF-8')

    fileAsString = template.read()
    fileAsString = fileAsString.replace('@ID', id)
    fileAsString = fileAsString.replace('@NAME', name)
    fileAsString = fileAsString.replace('@ROLE', role)
    fileAsString = fileAsString.replace('@PICTURE', image_url)
    return fileAsString


def generateCardFromTemplateForBulkUpload(template, id, name, role, photo):
    fileAsString = template.read()
    fileAsString = fileAsString.replace('@ID', id)
    fileAsString = fileAsString.replace('@NAME', name)
    fileAsString = fileAsString.replace('@ROLE', role)
    fileAsString = fileAsString.replace('@PICTURE', photo)
    return fileAsString


def generatePDF(form, files):
    fileAsString = generateCardFromTemplate(form, files)
    return convertToPdf(fileAsString)


def generateJPG(form, files):
    fileAsString = generateCardFromTemplate(form, files)
    return convertToJpg(fileAsString)


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
            fileAsString = generateCardFromTemplateForBulkUpload(template, id, name, role, photo)
            pdf = convertToPdf(fileAsString)
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
