author = 'DHDixon'
email = 'ddixon49@gsu.edu'
"""
9/12/2021

"""
import re

tab = "\t"
sep = "\n"

blanks = ('' or ' ' or sep or tab)
parentheses = ('(' or ')')

file = r""
folder_out = r'' + '\\'

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
        # LINE BELOW SHOULD BE if line not in blanks:
        if line != blanks:
            # print(line)
            words = line.split(' ')
            word_count += len(words)

    if word_count > 0:
        quest_count += 1
        file_out = open(folder_out + quest_name + '_' + str(quest_count) + '.txt', 'w+', encoding='utf-8')
        word_counts_list.append(word_count)
        word_count = sep + '<WORD COUNT: ' + str(word_count) + '>' + sep

        file_out.write('<QUEST = ' + quest_name + '>' + sep)
        file_out.write(str(word_count) + sep)

        for line in all_quest_dict[quest]:
            file_out.write(
                line + sep + sep)

print(sum(word_counts_list))

