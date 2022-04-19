import filecmp
f1 = "/Users/leichao/study/more_future/effective_python/20_mate_code/evalsupport.py"
f2 = "/Users/leichao/study/more_future/effective_python/20_mate_code/evaltime.py"

result = filecmp.cmp(f1, f2,shallow=False)
print(result)