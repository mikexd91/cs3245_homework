This is the README file for A0122081X's submission

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

index.py indexes the corpus and stores the dictionary as a (term, byte_offset, document_frequency) triple. The document frequency is needed to calculate the term idf later during the search phase, while the byte offset is used later in the search phase to bring the postings from the hard disk into memory. The total number of documents in the corpus is also stored as the first line of the dictionary file.

To construct the postings list, index.py calculates every term's normalised weight and stores it as a (doc_id, normalised_weight) pair. If a term is found in more than one document, the subsequent (doc_id, normalised_weight) pair is written on the same line.

For example, "5435 0.133971237705 9345 0.155525451398" means that the term is found in document 5435 with a normalised weight of 0.133, and in document 9345 with a normalised weight of 0.155. 

search.py first reads in the dictionary and stores the contents of dict.txt as a python dictionary. Then search.py reads in the set of queries and performs the necessary operations on every query term. In the query execution loop, the idf is calculated, the normalised weight for each query term is calculated. To get the score, the normalised weight of the term in the document is multiplied by the normalised weight of the term in the query, and summed up. The list of top 10 results are then written out to the output file.

During the operations, all values are stored in a python dictionary named "table". Each key of table contains another python dictionary. A sample structure is given below:

table: {
  "query": {
    "term": raw frequency,
    ...
  },

  "idf": {
    "term": term idf,
    ...
  },

  doc_id_1: {
    "term": normalised weight,
    ...
  },

  doc_id_2: {
    "term": normalised weight,
    ...
  }
}

Subsequently, the raw frequency in the "query" dictionary will be updated with the tf-idf and eventually the normalised weight.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py - the program in charge of generating the dictionary and postings file
search.py - the program that reads in queries from the query file and outputs them to the output file
ESSAY.txt - responses to the essay questions
README.txt - this file

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0122081X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

Full credit for the assignment.

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Ian Ngiaw (CS3245 classmate). We previously did HW2 together, so index.py might share similar code since I modified the indexer from HW2 to fit the requirements for this homework.
Other classmates on the forums for checking of results for certain query terms.









