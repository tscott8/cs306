# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:02:25 2016

@author: Tyler
"""
import random as rand
import math

def riffle_shuffle(code):
    n=1
    code = [code[i:i+n] for i in range(0, len(code), n)]
    cut = len(code)//2 # floor division in python 3, in 2 use /
    second_deck, deck = code[:cut], code[cut:]
    for index, item in enumerate(second_deck):
        insert_index = index*2 + 1
        deck.insert(insert_index, item)
    return (''.join(deck))


def rotate(strg,n):
    n = n % len(strg)
    return strg[n:] + strg[:n]

def paired_shuffle(code):
    if type(code) is not str:
        code = ''.join(code)
    code = [code[i:i+2] for i in range(0, len(code), 2)]
    rand.shuffle(code)
    return ''.join(code)

def rif_n(code, n):
    while n > 0:
        code = riffle_shuffle(code)
        n -= 1
    return code

def pair_n(code, n):
    while n > 0:
        #code=rotate(code,1)
        #code_saved = code[:n]
#        print(code_saved, len(code_saved))
        #code_remain = code[n:]
        #code = code_saved + paired_shuffle(code_remain,n)
        code = paired_shuffle(code)
        n -= 1
    return code

def fish_yates(code, energy):
  code = [code[i:i+1] for i in range(0, len(code), 1)]
  m = len(code)
  # While there remain elements to shuffle…
  while (m) :
    # Pick a remaining element…
    m-=1
#    i = math.floor(rand.random() * m)
    i = math.floor(energy * m)
    print(i)
    # And swap it with the current element.
    t = code[m]
    code[m] = code[i]
    code[i] = t

  return ''.join(code)


# def truffle_shuffle(code, completed=[]):
#     start_index = rand.randint(0, len(code))
#     letter = code[start_index]
#     if letter not in completed:
#         code = rotate(i)
#
#     # start at random index
#     # if letter not in completed list
#     #   shift until letter in position with highest score
#     #   add that letter to the list of completed letters
#     # recurse with the new string

def translate_energy(energy):
    energy = str(energy)
    energy = '0.' + energy
    energy = float(energy)
    return energy

def shuffle_n_elements(code, n):
    code = [code[i:i+1] for i in range(0, len(code), 1)]
    start_index = rand.randint(0, n)
    code_split = [''.join(code[:start_index:]), ''.join(code[start_index:])]
    print(code_split)
    code_split[1] = riffle_shuffle(code_split[1])
    print(code_split)
    code = code_split[0]+code_split[1]
    return code

def scaled_shuffle(code, energy):
    energy = translate_energy(energy)
    code = shuffle_n_elements(code, 19*energy)
    return code

string = 'abcdefghijklmnopqrst'
print(shuffle_n_elements(string, rand.randint(0, 19)))
#for i in range(100, 0, -1):
#    print(fish_yates(string, i))
#for i in range(10000):
#    shuf = rif_n(string, rand.randint(0,19))
#    print(shuf)
#print(riffle_shuffle('abcdefg'))
#print(paired_shuffle('abcdefg'))
