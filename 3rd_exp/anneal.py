# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 15:48:20 2016

@author: Tyler
"""
from itertools import permutations as perm
import random as rand
import numpy as np
import requests

orig_code = "abcdefghijklmnopqrst"
#quads = list(map(''.join, zip(*[iter(orig_code)]*(len(orig_code)//5))))

unordered_words = "a any appear be digit first for in just look numbers on or pattern random reason ten that the to"
uw_list =unordered_words.split()
# uw_zipped = ' '.join(uw_list)

# class Sentence():
#     def __init__(self):
#         self.unordered_words = "a any appear be digit first for in just look numbers on or pattern random reason ten that the to"
#         self.verbs = 'appear be look numbers pattern'.split()
#         self.adjs = 'first in just random ten'.split()
#         self.adverbs = 'any in just on that to'
#         self.nouns = 'digit in look numbers or pattern reason ten'.split()
#         self.pronouns = 'any that'.split()
#         self.determiners = 'a any that the'.split()
#         self.conjunctions = 'for or that'.split()
#         self.prepositions = 'for in on to'.split()
#         self.subjects = self.build_subjects()
#         self.predicates = self.build_predicates()
#         self.clauses = self.build_clauses()
#         self.phrases = self.build_phrases()
#         self.modifiers = self.build_modifiers()

#     def build_subjects(self):
#         pass
#         # must be noun or noun_phrase
#     def build_predicates(self):
#         pass
#     def build_clauses(self):
#         pass
#     def build_subjects(self):
#         pass
#     def build_phrases(self):
#         pass
#     def build_modifiers(self):
#         pass
#     def check_grammar(self, sentence):
#         return True


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
    
# new_code = shuffle_code(orig_code)
# while check_grammar(new_code) is False:
#     new_code = shuffle_code(short_code)
# print(decode(new_code))
# gen_perms(new_code)
# translate_file('perms.txt')
#guess ='for any random ten numbers just to look in the first digit be pattern on that or appear a reason'

guess = 'any pattern just look on or in the first ten digit numbers that appear to be random for a reason'
new_code = encode(guess)
print(new_code)
print(query(new_code))
#new_code = encode(guess)
#new_code = 'bnpistgckrdqalojhefm'
#new_code = 'bnipstgckrdqalojhefm'
#new_code = 'bnipsgtckrdqalojhefm'
#new_code = 'bnipsgctkrdqalojhefm'
#new_code = 'bnipsgcktrdqalojhefm'
#new_code = 'bnipsgckrtdqalojhefm'
#new_code = 'bnipsgtrkcdqalojhefm'
#new_code = 'bnipsgtrkcadlqojhefm'
#new_code = 'bnipsgtrkcadlqoefjmh'
#new_code = 'bnipsgckrtdqalojhefm'
#new_code = 'bnipgkcrtsdqalojhefm'
#print(decode(new_code))
#quads = list(map(''.join, zip(*[iter(new_code)]*(len(new_code)//2))))
#r = test_quad(quads[1],1)
#print(r)
new_code = 'bnijlfhmsqekrctdogap'
print(query(new_code))
print(decode(new_code))
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

