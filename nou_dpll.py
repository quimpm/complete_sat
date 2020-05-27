#!/usr/bin/env python3

import sys
import random

def clean_units_1(clauses, variable):
    index = []
    deletions = 0
    for i,clause in enumerate(clauses):
        if variable in clause:
            index.append(i)
        elif -variable in clause:
            if len(clauses[i]) == 1:
                return -1
            clauses[i].remove(-variable)

    for i in index:
        del clauses[i-deletions]
        deletions += 1
    return clauses

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

def solve_formula(clauses, interpretation, heuristic):
    clauses, new_interpretation = propagate(clauses)
    interpretation = interpretation + new_interpretation
    if clauses == - 1:
        return []
    if not clauses:
        return interpretation
    variable = heuristic(clauses)
    solution = solve_formula(clean_units(clauses, variable), interpretation + [variable], heuristic)
    if not solution:
        solution = solve_formula(clean_units(clauses, -variable), interpretation + [-variable], heuristic)
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



def get_literal_aparences(formula):
    apparences={}
    for clause in formula:
        for literal in clause:
            if literal in apparences:
                apparences[literal] += 1
            else:
                apparences[literal] = 1
    return apparences

def most_occurrences(formula):
    apparences = get_literal_aparences(formula)
    return max(apparences, key=apparences.get)

def get_most_apeared_literals(apparences):
    most_apeared = []
    bigest_num_of_apparences = 0
    for key,value in apparences.items():
        if value == bigest_num_of_apparences:
            most_apeared.append(key)
        if value > bigest_num_of_apparences:
            most_apeared = []
            most_apeared.append(key)
            bigest_num_of_apparences = value
    if bigest_num_of_apparences == 0:
        return [random.choice(most_apeared)]
    else:
        return most_apeared
        
def get_clauses_with_size(formula, size):
    clausues_with_size = []
    for clause in formula:
        if len(clause) == size:
            clausues_with_size.append(clause)
    return clausues_with_size

def tiebraker(most_apeared, formula, size):
    while len(most_apeared) > 1:
        size += 1
        clauses_with_size = get_clauses_with_size(formula, size)
        apparences = get_literal_aparences(clauses_with_size)
        apparences_in_bigger_clauses={} 
        for literal in most_apeared:
            if literal in apparences:
                apparences_in_bigger_clauses[literal] = apparences[literal]
            else:
                apparences_in_bigger_clauses[literal] = 0
        most_apeared = get_most_apeared_literals(apparences_in_bigger_clauses)
    return most_apeared[0]

def most_occurrences_minimum_size(formula):
    minimum_size_clauses = len(min(formula, key = lambda x : len(x)))
    clausues_with_minimum_size = get_clauses_with_size(formula, minimum_size_clauses)
    apparences = get_literal_aparences(clausues_with_minimum_size)
    most_apeared = get_most_apeared_literals(apparences)
    if len(most_apeared) > 1:
        final_literal = tiebraker(most_apeared, formula, minimum_size_clauses)
    else:
        final_literal = most_apeared[0]
    return final_literal

def most_equilibrated(formula):
    apparences={}
    for clause in formula:
        for literal in clause:
            if literal in apparences:
                apparences[literal][0] += 1
            elif -literal in apparences:
                apparences[-literal][1] += 1
            else:
                apparences[literal] = [1,0]
    return max(apparences, key = lambda x : apparences[x][0] * apparences[x][1])

def jeroslow_wang(formula, weight = 2):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return max(counter, key=counter.get)

def jeroslow_wang_2(formula, weight = 2):
    counter = {}
    for clause in formula:
        for literal in clause:
            try:
                counter[literal] += weight ** -len(clause)
            except KeyError:
                counter[literal] = weight ** -len(clause)
    return max(counter, key=counter.get)

def jeroslow_wang_2_sided(formula, weight = 2):
    counter = {}
    for clause in formula:
        for literal in clause:
            if abs(literal) in counter:
                counter[abs(literal)] += weight ** -len(clause)
            else:
                counter[abs(literal)] = weight ** -len(clause)
    return max(counter, key=counter.get)

def main():
    heuristic_1 = most_occurrences
    heuristic_2 = most_occurrences_minimum_size
    heuristic_3 = most_equilibrated
    heuristic_4 = jeroslow_wang
    heuristic_5 = jeroslow_wang_2
    heuristic_6 = jeroslow_wang_2_sided

    clauses, num_vars = parse_cnf(sys.argv[1])
    interpretation = solve_formula(clauses, [], heuristic_6)
    
    if interpretation:
        interpretation += [x for x in range(1, num_vars +1) if x not in interpretation and -x not in interpretation]
        interpretation.sort(key=abs)
        print('s SATISFIABLE')
        print('v '+ ' '.join([str(x) for x in interpretation]) + ' 0')
    else:
        print('s UNSATISFIABLE')

if __name__ == '__main__':
    main()
