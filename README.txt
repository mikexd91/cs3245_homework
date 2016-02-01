This is the README file for A0000000X's submission

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

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

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Ian Ngiaw (CS3245 classmate). It's rather hard to put in words what he helped with, so I will use an example to illustrate:

Let a, b, c be distinct 4-grams.
Let x be the total count of a particular language.
At first what I did was log(count(a) * count(b) * count(c)) / log(x**3), since I wanted to save time on division.
Subsequently, with his advice, I changed it to log(count(a)/x) + log(count(b)/x) + log(count(c)/x), because in the test sample, x is rather large, and when it's raised to the n-th power, it will result in an integer overflow, thus giving me wrong results.









