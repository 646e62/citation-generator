import os
import pickle
from django.core.cache import cache

from .mcgill_jurisprudence_rules import generate_citation

def cache_and_save():
    cache_key = 'canlii_citation'
    results = cache.get(cache_key)
    if results is None:
        file_path = 'results.pickle'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as handle:
                results = pickle.load(handle)
        else:
            results = generate_citation()
            cache.set(cache_key, results, 60 * 15)
            with open(file_path, 'wb') as handle:
                pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return results

