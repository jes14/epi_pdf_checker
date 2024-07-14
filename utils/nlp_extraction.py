import spacy

nlp = spacy.load("en_core_web_sm")

def extract_nlp_keywords(text, top_n=10):
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    keywords = list(set(keywords))  # Remove duplicates
    return keywords[:top_n]