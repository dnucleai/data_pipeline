############################################################################
                       # Tag Class - JSON-stored object
############################################################################
"""This is the Tag class stored on the database in JSON, contains metadata
tags and query keywords for fast lookup via LDA
"""

import json
import pandas as pd

class Tag(Object):
    """Tag class - JSON serializable object created from a Pandas
    data frame and metadata tags
    
    documentName - title of the document
    dataSource - origin of data
    date - date of data
    submitter - individual who facilitated data submission
    dateSubmitted - date of submission
    file - Pandas.DataFrame object containing schema and data
    documentation - explanation of data source for LDA 
    """
    
    def __init__(self, documentName, dataSource, date, submitter, dateSubmitted, file, documentation=None):
        self.documentName = name
        self.dataSource = dataSource
        self.date = date
        self.submitter = submitter
        self.dateSubmitted = dateSubmitted

        self.file = file
        
        if (not documentation): 
            self.ldaKeywords = self.get_lda(documentation)
        else:
            self.ldaKeywords = None
            
        self.meta = {"_documentname": name, "_datasource": dataSource, "_date": date,
                     "_submitter": submitter, "_datesubmitted": dateSubmitted, "_keywords" = self.ldaKeyWords}
    
    """Returns the data in JSON format without metatags
    """
    def get_json(self):
        return self.file.file.to_json(orient='row')
    
    """Returns the metatags in JSON format
    """
    def meta_json(self):
        return json.dumps(self.meta)

    """Returns keywords of the documentation associated with LDA
    """
    def get_lda(self, doc):
        pass

