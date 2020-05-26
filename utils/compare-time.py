#!/usr/bin/env python3
import matplotlib.pyplot as pl
from functools import reduce
import re


def get_file_data(lines):
    name = lines[0].split('/')[-1][:-1]
    time = []
    for l in lines[1:]:
        l = l[:-1]
        if not l:
            return name, reduce(lambda x, y: x + y, time) / 25
        l = l.replace(',', '.')
        time.append(float(l))
    return name, reduce(lambda x, y: x + y, time) / 25


def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()[2:]
    res = []
    while lines:
        name, mean = get_file_data(lines)
        lines = lines[27:]
        res.append([name, mean])
    return res


def get_diff_files(all_data):
    d50 = list(filter(lambda x: re.search('^exemple-50*',x[0]), all_data))
    return d50


def get_name(data):
    return list(map(lambda x: x[0].split('-')[2][:-4], data))

def get_comp(data, i):
    return list(map(lambda x: x[i], data))


def create_graphic(heuristics, index):
    for heuristic in heuristics:
        heuristic_data = read_file(file1)
        da50 = get_diff_files(heuristic_data)
        pl.figure(int(index) + 1)
        name = heuristics.split("/.")
        pl.plot(get_name(da50), get_comp(da50, 1), 'o-', label="Using: "+name)
        pl.legend()
        pl.savefig(name+'.png')


if __name__ == '__main__':
    MO = "./heuristics_time/most_occurrences.time"
    MOMS = "./heuristics_time/most_occurrences_minimum_size.time"
    ME = "./heuristics_time/most_equilibrated.time"
    JW = "./heuristics_time/jeroslow_wang.time"
    JW2S = "./heuristics_time/jeroslow_wang.time"
    heuristics = [MO, MOMS, ME, JW, JW2S]
    create_graphic(heuristics "2")

