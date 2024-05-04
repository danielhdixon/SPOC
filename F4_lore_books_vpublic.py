author = 'DHDixon'
email = 'ddixon49@gsu.edu'
'''
# 9/11/2021

# Fallout 4 Books texts to modified texts with word count
'''

import re
import glob

tab = "\t"
sep = "\n"
# Not sure this works after all
blanks = ('', ' ', sep, tab)
parentheses = ('(' or ')')

unique_lines = []
word_counts_list = []

path = r'' + '\\'

folder_out = r'' + '\\'

all_book_dict = {}

# READ IN
for file in glob.glob(path + '*.txt'):
    with open(file, encoding='utf-8', errors='ignore') as file_in:
        book_name = file.split('\\')[-1]

        # Separate to lines
        text = file_in.read()
        lines = text.split(sep)
        for line in lines:
            if line not in blanks:
                # Change square brackets to angled
                line = re.sub('\\[', '<', line)
                line = re.sub(']', '>', line)
                unique_lines.append(line)

        if book_name not in all_book_dict:
            all_book_dict[book_name] = []
        for line in unique_lines:
            all_book_dict[book_name].append(line)
        unique_lines = []
book_count = 0
for book in all_book_dict:
    print(book)
    word_count = 0
    for line in all_book_dict[book]:
        line = re.sub('<[^>]*>', '', line)
        if line not in blanks:
            words = line.split(' ')
            word_count += len(words)

    if word_count > 0:
        word_counts_list.append(word_count)

        # WRITE OUT
        book_count += 1
        file_out = open(folder_out + str(book_count) + '_' + book, 'w+')

        file_out.write('<' + book + '>' + sep)
        file_out.write('<WORD COUNT: ' + str(word_count) + '>' + sep + sep)
        for line in all_book_dict[book]:
            # line = re.sub('<[^>]*>', '', line)
            if line not in blanks:
                print(line)
                file_out.write(line + sep)






