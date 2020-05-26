bench=$1

time for f in  `ls $bench`; do ../nou_dpll.py $bench/$f;done
