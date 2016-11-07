# -*- coding: utf-8 -*-
"""
Created on Mon Nov 7 12:06:15 2016

@author: Tyler Scott
@collaborator(s): Shem Sedrick
"""
import timeit
import random
import functools
import math

###############################################################################
# Algorithms
###############################################################################

# N-Squared
def bubble_sort(arr):
    """
    """
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr


def shell_sort(arr):
    """
    """
    sublist_count = len(arr)//2
    while sublist_count > 0:
        for start_pos in range(sublist_count):
            gap_insertion_sort(arr, start_pos, sublist_count)
        # print("After increments of size", sublist_count, "The list is", arr)
        sublist_count = sublist_count//2
    return arr

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
def n1(arr):
    return arr
def n2(arr):
    return arr

###############################################################################
# Analysis
###############################################################################
def empirical_analysis(fun, size):
    analysis = {}
    case_type = "_"
    arr = []
    for i in range(3):
        if i is 0:
            case_type = 'best'
            arr = list(range(size))
        if i is 1:
            case_type = 'avg'
            arr = random.sample(range(100), size)
        if i is 2:
            case_type = 'worst'
            arr = list(reversed(range(size)))

        temp = []+[arr[:]]
        t = timeit.Timer(functools.partial(fun, arr))
        temp += [arr] + [t.timeit(5)]
        analysis[case_type+'_case'] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2]}

    # arr = list(range(size))
    # temp = []+[arr[:]]
    # t = timeit.Timer(functools.partial(fun, arr))
    # temp += [arr] + [t.timeit(5)]
    # analysis['best_case'] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2]}
    #
    # arr = random.sample(range(100), size)
    # temp = []+[arr[:]]
    # t = timeit.Timer(functools.partial(fun, arr))
    # temp += [arr] + [t.timeit(5)]
    # analysis['avg_case'] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2]}
    #
    # arr = list(reversed(range(size)))
    # temp = []+[arr[:]]
    # t = timeit.Timer(functools.partial(fun, arr))
    # temp += [arr] + [t.timeit(5)]
    # analysis['worst_case'] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2]}
    return analysis

def main():
    functions = [(bubble_sort, "Bubble Sort"),
                 (shell_sort, "Shell Sort"),
                 (n1, "n1"),
                 (n2, "n2")]
    for i in range(len(functions)):
        title = "Empirical Analysis of " + ("N-Squared" if i < len(functions)//2 else "N-Log-N") + " Algorithm : " + functions[i][1]
        divider = "-"*len(title)
        print(divider + "\n" + title + "\n"+divider)
        analysis = empirical_analysis(functions[i][0], 10)
        print("Best Case:\n",
              "  "+str(round(analysis['best_case']['time']*1000,4))+" ms\n",
              "  "+str(analysis['best_case']['unsorted_arr'])+"\n",
              "  "+str(analysis['best_case']['sorted_arr']))
        print("Average Case:\n",
              "  "+str(round(analysis['avg_case']['time']*1000,4))+" ms\n",
              "  "+str(analysis['avg_case']['unsorted_arr'])+"\n",
              "  "+str(analysis['avg_case']['sorted_arr']))
        print("Worst Case:\n",
              "  "+str(round(analysis['worst_case']['time']*1000,4))+" ms\n",
              "  "+str(analysis['worst_case']['unsorted_arr'])+"\n",
              "  "+str(analysis['worst_case']['sorted_arr']))

if __name__ == "__main__":
    main()
