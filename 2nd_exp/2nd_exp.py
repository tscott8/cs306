# -*- coding: utf-8 -*-
"""
Created on Mon Nov 7 12:06:15 2016

@author: Tyler Scott
@collaborator(s): Shem Sedrick
@usageNotes: Make sure to install the necessary libraries listed below for this to work properly in python 3
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
import codecs
from matplotlib import pyplot as plt

###############################################################################
# Algorithms
###############################################################################

# N^2
def bubble_sort(arr, cmp_count=0):
    """
    """
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            cmp_count += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, cmp_count

# N^2
def insertion_sort(arr, cmp_count=0):
    for i in range(1, len(arr)):
        current_value = arr[i]
        pos = i
        while (pos > 0) and (arr[pos-1] > current_value):
            arr[pos] = arr[pos-1]
            pos -= 1
        cmp_count += 1
        if pos != i:
            arr[pos] = current_value
    return arr, cmp_count

# N^2
def selection_sort(arr, cmp_count=0):
    for fill_slot in range(len(arr)-1,0,-1):
        position_of_max = 0
        for location in range(1,fill_slot+1):
            cmp_count += 1
            if arr[location] > arr[position_of_max]:
                position_of_max = location
        temp = arr[fill_slot]
        arr[fill_slot] = arr[position_of_max]
        arr[position_of_max] = temp
    return arr, cmp_count

# N-Log-N
def shell_sort(arr, cmp_count=0):
    """
    A form of insertion sort
    """
    sublist_count = len(arr)//2
    while sublist_count > 0:
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
    return t.timeit(1000)

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

def get_instance(analysis, time):
    if analysis['ordered']['time'] is time:
        return ' (ord)'
    if analysis['random']['time'] is time:
        return ' (rand)'
    if analysis['reversed']['time'] is time:
        return ' (rev)'
    return '?'

def display_analysis(functions, arr, text_file):
    """
    """
    rounder = 1000
    print(tab(
            [
                ['Data Type', str(type( arr[1][0][0]))],
                ['List Size', str(len(arr[1][0]))+' elements']
            ],headers=['Stat', 'Value'], tablefmt="orgtbl"), file=text_file)
    table = []
    sort_proof = []
    for i in range(len(functions)):
        analysis = empirical_analysis(functions[i][0], arr)
        time_collections = [] + [analysis['ordered']['time']] + [analysis['random']['time']] + [analysis['reversed']['time']]
        time_collections.sort()
        table += [[functions[i][1],
                   str(time_collections[0]*rounder)[:6] +' \N{GREEK SMALL LETTER MU}s' + get_instance(analysis, time_collections[0]),
                   str(time_collections[1]*rounder)[:6] +' \N{GREEK SMALL LETTER MU}s' + get_instance(analysis, time_collections[1]),
                   str(time_collections[2]*rounder)[:6] +' \N{GREEK SMALL LETTER MU}s' + get_instance(analysis, time_collections[2]),
                   str(analysis['ordered']['comparisons'])]]
        if i is 0:
            sort_proof += [['Input', analysis['random']['unsorted_arr'][:5] + ['...']],
                           ['Output', analysis['random']['sorted_arr'][:5] + ['...']]]
    if len(sort_proof) > 0:
        print(tab(sort_proof, tablefmt="orgtbl"), file=text_file)
    print('',file=text_file)
    print(tab(table, headers=['Algorithm', 'Best ', 'Average','Worst','Compares'],
                tablefmt='orgtbl'), file=text_file)
    return table

def build_graph_tables(tables, text_file):
    new_table = []
    bubble = ['Bubble']
    select = ['Selection']
    insert = ['Insertion']
    shell = ['Shell']
    merge = ['Merge']
    heap = ['Heap']
    for table in tables:
        bubble += [float(table[1][0][2][:6])]
        select += [float(table[1][1][2][:6])]
        insert += [float(table[1][2][2][:6])]
        shell += [float(table[1][3][2][:6])]
        merge += [float(table[1][4][2][:6])]
        heap += [float(table[1][5][2][:6])]
    new_table = [bubble]+[select]+[insert]+[shell]+[merge]+[heap]
    print(tab(new_table,tablefmt='orgtbl', numalign="right", headers=['Sort','Int','Float', 'String', 'Card']),file=text_file)
    return new_table

def display_graphs(graph_tables, sizes):
    bubble_graph = {'int':[],'float':[],'str':[],'card':[]}
    select_graph = {'int':[],'float':[],'str':[],'card':[]}
    insert_graph = {'int':[],'float':[],'str':[],'card':[]}
    shell_graph = {'int':[],'float':[],'str':[],'card':[]}
    merge_graph = {'int':[],'float':[],'str':[],'card':[]}
    heap_graph = {'int':[],'float':[],'str':[],'card':[]}
    headers = ['int','float','str','card']
    graph = [{},{},{},{},{},{}]
    print (graph)
    for table in graph_tables:
    #    temp = {'int':[],'float':[],'str':[],'card':[]}
    #    for i in range(6):
    #        temp['title'] = table[i][0]
    #        temp['int'] += [table[i][1]]
    #        temp['float'] += [table[i][2]]
    #        temp['str'] += [table[i][3]]
    #        temp['card'] += [table[i][4]]
    #        graph[i] = temp

        bubble_graph['title'] = table[0][0]
        bubble_graph['int'] += [table[0][1]]
        bubble_graph['float'] += [table[0][2]]
        bubble_graph['str'] += [table[0][3]]
        bubble_graph['card'] += [table[0][4]]

        select_graph['title'] = table[1][0]
        select_graph['int'] += [table[1][1]]
        select_graph['float'] += [table[1][2]]
        select_graph['str'] += [table[1][3]]
        select_graph['card'] += [table[1][4]]

        insert_graph['title'] = table[2][0]
        insert_graph['int'] += [table[2][1]]
        insert_graph['float'] += [table[2][2]]
        insert_graph['str'] += [table[2][3]]
        insert_graph['card'] += [table[2][4]]

        shell_graph['title'] = table[3][0]
        shell_graph['int'] += [table[3][1]]
        shell_graph['float'] += [table[3][2]]
        shell_graph['str'] += [table[3][3]]
        shell_graph['card'] += [table[3][4]]

        merge_graph['title'] = table[4][0]
        merge_graph['int'] += [table[4][1]]
        merge_graph['float'] += [table[4][2]]
        merge_graph['str'] += [table[4][3]]
        merge_graph['card'] += [table[4][4]]

        heap_graph['title'] = table[5][0]
        heap_graph['int'] += [table[5][1]]
        heap_graph['float'] += [table[5][2]]
        heap_graph['str'] += [table[5][3]]
        heap_graph['card'] += [table[5][4]]

    graph = [bubble_graph, select_graph, insert_graph, shell_graph, merge_graph, heap_graph]
    print(np.array(graph))
    for alg in graph:
        plt.plot(alg['int'], lw=2.0)
        plt.plot(alg['float'], lw=2.0)
        plt.plot(alg['str'], lw=2.0)
        # plt.plot(alg['card'], lw=2.0)
        plt.title(alg['title'])
        plt.ylabel('time (us)')
        plt.xlabel('size')
        plt.legend(headers, loc='upper left')
        plt.autoscale()
        plt.show()


def generate_lists(data_type, size):
    lists = []
    if type(data_type) is int:
        lists = [(list(range(size)), "ordered"),
                 (random.sample(range(size * 4), size), "random"),
                 (list(reversed(range(size))), "reversed")]
    if type(data_type) is float:
        lists = [([round(x / 1.0, 4) for x in range(size)], "ordered"),
                 ([round(x / float(random.randint(1,100)), 4) for x in range(size)], "random"),
                 ([round(x / 1.0, 4) for x in reversed(range(size))],"reversed")]
    if type(data_type) is str:
        chars = ascii_lowercase + ascii_uppercase + digits
        str_len = 5
        lists = [(["".join([chars[(j+i) % 62] for i in range(str_len)]) for j in range(size)], "ordered"),
                 (["".join([random.choice(chars) for i in range(str_len)]) for j in range(size)], "random"),
                 (["".join([chars[(j+i) % 62] for i in range(str_len)]) for j in reversed(range(size))], "reversed")]
    return lists

def generate_card_lists():
    lists = []
    deck1 = Deck()
    deck2 = Deck()
    deck3 = Deck()
    deck2.shuffle()
    deck3.reverse()
    lists = [(deck1.get_cards(), "ordered"), (deck2.get_cards(), "random"), (deck3.get_cards(), "reversed")]
    return lists

def run(size, text_file):
    functions = [(bubble_sort, "Bubble Sort", "N^2"),
                 (selection_sort, "Selection Sort", "N^2"),
                 (insertion_sort, "Insertion Sort", "N^2"),
                 (shell_sort, "Shell Sort", "N-Log-N"),
                 (merge_sort, "Merge Sort", "N-Log-N"),
                 (heap_sort, "Heap Sort", "N-Log-N")]
    print('N^2=', pow(size,2), '\nN-Log-N', size*math.log(size))
    arrs = []
    arrs += [generate_lists(int(), size)]
    arrs += [generate_lists(float(), size)]
    arrs += [generate_lists(str(), size)]
    arrs += [generate_card_lists()]
    collected_tables = []
    for i in range(len(arrs)):
        collected_tables+=[(str(type(arrs[i][1][0][0])), display_analysis(functions, arrs[i], text_file))]
        print('\\\\',file=text_file)
    graph_table = build_graph_tables(collected_tables, text_file)
    return graph_table

def main():
    graph_tables = []
    sizes = []
    for i in range(1,11):
        s = 10*i
        with codecs.open("results"+str(i)+".org", "w", "utf-8") as text_file:
            graph_tables += [run(s, text_file)]
            sizes += [s]
    display_graphs(graph_tables, sizes)
    # functions = [(bubble_sort, "Bubble Sort", "N^2"),
    #              (selection_sort, "Selection Sort", "N^2"),
    #              (insertion_sort, "Insertion Sort", "N^2"),
    #              (shell_sort, "Shell Sort", "N-Log-N"),
    #              (merge_sort, "Merge Sort", "N-Log-N"),
    #              (heap_sort, "Heap Sort", "N-Log-N")]
    # size = 52
    # print('N^2=', pow(size,2), '\nN-Log-N', size*math.log(size))
    # arrs = []
    # arrs += [generate_lists(int(), size)]
    # arrs += [generate_lists(float(), size)]
    # arrs += [generate_lists(str(), size)]
    # arrs += [generate_card_lists()]
    # tables = []
    # with codecs.open("results.org", "w", "utf-8") as text_file:
    #     for i in range(len(arrs)):
    #         tables+=[(str(type(arrs[i][1][0][0])), display_analysis(functions, arrs[i], text_file))]
    #         # print(('-'*150)+'\n',file=text_file)
    #         print('\\\\',file=text_file)
    #
    #     collections
    #     print(build_graph_tables(tables), file=text_file)

if __name__ == "__main__":
    main()
