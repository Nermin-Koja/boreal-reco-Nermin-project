# Boréal Marché — Grocery Recommendation Engine

**Individual Project by Nermin Koja**  
**Course:** 420-975-VA — Unsupervised Learning  
**Professor:** Steve  
**Semester:** Fall 2026  
**Submission Date:** November 4, 2026

---

## 1. Project Overview

Boréal Marché is a grocery recommendation engine that suggests products to customers based on the items already in their shopping baskets.

The project uses Association Rule Mining and the Apriori algorithm to discover relationships between products frequently purchased together.

The goal is to help customers discover relevant products while providing transparent explanations of why each product is recommended.

This is an individual project developed using the course datasets and Python-based data mining tools.

## 2. Dataset

The project uses the transaction and product catalogue datasets provided for the course.

### Transaction dataset

- 1,000,000 unique shopping baskets.
- 8,379,837 basket-product records.
- 98 unique products.
- Approximately 8.4 products per basket on average.

### Product catalogue

The catalogue contains 98 products, including:

- Product names in French and English.
- Product categories.
- Product prices.

### Product frequency analysis

The exploratory analysis identifies the most frequently purchased products and the five rarest products.

The most frequent product is **Sac réutilisable (Reusable bag)**, appearing in 900,026 baskets, representing approximately 90% of all baskets.

The rarest products include:

- Foie gras
- Vinaigre balsamique vieilli
- Caviar
- Huile de truffe
- Safran

Rare products may not appear in frequent itemsets when minimum support thresholds are applied.

## 3. Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- mlxtend
- Streamlit
- Jupyter Notebook

## 4. Project Structure

The project is organized as follows:

```text
boreal-reco-Nermin/
│
├── data/
│   ├── transactions.csv
│   └── products.csv
│
├── notebooks/
│   └── 01_mining.ipynb
│
├── models/
│   ├── rules.json
│   └── metadata.json
│
├── app/
│   └── streamlit_app.py
│
├── reports/
│   └── benchmark.md
│
├── screenshots/
│
├── README.md
└── requirements.txt
```

## 5. Methodology

The project follows these main steps:

1. Load and inspect the transaction and product datasets.
2. Explore product frequencies and transaction statistics.
3. Convert transactions into a sparse basket-product matrix.
4. Apply the Apriori algorithm to identify frequent itemsets.
5. Generate association rules.
6. Evaluate rules using support, confidence, and lift.
7. Compare seasonal purchasing patterns.
8. Select and export recommendation rules.
9. Build an interactive Streamlit application.

Apriori is the only frequent itemset mining algorithm used in this project.

## 6. Association Rule Mining

The Apriori algorithm identifies products that frequently appear together in shopping baskets.

Three main metrics are used to evaluate association rules:

- **Support:** How frequently the products in a rule appear together across all baskets.
- **Confidence:** How often the consequent product appears when the antecedent products are present.
- **Lift:** How much stronger the association is compared with what would be expected from the consequent product's normal frequency.

### Final recommendation rule selection

The main recommendation engine uses:

- Minimum support: `0.05`
- Minimum lift: `1.0`
- Lift filter: `lift > 1`

The exported recommendation rules contain:

- 215 association rules.
- Single-product consequents.
- Antecedents that may contain multiple products.

This allows the application to recommend a product based on either one product or a combination of products already in the basket.

## 7. Performance Benchmarking

Different minimum support values were evaluated using Apriori with `low_memory=True`.

The default Apriori execution was also compared with the low-memory implementation.

| Configuration | Minimum support | Frequent itemsets | Time (seconds) | Sampled peak RSS (MB) |
|---|---:|---:|---:|---:|
| Default | 0.05 | 191 | 74.11 | 5659.84 |
| Low memory | 0.05 | 191 | 4.77 | 274.17 |
| Low memory | 0.02 | 658 | 11.23 | 318.59 |
| Low memory | 0.01 | 2,267 | 39.68 | 307.38 |
| Low memory | 0.005 | 7,106 | 77.88 | 319.99 |

The benchmark shows that `low_memory=True` substantially reduced the sampled peak memory usage and execution time at minimum support 0.05.

Lower support thresholds produced more frequent itemsets and required more processing time.

The benchmark results demonstrate the trade-off between discovering more product combinations and computational efficiency.

## 8. Seasonal Analysis

The project compares purchasing patterns across summer and winter.

Separate association rules were generated to identify seasonal differences in product combinations.

### Seasonal results

| Metric | Summer | Winter |
|---|---:|---:|
| Shopping baskets | 252,474 | 246,965 |
| Frequent itemsets | 985 | 564 |
| Association rules | 8,904 | 2,382 |
| Simple rules | 596 | 478 |

The analysis identified:

- 224 rules found only in summer.
- 106 rules found only in winter.

### Examples of seasonal associations

**Summer:**

Charcoal → Sausages

- Support: 14.38%
- Confidence: 53.32%
- Lift: 3.44

**Winter:**

Raclette cheese → Fondue broth

- Support: 6.72%
- Confidence: 55.19%
- Lift: 6.81

These examples illustrate how purchasing associations can differ between seasons.

The absence of a rule from a seasonal result does not necessarily mean the association never occurs; it may simply fall below the selected support threshold.

## 9. Recommendation Engine

The selected recommendation rules are saved in:

```text
models/rules.json
```

The model metadata is saved in:

```text
models/metadata.json
```

### Exported model information

| Description | Value |
|---|---:|
| Association rules | 215 |
| Unique recommended products | 50 |
| Total catalogue products | 98 |
| Recommendation coverage | 51.02% |
| Minimum support | 0.05 |
| Minimum lift | 1.0 |

Recommendation coverage represents the proportion of catalogue products that can appear as recommended products in the exported rules.

The application loads the saved rules instead of running Apriori every time a customer changes their basket.

## 10. Streamlit Application

The interactive application allows customers to:

- Browse the grocery product catalogue.
- Search for products.
- Filter products by category.
- Add products to a shopping basket.
- View basket products, prices, and categories.
- Remove products from the basket.
- Clear the basket.
- View the basket total.
- Receive product recommendations based on basket contents.
- View recommendation confidence and lift.
- Understand why a product was recommended.

### Recommendation logic

The application:

1. Checks the products currently in the shopping basket.
2. Finds rules whose antecedents are all present in the basket.
3. Excludes products already in the basket.
4. Keeps the strongest rule when multiple rules recommend the same product.
5. Ranks recommendations by lift.
6. Displays up to five recommendations with their metrics and explanations.

The application supports multi-product antecedents and explains the products that triggered each recommendation.

## 11. Edge Cases and Application Behavior

The application is designed to handle several situations:

| Situation | Expected behavior |
|---|---|
| Empty basket | Displays a fallback message. |
| No recommendation rule fires | Displays a fallback message. |
| Recommended product already in basket | Excludes that product. |
| Multiple rules recommend the same product | Keeps the strongest rule. |
| Rare product has no matching rule | Explains that no recommendation is available. |

These cases help make the recommendation engine more reliable and understandable.

## 12. How to Run the Application

### Step 1 — Open the project directory

Open a terminal in the main project directory:

```bash
cd path/to/boreal-reco-Nermin
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Launch Streamlit

```bash
streamlit run app/streamlit_app.py
```

Streamlit will provide a local address in the terminal. Open that address in a web browser to use the application.

### Required files

Before launching the application, make sure the following files are present:

- `data/products.csv`
- `models/rules.json`
- `models/metadata.json`
- `app/streamlit_app.py`
- `requirements.txt`

## 13. Limitations and Ethical Considerations

### Association does not mean causation

Association Rule Mining identifies products that frequently occur together. It does not prove that purchasing one product causes a customer to purchase another.

A famous retail example often discussed in data mining is the association between diapers and beer. Such associations illustrate patterns in purchasing behavior, not causal relationships.

### Recommendation coverage

The exported rules cover 50 of the 98 catalogue products.

Products that do not appear as consequents in the selected rules cannot be recommended by this version of the engine.

### Popularity and recommendation bias

Frequently purchased products may appear in many association rules.

This can create popularity bias, where common products receive more recommendation opportunities than less frequently purchased products.

### Seasonal limitations

The seasonal analysis uses the available 2026 dataset. The seasonal results should not automatically be interpreted as long-term purchasing trends.

Additional years of data would help evaluate whether these patterns repeat.

### Privacy and Quebec Law 25

The project uses transaction and product data provided for the course.

In a real commercial deployment, customer data should be handled responsibly, with appropriate privacy safeguards, access controls, and transparency in accordance with applicable privacy requirements, including Quebec's Law 25 where applicable.

## 14. Reproducibility

The project separates the mining process from the recommendation application.

The Jupyter Notebook contains the data preparation, exploration, Apriori mining, association rule generation, and analysis.

The exported JSON files allow the Streamlit application to load the selected recommendation rules and metadata without repeating the mining process.

The dependency list is provided in `requirements.txt`.

## 15. Conclusion

Boréal Marché demonstrates how Association Rule Mining and the Apriori algorithm can be used to discover meaningful product relationships in grocery transactions.

The project combines data exploration, frequent itemset mining, association rule evaluation, seasonal analysis, performance benchmarking, and an interactive recommendation application.

By displaying recommendation metrics and explanations, the application provides a transparent way to explore product associations and support grocery shopping decisions.

---

**Project:** Boréal Marché — Grocery Recommendation