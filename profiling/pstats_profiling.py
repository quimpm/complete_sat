import pstats
p = pstats.Stats('output_profiling')
p.strip_dirs().sort_stats(-1).print_stats()
