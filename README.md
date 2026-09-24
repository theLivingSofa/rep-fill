# Google Forms Auto-Filler

Automatically fills and submits our Google Forms surveys. You put the answers in an Excel file, run one command, and the tool types them in for you — one by one, with human-like delays so nothing looks suspicious.

Each form (theme) already has **300 pre-generated responses** ready to go. You just need to install the tool and run it.

---

## ⚡ Quick Version (if you know what you're doing)

```bash
pip install -r requirements.txt
playwright install
cd forms/theme5
python3 ../../qol_submitter.py submit --config form_config \
    --file synthetic_responses.xlsx --sheet Responses \
    --start 0 --limit 10 --review --delay-min 10 --delay-max 20
```

---

## 📋 Full Setup Guide (Step by Step)

### What You Need

- **Google Chrome** — [download here](https://www.google.com/chrome/) if you don't have it
- **Python** — we'll install this below
- **This project** — download it from GitHub

---

### Step 1: Install Python

<details>
<summary><b>🍎 Mac</b></summary>

1. Go to https://www.python.org/downloads/
2. Click the big yellow **"Download Python 3.x.x"** button
3. Open the downloaded `.pkg` file
4. Click **Continue → Continue → Agree → Install** (just keep clicking through)
5. Enter your Mac password when asked
6. Done!

**To verify:** Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter) and type:
```
python3 --version
```
You should see something like `Python 3.12.x` or higher.

</details>

<details>
<summary><b>🪟 Windows</b></summary>

1. Go to https://www.python.org/downloads/
2. Click the big yellow **"Download Python 3.x.x"** button
3. Open the downloaded `.exe` file
4. **⚠️ IMPORTANT: Check the box that says "Add Python to PATH" at the bottom of the installer**
5. Click **Install Now**
6. Click through until it says "Setup was successful"
7. Done!

**To verify:** Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and type:
```
python --version
```
You should see something like `Python 3.12.x` or higher.

</details>

---

### Step 2: Download This Project

**Option A — Download as ZIP (easiest):**
1. On this GitHub page, click the green **"< > Code"** button
2. Click **"Download ZIP"**
3. Extract/unzip the downloaded file
4. Remember where you extracted it (e.g., your Desktop or Downloads folder)

**Option B — Git clone (if you have git):**
```
git clone <this-repo-url>
```

---

### Step 3: Open Terminal / Command Prompt in the Project Folder

<details>
<summary><b>🍎 Mac</b></summary>

1. Open **Finder** and navigate to the extracted `formfill` folder
2. Right-click the folder → **Services → New Terminal at Folder**

**OR** open Terminal and type:
```bash
cd ~/Desktop/formfill
```
(Change the path to wherever you extracted the project)

</details>

<details>
<summary><b>🪟 Windows</b></summary>

1. Open **File Explorer** and navigate to the extracted `formfill` folder
2. Click on the **address bar** at the top (where it shows the folder path)
3. Type `cmd` and press **Enter** — this opens Command Prompt right in that folder

**OR** open Command Prompt and type:
```cmd
cd %USERPROFILE%\Desktop\formfill
```
(Change the path to wherever you extracted the project)

</details>

---

### Step 4: Install Dependencies (One Time Only)

Run these commands one at a time. Copy-paste each line, press Enter, and wait for it to finish before running the next one.

<details>
<summary><b>🍎 Mac</b></summary>

```bash
pip3 install -r requirements.txt
```
```bash
python3 -m playwright install
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
pip install -r requirements.txt
```
```cmd
python -m playwright install
```

</details>

The second command downloads browser drivers (~200 MB). This is normal — just wait for it to finish.

---

## 🚀 How to Submit Responses

### Step 1: Navigate to the Form You Want to Fill

Each form is in its own folder inside `forms/`. Pick the one you need:

| Folder | Survey Topic |
|--------|-------------|
| `forms/theme1` | QoL / Quality of Life survey |
| `forms/theme3` | Child welfare & education survey |
| `forms/theme4` | QoL survey (alternate) |
| `forms/theme5` | Kirana stores & quick-commerce impact |

**Mac:**
```bash
cd forms/theme5
```

**Windows:**
```cmd
cd forms\theme5
```

(Replace `theme5` with whichever form you need)

---

### Step 2: Do a Test Run First (Recommended)

This submits just **3 responses** with a **pause before each submit** so you can verify everything looks right:

**Mac:**
```bash
python3 ../../qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --limit 3 --review --delay-min 10 --delay-max 20
```

**Windows:**
```cmd
python ..\..\qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --limit 3 --review --delay-min 10 --delay-max 20
```

**What happens:**
1. A Chrome window opens with the form
2. The terminal says *"Press Enter when the form is ready..."*
3. **Sign in to your Google account** in that Chrome window if needed
4. Come back to the terminal and **press Enter**
5. The tool fills in the first response — it pauses and says *"Press Enter to SUBMIT"*
6. Check the form looks correct in Chrome, then **press Enter** in the terminal to submit
7. Repeat for each row

---

### Step 3: Full Auto-Submit (Hands-Off)

Once you've verified the test run works, submit all 300 responses automatically:

**Mac:**
```bash
python3 ../../qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --stop-on-fail
```

**Windows:**
```cmd
python ..\..\qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --stop-on-fail
```

> **Note:** This takes a while! The tool waits **2.5–3 minutes between each submission** on purpose so they don't look automated. 300 responses ≈ 12–15 hours. You can leave your laptop running overnight.

> **Safe to restart:** If your laptop sleeps or you close the terminal, just run the same command again. It automatically skips rows that were already submitted.

---

### Step 4: Submit a Specific Range of Rows

If you want to split the work with someone else, use `--start` and `--limit`:

**Person A — rows 0 to 99:**

Mac:
```bash
python3 ../../qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --limit 100 --stop-on-fail
```
Windows:
```cmd
python ..\..\qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 0 --limit 100 --stop-on-fail
```

**Person B — rows 100 to 199:**

Mac:
```bash
python3 ../../qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 100 --limit 100 --stop-on-fail
```
Windows:
```cmd
python ..\..\qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 100 --limit 100 --stop-on-fail
```

**Person C — rows 200 to 299:**

Mac:
```bash
python3 ../../qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 200 --limit 100 --stop-on-fail
```
Windows:
```cmd
python ..\..\qol_submitter.py submit --config form_config --file synthetic_responses.xlsx --sheet Responses --start 200 --limit 100 --stop-on-fail
```

---

## ⚙️ Options Reference

| Flag | What it does | Default |
|------|-------------|---------|
| `--start N` | Start from row N (0 = first row) | `0` |
| `--limit N` | Only submit N rows | all rows |
| `--review` | Pause before each Submit so you can check | off |
| `--stop-on-fail` | Stop immediately if a row fails | off (continues to next row) |
| `--delay-min N` | Minimum seconds to wait between submissions | `150` (2 min 30 sec) |
| `--delay-max N` | Maximum seconds to wait between submissions | `180` (3 min) |

---

## 🔧 Troubleshooting

### "python3 is not recognized" (Windows)
Use `python` instead of `python3` in all commands. Windows uses `python`.

### "pip3 is not recognized" (Windows)
Use `pip` instead of `pip3`. Or try `python -m pip install -r requirements.txt`.

### The Chrome window opens but shows "You need permission"
The form requires a specific Google account. Sign in with the correct account in the Chrome window that opened.

### "Sign in to Google" loop
Delete the `chrome_profile` folder inside the theme directory and run the command again:

Mac: `rm -rf chrome_profile`

Windows: `rmdir /s /q chrome_profile`

### A row shows "FAILED"
The tool saves a screenshot (`failure_row_N.png`) so you can see what went wrong. Usually it means an answer didn't match the form's options exactly. The tool skips failed rows and continues.

### "No module named 'playwright'" or similar
You skipped the dependency install step. Go back to **Step 4** of the setup.

### My laptop went to sleep / I closed the terminal
Just run the same command again. It reads `submission_log.csv` to know which rows are already done and skips them.

### I want to re-submit rows that were already submitted
Delete the `submission_log.csv` file in the theme folder, then run again.

---

## 📂 Project Structure

```
formfill/
├── README.md                  ← you are here
├── requirements.txt           ← Python dependencies
├── browser_launch.py          ← Chrome launcher (shared)
├── dump_form.py               ← scans a Google Form to create form_config.py
├── qol_submitter.py           ← the main submitter tool
├── check_semantics.py         ← data validation helper
├── generate_synthetic_data.py ← generates synthetic responses
└── forms/
    ├── theme1/
    │   ├── form_config.py              ← form structure (auto-generated)
    │   ├── responses_template.xlsx     ← blank template
    │   └── synthetic_responses.xlsx    ← 300 pre-filled responses
    ├── theme3/
    │   ├── form_config.py
    │   ├── generate_synthetic_data.py  ← theme-specific generator
    │   ├── responses_template.xlsx
    │   └── synthetic_responses.xlsx
    ├── theme4/
    │   ├── form_config.py
    │   ├── responses_template.xlsx
    │   └── synthetic_responses.xlsx
    └── theme5/
        ├── form_config.py
        ├── responses_template.xlsx
        └── synthetic_responses.xlsx
```
