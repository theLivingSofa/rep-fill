"""
Shared Chrome launcher that hides automation fingerprints so Google
lets you sign in. Imported by dump_form.py and qol_submitter.py.
"""
import time

STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-infobars",
    "--disable-features=IsolateOrigins,site-per-process",
]

REAL_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def launch(p, profile_dir="chrome_profile", headless=False):
    """Launch Chrome with anti-detection settings."""
    ctx = p.chromium.launch_persistent_context(
        profile_dir,
        channel="chrome",
        headless=headless,
        args=STEALTH_ARGS,
        ignore_default_args=["--enable-automation"],
        user_agent=REAL_USER_AGENT,
        viewport={"width": 1280, "height": 850},
        locale="en-IN",
    )
    ctx.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
    )
    return ctx


def wait_for_login(page, form_url, timeout_seconds=600):
    """
    Wait until the user finishes signing in to Google.
    Google redirects back to the form automatically, so we just poll the URL.
    """
    start = time.time()
    while "accounts.google.com" in page.url:
        if time.time() - start > timeout_seconds:
            raise RuntimeError(
                f"Timed out after {timeout_seconds}s waiting for Google sign-in. "
                "Try deleting the chrome_profile folder and running again."
            )
        page.wait_for_timeout(2000)
    page.wait_for_load_state("domcontentloaded")
    if form_url not in page.url:
        page.goto(form_url)
        page.wait_for_load_state("domcontentloaded")