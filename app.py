import os
from flask import Flask, render_template, request, flash, send_file
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def converter(filename, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(filename, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/convert', methods=['POST', 'GET'])
def convert():

    txt_file = request.form.get("txtname")
    txt_file = txt_file + '.txt'
    # print(txt_file)

    target = os.path.join(APP_ROOT)
    # print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        if allowed_file(file.filename):
            # print(file)
            filename = file.filename
            destination = '/'.join([target, filename])
            # print(destination)
            file.save(destination)
            filename = destination
            filename = converter(filename)
            # print(filename)
            location = '/'.join([target, txt_file])
            # print(location)
            txtfile = open(txt_file, 'w')
            txtfile.write(filename)
            txtfile.close()
        else:
            return render_template('error.html')

    return render_template('success.html', output=filename, location=location)

if __name__ == '__main__':
    app.run(debug = True)