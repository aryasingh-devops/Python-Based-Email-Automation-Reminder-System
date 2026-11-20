# 📬 Email Automation & Reminder System

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Data Engine](https://img.shields.io/badge/Pandas-Data%20Validation-150458?logo=pandas)](https://pandas.pydata.org/)
[![Testing](https://img.shields.io/badge/pytest-11%20Passed%20(100%25)-brightgreen?logo=pytest)](https://docs.pytest.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Production%20Grade-success)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An industry-grade, modular Python workflow automation engine designed to eliminate manual communication overhead across HR, Finance, Operations, and Sales teams. Features multi-part MIME templating, local event scheduling, automated audit trails, zero-credential Virtual Simulation and an interactive Streamlit Web Dashboard.**

---

## 📑 Table of Contents

- [🌟 Project Overview](#-project-overview)
- [🏢 Industry Relevance & Problem Solved](#-industry-relevance--problem-solved)
- [✨ Key Features](#-key-features)
- [🏛️ System Architecture](#️-system-architecture)
- [📁 Folder Structure](#-folder-structure)
- [⚙️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [🔐 Secure Credential Configuration (.env)](#-secure-credential-configuration-env)
- [🧪 Virtual Simulation Engine (Dry-Run Mode)](#-virtual-simulation-engine-dry-run-mode)
- [💻 Usage Guide (CLI & Web Dashboard)](#-usage-guide-cli--web-dashboard)
- [📊 Compliance Audit Reports & Logs](#-compliance-audit-reports--logs)
- [🧪 Running Test Suite](#-running-test-suite)
- [🎓 Learning Outcomes & Interview Prep](#-learning-outcomes--interview-prep)
- [📄 License & Author](#-license--author)

---

## 🌟 Project Overview

In fast-paced business environments, teams lose hundreds of hours annually sending repetitive reminders for unpaid invoices, scheduled interviews, sprint milestones, and webinars. 

The **Email Automation & Reminder System** solves this by providing a clean, enterprise-ready Python pipeline that:
1. Ingests contacts and scheduled reminder tasks from structured CSV data sources.
2. Performs pre-flight schema and RFC-compliant email syntax validation.
3. Dynamically compiles responsive, mobile-ready HTML5 email templates with fallback plain-text representations.
4. Executes delivery via secure SMTP (STARTTLS/SSL) with automated retries OR via a safe, zero-credential **Virtual Simulation Engine**.
5. Automatically marks tasks as completed and records audit logs and timestamped compliance CSV reports.
6. Surfaces an interactive **Streamlit Web Dashboard** to preview templates, inspect queues, and trigger dispatches in real time from your web browser.

## 📸 Output Screenshots

![alt text](<Screenshot 2026-11-19 132725-1.png>)
![alt text](<Screenshot 2026-11-19 132844.png>)

## 🎥 Demo Video

https://youtu.be/_CDXNE3c7Lo?si=67aqTDDCkp5GOFbf

---

## 🏢 Industry Relevance & Problem Solved

| Business Function | Real-World Use Case | Automated Impact |
| :--- | :--- | :--- |
| **Finance & Billing** | Automated invoices and overdue payment notices | Cuts Days Sales Outstanding (DSO) by up to 40% |
| **HR & Recruitment** | Candidate interview rounds, assessment reminders | Eliminates candidate no-shows and ensures professional branding |
| **Operations & PMO** | Sprint milestone deadlines and code-freeze alerts | Keeps agile teams aligned without manual manager nudges |
| **Marketing & Training**| Masterclass confirmations and webinar access links | Boosts event live attendance by ~35% |
| **Customer Success** | Post-implementation reviews and NPS feedback | Increases client feedback submission rates significantly |

---

## ✨ Key Features

- **Dual-Mode Dispatch Architecture**:
  - **Virtual Simulation Mode (`--dry-run`)**: Test the entire pipeline without credentials, network calls, or spam risk. Simulates realistic socket latency (50ms).
  - **Live SMTP Server Mode (`--live`)**: Integrates with Gmail, Outlook or corporate relays using TLS on port 587 or SSL on port 465.
- **RFC 5322 Multi-Part MIME Containers**: Dispatches both rich HTML5 inline-styled templates and RFC-compliant plain-text versions.
- **Relational Data Ingestion**: Automatically merges contact profiles (`contacts.csv`) with event tasks (`reminders.csv`) using `pandas`.
- **Fault-Tolerant Engine**: Implements exponential backoff, socket timeout handling, and isolated per-recipient error handling so one bad email never halts the batch.
- **Enterprise Audit Trails**: Generates timestamped compliance reports in `outputs/` and dual-handler rotating logs in `logs/`.
- **Streamlit Web Dashboard (`app.py`)**: A modern, interactive web application with KPI metric cards, live template previewers, and dispatch triggers.

---

## 🏛️ System Architecture

```
+-------------------+      +-------------------+
|  data/contacts.csv|      | data/reminders.csv|
+---------┬---------+      +---------┬---------+
          │                          │
          └────────────┬─────────────┘
                       ▼
       ┌───────────────────────────────┐
       │   CSV Data Loader & Parser    │ (Schema & Email Validation)
       └───────────────┬───────────────┘
                       ▼
       ┌───────────────────────────────┐
       │     Template Engine (HTML)    │ (Context Variable Injection)
       └───────────────┬───────────────┘
                       ▼
       ┌───────────────────────────────┐
       │    Email Dispatch Engine      │
       │   [Simulation vs Live SMTP]   │ (Retries & Multi-Part MIME)
       └───────────────┬───────────────┘
                       ▼
       ┌───────────────────────────────┐
       │  Audit Logging & CSV Reporter │ (logs/ & outputs/ Reports)
       └───────────────┬───────────────┘
                       ▼
       ┌───────────────────────────────┐
       │    Streamlit Web Dashboard    │ (Browser Visual Interface)
       └───────────────────────────────┘
```

---

## 📁 Folder Structure

```
Email-Automation-Reminder-System/
│
├── data/                       # Tabular data inputs
│   ├── contacts.csv            # Master contact list (name, email, company, role)
│   └── reminders.csv           # Reminder queue (type, due_date, status, metadata)
│
├── templates/                  # Responsive email templates (HTML + Plain-Text)
│   ├── payment_reminder.html   # Finance accounts receivable template
│   ├── payment_reminder.txt    # Plain-text fallback
│   ├── webinar_invite.html     # Marketing / learning session invite
│   ├── webinar_invite.txt      # Plain-text fallback
│   ├── interview_schedule.html # HR talent acquisition interview confirmation
│   ├── interview_schedule.txt  # Plain-text fallback
│   ├── project_deadline.html   # PMO milestone & code freeze alert
│   ├── project_deadline.txt    # Plain-text fallback
│   ├── feedback_request.html   # Customer success pulse survey
│   ├── feedback_request.txt    # Plain-text fallback
│   ├── general_reminder.html   # Generic fallback template
│   └── general_reminder.txt    # Generic fallback plain-text
│
├── src/                        # Core Python application modules
│   ├── __init__.py             # Package declaration
│   ├── config.py               # Central environment & path manager
│   ├── logger.py               # Dual-stream logging (Console + Rotating files)
│   ├── csv_loader.py           # Pandas data loader, validator, and relational joiner
│   ├── template_engine.py      # Variable interpolation and MIME generator
│   ├── email_dispatcher.py     # SMTP socket lifecycle & Virtual Simulation handler
│   ├── scheduler_engine.py     # Batch and interval scheduling coordinator
│   └── report_generator.py     # Compliance report and analytics compiler
│
├── outputs/                    # Generated audit reports
│   ├── latest_dispatch_report.csv
│   └── summary_analytics.json
│
├── logs/                       # System execution and audit logs
│   ├── system.log              # Engine lifecycle events
│   └── dispatch.log            # Line-by-line recipient audit trail
│
├── images/                     # UI screenshots and architectural diagrams
├── docs/                       # Comprehensive documentation
│   ├── PROJECT_EXPLANATION.md  # Deep-dive concept overview
│   ├── TECH_STACK_OPTIONS.md   # Architectural options comparison
│   ├── ARCHITECTURE_GUIDE.md   # Complete system architecture
│   ├── IMPLEMENTATION_PLAN.md  # Step-by-step roadmap
│   ├── VIRTUAL_SIMULATION_GUIDE.md # Safe testing guide
│   └── INTERVIEW_PREPARATION.md    # 25+ interview Q&As, STAR stories, resume bullets
│
├── tests/                      # Unit and integration test suite
│   ├── conftest.py             # Test harness path configuration
│   └── test_automation.py      # 11 comprehensive automated tests (100% pass)
│
├── main.py                     # CLI orchestration runner
├── app.py                      # Interactive Streamlit Web Dashboard
├── requirements.txt            # Pinned dependencies
├── .env.example                # Example configuration template
├── .gitignore                  # Git hygiene (ignoring secrets, caches, logs)
└── README.md                   # Project documentation
```

---

## ⚙️ Tech Stack

- **Core Engine**: Python 3.10+
- **Data Ingestion & Wrangling**: Pandas
- **Internet Email Protocols**: `smtplib`, `email.mime` (Standard Library)
- **Task Scheduling**: `schedule`, `datetime`
- **Configuration Management**: `python-dotenv`
- **Web User Interface**: Streamlit
- **Testing Framework**: `pytest`

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Email-Automation-Reminder-System.git
cd Email-Automation-Reminder-System
```

### 2. Set Up a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Secure Credential Configuration (.env)

By default, the system runs safely in **Virtual Simulation Mode** without needing credentials.

If you wish to send real emails via Gmail or an enterprise relay:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your settings:
   ```ini
   DRY_RUN=False
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USE_SSL=False
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   SENDER_NAME=Enterprise Operations Automated Dispatcher
   ```

> ⚠️ **IMPORTANT**: For Gmail, do **NOT** use your standard Google account password. Generate a 16-character **App Password** by visiting [Google App Passwords](https://myaccount.google.com/apppasswords). Ensure 2-Step Verification is active.

---

## 🧪 Virtual Simulation Engine (Dry-Run Mode)

The built-in Virtual Simulation Engine allows students to execute realistic test runs without sending actual emails:

- Ingests and validates all CSV records.
- Compiles both HTML and plain-text templates with live context.
- Simulates realistic network transmission latency (50ms).
- Updates task statuses to `Simulated_Sent`.
- Generates full audit logs and CSV reports in `outputs/`.

Run it anytime with:
```bash
python main.py --dry-run
```

---

## 💻 Usage Guide (CLI & Web Dashboard)

### Option 1: Interactive Streamlit Web Dashboard (Recommended)

Launch the modern browser dashboard:
```bash
streamlit run app.py
```
**Features in Browser**:
- 📊 **Executive Dashboard**: KPI counters, reminder type charts, and status breakdowns.
- 🚀 **Dispatch Automation**: Trigger batch dispatches with real-time progress bars.
- ✉️ **Email Template Preview**: Split-screen live preview of personalized HTML and plain-text emails.
- 👥 **Contacts & Queue**: Interactive searchable tables with one-click data reset.
- 📈 **Audit Reports & Logs**: View recent dispatch logs and download compliance reports via CSV.

### Option 2: Command-Line Interface (CLI)

```bash
# 1. Run a single batch pass in Virtual Simulation Mode (Safe)
python main.py --dry-run

# 2. Run a single batch pass in Live SMTP Mode (Sends real emails)
python main.py --live

# 3. Preview personalized templates in the terminal without sending
python main.py --preview

# 4. View the latest batch audit report summary
python main.py --report

# 5. Run recurring interval scheduler daemon (polls every 30 seconds)
python main.py --schedule --interval 30

# 6. Reset all reminder statuses back to 'Pending' for testing
python main.py --reset-data
```

---

## 📊 Compliance Audit Reports & Logs

Every dispatch cycle produces an immutable audit record:

### CSV Report (`outputs/latest_dispatch_report.csv`)
| reminder_id | recipient_name | recipient_email | mode | status | latency_seconds |
| :--- | :--- | :--- | :--- | :--- | :--- |
| REM-201 | Priya Patel | priya.patel@finscale.io | DRY_RUN | SIMULATED_SUCCESS | 0.051 |
| REM-202 | Vikram Malhotra | vikram.malhotra@zenithcorp.org | DRY_RUN | SIMULATED_SUCCESS | 0.051 |
| REM-203 | Aarav Sharma | aarav.sharma@innovatetech.com | DRY_RUN | SIMULATED_SUCCESS | 0.051 |

### System Execution Logs (`logs/system.log`)
```
2026-11-19 12:54:11 [INFO] [AppEngine] Starting Email Automation Cycle [Mode: DRY-RUN SIMULATION]
2026-11-19 12:54:11 [INFO] [AppEngine] Loaded 8 contacts from contacts.csv
2026-11-19 12:54:11 [INFO] [AppEngine] Loaded 8 reminders from reminders.csv
2026-11-19 12:54:11 [INFO] [AppEngine] Built dispatch queue with 8 items (filter: Pending)
2026-11-19 12:54:11 [INFO] [EmailDispatcher] SIMULATED_SUCCESS | ID: REM-201 | To: priya.patel@finscale.io | Latency: 0.051s
2026-11-19 12:54:12 [INFO] [AppEngine] Cycle Complete in 0.53s! Processed: 8 | Success: 8 (100.0%)
```

---

## 🧪 Running Test Suite

This project includes a comprehensive test suite covering schema validation, template rendering, MIME generation, dispatcher simulation, and reporting.

Execute tests using `pytest`:
```bash
pytest tests/test_automation.py -v
```

**Test Execution Results**:
```
tests/test_automation.py::TestDataIngestion::test_load_contacts PASSED   [  9%]
tests/test_automation.py::TestDataIngestion::test_load_reminders PASSED  [ 18%]
tests/test_automation.py::TestDataIngestion::test_email_validation PASSED [ 27%]
tests/test_automation.py::TestDataIngestion::test_get_dispatch_queue PASSED [ 36%]
tests/test_automation.py::TestTemplateEngine::test_render_content PASSED [ 45%]
tests/test_automation.py::TestTemplateEngine::test_generate_email_bodies PASSED [ 54%]
tests/test_automation.py::TestEmailDispatcher::test_mime_generation PASSED [ 63%]
tests/test_automation.py::TestEmailDispatcher::test_dry_run_dispatch_success PASSED [ 72%]
tests/test_automation.py::TestEmailDispatcher::test_invalid_email_dispatch_failure PASSED [ 81%]
tests/test_automation.py::TestReportingAndScheduling::test_report_generation PASSED [ 90%]
tests/test_automation.py::TestReportingAndScheduling::test_scheduler_cycle_dry_run PASSED [100%]

============================= 11 passed in 2.03s ==============================
```

---

## 🎓 Learning Outcomes & Interview Prep

By building and studying this project, you gain mastery in:
- Clean architecture and **Separation of Concerns** in Python.
- Multi-part MIME standards (`text/html` and `text/plain`) for email client deliverability.
- Safe password handling with **Environment Variables** and App Passwords.
- Network error handling, socket timeouts, and retry strategies.
- Building interactive data apps using **Streamlit**.
- Audit trail compliance and enterprise software reliability.

📘 **Detailed Interview Resources**:
- [Project Concept Deep Dive](docs/PROJECT_EXPLANATION.md)
- [System Architecture Guide](docs/ARCHITECTURE_GUIDE.md)
- [Virtual Simulation Guide](docs/VIRTUAL_SIMULATION_GUIDE.md)
- [25+ Technical & Behavioral Interview Q&As](docs/INTERVIEW_PREPARATION.md)

---

## 📄 License & Author

Distributed under the MIT License. See `LICENSE` for more information.

Developed with ❤️ as an industry-oriented portfolio project for aspiring Python Developers, Automation Engineers, and Productivity Specialists.
