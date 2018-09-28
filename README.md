# Frequent-Itemset-Mining

> An course practice to perform frequent item sets mining. The benchmark dataset freq items dataset is supported by the IBM Almaden Quest research group, which contains 1,000 items and 100,000 transactions. For simplicity, each number uniquely identifies an item.

 

The frequent itemset mining runs in various times, which is very related to the complexity of the algorithms. Scanning transactions of the database is time consuming. *Apriori* is a classical way to mine frequent itemsets. *FP-growth* and *Relim* use more efficient ways to construct data structures and reduce the times of database scanning. This report shows different running times and explanations when performing frequent items mining with 3 different algorithms.

 

**Environment**

System: Windows 10, 64-bit Operating System

Processor: Intel(R) Core(TM) i7-7700HQ CPU @ 2.8GHz 2.80Hz

Installed RAM: 16.0 GB

 

**Apriori:** 

Running time: 1:04:11.844760

The [*Apriori Algorithm*](./frequent_mining_apriori.py) repeats the process of “generating candidates”, “pruning”, and “counting”. For each “counting” step, it is necessary to scan the original database once, which is very time consuming for a large data set.

The computational complexity of this approach is *O(2n),* because there are 2n possible candidates item sets. So, the computing time increasing rapidly as the data base goes larger.

 

 

**Frequent Pattern Growth (FP-growth):**

Running time: 0:02:50.800351

The [*FP-growth Algorithm*](./frequent_mining_fp-growth.py) is a much more efficient algorithm by reducing the number of data scanning. It only requires 2 scans of transactions database: collecting frequent items and constructing FP-tree to store the data. FP-tree will help keep all the rules in the dataset, so that it saves a lot of time of repeated scanning.

The complexity of this approach is *O(n2)*. So, the running time was much shorter than the *Apriori Algorithm.*

 

 

**Recursive Elimination (Relim):**

Running time: 0:00:37.440106

[*Recursive elimination*](./frequent_mining_relim.py) is an algorithm strongly inspired by the *FP-growth algorithm*. By constructing transaction lists recursively, it can mine the frequent itemset with simple data structure. Compare to FP-growth, it has several advantages:

(1)    Transactions list is a simpler structure to store data compare to the FP-tree, which is easier to implement. 

(2)    *Relim Algorithms* will eliminate small data set recursively and no re-representation of the transactions is necessary, which saves memory in the recursion.

Relim would have a better performance in small support or data with high frequency, and it might be slower when meeting long frequent dataset. As the experiments showed the *Relim Algorithm* performs best among the three methods in our dataset.

 

**Closed & Maximal Frequent Itemset:**

The [closed & maximal](./frequent_mining_closed_maximal.py) frequent Itemset is generated based on *Relim Algorithm*, because it’s relatively the most efficient algorithm.

Closed Frequent Itemset: An itemset is maximal frequent if none of its immediate supersets is frequent.

Maximal Frequent Itemset: An itemset is closed if none of its immediate supersets has the same support as the itemset.

 

**Number of Frequent Itemsets (min_sup = 150):**

Frequent Itemset: 19126

Closed Sets:  18650

Maximum Sets: 2399

 

**Notes:**

All .py files were written in Python 3. And the mining results for each method was exported to .csv file.