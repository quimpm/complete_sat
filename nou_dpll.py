#!/usr/bin/env python3

import sys


def parse_cnf(filename):
    clauses = []
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    for line in content:
        if line[0] == 'p':
            num_vars = line.split()[2]
        elif line[0] != 'c':
            clauses.append([int(x) for x in line[:-2].split()])
    return clauses, int(num_vars)

def main():
    clauses, num_vars = parse_cnf(sys.argv[1])
    print(clauses)
    print(num_vars)



if __name__ == '__main__':
    main()
