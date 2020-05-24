python3 -m cProfile -o output_profiling ../sat.py ../exemple.cnf
python3 pstats_profiling.py > result_profiling_gsat
