from elasticsearch import Elasticsearch, helpers
import certifi

from documents.metadocument import Metadocument


class ES:
    ES_ENDPOINT = "https://search-data-pipeline-poc-bdfr3wal5lxncg2zllpoo6nd2e.us-east-1.es.amazonaws.com"

    def __init__(self):
        self.client = Elasticsearch(self.ES_ENDPOINT, use_ssl=True, verify_certs=True, ca_certs=certifi.where())

    # allegheny_county_air_quality gives broken csv
    def bulk_upload(self, documents):
        result = None
        attempt = 0
        while result is None and attempt < 5:
            try:
                result = helpers.bulk(self.client, documents)
            except Exception as e:
                print(e)
                print("Retrying bulk upload...")
                pass
            attempt += 1


    def init_metadocument_index(self):
        print(self.client.indices.create(index=Metadocument.INDEX_NAME, body={
            "mappings": {
                Metadocument.TYPE: {
                    "properties": Metadocument.PROPERTY_MAPPING
                }
            }
        }))
