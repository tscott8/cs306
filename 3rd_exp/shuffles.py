# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:02:25 2016

@author: Tyler
"""
import random as rand


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
    return strg[n:] + strg[:n]
    
def paired_shuffle(code, n):
    if type(code) is not str:
        code = ''.join(code)
    code_saved = code[n:]
    code = code[:n]
    code=rotate(code,1)
    n = 2
    code = [code[i:i+n] for i in range(0, len(code), n)]
    rand.shuffle(code)
    return (code_saved+''.join(code))
    
def rif_n(code, n):
    while n > 0:
        code = riffle_shuffle(code)
        n -= 1
    return code

def pair_n(code, n):
    while n > 0:
        code = paired_shuffle(code,n)
        n -= 1
    return code

shuf = rif_n('abcdefghijklmnopqrst', rand.randint(1,10))
print(shuf)

shuf = pair_n('abcdefghijklmnopqrst', rand.randint(1,10))
print(shuf)
#print(riffle_shuffle('abcdefg'))
#print(paired_shuffle('abcdefg'))