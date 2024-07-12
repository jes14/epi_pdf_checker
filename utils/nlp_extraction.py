import spacy

nlp = spacy.load("en_core_web_sm")

def extract_nlp_keywords(text, top_n=10):
    doc = nlp(text)
    keywords = []

    for chunk in doc.noun_chunks:
        keywords.append(chunk.text)

    keywords = list(set(keywords))
    return keywords[:top_n]
