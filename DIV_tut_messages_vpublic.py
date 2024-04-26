author = 'DHDixon'
email = 'ddixon49@gsu.edu'

"""
9/8/2021
Writes out corpus texts for TUTORIAL TEXT
"""

import re
import os

tab = "\t"
sep = "\n"

file = r""

folder = r""

tut_dict = {}

punctuation_markers = ['.', '!', '?']

with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('\\|', '', text)
    text = re.sub('"', '', text)

    text = re.sub(r'\<[^>]*\>', '', text)

    lines = text.split(sep)
    for line in lines:
        cells = line.split(tab)
        tut_name = cells[0]
        tut_description = cells[1]
        tut_description = tut_description.strip()

        tut_name_split = tut_name.split('_')
        if tut_name_split[-1] == 'Title':
            # tut_title = tut_description
            tut_name_split.remove(tut_name_split[-1])
            tut_name = '_'.join(tut_name_split)
        if tut_name not in tut_dict:
            tut_dict[tut_name] = [tut_description]
        else:
            tut_dict[tut_name].append(tut_description)

# Most messages have 2 rows for a single message: Title and Description
# Put the single entries in list

single_entry_list = []
tut_count = 0
for t in tut_dict:
    title = ''
    description = ''
    if len(tut_dict[t]) == 2:
        tut_count += 1
        file_out = open(folder + '\\with_title\\' + str(tut_count) + '_' + t + '.txt', 'w+')
        file_out.write('<' + t + '>' + sep + sep)
        # print('<' + t + '>' + sep + sep)
        # print(sep + sep + t)
        for line in tut_dict[t]:
            for p in punctuation_markers:
                if p in line:
                    description = line
                    # break is needed so it skips the else statement if one punctuation marker is found. Otherwise if
                    # one of the p markers is not found, it assigns description to title
                    break
                else:
                    title = line
        file_out.write(title + sep + description + sep + sep)
        word_count = len(title.split(' '))
        word_count = word_count + len(description.split(' '))
        file_out.write('<WORD COUNT: ' + str(word_count) + '>')

    elif len(tut_dict[t]) == 1:
        description = tut_dict[t][0]

        tut_count += 1
        file_out = open(folder + '\\without_title\\' + str(tut_count) + '_' + t + '.txt', 'w+')  # WRITE OUT
        file_out.write('<' + t + '>' + sep + sep)
        file_out.write(description + sep + sep)
        word_count = len(description.split(' '))
        file_out.write('<WORD COUNT: ' + str(word_count) + '>')
    else:
        print(t)






