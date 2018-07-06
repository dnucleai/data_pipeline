#!/usr/bin/python

import sys

from es.es import ES
from scrapers.data_dot_gov_scraper import DataDotGovScraper
from search.search_client import SearchClient


def main():
    # print command line arguments
    args = sys.argv[1:]
    command = args[0]
    # Needs to be setup once to create explicit mappings for metadocuments
    if command == "setup":
        ES().init_metadocument_index()
    elif command == "ingest_data_gov_by_query":
        query = args[1]
        scraper = DataDotGovScraper(query)
        packages = scraper.get_packages()[1080:]
        for package in packages:
            try:
                print("Getting details for " + package)
                scraper.ingest_dataset(package)
            except:
                print("Could not load data.")
    elif command == "ingest_by_package_name":
        package = args[1]
        DataDotGovScraper(None).ingest_dataset(package)
    elif command == "search":
        query = args[1:]
        print(SearchClient().search_by_partial_match(query, 10))
    else:
        print("Unsupported command")

if __name__ == "__main__":
    main()