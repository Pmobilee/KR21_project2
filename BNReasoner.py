from typing import Union
from BayesNet import BayesNet
import pandas as pd
from copy import deepcopy
import random
import networkx as nx
import os

class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net

    # TODO: This is where your methods should go
    def get_parents(self, variable: str):

        return [c for c in self.bn.structure.predecessors(variable)]

    
    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.bn.get_all_variables():
            return []
        paths = []
    
    #Recursive function to search through all the possible paths.
    #Search through all parents and children of each variable,
    #If the end is not there, start search for each of these variables
    #until the end is found
    
        for node in self.bn.get_children(start)+self.get_parents(start):
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    
    def d_separation(self, start, end, given):
        
        paths = self.find_all_paths(start, end)
        print('These are all the paths: ', paths)
        count = 0
        closed_valve = []
        # In the loop, we look at each triplet in the path
        # and see if it is divergent, sequential or convergent
        # If sequential or divergent, if the middle node is given
        # path is closed. For convergent, the other way around.
        #If all paths closed, they're d-separated
        #Node is the start of triplet, path[count] is middle node and
        # path[count+1] end node of the triplet
        for path in paths:
            for node in path[:-2]:
                count += 1
                if path[count] in self.bn.get_children(node):
                    if path[count+1] in self.bn.get_children(path[count]): #sequential valve
                        if path[count] in given:
                            closed_valve.append(True)
                        else:
                            closed_valve.append(False)
                    if path[count+1] in self.get_parents(path[count]): #convergent
                        if path[count] in given:
                            closed_valve.append(False)
                        else:
                            conv=path[count]
                            closed_convergent_valve = True
                            while not not self.bn.get_children(conv):
                                for children in self.bn.get_children(conv):
                                    if children in given:
                                        closed_valve.append(False)
                                        closed_convergent_valve = False
                                        br=True
                                        break
                                if br==True:
                                    break
                            if closed_convergent_valve == True:
                                closed_valve.append(True)
                            
                if path[count] in self.get_parents(node):
                    if path[count+1] in self.bn.get_children(path[count]): #divergent valve
                        if path[count] in given:
                            closed_valve.append(True)
                        else:
                            closed_valve.append(False)
                    if path[count+1] in self.get_parents(path[count]): #sequential
                        if path[count] in given:
                            closed_valve.append(True)
                        else:
                            closed_valve.append(False)
        
        closed_path = []
        valves_old = 0
        valves_new = 0
        
        #We now have a list of all the closed and open valves,
        #Now we see if each path is closed by reviewing all the vales
        #in each path. The valves corresponding to a given path are
        #closed_valve[valves_old:valves_new + 1]. If any is closed (is_closed = True)
        #the path is closed. If one path is open (closed_ath = False),
        # then the variables are not d-separated
        for path in paths:
            valves_new = valves_new + len(path) - 2
            if True in closed_valve[valves_old:valves_new + 1]:
                closed_path.append(True)
            else:
                closed_path.append(False) 
                
        if False in closed_path:
            d_sep = False
        else:
            d_sep = True
            
        print('Closed valves: ', closed_valve)
        print('Closed paths: ', closed_path)
        print('Are', start, 'and', end, 'd-separated by' , given, '?', d_sep)
        return closed_valve, closed_path, d_sep
    
    
    def pruning(self, x, y, z, truth_value):

        if isinstance(z,str):
            z1 = []
            z1.insert(0,z)
        else:
            z1 = z
        #pruning leaf nodes
        for variable in self.bn.get_all_variables():
            if self.bn.get_children(variable)==[] and variable not in x and variable not in y and variable not in z1:
                self.bn.del_var(variable)
        
        #edge pruning
        count = 0
        for var in z1:
            
            for child in self.bn.get_children(var):
                new_cpt = self.bn.get_compatible_instantiations_table( pd.Series({var:truth_value[count]}), self.bn.structure.nodes[child]['cpt'])
                new_cpt = new_cpt.drop(var,axis=1).reset_index(drop=True)
                self.bn.structure.nodes[child]["cpt"] = new_cpt
            new_cpt = self.bn.get_compatible_instantiations_table( pd.Series({var:truth_value[count]}), self.bn.structure.nodes[var]['cpt'])
            self.bn.structure.nodes[var]["cpt"] = new_cpt.reset_index(drop=True)
            
            for edge_end in self.bn.get_children(var):
                self.bn.del_edge([var, edge_end])
            count +=1
        return self

    def order(self, query):
        variables = self.bn.get_all_variables()
        if "p" in variables:
            self.bn.del_var('p')
            variables = self.bn.get_all_variables()
        for item in query:
            variables.remove(item)
        random.shuffle(variables)
        order = variables
        order.extend(query)
        return order


    def multi_factor(self, lista):
        maybe = deepcopy(lista)
        if len(lista) == 1:
            return lista[0]
        while len(lista) > 1:
            x = lista[0]
            y = lista[1]
            overlapping_labels = x.columns[:-1].intersection(y.columns[:-1])
            overlapping_labels = overlapping_labels.tolist()
            if "p" not in x.columns:
                x.rename(columns={x.columns[-1]: 'p'}, inplace=True)
            if y.columns[-1] != "p":
                y.rename(columns={y.columns[-1]: 'p'}, inplace=True)
            z = x.merge(y, on=overlapping_labels, how="outer")
            z["factor"] = z['p_x'] * z['p_y']
            z = z.drop(['p_x', 'p_y'], axis=1)
            lista.pop(0)
            lista.pop(0)
            lista.append(z)

        a = lista[0]
        a = a.dropna(subset = ["factor"], inplace=False).reset_index(drop=True)
        return a

    def summing_out(self, cpt, variable):
        if len(cpt.index) == 1:
            df_new = cpt.drop(variable, axis = 1)
            if "p" in df_new.columns:
                df_new.rename(columns={df_new.columns[-1]: 'factor'}, inplace=True)
        else:

            df = cpt.drop(variable, axis = 1)
            d = df.columns[-1]
            agg = {d: 'sum'}
            groups = df.columns.to_list()[:-1]
            if len(groups) == 0:
                print(cpt)
                cpt.rename(columns={cpt.columns[-1]: "factor"}, inplace=True)
                return cpt
            df_new = df.groupby(groups, as_index=False).aggregate(agg).reindex(columns=df.columns)
        return df_new

    def maxing_out(self, cpt,variable):
        row = len(cpt.index)
        if 'p' in list(cpt.columns):
            cpt.rename(columns={"p": "factor"}, inplace=True)
        colssa = list(cpt.columns)
        colss = list(cpt.columns)
        colss.remove('factor')
        if len(colss) > 1:
            colss.remove(variable)
            colssa.remove(variable)
        b = cpt

        b = b.loc[b.groupby(colss)["factor"].idxmax()].reset_index(drop=True)
        cpt = cpt.groupby(colss)["factor"].agg('max').reset_index()
        if row == len(cpt.index) == 1:
            cpt = cpt[cpt['factor'] == cpt[ 'factor'].max()].reset_index(drop= True)
            b = deepcopy(cpt)
        return b, cpt

    def prior_marginals(self, order:list):
        all = self.bn.get_all_cpts()
        x = list(all.values())
        for variable in order:
            mention = []
            for cpt in x:
                if variable in cpt.columns.tolist():
                    mention.append(cpt)
            factor = self.summing_out(self.multi_factor(mention),variable)
            y = []
            for cpt in x:
                if variable not in cpt.columns.tolist():
                    y.append(cpt)
            y.append(factor)
            x = y
        return x

    def get_variables_from_order(self, variable):
        x = self.bn.get_children(variable)
        x.append(variable)
        return x

    def posterior_marginals(self,query:list, order: list, evidence):
        thing = self.bn.get_all_cpts()
        for key, value in evidence.items():
            for key_1, value_1 in thing.items():
                if key in value_1.columns:
                    value_1.drop(value_1.index[value_1[key] != value], inplace=True)
                    value_1.reset_index()
        for variable in order:
            mention_keys = []
            mention = []

            for key, df in thing.items():
                if variable in df.columns.tolist():
                    mention.append(df)
                    mention_keys.append(key)
            if variable not in query:
                factor = self.summing_out(self.multi_factor(mention), variable)
            else:
                factor = self.multi_factor(mention)
            for s in mention_keys:
                thing.pop(s)
            nm = ' '.join(mention_keys)
            name = f"Sigma {variable} factor {nm}"
            thing[name] = factor
#        ending = []
#        ending_keys = []
#        for variable in self.bn.get_all_variables():
#            if variable in order:
#                continue
#            for key, df in thing.items():
#                if variable in df.columns.tolist():
#                    ending.append(df)
#                    ending_keys.append(df.keys())
#        for key, df in thing.items():
#            ending.append(df)
#        print(ending)
#        end = self.multi_factor(ending)

        sum = factor["factor"].sum()
        factor["factor"] = factor["factor"].values / sum
        thing[name] = factor
        return thing

#    def MPE(self,evidence,order):
#        self.pruning([],[],evidence.index,evidence.values)
#        z = self.bn.get_all_cpts()
#        ins = []
#        for variable in order:
#            mention = []
#            mention_keys = []
#            for key, df in z.items():
#                if variable in df.columns.tolist():
#                    mention.append(df)
#                    mention_keys.append(key)
#            instant, factor = self.maxing_out(self.multi_factor(mention), variable)
#            instant.pop('factor')
#            for s in mention_keys:
#                z.pop(s)
#            nm = ' '.join(mention_keys)
#            name = f" MAX {variable} factor {nm}"
#            z[name] = factor
#            ins.append(instant)
#        while len(ins) > 1:
#            x = ins[0]
#            y = ins[1]
#            if len(x.columns.intersection(y.columns)) > 0:
#                overlapping_labels = x.columns.intersection(y.columns)
#                overlapping_labels = overlapping_labels.tolist()
#                a = x.merge(y, on=overlapping_labels, how="inner")
#                ins.append(a)
#                ins.pop(1)
#                ins.pop(0)
#                continue
#            if len(x.columns.intersection(y.columns)) == 0:
#                a = x.join(y)
#                ins.append(a)
#                ins.pop(1)
#                ins.pop(0)
#                continue
#        b = 1
#        while len(z) > 0:
#            print(z)
#            a = list(z.values())[0]["factor"]
#            b *= a.at[0]
#            z.pop(list(z.keys())[0])
#        return b,ins

    def MAP(self,query = None, evidence = pd.Series({}), heuristic = 'random'):
        if query is None:
            query = []
        self.pruning([], query, evidence.index, evidence.values)
        print("pruning done")
        z = self.bn.get_all_cpts()

        if heuristic == 'random':
            order = self.order(query)
        if heuristic == 'min_degree':
            order = self.get_order(heuristic ='min_degree', query = query)
        if heuristic == 'min_fill':
            order = self.get_order(heuristic='min_fill', query=query)
        print("order done")

        if not query:
            query = order
        ins = []
        for variable in order:
            mention_keys = []
            mention = []
            for key, df in z.items():
                if variable in df.columns.tolist():
                    mention.append(df)
                    mention_keys.append(key)
            if variable not in query:
                factor = self.summing_out(self.multi_factor(mention), variable)
                for s in mention_keys:
                    z.pop(s)
                nm = ' '.join(mention_keys)
                name = f"Sigma {variable} factor {nm}"
                z[name] = factor
            if variable in query:
                instant, factor = self.maxing_out(self.multi_factor(mention), variable)
                instant.pop('factor')
                for s in mention_keys:
                    z.pop(s)
                nm = ' '.join(mention_keys)
                name = f" MAX {variable} factor {nm}"
                z[name] = factor
                ins.append(instant)

        while len(ins) > 1:
            x = ins[0]
            y = ins[1]
            if len(x.columns.intersection(y.columns)) > 0:
                overlapping_labels = x.columns.intersection(y.columns)
                overlapping_labels = overlapping_labels.tolist()
                a = x.merge(y, on=overlapping_labels, how="inner")
                ins.append(a)
                ins.pop(1)
                ins.pop(0)
                continue
            if len(x.columns.intersection(y.columns)) == 0:
                a = x.join(y)
                ins.append(a)
                ins.pop(1)
                ins.pop(0)
                continue
        b=1
        while len(z) > 0:
            a = list(z.values())[0]["factor"]
            b *= a.at[0]
            z.pop(list(z.keys())[0])

        return b,ins
    

    def filter_(self, x, y):
        count = 0
        for edge in x:
            if edge not in y:
                count += 1
        return count


    # Function to return the order, takes the graph file and heuristic as input
    def get_order(self, heuristic, query = []):

        # Gets the interaction graph and stores the original version for later comparison
        self.graph = self.bn
        interaction_graph = self.graph.get_interaction_graph()
        original_interaction_graph = self.graph.get_interaction_graph()
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
                        edge_count = self.filter_(node_edges, child_node_edges) +1

                        # If the amount is less than our current best, the child node becomes the new node with the least amount of edges created if it were deleted
                        if edge_count < current_least_edges_count:
                            # print('node:', node, 'has edges:', edge_count)
                            current_least_edges = node
                            current_least_edges_count = edge_count
                            # print('-------------current least edges count = ', current_least_edges_count)

                if current_least_edges == None:
                    # print('NOTHING')
                    current_least_edges = list(interaction_graph.nodes)[0]

                    
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

                                if temp_adjacents[i] == current_adjacent:
                                    continue

                                # Add the edge between these two adjacent nodes
                                else:
                                    self.graph.add_edge(current_adjacent, temp_adjacents[j])
                        
                        # After the edges are added, we can safely delete the node and store it as our (next) node in the order list
                        print(f'deleting node: {min_degree_node}, left: {interaction_graph.nodes}')
                        self.graph.del_var(min_degree_node)
                        order.append(str(min_degree_node))
                    
                    # If there is there is just one adjacent node, it could mean that we've reached the final node, so we add that last node to our order list and return it, stopping the function
                    else:
                        if len(list(interaction_graph.nodes)) == 1:
                            order.extend(list(interaction_graph.nodes))
                            return order

                        # However, in all other cases it just means no edges need to be added as there is only one adjacent node  
                        else:
                            self.graph.del_var(min_degree_node)
                            order.append(str(min_degree_node))

        else:
            print(f'Given heuristic \'{heuristic}\' does not match min-degree or min-fill, exiting..')

