import numpy as np
import pandas as pd
from Bio import Entrez
from langchain_core.documents import Document


def search(query):
    Entrez.email = 'email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='250000',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def load_docs(topic: str):
    studies = search(topic)
    studiesIdList = studies['IdList']
    docs = []

    chunk_size = 10000
    for chunk_i in range(0, len(studiesIdList), chunk_size):
        chunk = studiesIdList[chunk_i:chunk_i + chunk_size]
        papers = fetch_details(chunk)

        for paper in papers['PubmedArticle']:
            title = paper['MedlineCitation']['Article']['ArticleTitle']
            try:
                abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            except:
                abstract = "No Abstract"

            metadata = {
                "title": title,
                "journal": paper['MedlineCitation']['Article']['Journal']['Title'],
                "language": paper['MedlineCitation']['Article']['Language'][0],
                "pub_year": paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year',
                                                                                                          'No Data'),
                "pub_month": paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Month',
                                                                                                           'No Data')
            }

            doc = Document(page_content=abstract, metadata=metadata)
            docs.append(doc)

    print(docs[0].page_content[:500])
    return docs




