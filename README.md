
# Information Retrieval Project - 
# Wikipedia Search Engine

## Overview
This project is an Information Retrieval (IR) system designed to search and retrieve relevant information from the entire English Wikipedia corpus. The system utilizes a combination of techniques, including tokenization, inverted indexing, and the BM25 ranking algorithm. Additionally, it incorporates PageRank scores to enhance result relevance.

## Inverted index with BM25:
Inverted index for the body and the titels of Wikipedia articles using the BM25 ranking algorithm. The process involves tokenizing the text, calculating term frequencies (tf), document frequencies (df), and BM25 scores. Additionally, the code handles the partitioning and writing of posting lists to a Google Cloud Storage (GCS) bucket.

## Inverted index with Cosine Similarity and TFIDF
Inverted index with cosine similarity and TFIDF (Term Frequency-Inverse Document Frequency) ranking for the body of Wikipedia articles. This index enhances the relevance of search results by considering the frequency of terms and their importance across the entire document corpus.

## PageRank and Page Views:
PageRank and Page Views to assess the importance of Wikipedia articles. The integration involves computing the PageRank scores for articles and incorporating the monthly page views data
