"""
Verify that synthetic_responses.xlsx is internally consistent.
Checks: earning members <= total family members; district always Jhajjar;
        checkbox cells contain ';'.
"""
import pandas as pd

import form_config as cfg

df = pd.read_excel("synthetic_responses.xlsx", sheet_name="Responses").astype(str)

fam_col = next(q for q in cfg.ENTRY_IDS
               if "how many members are there in your family" in q.lower())
earn_col = next(q for q in cfg.ENTRY_IDS
                if "earning members" in q.lower())


def b2i(b):
    b = b.lower()
    if "more than" in b:
        return 6
    for t in b.replace("member", "").split():
        if t.isdigit():
            return int(t)
    return 1


bad = df[df.apply(lambda r: b2i(r[earn_col]) > b2i(r[fam_col]), axis=1)]

print(f"Rows total                 : {len(df)}")
print(f"Rows with earning > family : {len(bad)}")
print(f"District unique values     : {df['District'].unique().tolist()}")
print(f"Family buckets seen        : {sorted(df[fam_col].unique())}")
print(f"Earning buckets seen       : {sorted(df[earn_col].unique())}")

for q in cfg.CHECKBOX_QUESTIONS:
    if q in df.columns:
        multi = df[q].str.contains(";").sum()
        print(f"Checkbox '{q[:45]}...': {multi} rows contain ';'")