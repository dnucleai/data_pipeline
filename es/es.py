from elasticsearch import Elasticsearch, helpers
import certifi

from documents.metadocument import Metadocument


class ES:
    ES_ENDPOINT = "https://search-data-pipeline-poc-bdfr3wal5lxncg2zllpoo6nd2e.us-east-1.es.amazonaws.com"

    def __init__(self):
        self.client = Elasticsearch(self.ES_ENDPOINT, use_ssl=True, verify_certs=True, ca_certs=certifi.where())

    def bulk_upload(self, documents):
        helpers.bulk(self.client, documents)

    def init_metadocument_index(self):
        print(self.client.indices.create(index=Metadocument.INDEX_NAME, body={
            "mappings": {
                Metadocument.TYPE: {
                    "properties": Metadocument.PROPERTY_MAPPING
                }
            }
        }))
