import pandas as pd
from collections import Counter, defaultdict
from itertools import combinations

class Trie:
    """
    A class representing a trie data structure for storing and searching frequent itemsets.
    """
    def __init__(self):
        self.child = defaultdict(Trie)
        self.is_leaf = False

    def insert(self, item):
        """
        Insert an item into the trie.
        """
        temp = self
        for i in item:
            temp = temp.child[i]
        temp.is_leaf = True

    def check(self, transaction, item, res):
        """
        Check a transaction against the trie to generate all possible frequent itemsets for counting frequency of candidate pairs.
        """
        if self.is_leaf is True:
            res.append(item) 
            return
        temp = self
        for i in transaction:
            if i in temp.child:
                temp.child[i].check(transaction[transaction.index(i) + 1:], item + [i], res)

def apriori(trans, min_support = 0.5):
    """
    An implementation of the Apriori algorithm for mining frequent itemsets.

    Args:
    trans (list): A 2D list of transactions, where each transaction is a list of positive integers, each integer represents for an item.
    min_support (float, default = 0.5): A float between 0 and 1 for minumum support of the itemsets returned.
      The support is computed as the fraction
      `transactions_where_item(s)_occur / total_transactions`.

    Returns:
    Report the number of frequent patterns, as well as the number of size-k frequent patterns for each size k with at least 
    one frequent pattern.
    freq_itemsets_df : A pandas DataFrame of frequent itemsets.
    """
    # Sort each of transaction
    trans = [sorted(x) for x in trans]
    total_transactions = len(trans)
    min_items = min_support * total_transactions
    
    # Count the frequency of each 1-itemset
    C1 = Counter()
    bucket = {}
    for transaction in trans:
        C1.update(transaction)
        for item_set in combinations(transaction, 2):
            key = hash(item_set)
            bucket[key] = bucket[key] + 1 if key in bucket else 0
    
    # Prune all of infrequent 1-itemsets from C1 and generate L1
    L1 = [x[0] for x in C1.items() if x[1] >= min_items]
    L1 = sorted(L1)
    print("Number of size-1 frequent patterns: {}".format(len(L1)))
    freq_itemsets_df = pd.Series([[x] for x in L1])

    # Prune all of 2-itemsets which are in infrequent buckets with minSup = minFreq * total_transaction - 1 and generate L2
    L2 = []
    for item_set in combinations(L1, 2):
        key = hash(item_set)
        if key in bucket and bucket[key] >= min_items - 1:
            L2.append(list(item_set))
    print("Number of size-2 frequent patterns: {}".format(len(L2)))
    freq_itemsets_df = pd.concat([freq_itemsets_df, pd.Series(L2)], ignore_index=True)
    
    # Calculate total frequent patterns in transaction with variable total_freq_patterns
    total_freq_patterns = len(L1) + len(L2)
    L = L2.copy()
    k = 3

    # For loop will stop when size of L is 0, which means we cannot find any frequent itemset with size larger than variable k.
    while len(L) >= 1:
        # Self-joining L_{k - 1} to generate C_{k}
        C = []
        for i in range(0, len(L) - 1):
            for j in range(i + 1, len(L)):
                if L[j][-2] == L[i][-2]:
                    temp = L[i][:] + [L[j][-1]]
                    C.append(temp)
                else:
                    break

        # Use hash_table to store the frequency of k-itemsets
        trie = Trie()
        hash_table = {}
        for item_set in C:
            trie.insert(item_set)
            hash_table[tuple(item_set)] = 0
       
        # Early stops using prefix tree to generate frequent k-itemsets from each transaction and count support for candidate itemsets
        for transaction in trans:
            if len(transaction) >= k:
                prefix_itemset = []
                trie.check(transaction, [], prefix_itemset)
                for item_set in prefix_itemset:
                    hash_table[tuple(item_set)] += 1
        
        # Clear the list L with frequent (k - 1)-itemsets to update new frequent itemsets with size k
        L.clear()
        for item_set in hash_table:
            if hash_table[item_set] >= min_items:
                L.append(list(item_set))
        L = sorted(L)
        if len(L) > 0:
            freq_itemsets_df = pd.concat([freq_itemsets_df, pd.Series(L)], ignore_index=True)
        total_freq_patterns += len(L)
        print("Number of size-{} frequent patterns: {}".format(k, len(L)))
        k += 1 
    print("Total number of frequent patterns with min_support = {}: {}".format(min_support, total_freq_patterns))
    print(freq_itemsets_df)