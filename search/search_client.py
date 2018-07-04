from es.es import ES
from documents.metadocument import Metadocument
from parsers.cleaner import Cleaner

'''
The following client will be used at runtime for querying the database. It
supports capabilities to query data based on partial string match, keywords,
'''


class SearchClient:
    def __init__(self):
        self.es = ES()

    '''
    Searches using partial string matches (i.e. similarities by strings)
    
    https://qbox.io/blog/mlt-similar-documents-in-elasticsearch-more-like-this-query
    '''

    def search_by_partial_match(self, phrases, num_results):
        cleaned_phrases = [Cleaner.clean(phrase) for phrase in phrases]
        return self.es.client.search(index=Metadocument.INDEX_NAME, body={
            'size': num_results,
            'query': {
                "more_like_this": {
                    "fields": ["dataset_name", "dataset_description", "dataset_notes", "dataset_keywords", "dataset_tags", "dataset_attributes"],
                    "min_doc_freq": 1,
                    "min_term_freq": 1,
                    "like": cleaned_phrases[0]
                }
            }
        })