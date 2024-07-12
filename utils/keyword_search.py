import re

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

    compiled_keywords = {key: re.compile(pattern, re.IGNORECASE) for key, pattern in keywords.items()}
    return compiled_keywords

def search_keywords(text, keywords):
    results = {}
    for key, pattern in keywords.items():
        if isinstance(pattern, re.Pattern):
            matches = pattern.findall(text)
        else:
            regex = re.compile(pattern, re.IGNORECASE)
            matches = regex.findall(text)
        results[key] = matches
    return results
