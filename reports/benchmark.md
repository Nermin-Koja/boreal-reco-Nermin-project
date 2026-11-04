# Apriori Benchmark Report

## 1. Objective

The purpose of this benchmark is to compare Apriori performance using different minimum support thresholds and to evaluate the effect of the `low_memory` option.

The benchmark measures:
- Number of frequent itemsets.
- Number of association rules.
- Execution time.
- Sampled peak process memory (RSS).
- Peak Python-traced memory using `tracemalloc`.

## 2. Benchmark Results

All measurements below come from the latest successful notebook execution.

| Apriori mode | Minimum support | Frequent itemsets | Association rules | Execution time (seconds) | Sampled peak RSS (MB) | Peak traced memory (MB) |
|---|---:|---:|---:|---:|---:|---:|
| Default | 0.05 | 191 | 370 | 38.89 | 7300.61 | 8689.47 |
| Low memory | 0.05 | 191 | 370 | 3.98 | 263.26 | 217.93 |
| Low memory | 0.02 | 658 | 3,746 | 7.49 | 322.65 | 262.34 |
| Low memory | 0.01 | 2,267 | 16,096 | 18.58 | 321.70 | 262.31 |
| Low memory | 0.005 | 7,106 | 63,662 | 51.72 | 323.58 | 262.32 |


## 3. Memory Measurement Method

Two memory measurement methods were used:

- **Sampled peak RSS:** Measured with `psutil` by monitoring the Python process's resident memory (RSS) during execution.
- **Peak Python-traced memory:** Measured with Python's `tracemalloc` module using the peak traced memory value.

RSS measures the memory used by the process, while `tracemalloc` measures memory allocations tracked by Python. The two measurements provide complementary views of memory usage.