import frequent_mining_relim as relim
import collections
import csv


def load_data():
    """
    Load the data from the raw data set.

    Returns:
        data: a tuple of transactions with tuple of items in each line
    """
    with open('./freq_items_datasets.txt') as f:
        data = f.read().split('\n')

    for i in range(len(data)):
        data[i] = tuple(data[i].split())

    return tuple(data)


def freq_items_minning(data, min_sup, min_conf):
    """
    This function use relim method which has been implemented in "A1_ykangae_20412340_code_relim.py" to generaete frequent item set.
    Args:
        min_sup: minimum support
        min_conf: minimum confidence
    Returns:
        freq_items: a dictinary of frequent items as keys and the corresponding occurencies as values
    """
    freq_items, rules = relim.main(data, min_sup, min_conf)
    
    return freq_items

def classify_freq_items(freq_items):
    """
    Classify the frequent items dictionary into k sub-dictionary inside a large one. 
    Set the key as the length of item sets.
    Args:
        freq_items: a dictinary of frequent items as keys and the corresponding occurencies as values
    Returns:
        freq_items_classify: a dictinary with key of different length and frequent items dicnaries as values
    """
    freq_items_classify = collections.defaultdict(dict)

    for key, value in freq_items.items():
        freq_items_classify[len(key)][key] = value
    
    return freq_items_classify


def max_close_mining(freq_items):
    """
    This function mines maximal closed frequent itemsets and maximal frequent itemsets from the frequent itemsets
    Args:
        freq_items: a dictinary of frequent items as keys and the corresponding occurencies as values
    Returns:
        max_freq_items: a dictinary stores the maximal frequent itemsets and the corresponding occurencies
        close_freq_items: a dictinary stores the closed frequent itemsets and the corresponding occurencies
    
    """
    # Classify the original freq_items to k sub-dictionary according to the length of sets
    freq_items_classify = classify_freq_items(freq_items)
    
    max_freq_items_list = []
    close_freq_items_list = []
    
    for k in  range(1,len(freq_items_classify)):
        for k_itemset in freq_items_classify[k].keys():
            check_max = 0    # variable to mark the max_freq_itemset: {0-yes, 1-no}
            check_close = 0   # variable to mark the close_freq_itemset: {0-yes, 1-no}
            for k_plus1_itemset in freq_items_classify[k+1].keys():
                # if the k-size itemset is the subset of the k+1-size itemset
                # the k-size itemset is not a max_freq_itemset
                if k_itemset.issubset(k_plus1_itemset):
                    check_max = 1
                    # given the item find a superset
                    # check the occurencies of them to check the property of closed itemset
                    if (freq_items[k_itemset] == freq_items[k_plus1_itemset]):
                        check_close = 1
                        break
            if (check_max == 0):
                max_freq_items_list.append(k_itemset)
            if (check_close == 0):
                close_freq_items_list.append(k_itemset)
    
    # Finally append the largest set (they must be maximal and closed)
    for k_itemset in freq_items_classify[len(freq_items_classify)].keys():
        max_freq_items_list.append(k_itemset)
        close_freq_items_list.append(k_itemset)
    
    max_freq_items = {}
    for max_item_set in max_freq_items_list:
        max_freq_items[max_item_set] = freq_items[max_item_set]
        
    close_freq_items = {}
    for close_item_set in close_freq_items_list:
        close_freq_items[close_item_set] = freq_items[close_item_set]
    
    return max_freq_items, close_freq_items


def export_dict_to_csv(path, dictionary):
    """
    Export dictionary to csv file
    Args:
        path: directory of .csv file to be stored
        dictionary: a dictionary to be wrote
    
    """
    w = csv.writer(open(path, "w", newline=''))
    for key, val in dictionary.items():
        w.writerow([key, val])

        
if __name__ == "__main__":
    # Load the data from .txt file
    data = load_data()
    
    min_sup = 150
    min_conf = 0
    
    # Frequent items mining
    freq_items = freq_items_minning(data, min_sup, min_conf)
    
    # Maximal and closed frequent items mining
    max_freq_items, close_freq_items = max_close_mining(freq_items)
    
    # Export the result
    export_dict_to_csv("maximal_output.csv", max_freq_items)
    export_dict_to_csv("closed_output.csv", close_freq_items)
    