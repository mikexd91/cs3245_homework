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
    doc_score_lst = [] # used to store all the (document, score) tuples

    query_lst = []
    document_lst = []

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

            # Input the NORMALIZED tf (read from the postings file) for the term in every document
            byte_offset = dictionary[term][0]
            # print (term, dictionary[term][0])
            posting_reader = NoobReader(postings, byte_offset)  
            containing_docs = posting_reader.to_list()

            # Build the rows
            for (doc_id, freq) in containing_docs:
                if doc_id not in table:
                    table[doc_id] = {}
                table[doc_id][term] = freq     

            # Calculate the score for term
            # Query scores don't change, they remain constant throughout the query
            # ltc scheme: NORMALIZE((1+lg(tf)) * idf)

            # Calculate the score for document
            # Document scores change per document

            # Pseudo code
            # 1. Read in all the documents that contain the query terms
            # 2. Calculate lnc score for the document - maintain a mapping from document id to document score
            # 3. After all scores have been calculated, sort them and return top 10
            
        # Normalising can only be done after every term has been looked at  
        # do the normalising here
        # print "outside the loop: ", table        

        # Overwrite the values with the tf-idf score for query (the values used to be raw tf)
        for (term, freq) in table["query"].items():
            table["query"][term] = (1+math.log(table["query"][term], 10)) * table["idf"][term]

        # Construct normalised value for query column
        unit_length = reduce(lambda x, y: x+y, map(lambda x: x[1]**2, table["query"].items()))
        unit_length = math.sqrt(unit_length)
        for (term, freq) in table["query"].items():
            # Overwrite the values with the normalised weight
            table["query"][term] = table["query"][term] / unit_length
            # print term, table["idf"][term]

        # Construct normalised value for every document
        all_doc_ids = table.keys()
        all_doc_ids.remove("idf")
        all_doc_ids.remove("query")

        # # Overwrite the values with the normalised score (the values used to be raw tf)
        # for doc_id in all_doc_ids:
        #     doc_dct = table[doc_id]
        #     print doc_dct
        #     doc_length = 0
            
        #     doc_length = reduce(lambda x, y: x+y, map(lambda x: x[1]**2, doc_dct.items()))
        #     doc_length = math.sqrt(doc_length)

        #     for (term, freq) in doc_dct.items():
        #         doc_dct[term] = doc_dct[term] / doc_length

        # print table # by this step, all the documents have a correct normalised weight for each term

        # Construct (doc_id, all query terms) score
        doc_score = {}
        for doc_id in all_doc_ids:
            doc_score[doc_id] = 0

        for (term, wt) in table["query"].items():
            for doc_id in all_doc_ids:
                if term in table[doc_id]:
                    doc_score[doc_id] += table[doc_id][term] * wt

        # print doc_score
        print sorted(doc_score.items(), key=lambda x: x[1], reverse=True)[:10]
        foo = map(lambda x: x[0], filter(lambda x: x[1] > 0, sorted(doc_score.items(), key=lambda x: x[1], reverse=True)[:10]))

        # Write to file
        output_line = reduce(lambda x, y: x + str(y) + " ", foo, "").strip() + "\n"
        output.write(output_line)

class NoobReader:
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
# print dictionary
execute_queries(input_post_file, input_query_file, output_file, dictionary, document_length)