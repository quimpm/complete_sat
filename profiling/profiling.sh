python3 -m cProfile -o output_profiling ../dpll.py ../estressat_cnf/estresSAT_4.cnf
python3 pstats_profiling.py > result_profiling
