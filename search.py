#!/usr/bin/python
import re
import nltk
import sys
import getopt
import math

# For testing convenience, remove when submitting
# python search.py -d dict.txt -p postings.txt -q queries.txt -o output.txt

def build_dict(input_dict_file):
    """
    Builds the dictionary from the dictionary file. Kept in memory.
    Returns a dictionary
    """
    dict_file = file(input_dict_file, 'r')
    dictionary = {}
    document_length = 0

    # dictionary format:
    # { term: (byte_offset, document_frequency), ... }

    for line in dict_file:
        split_line = line.strip().split(" ")
        
        # Reading in document length, which is the first line of the file (this if triggerrs only once)
        if len(split_line) == 1:
            document_length = int(split_line[0])
            continue

        # Construct python dictionary
        token = split_line[0]
        byte_offset = int(split_line[1])
        freq = int(split_line[2])
        dictionary[token] = (byte_offset, freq)

    dict_file.close()
    return (dictionary, document_length)

def execute_queries(input_post_file, input_query_file, output_file, dictionary, document_length):
    """
    Tests the queries in the input_query_file based on the dictionary and postings.
    Writes results into output_file.
    """   

    # Initialisation
    queries = file(input_query_file, 'r')   
    postings = file(input_post_file, 'r')
    output = file(output_file, 'w')
    stemmer = nltk.stem.porter.PorterStemmer()

    # Dictionary to store all the scores
    table = {}

    # Reads the query line by line    
    for query in queries.readlines():
        terms = query.strip().split(" ")
        table["query"] = {}
        table["idf"] = {}

        # Scheme: lnc.ltc
        for term in terms:
            term = stemmer.stem(term).lower()

            # Update tf in "query" dictionary
            if term not in table["query"]:
                table["query"][term] = 1
            else:
                table["query"][term] += 1 
            
            # Calculate idf of this term
            # Optimised against query such as "cat cat cat cat" to avoid 
            # repeated calculation of idf of the same term
            if term not in table["idf"]:
                document_freq = dictionary[term][1]
                idf = math.log((float(document_length)/document_freq), 10)
                table["idf"][term] = idf # store the idf of this term into the dictionary

            # Read the NORMALIZED wt (read from the postings file) of the term in every document
            byte_offset = dictionary[term][0]
            posting_reader = PostingReader(postings, byte_offset)  
            containing_docs = posting_reader.to_list()

            # Build the rows
            for (doc_id, freq) in containing_docs:
                if doc_id not in table:
                    table[doc_id] = {}
                table[doc_id][term] = freq     
            
        # Normalising for documents can only be done after every term has been looked at
        # Same goes for the calculation of score
        # Do the normalising here

        # Overwrite the values with the tf-idf weight for query (the values used to be raw tf)
        for (term, freq) in table["query"].items():
            table["query"][term] = (1+math.log(table["query"][term], 10)) * table["idf"][term]

        # Construct normalised weight for query column
        unit_length = reduce(lambda x, y: x+y, map(lambda x: x[1]**2, table["query"].items()))
        unit_length = math.sqrt(unit_length)
        for (term, freq) in table["query"].items():
            # Overwrite the values with the normalised weight
            table["query"][term] = table["query"][term] / unit_length
        
        # Construct (doc_id, all query terms) score
        all_doc_ids = table.keys()
        all_doc_ids.remove("idf")
        all_doc_ids.remove("query")

        doc_score = {}
        for doc_id in all_doc_ids:
            doc_score[doc_id] = 0

        for (term, wt) in table["query"].items():
            for doc_id in all_doc_ids:
                if term in table[doc_id]: # if the ith term of the query is present in the document
                    doc_score[doc_id] += table[doc_id][term] * wt # table[doc_id][term] contains the normalised wt for term

        # print sorted(doc_score.items(), key=lambda x: (x[1], -x[0]), reverse=True)[:10]
        top_10 = map(lambda x: x[0], filter(lambda x: x[1] > 0, sorted(doc_score.items(), key=lambda x: (x[1], -x[0]), reverse=True)[:10]))
    
        # Write to file
        output_line = reduce(lambda x, y: x + str(y) + " ", top_10, "").strip() + "\n"
        output.write(output_line)

class PostingReader:
    def __init__(self, postings_file, byte_offset):
        self.postings_file = postings_file
        self.byte_offset = byte_offset
        self.end = False
        self.output = []

    def to_list(self):
        output = []
        doc_freq_lst = []
        self.postings_file.seek(self.byte_offset)

        parsed_string = ""
        while True:
            next_char = self.postings_file.read(1)
            if next_char == " ":
                # do something
                doc_freq_lst.append(float(parsed_string))
                parsed_string = ""
                continue
            if next_char == "\n":
                # End of line reached
                doc_freq_lst.append(float(parsed_string))
                break
            parsed_string += next_char

        # Format the list into (doc_id, freq) tuples
        for i in range(0, len(doc_freq_lst), 2):
            output.append((int(doc_freq_lst[i]), doc_freq_lst[i+1]))
        
        # print output
        return output

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

input_dict_file = input_post_file = input_query_file = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        input_dict_file = a
    elif o == '-p':
        input_post_file = a
    elif o == '-q':
        input_query_file = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_dict_file == None or input_post_file == None or input_query_file == None or output_file == None:
    usage()
    sys.exit(2)

# Execution
(dictionary, document_length) = build_dict(input_dict_file)
execute_queries(input_post_file, input_query_file, output_file, dictionary, document_length)