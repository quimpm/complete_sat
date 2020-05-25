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

    variable = jeroslow_wang(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])

    return solution

def most_occurrences(formula):
    apparences={}
    for clause in formula:
        for literal in clause:
            if literal in apparences:
                apparences[literal] += 1
            else:
                apparences[literal] = 1
    return max(apparences, key=apparences.get)

def most_occurrences_minimum_size(formula):
    minimum_size_clauses = len(min(formula, key = lambda x : len(x)))
    clausues_with_minimum_size = []
    for clause in formula:
        if len(clause) == minimum_size_clauses:
            clausues_with_minimum_size.append(clause)
    return most_occurrences(clausues_with_minimum_size)

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

