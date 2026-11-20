# 3️⃣ Project Architecture & Data Flow Guide

---

## 🏛️ High-Level System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  INPUT SOURCES                                    |
|   +--------------------------+                     +--------------------------+   |
|   |   data/contacts.csv      |                     |   data/reminders.csv     |   |
|   |  - contact_id (PK)       |                     |  - reminder_id (PK)      |   |
|   |  - name, email, company  |                     |  - contact_id (FK)       |   |
|   |  - role, phone, status   |                     |  - type, due_date, status|   |
|   +--------------------------+                     +--------------------------+   |
+-----------------------------------------┬-----------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                           INGESTION & VALIDATION LAYER                            |
|                            [ src/csv_loader.py ]                                  |
|   - Strip whitespace & cleanse fields                                             |
|   - Regex syntax verification on email addresses                                  |
|   - Relational merge on 'contact_id' -> Unified Dispatch Task Queue               |
+-----------------------------------------┬-----------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                           PRESENTATION & TEMPLATE ENGINE                          |
|                         [ src/template_engine.py ]                                |
|   - Load HTML templates (templates/*.html) with inline CSS styling               |
|   - Load RFC fallback text templates (templates/*.txt)                            |
|   - Variable interpolation: {{ name }}, {{ amount_due }}, {{ due_date }}, etc.    |
|   - Build dual-part RFC 5322 MIME Container (MIMEMultipart "alternative")         |
+-----------------------------------------┬-----------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                          CORE DISPATCH & TRANSPORT ENGINE                         |
|                         [ src/email_dispatcher.py ]                               |
|                                                                                   |
|            +-----------------------------------------------------+                |
|            |            Operational Mode Controller              |                |
|            +--------------------------┬--------------------------+                |
|                                       │                                           |
|                  ┌────────────────────┴────────────────────┐                      |
|                  ▼                                         ▼                      |
|       [ Virtual Simulation Mode ]               [ Live SMTP Mode ]                |
|       - Dry-run validation                      - STARTTLS on Port 587 / SSL 465  |
|       - Realistic latency simulation (50ms)     - App Password Authentication     |
|       - Zero credentials required               - Exponential Backoff & Retry     |
|       - 100% safe for classroom & portfolio     - smtplib.send_message()          |
+-----------------------------------------┬-----------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                          AUDIT, LOGGING & REPORTING LAYER                         |
|   +------------------------------------+   +----------------------------------+   |
|   |         Logging Subsystem          |   |       Compliance Reporting       |   |
|   |        [ src/logger.py ]           |   |    [ src/report_generator.py ]   |   |
|   |  - logs/system.log (execution)     |   |  - outputs/dispatch_report_*.csv |   |
|   |  - logs/dispatch.log (audit trail) |   |  - outputs/summary_analytics.json|   |
|   |  - Console formatted output        |   |  - Success rate & avg latency    |   |
|   +------------------------------------+   +----------------------------------+   |
+-----------------------------------------┬-----------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                             USER INTERACTION CHANNELS                             |
|          +----------------------------+    +----------------------------+         |
|          |    CLI Automation Runner   |    |   Streamlit Web Dashboard  |         |
|          |        [ main.py ]         |    |         [ app.py ]         |         |
|          |  - Flags: --dry-run, --once|    |  - Real-time KPI metrics   |         |
|          |  - Interval scheduler daemon|   |  - Live email previewer    |         |
|          |  - Template preview & reset|    |  - One-click batch triggers|         |
|          +----------------------------+    +----------------------------+         |
+-----------------------------------------------------------------------------------+
```

---

## 🔀 Step-by-Step Data Flow

1. **Extraction**: `CSVLoader` reads `contacts.csv` and `reminders.csv` into Pandas DataFrames.
2. **Schema & Integrity Check**: Verifies that required primary and foreign keys exist. Rows with missing vital contact emails are flagged.
3. **Queue Construction**: An `inner join` matches each pending reminder with recipient demographic information.
4. **MIME Compilation**: For each queue item, `TemplateEngine` renders both HTML and Plain-Text representations and binds them inside an RFC 5322 MIME container.
5. **Transport Execution**:
   - In **Live Mode**: Initiates secure socket handshake with Gmail/Outlook, authenticates, and dispatches.
   - In **Dry-Run Mode**: Simulates socket transfer, validates payload compliance, and logs mock delivery.
6. **State Persistence**: The reminder's status is toggled from `Pending` to `Sent` (or `Simulated_Sent` or `Failed`) and saved back to `reminders.csv`.
7. **Compliance Archiving**: `ReportGenerator` calculates key performance indicators (KPIs) and writes a timestamped CSV report to `outputs/`.
8. **Visualization**: Streamlit reflects updated metrics, status distributions, and logs in the web interface.
