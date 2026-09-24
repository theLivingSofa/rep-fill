"""
Generate synthetic responses for theme5 (kirana stores & quick-commerce impact).
Respondent profile: small kirana shop owner in rural/semi-urban Jhajjar.
Biases: modest-size shops, high QC awareness, moderate-moderate impact,
        mixed adaptation (UPI/WhatsApp high, digital marketing low).
"""
import random
import pandas as pd
import form_config as cfg

random.seed(42)
N_ROWS = 300
DISTRICT = "Jhajjar"


def weighted(pairs):
    values, weights = zip(*pairs)
    return random.choices(values, weights=weights, k=1)[0]


# ----------------------------- bias pools -----------------------------
SETTLEMENT = [("Rural", 90), ("Semi-urban", 10)]

Q1_BUSINESS = [("Grocery/Kirana", 65), ("Convenience store", 12),
               ("General store", 18), ("Fruits & vegetables", 5)]
Q2_AGE_SHOP = [("Less than 2 years", 8), ("2–5 years", 15), ("6–10 years", 27),
               ("11–20 years", 32), ("More then 20 years", 18)]
Q3_WORKERS  = [("1", 25), ("2–3", 55), ("4–5", 15), ("6–10", 4), ("More than 10", 1)]
Q4_SALES    = [("Less than ₹50,000", 15), ("₹50,000–₹1 lakh", 35),
               ("₹1–3 lakh", 35), ("₹3–5 lakh", 10),
               ("More than ₹5 lakh", 3), ("Prefer not to say", 2)]
Q5_AWARE_QC = [("Yes", 88), ("No", 12)]
Q6_PLATFORMS = [("Blinkit", 45), ("Zepto", 25), ("Swiggy Instamart", 20),
                ("BigBasket/BB Now", 5), ("Don't know", 5)]
Q7_CUST_FREQ = [("Very frequently", 20), ("Frequently", 30), ("Sometimes", 25),
                ("Rarely", 15), ("Never", 5), ("Don't know", 5)]
Q8_COMP_SIG  = [("Not at all significant", 5), ("Slightly significant", 12),
                ("Moderately significant", 30), ("Significant", 33),
                ("Very significant", 20)]
Q9_ASSORT    = [("I have expanded my product range to compete", 15),
                ("I have added selected products that are popular online", 25),
                ("No significant change in my product range", 35),
                ("I have reduced products that face strong online competition", 18),
                ("I have substantially reduced my product range", 7)]

# --- Q10 "since 2021, how has X changed" (1=Decreased Significantly, 6=Increased Significantly) ---
Q10_FOOTFALL = [(1, 20), (2, 25), (3, 25), (4, 15), (5, 10), (6, 5)]
Q10_SALES    = [(1, 12), (2, 22), (3, 28), (4, 18), (5, 15), (6, 5)]
Q10_MARGIN   = [(1, 22), (2, 28), (3, 25), (4, 12), (5, 10), (6, 3)]
Q10_PRICECOMP= [(1, 2), (2, 3), (3, 5), (4, 18), (5, 35), (6, 37)]
Q10_CUSTCMP  = [(1, 1), (2, 2), (3, 5), (4, 15), (5, 35), (6, 42)]
Q10_FASTDEL  = [(1, 2), (2, 3), (3, 5), (4, 15), (5, 35), (6, 40)]
Q10_HOMEDEL  = [(1, 2), (2, 3), (3, 7), (4, 15), (5, 35), (6, 38)]
Q10_VARIETY  = [(1, 3), (2, 5), (3, 10), (4, 25), (5, 35), (6, 22)]
Q10_ASSORT   = [(1, 5), (2, 10), (3, 20), (4, 30), (5, 25), (6, 10)]
Q10_DIGIPAY  = [(1, 1), (2, 2), (3, 3), (4, 10), (5, 32), (6, 52)]

# --- Q11 number of kirana stores in bazaar changed ---
Q11_STORES = [("Decreased Significantly", 12), ("Decreased", 25),
              ("Slightly Decreased", 28), ("Slightly Increased", 20),
              ("Increased", 10), ("Increased Significantly", 5)]

Q12_CLOSED = [("None (0%)", 8), ("Less than 10%", 20), ("10–25%", 40),
              ("26–50%", 22), ("More than 50%", 5), ("Don't know", 5)]

# --- Q13 strategies adopted (1=Not at all, 6=To a very large extent) ---
Q13_HOMEDEL   = [(1, 20), (2, 15), (3, 15), (4, 20), (5, 20), (6, 10)]
Q13_WHATSAPP  = [(1, 8),  (2, 7),  (3, 10), (4, 20), (5, 30), (6, 25)]
Q13_UPI       = [(1, 2),  (2, 3),  (3, 5),  (4, 10), (5, 30), (6, 50)]
Q13_DISCOUNTS = [(1, 20), (2, 20), (3, 20), (4, 20), (5, 15), (6, 5)]
Q13_EXPAND    = [(1, 12), (2, 15), (3, 20), (4, 25), (5, 20), (6, 8)]
Q13_NICHE     = [(1, 20), (2, 18), (3, 20), (4, 22), (5, 15), (6, 5)]
Q13_PERSONAL  = [(1, 3),  (2, 5),  (3, 10), (4, 20), (5, 35), (6, 27)]
Q13_CREDIT    = [(1, 8),  (2, 10), (3, 15), (4, 25), (5, 25), (6, 17)]
Q13_HOURS     = [(1, 30), (2, 20), (3, 18), (4, 15), (5, 12), (6, 5)]
Q13_DIGIMKT   = [(1, 45), (2, 20), (3, 15), (4, 10), (5, 7),  (6, 3)]
Q13_FASTDEL   = [(1, 30), (2, 18), (3, 15), (4, 18), (5, 13), (6, 6)]
Q13_BULK      = [(1, 15), (2, 13), (3, 15), (4, 22), (5, 22), (6, 13)]
Q13_OTHER     = [(1, 55), (2, 15), (3, 10), (4, 10), (5, 5),  (6, 5)]

Q14_MDR_AWARE = [("Yes", 30), ("No", 50), ("Not sure", 20)]
Q15_MDR_EXP   = [("Very negatively", 5), ("Negatively", 22),
                 ("Slightly negatively", 38), ("Slightly positively", 20),
                 ("Positively", 10), ("Very positively", 5)]
Q16_MDR_PREF  = [(1, 15), (2, 15), (3, 20), (4, 30), (5, 15), (6, 5)]
Q17_MDR_COST  = [("No impact", 5), ("Very little impact", 10), ("Little impact", 20),
                 ("Moderate impact", 35), ("Significant impact", 22),
                 ("Very significant impact", 8)]
Q18_MDR_CUST  = [("No influence", 5), ("Very little influence", 10),
                 ("Little influence", 20), ("Moderate influence", 35),
                 ("Significant influence", 22), ("Very significant influence", 8)]


# ----------------------------- row builder -----------------------------
def make_row():
    questions = list(cfg.ENTRY_IDS.keys())
    row = {}

    # Correlated: awareness of QC drives downstream answers
    aware_qc = weighted(Q5_AWARE_QC)

    for q in questions:
        ql = q.lower().strip()

        if q == "District":
            row[q] = DISTRICT
        elif q == "Type of settlement":
            row[q] = weighted(SETTLEMENT)
        elif ql.startswith("1. type of business"):
            row[q] = weighted(Q1_BUSINESS)
        elif ql.startswith("2. how long has your shop"):
            row[q] = weighted(Q2_AGE_SHOP)
        elif ql.startswith("3. number of people working"):
            row[q] = weighted(Q3_WORKERS)
        elif ql.startswith("4. approximate monthly sales"):
            row[q] = weighted(Q4_SALES)

        # Q5 awareness
        elif ql.startswith("5. are you aware of quick-commerce"):
            row[q] = aware_qc

        # Q6 platforms (only meaningful if aware)
        elif ql.startswith("6. which platforms"):
            row[q] = "Don't know" if aware_qc == "No" else weighted(Q6_PLATFORMS)

        # Q7 customer frequency
        elif ql.startswith("7. how frequently do your customers"):
            row[q] = "Don't know" if aware_qc == "No" else weighted(Q7_CUST_FREQ)

        # Q8 significance
        elif ql.startswith("8. how significant"):
            row[q] = "Not at all significant" if aware_qc == "No" else weighted(Q8_COMP_SIG)

        # Q9 assortment
        elif ql.startswith("9. how has quick-commerce competition"):
            row[q] = weighted(Q9_ASSORT)

        # Q10 – 10 sub-questions
        elif ql.startswith("10. compared with the period"):
            if "customer footfall" in ql:       row[q] = str(weighted(Q10_FOOTFALL))
            elif "sales of my shop" in ql:      row[q] = str(weighted(Q10_SALES))
            elif "profit margins" in ql:        row[q] = str(weighted(Q10_MARGIN))
            elif "price competition" in ql:     row[q] = str(weighted(Q10_PRICECOMP))
            elif "customers compare prices" in ql: row[q] = str(weighted(Q10_CUSTCMP))
            elif "customers expect faster" in ql:  row[q] = str(weighted(Q10_FASTDEL))
            elif "demand for home delivery" in ql: row[q] = str(weighted(Q10_HOMEDEL))
            elif "demand for greater product variety" in ql: row[q] = str(weighted(Q10_VARIETY))
            elif "product assortment in my shop" in ql: row[q] = str(weighted(Q10_ASSORT))
            elif "use of digital payments" in ql: row[q] = str(weighted(Q10_DIGIPAY))
            else: row[q] = "4"

        # Q11 – number of kirana stores changed
        elif ql.startswith("11. compared with the period"):
            row[q] = weighted(Q11_STORES)

        # Q12 – % closed
        elif ql.startswith("12. approximately what percentage"):
            row[q] = weighted(Q12_CLOSED)

        # Q13 – 14 sub-questions about strategies
        elif ql.startswith("13. to what extent"):
            if "home delivery" in ql:              row[q] = str(weighted(Q13_HOMEDEL))
            elif "whatsapp" in ql or "phone-based" in ql: row[q] = str(weighted(Q13_WHATSAPP))
            elif "upi and other digital" in ql:    row[q] = str(weighted(Q13_UPI))
            elif "discounts" in ql:                row[q] = str(weighted(Q13_DISCOUNTS))
            elif "expansion of product" in ql:     row[q] = str(weighted(Q13_EXPAND))
            elif "focus on products not readily" in ql: row[q] = str(weighted(Q13_NICHE))
            elif "personalised customer" in ql:    row[q] = str(weighted(Q13_PERSONAL))
            elif "credit facilities" in ql:        row[q] = str(weighted(Q13_CREDIT))
            elif "extended business hours" in ql:  row[q] = str(weighted(Q13_HOURS))
            elif "digital/social-media marketing" in ql: row[q] = str(weighted(Q13_DIGIMKT))
            elif "faster local delivery" in ql:    row[q] = str(weighted(Q13_FASTDEL))
            elif "bulk purchasing" in ql:          row[q] = str(weighted(Q13_BULK))
            elif "other business strategies" in ql: row[q] = str(weighted(Q13_OTHER))
            else: row[q] = "3"

        # Q14 – MDR awareness
        elif ql.startswith("14. are you aware of the proposed"):
            row[q] = weighted(Q14_MDR_AWARE)

        # Q15 – expected MDR effect
        elif ql.startswith("15. how do you expect"):
            row[q] = weighted(Q15_MDR_EXP)

        # Q16 – MDR influence on preference
        elif ql.startswith("16. to what extent do you think the introduction"):
            row[q] = str(weighted(Q16_MDR_PREF))

        # Q17 – MDR cost impact
        elif ql.startswith("17. to what extent do you think upi mdr"):
            row[q] = weighted(Q17_MDR_COST)

        # Q18 – MDR influence on customers
        elif ql.startswith("18. to what extent do you think upi mdr will influence customers"):
            row[q] = weighted(Q18_MDR_CUST)

        else:
            row[q] = ""

    return row


def main(n_rows=N_ROWS):
    questions = list(cfg.ENTRY_IDS.keys())
    rows = [make_row() for _ in range(n_rows)]
    df = pd.DataFrame(rows, columns=questions).astype(str)

    empty_cols = [c for c in df.columns if (df[c] == "").all()]
    if empty_cols:
        print("WARNING — these questions were never filled:")
        for c in empty_cols:
            print(f"   - {c[:100]}")

    df.to_excel("synthetic_responses.xlsx", sheet_name="Responses", index=False)
    print(f"\nCreated synthetic_responses.xlsx: {len(df)} rows, {len(df.columns)} columns")
    print(f"District: {DISTRICT}")
    print("Biases: small kirana shops, high QC awareness, moderate-negative impact,")
    print("        high adoption of UPI/WhatsApp, low digital marketing.")


if __name__ == "__main__":
    main()