__author__ = 'DHDixon'  # https://sites.google.com/view/danielhdixon/home
"""
SKYRIM SPEECH PARSER
Revised 07/02/2023
Immersion vs. Interactive Speech operationalization: If Player has choice, the text is 'Interactive Speech' 
else: 'Immersion Speech'
ONE TEXT is all lines in a single *BRANCH* in a single quest IF NO BRANCH: all lines in a single *CATEGORY* in a single 
quest
All lines have a quest listed

"""

import re
import os

sep = '\n'
tab = '\t'

raw_file = r''  # Raw file from mod tool
out_folder = r''
text_count = 0


def make_json(file):
    quest_dict = {}
    with open(file, encoding='utf-8') as file_in:
        text = file_in.read()
        text = re.sub('""', '272727', text)
        text = re.sub('"', '', text)
        text = re.sub('272727', '"', text)
        lines = text.split(sep)
        for line in lines[1:]:
            cells = line.split(tab)
            quest = cells[6]
            response_text = cells[20].strip()  # added strip 7.2.23
            if response_text != '':
                if quest not in quest_dict:
                    quest_dict[quest] = [line]
                else:
                    if line not in quest_dict[quest]:  # AVOIDS DUPLICATES: Not sure if there are any exact duplicates
                        quest_dict[quest].append(line)
                    else:
                        print('DUPLICATE NOT ADDED')
                        print(quest)
                        print(line)
                        print('--------------------')
    return quest_dict


quest_dict = make_json(raw_file)

imm_text_count = 0
int_text_count = 0

imm_all_word_count = 0
int_all_word_count = 0

for quest in quest_dict:
    print(quest)
    branch_dict = {}  # a single text: if a branch is listed, the branch is the unit, else, the category becomes the unit

    for line in quest_dict[quest]:
        cells = line.split(tab)

        branch = cells[7]
        cat = cells[8]

        if branch == '(none)':
            branch = 'CAT_' + cat

        if branch not in branch_dict:
            branch_dict[branch] = [line]
        else:
            if line not in branch_dict[branch]:  # AVOID DUPLICATES
                branch_dict[branch].append(line)
            else:
                print('DUPLICATE NOT ADDED')
                print(branch)
                print(line)
                print('--------------------')

    for text in branch_dict:  # text is either all lines with unique [1) branch or 2)category in a unique quest
        # print(text)
        out_lines_list = []
        frame_cat = 'immersive_speech'  # by default make it immersion so that if a Player option is found,
        # it simply changes to 'interactive'
        word_count_list = []
        repeat_word_count_list = []
        repeat_word_count = 0
        repeat_lines_list = []
        prompt_list = []  # stores player options and if > 0 text = interactive
        line_dict = {}  # used to check if the spoken line is a duplicate by a different speaker

        for line in branch_dict[text]:
            cells = line.split(tab)

            script_notes = cells[23].strip()
            if 'DO NOT RECORD' in script_notes:  # None found
                print('XXXXXXXX')
                print(quest)

            prompt = cells[19].strip()
            response_text = cells[20].strip()  # Main line of dialogue
            response_text = re.sub(' +', ' ', response_text)
            voice_type = '<' + cells[5].strip() + '>'

            branch = cells[7]
            if branch == '(none)':
                branch = 'NONE'
            category = cells[8]
            if category == '':
                category = 'NONE'

            if response_text != '':
                if response_text not in line_dict:
                    line_dict[response_text] = [voice_type]
                    single_dialogue_line = [voice_type, response_text]  # The first speaker in the data is listed as
                    # speaker for duplicate lines
                    word_count_list.append(response_text)

                # PROMPT CATEGORY DECISION
                    if prompt != '':
                        if prompt not in prompt_list:
                            prompt_list.append(prompt)
                            frame_cat = 'interactive_speech'  # if the prompt is not blank on any line in the text,
                            # then it will be 'interactive'

                    single_dialogue_line = ' '.join(single_dialogue_line)
                    single_dialogue_meta = ''
                    if prompt != '':
                        single_dialogue_meta = single_dialogue_meta + '<PLAYER CHOICE: ' + prompt + '>\n'
                    if script_notes != '':
                        single_dialogue_meta = single_dialogue_meta + '<SCRIPT NOTES: ' + script_notes + '>\n'

                    out_line = single_dialogue_line + sep + single_dialogue_meta + sep

                    if out_line not in out_lines_list:
                        out_lines_list.append(out_line)
                else:
                    voice_type = re.sub('>', '', voice_type)
                    repeat_lines_list.append(voice_type + ' ---> ' + response_text + '>')
                    repeat_word_count_list.append(response_text)

        if len(out_lines_list) > 0:
            word_count = 0
            for line in word_count_list:
                line = line.strip()
                words = line.split()
                word_count += len(words)

            if len(repeat_word_count_list) > 0:
                repeat_word_count = 0
                for line in repeat_word_count_list:
                    line = line.strip()
                    words = line.split()
                    repeat_word_count += len(words)

            file_out_folder = out_folder + '/' + frame_cat  # Make folder in either immersive or interactive folder
            if not os.path.exists(file_out_folder):
                os.mkdir(file_out_folder)

            if frame_cat == 'interactive_speech':
                int_text_count += 1
                text_count = int_text_count
                txt_prefix = 'sky_sp_int_'

            else:
                imm_text_count += 1
                text_count = imm_text_count
                txt_prefix = 'sky_sp_imm_'

            txt_file = txt_prefix + str(text_count) + '_' + quest + '.txt'
            file_out = open(file_out_folder + '/' + txt_file, 'w+', encoding='utf-8')

            file_out.write('<TEXT NAME: ' + txt_file + '>' + sep)
            file_out.write('<REGISTER: ' + frame_cat + '>' + sep)
            file_out.write('<RELATED QUEST: ' + quest + '>' + sep)

            file_out.write('<BRANCH: ' + branch + '>' + sep)
            file_out.write('<DEVELOPER CATEGORY: ' + category + '>' + sep * 2)

            prompts = ' - '.join(prompt_list)
            if frame_cat == 'interactive_speech':
                file_out.write('<PLAYER CHOICES: ' + prompts + '>' + sep + sep)

            for line in out_lines_list:
                file_out.write(line.strip() + sep * 2)

            file_out.write('<WORD COUNT: ' + str(word_count) + '>' + sep * 2)

            if len(repeat_lines_list) > 0:
                file_out.write('<DUPLICATE LINES BY AN ALTERNATE SPEAKER>' + sep * 2)
                for line in repeat_lines_list:
                    file_out.write(line + sep * 2)
                file_out.write('<REPEATED LINES WORD COUNT: ' + str(repeat_word_count) + '>' + sep * 2)
                total_word_count = word_count + repeat_word_count
                file_out.write('<TOTAL WORD COUNT: ' + str(total_word_count) + '>')

        print(text_count)

