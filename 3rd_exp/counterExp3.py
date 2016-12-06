import random
import requests
import difflib as diff

# shell_command_format_string = 'curl -s https://firstthreeodds.org/run/app?lcdq+
correct_query_string = '8202721241112883084A200010'
all_words = ["digit",
             "is",
             "be",
             "perhaps",
             "to",
             "just",
             "a",
             "product",
             "two",
             "any",
             "numbers",
             "or",
             "pattern",
             "pieces",
             "first",
             "and",
             "five",
             "reason",
             "appear",
             "on",
             "inside",
             "short",
             "long",
             "third",
             "look",
             "it",
             "ten",
             "half",
             "that",
             "for",
             "alone",
             "of",
             "in",
             "chunks",
             "random",
             "the"]

words_that_cant_start = ['or','and']
bad_words = []

def calc_line_query_string(line):
    line_clean = [str(s) for s in line.split()]
    # print(line_clean)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    count = [0]*26
    for i, word in enumerate(line_clean):
        for j, letter in enumerate(word):
            index = alphabet.index(letter)
            # print(count[index])
            count[index] += 1
    # print(count)
    string_num = ""
    for number in count:
        if number > 9:
            string_num += get_hex(number)
        else:
            string_num += str(number)
    # print(string_num)
    return string_num

def get_hex(num):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = alphabet.upper()
    return alphabet[num - 10]

def check_line_rules(line):
    line_clean = [str(s) for s in line.split()]

    if line_clean[0] in words_that_cant_start:
        return False
    for word in line_clean:
        if word in bad_words:
            # print(word)
            return False
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

    # text_file = f.read()
    for line in fin:
        qstring = calc_line_query_string(line)
        if len(qstring) < 27:
            print(qstring, end='\n', file=fout)
    fin.close()
    fout.close()

def narrow_results():
    f = open('newer-codes.txt', 'r')
    lines = []
    matches = diff.get_close_matches(correct_query_string, f)
    f.close()
    # for j, match in enumerate(matches):
    #     matches[j] = match.replace('\n','')
    # print (matches)
    f = open('newer-codes.txt', 'r')
    for i, line in enumerate(f):
        # print(line, matches)
        # if line is correct_query_string:
            # lines += [i]
        for m in matches:
            if line == m:
                lines += [i]
    f.close()
    fin = open('even-better-candidates.txt','r')
    fout = open('top-3-candidates.txt','w')
    for j, line in enumerate(fin):
        if j in lines:
            print(line, end='', file=fout)
    fin.close()
    fout.close()

def remove_words():
    new_words = all_words[:]
    bad_letters = []
    bad_words = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for i, freq in enumerate(correct_query_string):
        if freq == str(0):
            bad_letters  += [alphabet[i]]
    for j, word in enumerate(all_words):
        for letter in bad_letters:
            if letter in word:
                bad_words += [word]
                new_words.remove(word)
    # print(bad_words)
    return new_words, bad_words

def lcd_query(num_string):
    url = 'https://firstthreeodds.org/run/app?lcdq+'
    query_string = url + num_string
    r = requests.post(query_string)
    # print(r.text)
    return int(r.text)
    # return random.randint(0,1000)

def collect_distances():
    fread = open('new-codes.txt','r')
    distances = []
    for j, line in enumerate(fread):
        distances += [lcd_query(line)]
        # if j > len(fread)//4:
        #     break
    closest_indexes = []
    for i, dist in enumerate(distances):
        if dist < 20:
            closest_indexes += [i]
            # print(distances[i])
    print(closest_indexes)
    fread.close()
    fread2 = open('better-candidates.txt','r')
    # fwrite = open('newer-codes.txt', 'w')
    fwrite = open('even-better-candidates.txt', 'w')
    for l, line in enumerate(fread2):
        if l in closest_indexes:
            print(line, end='', file=fwrite)
    fread2.close()
    fwrite.close()




# filtered_words, bad_words = remove_words()
# trim_candidates()
# generate_codes()
# collect_distances()
# print(len(all_words), len(filtered_words))
closest_matches = narrow_results()
print(closest_matches, len(closest_matches))
