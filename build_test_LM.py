#!/usr/bin/python
import re
import nltk
import sys
import getopt

# To calculate the sum of low probabilities
import math

# python build_test_LM.py -b input.train.txt -t input-file-for-testing-LM -o output-file

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'

    # Initialise all variables
    d = {}
    d["malaysian"] = {}
    d["indonesian"] = {}
    d["tamil"] = {}
    d_all = {} # to be used for smoothing
    wordcount = {}
    wordcount["malaysian"] = 0
    wordcount["indonesian"] = 0
    wordcount["tamil"] = 0

    # Read the file
    f = open(in_file, 'r')
    for line in f:
        label = line.split()[0]
        
        # Split the line (excluding label) into characters & exclude "\r\n" which are the last two characters
        tokens = list(line[len(label)+1:])[:-2] 

        # Build the dictionary
        for i in range(len(tokens)-3):
            tup = tuple(tokens[i:i+4])
            if tup in d[label]:
                d[label][tup] += 1
                d_all[tup] += 1
            else:
                d[label][tup] = 1
                d_all[tup] = 1
            wordcount[label] += 1
    print wordcount
    print d["malaysian"][('e','m','u','a')]

    # Smoothing
    for label, dct in d.iteritems():
        for tup, val in dct.iteritems():
            dct[tup] += 1

    for k, v in d_all.iteritems():
        for label, _ in d.iteritems():
            if k not in d[label]:
                d[label][k] = 1
                wordcount[label] += 1

    temp_malay = 0
    print d["malaysian"]
    for tup, val in d["malaysian"].iteritems():
        temp_malay += 1

    print wordcount
    # print d["malaysian"][('e','m','u','a')]+1 / float(35690)


    # print d["tamil"]
    # print d["malaysian"]
    # print d["all"]
    print "Finished building language models"
    return d, wordcount
    
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below

    # this method is supposed to take in each line of the input.text.txt and output a 
    # corresponding label for the language
    # need to print the labels into the out_file which is input.predict.txt

    # Initaliaze
    d = LM[0]
    wordcount = LM[1]
    count = 0

    # Read the test file
    f = open(in_file, 'r')
    o = open(out_file, 'w')
    for line in f:
        malay, indon, tamil = 1, 1, 1
        tokens = list(line)
        for i in range(len(tokens)-3):
            tup = tuple(tokens[i:i+4])
            
            # Add up the probabilities first
            try:
                malay *= d["malaysian"][tup]
                indon *= d["indonesian"][tup]
                tamil *= d["tamil"][tup]
            except:
                pass
            count += 1

        malay = math.log(malay) - math.log(wordcount["malaysian"]**count)
        indon = math.log(indon) - math.log(wordcount["indonesian"]**count)
        tamil = math.log(tamil) - math.log(wordcount["tamil"]**count)

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
