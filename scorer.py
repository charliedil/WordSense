import sys
import re
from sklearn.metrics import confusion_matrix

pred_path = sys.argv[1]
true_path = sys.argv[2]
pred_file = open(pred_path, "r")
true_file = open(true_path, "r")
true = []
pred = []
labels = ["phone", "product"]
pred_lines = pred_file.read().split("\n")
true_lines = true_file.read().split("\n")
for line in pred_lines:
    if line!="":
        id = re.search("instance=\"(.*)\"\s", line).group(1)
        sense = re.search("senseid=\"(.*)\"",line).group(1)
        pred.append(sense)
        for line2 in true_lines:
            if line2!="" and id==re.search("instance=\"(.*)\"\s", line2).group(1):
                true.append(re.search("senseid=\"(.*)\"",line2).group(1))
                break
pred_file.close()
true_file.close()

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

