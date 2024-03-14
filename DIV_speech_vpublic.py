author = 'DHDixon'

"""
Original: 04/23/2022
Revised: 07/02/2023

Redo speech categories with newer operationalization that if a unit of speech has player choice, then that is 
interactive speech. If no options, then it is immersive speech. 

Also removed 'copy' files from raw data
"""

import re
import json
import os

sep = '\n'
tab = '\t'

raw_file = r''  # all speech .txt


out_folder = r'/'


# reads in raw speech file and converts it to json KEY: quest VALUE: all rows with that quest listed as QUEST
def make_json(file):
    quest_dict = {}
    with open(file, encoding='utf-8') as file_in:
        text = file_in.read()
        text = re.sub("'</i>", ' ', text)
        text = re.sub("<i>'", ' ', text)
        text = re.sub("</i>", ' ', text)
        text = re.sub("<i>", ' ', text)
        text = re.sub('<br>', ' ', text)
        text = re.sub('"', '', text)
        # text = re.sub('\\(', '<', text)
        # text = re.sub('\\)', '>', text)
        lines = text.split(sep)
        for line in lines[1:]:
            cells = line.split(tab)

            quest = cells[8]  # This is single line in the raw because some files have more than one filename in
            # original cell
            response_text = cells[3].strip()  # added strip 7.2.23
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
    out_lines_list = []
    frame_cat = 'immersive_speech'  # by default make it immersion so that if a Player option is found,
    # it simply changes to 'interactive'
    word_count_list = []
    repeat_word_count_list = []
    repeat_word_count = 0
    repeat_lines_list = []
    prompt_list = []  # stores player options and if > 0 text = interactive
    line_dict = {}  # used to check if the spoken line is a duplicate by a different speaker

    for line in quest_dict[quest]:
        quest = re.sub('\.lsj', '', quest)
        text = quest + '.txt'
        print(text)
        player_choice = ''
        cells = line.split(tab)

        hcontext = cells[0]
        reference = cells[3]  # dialogue string
        reference = re.sub(' +', ' ', reference)
        reference = reference.strip()
        speaker_type = cells[6]

        speaker = cells[7]

        speaker = re.sub(' +', ' ', speaker)

        if len(speaker.split('(')) > 1:
            speaker_notes = speaker.split('(')[1]
            speaker = speaker.split('(')[0].strip()
            speaker_notes = re.sub('\)', '', speaker_notes).strip()
            speaker_notes = re.sub(',', ', ', speaker_notes)
        else:
            speaker_notes = ''
        speaker = '<' + speaker + '>'
        # speaker = re.sub('"', '', speaker)

        category = cells[9]

        if '*' in reference:  # First indicator of interactive

            # DIALOGUE CHOICES
            reference = re.sub("\\*", '', reference)
            if speaker == '<GROUP_Players>':  # Second indicator of interactive
                frame_cat = 'interactive_speech'
                player_choice = reference
                reference = ''  # So the non-spoken player choice doesn't get added to spoken lines below

                if player_choice != '':
                    if player_choice not in prompt_list:
                        prompt_list.append(player_choice)


        if reference != '':
            if reference not in line_dict:
                line_dict[reference] = [speaker]  # I don't think this is being used
                single_dialogue_line = [speaker, reference]  # The first speaker in the data is listed as
                # speaker for duplicate lines
                word_count_list.append(reference)

                single_dialogue_line = ' '.join(single_dialogue_line)
                single_dialogue_meta = ''
                if speaker_notes != '':
                    single_dialogue_meta = '<SPEAKER NOTES: ' + speaker_notes + '>' + sep
                if speaker != '<' + speaker_type + '>':
                    single_dialogue_meta = single_dialogue_meta + '<SPEAKER TYPE: ' + speaker_type + '>'

                out_line = single_dialogue_line + sep + single_dialogue_meta + sep

                if out_line not in out_lines_list:
                    out_lines_list.append(out_line)
            else:
                speaker = re.sub('>', '', speaker)
                repeat_lines_list.append(speaker + ' ---> ' + reference + '>')
                repeat_word_count_list.append(reference)

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
            txt_prefix = 'div_sp_int_'

        else:
            imm_text_count += 1
            text_count = imm_text_count
            txt_prefix = 'div_sp_imm_'

        txt_file = txt_prefix + str(text_count) + '_' + text  # Since txts have unique numbers,
        # I'll just use the quest name here
        file_out = open(file_out_folder + '/' + txt_file, 'w+', encoding='utf-8')

        file_out.write('<TEXT NAME: ' + txt_file + '>' + sep)
        file_out.write('<REGISTER: ' + frame_cat + '>' + sep)
        file_out.write('<RELATED QUEST: ' + quest + '>' + sep)
        file_out.write('<DEVELOPER CATEGORY: ' + category + '>' + sep)
        file_out.write('<HCONTEXT: ' + hcontext + '>' + sep * 2)


        if frame_cat == 'interactive_speech':
            prompts = ' - '.join(prompt_list)
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


