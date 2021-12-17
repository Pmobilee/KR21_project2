from typing import Union
from BayesNet import BayesNet
import pandas as pd
from copy import deepcopy
import random


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

    def order(self, heuristic, query):
        variables = self.bn.get_all_variables()
        if "p" in variables:
            self.bn.del_var('p')
            variables = self.bn.get_all_variables()
        for item in query:
            variables.remove(item)
        if heuristic == "random":
            random.shuffle(variables)
            order = variables
            order.extend(query)

        return order


    def multi_factor(self, lista):
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
        return lista[0]

    def summing_out(self, cpt, variable):
        df = cpt.drop(variable, axis = 1)
        d = df.columns[-1]
        agg = {d: 'sum'}
        groups = df.columns.to_list()[:-1]
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
        if row == len(cpt.index):
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

    def posterior_marginals(self, order: list, evidence):
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

            factor = self.summing_out(self.multi_factor(mention), variable)
            for s in mention_keys:
                thing.pop(s)
            sum = factor["factor"].sum()
            factor["factor"] = factor["factor"].values / sum
            nm = ' '.join(mention_keys)
            name = f"Sigma {variable} factor {nm}"
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
        z = self.bn.get_all_cpts()
        order = self.order(heuristic, query)
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
                print('yes')
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
