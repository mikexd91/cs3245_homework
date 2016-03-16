#!/usr/bin/python
import re
import nltk
import sys
import getopt

from os import listdir
from os.path import isfile, join

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from math import sqrt

stemmer = nltk.stem.porter.PorterStemmer()

# Convenience methods
# python index.py -i /Users/mx/nltk_data/corpora/reuters/training -d dict.txt -p postings.txt
# python index.py -i ./training -d dict.txt -p postings.txt
# python index.py -i ./small -d dict.txt -p postings.txt

def build_index(document_dir):
    """
    Builds the index
    """
    index = {}
    term_freq = {}
    doc_word_count = {}
    files = listdir(document_dir)
    try:
        files.remove(".DS_Store")
    except:
        pass
    files.sort(key=lambda f: int(f))
    for f in files:
        path = join(document_dir, f)
        if isfile(path):
            input_file = file(path, 'r')
            for line in input_file:
                for sent in sent_tokenize(line):
                    for word in word_tokenize(sent):
                        stemmed_word = stemmer.stem(word)
                        token = stemmed_word.lower()
                        
                        # Builds the document frequency hash table
                        if token not in index:
                            index[token] = []
                        if len(index[token]) == 0 or index[token][-1] != f: # f is file name
                            index[token].append(f)

                        # Builds the term frequency hash table
                        if token not in term_freq:
                            term_freq[token] = []
                        term_freq[token].append(f)

                        # Builds the number of words hash table
                        if f not in doc_word_count:
                            doc_word_count[f] = {}
                        if token not in doc_word_count[f]:
                            doc_word_count[f][token] = 0
                        doc_word_count[f][token] += 1

    # Calculate the doc cosine normalisation denominator
    euclidean_denominator = {}
    for doc_id in files:
        # print map(lambda x: x[1], doc_word_count[doc_id].items())
        denominator = reduce(lambda x, y: x + y,map(lambda x: x[1]**2, doc_word_count[doc_id].items()))
        euclidean_denominator[doc_id] = sqrt(denominator)
        print euclidean_denominator[doc_id]

    return (index, term_freq, files, euclidean_denominator)

def write_index(output_dict_file, output_post_file, index, term_freq, doc_ids, euclidean_denominator):
    """
    Writes the index to the output dictionary file and postings file
    """
    dict_file = file(output_dict_file, "w")
    post_file = file(output_post_file, "w")
    count_bytes = 0

    # Write the document length as first line of dictionary file
    dict_file.write(str(len(doc_ids)) + "\n")
    # count_bytes += len(doc_ids)
    
    # Writes doc, freq into postings file
    for token in index:
        postings = index[token] # a list of unique document id that contains the term
        term_occurrences = term_freq[token] # a list of document id that contains the term (repeats include)

        # Constructing the string to be written into the postings
        postings_string = generate_postings_string(postings, term_occurrences, euclidean_denominator)

        # Constructing the string to be written into the dictionary
        dict_string = token + " " + str(count_bytes) + " " + str(len(postings)) + "\n"

        # Writing to the respective files
        dict_file.write(dict_string)
        post_file.write(postings_string)
        
        # Update the byte offset so that postings file is written correctly
        count_bytes += len(postings_string)
    
    dict_file.close()
    post_file.close()

def generate_postings_string(postings, term_occurrences, euclidean_denominator):
    """
    Generates the posting for a term
    """
    # Creates the term frequency hash table
    term_freq = {}
    for doc_id in term_occurrences:
        if doc_id not in term_freq:
            term_freq[doc_id] = 1
        else:
            term_freq[doc_id] += 1

    # Constructs the string
    string = ""
    for doc_id in postings:
        string += doc_id + " " + str(term_freq[doc_id]/euclidean_denominator[doc_id]) + " "
    return string.strip() + "\n"

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

document_dir = output_dict_file = output_post_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        document_dir = a
    elif o == '-d':
        output_dict_file = a
    elif o == '-p':
        output_post_file = a
    else:
        assert False, "unhandled option"
if document_dir == None or output_dict_file == None or output_post_file == None:
    usage()
    sys.exit(2)

# dict and postings creation
(index, term_freq, doc_ids, euclidean_denominator) = build_index(document_dir)
write_index(output_dict_file, output_post_file, index, term_freq, doc_ids, euclidean_denominator)