"""
Read any Google Form and create:
  - form_config.py         : form URL + question -> entry ID map
  - responses_template.xlsx: 'Responses' and 'Options' sheets

Usage:
    python3 dump_form.py "https://docs.google.com/forms/d/e/XXXX/viewform"
"""
import json
import re
import sys

import pandas as pd

PROFILE_DIR = "chrome_profile"

SKIP_TYPES = {6, 8, 11, 12}
DATE_TYPE, CHECKBOX_TYPE, GRID_TYPE = 9, 4, 7


def parse_form(html):
    m = re.search(r"FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);\s*</script>", html, re.S)
    if not m:
        raise RuntimeError(
            "Could not find form data. Are you logged in / is the link right?"
        )
    data = json.loads(m.group(1))
    questions, seen = [], {}
    for it in data[1][1] or []:
        title, qtype, subs = it[1], it[3], (it[4] if len(it) > 4 else None)
        if qtype in SKIP_TYPES or not subs:
            continue
        for sub in subs:
            label = (title or "").strip()
            if qtype == GRID_TYPE and len(sub) > 3 and sub[3]:
                label += f" [{sub[3][0]}]"
            seen[label] = seen.get(label, 0) + 1
            if seen[label] > 1:
                label += f" ({seen[label]})"
            opts = [o[0] for o in (sub[1] or []) if o and o[0]]
            questions.append({
                "title": label,
                "entry": f"entry.{sub[0]}",
                "type": qtype,
                "required": bool(sub[2]) if len(sub) > 2 else False,
                "options": opts,
            })
    return questions


def main(url):
    from playwright.sync_api import sync_playwright
    from browser_launch import launch, wait_for_login

    base = url.split("?")[0]
    with sync_playwright() as p:
        ctx = launch(p, PROFILE_DIR)
        page = ctx.new_page()
        page.goto(base)
        if "accounts.google.com" in page.url:
            print("→ Sign in to Google in the opened Chrome window.")
            print("  The browser will return to the form when you are done.")
            wait_for_login(page, base)
        page.wait_for_load_state("domcontentloaded")
        html = page.content()
        ctx.close()

    qs = parse_form(html)

    with open("form_config.py", "w", encoding="utf-8") as f:
        f.write(f"FORM_URL_BASE = {base!r}\n\nENTRY_IDS = {{\n")
        for q in qs:
            f.write(f"    {q['title']!r}: {q['entry']!r},\n")
        f.write("}\n\n")
        f.write(f"DATE_QUESTIONS = {[q['title'] for q in qs if q['type'] == DATE_TYPE]!r}\n")
        f.write(f"CHECKBOX_QUESTIONS = {[q['title'] for q in qs if q['type'] == CHECKBOX_TYPE]!r}\n")

    with pd.ExcelWriter("responses_template.xlsx") as xw:
        pd.DataFrame(columns=[q["title"] for q in qs]).to_excel(
            xw, sheet_name="Responses", index=False
        )
        pd.DataFrame([{
            "Question": q["title"],
            "Required": "YES" if q["required"] else "",
            "Type code": q["type"],
            "Allowed answers (copy exactly)": " | ".join(q["options"]),
        } for q in qs]).to_excel(
            xw, sheet_name="Options", index=False
        )

    print(f"Found {len(qs)} questions.")
    print("Created form_config.py and responses_template.xlsx")
    print("Checkbox questions: put multiple answers in one cell separated by ';'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])