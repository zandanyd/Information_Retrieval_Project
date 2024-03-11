
# Information Retrieval Project - Wikipedia Search Engine

## Overview
This project is an Information Retrieval (IR) system designed to search and retrieve relevant documents from the entire English Wikipedia corpus (over 6 million articles). The system utilizes a combination of techniques, including tokenization, inverted indexing, and the BM25 ranking algorithm. Additionally, it incorporates PageRank scores to enhance result relevance.

# Inverted Inddex
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

## Inverted index with Cosine Similarity and TFIDF (Not used in the backend search)
Inverted index with cosine similarity and TFIDF (Term Frequency-Inverse Document Frequency) ranking for the body and title of Wikipedia articles. The process involves tokenizing the text, calculating term frequencies (tf), document frequencies (df). This index enhances the relevance of search results by considering the frequency of terms and their importance across the entire document corpus. Additionally, the code handles the partitioning and writing of posting lists to a Google Cloud Storage (GCS) bucket.

## PageRank and Page Views:
PageRank and Page Views to assess the importance of Wikipedia articles. The integration involves computing the PageRank scores for articles and incorporating the monthly page views data.

# Backend Search
### 1. Loading Index and Data
Retrieving Index and Data from GCS Bucket: Utilizes the read_pickle function to download pickled objects from a GCS bucket.
Read the index_title, index_data, title_dict and pageRank  
### 2. Tokenization and Stopword Removal
Tokenization and Stopword Removal for the query: Utilizes a regular expression (RE_WORD) for tokenization and removes common English stopwords to improve search accuracy.
### 3. Search Backend
Search Backend Functionality (search_backend): Processes user queries, tokenizes them, and performs parallel searches on title and body indices using BM25 and PageRank scores.
ThreadPoolExecutor for Parallel Execution: Employs concurrent.futures.ThreadPoolExecutor for parallel execution of search tasks.
Merging and Ranking Results for title and body: Merges and ranks the results of the body and title using BM25 and PageRank scores, returning the top 50 documents.
### 4. Search Helper
Search Helper Functionality (search_helper): Calculates scores for relevant documents based on BM25 and PageRank.
Inverted Index Utilization: Utilizes the inverted index for retrieving posting lists.
Sorting Relevant Documents: Returns a sorted list of relevant documents based on calculated scores.
### 5. Query IDF Calculation
Query IDF Calculation (query_idf): Computes IDF scores for query terms based on BM25.
Inverted Index Statistics Utilization: Utilizes document frequency and collection size from the inverted index.
Returns Term-to-IDF Mappings: Returns a dictionary of term-to-IDF mappings.
### 6. Merging Title and Body Results
Merging Title and Body Results (merge_title_body): Combines results from the title and body indices.
Weight Adjustment based on Query Length: Adjusts weights based on the length of the user query.
Sorting Relevant Documents: Returns a sorted list of merged document scores.
### 7. Mapping Results to Titles
Mapping Results to Titles (map): Retrieves titles for the top results using document IDs.
Returns Document ID-Title Pairs: Returns a list of tuples containing document IDs and corresponding titles.
### 8. PageRank and Page Views
PageRank Integration: PageRank scores are considered in document ranking.
Potential Page Views Integration: Functionality can be extended to integrate Page Views data for enhanced relevance.


