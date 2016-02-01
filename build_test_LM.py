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
    all_lst = []

    wordcount = {}
    wordcount["malaysian"] = 0
    wordcount["indonesian"] = 0
    wordcount["tamil"] = 0

    # Read the file
    f = open(in_file, 'r')
    for line in f:
        label = line.split()[0]
        
        # Split the line (excluding label) into characters & exclude "\r\n"
        tokens = list(line[len(label)+1:].strip())

        # Build the dictionary
        for i in range(len(tokens)-3): # so as to keep the length of each tuple as 4
            tup = tuple(tokens[i:i+4])
            if tup in d[label]:
                d[label][tup] += 1
            else:
                d[label][tup] = 1
            wordcount[label] += 1
            all_lst += [tup,]

    # Smoothing
    # Add 1 to all existing entries
    for label, dct in d.iteritems():
        for tup, val in dct.iteritems():
            dct[tup] += 1
            wordcount[label] += 1

    # Add non-existing tuple to dictionaries, and 1 count
    for tup in all_lst:
        for label, _ in d.iteritems():
            if tup not in d[label]:
                # print tup, "added to " + label
                d[label][tup] = 1
                wordcount[label] += 1

    # print wordcount
    print d["malaysian"]
    # print d["indonesian"]
    # print d["tamil"]
    # print d["malaysian"][('e','m','u','a')] / float(wordcount["malaysian"])
    # print d["indonesian"][('e','m','u','a')] / float(wordcount["indonesian"])
    # print d["tamil"][('e','m','u','a')] / float(wordcount["tamil"])
    # print d["malaysian"][('e','m','u','a')]+1 / float(35690)


    # print d["tamil"]
    # print d["malaysian"]
    # print d["all"]
    print "Finished building language models"
    
    asdf = open("testtest.txt", "w")
    asdf.write(str(d))

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
        # malay, indon, tamil = 1, 1, 1
        malay, indon, tamil = 0, 0, 0
        tokens = list(line)
        for i in range(len(tokens)-3):
            tup = tuple(tokens[i:i+4])
            
            # Add up the probabilities first
            try:
                # malay *= d["malaysian"][tup]
                # indon *= d["indonesian"][tup]
                # tamil *= d["tamil"][tup]
                malay += math.log(d["malaysian"][tup] / float(wordcount["malaysian"]))
                indon += math.log(d["indonesian"][tup] / float(wordcount["indonesian"]))
                tamil += math.log(d["tamil"][tup] / float(wordcount["tamil"]))
            except:
                pass
            # count += 1

        # malay = math.log(malay) - math.log(wordcount["malaysian"]**count)
        # indon = math.log(indon) - math.log(wordcount["indonesian"]**count)
        # tamil = math.log(tamil) - math.log(wordcount["tamil"]**count)

        output = max(malay, indon, tamil)
        print malay, indon, tamil
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
