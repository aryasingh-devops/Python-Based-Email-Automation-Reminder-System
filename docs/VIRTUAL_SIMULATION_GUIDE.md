# 8️⃣ Virtual Simulation Guide: Testing Safely Without Real SMTP

---

## 💡 Why Virtual Simulation is Essential for Students & Portfolios

Most students face two major obstacles when working on automation projects:
1. **Lack of Enterprise Mail Relays**: Companies use dedicated servers (SendGrid, Mailgun, Amazon SES). Students only have personal Gmail or Outlook accounts.
2. **Account Blocking & Spam Risks**: Testing email loops with personal Gmail accounts can trigger Google's automated anti-abuse algorithms, locking personal accounts.

To solve this, this project includes a built-in **Virtual Simulation Engine (`--dry-run`)**.

---

## 🛡️ How the Virtual Simulation Engine Works

When running in **Simulation Mode** (enabled by default when credentials are absent or via `--dry-run`):

1. **Full Ingestion**: Loads real CSV data, parses dates, verifies email syntax.
2. **Full Compilation**: Assembles real HTML and Plain-Text templates and injects recipient variables.
3. **MIME RFC 5322 Packaging**: Assembles the exact headers (`Message-ID`, `X-Priority`, `To`, `From`, `Date`).
4. **Simulated Latency**: Adds realistic network transmission delay (30-60ms) to mirror physical TCP socket handshakes.
5. **Real State Tracking**: Marks the reminder as `Simulated_Sent` in `reminders.csv`.
6. **Full Audit Generation**: Writes genuine timestamped CSV reports into `outputs/` and logs into `logs/`.

> **Result**: You can demo and test the entire project thousands of times with **zero credentials, zero cost, and zero risk**!

---

## 📸 Recommended Artifacts & Screenshots to Capture for GitHub

When showcasing this project on your GitHub repository or LinkedIn:

1. **Terminal Batch Run Screenshot**:
   - Run `python main.py --dry-run`
   - Capture the ASCII banner, processing logs, and batch summary table.
2. **Streamlit Executive Dashboard Screenshot**:
   - Run `streamlit run app.py`
   - Capture the top metric KPI cards and the Reminder Category distribution chart.
3. **Email Template Live Preview Screenshot**:
   - On the Streamlit UI, navigate to the **Email Template Preview** tab.
   - Capture the split-view showing the rendered HTML email alongside the plain-text fallback.
4. **Audit Report CSV Preview**:
   - Open `outputs/latest_dispatch_report.csv` in Excel or VS Code table view.
   - Show how enterprise compliance teams inspect timestamps, status, and latency.

---

## 🚨 Security Rules: What NEVER to Upload to GitHub

> [!CAUTION]
> Committing credentials to a public GitHub repo is detected by automated scanners within seconds and will compromise your account!

- ❌ **NEVER commit `.env`**: Make sure `.env` is listed in `.gitignore`. Only commit `.env.example`.
- ❌ **NEVER commit real Gmail / Outlook passwords or App Passwords**.
- ❌ **NEVER commit confidential company contact emails**. Always use synthetic dummy data (e.g., `@example.com`, `@innovatetech.com`).
- ✅ **DO commit**:
  - Sample dummy CSVs (`data/contacts.csv`, `data/reminders.csv`)
  - All HTML & Plain-Text templates (`templates/*.html`, `templates/*.txt`)
  - Full modular Python code (`src/`, `main.py`, `app.py`)
  - Sample generated audit reports (`outputs/latest_dispatch_report.csv`)
  - Project documentation & screenshots in `images/`
