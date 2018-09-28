# coding: utf-8
"""
Created on Sep. 26th 2018
@author: AndyKANG98
"""

import itertools
import csv


def load_data():
    """
    Load data from 'freq_items_datasets.txt' file
    Returns:
        data: tuple of tuples
    """
    with open('./freq_items_datasets.txt') as f:
        data = f.read().split('\n')

    for i in range(len(data)):
        data[i] = tuple(data[i].split())
    return tuple(data)


def get_item_dict(data):
    """
    Count the number of i-itemset and generate a dictionaty
    Args:
        data: loaded raw data
    Returns:
        item_dict: dictionary with keys of distinct items and values of occurrences numbers
    """
    item_set = set(item for transaction in data for item in transaction)

    item_dict = {}
    for item in item_set:
        item_dict[item] = sum(transaction.count(item) for transaction in data)
    
    return item_dict


def generate_candidates(large_item_set):
    """
    Generate k+1 candidates for k-size large_item_set
    Args:
        large_item_set: a list of k-size lists stores all large_item_set with size k
    Returns:
        candidates: generate k+1-size candidates for those sets with same prefix
    """
    candidates = []
    for i in range(len(large_item_set)):
        for j in large_item_set[i+1:]:
            if (frozenset(large_item_set[i][0:-1]) == frozenset(j[0:-1])):
                candidates.append(list(set().union(large_item_set[i],j)))
    return candidates


def count_step(candidates, data, min_sup):
    """
    Count the number of occurencies for each candidate and select the next k+1-size itemset
    Args:
        candidates - list of lists candidates itemset(after prune step(for k>=3))
        data - the otiginal tuple data
        min_sup - minimum support to be selected
    Returns:
        large_itemset_dict - a dictionary with key of lists for selected large itemsets after counting step and the value of corresponding counting value
    """
    # Convert lists to sets in order to accelerate the "issubset" operation
    for i in range(len(candidates)):
        candidates[i] = frozenset(candidates[i])

    copy_data = list(data)
    for i in range(len(copy_data)):
        copy_data[i] = frozenset(copy_data[i])

    # counting step
    large_itemset_dict = {}
    for i in candidates:
        count = 0
        for j in copy_data:
            if (i.issubset(j)):
                count = count + 1
        if (count>= min_sup):
            large_itemset_dict[frozenset(i)] = count
        
    return large_itemset_dict


def prune_step(candidates, large_item_set):
    """
    Only for k>=3.
    Check if the (k-1)size subsets are all large itemsets as well. Only select the candidates with no small subsets
    Args:
        candidates - the candidates to be checked generated from generate_candidates() step
        large_item_set - the selected (k-1)size large item sets
    Returns:
        new_candidates - the new candidaets after prune step
    """
    large_item_set_copy = set(frozenset(item) for item in large_item_set)

    new_candidates = []
    for i in range(len(candidates)):
        subset = list(itertools.combinations(candidates[i], len(candidates[i])-1))
        for j in range(len(subset)):
            subset[j] = frozenset(subset[j])
        if (set(subset).issubset(large_item_set_copy)):
            new_candidates.append(list(candidates[i]))
    
    return new_candidates

if __name__ == "__main__":
    from datetime import datetime
    startTime = datetime.now()
    
    # load the data
    data = load_data()

    # Count the number of 1-itemset and make a dcitionary
    item_dict = get_item_dict(data)

    # Set the result dictionary
    result = {}

    # Gnerate frequent itemsets of length 1
    min_sup = 150
    large_item_dict = {key: value for key, value in item_dict.items() if value >= min_sup}
    # Add to the fianl result
    for key, value in large_item_dict.items():
        result[frozenset([key])] = value

    # Start the loop of generating frequent items from k=2
    large_item_set = []
    for key in large_item_dict.keys():
        large_item_set.append(list([key]))

    k = 2
    while (len(large_item_set) != 0):
        candidates = generate_candidates(large_item_set)
        if (k >= 3):
            candidates = prune_step(candidates, large_item_set)
        large_itemset_dict = count_step(candidates, data, min_sup)
        for key, value in large_itemset_dict.items():
            result[frozenset([key])] = value
        large_item_set = list(list(itemset) for itemset in large_itemset_dict.keys())
        k = k + 1

    # print results
    for key, value in result.items():
        print (key,": ", value)
    print ('Total amount of frequent items: ' + str(len(result)))
    print ('Running time: ' + str(datetime.now() - startTime))
    
    # Export the result to csv
    w = csv.writer(open("Apriori_output.csv", "w", newline = ''))
    for key, val in result.items():
        w.writerow([key, val])
    

