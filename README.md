# Data Pipeline

## Overview
This package maintains all necessary logic for ingesting, cleaning, and querying data to be used by nuclei.ai.

## APIs/ CLI
The following are the APIs currently supported as well as CLI examples:
* `search`
  * Searches our elasticsearch by topics and keywords.
  * `./main.py -s "aids"`
* `download`
  * Downloads the data specified by the id as a panda dataframe.
  * `./main.py -d "filgZ2QBr5XMuPgIx4DZ"` where filgZ2QBr5XMuPgIx4DZ is the _id returned by search. The
  example _id will be stored in the current working directory as `filgZ2QBr5XMuPgIx4DZ_dataframe.pkl`
* `download_and_tensorize`
  * Downloads the data, one hot encodes it, coerces it to floats, and saves it as a pyTorch tensor.
  * `./main.py -dt "filgZ2QBr5XMuPgIx4DZ"` where filgZ2QBr5XMuPgIx4DZ is the _id returned by search. The
  example _id will be stored in the current working directory as `filgZ2QBr5XMuPgIx4DZ.tensor`
* `download_tensorize_two_way_split`
  * Downloads the data, splits it randomly by rows and columns, one hot encodes it, coerces it to floats, and saves it as pyTorch tensor.
  * `./main.py -dttws "https://data.wprdc.org/dataset/2cff4c07-423a-4b61-af08-7288fbb773eb/resource/b0c22ad4-7afb-496b-9500-3aebf91e67d6/download/toxics-release-inventory-pennsylvania-1987-2015.csv"`

## Setup Commands

### Setting up elasticsearch from scratch
The elasticsearch cluster is able to efficiently reduce memory be using property mappings and types. The
metadocument index which stores metadata of all datasets uses this.
However, this requires a one time setup with `./main.py -ots`

### Populating elasticsearch
For an example of how this elasticsearch cluster will look, try ingesting some sample datasets. You
can ingest datasets by query words (recommended) or you can go by package names (the unique names of the
datasets from data.gov). As of now, we only accept data from data.gov that is in a CSV format. To try this
out, run `./main.py -iq "aids"`

## Original Design
https://docs.google.com/document/d/19ouGD-fTquIGQ2zHxmWc8ZM6DNSLCk7gdREckT72dco/edit