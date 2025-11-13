import importlib
import time
import tracemalloc
import gc

# libraries to benchmark
LIBRARIES = [
    "scurrypy",
    "hikari",
    "discord",
    "disnake",
]

def benchmark_import(libname: str):
    """Measure import time, memory delta, and object count."""
    gc.collect()
    tracemalloc.start()

    start_time = time.perf_counter()
    before_objects = len(gc.get_objects())

    try:
        module = importlib.import_module(libname)
    except Exception as e:
        print(f"Failed to import {libname}: {e}")
        return None

    after_objects = len(gc.get_objects())
    mem_current, mem_peak = tracemalloc.get_traced_memory()
    end_time = time.perf_counter()
    tracemalloc.stop()

    return {
        "name": libname,
        "time_ms": (end_time - start_time) * 1000,
        "mem_mb": mem_current / 1024 / 1024,
        "objects": after_objects - before_objects,
    }


print(f"{'Library':<12} {'Time (ms)':>12} {'Memory Δ (MB)':>16} {'Objects':>12}")
print("-" * 56)

results = []
for lib in LIBRARIES:
    result = benchmark_import(lib)
    if result:
        results.append(result)
        print(
            f"{result['name']:<12} "
            f"{result['time_ms']:>12.1f} "
            f"{result['mem_mb']:>16.2f} "
            f"{result['objects']:>12}"
        )
