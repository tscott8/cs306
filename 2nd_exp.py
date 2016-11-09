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
from copy import deepcopy as dc
from string import ascii_lowercase, ascii_uppercase, digits
###############################################################################
# Algorithms
###############################################################################

# N^2
def bubble_sort(arr):
    """
    """
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                """temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp"""
    return arr

def shell_sort(arr):
    """
    A form of insertion sort
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
def merge_sort(arr):
    """
    """
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
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr

def heap_sort(arr):
    """
    """
    # convert arr to heap
    length = len( arr ) - 1
    leastParent = length // 2
    for i in range ( leastParent, -1, -1 ):
        move_down( arr, i, length )

    # flatten heap into sorted array
    for i in range ( length, 0, -1 ):
        if arr[0] > arr[i]:
            arr[0], arr[i] = arr[i], arr[0]
            move_down( arr, 0, i - 1 )
    return arr

def move_down(arr, first, last):
    """
    Helper for heap_sort
    """
    largest = 2 * first + 1
    while largest <= last:
        # right child exists and is larger than left child
        if ( largest < last ) and ( arr[largest] < arr[largest + 1] ):
            largest += 1

        # right child is larger than parent
        if arr[largest] > arr[first]:
            arr[largest], arr[first] = arr[first], arr[largest]
                # move down to largest child
            first = largest;
            largest = 2 * first + 1
        else:
            return # force exit


###############################################################################
# Analysis
###############################################################################
def compare_times(analysis):
    """
    """
    times = []
    return times

def compare_space(analysis):
    """
    """
    spaces = []
    return spaces

def empirical_analysis(fun, arrs=[]):
    """
    """
    analysis = {}
    case_type = "_"
    local_arrs = dc(arrs)
    for i in range(len(arrs)):
        arr = local_arrs[i][0]
        temp = []+[arr[:]]
        t = timeit.Timer(functools.partial(fun, arr))
        temp += [arr] + [t.timeit(5)]
        analysis[local_arrs[i][1]] = {'unsorted_arr': temp[0], 'sorted_arr': temp[1], 'time': temp[2]}
    analysis['comparisons'] = compare_times(analysis)
    return analysis

def display_analysis(functions, arrs):
    """
    """
    for i in range(len(functions)):
        title = "Empirical Analysis of " + ("N^2" if i < len(functions)//2 else "N-Log-N") + " Algorithm : " + functions[i][1]
        divider = "-"*len(title)
        print(divider + "\n" + title + "\n"+divider)
        analysis = empirical_analysis(functions[i][0], arrs)
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
        print()

def generate_lists(data_type, size):
    lists = []
    if type(data_type) is int:
        lists = [(list(range(size)), "best_case"),
                 (random.sample(range(100), size), "avg_case"),
                 (list(reversed(range(size))),"worst_case")]
    if type(data_type) is float:
        lists = [([round(x / 1.0, 4) for x in range(size)], "best_case"),
                 ([round(x / float(random.randint(1,100)), 4) for x in range(size)], "avg_case"),
                 ([round(x / 1.0, 4) for x in reversed(range(size))],"worst_case")]
    if type(data_type) is str:
        chars = ascii_lowercase + ascii_uppercase + digits
        str_len = 5
        lists = [(["".join([chars[j+i] for i in range(str_len)]) for j in range(size)], "best_case"),
                 (["".join([random.choice(chars) for i in range(str_len)]) for j in range(size)], "avg_case"),
                 (["".join([chars[j+i] for i in range(str_len)]) for j in reversed(range(size))], "worst_case")]
    return lists

def main():
    functions = [(bubble_sort, "Bubble Sort"), (shell_sort, "Shell Sort"),
                 (merge_sort, "Merge Sort"), (heap_sort, "Heap Sort")]
    size = 25
    args = []
    args += [generate_lists(int(), 25)]
    args += [generate_lists(float(), 25)]
    args += [generate_lists(str(), 25)]
    for i in range(len(args)):
        display_analysis(functions, args[i])

if __name__ == "__main__":
    main()
