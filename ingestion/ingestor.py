import calendar
import time

from es.es import ES
from documents.document import Document
from documents.metadocument import Metadocument
from parsers.csv_parser import CSVParser


class Ingestor:
    def __init__(self):
        self.es = ES()

    def ingest(self, dataset_name, dataset_source, dataset_description, dataset_author,
               dataset_notes, dataset_creation_time, dataset_tags, online=True):
        """
        The following will clean, parse, and upload datasets to our database.

        :param dataset_name: Name of the dataset.
        :param dataset_source: Source of the dataset (i.e. filename or URL).
        :param dataset_description: Description of the dataset.
        :param dataset_author: Author of the dataset.
        :param dataset_notes: Any notes on the dataset by us.
        :param dataset_creation_time: Time the dataset was created.
        :param online: boolean of whether the data is a local file (offline) or a URL (online).
        """
        if CSVParser.is_csv(dataset_source):
            if online:
                raw_documents = CSVParser.convert_csv_url_to_json_list(dataset_source)
            else:
                raw_documents = CSVParser.convert_csv_file_to_json_list(dataset_source)
            dataset_attributes = raw_documents[0].keys()
            es_documents = [Document(dataset_name, raw_document).get_es_document() for raw_document in raw_documents]
            self.es.bulk_upload(es_documents)
        else:
            print("Unsupported file format.")

        metadocument = {
            "dataset_name": dataset_name,
            "dataset_description": dataset_description,
            "dataset_notes": dataset_notes,
            "dataset_keywords": None,  # TODO: Add explicit keywords for datasets through ML
            "dataset_tags": dataset_tags,
            "dataset_author": dataset_author,
            "time_ingested": calendar.timegm(time.gmtime()),
            "time_created": dataset_creation_time,
            "dataset_source": dataset_source,
            "dataset_attributes": dataset_attributes,
            "dataset_num_docs": len(es_documents),
        }
        self.es.bulk_upload([Metadocument(metadocument, dataset_name).get_es_document()])
