from parsers.cleaner import Cleaner


class Metadocument:
    TYPE = "metadata_on_datasets_type"
    INDEX_NAME = "metadata_on_datasets"
    PROPERTY_MAPPING = {
        "dataset_name": {
            "type":"keyword"
        },
        "dataset_description": {
            "type":"text"
        },
        "dataset_notes": {
            "type":"text"
        },
        "dataset_keywords": {
            "type":"keyword"
        },
        "dataset_author": {
            "type":"keyword"
        },
        "dataset_tags": {
            "type":"keyword"
        },
        "time_ingested": {
            "type":"keyword"
        },
        "time_created": {
            "type":"date"
        },
        "dataset_source": {
            "type":"keyword"
        },
        "dataset_attributes": {
            "type":"keyword"
        },
        "dataset_num_docs": {
            "type": "long"
        }
    }

    def __init__(self, contents, content_name):
        self.contents = contents
        self.id = Cleaner.format_es_fields(content_name)

    def get_es_document(self):
        return {
            "_index": Metadocument.INDEX_NAME,
            "_id": self.id,
            "_type": Metadocument.TYPE,
            "_source": self.contents,

        }
