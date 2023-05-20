from flask import Flask, render_template, request, send_file
from io import BytesIO
from service.response_builder import generatePDF, generateJPG, generateZIP, createPDFResponse, createZIPResponse


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/handle_download', methods=['POST'])
def handle_download():
    form = request.form
    if form['action'] == 'Download PDF':
        pdf = generatePDF(form, request.files)
        return createPDFResponse(pdf)
    elif form['action'] == 'Download Image':
        image_data = generateJPG(form, request.files)
        return send_file(BytesIO(image_data), mimetype='image/jpeg', as_attachment=True, attachment_filename='id-card.jpg')


@ app.route('/handle_bulk_download', methods=['POST'])
def handle_bulk_download():
    zip = generateZIP(request.files)
    return createZIPResponse(zip)


if __name__ == "__main__":
    app.run(debug=True)
