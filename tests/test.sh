#!/bin/bash


solver="../nou_dpll.py"

> given_output
for file in `ls bench`;do ./$solver bench/$file >> given_output;done

diff expected_output given_output
