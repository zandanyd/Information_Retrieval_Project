# -*- coding: utf-8 -*-
import subprocess
import concurrent.futures
import re
import math
import pickle
from collections import defaultdict
import numpy as np
from nltk.corpus import stopwords
from inverted_index_gcp import *
import nltk
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')

inverted_index = InvertedIndex()
subprocess.call(['pip', 'install', 'pyspark'])

'''
Retrieving Index and Data from GCS Bucket: 
Utilizes the read_pickle function to download pickled objects from a GCS bucket.
'''
def read_pickle(bucket_name, pickle_route):
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(pickle_route)
    pick = pickle.loads(blob.download_as_bytes())
    return pick
    
# Read the index_title, index_data, title_dict and pageRank
index_title = read_pickle('208564682title','body/Title_BM25.pkl')
index_data = read_pickle('208564682bodyindex','body/body_BM25.pkl')
title_dict = read_pickle('208564682indextitle','path/to/TitleId.pickle')
pageRank = read_pickle('208564682pagerank','result_dict.pickle')

# Tokenize and remove stopwords
english_stopwords = frozenset(stopwords.words('english'))
corpus_stopwords = ["category", "references", "also", "external", "links",
                    "may", "first", "see", "history", "people", "one", "two",
                    "part", "thumb", "including", "second", "following",
                    "many", "however", "would", "became"]

all_stopwords = english_stopwords.union(corpus_stopwords)
RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}|3D""", re.UNICODE)
NUM_BUCKETS = 124

def tokenize(text):
        """
        Tokenizes the input text into a list of tokens and filters out stopwords.
        Parameters:
            text (str): The input text to tokenize.
        Returns:
            list of str: A list of tokens extracted from the text, excluding stopwords.
        """
        tokens = [token.group() for token in RE_WORD.finditer(text.lower()) ]
        return [token for token in tokens if token not in all_stopwords]


# Returns 50 of your best search results for the query
def search_backend(query):
  tokens = tokenize(query)
  # Use ThreadPoolExecutor for parallel execution
  with concurrent.futures.ThreadPoolExecutor() as executor:
      # Execute search_helper concurrently for title and body
      future_title = executor.submit(search_helper, tokens, '208564682title', index_title)
      future_body = executor.submit(search_helper, tokens, '208564682bodyindex', index_data)
      # Wait for both threads to complete
      top_title = future_title.result()
      top_body = future_body.result()
  # combine the title and body results
  top = merge_title_body(top_title,top_body, len(tokens))
  return map(top)

# calculate the score
def search_helper(tokens,bucket,index):
  SigmaIDF = query_idf(tokens,index)
  relevant_docs={}
  for term in tokens:
      posting_list = index.read_a_posting_list("", term, bucket)
      for id1 , tf in posting_list:
          page_rank = math.log10(pageRank[id1]) if id1 in pageRank and pageRank[id1] > 0 else 0
          relevant_docs[id1] = relevant_docs.get(id1,0) + (SigmaIDF.get(term, 0))*(tf*(1.5+1))/(tf+index.similarity[id1])+page_rank 
  # Sorting relevant_docs by score in descending order
  sorted_docs = sorted(relevant_docs.items(), key=lambda x: x[1], reverse=True)
  return sorted_docs[:50]

# calculate the query IDF
def query_idf(query,index):
  SigmaIDF = {}
  for term in np.unique(query):
      N = index.N
      n = index.df.get(term, 0)
      SigmaIDF[term] = math.log(((N - n + 0.5) / (n + 0.5)) + 1)
  return SigmaIDF

# combine the title and body results
def merge_title_body(title,data, query_len):
  title_weight, data_weight = (0.9, 0.1) if query_len <3 else (0.1, 0.9)
  merge = defaultdict(float)
  for key, value in title:
      merge[key] = merge.get(key,0) + title_weight * value
  for key, value in data:
      merge[key] = merge.get(key,0) + data_weight * value
  # Sorting relevant_docs by score in descending order
  sorted_docs = sorted(merge.items(), key=lambda x: x[1], reverse=True)
  return sorted_docs[:50]

# Find the titles for the top results
def map(top):
  new_dict = []
  for  id1, w in top:
          title = title_dict[id1]
          new_dict.append((str(id1), title))
  return new_dict
