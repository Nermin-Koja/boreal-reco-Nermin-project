import json
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 1. Configure the application
# ---------------------------------------------------------
st.set_page_config(
    page_title="Boréal Marché",
    page_icon="🛒",
    layout="wide"
)

st.title("Boréal Marché")
st.subheader("Smart Grocery Recommendation Engine")

# ---------------------------------------------------------
# 2. Load saved files (the app does not run Apriori)
# ---------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
products = pd.read_csv(ROOT / "data" / "products.csv")

with open(ROOT / "models" / "rules.json", "r", encoding="utf-8") as file:
    rules = json.load(file)

with open(ROOT / "models" / "metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)

product_by_item = products.set_index("Item").to_dict("index")
english_by_item = products.set_index("Item")["Item_EN"].to_dict()

st.caption(
    f"Products loaded: {len(products)}  |  "
    f"Recommendation rules loaded: {len(rules)}  |  "
    f"Mining date: {metadata.get('mining_date', 'Not recorded')}"
)

# ---------------------------------------------------------
# 3. Helper functions
# ---------------------------------------------------------
def display_name(item):
    return english_by_item.get(item, item)


def lift_strength(lift):
    if lift < 1.5:
        return "Weak"
    if lift < 3:
        return "Moderate"
    if lift < 5:
        return "Strong"
    return "Very strong"


def popular_fallback(excluded_items, limit=5):
    """Return popular catalogue products, excluding basket items."""
    fallback = []
    for item in metadata.get("popular_products", []):
        item_name = item.get("Item")
        if item_name and item_name not in excluded_items:
            fallback.append(item)
        if len(fallback) >= limit:
            break
    return fallback


def product_table_rows(items):
    rows = []
    for item in items:
        info = product_by_item.get(item, {})
        rows.append({
            "Product": info.get("Item_EN", item),
            "Category": info.get("Category", "Unknown"),
            "Price": float(info.get("Price", 0))
        })
    return rows


# ---------------------------------------------------------
# 4. Product catalogue
# ---------------------------------------------------------
st.header("🛒 Product Catalogue")
st.write("Browse the 98 products, filter by category, and add products to your basket.")

search_query = st.text_input(
    "Search for a product",
    placeholder="Example: Chicken, cheese, bread..."
)

categories = ["All categories"] + sorted(
    products["Category"].dropna().unique().tolist()
)
selected_category = st.selectbox("Filter by category", categories)

filtered_products = products.copy()

if search_query:
    filtered_products = filtered_products[
        filtered_products["Item_EN"].str.contains(
            search_query, case=False, na=False
        )
    ]

if selected_category != "All categories":
    filtered_products = filtered_products[
        filtered_products["Category"] == selected_category
    ]

st.write("Products found:", len(filtered_products))
st.dataframe(
    filtered_products[["Item_EN", "Category", "Price"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Price": st.column_config.NumberColumn("Price", format="$%.2f")
    }
)

# ---------------------------------------------------------
# 5. Shopping basket
# ---------------------------------------------------------
st.header("🧺 Your Shopping Basket")

if "basket" not in st.session_state:
    # Keys are the original Item values used by the rules.
    st.session_state.basket = {}

available_items = products["Item"].dropna().tolist()
basket_product = st.selectbox(
    "Choose a product to add",
    available_items,
    format_func=display_name
)

basket_quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

if st.button("Add to basket"):
    st.session_state.basket[basket_product] = (
        st.session_state.basket.get(basket_product, 0)
        + int(basket_quantity)
    )
    st.success(f"{display_name(basket_product)} added to your basket.")

basket_items = set(st.session_state.basket.keys())

if basket_items:
    basket_rows = []
    for item, quantity in st.session_state.basket.items():
        info = product_by_item.get(item, {})
        unit_price = float(info.get("Price", 0))
        basket_rows.append({
            "Product": info.get("Item_EN", item),
            "Category": info.get("Category", "Unknown"),
            "Quantity": quantity,
            "Unit price": unit_price,
            "Subtotal": unit_price * quantity
        })

    basket_table = pd.DataFrame(basket_rows)
    st.dataframe(
        basket_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Unit price": st.column_config.NumberColumn(
                "Unit price", format="$%.2f"
            ),
            "Subtotal": st.column_config.NumberColumn(
                "Subtotal", format="$%.2f"
            )
        }
    )
    st.metric(
        "Basket total",
        f"${basket_table['Subtotal'].sum():,.2f}"
    )

    remove_col, clear_col = st.columns(2)
    with remove_col:
        item_to_remove = st.selectbox(
            "Choose a product to remove",
            list(st.session_state.basket.keys()),
            format_func=display_name,
            key="remove_product"
        )
        if st.button("Remove selected product"):
            del st.session_state.basket[item_to_remove]
            st.rerun()

    with clear_col:
        st.write("")
        st.write("")
        if st.button("Clear entire basket"):
            st.session_state.basket.clear()
            st.rerun()
else:
    st.info("Your basket is empty. Add products to receive recommendations.")

# ---------------------------------------------------------
# 6. Recommendation engine
# ---------------------------------------------------------
st.header("⭐ Recommended Products")

if not basket_items:
    # Edge case 1: empty basket -> popular-product fallback.
    st.write("Your basket is empty, so here are popular products to get started.")
    popular = popular_fallback(set(), limit=5)
    if popular:
        st.dataframe(
            pd.DataFrame([
                {
                    "Product": p.get("Item_EN", p.get("Item")),
                    "Category": p.get("Category", "Unknown"),
                    "Price": float(p.get("Price", 0))
                }
                for p in popular
            ]),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Price": st.column_config.NumberColumn(
                    "Price", format="$%.2f"
                )
            }
        )
    else:
        st.info("No popular-product fallback is available yet.")

else:
    matching_rules = []
    best_rule_for_product = {}

    # A rule fires only when EVERY antecedent product is in the basket.
    for rule in rules:
        antecedents = set(rule.get("antecedents", []))
        consequent = rule.get("consequent")

        if (
            antecedents
            and antecedents.issubset(basket_items)
            and consequent
            and consequent not in basket_items
        ):
            matching_rules.append(rule)

            # Edge case 4: keep the highest-lift rule for duplicate suggestions.
            current_best = best_rule_for_product.get(consequent)
            if current_best is None or rule["lift"] > current_best["lift"]:
                best_rule_for_product[consequent] = rule

    if best_rule_for_product:
        ranked_rules = sorted(
            best_rule_for_product.values(),
            key=lambda rule: rule["lift"],
            reverse=True
        )[:5]

        recommendation_rows = []
        for rule in ranked_rules:
            info = rule.get("consequent_info", {})
            recommendation_rows.append({
                "Recommended product": info.get(
                    "Item_EN", display_name(rule["consequent"])
                ),
                "Category": info.get("Category", "Unknown"),
                "Price": float(info.get("Price", 0)),
                "Support (%)": round(rule["support"] * 100, 2),
                "Confidence (%)": round(rule["confidence"] * 100, 1),
                "Lift": round(rule["lift"], 2),
                "Strength": lift_strength(rule["lift"])
            })

        st.write("Recommendations are ranked by lift (highest first).")
        st.dataframe(
            pd.DataFrame(recommendation_rows),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Price": st.column_config.NumberColumn(
                    "Price", format="$%.2f"
                )
            }
        )

        st.subheader("Why are these products recommended?")
        for rule in ranked_rules:
            antecedent_names = [
                display_name(item) for item in rule["antecedents"]
            ]
            antecedent_text = " and ".join(antecedent_names)
            consequent_name = display_name(rule["consequent"])
            confidence_percent = rule["confidence"] * 100
            lift_value = rule["lift"]
            support_percent = rule["support"] * 100
            strength = lift_strength(lift_value)

            with st.expander(f"{consequent_name} — recommendation details"):
                st.write(
                    f"Because your basket contains **{antecedent_text}**, "
                    f"customers who buy those also buy **{consequent_name}** "
                    f"{confidence_percent:.1f}% of the time — "
                    f"that is **{lift_value:.2f}×** more often than average."
                )
                st.write(f"**Association strength:** {strength}")
                st.write(f"**Support:** {support_percent:.2f}%")
                st.write(f"**Confidence:** {confidence_percent:.1f}%")
                st.write(f"**Lift:** {lift_value:.2f}")
                st.caption(
                    "Association does not prove that buying one product causes "
                    "customers to buy the other."
                )

        # Edge case 5: explain products below the mining support threshold
        # when they do not participate in any rule that fired.
        fired_antecedents = set()
        for rule in matching_rules:
            fired_antecedents.update(rule.get("antecedents", []))

        support_map = metadata.get("product_support_by_item", {})
        min_support = float(metadata.get("min_support", 0.05))
        rare_items = [
            item for item in basket_items
            if item not in fired_antecedents
            and float(support_map.get(item, 0)) < min_support
        ]
        if rare_items:
            st.info(
                "Some products in your basket may not trigger a rule because "
                "they occur too rarely in the transaction data to meet the "
                "minimum support threshold."
            )
            for item in rare_items:
                observed_support = float(support_map.get(item, 0)) * 100
                st.write(
                    f"- **{display_name(item)}:** observed in "
                    f"{observed_support:.3f}% of baskets; the mining threshold "
                    f"was {min_support * 100:.1f}%."
                )

        # Edge case 3: rules that suggest products already in the basket
        # are excluded by the recommendation condition above.

        # Edge case 2: no rule fires -> explicit message + popular fallback.
    else:
        st.info(
            "No association rule matched the current basket. "
            "Here are popular products you may want to consider instead."
        )
        fallback = popular_fallback(basket_items, limit=5)
        if fallback:
            st.dataframe(
                pd.DataFrame([
                    {
                        "Product": p.get("Item_EN", p.get("Item")),
                        "Category": p.get("Category", "Unknown"),
                        "Price": float(p.get("Price", 0))
                    }
                    for p in fallback
                ]),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Price": st.column_config.NumberColumn(
                        "Price", format="$%.2f"
                    )
                }
            )
        else:
            st.write("No additional popular products are available.")

        support_map = metadata.get("product_support_by_item", {})
        min_support = float(metadata.get("min_support", 0.05))
        rare_items = [
            item for item in basket_items
            if float(support_map.get(item, 0)) < min_support
        ]
        if rare_items:
            st.write("Why a product may not trigger a rule:")
            for item in rare_items:
                observed_support = float(support_map.get(item, 0)) * 100
                st.write(
                    f"- **{display_name(item)}** appears in "
                    f"{observed_support:.3f}% of baskets, below the "
                    f"{min_support * 100:.1f}% minimum support threshold."
                )

    # Edge case 4 audit: display every matching rule, not just the winning
    # rule for each consequent, so the recommendation process is transparent.
    with st.expander("Rules that fired"):
        if matching_rules:
            fired_rows = []
            for rule in matching_rules:
                fired_rows.append({
                    "Antecedent": " + ".join(
                        display_name(item) for item in rule["antecedents"]
                    ),
                    "Consequent": display_name(rule["consequent"]),
                    "Support": round(rule["support"], 4),
                    "Confidence": round(rule["confidence"], 4),
                    "Lift": round(rule["lift"], 3)
                })
            st.dataframe(
                pd.DataFrame(fired_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No association rules fired for this basket.")

st.divider()
st.caption(
    "Boréal Marché — Association-rule recommendations are based on "
    "historical co-purchases, not causal relationships."
)
