# Apriori Performance Benchmark

## 1. Purpose

This benchmark compares different Apriori configurations on the Boréal Marché transaction dataset.

It evaluates how the `low_memory` parameter and minimum support threshold affect:

- The number of frequent itemsets.
- Execution time.
- Sampled memory usage.

## 2. Dataset

The experiments used:

- 1,000,000 unique shopping baskets.
- 98 unique products.
- 8,379,837 basket-product records.

## 3. Benchmark Results

The values below are taken from the latest successful execution of `notebooks/01_mining.ipynb`.

| Apriori mode | Minimum support | Frequent itemsets | Execution time (seconds) | Sampled peak RSS (MB) | Outcome |
|---|---:|---:|---:|---:|---|
| Default (`low_memory=False`) | 0.05 | 191 | 74.11 | 5,659.84 | Completed successfully |
| `low_memory=True` | 0.05 | 191 | 4.77 | 274.17 | Completed successfully; same itemsets as default |
| `low_memory=True` | 0.02 | 658 | 11.23 | 318.59 | Completed successfully |
| `low_memory=True` | 0.01 | 2,267 | 39.68 | 307.38 | Completed successfully |
| `low_memory=True` | 0.005 | 7,106 | 77.88 | 319.99 | Completed successfully |

**Association-rule counts:** The latest notebook benchmark records frequent-itemset counts for these five experiments, but it does not record a separate association-rule count for each benchmark configuration. These counts are therefore not reported rather than estimated or invented. The notebook separately reports association-rule counts for the seasonal experiments.

## 4. Key Findings

### 4.1 Effect of `low_memory`

At minimum support 0.05, both configurations generated exactly 191 frequent itemsets.

Compared with the default configuration, `low_memory=True`:

- Reduced sampled peak RSS from 5,659.84 MB to 274.17 MB.
- Used approximately 95.2% less sampled peak RSS.
- Reduced execution time from 74.11 seconds to 4.77 seconds.
- Was approximately 15.5 times faster.

Both configurations completed successfully. The default run did not produce a `MemoryError`.

These results show that `low_memory=True` was substantially more efficient in this environment while producing the same frequent itemsets at support 0.05.

### 4.2 Effect of Minimum Support

As the minimum support threshold decreases, the algorithm discovers more frequent itemsets:

- Support 0.05: 191 itemsets.
- Support 0.02: 658 itemsets.
- Support 0.01: 2,267 itemsets.
- Support 0.005: 7,106 itemsets.

The lowest threshold took the longest among the low-memory runs, at 77.88 seconds.

Lower thresholds reveal less frequent product combinations but increase computational work.

## 5. Measurement Method

- Execution time was measured in seconds using the notebook's timer.
- The Python process's Resident Set Size (RSS) was sampled every 0.05 seconds.
- The reported memory value is the highest sampled RSS during each run.
- This is a sampled peak, not a guaranteed absolute operating-system peak.
- Measurements may vary between runs depending on the machine's available resources and background activity.

## 6. Recommendation and Conclusion

For this dataset and environment, `low_memory=True` is the more efficient Apriori configuration.

At minimum support 0.05, it produced the same 191 frequent itemsets as the default configuration, with approximately 95.2% less sampled peak RSS and a runtime approximately 15.5 times faster.

The main recommendation engine uses minimum support **0.05**, which generated 191 frequent itemsets in the benchmark. The exported recommendation rules are filtered using `lift > 1`.

A minimum support of **0.02** was also evaluated and used for the seasonal mining experiments. This lower threshold generated 658 frequent itemsets in the benchmark.

The benchmark demonstrates the trade-off between discovering more product combinations and computational efficiency.

### Remaining Benchmark Detail

The course benchmark specification asks for the number of association rules at each support threshold.

The latest notebook output does not contain those five counts. They must be obtained from the corresponding frequent-itemset results before this benchmark can be considered fully complete.

No association-rule counts have been fabricated or estimated.

---

**Project:** Boréal Marché — Grocery Recommendation Engine  
**Author:** Nermin Koja  
**Algorithm:** Apriori  
**Course:** 420-975-VA — Unsupervised Learning  
**Semester:** Fall 2026