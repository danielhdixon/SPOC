# 9/11/2021
import re
author = 'dhdixon'  # https://sites.google.com/view/danielhdixon/home

tab = "\t"
sep = "\n"

file = r""

q_id_list_file = r''

folder_out = r' ' + '\\'

# Dict below is made from q_id_list_file
q_id_title_dict = {}
qid_rows_dict = {}

# Use the 00_quest_id_title_list to create dictionary with id at key and title as value
with open(q_id_list_file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    lines = text.split(sep)
    for line in lines:
        cells = line.split(tab)
        qid = cells[0]
        title = cells[1]
        # QUEST ID IS KEY AND THE TITLE IS THE VALUE
        q_id_title_dict[qid] = title

# Create q_id_rows_dict with quest TITLE as key and a list of rows as the value
with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('"', '', text)
    lines = text.split(sep)
    for line in lines[1:]:
        cells = line.split(tab)

        obj_id = cells[0]
        # This title is too long so I take out a few _TITLE here
        if 'Sewers_Q_IsDead' in obj_id:
            obj_id = re.sub('Sewers_Q_IsDead', '', obj_id)
        # the p needs to be capital - Larian messed up
        if 'Garethparents' in obj_id:
            obj_id = re.sub('Garethparents', 'GarethParents', obj_id)

        print(obj_id)
        description = cells[1]
        priority = cells[2]
        markers = cells[3]

        quest_id = obj_id.split('_')[:-1]
        quest_id = '_'.join(quest_id)
        if 'ARX_CreepyCraftsman' in quest_id:
            quest_id = re.sub('ARX_CreepyCraftsman', 'ARX_CreepyCraftsman_REMOVED', quest_id)
        # print(quest_id)
        if quest_id in q_id_title_dict:
            print(quest_id + ' is' + ' ' + q_id_title_dict[quest_id])
        else:
            quest_id = quest_id.split('_')[:-1]
            quest_id = '_'.join(quest_id)
            if quest_id in q_id_title_dict:
                print(quest_id + ' is' + ' ' + q_id_title_dict[quest_id])
            else:
                quest_id = quest_id.split('_')[:-1]
                quest_id = '_'.join(quest_id)
                if quest_id in q_id_title_dict:
                    print(quest_id + ' is' + ' ' + q_id_title_dict[quest_id])
                else:
                    print("NOPE: " + quest_id)
        q_title = q_id_title_dict[quest_id]
        if q_title not in qid_rows_dict:
            qid_rows_dict[q_title] = [line]
        else:
            qid_rows_dict[q_title].append(line)

print('XXXXXXXXXXXXXXXXXXXXXX')

qid_count = 0
# write out .txt files
for qid in qid_rows_dict:
    qid_count += 1  # File name count
    word_count = 0
    title = qid
    file_out = open(folder_out + str(qid_count) + '_' + title + '.txt', 'w+')
    print('<' + title + '>')
    file_out.write('<' + title + '>' + sep + sep)
    # file_out.write('<TITLE: ' + qid + '>' + sep + q_id_title_dict[qid])

    out_lines = []
    for line in qid_rows_dict[qid]:
        cells = line.split(tab)

        priority = cells[2]
        # zfill formats as 2
        priority = str(priority).zfill(2)

        out_line = str(priority) + tab + line
        out_lines.append(out_line)

    # sort lines by priority number in raw files

    for line in sorted(out_lines):
        # print(line)
        cells = line.split(tab)
        objid = cells[1]
        description = cells[2]
        priority = cells[3]
        markers = cells[4]
        if markers == '':
            markers = 'NONE'

        word_count += len(description.split())
        out_line = description + ' ' + '<' + str(priority) + ' ' + 'OBJ_ID: ' + objid + ' ' + 'MARKERS: ' + \
                   markers + '>'
        print(out_line)
        file_out.write(out_line + sep + sep)

    file_out.write(sep + '<WORD COUNT: ' + str(word_count) + '>')


