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
        
        # Document length
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
                idf = math.log((document_length/document_freq), 10)
                table["idf"][term] = idf # store the idf of this term into the dictionary

            # Input the tf for the term in every document
            byte_offset = dictionary[term][0]
            posting_reader = PostingReader(postings, byte_offset)  
            containing_docs = posting_reader.to_list()

            # Build the rows
            for (doc_id, freq) in containing_docs:
                if doc_id not in table:
                    table[doc_id] = {}
                else:
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

        # Construct Reverse Polish Notation
        rpn_lst = shunting_yard(query)
        result = rpn_interpreter(dictionary, rpn_lst, postings)
        output_line = reduce(lambda x, y: x + str(y) + " ", result, "").strip() + "\n"
        output.write(output_line)

class NoobReader:
    def __init__(self, postings_file, byte_offset):
        self.postings_file = postings_file
        self.byte_offset = byte_offset
        self.end = False
        self.foo = []

    def read(self):
        return

class PostingReader:
    """
    PostingReader reads a posting list in a provided postings file object
    using the byte offset provided by a dictionary.
    """
    def __init__(self, postings_file, byte_offset):
        self.postings_file = postings_file
        self.byte_offset = byte_offset
        self.current = 0 # this is the offset that is added to the byte offset when seeking
        self.end = False # set to true when reached end of the list (end of line)

    def peek(self):
        """
        Retrieves the next doc id in the postings list
        """
        if self.end:
            return "END"
        current_offset = self.current
        self.postings_file.seek(self.byte_offset + current_offset)
        parsed_string = self.postings_file.read(1)
        current_offset += 1
        
        # Encounters a skip pointer, denoted in our postings file by a '*'
        is_skip = parsed_string == "*"
        if is_skip:
            # "*" in the postings list file indicates the number after it is a skip pointer
            parsed_string = "" 

        while True:
            self.postings_file.seek(self.byte_offset + current_offset)
            next_char = self.postings_file.read(1)
            if next_char == " ":
                current_offset += 1
                break
            if next_char == "\n":
                # End of line reached
                break
            parsed_string += next_char
            current_offset += 1

        if is_skip:
            # Returns a 3-tuple, the last being the new current if the skip pointer is used
            skip_gap = int(parsed_string)
            return (True, self.get_skip_value(current_offset, skip_gap), current_offset + skip_gap)

        return (False, int(parsed_string))
    
    def next(self):
        """
        Retrieves the next doc id in the postings list
        """
        if self.end:
            return "END"
        current_offset = self.current
        self.postings_file.seek(self.byte_offset + current_offset)
        parsed_string = self.postings_file.read(1)
        current_offset += 1
        
        # Encounters a skip pointer, denoted in our postings file by a '*'
        is_skip = parsed_string == "*"
        if is_skip:
            # "*" in the postings list file indicates the number after it is a skip pointer
            parsed_string = "" 

        while True:
            self.postings_file.seek(self.byte_offset + current_offset)
            next_char = self.postings_file.read(1)
            if next_char == " ":
                current_offset += 1
                break
            if next_char == "\n":
                # End of line reached
                self.end = True
                break
            parsed_string += next_char
            current_offset += 1

        self.current = current_offset
        if is_skip:
            # Returns a 3-tuple, the last being the new current if the skip pointer is used
            skip_gap = int(parsed_string)
            return (True, self.get_skip_value(current_offset, skip_gap), current_offset + skip_gap)

        return (False, int(parsed_string))
    
    def get_skip_value(self, current_offset, skip_gap):
        parsed_string = ""
        while True:
            self.postings_file.seek(self.byte_offset + current_offset + skip_gap)
            next_char = self.postings_file.read(1)
            if next_char == " " or next_char == "\n":
                break
            parsed_string += next_char
            skip_gap += 1
        return int(parsed_string)
    
    def skip_to(self, new_current):
        """
        Sets the current to the provided new_current value
        """
        self.current = new_current

    def to_list(self):
        temp_current = self.current
        temp_end = self.end

        result = []
        self.current = 0
        self.end = False

        while self.peek() != "END":
            next_item = self.peek()
            if not next_item[0]:
                result.append(next_item[1])
            self.next()

        self.current = temp_current
        self.send = temp_end
        return result

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
print dictionary
execute_queries(input_post_file, input_query_file, output_file, dictionary, document_length)