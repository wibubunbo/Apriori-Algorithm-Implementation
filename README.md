# Apriori-Algorithm-Implementation

This is a Python implementation of the Apriori algorithm for mining frequent itemsets.

# Description
The Apriori algorithm is a classic algorithm in data mining for discovering frequent itemsets in a transactional database. It uses a bottom-up approach, where frequent subsets of items are used to generate candidate sets of larger size, which are then pruned based on their support. The algorithm terminates when no further successful extensions are found.

This implementation is based on the the knowledge I learnt in course SDSC3002 Data Mining in City University of Hong Kong.

# Requirements
Python 3.7 or later

pandas

# Installation
You can download the source code and install it manually:
```
git clone https://github.com/wibubunbo/Apriori-Algorithm-Implementation.git
cd <repository>
pip install .
```
# Usage
```from apriori import apriori```

# Example usage
```
transactions = [
    [1, 2, 5],
    [2, 4],
    [2, 3],
    [1, 2, 4],
    [1, 3],
    [2, 3],
    [1, 3],
    [1, 2, 3, 5],
    [1, 2, 3]
]

min_support = 0.3
apriori(transactions, min_support)
```
