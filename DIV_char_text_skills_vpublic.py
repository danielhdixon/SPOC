author = 'DHDixon'
email = 'ddixon49@gsu.edu'
"""
9/8/2021
Writes out corpus texts for SKILLS
"""

import re
import os
# from numpy import std

tab = "\t"
sep = "\n"

file = r""

folder = r""
skill_dict = {}

with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('\\|', '', text)
    text = re.sub('"', '', text)

    lines = text.split(sep)
    for line in lines[1:]:
        cells = line.split(tab)

        category = cells[0]
        # name = cells[1]
        # display_name = cells[2]
        description = cells[3]

        if description != '':
            if category not in skill_dict:
                skill_dict[category] = [line]
            else:
                skill_dict[category].append(line)

skill_count = 0
for category in skill_dict:
    print(category)
    cat_folder = folder + '\\' + category
    os.mkdir(cat_folder)
    for line in skill_dict[category]:
        cells = line.split(tab)
        # category = cells[0]
        name = cells[1]

        display_name = cells[2]
        display_name = display_name.strip()

        description = cells[3]
        description = description.strip()

        word_count = len(description.split()) + len(display_name.split())

        skill_count += 1
        text_file = open(cat_folder + '\\' + str(skill_count) + '_' + name + '.txt', 'w+')

        text_file.write('<' + category + '>' + sep)
        text_file.write('<' + name + '>' + sep + sep)
        text_file.write(display_name + sep)
        text_file.write(description + sep + sep)
        text_file.write('<WORD COUNT: ' + str(word_count) + '>')

        print('<' + category + '>' + sep)
        print('<' + name + '>' + sep + sep)
        print(display_name + sep)
        print(description + sep + sep)
        print('<WORD COUNT: ')



