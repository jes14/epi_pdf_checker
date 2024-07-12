from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def correct_tokenization(pdf_text):
    import re

    def paste_idx(text_list, idx):
        text_list[idx] = text_list[idx] + ' ' + text_list[idx + 1]
        del text_list[idx + 1]
        return text_list

    pdf_text_corrected = pdf_text.split('.')
    sentence_paste_idx = [i for i, text in enumerate(pdf_text_corrected) 
                          if re.search(r"accession nr.|accession no.|ccession nos.|ccession nrs.$", text.strip())]

    for idx in sentence_paste_idx[::-1]:
        pdf_text_corrected = paste_idx(pdf_text_corrected, idx)

    return '. '.join(pdf_text_corrected)
