from flask import Flask, render_template, request
from service.response_builder import generatePDF, generateZIP, createPDFResponse, createZIPResponse


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/handle_download', methods=['POST'])
def handle_download():
    pdf = generatePDF(request.form, request.files)
    return createPDFResponse(pdf)


@app.route('/handle_bulk_download', methods=['POST'])
def handle_bulk_download():
    zip = generateZIP(request.files)
    return createZIPResponse(zip)


if __name__ == "__main__":
    app.run(debug=True)
