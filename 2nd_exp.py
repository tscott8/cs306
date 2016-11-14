# -*- coding: utf-8 -*-
"""
Created on Mon Nov 7 12:06:15 2016

@author: Tyler Scott
@collaborator(s): Shem Sedrick
"""
import timeit
import random
import numpy as np
import functools
import math
from copy import deepcopy as dc
from string import ascii_lowercase, ascii_uppercase, digits
from Card import Deck
# from memory_profiler import profile
from tabulate import tabulate as tab

###############################################################################
# Algorithms
###############################################################################

# N^2
def bubble_sort(arr, cmp_count=0):
    """
    """
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        cmp_count += j
    return arr, cmp_count

# N^2
def insertion_sort(arr, cmp_count=0):
    for i in range(1,len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j-1]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j=j-1
        cmp_count += j
    return arr, cmp_count


# N-Log-N
def shell_sort(arr, cmp_count=0):
    """
    A form of insertion sort
    """
    sublist_count = len(arr)//2
    while sublist_count > 0:
        cmp_count += 1
        for start_pos in range(sublist_count):
            # cmp_count += sublist_count
            gap_insertion_sort(arr, start_pos, sublist_count)
            # print('CALLED GAP INSERT\n')
        # print("After increments of size", sublist_count, "The list is", arr)
        sublist_count = sublist_count//2
        cmp_count += start_pos
    return arr, cmp_count

def gap_insertion_sort(arr, start, gap):
    """
    Helper for shell_sort
    """
    for i in range(start+gap, len(arr), gap):
        current_value = arr[i]
        position = i

        while position >= gap and arr[position - gap] > current_value:
            arr[position] = arr[position - gap]
            position = position - gap
        arr[position] = current_value

# N-Log-N
def merge_sort(arr, cmp_count=0):
    """
    """
    cmp_count += 1
    if len(arr) > 1:
        mid = len(arr)//2
        left = arr[mid:]
        right = arr[:mid]

        merge_sort(left)
        merge_sort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            cmp_count += 2
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            cmp_count += 1
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            cmp_count += 1
            arr[k] = right[j]
            j += 1
            k += 1
    return arr, cmp_count

# N-Log-N
def heap_sort(arr, cmp_count=0):
    """
    """
    # convert arr to heap
    length = len( arr ) - 1
    leastParent = length // 2
    for i in range (leastParent, -1, -1 ):
        cmp_count = move_down(arr, i, length, cmp_count)

    # flatten heap into sorted array
    for i in range ( length, 0, -1 ):
        cmp_count += 1
        if arr[0] > arr[i]:
            arr[0], arr[i] = arr[i], arr[0]
            move_down( arr, 0, i - 1, cmp_count )
    return arr, cmp_count

def move_down(arr, first, last, cmp_count):
    """
    Helper for heap_sort
    """
    largest = 2 * first + 1
    while largest <= last:
        cmp_count += 2
        # right child exists and is larger than left child
        if ( largest < last ) and ( arr[largest] < arr[largest + 1] ):
            largest += 1

        # right child is larger than parent
        cmp_count += 1
        if arr[largest] > arr[first]:
            arr[largest], arr[first] = arr[first], arr[largest]
            # move down to largest child
            first = largest;
            largest = 2 * first + 1
        else:
            return cmp_count # force exit
    return cmp_count


###############################################################################
# Analysis
###############################################################################
def time(fun, arr):
    """
    """
    t = timeit.Timer(functools.partial(fun, arr))
    return t.timeit(5)

def space(analysis):
    """
    """
    spaces = []
    return spaces

def comparison(fun, arr):
    """
    :param analysis:
    :return:
    """
    cmp_count = fun(arr, cmp_count=0)
    return cmp_count[1]

def empirical_analysis(fun, arrs=[]):
    """
    """
    analysis = {}
    case_type = "_"
    local_arrs = dc(arrs)
    for i in range(len(arrs)):
        arr1 = local_arrs[i][0]
        arr2 = local_arrs[i][0]
        temp = [] + [arr1[:]]
        time_analysis = time(fun, arr1)
        temp += [arr1] + [time_analysis]
        compare_analysis = comparison(fun, arr2)
        temp += [compare_analysis]
        analysis[local_arrs[i][1]] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2], 'comparisons': temp[3]}
    return analysis

def display_analysis(functions, arrs):
    """
    """
    for i in range(len(functions)):
        title = "Empirical Analysis of " + ("N^2" if i < len(functions)//2 else "N-Log-N") + " Algorithm : " + functions[i][1]
        divider = "-"*len(title)
        print(divider + "\n" + title + "\n"+divider)
        analysis = empirical_analysis(functions[i][0], arrs)
        print(tab(
        [['Input', analysis['avg_case']['unsorted_arr'][:5] + ['...']],
         ['Output', analysis['avg_case']['sorted_arr'][:5] + ['...']]], tablefmt='orgtbl'))
        print()
        print(tab(
            [['Best',    str(round(analysis['best_case']['time']*1000,4)) +' ms'],
             ['Average', str(round(analysis['avg_case']['time']*1000,4))  +' ms'],
             ['Worst',   str(round(analysis['worst_case']['time']*1000,4))+' ms'],
             ['Compares',(analysis['best_case']['comparisons']+analysis['avg_case']['comparisons']+analysis['worst_case']['comparisons'])//3]
            ], headers=['Case', 'Metric'], tablefmt='orgtbl'))
        print()

def generate_lists(data_type, size):
    lists = []
    if type(data_type) is int:
        lists = [(list(range(size)), "best_case"),
                 (random.sample(range(size * 4), size), "avg_case"),
                 (list(reversed(range(size))), "worst_case")]
    if type(data_type) is float:
        lists = [([round(x / 1.0, 4) for x in range(size)], "best_case"),
                 ([round(x / float(random.randint(1,100)), 4) for x in range(size)], "avg_case"),
                 ([round(x / 1.0, 4) for x in reversed(range(size))],"worst_case")]
    if type(data_type) is str:
        chars = ascii_lowercase + ascii_uppercase + digits
        str_len = 5
        lists = [(["".join([chars[(j+i) % 62] for i in range(str_len)]) for j in range(size)], "best_case"),
                 (["".join([random.choice(chars) for i in range(str_len)]) for j in range(size)], "avg_case"),
                 (["".join([chars[(j+i) % 62] for i in range(str_len)]) for j in reversed(range(size))], "worst_case")]
    return lists

def generate_card_lists():
    lists = []
    deck1 = Deck()
    deck2 = Deck()
    deck3 = Deck()
    deck2.shuffle()
    deck3.reverse()
    lists = [(deck1.get_cards(), "best_case"), (deck2.get_cards(), "avg_case"), (deck3.get_cards(), "worst_case")]
    return lists

def main():
    functions = [(bubble_sort, "Bubble Sort"), (insertion_sort, "Insertion Sort"),
                 (shell_sort, "Shell Sort"), (merge_sort, "Merge Sort"), (heap_sort, "Heap Sort")]
    size = 1000
    args = []
    args += [generate_lists(int(), size)]
    # args += [generate_lists(float(), size)]
    # args += [generate_lists(str(), size)]
    # args += [generate_card_lists()]
    for i in range(len(args)):
        display_analysis(functions, args[i])

if __name__ == "__main__":
    main()
