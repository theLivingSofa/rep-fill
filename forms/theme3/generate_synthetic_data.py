"""
Generate synthetic responses for theme3 (women's empowerment / health / nutrition).

Biases:
  • District: always Jhajjar
  • Settlement: 90% Rural, 10% Semi-urban (no Urban)
  • Income capped low (mostly the two lowest brackets)
  • Gender ~80% Female
  • Moderate attitudes on 1–6 scales (peaked at 3–4)
  • Earning members ≤ family members
  • Occupation ↔ Q1 work status consistent
  • Conditional follow-ups (Q16b, Q20b, Q22b) populated only when parent is Yes
  • Q11/Q13/Q27/Q29/Q33 multi-select joined with ';'
"""
import random
import pandas as pd
import form_config as cfg

random.seed(42)
N_ROWS = 300
DISTRICT = "Jhajjar"
SETTLEMENT_POOL = [("Rural", 90), ("Semi-urban", 10)]


def weighted(pairs):
    values, weights = zip(*pairs)
    return random.choices(values, weights=weights, k=1)[0]


def pick_options(pool, k_min=1, k_max=3):
    k = min(random.randint(k_min, k_max), len(pool))
    items = list(pool)
    picked = []
    for _ in range(k):
        vals = [x[0] for x in items]
        wts = [x[1] for x in items]
        choice = random.choices(vals, weights=wts, k=1)[0]
        picked.append(choice)
        items = [x for x in items if x[0] != choice]
    return ";".join(picked)


# ============================ POOLS ============================
AGE = [("18-25 years", 15), ("26-35 years", 35), ("36-45 years", 30),
       ("46-55 years", 15), ("56-65 years", 4), ("above 65 years", 1)]
GENDER = [("Female", 80), ("Male", 18), ("Transgender", 2)]
INCOME = [("Upto ₹2,50,000", 45), ("₹2,50,000–₹5,00,000", 40),
          ("₹5,00,000–₹10,00,000", 15)]
FAM_SIZE = [("1 member", 3), ("2 member", 10), ("3 member", 25),
            ("4 member", 35), ("More than 5 members", 27)]
MARITAL = [("Single", 15), ("Married", 70), ("Divorced/separated", 5),
           ("Widowed", 8), ("Prefer not to say", 2)]
EDU = [("No formal education", 20), ("Below class 10", 25),
       ("Secondary (Class 10)", 25), ("Higher secondary (Class 12)", 20),
       ("Undergraduate", 8), ("Postgraduate", 2)]
OCC = [("Student", 8), ("Government employee", 3), ("Private-sector employee", 8),
       ("Self-employed/business", 10), ("Agricultural work", 25),
       ("Casual/daily wage work", 20), ("Homemaker", 25),
       ("Unemployed/seeking work", 1)]

WORK = [("Not working", 20), ("Full-time employed", 15), ("Part-time employed", 12),
        ("Self-employed/business", 10), ("Family business/agricultural work", 28),
        ("Casual/daily wage work", 15)]

NATURE = [("Agricultural work", 30), ("Non-agricultural wage work", 15),
          ("Government employment", 3), ("Private-sector employment", 10),
          ("Self-employment/business", 12), ("Domestic/care work", 20),
          ("Family enterprise", 5), ("Not applicable", 5)]
COMP = [("Cash", 50), ("Cash and kind", 15), ("Kind only", 8),
        ("Not paid", 15), ("Not applicable", 12)]
HOURS = [("Less than 10 hours", 8), ("10–19 hours", 10), ("20–29 hours", 12),
         ("30–39 hours", 15), ("40–49 hours", 25), ("50 hours or more", 20),
         ("Not applicable", 10)]
BANK = [("Yes, and I operate it independently", 40),
        ("Yes, but someone else mainly operates it", 30),
        ("Yes, but I rarely use it", 20), ("No", 10)]

DEC_HEALTH = [(1, 15), (2, 25), (3, 35), (4, 15), (5, 10)]
DEC_PURCH  = [(1, 5),  (2, 20), (3, 55), (4, 15), (5, 5)]
DEC_EARN   = [(1, 20), (2, 30), (3, 30), (4, 15), (5, 5)]
DEC_VISIT  = [(1, 10), (2, 25), (3, 40), (4, 20), (5, 5)]

EARN_SELF  = [("No regular personal earnings", 40), ("Less than ₹10,000", 35),
              ("₹10,000–₹19,999", 20), ("₹20,000–₹39,999", 4),
              ("₹40,000–₹59,999", 1)]
EARN_WOM   = [("No regular personal earnings", 45), ("Less than ₹10,000", 35),
              ("₹10,000–₹19,999", 15), ("₹20,000–₹39,999", 4),
              ("₹40,000–₹59,999", 1)]
EARN_MAN   = [("No regular personal earnings", 10), ("Less than ₹10,000", 20),
              ("₹10,000–₹19,999", 35), ("₹20,000–₹39,999", 25),
              ("₹40,000–₹59,999", 8), ("₹60,000 or more", 2)]
EARN_CMP   = [("Women earn much less", 35), ("Women earn somewhat less", 40),
              ("Earnings are approximately equal", 20),
              ("Women earn somewhat more", 3), ("Women earn much more", 1),
              ("Don't know", 1)]

HELP_181 = [("Yes", 40), ("No", 45), ("Not sure", 15)]
CONF = [("Not at all confident", 10), ("Slightly confident", 20),
        ("Somewhat confident", 30), ("Moderately confident", 20),
        ("Very confident", 15), ("Extremely confident", 5)]

AGREE6 = [(1, 5), (2, 15), (3, 30), (4, 35), (5, 12), (6, 3)]

Q16_USED = [("Yes", 12), ("No", 88)]
Q16_EXP  = [("Very negative", 15), ("Negative", 25),
            ("Neither positive nor negative", 35), ("Positive", 20),
            ("Very positive", 3), ("Prefer not to say", 2)]

CHILD_AGE = [("5–9 years", 30), ("10–13 years", 40), ("14–17 years", 30)]
CHILD_ENR = [("Yes", 80), ("No", 10),
             ("Previously enrolled but currently not attending", 10)]
CHILD_ATT = [("Regularly", 55), ("Occasionally absent", 25),
             ("Frequently absent", 10), ("Not currently attending", 5),
             ("Don't know", 5)]
CHILD_DRP = [("No", 70), ("Yes, temporarily", 10),
             ("Yes, permanently", 15), ("Not applicable", 5)]
DRP_RSN   = [("Financial constraints", 25), ("Need to work", 15),
             ("Household responsibilities", 15), ("Marriage", 15),
             ("Pregnancy", 3), ("Lack of interest", 10),
             ("Poor academic performance", 8),
             ("Distance/transportation", 5), ("Health reasons", 4)]
CHILD_WRK = [("Yes, paid work", 8), ("Yes, unpaid work", 15),
             ("No", 70), ("Don't know", 7)]
CHILD_HSE = [("Yes", 55), ("No", 40), ("Don't know", 5)]

ACCESS = {
    "healthcare when needed":              [("Yes", 75), ("No", 20), ("Don't Know", 5)],
    "recommended immunisations":           [("Yes", 85), ("No", 10), ("Don't Know", 5)],
    "safe drinking water":                 [("Yes", 70), ("No", 25), ("Don't Know", 5)],
    "functional sanitation":               [("Yes", 55), ("No", 35), ("Don't Know", 10)],
    "school meal":                         [("Yes", 80), ("No", 15), ("Don't Know", 5)],
    "digital access needed for education": [("Yes", 25), ("No", 70), ("Don't Know", 5)],
}
FOOD = {
    "grains, roots and tubers":         [("Yes", 98), ("No", 2)],
    "pulses, beans and peas":           [("Yes", 75), ("No", 25)],
    "nuts and seeds":                   [("Yes", 25), ("No", 75)],
    "milk and dairy":                   [("Yes", 60), ("No", 40)],
    "meat, poultry or fish":            [("Yes", 20), ("No", 80)],
    "eggs":                             [("Yes", 40), ("No", 60)],
    "dark green leafy vegetables":      [("Yes", 55), ("No", 45)],
    "other vegetables":                 [("Yes", 85), ("No", 15)],
    "vitamin-a-rich fruits/vegetables": [("Yes", 45), ("No", 55)],
    "other fruits":                     [("Yes", 35), ("No", 65)],
}
MEALS    = [("One", 3), ("Two", 30), ("Three", 60), ("Four", 5), ("Five or nore", 2)]
PACKAGED = [("Never", 15), ("Less than once a week", 30), ("1–2 times a week", 35),
            ("3–5 times a week", 15), ("Daily", 5)]
Q_NUTR   = [("Very poor", 5), ("Poor", 10), ("Below average", 20),
            ("Above average", 25), ("Good", 25), ("Very good", 10),
            ("Not aware/not used", 5)]
TREAT    = [("Government hospital/health centre", 45),
            ("Private hospital/clinic", 25), ("Local doctor", 15),
            ("Pharmacy/chemist", 8), ("AYUSH/traditional practitioner", 3),
            ("Self-medication/home remedies", 3),
            ("Did not seek treatment", 1)]
INSUR    = [("Yes, government health insurance/coverage", 45),
            ("Yes, private health insurance", 8),
            ("Yes, both government and private coverage", 3),
            ("No", 40), ("Don't know", 4)]
DIG_HLTH = [("Yes, frequently", 3), ("Yes, occasionally", 12), ("Yes, once", 10),
            ("No", 65), ("Not aware of such services", 10)]
HLTH_RATE= [("Very poor", 3), ("Poor", 10), ("Below average", 22),
            ("Above average", 35), ("Good", 25), ("Very good", 5)]
BBBP_HRD = [("Yes, and I know its purpose", 25),
            ("Yes, but I know little about it", 35),
            ("I have heard the name only", 25),
            ("No, I had not heard of it", 15)]
GIRL_EDU = [("Decreased substantially", 2), ("Decreased somewhat", 8),
            ("Remained about the same", 25), ("Increased somewhat", 45),
            ("Increased substantially", 15), ("Not sure / cannot say", 5)]
SUKANYA  = [("Yes, and I know how to access them", 15),
            ("Yes, but I do not know how to access them", 25),
            ("I have heard of them but know very little", 30),
            ("No, I am not aware of such programmes", 30)]

Q11_POOL = [
    ("Differences in education/qualifications", 8),
    ("Differences in skills or experience", 8),
    ("Differences in type of employment", 8),
    ("More unpaid household/care responsibilities", 20),
    ("Fewer working hours", 12),
    ("Limited access to better-paying jobs", 10),
    ("Discrimination against women", 12),
    ("Occupational segregation", 8),
    ("Lack of negotiation opportunities", 5),
    ("Lack of mobility", 7),
    ("Don't know", 2),
]
Q13_POOL = [
    ("Women's helpline 181", 15), ("Police", 25),
    ("One Stop Centre/Sakhi Centre", 10),
    ("Women and Child Development Department", 12),
    ("Legal aid services", 8), ("Local women's organisations/NGOs", 10),
    ("ASHA/Anganwadi worker", 18), ("None", 2),
]
Q27_POOL = [
    ("Iron/folic acid or other nutrition supplements", 25),
    ("Nutrition counselling", 10), ("Anganwadi nutrition services", 25),
    ("Take-home ration", 15), ("Poshan-related services", 10),
    ("Maternal/child nutrition services", 10), ("None", 3), ("Don't know", 2),
]
Q29_POOL = [
    ("Fever/infections", 20), ("Respiratory problems", 10),
    ("Gastrointestinal problems", 12),
    ("Reproductive/maternal health problems", 10),
    ("Anaemia/weakness", 20),
    ("Mental health/stress-related problems", 8),
    ("Chronic condition such as diabetes, hypertension or asthma", 15),
    ("None", 5),
]
Q33_POOL = [
    ("High treatment cost", 20), ("High medicine cost", 15),
    ("Long waiting time", 12), ("Lack of doctors", 10), ("Lack of medicines", 8),
    ("Distance to facility", 10), ("Transportation difficulties", 8),
    ("Inconvenient opening hours", 5), ("Poor quality of care", 5),
    ("Difficulty obtaining appointments", 4), ("None", 3),
]


# ============================ CONSISTENCY HELPERS ============================
def work_status_for(occupation):
    """Q1 answer consistent with the chosen occupation."""
    if occupation == "Student":
        return weighted([("Not working", 55),
                         ("Casual/daily wage work", 30),
                         ("Part-time employed", 15)])
    if occupation == "Government employee":
        return "Full-time employed"
    if occupation == "Private-sector employee":
        return weighted([("Full-time employed", 85), ("Part-time employed", 15)])
    if occupation == "Self-employed/business":
        return "Self-employed/business"
    if occupation == "Agricultural work":
        return weighted([("Family business/agricultural work", 80),
                         ("Casual/daily wage work", 20)])
    if occupation == "Casual/daily wage work":
        return weighted([("Casual/daily wage work", 90),
                         ("Part-time employed", 10)])
    if occupation == "Homemaker":
        return weighted([("Not working", 50),
                         ("Family business/agricultural work", 40),
                         ("Part-time employed", 10)])
    if occupation == "Unemployed/seeking work":
        return "Not working"
    return "Not working"


def nature_for(work_status, occupation):
    """Q2 answer consistent with Q1."""
    if work_status == "Not working":
        return "Not applicable"
    if work_status == "Self-employed/business":
        return "Self-employment/business"
    if work_status == "Casual/daily wage work":
        return "Non-agricultural wage work"
    if work_status == "Full-time employed":
        if occupation == "Government employee":
            return "Government employment"
        if occupation == "Private-sector employee":
            return "Private-sector employment"
        return weighted([("Agricultural work", 40),
                         ("Non-agricultural wage work", 25),
                         ("Private-sector employment", 20),
                         ("Family enterprise", 15)])
    if work_status == "Part-time employed":
        return weighted([("Domestic/care work", 40),
                         ("Agricultural work", 25),
                         ("Non-agricultural wage work", 20),
                         ("Family enterprise", 15)])
    if work_status == "Family business/agricultural work":
        return weighted([("Agricultural work", 60),
                         ("Domestic/care work", 25),
                         ("Family enterprise", 15)])
    return "Not applicable"


def comp_for(work_status):
    """Q3 answer consistent with Q1."""
    if work_status == "Not working":
        return "Not applicable"
    if work_status in ("Family business/agricultural work",):
        return weighted([("Cash", 40), ("Cash and kind", 25),
                         ("Kind only", 20), ("Not paid", 15)])
    if work_status in ("Full-time employed", "Self-employed/business"):
        return weighted([("Cash", 80), ("Cash and kind", 20)])
    if work_status == "Part-time employed":
        return weighted([("Cash", 55), ("Cash and kind", 15),
                         ("Kind only", 10), ("Not paid", 20)])
    if work_status == "Casual/daily wage work":
        return weighted([("Cash", 60), ("Cash and kind", 20),
                         ("Kind only", 10), ("Not paid", 10)])
    return "Not applicable"


def hours_for(work_status):
    """Q4 answer consistent with Q1."""
    if work_status == "Not working":
        return "Not applicable"
    if work_status == "Full-time employed":
        return weighted([("40–49 hours", 50), ("50 hours or more", 45),
                         ("30–39 hours", 5)])
    if work_status == "Part-time employed":
        return weighted([("10–19 hours", 35), ("20–29 hours", 40),
                         ("30–39 hours", 25)])
    if work_status == "Casual/daily wage work":
        return weighted([("30–39 hours", 25), ("40–49 hours", 35),
                         ("50 hours or more", 40)])
    if work_status == "Self-employed/business":
        return weighted([("40–49 hours", 40), ("50 hours or more", 50),
                         ("30–39 hours", 10)])
    if work_status == "Family business/agricultural work":
        return weighted([("20–29 hours", 20), ("30–39 hours", 25),
                         ("40–49 hours", 35), ("50 hours or more", 20)])
    return weighted(HOURS)


# ============================ ROW BUILDER ============================
def make_row():
    questions = list(cfg.ENTRY_IDS.keys())
    row = {}

    # --- correlated decisions, computed once ---
    occupation = weighted(OCC)
    work_status = work_status_for(occupation)
    is_working = work_status != "Not working"

    fam_bucket = weighted(FAM_SIZE)
    fam_n = 6 if "More than" in fam_bucket else int(fam_bucket.split()[0])
    earn_n = max(1, min(random.choices([1, 2, 3, 4, 5, 6],
                                       weights=[40, 40, 15, 4, 1, 0])[0], fam_n))
    earn_bucket = "More than 5 members" if earn_n >= 5 else f"{earn_n} member"

    q16_used  = weighted(Q16_USED)
    q20_drop  = weighted(CHILD_DRP)
    q22_house = weighted(CHILD_HSE)

    for q in questions:
        ql = q.lower().strip()

        # ---- basics ----
        if q == "District":
            row[q] = DISTRICT
        elif q == "Type of Settlement":
            row[q] = weighted(SETTLEMENT_POOL)
        elif q == "Age":
            row[q] = weighted(AGE)
        elif q == "Gender":
            row[q] = weighted(GENDER)
        elif q == "Annual Family income":
            row[q] = weighted(INCOME)
        elif "how many members are there in your family" in ql:
            row[q] = fam_bucket
        elif "earning members" in ql:
            row[q] = earn_bucket
        elif q == "Marital status":
            row[q] = weighted(MARITAL)
        elif q == "Highest level of education completed":
            row[q] = weighted(EDU)
        elif q == "Current occupation/employment status":
            row[q] = occupation

        # ---- Q1-Q4 work ----
        elif ql.startswith("1. what is your current work status"):
            row[q] = work_status
        elif ql.startswith("2. what is the nature"):
            row[q] = nature_for(work_status, occupation)
        elif ql.startswith("3. how are you compensated"):
            row[q] = comp_for(work_status)
        elif ql.startswith("4. approximately how many hours"):
            row[q] = hours_for(work_status)

        # ---- Q5 bank ----
        elif ql.startswith("5. do you have a bank account"):
            row[q] = weighted(BANK)

        # ---- Q6 decision making ----
        elif ql.startswith("6. who usually makes decisions"):
            if "your own healthcare" in ql:
                row[q] = str(weighted(DEC_HEALTH))
            elif "major household purchases" in ql:
                row[q] = str(weighted(DEC_PURCH))
            elif "use of your own earnings" in ql:
                row[q] = str(weighted(DEC_EARN))
            elif "visits to family or relatives" in ql:
                row[q] = str(weighted(DEC_VISIT))
            else:
                row[q] = str(weighted(DEC_PURCH))

        # ---- Q7-Q9 earnings ----
        elif ql.startswith("7. if you are currently working"):
            row[q] = ("No regular personal earnings" if not is_working
                      else weighted(EARN_SELF))
        elif ql.startswith("8. if another adult woman"):
            row[q] = weighted(EARN_WOM)
        elif ql.startswith("9. if another adult man"):
            row[q] = weighted(EARN_MAN)

        # ---- Q10 comparison ----
        elif ql.startswith("10. among men and women"):
            row[q] = weighted(EARN_CMP)

        # ---- Q11-Q14 ----
        elif ql.startswith("11. what are the main reasons"):
            row[q] = pick_options(Q11_POOL, 2, 3)
        elif ql.startswith("12. before today"):
            row[q] = weighted(HELP_181)
        elif ql.startswith("13. which of the following support"):
            row[q] = pick_options(Q13_POOL, 2, 4)
        elif ql.startswith("14. if a woman in your community"):
            row[q] = weighted(CONF)

        # ---- Q15 (4 sub-qs, 1-6) ----
        elif ql.startswith("15. please indicate your agreement"):
            row[q] = str(weighted(AGREE6))

        # ---- Q16 + Q16b ----
        elif ql.startswith("16. have you or any woman"):
            row[q] = q16_used
        elif "how would you describe the experience" in ql:
            row[q] = weighted(Q16_EXP) if q16_used == "Yes" else ""

        # ---- Q17-Q19 ----
        elif ql.startswith("17. how old is the child"):
            row[q] = weighted(CHILD_AGE)
        elif ql.startswith("18. is the child currently enrolled"):
            row[q] = weighted(CHILD_ENR)
        elif ql.startswith("19. during the current school year"):
            row[q] = weighted(CHILD_ATT)

        # ---- Q20 + Q20b ----
        elif ql.startswith("20. has the child ever dropped out"):
            row[q] = q20_drop
        elif "what was the main reason" in ql:
            row[q] = weighted(DRP_RSN) if q20_drop.startswith("Yes") else ""

        # ---- Q21 ----
        elif ql.startswith("21. during the last 7 days, did the child engage"):
            row[q] = weighted(CHILD_WRK)

        # ---- Q22 + Q22b ----
        elif ql.startswith("22. during the last 7 days, did the child perform"):
            row[q] = q22_house
        elif "approximate time spent" in ql:
            row[q] = f"{random.randint(5, 30)} hours" if q22_house == "Yes" else ""

        # ---- Q23 access ----
        elif ql.startswith("23. does the child currently have"):
            row[q] = "Yes"
            for key, pool in ACCESS.items():
                if key in ql:
                    row[q] = weighted(pool)
                    break

        # ---- Q24 food ----
        elif ql.startswith("24. during the previous 24 hours"):
            row[q] = "Yes"
            for key, pool in FOOD.items():
                if key in ql:
                    row[q] = weighted(pool)
                    break

        # ---- Q25-Q30 ----
        elif ql.startswith("25. on a typical day"):
            row[q] = weighted(MEALS)
        elif ql.startswith("26. how often do you consume packaged"):
            row[q] = weighted(PACKAGED)
        elif ql.startswith("27. during the past 12 months, have you received"):
            row[q] = pick_options(Q27_POOL, 1, 3)
        elif ql.startswith("28. how would you rate the quality of nutrition"):
            row[q] = weighted(Q_NUTR)
        elif ql.startswith("29. during the past 12 months, which of the following health"):
            row[q] = pick_options(Q29_POOL, 1, 2)
        elif ql.startswith("30. when you or a household member"):
            row[q] = weighted(TREAT)

        # ---- Q31 healthcare statements (5 subs) ----
        elif ql.startswith("31. please indicate your agreement"):
            row[q] = str(weighted(AGREE6))

        # ---- Q32-Q35 ----
        elif ql.startswith("32. does your household currently have any form"):
            row[q] = weighted(INSUR)
        elif ql.startswith("33. which of the following difficulties"):
            row[q] = pick_options(Q33_POOL, 1, 3)
        elif ql.startswith("34. have you used any digital health"):
            row[q] = weighted(DIG_HLTH)
        elif ql.startswith("35. overall, how would you rate the healthcare"):
            row[q] = weighted(HLTH_RATE)

        # ---- Q36-Q41 ----
        elif ql.startswith("36. before today, had you heard of the beti"):
            row[q] = weighted(BBBP_HRD)
        elif ql.startswith("37. how familiar are you"):
            row[q] = str(weighted(AGREE6))
        elif ql.startswith("38. in your opinion, how effective has the beti"):
            row[q] = str(weighted(AGREE6))
        elif ql.startswith("39. compared with the past"):
            row[q] = weighted(GIRL_EDU)
        elif ql.startswith("40. in your opinion, how effective have government"):
            row[q] = str(weighted(AGREE6))
        elif ql.startswith("41. are you aware of any government financial"):
            row[q] = weighted(SUKANYA)

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
    print("Settlement: 90% Rural, 10% Semi-urban")
    print("Occupation ↔ Q1/Q2/Q3/Q4 are consistent.")
    print("Attitudes peaked at 3–4 on 6-point scales.")


if __name__ == "__main__":
    main()