author = 'DHDixon'
email = 'ddixon49@gsu.edu'

"""
9/8/2021
Writes out corpus texts for STATUS EFFECTS
"""

import re

tab = "\t"
sep = "\n"
file = r""
folder = r""

with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('\\|', '', text)
    text = re.sub('"', '', text)

    lines = text.split(sep)

    stat_count = 0
    for line in lines[1:]:
        cells = line.split(tab)

        name = cells[0]
        display_name = cells[1]
        display_name = display_name.strip()
        description = cells[2]
        description = description.strip()

        if description != '':
            word_count = len(description.split()) + len(display_name.split())

            stat_count += 1
            text_file = open(folder + '\\' + str(stat_count) + '_' + name + '.txt', 'w+')
            text_file.write('<' + name + '>' + sep + sep)
            text_file.write(display_name + sep)
            text_file.write(description + sep + sep)
            text_file.write('<WORD COUNT: ' + str(word_count) + '>')

            print('<' + name + '>' + sep + sep)
            print(display_name + sep)
            print(description + sep + sep)
            print('<WORD COUNT: ' + str(word_count) + '>')



