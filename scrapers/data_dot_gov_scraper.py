import urllib
import urllib2
import json

from ingestion.ingestor import Ingestor


class DataDotGovScraper:
    def __init__(self, query):
        self.query = query
        self.ingestor = Ingestor()

    def get_packages(self, limit=10000):
        uri_encoded_query = urllib.quote(self.query.encode("utf-8"))
        start = 0
        rows = min(1000, limit)
        package_names = []
        while start < 10000:
            response = urllib2.urlopen(
                'https://catalog.data.gov/api/3/search/dataset?q=' + uri_encoded_query + '&sort=score+desc&start=' +
                str(start) + '&rows=' + str(rows))
            package_names.extend(json.loads(response.read())["results"])
            start += rows
        return package_names

    def ingest_dataset(self, package):
        response = urllib2.urlopen("https://catalog.data.gov/api/3/action/package_show?id=" + package)
        meta_details = json.loads(response.read())["result"]

        resource = self.get_csv_resource(meta_details["resources"])
        if not resource is None:
            dataset_name = meta_details["title"]
            dataset_source = resource["url"]
            dataset_description = resource["description"]
            dataset_tags = [tag["name"] for tag in meta_details["tags"]]
            dataset_author = meta_details["author_email"] or meta_details["maintainer_email"] \
                             or meta_details["author"] or meta_details["maintainer"] \
                             or meta_details["organization"]["name"] or meta_details["creator_user_id"]
            dataset_notes = meta_details["notes"]
            time_created = meta_details["metadata_created"]
            self.ingestor.ingest(dataset_name, dataset_source, dataset_description, dataset_author,
                                 dataset_notes, time_created, dataset_tags)
        else:
            print("Error. No CSV resource.")

    def get_csv_resource(self, resources):
        for resource in resources:
            if ".csv" in resource["url"]:
                return resource
        return None
