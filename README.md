# CECS427Assignment4
# Brandon Cazares
# Professor Ponce 
# CECS 427 Sec 1 
# Due Date: 4/15/2025 

# Objective
- In this assignment, we're going to develop practical proficiency in Python programming, meaning on the manipulation of bipartite graphs.
- We need to have a good understanding of the market-clearing algorithm because we need to run a specific command.

# Requirement 
- This is the command to execute the Python script market_strategy.py located in the current directory that reads this file market.gml.
- Here, market.gml will be used for the analysis and the format is Graph Modeling Language (.gml) which describes the graph's structure with attributes.
- This program should read the attributes of the nodes and edges in a file. 
- python ./market_strategy.py market.gml --plot --interactive

- market.gml encodes a bipartite graph of 2n nodes with two sets A=(0, 1, .. n-1) and B=(n-1, n, .. 2n-1) where the nodes of set A have a price and the valuations of set B are set as attributes of the edges 

# Description of Parameters
- The script market_strategy.py must be located in the current directory
- Next, we need to ensure a robust file handles mechanisms such as error checking, file existence validation, and appropriation error messages.
-- plot
- This requests that the graph should be plotted. This parameter triggers our graph which includes, nodes, plots, edges and possiblty additional metrics or shortest paths.
-- interactive
- This requests that our program demonstrates a round of every graph which is also our output. A round is known as the seller graph, computed constricted sets matching and updating our evaluation based on our results.

# Results 
- When I ran this given command for the assignment, it gave me 3 of both buyers and sellers for my loaded market graph before my first round and my valuations. 
- For round 1, it gave me a matching set and 4 constricted sets.
- For round 2, it gave me the same exact thing as round 1.
- For round 3, it gave me 5 matching sets and our constricted sellers are a final set.
- Finally, I calculated my market-clearing equilibrium graph. 
