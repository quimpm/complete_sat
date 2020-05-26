#! /bin/bash
echo 'TIME TABLES-------------------'
TIMEFORMAT=%U
for file in ../cnfs/*
do
    printf "\n$file\n"
    for i in `seq 25`; do
      echo -n $(time python3 ../nou_dpll.py $file | grep user)
    done
done
