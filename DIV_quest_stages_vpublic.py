author = 'DHDixon'
email = 'ddixon49@gsu.edu'

""""
9/11/2021
Create dictionary of quests names as keys and all rows within quest as values (each row an element in a list)
"""

import re

tab = "\t"
sep = "\n"

file = r""

folder_out = r'' + '\\'

id_rows_dict = {}
q_id_title_dict = {}

with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('"', '', text)
    lines = text.split(sep)
    for line in lines[2:]:
        cells = line.split(tab)

        quest_id = cells[0]
        if quest_id != '':
            quest_key = quest_id
            if quest_key not in id_rows_dict:
                id_rows_dict[quest_key] = [line]
        elif quest_id == '':
            id_rows_dict[quest_key].append(line)
stage_count = 0
for qid in id_rows_dict:
    # print(qid)
    row_1 = id_rows_dict[qid][0]

    cells = row_1.split(tab)
    title = cells[1]
    title = re.sub(' ', '_', title)
    title = re.sub('\\?', '', title)
    category_id = cells[2]
    main_quest = cells[3]
    sorting_priority = cells[6]
    meta_data = '<' + title + '>' + sep + '<' + qid + '>' + sep + '<CATEGORY: ' + category_id + '>' + sep + \
                '<MAIN QUEST: ' + main_quest + '>' + sep + '<SORTING: ' + sorting_priority + '>' + sep

    # Create dictionary for use in objectives code: id as key and title as value
    if qid not in q_id_title_dict:
        q_id_title_dict[qid] = title
    else:
        print(qid + ' is already in dictionary with value ' + q_id_title_dict[qid])

    word_count = 0
    lines_out = []
    for row in id_rows_dict[qid]:
        row_cells = row.split(tab)
        status_id = row_cells[7]
        description = row_cells[9]
        description = re.sub('<[^>]*>', '', description)
        if description != '':
            lines_out.append('<' + status_id + '> ' + description)
            word_count += len(description.split())
    if word_count != 0:
        stage_count += 1
        file_out = open(folder_out + str(stage_count) + '_' + title + '.txt', 'w+')
        # print(meta_data)
        file_out.write(meta_data + sep)
        for line_out in lines_out:
            # print(line_out)
            file_out.write(line_out + sep + sep)
        # print(sep + '<WORD COUNT: ' + str(word_count) + '>' + sep)
        file_out.write(sep + '<WORD COUNT: ' + str(word_count) + '>' + sep)

quest_list_out = open(folder_out + '00_quest_id_title_list.txt', 'w+')
for qid in q_id_title_dict:
    quest_list_out.write(qid + tab + q_id_title_dict[qid] + sep)
