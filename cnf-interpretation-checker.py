#!/bin/env python3
import sys
import nou_dpll

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

def get_interpretation(interpretation_file):
    for line in open(interpretation_file):
        interpretation = [int(x) for x in line[:-2].split()]
    return interpretation
        
if __name__ == "__main__":

    cnf_file=sys.argv[1]

    formula, num_vars = parse(cnf_file) 

    interpretation = nou_dpll.solve_formula(formula, [], nou_dpll.jeroslow_wang_2_sided)
    print('hola')

    for i in interpretation:
        formula = bcp(formula, i)
    
    if formula:
        print("NOT WORKING")
    else:
        print("UR A FUKING BOSS")
