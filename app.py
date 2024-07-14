from flask import Flask, render_template, request, redirect, url_for
import os
from utils.file_handling import allowed_file
from utils.pdf_processing import extract_text_from_pdf, correct_tokenization
from utils.keyword_search import create_keyword_list, search_keywords
from utils.nlp_extraction import extract_nlp_keywords

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'uploaded_file.pdf'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                pdf_text = extract_text_from_pdf(filepath)
                corrected_text = correct_tokenization(pdf_text)
                return render_template('index.html', text=corrected_text)
            except Exception as e:
                print(f"Error processing file: {e}")
                return "There was an error processing the file."

    return render_template('index.html', text=None)

@app.route('/search', methods=['POST'])
def search():
    if 'text' not in request.form:
        return redirect(url_for('index'))

    text = request.form['text']
    keywords = create_keyword_list()
    results = search_keywords(text, keywords)
    nlp_keywords = extract_nlp_keywords(text)
    return render_template('results.html', results=results, nlp_keywords=nlp_keywords)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
