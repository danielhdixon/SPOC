__author__ = 'DHDixon'  # https://sites.google.com/view/danielhdixon/home

"""
FALLOUT 4 SPEECH PARSER
Original 07/07/2021 
Revised 07/02/2023
Immersion vs. Interactive Speech operationalization: If Player has choice, the text is 'Interactive Speech' 
else: 'Immersion Speech'
ONE TEXT is all lines in a single *scene* in a single quest IF NO SCENE: all lines in a single *CATEGORY* in a single 
quest
All lines have a quest listed
"""

import re
import json
import os

sep = '\n'
tab = '\t'

raw_file = r''  # all speech .txt
out_folder = r'/Users/house/Desktop/SPOC Temp/out'


# reads in raw speech file and converts it to json KEY: quest VALUE: all rows with that quest listed as QUEST
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

            quest = cells[10]
            response_text = cells[5].strip()  # added strip 7.2.23
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
    scene_dict = {}  # a single text: if a scene is listed, the scene is the unit, else, the category becomes the unit
    # cat_dict = {}

    for line in quest_dict[quest]:
        cells = line.split(tab)
        scene = cells[13]
        cat = cells[30]

        if scene == '':
            scene = 'CAT_' + cat

        if scene not in scene_dict:
            scene_dict[scene] = [line]
        else:
            if line not in scene_dict[scene]:  # AVOID DUPLICATES
                scene_dict[scene].append(line)
            else:
                print('DUPLICATE NOT ADDED')
                print(scene)
                print(line)
                print('--------------------')

    for text in scene_dict:  # text is either all lines with unique [1) scene or 2)category] in a unique quest
        out_lines_list = []
        print(text)
        frame_cat = 'immersive_speech'  # by default make it immersion so that if a Player option is found,
        # it simply changes to 'interactive'
        word_count_list = []
        repeat_word_count_list = []
        repeat_word_count = 0
        repeat_lines_list = []
        prompt_list = []  # stores player options and if > 0 text = interactive
        line_dict = {}  # used to check if the spoken line is a duplicate by a different speaker

        for line in scene_dict[text]:
            cells = line.split(tab)

            q_type = cells[31]  # Combat, Favor, PlayerDialogue, etc.
            script_notes = cells[0].strip()
            prompt = cells[1].strip()
            response_text = cells[5].strip()  # Main line of dialogue
            response_text = re.sub(' +', ' ', response_text)
            voice_type = '<' + cells[7].strip() + '>'

            scene = cells[13]
            if scene == '':
                scene = 'NONE'
            category = cells[30]
            if category == '':
                category = 'NONE'

            if response_text != '' and script_notes != 'DO NOT RECORD':
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
                txt_prefix = 'f4_sp_int_'

            else:
                imm_text_count += 1
                text_count = imm_text_count
                txt_prefix = 'f4_sp_imm_'

            txt_file = txt_prefix + str(text_count) + '_' + quest + '.txt'  # Since txts have unique numbers,
            # I'll just use the quest name here
            file_out = open(file_out_folder + '/' + txt_file, 'w+', encoding='utf-8')

            file_out.write('<TEXT NAME: ' + txt_file + '>' + sep)
            file_out.write('<REGISTER: ' + frame_cat + '>' + sep)
            file_out.write('<RELATED QUEST: ' + quest + '>' + sep)

            file_out.write('<SCENE: ' + scene + '>' + sep)
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
