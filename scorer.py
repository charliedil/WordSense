"""
Charlie Dil - Word Sense Disambiguation Project (scorer.py) 4/3/2022 Python 3.10
PROBLEM
Need to compare the output from my wsd.py file and the key file.

EXAMPLE:
You can run this program by running the following command:
python3.10 scorer.py predicted.txt line-key.txt

Output:
              phone   product
phone         54      18
product        3      51
OVERALL ACCURACY:
0.8333333333333334

Algorithm:
1. Open and read prediction file. Extract the following info: senseid and id. Append sense id to pred list. Open test
file and find the same id and add the sense of that to the true list.
2. Pass pred and true lists along with a labels list ("phone", "product") into the sklearn function for generating
a confusion matrix
3. Print the confusion matrix
4. Calculate accuracy. This is done by summing the diagonal of the matrix and dividing it by the total. Print this
result out.


"""


import sys
import re
from sklearn.metrics import confusion_matrix
# Collect command line args
pred_path = sys.argv[1]
true_path = sys.argv[2]

# open files
pred_file = open(pred_path, "r")
true_file = open(true_path, "r")

# used to store predictions vs actual
true = []
pred = []
labels = ["phone", "product"]  # all possible labels

# read files, parse line by line
pred_lines = pred_file.read().split("\n")
true_lines = true_file.read().split("\n")
# I assumed that there was a chance that the key wasn't in order.
for line in pred_lines:
    if line!="":
        id = re.search("instance=\"(.*)\"\s", line).group(1)  # extract id
        sense = re.search("senseid=\"(.*)\"",line).group(1)  # extract predicted senseid
        pred.append(sense)  # add to predicted labels
        for line2 in true_lines:  # now we have to find the corresponding line in the key
            if line2!="" and id==re.search("instance=\"(.*)\"\s", line2).group(1):  # extract id and compare in one line
                true.append(re.search("senseid=\"(.*)\"",line2).group(1))  # add to true labels
                break

# close the files
pred_file.close()
true_file.close()

# generate confusion matrix
cf_mat = confusion_matrix(true, pred, labels=labels)

# Printing results
sum_correct = 0  # used for overall accuracy
for i in range(len(labels)):
    sum_correct+=cf_mat[i][i]  # we add the diagonal
line = "              "  # to make the heading match up right
for l in labels:
    line+="{:8}".format(l)  # header line of matrix, has labels
print(line)
i=0  # used for printing the heading columns
for row in cf_mat:
    line = ""
    first = True  # if its first, print the label
    for val in row:
        if first:  # right here
            line+='{:8}'.format(labels[i])
            first = False  # now we do the rest of the line (the numbers)
            i+=1
        line+='{:8}'.format(val)
    print(line)  # we're printing it one row at a time

print("OVERALL ACCURACY:")
print(sum_correct/len(pred))  # print overall accuracy, calculated here

