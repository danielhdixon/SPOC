author = 'DHDixon'
email = 'ddixon49@gsu.edu'

# 9/12/2021
# CHARACTER TEXT
import re
import os

tab = "\t"
sep = "\n"

file = r''
file_out_folder = r'' + '\\'
category_dict = {}
# Make character_text single .txts from character_text.txt
# some text contains <> so that needs to be changed to something else. Maybe '[ ]'  done
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

char_count = 0
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
        description = re.sub('<', '(', description)
        description = re.sub('>', ')', description)

        # item_file_name = re.sub(' ', '_', item)
        char_count += 1
        file_out = open(cat_folder + '\\' + str(char_count) + '_' + id_name + '.txt', 'w+', encoding='utf-8')
        #
        word_count += len(real_name.split())
        word_count += len(description.split())
        #
        word_count = '<WORD COUNT: ' + str(word_count) + '>'
        entry = '<' + category + '>' + sep + '<' + id_name + '>' + sep + '<' + form_id + '>' + sep + sep
        entry_2 = real_name + sep + description + sep + sep + word_count
        file_out.write(entry + entry_2)


# This creates the .txt that the above code reads in and makes sorted txts
def make_raw_txt():
    names_file = r""

    descriptions_file = r''

    # Read in descriptions. Make a dict. Compare keys in dict to items to get "real" name of item.
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

            if description != '':
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






