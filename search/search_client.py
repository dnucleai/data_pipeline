from es.es import ES
from documents.metadocument import Metadocument
from parsers.cleaner import Cleaner

"""
The following client will be used at runtime for querying the database. It
supports capabilities to query data based on partial string match, keywords,
"""

class SearchClient:
    def __init__(self):
        self.es = ES()

    def search_by_partial_match(self, phrase, num_results):
        """
        Searches using partial string matches (i.e. similarities by strings)
        Read more at: https://qbox.io/blog/mlt-similar-documents-in-elasticsearch-more-like-this-query

        :param phrase: Search phrase to lookup (case sensitive)
        :param num_results: The number of results to return
        :return: List of methadocuments
        """
        cleaned_phrase = Cleaner.clean(phrase)
        print(cleaned_phrase)
        return self.es.client.search(index=Metadocument.INDEX_NAME, body={
            'size': num_results,
            'query': {
                "more_like_this": {
                    "fields": ["dataset_name", "dataset_description", "dataset_notes", "dataset_keywords", "dataset_tags", "dataset_attributes"],
                    "like": cleaned_phrase,
                    "min_doc_freq": 1,
                    "min_term_freq": 1,
                }
            }
        })


    def search_by_id(self, _id):
        """
        Grabs metadocument of dataset by id
        :param _id: The _id field of the metadocument class.
        :return: metadocument of dataset
        """
        return self.es.client.get(index=Metadocument.INDEX_NAME, id=_id, doc_type=Metadocument.TYPE)