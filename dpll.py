#!/usr/bin/env python3

import random
import sys

def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars = line.split()[2]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars)

def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified

def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def backtracking(formula, assignment):

    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = most_occurrences_minimum_size(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])

    return solution


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

    clauses, n_vars = parse(sys.argv[1])

    solution = backtracking(clauses, [])

    if solution:
        solution += [x for x in range(1, n_vars + 1) if x not in solution and -x not in solution]
        solution.sort(key=abs)
        print('s SATISFIABLE')
        print('v ' + ' '.join([str(x) for x in solution]) + ' 0')
    else:
        print('s UNSATISFIABLE')

if __name__ == '__main__':
     main()

