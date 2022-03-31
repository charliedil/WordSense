import re
import sys

train_path = sys.argv[1]
test_path = sys.argv[2]
log_path = sys.argv[3]

train_file = open(train_path, "r")
train_file_text = train_file.read()
train_file.close()

## Parse training file

train_lines = train_file_text.split("\n")
for line in train_lines:
