__author__ = 'DHDixon'  # https://sites.google.com/view/danielhdixon/home
"""
Original: 7/09/2021
Revised: 07/03/2023
Operationalization: If Player has choice, the text is 'Interactive Speech' else: 'Immersion Speech'
Parsed at the level of filename

"""


import re
# import json
import os

sep = '\n'
tab = '\t'

raw_file = r''

out_folder = r''

g_choice_count = 0
# scene_dict = {}
imm_text_count = 0
int_text_count = 0

with open(raw_file, encoding='utf-8') as file_in:
    text = file_in.read()

    text = re.sub(r'\([^)]* *\)', '', text)  # Remove everything between ()
    text = re.sub('== true\)', '', text)
    text = re.sub('== false\)', '', text)
    scenes = text.split('.w2scene:')
    scene_index = 0
    for scene in scenes[1:]:
        # word_count = 0
        word_count_lines = []
        word_count_repeat_lines = []
        out_lines = []
        repeat_lines = []
        player_choices = []  # add all Geralt choices to this list with just the text of the choice
        frame_cat = 'immersive_speech'
        scene_index += 1  # add one here because it starts at 0 and loop starts at 1, so this makes index match loop
        # print(scene_index)

        scene_header = scenes[scene_index - 1].split(sep)[-1]  # Takes the previous scenes final line (the header)
        # which is current scene's header due to split above

        scene_name = scene_header.split('/')[-1]

        lines = scene.split(sep)[:-1]  # Stop before the last line because this line is the next scene's header
        line_count = 0
        for line in lines:
            # print(line)
            line = re.sub(' +', ' ', line)
            line = line.strip()
            line = re.sub('^\d+ ', '', line)  # Remove digits at beginning of string
            line_count += 1  # index will be line_count - 1, or next line is equal to line_count
            if line != '':
                if '==>' not in line:  # I think this points to the next line in raw... check out later
                    if '<==' not in line:
#
                        if 'Geralt choice:' in line:
                            g_choice_count += 1
                            frame_cat = 'interactive_speech'
                            p_choice = line.split('choice: ')[-1]
                            p_choice = re.sub('\\[', '', p_choice)
                            p_choice = re.sub(']', '', p_choice)
                            p_choice = p_choice.strip()
                            player_choices.append(p_choice)
                            line = '<' + line + '>'
                        else:
                            if ':' in line:
                                speaker = line.split(':')[0]
                                dialogue_line = line.split(':')[1].strip()
                                word_count_lines.append(dialogue_line)
                                speaker = '<' + speaker + '>'.strip()
                                line = speaker + ' ' + dialogue_line
                            else:
                                print('NO COLON')
                                print(scene_name)
                                print(line)

                        if dialogue_line not in out_lines:
                            out_lines.append(line)
                        else:
                            print('DUPLICATE!')
                            print(line)
                            word_count_repeat_lines.append(dialogue_line)
                            speaker = re.sub('>', ' ---> ', speaker)
                            dialogue_line = dialogue_line + '>'
                            line = speaker + dialogue_line
                            repeat_lines.append(line)

        file_out_folder = out_folder + '/' + frame_cat  # Make folder in either immersive or interactive folder
        if not os.path.exists(file_out_folder):
            os.mkdir(file_out_folder)
        if len(out_lines) > 0:
            if frame_cat == 'immersive_speech':
                imm_text_count += 1
                text_count = imm_text_count
                text_prefix = 'w3_sp_imm_' + str(text_count) + '_'
            else:
                int_text_count += 1
                text_count = int_text_count
                text_prefix = 'w3_sp_int_' + str(text_count) + '_'

            text_name = text_prefix + scene_name + '.txt'
            word_count = 0
            for line in word_count_lines:
                line = line.strip()
                words = line.split()
                word_count += len(words)

            file_out = open(file_out_folder + '/' + text_name, 'w+', encoding='utf-8')
            file_out.write('<TEXT NAME: ' + text_name + '>' + sep)
            file_out.write('<REGISTER: ' + frame_cat + '>' + sep)
            file_out.write('SCENE: ' + scene_header + '>' + sep * 2)

            if len(player_choices) > 0:
                player_choices = ' - '.join(player_choices)
                file_out.write('<PLAYER CHOICES: ' + player_choices + '>' + sep * 2)

            written_out_lines = []  # Used to reverse line order of geralt choices
            for i, line in enumerate(out_lines):
                if line not in written_out_lines:
                    if 'Geralt choice:' in line:
                        if len(out_lines) > i + 2:
                            if 'Geralt choice:' not in out_lines[i + 1]:
                                file_out.write(out_lines[i + 1] + sep + out_lines[i] + sep * 2)
                                written_out_lines.append(out_lines[i + 1])
                                written_out_lines.append(out_lines[i])
                            else:
                                file_out.write(out_lines[i] + sep + '<NO ASSOCIATED AUDIO WITH CHOICE>' + sep * 2)
                                written_out_lines.append(out_lines[i])
                        else:
                            file_out.write(out_lines[i] + sep + '<NO ASSOCIATED AUDIO WITH CHOICE>' + sep * 2)
                            written_out_lines.append(out_lines[i])
                    else:
                        file_out.write(line + sep * 2)
            file_out.write(sep + '<WORD COUNT: ' + str(word_count))

            if len(repeat_lines) > 0:
                repeat_lines_word_count = 0
                file_out.write(sep + '<DUPLICATE LINES BY AN ALTERNATE SPEAKER>' + sep * 2)
                for line in word_count_repeat_lines:
                    line = line.strip()
                    words = line.split()
                    repeat_lines_word_count += len(words)
                for line in repeat_lines:
                    file_out.write(line + sep * 2)
                file_out.write('<REPEATED LINES WORD COUNT: ' + str(repeat_lines_word_count) + '>' + sep * 2)
                total_words = word_count + repeat_lines_word_count
                file_out.write('<TOTAL WORD COUNT: ' + str(total_words) + '>')


