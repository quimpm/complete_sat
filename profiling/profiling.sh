python3 -m cProfile -o output_profiling ../nou_dpll.py ../estressat_cnf
python3 pstats_profiling.py > result_profiling
