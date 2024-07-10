from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def correct_tokenization(pdf_text):
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

def create_keyword_list():
    keywords = {
        'Date': r'\b\d{4}-\d{2}-\d{2}\b',
        'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'Phone': r'\b\d{3}-\d{3}-\d{4}\b',
        'available': r"\b(included|deposited|released|is provided|are provided|contained in|available|reproduce|accessible|can be accessed|submitted|can be downloaded|reported in|uploaded|are public on)\b",
        'was_available': r"\b(was provided|were provided|was contained in|were contained in|was available|were available|was accessible|were accessible|deposited by|were reproduced)\b",
        'not_available': r"\b(not included|not deposited|not released|not provided|not contained in|not available|not accessible|not submitted)\b",
        'field_specific_repo': r"\b(GEO|Gene Expression Omnibus|European Nucleotide Archive|National Center for Biotechnology Information|European Molecular Biology Laboratory|EMBL-EBI|BioProject|Sequence Read Archive|SRA|ENA|MassIVE|ProteomeXchange|Proteome Exchange|ProteomeExchange|MetaboLights|Array-Express|ArrayExpress|Array Express|PRIDE|DNA Data Bank of Japan|DDBJ|Genbank|Protein Databank|Protein Data Bank|PDB|Metagenomics Rapid Annotation using Subsystem Technology|MG-RAST|metabolights|OpenAgrar|Open Agrar|Electron microscopy data bank|emdb|Cambridge Crystallographic Data Centre|CCDC|Treebase|dbSNP|dbGaP|IntAct|ClinVar|European Variation Archive|dbVar|Mgnify|NCBI Trace Archive|NCBI Assembly|UniProtKB|Protein Circular Dichroism Data Bank|PCDDB|Crystallography Open Database|Coherent X-ray Imaging Data Bank|CXIDB|Biological Magnetic Resonance Data Bank|BMRB|Worldwide Protein Data Bank|wwPDB|Structural Biology Data Grid|NeuroMorpho|G-Node|Neuroimaging Informatics Tools and Resources Collaboratory|NITRC|EBRAINS|GenomeRNAi|Database of Interacting Proteins|IntAct|Japanese Genotype-phenotype Archive|Biological General Repository for Interaction Datasets|PubChem|Genomic Expression Archive|PeptideAtlas|Environmental Data Initiative|LTER Network Information System Data Portal|Global Biodiversity Information Facility|GBIF|Integrated Taxonomic Information System|ITIS|Knowledge Network for Biocomplexity|Morphobank|Kinetic Models of Biological Systems|KiMoSys|The Network Data Exchange|NDEx|FlowRepository|ImmPort|Image Data Resource|Cancer Imaging Archive|SICAS Medical Image Repository|Coherent X-ray Imaging Data Bank|CXIDB|Cell Image Library|Eukaryotic Pathogen Database Resources|EuPathDB|Influenza Research Database|Mouse Genome Informatics|Rat Genome Database|VectorBase|Xenbase|Zebrafish Model Organism Database|ZFIN|HIV Data Archive Program|NAHDAP|National Database for Autism Research|NDAR|PhysioNet|National Database for Clinical Trials related to Mental Illness|NDCT|Research Domain Criteria Database|RdoCdb|Synapse|UK Data Service|caNanoLab|ChEMBL|IoChem-BD|Computational Chemistry Datasets|STRENDA|European Genome-phenome Archive|European Genome phenome Archive|accession number|accession code|accession numbers|accession codes)\b",
        'repositories': r"\b(figshare|dryad|zenodo|dataverse|DataverseNL|osf|open science framework|mendeley data|GIGADB|GigaScience database|OpenNeuro)\b",
        'github': r"\b(github)\b",
    }
    # Compile patterns
    compiled_keywords = {key: re.compile(pattern, re.IGNORECASE) for key, pattern in keywords.items()}
    return compiled_keywords


def search_keywords(text, keywords):
    results = {}
    for key, pattern in keywords.items():
        # If the pattern is a compiled regex, use it directly
        if isinstance(pattern, re.Pattern):
            matches = pattern.findall(text)
        else:
            # If the pattern is a string, compile it with flags
            regex = re.compile(pattern, re.IGNORECASE)
            matches = regex.findall(text)
        results[key] = matches
    return results

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
    return render_template('results.html', results=results)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
