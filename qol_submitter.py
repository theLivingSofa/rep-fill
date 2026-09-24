"""
QoL Google Form bulk filler.

Reads responses from an Excel file, builds a pre-filled link for each row,
opens it in a signed-in Chrome, ticks the "record email" checkbox if present,
then clicks Next/Submit through every page.

Between rows, waits a randomized delay (default 150–180 seconds = 2m30s–3m)
so submissions don't look automated.

Clicks are done via JavaScript, so the Chrome window does not steal focus
and your typing in other apps won't affect the form.

Usage:
    python3 qol_submitter.py links --config form_config \
        --file synthetic_responses.xlsx --sheet Responses

    python3 qol_submitter.py submit --config form_config \
        --file synthetic_responses.xlsx --sheet Responses \
        --start 0 --limit 3 --review --delay-min 10 --delay-max 20

    python3 qol_submitter.py submit --config form_config \
        --file synthetic_responses.xlsx --sheet Responses \
        --start 0 --limit 100 --stop-on-fail

Rows already marked OK in submission_log.csv are skipped, so re-running is safe.
"""
import argparse
import csv
import importlib
import os
import random
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, os.getcwd())

CFG = None
LOG_FILE = "submission_log.csv"
LINKS_FILE = "submission_links.txt"
PROFILE_DIR = "chrome_profile"


# ----------------------------------------------------------------------
# JavaScript snippets
# ----------------------------------------------------------------------
DISMISS_DIALOG_JS = """
() => {
    const dialog = document.querySelector('[role="dialog"]');
    if (!dialog) return 'no-dialog';
    const candidates = dialog.querySelectorAll(
        '[role="button"], button, a, span'
    );
    for (const el of candidates) {
        const text = (el.innerText || '').trim();
        if (text === 'Continue' || text === 'Use previous draft') {
            el.click();
            return 'clicked:' + text;
        }
    }
    return 'no-button';
}
"""

TICK_EMAIL_JS = """
() => {
    const boxes = document.querySelectorAll(
        'input[type="checkbox"], [role="checkbox"]'
    );
    for (const el of boxes) {
        let node = el.closest('div') || el.parentElement;
        let text = '';
        for (let i = 0; i < 4 && node; i++) {
            text += ' ' + (node.innerText || '');
            node = node.parentElement;
        }
        text = text.toLowerCase();
        if (text.includes('as the email to be included')) {
            const checked = el.getAttribute('aria-checked') === 'true'
                            || el.checked === true;
            if (!checked) {
                el.click();
                return 'clicked';
            }
            return 'already-checked';
        }
    }
    return 'not-found';
}
"""

# JS click: finds a button by visible text and clicks it without moving
# the OS mouse or requiring Chrome to be the foreground window.
CLICK_BUTTON_JS = """
(text) => {
    const nodes = document.querySelectorAll(
        'div[role="button"], button, [role="button"]'
    );
    for (const el of nodes) {
        if ((el.innerText || '').trim() === text) {
            el.click();
            return true;
        }
    }
    return false;
}
"""


# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------
def clean(v):
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if re.fullmatch(r"-?\d+\.0", s):
        s = s[:-2]
    return s


def parse_date(s):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def build_link(row):
    date_qs = getattr(CFG, "DATE_QUESTIONS", [])
    multi_qs = getattr(CFG, "CHECKBOX_QUESTIONS", [])
    params = []
    for header, entry in CFG.ENTRY_IDS.items():
        val = clean(row.get(header, ""))
        if not val:
            continue
        if header in date_qs:
            d = parse_date(val)
            if d:
                params += [(f"{entry}_year", d.year),
                           (f"{entry}_month", d.month),
                           (f"{entry}_day", d.day)]
                continue
        if header in multi_qs:
            params += [(entry, part.strip())
                       for part in val.split(";") if part.strip()]
            continue
        params.append((entry, val))
    return f"{CFG.FORM_URL_BASE}?usp=pp_url&{urllib.parse.urlencode(params)}"


# ----------------------------------------------------------------------
# Human-like delay between submissions
# ----------------------------------------------------------------------
def human_delay(min_sec, max_sec):
    total = random.uniform(min_sec, max_sec)
    total = max(6, total)   # 6-second floor
    mins, secs = divmod(int(total), 60)
    print(f"   ⏱  Waiting {mins}m {secs:02d}s before next submission "
          f"(~{int(total)}s)")
    end = time.time() + total
    last_report = -1
    while True:
        remaining = end - time.time()
        if remaining <= 0:
            break
        time.sleep(min(15, remaining))
        r = int(end - time.time())
        if r > 0 and r // 30 != last_report:
            last_report = r // 30
            print(f"      ...{r // 60}m {r % 60:02d}s left")


# ----------------------------------------------------------------------
# Browser-side helpers
# ----------------------------------------------------------------------
def dismiss_blockers(page, tries=4):
    for _ in range(tries):
        try:
            result = page.evaluate(DISMISS_DIALOG_JS)
        except Exception:
            return
        if isinstance(result, str) and result.startswith("clicked:"):
            page.wait_for_timeout(1800)
        else:
            page.wait_for_timeout(300)
            return


def tick_email_consent(page):
    try:
        result = page.evaluate(TICK_EMAIL_JS)
        if result == "clicked":
            page.wait_for_timeout(300)
    except Exception:
        pass


def click_button_js(page, text):
    """Click a button by its visible text via JS. No focus, no mouse move."""
    try:
        return page.evaluate(CLICK_BUTTON_JS, text)
    except Exception:
        return False


def load_and_prepare(page, url):
    for attempt in range(3):
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(1800)
        dismiss_blockers(page)
        page.wait_for_timeout(800)
        try:
            items = page.locator('[role="listitem"]').count()
        except Exception:
            items = 0
        if items > 0:
            tick_email_consent(page)
            return True
        page.wait_for_timeout(1500)
    tick_email_consent(page)
    return False


# ----------------------------------------------------------------------
# Data helpers
# ----------------------------------------------------------------------
def load_rows(file, sheet, start, limit):
    df = pd.read_excel(file, sheet_name=sheet, dtype=str,
                       keep_default_na=False, na_values=[])
    df = df[df.apply(lambda r: r.str.strip().ne("").any(), axis=1)]
    end = None if limit is None else start + limit
    return df.iloc[start:end]


def read_log():
    if not Path(LOG_FILE).exists():
        return {}
    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        return {(r["sheet"], int(r["row"])): r["status"]
                for r in csv.DictReader(f)}


def write_log(sheet, row, status):
    new = not Path(LOG_FILE).exists()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["sheet", "row", "status", "time"])
        w.writerow([sheet, row, status,
                    datetime.now().isoformat(timespec="seconds")])


# ----------------------------------------------------------------------
# Pre-flight
# ----------------------------------------------------------------------
def preflight_signin(page, form_url):
    print()
    print("=" * 64)
    print("  Opening the form...")
    print("=" * 64)

    load_and_prepare(page, form_url)

    print()
    print("  Chrome is open. Before continuing, make sure that:")
    print("    1. You are signed in with the Google account you want to use.")
    print("    2. You can see the form's title and questions —")
    print("       NOT a 'Sign in' popup or 'You need permission' message.")
    print("    3. Any 'Continue current draft?' popup has been dismissed.")
    print()
    print("  If you need to switch accounts:")
    print("    • Click the account icon (top-right of the form)")
    print("    • Choose 'Add another account' or 'Switch account'")
    print("    • Sign in and finish any 2FA")
    print("    • Wait for the form to come back")
    print()
    input("  Press Enter here when the form is ready... ")

    load_and_prepare(page, form_url)
    print("✓ Starting submissions.\n")


# ----------------------------------------------------------------------
# Failure diagnostics
# ----------------------------------------------------------------------
def dump_failure(page, idx):
    shot = f"failure_row_{idx}.png"
    html_file = f"failure_row_{idx}.html"
    try:
        page.screenshot(path=shot, full_page=True)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(page.content())
        print(f"   -> saved {shot} and {html_file}")
    except Exception:
        pass


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------
def cmd_links(args):
    rows = load_rows(args.file, args.sheet, args.start, args.limit)
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        for _, row in rows.iterrows():
            f.write(build_link(row) + "\n")
    print(f"Wrote {len(rows)} links to {LINKS_FILE}")


def cmd_submit(args):
    from playwright.sync_api import sync_playwright
    from browser_launch import launch

    rows = load_rows(args.file, args.sheet, args.start, args.limit)
    done = read_log()

    with sync_playwright() as p:
        ctx = launch(p, PROFILE_DIR)
        page = ctx.new_page()

        preflight_signin(page, CFG.FORM_URL_BASE)

        first_row = True
        for idx, row in rows.iterrows():
            if done.get((args.sheet, idx)) == "OK":
                print(f"Row {idx}: already submitted, skipping")
                continue

            if not first_row:
                human_delay(args.delay_min, args.delay_max)
            first_row = False

            load_and_prepare(page, build_link(row))

            status = "FAILED"
            for _ in range(20):
                page.wait_for_timeout(1000)

                if page.get_by_text("Your response has been recorded").count():
                    status = "OK"
                    break

                dismiss_blockers(page)
                tick_email_consent(page)

                submit = page.get_by_role("button", name="Submit", exact=True)
                nxt = page.get_by_role("button", name="Next", exact=True)

                if submit.count():
                    if args.review:
                        input(f"Row {idx}: check the form, "
                              "press Enter to SUBMIT... ")
                    click_button_js(page, "Submit")
                    page.wait_for_timeout(1200)
                elif nxt.count():
                    click_button_js(page, "Next")
                    page.wait_for_timeout(1200)
                else:
                    page.wait_for_timeout(1500)
                    submit = page.get_by_role("button", name="Submit", exact=True)
                    nxt = page.get_by_role("button", name="Next", exact=True)
                    if not (submit.count() or nxt.count()):
                        break

            write_log(args.sheet, idx, status)
            print(f"Row {idx}: {status}")
            if status != "OK":
                dump_failure(page, idx)
                print("   -> A required field is empty, or an answer "
                      "doesn't match a form option.")
                if args.stop_on_fail:
                    print("   --stop-on-fail set — stopping here.")
                    break

        ctx.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["links", "submit"])
    ap.add_argument("--config", default="form_config")
    ap.add_argument("--file", default="synthetic_responses.xlsx")
    ap.add_argument("--sheet", default="Responses")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--review", action="store_true",
                    help="pause before each Submit")
    ap.add_argument("--stop-on-fail", action="store_true",
                    help="stop the batch as soon as a row fails")
    ap.add_argument("--delay-min", type=int, default=150,
                    help="minimum seconds between submissions (default 150 = 2m30s)")
    ap.add_argument("--delay-max", type=int, default=180,
                    help="maximum seconds between submissions (default 180 = 3m)")
    a = ap.parse_args()
    CFG = importlib.import_module(a.config)
    cmd_links(a) if a.mode == "links" else cmd_submit(a)