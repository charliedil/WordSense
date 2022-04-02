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


print(len(context_to_label["product"]))
print(len(context_to_label["phone"]))
