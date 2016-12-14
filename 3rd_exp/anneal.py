# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:48:20 2016

@author: Tyler
"""
from itertools import permutations as perm
import random as rand
import numpy as np
import requests
import difflib as diff
correct_code = 'bnhmpgsqekrlafjictdo'
orig_code = "abcdefghijklmnopqrst"
unordered_words = "a any appear be digit first for in just look numbers on or pattern random reason ten that the to"
uw_list =unordered_words.split()
def check_grammar(code):
    # if decode(code)[0] in wcs_list:
    #     return False
    return True

def shuffle_code(code):
    code_list = list(code)
    rand.shuffle(code_list)
    code = ''.join(code_list)
    return code

def gen_perms(code):
    fout = open('perms.txt', 'w')
    perms = perm(code)
    for i, p in enumerate(perms):
        if i > 10000:
            break
        print(''.join(p), end='\n', file=fout)
    fout.close()

def decode(code):
    phrase = []
    for letter in code:
        phrase += [uw_list[orig_code.index(letter)]]
    return ' '.join(phrase)

def encode(phrase):
    words = phrase.split()
    code = []
    for word in words:
        code += [orig_code[uw_list.index(word)]]
    return ''.join(code)

def translate_file(filename):
    fin = open(filename, 'r')
    for line in fin:
        print(decode(line.replace('\n','')))
    fin.close()

def query(code):
    url = 'https://firstthreeodds.org/run/app?permdq+'
    query_string = url + code
    r = requests.post(query_string)
    return int(r.text)

def test_quad(quad, index):
    perms = perm(quad)
    remains = quads[:]
    testers = []
    for p in perms:
        remains[index] = ''
        remains[index] = ''.join(p)
        test = ''
        for q in remains:
            test += q
        testers += [test]
    collection = []
    fout = open('tests'+str(index)+'.txt','w')
    for t in testers:
        result = query(t)
        print(str(result) + '\t' + t, end='\n', file=fout)
        collection += [result]
    fout.close()
    return collection.index(min(collection))

def meat_chunks():
    chunks = ['any pattern in',
              'a first look',
              'ten digit numbers',
              'be random',
              'just appear to',
              'or reason for',
              'on', 'that', 'the']
    perms = perm(chunks)
    fout = open('meatchunks.txt', 'w')
    for p in perms:
        pcode = encode(' '.join(p))
        if pcode[0] == 'b' and pcode[len(pcode)-1] == 'o':
            print(pcode, end='\n', file=fout)
    fout.close()

def compute_meat():
    fin = open('meatchunks.txt', 'r')
    fout = open('chunkiness.txt','w')
    collection = []
    for i,line in enumerate(fin):
  #      print(line.replace('\n', ''))
        result = query(line.replace('\n', ''))
        print(str(result) + '\t' + line, end='\n', file=fout)
        collection += [result]
    fin.close()
    fout.close()
    r = collection.index(min(collection))
    fin2 = open('chunkiness.txt', 'r')
    fout2 = open('result2.txt', 'r')
    for j, line in enumerate(fin2):
        if r == j:
          print(line.replace('\n','')+'\t q'+str(j),end='\n',file=fout2)
    fin2.close()
    fout2.close()

def riffle(deck):
    '''
    Shuffle a list like a deck of cards.
    i.e. given a list, split with second set have the extra if len is odd
    and then interleave, second deck's first item after first deck's first item
    and so on. Thus:
    riffle([1,2,3,4,5,6,7])
    returns [1, 4, 2, 5, 3, 6, 7]
    '''
    cut = len(deck)//2 # floor division in python 3, in 2 use /
    deck, second_deck = deck[:cut], deck[cut:]
    for index, item in enumerate(second_deck):
        insert_index = index*2 + 1
        deck.insert(insert_index, item)
    return deck

def riffle_shuffle(code):
    n=1
    code = [code[i:i+n] for i in range(0, len(code), n)]
    cut = len(code)//2 # floor division in python 3, in 2 use /
    deck, second_deck = code[:cut], code[cut:]
    print(deck, second_deck)
    for index, item in enumerate(second_deck):
        insert_index = index*2 + 1
        deck.insert(insert_index, item)
    return deck

def paired_shuffle(code):
    n = 2
    if type(code) is not str:
        code = ''.join(code)
    code = [code[i:i+n] for i in range(0, len(code), n)]
    rand.shuffle(code)
    return (''.join(code))

print(riffle_shuffle('abcdefg'))
print(paired_shuffle('abcdefg'))

print(decode('bnhmpgsqekrlafjictdo'))
#compute perms
#for each perm compute heat, if heat goes up stop, return code
#repeat with new code
#meat_chunks()
#compute_meat()
#new_code = 'bnhqekrctjogapidlmfs'
#new_code = 'bnhmpgsqekrlafjictdo'
#print(query(new_code))
#print(decode(new_code))
#guess = 'any pattern just be on or in the first ten digit numbers that appear to look random for a reason'
#guess = 'any pattern just be for reason look random on or in the a first ten digit numbers that appear to'
#new_code = encode(guess)
#print(new_code)
#print(query(new_code))

#quads = list(map(''.join, zip(*[iter(new_code)]*(len(new_code)//2))))
#r = test_quad(quads[1],1)
#print(r)

#quads = list(map(''.join, zip(*[iter(new_code)]*(len(new_code)//4))))
##
#stuff = []
#fout = open('results1.txt', 'w')
#for i,q in enumerate(quads):
#    r = test_quad(q, i)
#    fin = open('tests'+str(i)+'.txt', 'r')
#    for j, line in enumerate(fin):
#        if r == j:
#            print(line.replace('\n','')+'\t q'+str(i),end='\n',file=fout)
#            stuff += [line.split() + [i]]
#    fin.close()
#fout.close()
#print(decode(stuff[0][1]))
#print(np.array(stuff))
