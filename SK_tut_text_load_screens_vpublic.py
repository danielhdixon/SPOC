author = 'DHDixon'
email = 'ddixon49@gsu.edu'

"""
9/12/2021
Load screens to texts in tutorial text
"""

import re

tab = "\t"
sep = "\n"

file = r""

folder = r"" + '\\'

load_dict = {}

load_count = 0
with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()

    text = re.sub('"', '', text)

    lines = text.split(sep)
    for line in lines:
        cells = line.split(tab)
        if len(cells) > 3:
            name = cells[1]
            description = cells[3]

            if description != '':
                if description != 'Standard':
                    # print(description)
                    load_count += 1
                    file_out = open(folder + '\\' + str(load_count) + '_' + name + '.txt', 'w+', encoding='utf-8')
                    file_out.write('<' + name + '>' + sep * 2)
                    file_out.write(description + sep * 2)
                    word_count = len(description.split(' '))
                    file_out.write("<WORD COUNT: " + str(word_count) + '>')

        else:
            print("XXXX" + line)



