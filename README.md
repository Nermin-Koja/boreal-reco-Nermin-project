# Boréal Marché — Grocery Product Recommendation System

**Course:** 420-975-VA — Unsupervised Learning  
**Project:** Individual Project — Association Rules and Apriori  
**Student:** Nermin Koja  
**Professor:** Steve  
**Semester:** Fall 2026

---

## 1. Project Overview

Boréal Marché is a grocery product recommendation system built using association rule mining.

The project analyzes one million shopping baskets to discover products that are frequently purchased together. It uses the Apriori algorithm to identify frequent itemsets and generate association rules.

A Streamlit application allows users to browse a grocery catalogue, create a shopping basket, and receive product recommendations based on the saved association rules.

The application loads precomputed rules from JSON files. It does not run Apriori when a customer uses the application.

## 2. Dataset Description

The project uses a grocery transaction dataset containing:

| Dataset characteristic | Value |
|---|---:|
| Total transactions (baskets) | 1,000,000 |
| Transaction-product rows | 8,379,837 |
| Unique products | 98 |
| Average products per basket | 8.38 |
| Date range | January–December 2026 |

The catalogue contains four fields:

- `Item`: Original French product name.
- `Item_EN`: English product name.
- `Category`: Product category.
- `Price`: Product price.

The transaction dataset contains transaction IDs, dates, customer IDs, and product names.

The most frequently purchased product is **Sac réutilisable (Reusable bag)**, appearing in 900,026 baskets, or approximately 90% of all baskets.

The five rarest products are:

- Foie gras
- Vinaigre balsamique vieilli
- Caviar
- Huile de truffe
- Safran

Their low frequency is important because products appearing in very few baskets may not meet the minimum support threshold used during mining.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- mlxtend
- Apriori algorithm
- Streamlit
- Matplotlib
- psutil
- tracemalloc
- Jupyter Notebook
- JSON

## 4. Project Structure

```text
boreal-reco-Nermin/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── products.csv
│   └── transactions.csv
│
├── models/
│   ├── rules.json
│   └── metadata.json
│
├── notebooks/
│   └── 01_mining.ipynb
│
├── reports/
│   └── benchmark.md
│
├── screenshots/
│
├── README.md
└── requirements.txt
```

The transaction dataset is large. It should be obtained from the course-provided source and placed in the `data/` folder as `transactions.csv`. The raw transaction file should not be committed to GitHub if it exceeds the repository's file-size limit.

## 5. Data Preparation and Catalogue Review

The transaction data was loaded and checked before mining.

The analysis confirmed:

- 1,000,000 unique shopping baskets.
- 8,379,837 transaction-product rows.
- 98 unique catalogue products.
- An average basket size of approximately 8.38 products.
- No duplicate basket-product records were found.

The transaction data was transformed into a Boolean basket representation, where each row represents a basket and each product is represented by a Boolean value indicating whether it was purchased.

### Product catalogue review

The catalogue was reviewed for possible duplicate product entries.

Two similar entries were identified:

- Baguette — $2.99
- Pain baguette rustique — $3.99

These entries were kept separate because their names and prices differ, and the available catalogue information does not establish that they represent the same product.

No confirmed duplicate product pair could be established from the available catalogue information. This is an important data-quality observation rather than an assumption that two different products are duplicates.

### Initial prediction

Before running Apriori, I predicted that **Sac réutilisable (Reusable bag)** could cause difficulties because it appears in approximately 90% of all baskets.

The results supported this prediction. Rules involving this product can have high confidence simply because the product is extremely common, while their lift may remain close to 1.

This demonstrates why confidence should not be interpreted without considering lift.

## 6. Apriori Algorithm and Association Metrics

The project uses the Apriori implementation from:

`mlxtend.frequent_patterns.apriori`

The following minimum support thresholds were tested:

- 0.05
- 0.02
- 0.01
- 0.005

The low-memory option was used for the main mining runs.

### Association rule metrics

**Support:** The proportion of all shopping baskets that contain both the antecedent and consequent products.

**Confidence:** The proportion of baskets containing the antecedent that also contain the consequent.

**Lift:** How much more frequently the products occur together compared with what would be expected if their purchases were independent.

A lift greater than 1 indicates a positive association. A lift equal to 1 indicates no association beyond independence, while a lift below 1 indicates a negative association.

The project focuses on rules with lift greater than 1.

Simple rules, containing one product on each side, were examined separately from rules with multiple products in the antecedent.

## 7. Final Recommendation Rules

The saved recommendation model contains **215 association rules**.

The main saved model uses:

- Minimum support: 0.05
- Minimum lift: Greater than 1
- Saved rules: 215
- Catalogue products: 98
- Products represented in recommendations: 50
- Catalogue coverage: 51.02%

Rules can contain multiple products in their antecedent. The recommendation application checks that all antecedent products are present in the customer's basket before a rule fires.

### Verified example from the saved model

**Charbon de bois (Charcoal) → Saucisses (Sausages)**

| Metric | Value |
|---|---:|
| Support | 7.0764% |
| Confidence | 50.344% |
| Lift | 5.983287 |

This indicates a positive association between charcoal and sausages in the transaction dataset.

The association does not prove that purchasing one product causes the purchase of the other.

## 8. Seasonal Analysis

The seasonal analysis compares:

- **Summer:** June, July, and August.
- **Winter:** December, January, and February.

The same mining approach was applied to each seasonal dataset.

### Seasonal results

| Measure | Summer | Winter |
|---|---:|---:|
| Transactions | 252,474 | 246,965 |
| Frequent itemsets | 985 | 564 |
| Association rules | 8,904 | 2,382 |
| Simple rules | 596 | 478 |

The comparison identified:

- 224 simple rules found only in summer.
- 106 simple rules found only in winter.

For example, the winter analysis identified a strong association between:

**Bouillon à fondue (Fondue broth) → Fromage à raclette (Raclette cheese)**

| Metric | Value |
|---|---:|
| Support | 6.7248% |
| Confidence | 82.9653% |
| Lift | 6.808285 |

This rule was identified in the winter analysis and not in the summer simple-rule results.

A rule absent from one seasonal result may have fallen below the mining threshold; this does not necessarily mean that the two products were never purchased together.

The dataset covers only one calendar year, so the seasonal patterns should not be treated as proof of a permanent yearly trend.

### Recommendation

The association rules should be reviewed and re-mined regularly. Monthly re-mining is a reasonable recommendation because customer purchasing patterns can change over time.

Using year-round rules without checking their relevance could lead to less useful recommendations during specific seasons.

## 9. Streamlit Recommendation Application

The Streamlit application provides three main areas.

### Zone 1 — Product Catalogue

Users can:

- Browse the 98 catalogue products.
- Search for products.
- Filter by category.
- View product categories and prices.
- Add products to their shopping basket.

### Zone 2 — Shopping Basket

Users can:

- View selected products.
- View categories, quantities, and prices.
- See each product subtotal.
- See the total basket price.
- Remove a selected product.
- Clear the entire basket.

### Zone 3 — Product Recommendations

The recommendation engine:

- Loads the precomputed rules from `models/rules.json`.
- Uses the metadata stored in `models/metadata.json`.
- Checks whether all antecedent products are present in the basket.
- Excludes products already in the basket.
- Removes duplicate suggestions while keeping the rule with the highest lift.
- Sorts recommendations by descending lift.
- Displays up to five recommendations.

Each recommendation includes the product name, category, price, support, confidence, lift, and a strength label.

The application also provides plain-language explanations of the rules.

The expandable **Rules that fired** section makes the recommendation process more transparent.

**Important:** The Streamlit application does not run Apriori. Mining is completed beforehand, and the application uses the saved JSON model.

## 10. Application Edge Cases

The application was designed to handle the following situations:

| Edge case | Expected application behavior |
|---|---|
| Empty basket | Displays a message and popular-product fallback recommendations. |
| No rule matches | Explains that no association rule matched and displays popular alternatives. |
| Product already in basket | Does not recommend a product that is already in the basket. |
| Duplicate recommendations | Keeps the recommendation supported by the highest-lift rule. |
| Rare product | Explains when the product's support is below the mining threshold. |

The application also supports rules with multiple products in the antecedent.

## 11. Benchmark and Performance Analysis

The benchmark compares the default Apriori mode with the low-memory mode at a support threshold of 0.05. It also measures low-memory performance at lower support thresholds.

Two memory measurements were recorded:

- **Sampled peak RSS:** Process memory measured periodically using psutil.
- **Peak traced memory:** Python memory allocations measured using tracemalloc.

These measurements are different and should not be interpreted as interchangeable.

### Benchmark results

| Apriori mode | Support | Itemsets | Rules | Time (seconds) | Sampled peak RSS (MB) | Peak traced memory (MB) |
|---|---:|---:|---:|---:|---:|---:|
| Default | 0.05 | 191 | 370 | 38.89 | 7300.61 | 8689.47 |
| Low memory | 0.05 | 191 | 370 | 3.98 | 263.26 | 217.93 |
| Low memory | 0.02 | 658 | 3,746 | 7.49 | 322.65 | 262.34 |
| Low memory | 0.01 | 2,267 | 16,096 | 18.58 | 321.70 | 262.31 |
| Low memory | 0.005 | 7,106 | 63,662 | 51.72 | 323.58 | 262.32 |

### Benchmark observations

At a support threshold of 0.05, both modes produced the same 191 frequent itemsets and 370 association rules.

The low-memory mode completed in 3.98 seconds, compared with 38.89 seconds for the default mode.

The sampled peak RSS was also substantially lower with low-memory mode.

As the minimum support threshold decreases, the number of frequent itemsets and association rules increases. This also increases the mining time.

The default Apriori run completed successfully. No MemoryError occurred during the benchmark. The high measured memory usage nevertheless makes the low-memory option more practical for this dataset.

The RSS measurement is sampled periodically and may miss short-lived peaks. Tracemalloc measures Python allocations and does not capture every native or NumPy allocation.

For additional benchmark details, see `reports/benchmark.md`.

## 12. Famous Retail Example: Beer and Diapers

The famous Beer-and-Diapers retail example was checked against the actual transaction dataset rather than assumed to be true.

The separate verification produced the following results:

| Measure | Result |
|---|---:|
| Total baskets | 1,000,000 |
| Baskets containing Beer | 150,468 |
| Baskets containing Diapers | 83,966 |
| Baskets containing both | 30,696 |
| Support | 3.0696% |
| Confidence (Beer → Diapers) | 20.4004% |
| Confidence (Diapers → Beer) | 36.5577% |
| Lift | 2.4296 |

The lift of 2.4296 indicates that Beer and Diapers occur together approximately 2.43 times as often as would be expected if their purchases were independent.

This demonstrates a positive association in this dataset. However, correlation or association does not prove causation. We cannot conclude that purchasing Beer causes a customer to purchase Diapers.

**Mining threshold limitation:** The main Apriori analysis uses a minimum support of 5%. The Beer-and-Diapers pair has support of 3.0696%, so it does not appear in the saved recommendation rules. It was verified separately using the original transaction data.

## 13. Ethical Considerations and Limitations

### Explainability

Recommendations are based on historical co-purchases. The application displays support, confidence, and lift so that users can understand why a product was recommended.

The expandable Rules that fired section provides additional transparency.

### Quebec Law 25 and privacy

The project uses transaction data containing customer identifiers. In a real commercial deployment, customer information should be handled responsibly and protected.

A production implementation should apply appropriate privacy safeguards, restrict access to personal information, minimize the data collected and retained, and assess its obligations under Quebec's Law 25 and applicable privacy legislation.

The demonstration application does not need to display individual customer identities to generate product recommendations.

### Reinforcement bias

Frequently purchased products may continue to be recommended more often because they already appear frequently in historical transactions.

This can reinforce existing purchasing patterns and reduce exposure to less common products.

### Coverage limitation

The saved recommendation model covers 50 of the 98 catalogue products, or approximately 51.02%.

Some rare products do not meet the minimum support threshold and therefore may not participate in the saved rules.

### Seasonal limitation

The dataset contains only one year of transactions. Seasonal results may not represent long-term purchasing behavior.

### Association is not causation

Association rules identify patterns in historical purchases. They do not explain why customers buy products together and cannot establish causal relationships.

## 14. Installation and Execution

### Requirements

The project dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Run the mining notebook

Open:

```text
notebooks/01_mining.ipynb
```

Ensure the course-provided transaction data is available in the `data/` directory before running the notebook.

### Run the Streamlit application

From the project root directory:

```bash
streamlit run app/streamlit_app.py
```

The application loads the saved rules and metadata from the `models/` directory.

Apriori does not run when the application starts.

## 15. Screenshots

The `screenshots/` directory contains 14 screenshots documenting the project, including:

- Product catalogue.
- Shopping basket.
- Product recommendations.
- Rules that fired.
- Empty-basket behavior.
- No-matching-rule behavior.
- Rare-product explanation.
- Notebook data preparation.
- Product frequency analysis.
- Apriori benchmark comparison.
- Top 10 association rules by lift.
- Top 10 association rules by confidence.
- Seasonal comparison.
- Winter-only and summer-only rules.

These screenshots demonstrate the mining analysis, recommendation application, and its behavior in different scenarios.

## 16. Conclusion

This project demonstrates how association rule mining can be used to discover purchasing patterns and build a grocery recommendation system.

The Apriori algorithm identified frequent product combinations, while support, confidence, and lift helped evaluate the usefulness of the resulting rules.

The seasonal analysis showed that associations can differ across periods. Benchmarking demonstrated the practical advantage of low-memory Apriori for this dataset.

Finally, the Streamlit application uses precomputed rules to provide explainable recommendations without repeating the mining process.

The project also highlights important limitations involving rare products, catalogue coverage, seasonal variation, privacy, reinforcement bias, and the difference between association and causation.