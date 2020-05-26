#!/bin/bash
for i in 75 100 125 150 175 200 220 280 300 320 330 340 350; do
  ./rnd-cnf-gen.py 75 $i 3 > cnfs/exemple-75-$i.cnf
done

