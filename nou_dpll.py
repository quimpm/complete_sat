#!/usr/bin/env python3

import sys
from os import listdir
from os.path import isfile, join

def clean_units(clauses, variable):
    new_clauses = []
    for clause in clauses:
        if variable not in clause:
            if -variable in clause:
                new_clause = [x for x in clause if x != -variable]
                if not new_clause:
                    return -1
                new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
    return new_clauses

def propagate(clauses):
    interpretation = []
    units = [c for c in clauses if len(c) == 1]
    while units:
        first = units[0]
        clauses = clean_units(clauses, first[0])
        interpretation += [first[0]]
        if clauses == -1:
            return -1, []
        if not clauses:
            return clauses, interpretation
        units =  [c for c in clauses if len(c) == 1]
    return clauses, interpretation

def solve_formula(clauses, interpretation):
    clauses, new_interpretation = propagate(clauses)
    interpretation = interpretation + new_interpretation
    if clauses == - 1:
        return []
    if not clauses:
        return interpretation
    variable = jeroslow_wang(clauses)
    solution = solve_formula(clean_units(clauses, variable), interpretation + [variable])
    if not solution:
        solution = solve_formula(clean_units(clauses, -variable), interpretation + [-variable])
    return solution

def parse_cnf(filename):
    clauses = []
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        if line[0] == 'p':
            num_vars = line.split()[2]
        elif line[0] != 'c':
            clauses.append([int(x) for x in line[:-2].split()])
    return clauses, int(num_vars)

def jeroslow_wang(formula, weight=2): # debugging
    counter = {}
    for clause in formula:
        for literal in clause:
            try:
                counter[literal] += weight ** -len(clause)
            except KeyError:
                counter[literal] = weight ** -len(clause)
    return max(counter, key=counter.get)

def main_1():
    clauses, num_vars = parse_cnf(sys.argv[1])
    interpretation = solve_formula(clauses, [])
    
    if interpretation:
        interpretation += [x for x in range(1, num_vars +1) if x not in interpretation and -x not in interpretation]
        interpretation.sort(key=abs)
        print('s SATISFIABLE')
        print('v '+ ' '.join([str(x) for x in interpretation]) + ' 0')
    else:
        print('s UNSATISFIABLE') #2 s'hauria de treure



def main_2():
    folder = sys.argv[1]
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    for cnf in files:
        clauses, num_vars = parse_cnf(folder + "/" + cnf)
        interpretation = solve_formula(clauses, [])
        
        if interpretation:
            interpretation += [x for x in range(1, num_vars +1) if x not in interpretation and -x not in interpretation]
            interpretation.sort(key=abs)
            print('s SATISFIABLE')
            print('v '+ ' '.join([str(x) for x in interpretation]) + ' 0')
        else:
            print('s UNSATISFIABLE') #2 s'hauria de treure

if __name__ == '__main__':
    main_1()



''' 
1   és possible que símplement especificant d'alguna forma que
    aquella clàusula ja no és vàlida en ves de crear-ne tota 
    l'estona pugui donar millors resultats. Podria conflictir
    amb backtracking 

2   retornar directament el UNSATISFIABLE

'''
