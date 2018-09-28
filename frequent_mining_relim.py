# -*- coding: utf-8 -*-
"""
Created on Sep.27th, 2018

@author: AndyKANG (modified from comp4331fall18's sample code)
"""

from pymining import itemmining, assocrules
import csv

class freq_mining(object):
    """docstring for ClassName"""
    def __init__(self, transactions, min_sup, min_conf):
        self.transactions = transactions  # database
        self.min_sup = min_sup  # minimum support
        self.min_conf = min_conf  # minimum confidence

    def freq_items(self):
        """
        Import the itemming tools and perform relim mining
        Returns:
            item_sets: frequent item sets
        """
        relim_input = itemmining.get_relim_input(self.transactions)
        item_sets = itemmining.relim(relim_input, self.min_sup)
        return item_sets

    def association_rules(self):
        item_sets = self.freq_items()
        rules = assocrules.mine_assoc_rules(item_sets, self.min_sup, self.min_conf)
        return rules

def main(transactions, min_sup, min_conf):

    item_mining = freq_mining(transactions, min_sup, min_conf)
    freq_items = item_mining.freq_items()
    rules = item_mining.association_rules()
    
    return freq_items, rules
    
    
if __name__ == "__main__":
    # Counting time
    from datetime import datetime
    startTime = datetime.now()
    
    # Load the data from freq_items_datasets.txt file
    with open('./freq_items_datasets.txt') as f:
        data = f.read().split('\n')

    for i in range(len(data)):
        data[i] = tuple(data[i].split())
        
    transactions = tuple(data)

    # Set the minimum support and confidence
    min_sup = 150
    min_conf = 0

    # Implement the relim mining
    freq_items, rules = main(transactions, min_sup, min_conf)
    
    
    # Print the result
    for key, value in freq_items.items():
        print (key,": ", value)
    print ('Total amount of frequent items: ' + str(len(freq_items)))
    
    print ('Running time: ' + str(datetime.now() - startTime))
    
    # Write the resule to csv file 
    w = csv.writer(open("relim_output.csv", "w", newline=''))
    for key, val in freq_items.items():
        w.writerow([key, val])






