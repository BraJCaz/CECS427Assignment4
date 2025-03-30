# CECS427Assignment4
# Brandon Cazares
# Professor Ponce 
# CECS 427 Sec 1 

# Objective
- In this assignment, we're going to develop practical proficiency in Python programming, meaning on the manipulation of bipartite graphs.
- We need to have a good understanding of the market-clearing algorithm because we need to run a specific command.

# Requirement 
- This is the command to execute the Python script market_strategy.py located in the current directory that reads this file market.gml.
- Here, market.gml will be used for the analysis and the format is Graph Modeling Language (.gml) which describes the graph's structure with attributes.
- This program should read the attributes of the nodes and edges in a file. 
python ./market_strategy.py market.gml --plot --interactive

- market.gml encodes a bipartite graph of 2n nodes with two sets A=(0, 1, .. n-1) and B=(n-1, n, .. 2n-1) where the nodes of set A have a price and the valuations of set B are set as attributes of the edges 

# Description of Parameters
- The script market_strategy.py must be located in the current directory
- Next, we need to ensure a robust file handles mechanisms such as error checking, file existence validation, and appropriation error messages. 
