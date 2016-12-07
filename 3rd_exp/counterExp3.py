import numpy as np
import requests
import difflib as diff

def unique_words():
    input_file = open('good-candidates.txt', 'r')
    file_contents = input_file.read()
    input_file.close()
    word_list = file_contents.split()
    output = []
    unique_words = set(word_list)
    for word in unique_words:
        output+=[str(word)]
    return output

def calc_line_query_string(line):
    line_clean = [str(s) for s in line.split()]
    count = [0]*26
    for i, word in enumerate(line_clean):
        for j, letter in enumerate(word):
            index = alphabet.index(letter)
            count[index] += 1
    string_num = ""
    for number in count:
        if number > 9:
            string_num += get_hex(number)
        else:
            string_num += str(number)
    return string_num

def get_hex(num):
    alphabet_caps = alphabet.upper()
    return alphabet_caps[num - 10]

def check_line_rules(line):
    line_clean = [str(s) for s in line.split()]
    for req in required_words:
        if req not in line_clean:
            return False
#    for word in line_clean:
#        if word in known_bad_words:
#            return False
    return True

def trim_candidates():
    fin = open('good-candidates.txt', 'r')
    fout = open('better-candidates.txt', 'w')
    for line in fin:
        if check_line_rules(line):
            print(line, end='', file=fout)
    fin.close()
    fout.close()


def generate_codes():
    fin = open('better-candidates.txt', 'r')
    fout = open('new-codes.txt', 'w')
    for line in fin:
        qstring = calc_line_query_string(line)
        if len(qstring) < 27:
            print(qstring, end='\n', file=fout)
    fin.close()
    fout.close()

def cmp_codes(c1, c2):
    s = diff.SequenceMatcher(a=c1, b=c2)
    return s.ratio()

def get_top_codes():
    fin = open('new-codes.txt', 'r')
    code_list = []
    for line in fin:
        code_list += [line.replace('\n', '')]
    fin.close()
    top_codes = []
    fout = open('newer-codes.txt', 'w')
    for code in code_list:
        if cmp_codes(code, correct_query_string) >= .7:
            top_codes +=[code]
            print(code, end='\n', file=fout)
    fout.close()
    fin2 = open('better-candidates.txt','r')
    fout2 = open('top-candidates.txt', 'w')
    for line in fin2:
        if calc_line_query_string(line) in top_codes:
            print(line, end='', file=fout2)
    fin2.close()
    fout2.close()
    return top_codes

def remove_wrong_letter_words():
    # new_words = all_words[:]
    bad_letters = []
    bad_words = []
    for i, freq in enumerate(correct_query_string):
        if freq == str(0):
            bad_letters  += [alphabet[i]]
    for j, word in enumerate(all_words):
        for letter in bad_letters:
            if letter in word:
                bad_words += [word]
    return bad_words

def lcd_query(num_string):
    url = 'https://firstthreeodds.org/run/app?lcdq+'
    query_string = url + num_string
    r = requests.post(query_string)
    return int(r.text)

#def trim_more_words():
#    collected_words = []
#    bad_words = []
#    fin = open('better-candidates.txt', 'r')
#    for i, line in enumerate(fin):
#        line_clean = [str(s) for s in line.split()]
#        for j, word in enumerate(line_clean):
#           if word not in collected_words:
#               collected_words += [word]
#
#    for k, w in enumerate(filtered_words):
#        if w not in collected_words:
#            bad_words += [w]
#    return bad_words

def trim_more_words():
    print('TRIM MORE!')
    collected_words = []
    bad_words = []
    good_words = []
    fin = open('top-candidates.txt', 'r')
    for i, line in enumerate(fin):
        line_clean = [str(s) for s in line.split()]
        for j, word in enumerate(line_clean):
           if word in filtered_words:
               collected_words += [word]
    fin.close()
    collected_words.sort()
    while len(filtered_words) != 20:

        counts = []
        vals = []
        for c, cw in enumerate(collected_words):
            tup = [cw, collected_words.count(cw)]
            if tup not in counts:
                counts += [tup]
                vals += [collected_words.count(cw)]
        print(counts)
        if len(vals) > 20:
            bad = vals.index(min(vals))
            good = vals.index(max(vals))
            good_words += [counts[good][0]]
            collected_words.remove(counts[good][0])
            bad_words += [counts[bad][0]]
            collected_words.remove(counts[bad][0])
#            for count in counts:
#                if count[1] == bad:
#                    bad_words += [count[0]]
#                    collected_words.remove(count[0])
#                if count[1] == good:
#                    good_words += [count[0]]
#                    collected_words.remove(count[0])
            update_bad_words(bad_words)
            update_good_words(good_words)
        else:
            break
#    for j, count in enumerate(counts):
#        if counts[j][1] > counts[j=1][1] and j != len(counts):
#            selected = j+1
#        if counts[selected][1] <= 2 and count[0] not in required_words:
#            bad_words += [count[0]]
 #   return bad_words

def update_bad_words(bad_words):
    if len(bad_words) > 1:
        for word in bad_words:
            if word not in known_bad_words and word not in required_words:
                known_bad_words.append(word)
        remove_words(known_bad_words[:])
        print(known_bad_words)

def update_good_words(good_words):
    if len(good_words) > 1:
        for word in good_words:
            if word not in required_words and word not in known_bad_words:
                required_words.append(word)

def remove_words(words_to_remove):
    for word in words_to_remove:
        if word not in required_words and word in filtered_words:
            filtered_words.remove(word)
    print(len(filtered_words))

def print_line(line):
    line.sort()
    return ' '.join(line)


alphabet = 'abcdefghijklmnopqrstuvwxyz'
correct_query_string = '8202721241112883084A200010'
required_words = ['look', 'any', 'just', 'numbers', 'be', 'digit', 'random',
                  'that']
known_bad_words = ['alone','half', 'long', 'third', 'inside', 'and','is',
                   'perhaps', 'it', 'short']
shems_guess = ['look', 'any', 'just', 'numbers', 'be', 'digit', 'random',
               'pattern', 'reason', 'on', 'ten', 'in', 'appear', 'the', 'a',
               'that', 'first', 'for', 'to', 'or']

marcs_guess = ['any','just','look','digit','numbers', 'be', 'random','the',
               'appear', 'pattern', 'that', 'first', 'reason', 'on', 'ten',
               'in', 'for', 'a', 'or', 'to']




all_words = unique_words()
print(len(unique_words()))
trim_candidates()
generate_codes()
top_codes = get_top_codes()

filtered_words = all_words[:]
bad_words = remove_wrong_letter_words()
print(bad_words)
update_bad_words(bad_words)
print(print_line(known_bad_words))
#remove_words(known_bad_words)
#print(print_line(filtered_words))


trim_more_words()
#    update_bad_words(bad_words)
#print(print_line(known_bad_words))
#remove_words(known_bad_words)
#print(print_line(filtered_words))

final_line = print_line(filtered_words)
print('SHEM: ', print_line(shems_guess))
print('MARC: ', print_line(marcs_guess))
print('TYLER:', final_line)
final_code = calc_line_query_string(final_line)
print(final_code)
print(len(all_words), len(filtered_words))

print(cmp_codes(final_code, correct_query_string))
