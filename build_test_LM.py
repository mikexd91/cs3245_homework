#!/usr/bin/python
import re
import nltk
import sys
import getopt

# For the math.log function to calculate the sum of low probabilities
import math

# ngram size, for Question 4
ngram_size = 4

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'

    # Dictionaries to hold the labels and their corresponding tuples
    d = {}
    d["malaysian"] = {}
    d["indonesian"] = {}
    d["tamil"] = {}
    all_lst = [] # stores all existing tuples from the training set. Used for smoothing later.

    # Store the total tuple count label
    tuplecount = {}
    tuplecount["malaysian"] = 0
    tuplecount["indonesian"] = 0
    tuplecount["tamil"] = 0

    # Read the file
    f = open(in_file, 'r')
    for line in f:
        label = line.split()[0]
        
        # Split the line (excluding label) into characters & exclude "\r\n"
        tokens = list(line[len(label)+1:].strip())

        # Testing for Qn 3b
        # tokens = list(line[len(label)+1:].strip().lower())

        # Build the dictionary
        for i in range(len(tokens)-(ngram_size-1)): # so as to keep the length of each tuple as ngram_size
            tup = tuple(tokens[i:i+ngram_size])
            if tup in d[label]:
                d[label][tup] += 1
            else:
                d[label][tup] = 1
            tuplecount[label] += 1
            all_lst += [tup,]

    # Smoothing
    # Add 1 to all existing entries
    for label, dct in d.iteritems():
        for tup, val in dct.iteritems():
            dct[tup] += 1
            tuplecount[label] += 1

    # Add non-existing tuple to dictionaries, and 1 count to each of the tuple
    for tup in all_lst:
        for label, _ in d.iteritems():
            if tup not in d[label]:
                d[label][tup] = 1
                tuplecount[label] += 1

    print "Finished building language models"
    return d, tuplecount
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."

    # this method is supposed to take in each line of the input.text.txt and output a 
    # corresponding label for the language
    # need to print the labels into the out_file which is input.predict.txt

    # Initalise
    d = LM[0]
    wordcount = LM[1]

    # Read the test file
    f = open(in_file, 'r')
    o = open(out_file, 'w')
    for line in f:
        misses = 0
        total_checks = 0
        malay, indon, tamil = 0, 0, 0
        tokens = list(line)
        
        for i in range(len(tokens)-(ngram_size-1)):
            tup = tuple(tokens[i:i+ngram_size])
            total_checks += 1

            # Calculate probabilities using log 
            try:
                malay += math.log(d["malaysian"][tup] / float(wordcount["malaysian"]))
                indon += math.log(d["indonesian"][tup] / float(wordcount["indonesian"]))
                tamil += math.log(d["tamil"][tup] / float(wordcount["tamil"]))
            except:
                # use this to calculate probabilities of being an alien string
                misses += 1
        
        # Check for alien. Use 75% miss-rate as arbitrary cut-off point (since 75 is A1)
        miss_rate = misses / float(total_checks)
        if miss_rate > 0.75:
            o.write("other " + line)
        else:
            output = max(malay, indon, tamil)
            if output == malay:
                o.write("malaysian " + line)
            elif output == indon:
                o.write("indonesian " + line)
            else:
                o.write("tamil " + line)

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
