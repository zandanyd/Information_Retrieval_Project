
# Information Retrieval Project - Wikipedia Search Engine

## Overview
This project is an Information Retrieval (IR) system designed to search and retrieve relevant information from the entire English Wikipedia corpus. The system utilizes a combination of techniques, including tokenization, inverted indexing, and the BM25 ranking algorithm. Additionally, it incorporates PageRank scores to enhance result relevance.

## Inverted Inddex GCP
inverted index for information retrieval, incorporating functionality for writing and reading the index to and from disk. The code employs multiple file writers and readers to handle large posting lists efficiently. Additionally, it includes methods for adding documents to the index and calculating global term statistics.
Parameters:
self.df: Counter object storing the document frequency per term.
self.term_total:Counter object storing the total frequency per term.
self._posting_list: defaultdict(list) for storing posting lists while building the index.
Use: Internally holds posting lists during the index construction phase.
self.posting_locs: defaultdict(list) mapping terms to posting list file locations.
self.N: Integer storing the total number of documents in the index.
self.similarity: Dictionary storing cosine similarity or BM25 values between documents.

## Inverted index with BM25:
Inverted index for the body and the titels of Wikipedia articles using the BM25 ranking algorithm. The process involves tokenizing the text, calculating term frequencies (tf), document frequencies (df), and BM25 scores. Additionally, the code handles the partitioning and writing of posting lists to a Google Cloud Storage (GCS) bucket.

## Inverted index with Cosine Similarity and TFIDF
Inverted index with cosine similarity and TFIDF (Term Frequency-Inverse Document Frequency) ranking for the body and title of Wikipedia articles. The process involves tokenizing the text, calculating term frequencies (tf), document frequencies (df). This index enhances the relevance of search results by considering the frequency of terms and their importance across the entire document corpus. Additionally, the code handles the partitioning and writing of posting lists to a Google Cloud Storage (GCS) bucket.

## PageRank and Page Views:
PageRank and Page Views to assess the importance of Wikipedia articles. The integration involves computing the PageRank scores for articles and incorporating the monthly page views data.




