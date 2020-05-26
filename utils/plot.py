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


def create_graphic(file1, file2, file3, file4, file5, file6, index):
    mo_data = read_file(file1)
    moms_data = read_file(file2)
    me_data = read_file(file3)
    jw_data = read_file(file4)
    jw2_data = read_file(file5)
    jw2s_data = read_file(file6)
    mo50 = get_diff_files(mo_data)
    moms50 = get_diff_files(moms_data)
    me50 = get_diff_files(me_data)
    jw50 = get_diff_files(jw_data)
    jw250 = get_diff_files(jw2_data)
    jw2s50 = get_diff_files(jw2s_data)
    pl.figure(int(index) + 1)
    pl.plot(get_name(mo50), get_comp(mo50, 1), 'o-', label="Using Most Occurrences")
    pl.plot(get_name(moms50), get_comp(moms50, 1), 'o-', label="Using Most Occurrences in Minimum Size")
    pl.plot(get_name(me50), get_comp(me50, 1), 'o-', label="Using Most Equilibrated")
    pl.plot(get_name(jw50), get_comp(jw50, 1), 'o-', label="Using Jeroslow Wang")
    pl.plot(get_name(jw250), get_comp(jw250, 1), 'o-', label="Using Jeroslow Wang 2")
    pl.plot(get_name(jw2s50), get_comp(jw2s50, 1), 'o-', label="Using Jeroslow Wang 2 Sided")
    pl.legend()
    pl.savefig(f'50-graphic-{index}.png')


if __name__ == '__main__':
    MO = "./times/most_occurrences.time"
    MOMS = "./times/most_occurrences_minimum_size.time"
    ME = "./times/most_equilibrated.time"
    JW = "./times/jeroslow_wang.time"
    JW2 = "./times/jeroslow_wang_2.time"
    JW2S = "./times/jeroslow_wang_2_sided.time"
    create_graphic(MO, MOMS, ME, JW, JW2, JW2S, "2")

