This is the README file for A0122081X's submission

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

I used a dictionary with the language labels as keys. Under each label is a dictionary, with the 4-grams as key and its corresponding number of occurrences as value. I used a tuple to represent the 4-gram. For example, "abcd" would be stored as ('a', 'b', 'c', 'd'). I have also chosen not to pad the ngram. The data structure is simplified as below:

{
  "malaysian": {('a', 'b', 'c', 'd'): 4, ('b', 'c', 'd', 'e'): 1, ...},
  "indonesian": {('a', 'b', 'c', 'd'): 2, ('b', 'c', 'd', 'e'): 2, ...},
  "tamil": {('a', 'b', 'c', 'd'): 3, ('b', 'c', 'd', 'e'): 5, ...},
}

I also have list containing all possible 4-grams that is used for smoothing. While the 4-grams are being constructed and added to each language's dictionary, I update their total tuple counts.

For essay experiments, line 42 is for Question 3b (effects of lowercase on accuracy). Line 11 is for varying the n-gram size for Question 4. 

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

build_test_LM.py - the file to run to create the LMs for testing
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

Full credit for the assignment. The only help I sought was for a mathematical oversight which is rather crucial, but not related to programming the algorithm for this homework.

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Ian Ngiaw (CS3245 classmate). It's rather hard to put in words what he helped with, so I will use an example to illustrate:

Let a, b, c be distinct 4-grams.
Let x be the total count of a particular language.
At first what I did was log(count(a) * count(b) * count(c)) / log(x**3), since I wanted to save time on division.
Subsequently, with his advice, I changed it to log(count(a)/x) + log(count(b)/x) + log(count(c)/x), because in the test sample, x is rather large, and when it's raised to the n-th power, it will result in an integer overflow, thus giving me wrong results.









