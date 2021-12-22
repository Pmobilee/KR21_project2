from typing import Union
from BayesNet import BayesNet
import BNReasoner
import os


from typing import List, Tuple, Dict
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.readwrite import XMLBIFReader
import math
import itertools
import pandas as pd
from copy import deepcopy


# This code is for local testing only, see it's implementation in BNReasoner for normal use

cwd = os.getcwd()
test_file = BNReasoner.BNReasoner(net = f'{cwd}/testing/dog_problem.BIFXML')
# test_file  = BNReasoner.BNReasoner(net = nx.read_gpickle(f"{cwd}/net25/net25_2.gpickle"))

# Function to compare edges between nodes, always returns at least 1 since two connected nodes share an edge to each other
def filter_(x, y):
    count = 0
    for edge in x:
        if edge not in y:
            count += 1
    return count

# Function to return the order, takes the graph file and heuristic as input
def get_order(graph, heuristic, query = []):

    # Gets the interaction graph and stores the original version for later comparison
    graph = graph
    interaction_graph = graph.bn.get_interaction_graph()
    original_interaction_graph = graph.bn.get_interaction_graph()
    original_interaction_graph.remove_nodes_from(query)
    
    order = []

    # Min-degree heuristic
    if heuristic == 'min_degree':

        # For the amount of nodes in the interaction graph..
        length = len(list(original_interaction_graph.nodes))
        for i in range(length):
            
            # Get the degrees (adjacent nodes)
            # interaction_graph = graph.bn.get_interaction_graph()
            
            degrees = dict(interaction_graph.degree)
            
            # And sort the degrees (adjacent nodes) based on number of edges 
            sorted_degrees = dict(sorted(degrees.items(), key=lambda item: item[1]))
            
            # This is ugly but true: this entire function was written for dog_problem, and worked. But the other examples went past the length of the amount of nodes, this is a failsafe
            # So if this entire loop is run the amount of times that there are nodes, the entire function is stopped, and the last remaining node is added to the order list
            if i == length - 1:
                order.extend(list(interaction_graph.nodes))

                # For some reason with one of the example files, it added a previously deleted node to the order list 'winter', so if there are more items in the order list than there are actual nodes, delete the last item which does not belong there
                if len(order) > len(list(original_interaction_graph.nodes)):
                    order.pop(-1)

                
                for z in range(len(query)):
                    if query[z] in order:
                        order.remove(query[z])
                
                temp_list = list(set(list(original_interaction_graph.nodes)) - set(order))
                order.extend(temp_list)
                order.extend(query)
                return order

            # The node with minimal amount of degrees is the first item of the sorted dictionary. Then you get its adjacent nodes, which returns a dictionary, and you take the key values for the actual node names
            
            for x in sorted_degrees.keys():
                min_degree_node = next(iter(sorted_degrees))
                if min_degree_node in query:
                    continue
                else:
                    break


            min_node_adjacents = interaction_graph.adj[min_degree_node]
            adjacents = list(min_node_adjacents.keys())
            

            # if the minimum node has more than 1 adjacent nodes
            if len(min_node_adjacents.keys()) > 1:

                # store the adjecent nodes in temp list, so not to actually alter the list with adjacent nodes
                temp_adjacents = adjacents

                # Then for every adjacent node
                for i in range(len(min_node_adjacents.keys())):

                    # store the current adjacent node and remove it from the list (so it does not create an edge with itself, which returns a cyclic error)
                    current_adjacent = temp_adjacents[i]
                    
                    # for every adjacent node that does not equal the adjacent node we're currently trying to add an edge to...
                    for j in range(len(temp_adjacents)):

                        if temp_adjacents[i] == current_adjacent:
                            continue

                        # Add the edge between these two adjacent nodes
                        else:
                            interaction_graph.add_edge(current_adjacent, temp_adjacents[j])
                
                # After the edges are added, we can safely delete the node and store it as our (next) node in the order list
                interaction_graph.remove_node(min_degree_node)
                if min_degree_node not in query:
                    order.append(str(min_degree_node))
            
            # If there is there is just one adjacent node, it could mean that we've reached the final node, so we add that last node to our order list and return it, stopping the function
            else:
                if len(list(interaction_graph.nodes)) == 1:
                    if min_degree_node not in query:
                        order.extend(list(interaction_graph.nodes))

                    
                    for i in range(len(query)):
                        if query[i] in order:
                            order.remove(query[i])
                    
                    return order

                # However, in all other cases it just means no edges need to be added as there is only one adjacent node  
                else:
                   
            
                    interaction_graph.remove_node(min_degree_node)
                    
                    if min_degree_node not in query:
                        order.append(str(min_degree_node))

    # Min_fill heuristic
    elif heuristic == 'min_fill':
        
        length = len(list(original_interaction_graph.nodes))
        interaction_graph = nx.Graph(original_interaction_graph)

        # For the amount of nodes in the interaction graph..
        for i in range(length):
            
            
            

            # This is ugly but true: this entire function was written for dog_problem, and worked. But the other examples went past the length of the amount of nodes, this is a failsafe
            # So if this entire loop is run the amount of times that there are nodes, the entire function is stopped, and the last remaining node is added to the order list
            if i == length-1:

                if current_least_edges not in query:
                    order.extend(list(interaction_graph.nodes))
                if len(order) > len(list(original_interaction_graph.nodes)):
                    order.pop(-1)

                for t in range(len(query)):
                    if query[t] not in order:
                        order.append(query[t])
                return order

            # Setting our current node with least edges to None, and giving the current least number of edges to an unrealistically high number
            

            current_least_edges = None
            current_least_edges_count = 1000
            # Set the current node
            for j in range(len(interaction_graph.nodes)):
                

                # print('nodes:', interaction_graph.nodes, 'i:', j)
                node = list(interaction_graph.nodes)[j]
                

                # Find its adjacents
                node_adjacents = interaction_graph.adj[node]

            
                node_adjacents_list = list(node_adjacents.keys())

                # Could not think of a better name, this returns the edges that the node has, but in a list with tuples, that we have to extract below
                node_edges_list = list(interaction_graph.edges(node))
                node_edges = []
                
                # For every item in the previous list, extract the tuple, and get the actual edge node by taking the second value in that tuple, example from a current node 'dog-bark' : ('dog-bark', 'bowel-problem')[1] == 'bowel-problem' <- edge node
                for g in range(len(node_edges_list)):
                    node_tuples = node_edges_list[g]
                    node_edges.append(node_tuples[1])
                


                # For all adjacents check how many of their edges do not match the root node adjacents (so we can calculate how many new edges we would make if we removed our current node)
                for z in range(len(node_adjacents_list)):

                    # Pick our first child node that is adjacent to our current node
                    child_node = node_adjacents_list[z]

                    # Get its edges
                    child_node_list = list(interaction_graph.edges(child_node))
                    child_node_edges = []

                    # Now we get all the edges of the child node to compare to our current node, so we can calculate how many new edges we would create later
                    for g in range(len(child_node_list)):
                        child_node_tuples = child_node_list[g]
                        child_node_edges.append(child_node_tuples[1])
                        
                    
                    # Use the filter_ function to calculate how many new edges would have to be created on this child node
                    edge_count = filter_(node_edges, child_node_edges) +1

                    # If the amount is less than our current best, the child node becomes the new node with the least amount of edges created if it were deleted
                    if edge_count < current_least_edges_count:
                        # print('node:', node, 'has edges:', edge_count)
                        current_least_edges = node
                        current_least_edges_count = edge_count
                        # print('-------------current least edges count = ', current_least_edges_count)

            if current_least_edges == None:
                # print('NOTHING')
                current_least_edges = list(interaction_graph.nodes)[0]


            # print('Least edges:', current_least_edges)

            
            # This seems a little strange, but I copied everything below from min_degree, as removing the nodes and adding edges is the exact same
            # Please disregard the naming scheme, we just set min_degree node to our min_fill node
            min_degree_node = current_least_edges
            
            min_node_adjacents = interaction_graph.adj[min_degree_node]


            adjacents = list(min_node_adjacents.keys())
            

             # if the minimum node has more than 1 adjacent nodes
            if len(min_node_adjacents.keys()) > 1:

                # store the adjecent nodes in temp list, so not to actually alter the list with adjacent nodes
                temp_adjacents = adjacents





                # Then for every adjacent node
                for i in range(len(min_node_adjacents.keys())):

                    # store the current adjacent node and remove it from the list (so it does not create an edge with itself, which returns a cyclic error)
                    current_adjacent = temp_adjacents[i]
                    
                    # for every adjacent node that does not equal the adjacent node we're currently trying to add an edge to...
                    for j in range(len(temp_adjacents)):

                        if temp_adjacents[j] == current_adjacent:
                            continue
                       
                        # Add the edge between these two adjacent nodes
                        else:
                            interaction_graph.add_edge(current_adjacent, temp_adjacents[j])
                

                



                # After the edges are added, we can safely delete the node and store it as our (next) node in the order list
                # print(f'deleting node: {min_degree_node}, left: {interaction_graph.nodes}')
                interaction_graph.remove_node(min_degree_node)
                order.append(str(min_degree_node))
            
            # If there is there is just one adjacent node, it could mean that we've reached the final node, so we add that last node to our order list and return it, stopping the function
            else:
                if len(list(interaction_graph.nodes)) == 1:
                    # order.extend(list(interaction_graph.nodes))
                    # return order
                    # print(f'deleting node: {min_degree_node}, left: {interaction_graph.nodes}')
                    interaction_graph.remove_node(min_degree_node)
                    order.append(str(min_degree_node))

                # However, in all other cases it just means no edges need to be added as there is only one adjacent node  
                else:
                    # print(f'deleting node: {min_degree_node}, left: {interaction_graph.nodes}')
                    interaction_graph.remove_node(min_degree_node)
                    
                    order.append(str(min_degree_node))

    else:
        print(f'Given heuristic \'{heuristic}\' does not match min-degree or min-fill, exiting..')


# interaction_graph = test_file.bn.get_interaction_graph()
# degrees = dict(interaction_graph.degree)
# print(degrees)

# print()


# test_file  = BNReasoner.BNReasoner(net = nx.read_gpickle(f"{cwd}/net15/net15_2.gpickle"))
print(test_file.bn.get_all_variables())
print(get_order(test_file, 'min_fill', query = [])) 