# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 17:05:26 2021

@author: Pablo
"""

def find_all_paths(net, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in net.get_all_variables():
        return []
    paths = []
    
    #Recursive function to search through all the possible paths.
    #Search through all parents and children of each variable,
    #If the end is not there, start search for each of these variables
    #until the end is found
    
    for node in net.get_children(start)+net.get_parents(start):
        if node not in path:
            newpaths = find_all_paths(net, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths
    
def d_separation(net, start, given, end):
    
    paths = find_all_paths(net, start, end)
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
            if path[count] in net.get_children(node):
                if path[count+1] in net.get_children(path[count]): #sequential valve
                    if path[count] in given:
                        closed_valve.append(True)
                    else:
                        closed_valve.append(False)
                if path[count+1] in net.get_parents(path[count]): #convergent
                    if path[count] not in given:
                        closed_valve.append(True)
                    else:
                        closed_valve.append(False)
                        
            if path[count] in net.get_parents(node):
                if path[count+1] in net.get_children(path[count]): #divergent valve
                    if path[count] in given:
                        closed_valve.append(True)
                    else:
                        closed_valve.append(False)
                if path[count+1] in net.get_parents(path[count]): #sequential
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