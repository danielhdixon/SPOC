author = 'DHDixon'
email = 'ddixon49@gsu.edu'

# 9/11/2021

import re
import os

tab = "\t"
sep = "\n"

file = r'D:\Dropbox\0_python_working_directory\dissertation_python_wd\O_GAME_CORPUS\F4\raw\written_raw' \
       r'\character_text_raw\F4_character_text.txt'
file_out_folder = r'D:\Dropbox\0_python_working_directory\dissertation_python_wd\O_GAME_CORPUS\F4\sorted' \
                  r'\written_sorted\character_text_v2'

category_dict = {}
# Make character_text single .txts from character_text.txt
# some text contains <> so that needs to be changed to something else. Maybe '[ ]'
with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    line_count = 0
    lines = text.split(sep)
    for line in lines:
        line_count += 1
        print(line_count)
        word_count = 0
        cells = line.split(tab)
        category = cells[2]

        if category not in category_dict:
            category_dict[category] = [line]
        else:
            category_dict[category].append(line)
cat_count = 0
for category in category_dict:
    cat_folder = file_out_folder + '\\' + category
    print(category)
    os.mkdir(cat_folder)
    for line in category_dict[category]:
        word_count = 0
        cells = line.split(tab)

        form_id = cells[0]
        id_name = cells[1]
        category = cells[2]
        real_name = cells[4]
        description = cells[5]
        if description != '<NO DESCRIPTION>':
            description = re.sub('<', '(', description)
            description = re.sub('>', ')', description)

        # item_file_name = re.sub(' ', '_', item)

        cat_count += 1
        file_out = open(cat_folder + '\\' + str(cat_count) + '_' + id_name + '.txt', 'w+')
        #
        word_count += len(real_name.split())
        if description != '<NO DESCRIPTION>':
            word_count += len(description.split())
        #
        word_count = '<WORD COUNT: ' + str(word_count) + '>'
        entry = '<' + category + '>' + sep + '<' + id_name + '>' + sep + '<' + form_id + '>' + sep + sep
        entry_2 = real_name + sep + description + sep + sep + word_count
        file_out.write(entry + entry_2)





