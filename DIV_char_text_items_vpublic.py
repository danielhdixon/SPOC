author = 'DHDixon'
email = 'ddixon49@gsu.edu'

"""
9/8/2021
Writes out corpus texts for ITEMS in Divinity 2
"""

import re
import os

tab = "\t"
sep = "\n"

file = r""
folder = r""

item_dict = {}
punctuation_markers = ['.', '!', '?']

with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('\\|', '', text)
    text = re.sub('"', '', text)

    lines = text.split(sep)
    for line in lines[1:]:
        line = line.lstrip()
        cells = line.split(tab)
        reference = cells[0]

        item = cells[1]
        item = re.sub(' ', '_', item)

        if item not in item_dict:
            item_dict[item] = [reference]
        else:
            if reference not in item_dict[item]:
                item_dict[item].append(reference)
ref_count = 0
for item in item_dict:
    print(item)
    for ref in item_dict[item]:
        for p in punctuation_markers:
            if p in ref:
                item_dict[item].remove(ref)
                item_dict[item].append(ref)
                ref_count += 1
print(ref_count)
item_count = 0
for item in item_dict:
    item_count += 1
    word_count = 0
    file_out = open(folder + '\\' + str(item_count) + '_' + item + '.txt', 'w+')
    file_out.write('<' + item + '>' + sep + sep)
    for ref in item_dict[item]:
        file_out.write(ref + sep)

        word_count += len(ref.split())
    file_out.write(sep + '<WORD COUNT: ' + str(word_count) + '>')


