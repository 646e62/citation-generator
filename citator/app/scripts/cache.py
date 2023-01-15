import os
import pickle
from django.core.cache import cache

'''
These functions check to see if a citation has already been accessed and
serialized. If so, the citation is retrieved from the cache. If not, a function
calls the CanLII API and serializes the citation.
'''

def check_cache(url) -> bool:

    if cache.get(url):
        return True
    else:
        return False

def check_stored_citations(url) -> bool:
    
        with open('stored_citations.txt', 'rb') as f:
            stored_citations = pickle.load(f)
    
        if url in stored_citations:
            return True
        else:
            return False

def serialize(url, data) -> dict:
    '''
    Serializes the citation data and stores it in the cache. Will be called
    by the generate_citation function, which will use the cache & save file
    as a data source.
    '''
    
    url_split = url.split('/')
    citation = {
            'url': url,
            'short_url': data['url'],
            'year': url_split[7],
            'language': url_split[3],
            'case_jurisdiction': url_split[4],
            'court': url_split[5],
            'canlii_citation': url_split[8],
            'date': data['decisionDate'],
            'style_of_cause': data['title'].replace('.', ''),
            'docket_number': data['docketNumber'],
            'keywords': data['keywords'],
            }

    with open('stored_citations.txt', 'rb') as f:
        stored_citations = pickle.load(f)

    if url in stored_citations:
        return citation
    else:
        stored_citations.append(url)
        with open('stored_citations.txt', 'wb') as f:
            pickle.dump(stored_citations, f)
        cache.set(url, citation)
        return citation

