author = 'DHDixon'
email = 'ddixon49@gsu.edu'

# Fallout 4 Quest Stages CSV TO TEXTS .TXTs
# 9/12 /2021

import re

tab = "\t"
sep = "\n"
blanks = ('' or ' ' or sep or tab)
parentheses = ('(' or ')')

file = r""
folder_out = r"" + '\\'
all_quest_dict = {}
word_counts_list = []
all_speaker_list = []


with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    # get rid of quotation marks
    text = re.sub('"', '', text)
    text = re.sub('\\[QUOTE]', '', text)
    lines = text.split(sep)

    for line in lines:
        if line != lines[-1]:

            cells = line.split(tab)
            if len(cells) > 3:
                # cells = cells[0:4]
                quest = cells[1]
                quest_line = cells[3]

                if quest_line != '':
                    # print('---> not blank ---->' + quest_line)
                    if quest not in all_quest_dict:
                        all_quest_dict[quest] = []
                    all_quest_dict[quest].append(quest_line)
quest_count = 0
for quest in all_quest_dict:
    print('NEW QUEST')
    print(quest + sep + sep + 'xxxx')
    for q in all_quest_dict[quest]:
        print(q)

    quest_name = str(quest)
    word_count = 0
    all_words = []
    for line in all_quest_dict[quest]:
        line = line.strip()  # added 9/12/2021
        if line != blanks:
            # print(line)
            words = line.split(' ')
            word_count += len(words)

    if word_count > 0:

        quest_count += 1
        file_out = open(folder_out + quest_name + '_' + str(quest_count) + '.txt', 'w+')
        word_counts_list.append(word_count)
        word_count = sep + '<WORD COUNT: ' + str(word_count) + '>'

        file_out.write('<QUEST = ' + quest_name + '>' + sep)

        for line in all_quest_dict[quest]:
            file_out.write(line + sep + sep)

        file_out.write(str(word_count))

print(sum(word_counts_list))

