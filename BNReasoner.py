from typing import Union
from BayesNet import BayesNet


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

    def multi_factor(self, lista):

        while len(lista) > 1:
            x = lista[0]
            y = lista[1]
            new = []
            overlapping_labels = x.columns[:-1].intersection(y.columns[:-1])
            overlapping_labels = overlapping_labels.tolist()
            if x.columns[-1] != "p":
                x.rename(columns={x.columns[-1]: 'p'}, inplace=True)
            if y.columns[-1] != "p":
                y.rename(columns={y.columns[-1]: 'p'}, inplace=True)
            z = x.merge(y, on=overlapping_labels, how="outer")
            z["factor"] = z['p_x'] * z['p_y']
            z = z.drop(['p_x', 'p_y'], axis=1)
            lista.pop(0)
            lista.pop(0)
            lista.append(z)
        return z

    def summing_out(self, cpt, variable):
        df = cpt.drop(variable, axis = 1)
        d = df.columns[-1]
        agg = {d: 'sum'}
        groups = df.columns.to_list()[:-1]
        df_new = df.groupby(groups, as_index=False).aggregate(agg).reindex(columns=df.columns)
        return df_new

    def maxing_out(self, cpt, variable):
        df_other = cpt.loc[cpt.groupby('Sprinkler?')[cpt.columns[-1]].idxmax()].reset_index(drop=True)
        df_other["instantiation"] = f"{variable} =" + df_other[variable].astype(str)
        df_other = df_other.drop(variable, axis =1 )
        return df_other

    def prior_marginals(self, order):
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
    
        for node in self.bn.get_children(start)+self.bn.get_parents(start):
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
                    if path[count+1] in self.bn.get_parents(path[count]): #convergent
                        if path[count] not in given:
                            closed_valve.append(True)
                        else:
                            closed_valve.append(False)
                            
                if path[count] in self.bn.get_parents(node):
                    if path[count+1] in self.bn.get_children(path[count]): #divergent valve
                        if path[count] in given:
                            closed_valve.append(True)
                        else:
                            closed_valve.append(False)
                    if path[count+1] in self.bn.get_parents(path[count]): #sequential
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
    
    
    def pruning(self, x, y, z):

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
        for var in z1:
            for edge_end in self.bn.get_children(var):
                self.bn.del_edge([var, edge_end])

                
        return self