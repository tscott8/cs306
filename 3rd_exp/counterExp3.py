def calc_line_query_string(line):
    line_clean = [str(s) for s in line.split()]
    # print(line_clean)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    count = [0]*26
    for i, word in enumerate(line_clean):
        for j, letter in enumerate(word):
            index = alphabet.index(letter)
            count[index] += 1
    # print(count)
    string_num = ""
    for number in count:
        string_num += str(number)
    # print(string_num)
    return string_num

fin = open('good-candidates.txt', 'r')
fout = open('new-codes.txt', 'w')
# text_file = f.read()
for line in fin:
    qstring = calc_line_query_string(line)
    if len(qstring) < 27:
        print(qstring, end='\n', file=fout)
# for line in text_file


correct_query_string = '8202721241112883084A200010'
