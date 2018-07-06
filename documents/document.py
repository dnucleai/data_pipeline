from parsers.cleaner import Cleaner


class Document:
    def __init__(self, index_name, contents):
        """
        Constructor for document object to be used.

        :param index_name: Name of the elasticsearch index in under which this doc will be stored
        :param property_mapping: Explicit mapping of field names to data types
        :param contents: Explicit mapping of field names to content values
        """
        self.index_name = Cleaner.format_es_fields(index_name)
        self.contents = contents

    def get_es_document(self):
        return {
            "_index": self.index_name,
            "_type": self.index_name + "_type",
            "_source": self.contents
        }
