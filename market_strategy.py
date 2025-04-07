# Brandon Cazares
# CECS 427 Sec 1
# Professor Ponce
# Due Date: 4/15/2025
# Assignment 4: Market and Strategic Interaction in Network
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
# First, we load our graph as a GML file
def load_bipartite_graph(file_path):
    """ This loads a bipartite graph from a .gml file"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' doesn't exist.")
    try:
        Graph = nx.read_gml(file_path, label="id")

        # Set node type: buyer or seller
        for node, data in Graph.nodes(data=True):
            if data.get("bipartite") == 0:
                Graph.nodes[node]["type"] = "buyer"
            elif data.get("bipartite") == 1:
                Graph.nodes[node]["type"] = "seller"
            if "price" not in Graph.nodes[node]:
                Graph.nodes[node]["price"] = 0  # default price

        return Graph
    except Exception as error:
        raise ValueError(f"There was an error loading GML file: {error}")
# Now, we verify the bipartite structure
def is_bipartite_market(Graph):
    """Checks if the graph is bipartite with correct 'buyer' and 'seller' labels"""
    # our buyers
    buyers = {n for n, d in Graph.nodes(data=True) if d.get("type") == "buyer"}
    # our sellers
    sellers = {n for n, d in Graph.nodes(data=True) if d.get("type") == "seller"}

    # These are our graph edges
    for u, v in Graph.edges:
        if (u in buyers and v in buyers) or (u in sellers and v in sellers):
            return False  # Invalid bipartite structure (buyer-buyer or seller-seller edge)
    return True
file_path = "market.gml"
market_graph = load_bipartite_graph(file_path)
# we extract our market data
def extract_market_data(Graph):
    """Extracts buyers, sellers, and valuations from a bipartite graph"""
    # our buyers when extracted
    buyers = {n for n, d in Graph.nodes(data=True) if d.get("type") == "buyer"}
    # our sellers when extracted
    sellers = {n for n, d in Graph.nodes(data=True) if d.get("type") == "seller"}

    # Edge attributes (valuation)
    valuations = {(u, v): Graph.edges[u, v].get("valuation", 0) for u, v in Graph.edges}

    for s in sellers:
        if "price" not in Graph.nodes[s]:
            Graph.nodes[s]["price"] = 0

    return buyers, sellers, valuations

# Next, we will plot our graph
def plot_bipartite_graph(Graph, ax=None):
    """We will plot the bipartite graph"""
    plt.figure(figsize=(10, 8))
    # We will seperate both buyers and sellers
    buyers = [n for n, d in Graph.nodes(data=True) if d.get("type") == "buyer"]
    sellers = [n for n, d in Graph.nodes(data=True) if d.get("type") == "seller"]

    # Then, we generate b
    position = {}  # This adjusts layout for visualization
    position.update((n, (1, i)) for i, n in enumerate(buyers)) # Buyers on one side
    position.update((n, (2, i)) for i, n in enumerate(sellers)) # Sellers on the other


    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the directed graph
    nx.draw(Graph, position, with_labels=True, node_size=1000, node_color='lightblue', edge_color='black')
    # We draw edge labels for valuations
    labels = nx.get_edge_attributes(Graph, "valuation")
    nx.draw_networkx_edge_labels(Graph, position, edge_labels=labels, ax=ax)
    # our graph title
    plt.title("Bipartite Market Graph")
    plt.tight_layout()
    plt.show()
# We plot our preferred seller graph
def plot_preference_seller_graph(preferred_graph, ax=None):
    """Plots the directed preferred-seller graph"""
    plt.figure(figsize=(10, 8))

    # Positioning: separate buyers and sellers
    buyers = [n for n in preferred_graph.nodes if preferred_graph.in_degree(n) > 0]
    sellers = [n for n in preferred_graph.nodes if preferred_graph.out_degree(n) > 0]

    # These are our positions
    position = {}
    position.update((n, (1, i)) for i, n in enumerate(buyers))   # buyers on left
    position.update((n, (2, i)) for i, n in enumerate(sellers))  # sellers on right

    if ax is None:
        figure, ax = plt.subplots(figsize=(10, 8))

    # Draw the directed graph
    nx.draw(preferred_graph, position, with_labels=True, node_size=1000, node_color='lightblue', edge_color='gray', arrows=True)
    plt.title("Preferred-Seller Graph")
    plt.tight_layout()
    plt.show()
# First, we will construct our preference seller graph
def construct_preference_seller_graph(Graph):
    """This creates the preference seller graph based on highest effective valuation for each buyer"""
    preferred_graph = nx.DiGraph()

    for b in Graph.nodes:
        # buyers
        if Graph.nodes[b].get("type") == "buyer": # This only processes the buyers
            maximum_value = -float('inf')
            preferred_sellers = []

            for s in Graph.neighbors(b):
                # sellers
                if Graph.nodes[s].get("type") == "seller":
                    valuation = Graph.edges[b, s].get("valuation", 0)
                    price = Graph.nodes[s].get("price", 0)
                    effective_valuation = valuation - price

                    if effective_valuation > maximum_value:
                        maximum_value = effective_valuation
                        preferred_sellers = [s]
                    elif effective_valuation == maximum_value:
                        preferred_sellers.append(s)
            # Now, we add edges in preference seller graph
            for seller in preferred_sellers:
                preferred_graph.add_edge(b, seller)

    return preferred_graph
# Second, we implement Matching & Constricted Set Detection
def find_constricted_set(Graph, preferred_graph):
    """This will help us compute matching and identify constricted sets"""
    matching = nx.bipartite.maximum_matching(preferred_graph)

    unmatched_buyers = {b for b in Graph.nodes if Graph.nodes[b].get("type") == "buyer"} - set(matching.keys())

    constricted_sellers = set()
    for b in unmatched_buyers:
        constricted_sellers.update(preferred_graph.neighbors(b))

    return matching, constricted_sellers

# Third, we implement valuation updates
def update_valuations(Graph, constricted_sellers):
    """This increases prices for sellers in the constricted set"""
    for s in constricted_sellers:
        Graph.nodes[s]["price"] += 1 # This increases seller's price by 1

# Now, we compute our market clearing algorithm and find a stopping condition
def market_clearing(Graph, interactive=False, maximum_rounds=20):
    """Now, we implement the market-clearing algorithm interactively"""
    rounds = 0

    # this indicates our rounds
    while rounds < maximum_rounds:
        print(f"\nRound {rounds+1}:")

        preferred_graph = construct_preference_seller_graph(Graph)
        matching, constricted_sellers = find_constricted_set(Graph, preferred_graph)

        # this prints our matching graph
        print(f"Matching: {matching}")
        # this prints our constricted sellers
        print(f"Constricted Sellers: {constricted_sellers}")

        if not constricted_sellers: # This stops if not a constricted set
            print("Market-clearing equilibrium is calculated!")
            break

        update_valuations(Graph, constricted_sellers)

        if interactive:
            plot_bipartite_graph(Graph) # This shows updated graph state

        rounds += 1

    if rounds == maximum_rounds:
        print("We have reached our maximum iterations without a full market clearing.")

# This is our main function
def main():
    parser = argparse.ArgumentParser(description="Market Clearing Algorithm on a Bipartite Graph")
    parser.add_argument("--file", required=True, help="Input GML file representing the market")
    parser.add_argument("--plot", action="store_true", help="Plot the graph")
    parser.add_argument("--interactive", action="store_true", help="Show each round of computation")

    # Check if the user provided enough arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    Graph = load_bipartite_graph(args.file)
    if not Graph or not is_bipartite_market(Graph):
        print("Error: Invalid bipartite market graph.")
        return

    buyers, sellers, valuations = extract_market_data(Graph)
    # Our loaded market graph is printed with both our buyers and sellers
    print(f"\n Loaded Market Graph: {len(buyers)} Buyers, {len(sellers)} Sellers")
    # our valuations are printed
    print("Valuations:", valuations)

    if args.plot:
        plot_bipartite_graph(Graph)

    market_clearing(Graph, interactive=args.interactive)
if __name__ == "__main__":
    main()
