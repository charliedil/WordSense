"""
Charlie Dil - Word Sense Disambiguation Project (wsd.py) 4/3/2022 Python 3.10

PROBLEM
With this program, we want to be able to distinguish the semantic meaning between words that look the same but mean
different things. In this project we are specifically distinguishing between phone line and product line.

EXAMPLE INPUT AND OUTPUT
To run the code from command line, run this line:

python3.10 wsd.py train_path test_path log_path

Notice that python3.10 is required for running this program.

The output will look like this:

<answer instance="line-n.w8_059:8174:" senseid="phone"/>
<answer instance="line-n.w8_059:8174:" senseid="product"/>
<answer instance="line-n.w8_059:8174:" senseid="phone"/>
...
Cut off for conciseness.

ALGORITHM - Bag of Words + Decision List
Step 1: Parse training data, extract data between <context> tag and the senseid located in the <answer> tag. Insert
into context_to_label dict (keys are the senseid, value is a list of all the contexts)
Step 2: Compare the length of context_to_label["phone"] with context_to_label["product"]. Mark the larger one as most
frequent sense for baseline and also default case if all the branches of the decision list fail.
Step 3: Create two unigram frequency tables, one for the contexts labeled phone and one for product. Iterate through the
sentences in the context_to_label dict to tally up the unigrams.
Step 4: Calculate the log ratio score of all the unigrams. If the word only occured in the context of one sense, I
assigned it a score of 1. There was no reason for this, and it may be worth experimenting with. This is all stored in
the feature_store dictionary where the key is the unigram and the value is an array of two elements: the absolute value
of the score and the senseid that is more frequently found with.
Step 5: Sort the features by score and take the top N. In this case, I used N=40. I merged these steps into for
efficiency by just looking for the max N times (I include a condition to ensure the same feature isn't picked multiple
times. I add the features into feature_vec and the associated label with that feature into feature_result
Step 6: Evaluation! I open the test file and parse in a similar fashion to step 1 to get the id and the sentence. I then
iterate through the features in feature_vec and check to see if each unigram is in the sentence. If it is, then the
corresponding label from feature_result is selected and output with the id extracted, similar to the example shown
above. All of this is also output to the log file for my testing purposes.

Features identified: ['telephone', 'access', 'machines', 'you', "ibm's", 'sales', 'plans', 'analysts', 'corp.', 'she',
'product', 'current', 'people', 'international', 'less', 'spokesman', 'selling', 'sell', 'first', 'sale',
'communications', 'information', 'line,', 'under', 'designed', 'american', 'includes', 'industry', 'years', 'no',
'calls', 'end', 'open', 'products', 'said.', 'stores', 'pacific', 'office', 'analyst', 'vice']

My implementation of the decision list simply loops through the features in my list and checks to see if that string
is present in the sentence containing the sense we are evaluating. If it is present, I output the value which is in the
same index of the feature in my list of values.

Most Frequent Sense Baseline:
              phone   product
phone          0      72
product        0      54
OVERALL ACCURACY:
0.42857142857142855

Bag of words, decision list N=40:
              phone   product
phone         54      18
product        3      51
OVERALL ACCURACY:
0.8333333333333334

As you increase N, it gets marginally better. But overall way better than the baseline :)

"""

import math
import re
import sys

# Take in command line args
train_path = sys.argv[1]
test_path = sys.argv[2]
log_path = sys.argv[3]

# Read training data
train_file = open(train_path, "r")
train_file_text = train_file.read()
train_file.close()

## Parse training file

context_to_label = {"phone": [], "product": []}  # Used to store context data associated with a certain sense id
phone_word_freq = {}  # unigram table for phone sense
product_word_freq = {}  # unigram table for product sense
feature_score = {}  # score the unigrams (log ratio). Also stores associated sense for Decision list component

last_label = ""  # used to hold the senseid
context = False  # have we seen the opening context tag?
train_lines = train_file_text.split("\n")  # parse line by line
for line in train_lines:
    if context:  # if we saw the context tag, the next line is the sentence we want to snag
        context_to_label[last_label].append(line)  # add this context to the list associated with whatever the sense is
        context = False  # reset this flag
        last_label = ""  # reset the label
    if line.startswith("<answer"):  # answer tag? we want the id
        last_label = re.search(r"senseid=\"(.*)\"", line).group(1)  # this regex pulls the senseid
    if line.startswith("<context>"):  # context tag? the next line will have the sentence, so change flag value now!
        context = True  # yes we have seen a context tag
mfs = ""  # "Most Frequent Sense"
if (len(context_to_label["product"]) > len(context_to_label["phone"])):  # Which was more common? prod or phone?
    mfs = "product"  # whichever is more common is the most common sense
else:
    mfs = "phone"
# Bag of words + D-list code below!
for sent in context_to_label["phone"]:  # Build unigram table for phone
    toks = sent.split(" ")
    for tok in toks:
        if not tok.startswith("<") and tok != "":  # remove noise
            if tok.lower() not in phone_word_freq:
                phone_word_freq[tok.lower()] = 1
            else:
                phone_word_freq[tok.lower()] += 1
for sent in context_to_label["product"]:  # build unigram table for product, same thing really
    toks = sent.split(" ")
    for tok in toks:
        if not tok.startswith("<") and tok != "":
            if tok.lower() not in product_word_freq:
                product_word_freq[tok.lower()] = 1
            else:
                product_word_freq[tok.lower()] += 1

for key in phone_word_freq:
    if key in product_word_freq:  # we can only calculate the score if it is in both tables
        score = math.log(phone_word_freq[key] / product_word_freq[key])  # the total part of this calculation cancels
        if score <= 0:
            feature_score[key] = [-score, "product"]
        else:
            feature_score[key] = [score, "phone"]
    else:
        feature_score[key] = [1, "phone"]

for key in product_word_freq:
    if key not in feature_score:
        feature_score[key] = [1, "product"]

n = 40  # it can be anything though
feature_vec = []  # this will have the names of the features
feature_result = [] # this will have the value (phone or product)

for i in range(n):  # find the max N times
    max = -1
    max_key = ""
    for key in feature_score:
        if feature_score[key][0] > max and key not in feature_vec:
            max = feature_score[key][0]
            max_key = key
    feature_vec.append(max_key)
    feature_result.append(feature_score[max_key][1])

# time for inference
test_file = open(test_path, "r")
test_lines = test_file.read().split("\n")
test_file.close()

log_file = open(log_path, "w")

# print(feature_vec)
# print(feature_result)

context = False  # used to mark whether we have just seen the context tag
id = ""
for line in test_lines:
    if line.startswith("<instance"):
        id = re.search(r"id=\"(.*)\"", line).group(1)  # get id
    if context:
        context = False
        found = False  # if this is false, then we are just going to assign it the mfs
        for i in range(len(feature_vec)):  # this is the decision list. instead of having n branches, I chose to loop N
            if feature_vec[i] in line.lower().split(" "):  # if the feature is present, we output right away
                print("<answer instance=\"" + id + "\" senseid=\"" + feature_result[i] + "\"/>")
                log_file.write("<answer instance=\"" + id + "\" senseid=\"" + feature_result[i] + "\"/>\n")
                found = True
                break
        if not found:
            print("<answer instance=\"" + id + "\" senseid=\"" + mfs + "\"/>")  # otherwise, output mfs instead
            log_file.write("<answer instance=\"" + id + "\" senseid=\"" + mfs + "\"/>\n")
    if line.startswith("<context>"):
        context = True  # mark that we just saw the context tag
log_file.close()

### BASELINE CODE - very similar to previous code, but simpler.

# test_file = open(test_path,"r")
# test_lines = test_file.read().split("\n")
# test_file.close()
#
# log_file = open(log_path,"w")
#
# for line in test_lines:
#     if line.startswith("<instance"):
#         id = re.search(r"id=\"(.*)\"", line).group(1)
#         print("<answer instance=\""+id+"\" senseid=\""+mfs+"\"/>")
#         log_file.write("<answer instance=\""+id+"\" senseid=\""+mfs+"\"/>\n")
# log_file.close()
