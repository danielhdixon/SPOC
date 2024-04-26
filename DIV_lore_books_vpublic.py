author = 'DHDixon'
email = 'ddixon49@gsu.edu'

"""
Writes out corpus texts for LORE books in Divinity 2
"""

import re

tab = "\t"
sep = "\n"

file = r""

folder = r""

book_dict = {}


with open(file, encoding='utf-8', errors='ignore') as file_in:
    text = file_in.read()
    text = re.sub('\\|', '', text)
    text = re.sub('"', '', text)
    text = re.sub(r'\<[^>]*\>', ' ', text)
    text = re.sub('  ', ' ', text)

    lines = text.split(sep)
    book_count = 0
    for line in lines[1:]:
        cells = line.split(tab)
        book_name = cells[0]
        book_name = book_name.strip()
        book_description = cells[1]
        book_description = book_description.strip()
        word_count = len(book_description.split(' '))

        # Fix 6/25/2021 added encoding
        book_count += 1
        file_out = open(folder + '\\' + str(book_count) + '_' + book_name + '.txt', 'w+', encoding='utf-8')
        file_out.write('<' + book_name + '>' + sep + sep)
        file_out.write(book_description + sep + sep)
        file_out.write('<WORD COUNT: ' + str(word_count) + '>')

        print(sep * 2)
        print(book_name)
        print(book_description)
        print(word_count)




