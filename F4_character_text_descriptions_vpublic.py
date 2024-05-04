author = 'DHDixon'
email = 'ddixon49@gsu.edu'

# 2/27/2021
# Fallout 4 character text raw file generator
# copy SK make_raw_file def

import re
import os

tab = "\t"
sep = "\n"

descriptions_file = r""
names_file = r""

form_id_dict = {}
# READ IN
line_count = 0
with open(names_file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('"', '', text)
    # print(text)
    lines = text.split(sep)
    for line in lines:
        line_count += 1
        cells = line.split(tab)

        form_id = cells[0]
        id_name = cells[1]
        # get rid of empty space
        id_name = id_name.strip()

        category = cells[2]
        real_name = cells[4]

        if id_name != '':
            if form_id not in form_id_dict:
                form_id_dict[form_id] = line
                print(line)
            else:
                print(id_name + ' ALREADY EXISTS???')
                print(line_count)
print(len(form_id_dict))

match_list = []
no_match_list = []

line_count = 0

# DESCRIPTION FILE
with open(descriptions_file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    lines = text.split(sep)
    for line in lines:
        line_count += 1

        cells = line.split(tab)

        form_id = cells[0]
        # id_name = cells[1]
        description = cells[3].strip()
        if description == '':
            description = '<NO DESCRIPTION>'
            # print(description)
        if form_id in form_id_dict:
            entry = form_id_dict[form_id] + tab + description
            print(entry)
            match_list.append(entry)

        else:
            entry = line
            no_match_list.append(entry)

file_out_character = open(r'', 'w+')
file_out_immersion = open(r'', 'w+')

for line in no_match_list:
    # print(line)
    file_out_immersion.write(line + sep)

for line in match_list:
    # print(line)
    file_out_character.write(line + sep)

