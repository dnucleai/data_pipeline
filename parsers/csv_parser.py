import csv
import re
import sys
import urllib2

# CSV limit has failed for datasets
csv.field_size_limit(sys.maxsize)

class CSVParser:
    def __init__(self):
        pass

    @staticmethod
    def convert_csv_file_to_json_list(csv_file):
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

    @staticmethod
    def convert_csv_url_to_json_list(csv_url):
        response = urllib2.urlopen(csv_url)
        cr = csv.DictReader(response)
        json_dictionary = list(cr)
        # Some values are not ascii
        remove_ascii_dic = [{k: re.sub(r'[^\x00-\x7F]', ' ', v) for k, v in dic.items()} for dic in json_dictionary]
        # Some attributes are empty
        return [dict((k, v) for k, v in dic.iteritems() if v) for dic in remove_ascii_dic]

    @staticmethod
    def is_csv(url):
        return ".csv" in url
