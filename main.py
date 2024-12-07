#!/usr/bin/env python2

import argparse
import pandas as pd
import numpy as np
import torch

from es.es import ES
from scrapers.data_dot_gov_scraper import DataDotGovScraper
from search.search_client import SearchClient
from random import randint

def main():
    # create parser object
    parser = argparse.ArgumentParser(description="nucleai cli for searching, ingesting, and downloading datasets.")

    # defining arguments for parser object
    parser.add_argument("-ots", "--one_time_setup", nargs="*",
                        help="Setups up metadocument index in the elasticsearch. This only needs to be done once.")

    parser.add_argument("-s", "--search", nargs=1,
                        help="Searched metadocument index by keywords. Returns top 10 matches by reverse indexing.")

    parser.add_argument("-d", "--download", type=str, nargs=1,
                        help="Downloads and pickles data based off dataset id.")

    parser.add_argument("-dt", "--download_and_tensorize", type=str, nargs=1,
                        help="Downloads, tensorizes, and pickles data based off dataset id.")

    parser.add_argument("-dttws", "--download_tensorize_two_way_split", type=str, nargs=1,
                        help="Downloads, tensorizes, splits across two tensors, and pickles data based off dataset id.")


    # The following should probably live in a different package as they help to ingest.
    parser.add_argument("-iq", "--ingest_by_query", type=str, nargs=1,
                        help="Ingests data from data.gov into the elasticsearch by keywords.")

    parser.add_argument("-ip", "--ingest_by_package", type=str, nargs=1,
                        help="Ingests data from data.gov into the elasticsearch by name of data.gov package.")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.one_time_setup != None:
        print("INFO: Setting up metadocument index.")
        ES().init_metadocument_index()
    elif args.ingest_by_query != None:
        query = args.ingest_by_query[0]
        print("INFO: Ingesting all datasets related to %s." % query)
        scraper = DataDotGovScraper(query)
        packages = scraper.get_packages()[1080:]
        for package in packages:
            try:
                print("Getting details for " + package)
                scraper.ingest_dataset(package)
            except:
                print("ERROR: Could not load data.")
    elif args.ingest_by_package != None:
        package = args.ingest_by_package[0]
        print("INFO: Ingesting dataset called to %s." % package)
        DataDotGovScraper(None).ingest_dataset(package)
    elif args.search != None:
        query = args.search[0]
        print("INFO: Searching our database for %s." % query)
        print(SearchClient().search_by_partial_match(query, 10))
    elif args.download != None:
        dataset_id = args.download[0]
        cleaned_dataframe = get_cleaned_dataframe(dataset_id)

        print("INFO: Pickling %s dataset." % dataset_id)
        cleaned_dataframe.to_pickle("%s_dataframe.pkl" % dataset_id)
    elif args.download_and_tensorize != None:
        dataset_id = args.download_and_tensorize[0]
        cleaned_dataframe = get_cleaned_dataframe(dataset_id)
        torch_tensor = one_hot_encode_and_tensorize(dataset_id, cleaned_dataframe)

        print("INFO: Pickling %s dataset." % dataset_id)
        torch.save(torch_tensor, "%s.tensor" % dataset_id)
    elif args.download_tensorize_two_way_split != None:
        # For now, comment these lines out since the elasticsearch is down.
        # dataset_id = args.download[0]
        # cleaned_dataframe = get_cleaned_dataframe(dataset_id)

        # Temporarily, dataset_id will refer to the URL passed in.
        dataset_id = args.download_tensorize_two_way_split[0]
        cleaned_dataframe = get_cleaned_dataframe_by_url(dataset_id)

        num_rows = cleaned_dataframe.shape[0]
        num_columns = len(cleaned_dataframe.columns)

        first_split_rows_sample_size = randint(num_rows / 2 - 1, num_rows)
        second_split_rows_sample_size = randint(num_rows / 2 - 1, num_rows)

        first_split_columns_sample_size = randint(num_columns / 2 - 1, num_columns)
        second_split_columns_sample_size = randint(num_columns / 2 - 1, num_columns)

        first_split_dataframe = cleaned_dataframe.sample(first_split_rows_sample_size)\
            .sample(first_split_columns_sample_size, axis=1).apply(np.random.permutation)
        second_split_dataframe = cleaned_dataframe.sample(second_split_rows_sample_size)\
            .sample(second_split_columns_sample_size, axis=1).apply(np.random.permutation)

        first_torch_tensor = one_hot_encode_and_tensorize(dataset_id, first_split_dataframe)
        second_torch_tensor = one_hot_encode_and_tensorize(dataset_id, second_split_dataframe)

        print("INFO: Pickling %s dataset." % dataset_id)
        torch.save(first_torch_tensor, "tmp-%s-1.tensor" % hash(dataset_id))
        torch.save(second_torch_tensor, "tmp-%s-2.tensor" % hash(dataset_id))

def get_cleaned_dataframe(dataset_id):
    print("INFO: Converting %s to dataframe." % dataset_id)
    metadocument = SearchClient().search_by_id(dataset_id)
    dataframe = pd.read_csv(metadocument["_source"]["dataset_source"])
    return dataframe.apply(pd.to_numeric, errors='ignore')

def get_cleaned_dataframe_by_url(url):
    print("INFO: Converting %s to dataframe." % url)
    dataframe = pd.read_csv(url)
    return dataframe.apply(pd.to_numeric, errors='ignore')

def one_hot_encode_and_tensorize(dataset_id, cleaned_dataframe):
    print("INFO: One shot encoding %s dataset." % dataset_id)
    one_hot_encoded = pd.get_dummies(cleaned_dataframe)

    print("INFO: Tensorizing %s dataset." % dataset_id)
    tensorized_dataframe = one_hot_encoded.astype(np.float64)
    matrix = [tensorized_dataframe[column].values for column in tensorized_dataframe if not type(tensorized_dataframe[column].values[0]) is np.ndarray]
    # Somewhere along the way, a column is becoming a tuple rather than scalar. Temporary hack to bypass this issue.
    return torch.tensor(matrix)

if __name__ == "__main__":
    main()