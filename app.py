from flask import Flask, render_template, request, Response
import base64
from service.card_generator import pdfGenerator


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/handle_form', methods=['POST'])
def handle_form():
    pdf = generatePDF(request.form, request.files)
    return createResponse(pdf)


def generatePDF(form, files):
    file = open('static/card_template/template.html', 'r')

    id = form.get('id')
    name = form.get('name')
    role = form.get('role')
    picture = files['photo']
    picture = base64.b64encode(picture.read()).decode('UTF-8')
    return pdfGenerator(file, id, name, role, picture)


def createResponse(pdf):
    response = Response(pdf)
    response.headers['Content-Disposition'] = "inline; 'ID Card Genarated'"
    response.mimetype = 'application/pdf'
    return response


if __name__ == "__main__":
    app.run(debug=True)
