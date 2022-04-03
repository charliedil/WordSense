"""
Most Frequent Sense Baseline:
              phone   product
phone          0      72
product        0      54
OVERALL ACCURACY:
0.42857142857142855

"""


import math
import re
import sys

train_path = sys.argv[1]
test_path = sys.argv[2]
log_path = sys.argv[3]

train_file = open(train_path, "r")
train_file_text = train_file.read()
train_file.close()

## Parse training file

context_to_label = {"phone":[],"product":[]}
phone_word_freq = {}
product_word_freq = {}
feature_score = {}

last_label = ""
context = False
train_lines = train_file_text.split("\n")
for line in train_lines:
    if context:
        context_to_label[last_label].append(line)
        context = False
        last_label = ""
    if line.startswith("<answer"):
        last_label = re.search(r"senseid=\"(.*)\"", line).group(1)
    if line.startswith("<context>"):
        context = True
mfs = ""
if (len(context_to_label["product"]) >len(context_to_label["phone"]) ):
    mfs = "product"
else:
    mfs = "phone"

for sent in context_to_label["phone"]:
    toks = sent.split(" ")
    for tok in toks:
        if not tok.startswith("<") and tok!="":
            if tok not in phone_word_freq:
                phone_word_freq[tok] = 1
            else:
                phone_word_freq[tok] += 1
for sent in context_to_label["product"]:
    toks = sent.split(" ")
    for tok in toks:
        if not tok.startswith("<") and tok!="":
            if tok not in product_word_freq:
                product_word_freq[tok] = 1
            else:
                product_word_freq[tok] += 1

for key in phone_word_freq:
    if key in product_word_freq:
        score = math.log(phone_word_freq[key]/product_word_freq[key])
        if score <= 0:
            feature_score[key] = [-score, "product"]
        else:
            feature_score[key] = [score, "phone"]
    else:
        feature_score[key] = [1, "phone"]

for key in product_word_freq:
    if key not in feature_score:
        feature_score[key] = [1, "product"]

n=10 #it can be anything tho
feature_vec = []
feature_result =[]

for i in range(n):
    max = -1
    max_key = ""
    for key in feature_score:
        if feature_score[key][0]>max and key not in feature_vec:
            max = feature_score[key][0]
            max_key = key
    feature_vec.append(max_key)
    feature_result.append(feature_score[max_key][1])

test_file = open(test_path,"r")
test_lines = test_file.read().split("\n")
test_file.close()

log_file = open(log_path,"w")


print(feature_vec)
print(feature_result)

for line in test_lines:
    if line.startswith("<instance"):
        id = re.search(r"id=\"(.*)\"", line).group(1)
        print("<answer instance=\""+id+"\" senseid=\""+mfs+"\"/>")
        log_file.write("<answer instance=\""+id+"\" senseid=\""+mfs+"\"/>\n")
    if line.startswith("<context>"):

log_file.close()
 ### BASELINE CODE

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