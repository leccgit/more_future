import tracemalloc

tracemalloc.start(10)

import gc

from pympler import muppy, summary, tracker

#

# 打印执行代码前后的引用计数
print(len(gc.get_objects()))
...
print(len(gc.get_objects()))

# 打印执行代码前后的内存使用
snapshot1 = tracemalloc.take_snapshot()
...
snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("[ Top 10 differences ]")
for stat in top_stats[:10]:
    print(stat)

# 打印执行代码前后的内存使用
memory_tracker = tracker.SummaryTracker()
...
memory_tracker.print_diff()
